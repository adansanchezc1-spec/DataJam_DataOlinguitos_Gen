"""Orquestación de la exploración dataset por dataset para los notebooks EDA.

`explorar_dataset` recibe una especificación del dataset (origen, corte,
valor público, indicadores) y produce, en una sola llamada:
ficha, esquema, perfil estadístico completo, gráficos, interpretación
dinámica con métricas y exportación a reports/eda/perfiles/.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.eda.profiling import (
    clasificar_variables,
    dataset_profile,
    detect_territorial_columns,
    localidad_de_codigo,
    standardize_locality,
    variables_profile,
)
from src.eda.quality import load_dataset, load_dataset_layer
from src.eda.readers import read_gtfs_zip
from src.eda.viz import barras, heatmap_nulos, histograma, mapa, set_style

set_style()


def _display(*objs):
    try:
        import IPython
        if IPython.get_ipython() is None:
            raise ImportError
        from IPython.display import display

        for o in objs:
            display(o)
    except ImportError:
        for o in objs:
            if isinstance(o, (pd.DataFrame, pd.Series)):
                print(o.head(25).to_string())
            else:
                print(o)


def _markdown(text: str):
    try:
        import IPython
        if IPython.get_ipython() is None:
            raise ImportError
        from IPython.display import Markdown

        _display(Markdown(text))
    except ImportError:
        print(text)


def _df_from(data: dict, spec: dict) -> pd.DataFrame:
    tipo = spec.get("tipo") or data.get("tipo", "")
    if spec.get("capa"):
        gdf = data.get("gdf")
        if gdf is not None and "geometry" in gdf.columns:
            return pd.DataFrame(gdf.drop(columns="geometry"))
        return pd.DataFrame(gdf)
    if "df" in data and data["df"] is not None:
        return data["df"]
    if "gdf" in data and data["gdf"] is not None:
        return pd.DataFrame(data["gdf"].drop(columns="geometry", errors="ignore"))
    return pd.DataFrame()


def _gdf_from(data: dict, spec: dict):
    if spec.get("capa") or data.get("tipo") in ("gpkg", "geojson"):
        gdf = data.get("gdf")
        if gdf is not None and hasattr(gdf, "geometry") and "geometry" in gdf.columns:
            return gdf
    return None


def _interpretacion(spec: dict, profile: dict, stats: pd.DataFrame, var_table: pd.DataFrame, gdf=None, territorial: pd.DataFrame | None = None) -> str:
    lines = [f"## Interpretación — {spec.get('titulo', spec.get('id', ''))}", ""]
    lines.append(f"**Origen**: {spec.get('origen', 'no declarado')}  ")
    lines.append(f"**Corte temporal**: {spec.get('corte', 'no declarado')}  ")
    lines.append(f"**Valor público**: {spec.get('valor_publico', 'no declarado')}")
    lines.append("")
    lines.append(f"**Qué contiene**: {profile.get('filas', 0):,} filas y {profile.get('columnas', 0)} columnas; {profile.get('pct_nulos_total', 0)}% de celdas nulas y {profile.get('duplicados', 0)} duplicados.")
    if gdf is not None:
        lines.append(f"Capas con geometría ({gdf.geometry.geom_type.dropna().unique()}) en CRS {gdf.crs}.")
    if profile.get("columnas_territoriales"):
        lines.append(f"Columnas territoriales detectadas: **{', '.join(profile['columnas_territoriales'])}**.")
    num_rows = stats[stats["sin_valores_numericos"].fillna(False).eq(False)] if "sin_valores_numericos" in stats.columns else pd.DataFrame()
    if not num_rows.empty:
        lines.append("")
        lines.append("**Comportamiento de variables numéricas**:")
        for _, r in num_rows.head(5).iterrows():
            cv = r.get("CV_pct")
            skew = r.get("asimetria_skew")
            notes = []
            if cv is not None and not pd.isna(cv) and abs(cv) >= 50:
                notes.append(f"variabilidad alta (CV={cv:.0f}%)")
            if skew is not None and not pd.isna(skew) and abs(skew) > 1:
                notes.append(f"asimetría {'positiva' if skew > 0 else 'negativa'} ({skew:+.2f})")
            if r.get("n_outliers_iqr"):
                notes.append(f"{r['n_outliers_iqr']} outliers IQR ({r.get('pct_outliers', 0):.0f}%)")
            extra = " — " + "; ".join(notes) if notes else ""
            lines.append(f"- `{r['columna']}`: media {r.get('media', float('nan')):,.1f}, mediana {r.get('mediana', float('nan')):,.1f}, desv {r.get('desv_est', float('nan')):,.1f}, rango [{r.get('min', float('nan')):,.0f}, {r.get('max', float('nan')):,.0f}], curtosis {r.get('curtosis', float('nan')):+.1f}{extra}")
    cat_rows = stats[stats.get("n_categorias", pd.Series(dtype=float)).notna()] if "n_categorias" in stats.columns else pd.DataFrame()
    if not cat_rows.empty:
        lines.append("")
        lines.append("**Categóricas dominantes**:")
        for _, r in cat_rows.head(4).iterrows():
            lines.append(f"- `{r['columna']}`: {r.get('n_categorias', 0):,} categorías; dominante '{r.get('dominante', '')}' ({r.get('pct_dominante', 0):.0f}%)")
    if territorial is not None and not territorial.empty:
        n_loc = territorial["localidad"].nunique()
        lines.append("")
        lines.append(f"**Cobertura territorial**: {n_loc} localidades con dato (de 20 + Bogotá).")
    if spec.get("notas"):
        lines.append("")
        lines.append(f"**Notas / qué falta**: {spec['notas']}")
    return "\n".join(lines)


def _save_perfiles(spec: dict, stats: pd.DataFrame, territorial: pd.DataFrame | None, perfiles_dir: Path, gdf=None):
    perfiles_dir.mkdir(parents=True, exist_ok=True)
    key = spec["id"]
    stats.to_csv(perfiles_dir / f"{key}.csv", index=False, encoding="utf-8-sig")
    if territorial is not None and not territorial.empty:
        territorial.to_csv(perfiles_dir / f"{key}__territorial.csv", index=False, encoding="utf-8-sig")
    meta = {
        "id": key,
        "titulo": spec.get("titulo", ""),
        "origen": spec.get("origen", ""),
        "corte": spec.get("corte", ""),
        "valor_publico": spec.get("valor_publico", ""),
        "indicadores": spec.get("indicadores", ""),
        "path": spec.get("path", ""),
        "capa": spec.get("capa", ""),
        "tipo": spec.get("tipo", ""),
    }
    (perfiles_dir / f"{key}__meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def _territorial_counts(df: pd.DataFrame) -> pd.DataFrame | None:
    cols = detect_territorial_columns(df)
    if not cols:
        return None
    out = pd.DataFrame()
    for col in cols:
        values = pd.to_numeric(df[col], errors="coerce")
        is_codes = (
            values.notna().mean() > 0.8
            and values.dropna().between(1, 20).mean() > 0.8
        )
        mapper = localidad_de_codigo if is_codes else standardize_locality
        tmp = df[[col]].copy()
        tmp["localidad"] = tmp[col].map(mapper)
        counts = tmp.dropna(subset=["localidad"]).groupby("localidad").size().reset_index(name="n")
        counts = counts.rename(columns={"n": f"n_{col}"})
        if out.empty:
            out = counts[["localidad", f"n_{col}"]]
        else:
            out = out.merge(counts[["localidad", f"n_{col}"]], on="localidad", how="outer")
    return out.sort_values("localidad") if not out.empty else None


def _plots_for(df: pd.DataFrame, stats: pd.DataFrame, gdf=None, max_num=6, max_cat=3):
    num_cols = []
    if "sin_valores_numericos" in stats.columns:
        num_cols = stats[stats["sin_valores_numericos"].fillna(False).eq(False)]["columna"].tolist()
        # Filter out typical metadata or technical ID columns to avoid uninformative plots
        ignore_patterns = ["id", "objectid", "codigo", "code", "fax", "tel", "phone", "celular", "consecutivo", "index", "fila"]
        num_cols = [c for c in num_cols if not any(pat in c.lower() for pat in ignore_patterns)]
        
        if "CV_pct" in stats.columns:
            cv = stats.set_index("columna")["CV_pct"].dropna()
            num_cols = sorted(num_cols, key=lambda c: -abs(cv.get(c, 0)))
    for col in num_cols[:max_num]:
        histograma(df[col], title=f"Distribución de {col}")
    cat_cols = []
    if "n_categorias" in stats.columns:
        cat_cols = stats[stats["n_categorias"].notna() & stats["n_categorias"].gt(1)]["columna"].tolist()
    for col in cat_cols[:max_cat]:
        barras(df[col], title=f"Frecuencia de {col}")
    heatmap_nulos(df)
    if gdf is not None and len(gdf):
        mapa(gdf, f"Mapa: {gdf.geometry.geom_type.dropna().unique()[:1]}")


def _resolve_path(spec_path: str | Path, raw_dir: Path) -> Path:
    """Resuelve la ruta de un archivo contra raw_dir o ROOT si es relativa."""
    p = Path(spec_path)
    if p.is_absolute() and p.exists():
        return p.resolve()
    if p.exists():
        return p.resolve()
    if (raw_dir / p).exists():
        return (raw_dir / p).resolve()
    root = raw_dir.resolve().parents[1] if raw_dir.resolve().name == "raw" else raw_dir.resolve().parent
    if (root / p).exists():
        return (root / p).resolve()
    parts = p.parts
    if "raw" in parts:
        idx = parts.index("raw")
        subpath = Path(*parts[idx + 1:])
        if (raw_dir / subpath).exists():
            return (raw_dir / subpath).resolve()
    for candidate in raw_dir.rglob(p.name):
        if candidate.is_file():
            return candidate.resolve()
    return (raw_dir / p).resolve()


def explorar_dataset(spec: dict, raw_dir: Path, perfiles_dir: Path, smoke: bool = True) -> dict:
    """Explora un dataset completo: ficha, esquema, perfil, gráficos, interpretación y exportación."""
    _markdown(f"### {spec.get('titulo', spec.get('id', ''))}")
    path = _resolve_path(spec["path"], raw_dir)
    if spec.get("tipo") == "gtfs":
        return _explorar_gtfs(spec, path, perfiles_dir, smoke)

    data = load_dataset_layer(path, spec["capa"], smoke=smoke) if spec.get("capa") else load_dataset(path, raw_dir, smoke=smoke)
    if data.get("error") and data.get("df") is None and data.get("gdf") is None and data.get("hojas") is None:
        _markdown(f"**Error de lectura**: {data['error']}")
        return {"id": spec["id"], "error": data["error"]}

    df = _df_from(data, spec)
    gdf = _gdf_from(data, spec)
    if gdf is not None and len(gdf) and "geometry" in gdf:
        df = df.copy()

    profile = dataset_profile(df)
    var_table = clasificar_variables(df)
    stats = variables_profile(df)
    territorial = _territorial_counts(df)

    _display(clasificar_variables(df))
    _display(stats)
    _plots_for(df, stats, gdf)
    _markdown(_interpretacion(spec, profile, stats, var_table, gdf, territorial))
    _save_perfiles(spec, stats, territorial, perfiles_dir)
    return {
        "id": spec["id"],
        "filas": profile["filas"],
        "columnas": profile["columnas"],
        "pct_nulos_total": profile["pct_nulos_total"],
        "duplicados": profile["duplicados"],
        "columnas_territoriales": profile["columnas_territoriales"],
        "n_localidades": territorial["localidad"].nunique() if territorial is not None else 0,
        "error": "",
    }


def _explorar_gtfs(spec: dict, path: Path, perfiles_dir: Path, smoke: bool) -> dict:
    tables, meta = read_gtfs_zip(path, nrows=1000 if smoke else None)
    _markdown(f"### {spec.get('titulo', 'GTFS')}")
    _display(pd.DataFrame({"tabla": meta["tablas"]}))
    summary = {"id": spec["id"], "tablas": len(meta["tablas"])}
    for table, df in tables.items():
        _markdown(f"**Tabla `{table}`** — {len(df):,} filas muestra, {df.shape[1]} columnas")
        _display(clasificar_variables(df))
        _display(variables_profile(df))
        _plots_for(df, variables_profile(df), max_num=4, max_cat=2)
        stats = variables_profile(df)
        stats.to_csv(perfiles_dir / f"{spec['id']}__{table}.csv", index=False, encoding="utf-8-sig")
    _markdown(_interpretacion(spec, {"filas": 0, "columnas": len(meta["tablas"]), "pct_nulos_total": 0, "duplicados": 0, "columnas_territoriales": []}, pd.DataFrame(), pd.DataFrame()))
    return summary
