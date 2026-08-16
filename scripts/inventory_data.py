"""Genera un inventario reproducible de los datos en data/raw.

Escanea GeoPackage, GeoJSON y CSV, y escribe un reporte Markdown en
`docs/01-requirements/01-data-inventory.md`.
"""

import warnings
from datetime import date
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pyogrio

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"
OUT = ROOT / "docs" / "01-requirements" / "01-data-inventory.md"

SAMPLE_LIMIT = 25_000
FULL_LIMIT = 100_000


def escanear_gpkg(path: Path) -> list[dict]:
    """Devuelve inventario de las capas dentro de un GeoPackage."""
    capas = []
    try:
        info_layers = gpd.list_layers(path)
    except Exception as exc:
        return [{"layer": "ERROR", "nota": str(exc)}]

    for fila in info_layers.itertuples(index=False):
        nombre = getattr(fila, "name", fila[0])
        geom = getattr(fila, "geometry_type", fila[1] if len(fila) > 1 else "-")
        registro = {"layer": str(nombre), "geometry": str(geom)}

        try:
            info = pyogrio.read_info(path, layer=nombre)
            n_total = int(info.get("features", -1))
            registro["features"] = n_total
            registro["crs"] = str(info.get("crs") or "sin CRS")
            if not info.get("geometry_type"):
                registro["geometry"] = "Tabla no espacial"
        except Exception as exc:
            try:
                gdf_full = gpd.read_file(path, layer=nombre)
                registro["features"] = len(gdf_full)
                registro["crs"] = str(gdf_full.crs) if gdf_full.crs else "sin CRS"
            except Exception as exc2:
                registro["features"] = -1
                registro["error"] = f"{exc}; fallback: {exc2}"

        if "crs" not in registro:
            try:
                gdf = gpd.read_file(path, layer=nombre, rows=2)
                registro["crs"] = str(gdf.crs) if gdf.crs else "sin CRS"
            except Exception as exc:
                registro["crs"] = f"error CRS: {exc}"

        try:
            n_total = registro.get("features", 0)
            filas = min(n_total, SAMPLE_LIMIT) if n_total > FULL_LIMIT else n_total
            if filas > 0:
                df = gpd.read_file(path, layer=nombre, rows=filas, read_geometry=False)
                registro["muestra"] = filas
                registro["n_cols"] = len(df.columns)
                nulos = df.isna().sum()
                registro["cols_nulas_mayores"] = [
                    {"col": c, "nulos": int(v)}
                    for c, v in nulos[nulos > 0].items()
                ]
                registro["pct_nulos_total"] = round(
                    float(nulos.sum() / (df.shape[0] * df.shape[1]) * 100), 2
                )
                registro["duplicados"] = int(df.duplicated().sum())
        except Exception as exc:
            registro["nota_calidad"] = str(exc)

        capas.append(registro)
    return capas


def escanear_csv(path: Path) -> dict:
    """Inventario de un CSV con detección de encoding y nulos."""
    registro = {"file": path.name}
    encoding_usado = None
    for enc in ("utf-8", "utf-8-sig", "latin1", "cp1252"):
        try:
            pd.read_csv(path, sep=None, engine="python", encoding=enc, nrows=5)
            encoding_usado = enc
            break
        except Exception:
            continue
    if encoding_usado is None:
        return {**registro, "error": "no se pudo leer"}

    try:
        df_full = pd.read_csv(path, sep=None, engine="python", encoding=encoding_usado)
    except Exception as exc:
        return {**registro, "error": str(exc)}

    registro["encoding"] = encoding_usado
    registro["rows"] = len(df_full)
    registro["columns"] = list(df_full.columns)
    registro["n_cols"] = len(df_full.columns)
    nulos = df_full.isna().sum()
    registro["pct_nulos_total"] = round(
        float(nulos.sum() / (len(df_full) * len(df_full.columns)) * 100), 2
    ) if len(df_full) else 0.0
    registro["cols_nulas_mayores"] = [
        {"col": c, "nulos": int(v)} for c, v in nulos[nulos > 0].items()
    ]
    registro["duplicados"] = int(df_full.duplicated().sum())
    return registro


def escanear_geojson(path: Path) -> dict:
    """Inventario de un GeoJSON pequeño."""
    try:
        gdf = gpd.read_file(path)
    except Exception as exc:
        return {"file": path.name, "error": str(exc)}
    registro = {
        "file": path.name,
        "features": int(len(gdf)),
        "geometry": str(gdf.geom_type.drop_duplicates().tolist() if len(gdf) else "-"),
        "crs": str(gdf.crs) if gdf.crs else "sin CRS",
        "columns": list(gdf.columns),
        "n_cols": len(gdf.columns),
        "pct_nulos_total": round(
            float(gdf.isna().sum().sum() / (len(gdf) * len(gdf.columns)) * 100), 2
        ) if len(gdf) else 0.0,
        "duplicados": int(gdf.duplicated().sum()),
    }
    return registro


def markdown_section(title: str, body: str) -> str:
    return f"\n## {title}\n\n{body}\n"


def main() -> None:
    lines: list[str] = []
    lines.append("# 01 - Inventario de Datos")
    lines.append("")
    lines.append("**Generado por**: `scripts/inventory_data.py`")
    lines.append(f"**Fecha**: {date.today().isoformat()}")
    lines.append("")

    lines.append(markdown_section("1. GeoPackages", ""))
    for path in sorted(DATA_DIR.rglob("*.gpkg")):
        lines.append(f"### `{path.relative_to(ROOT)}`")
        lines.append("")
        lines.append("| Capa | Geometria | CRS | Features | Muestra | Columnas | Duplicados | Nulos % |")
        lines.append("|------|-----------|-----|----------|---------|----------|-----------|---------|")
        for layer in escanear_gpkg(path):
            lines.append(
                f"| {layer['layer']} | {layer.get('geometry','-')} | {layer.get('crs','-')} | {layer.get('features','-')} | {layer.get('muestra','-')} | {layer.get('n_cols','-')} | {layer.get('duplicados','-')} | {layer.get('pct_nulos_total','-')} |"
            )
            if layer.get("cols_nulas_mayores"):
                detail = ", ".join(f"{d['col']}={d['nulos']}" for d in layer["cols_nulas_mayores"][:6])
                lines.append(f"  - Columnas con nulos: {detail}")
        lines.append("")

    lines.append(markdown_section("2. GeoJSON", ""))
    for path in sorted(DATA_DIR.rglob("*.geojson")):
        reg = escanear_geojson(path)
        if reg.get("error"):
            lines.append(f"### `{path.relative_to(ROOT)}`\n\n- Error: {reg['error']}\n")
            continue
        lines.append(f"### `{path.relative_to(ROOT)}`")
        lines.append("")
        lines.append(f"- Features: {reg['features']} | Geometria: {reg['geometry']} | CRS: {reg['crs']}")
        lines.append(f"- Columnas({reg['n_cols']}): {', '.join(map(str, reg['columns']))}")
        lines.append(f"- Nulos totales: {reg['pct_nulos_total']}% | Duplicados: {reg['duplicados']}")
        lines.append("")

    lines.append(markdown_section("3. CSV", ""))
    for path in sorted(DATA_DIR.rglob("*.csv")):
        if path.name == ".gitkeep":
            continue
        reg = escanear_csv(path)
        lines.append(f"### `{path.relative_to(ROOT)}`")
        lines.append("")
        lines.append(f"- Filas: {reg.get('rows','-')} | Columnas: {reg.get('n_cols','-')} | Encoding: {reg.get('encoding','-')}")
        lines.append(f"- Columnas: {', '.join(map(str, reg.get('columns', [])))}")
        lines.append(f"- Nulos totales: {reg.get('pct_nulos_total','-')}% | Duplicados: {reg.get('duplicados','-')}")
        if reg.get("cols_nulas_mayores"):
            detail = ", ".join(f"{d['col']}={d['nulos']}" for d in reg["cols_nulas_mayores"][:6])
            lines.append(f"- Columnas con nulos: {detail}")
        if reg.get("error"):
            lines.append(f"- Error: {reg['error']}")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Inventario generado: {OUT}")


if __name__ == "__main__":
    main()
