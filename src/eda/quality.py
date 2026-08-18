"""Reglas de calidad y perfil consolidado por archivo/capa/hoja para el EDA."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.eda.profiling import (
    clasificar_variables,
    dataset_profile,
    detect_territorial_columns,
    standardize_locality,
)
from src.eda.readers import (
    gpkg_layer_info,
    read_csv_robust,
    read_geojson,
    read_gpkg_layer,
    read_gtfs_zip,
    read_xlsx_sheet,
)

MR_MARKERS = ("gpkg_mr_v03.26",)
MR_REFERENCE_LAYERS = {"Loca", "UPL", "Muni"}
VALIDACIONES_MARKER = "validaciones"


def sector_from_path(path: Path, raw_dir: Path) -> str:
    try:
        return path.resolve().relative_to(raw_dir.resolve()).parts[0]
    except Exception:
        return ""


def _size_mb(path: Path) -> float:
    try:
        return round(path.stat().st_size / 1024 / 1024, 3)
    except Exception:
        return 0.0


def _territorial_counts(key: str, df: pd.DataFrame, out: dict[str, pd.DataFrame]):
    for col in detect_territorial_columns(df):
        tmp = df[[col]].copy()
        tmp["localidad"] = tmp[col].map(standardize_locality)
        counts = tmp.dropna(subset=["localidad"]).groupby("localidad").size().reset_index(name="registros")
        if not counts.empty:
            out[f"{key}::{col}"] = counts


def problem_flags(entry: dict) -> str:
    """Convierte un perfil en banderas de problemas legibles."""
    flags = []
    if entry.get("error_lectura"):
        flags.append("error_lectura")
    if entry.get("n_unnamed", 0) > 1:
        flags.append("columnas_unnamed")
    if entry.get("n_cols_vacias", 0) > 1:
        flags.append("columnas_vacias")
    if entry.get("filas_titulo_omitidas", 0) > 0:
        flags.append("encabezado_detectado")
    if entry.get("pct_nulos_total") is not None and entry["pct_nulos_total"] >= 40:
        flags.append("nulos_altos")
    if entry.get("duplicados"):
        flags.append("duplicados")
    if not entry.get("columnas_territoriales"):
        flags.append("sin_columna_territorial")
    if entry.get("encoding_legacy"):
        flags.append("encoding_legacy")
    if entry.get("muestra_por_performance"):
        flags.append("muestra_por_performance")
    if entry.get("bbox_fuera_bogota"):
        flags.append("bbox_fuera_bogota")
    return ", ".join(dict.fromkeys(flags)) if flags else "sin_alertas"


def _base_entry(path: Path, raw_dir: Path, formato: str) -> dict:
    rel = path.resolve().relative_to(raw_dir.resolve())
    return {
        "sector": sector_from_path(path, raw_dir),
        "ruta": str(rel),
        "archivo": path.name,
        "formato": formato,
        "tamano_mb": _size_mb(path),
        "error_lectura": "",
        "encoding": "",
        "separador": "",
        "crs": "",
        "geometria": "",
        "filas_totales": None,
        "filas_muestra": None,
        "columnas": None,
        "n_unnamed": 0,
        "n_cols_vacias": 0,
        "filas_titulo_omitidas": 0,
        "pct_nulos_total": None,
        "duplicados": None,
        "columnas_territoriales": "",
        "variables_numericas": 0,
        "variables_categoricas": 0,
        "variables_temporales": 0,
        "variables_espaciales": 0,
        "encoding_legacy": False,
        "muestra_por_performance": False,
        "bbox_fuera_bogota": False,
    }


def _fill_from_profile(entry: dict, profile: dict, var_table: pd.DataFrame | None = None) -> dict:
    entry.update(
        {
            "filas_muestra": profile.get("filas"),
            "columnas": profile.get("columnas"),
            "pct_nulos_total": profile.get("pct_nulos_total"),
            "duplicados": profile.get("duplicados"),
            "columnas_territoriales": ", ".join(profile.get("columnas_territoriales", [])),
        }
    )
    if var_table is not None and not var_table.empty:
        entry.update(
            {
                "variables_numericas": int(var_table["tipo_variable"].str.startswith("numérica").sum()),
                "variables_categoricas": int(var_table["tipo_variable"].str.startswith("categórica").sum()),
                "variables_temporales": int(var_table["tipo_variable"].eq("temporal").sum()),
                "variables_espaciales": int(var_table["tipo_variable"].eq("espacial").sum()),
            }
        )
    return entry


def profile_csv(path: Path, raw_dir: Path, nrows: int | None = None) -> list[dict]:
    entry = _base_entry(path, raw_dir, "csv")
    df, meta = read_csv_robust(path, nrows=nrows)
    if meta["error"]:
        entry["error_lectura"] = meta["error"]
        entry["problemas_detectados"] = problem_flags(entry)
        return [entry]
    entry["encoding"] = meta["encoding"]
    entry["separador"] = meta["sep"]
    entry["n_unnamed"] = meta["n_unnamed"]
    entry["n_cols_vacias"] = meta["n_cols_vacias"]
    entry["encoding_legacy"] = meta["encoding"] in ("latin-1", "cp1252")
    profile = dataset_profile(df)
    profile["filas"] = profile.pop("filas")
    entry = _fill_from_profile(entry, profile, clasificar_variables(df))
    entry["problemas_detectados"] = problem_flags(entry)
    return [entry]


def profile_geojson(path: Path, raw_dir: Path) -> list[dict]:
    entry = _base_entry(path, raw_dir, "geojson")
    gdf, meta = read_geojson(path)
    if meta["error"] or gdf is None:
        entry["error_lectura"] = meta["error"]
        entry["problemas_detectados"] = problem_flags(entry)
        return [entry]
    entry.update({"crs": meta["crs"], "geometria": meta["geometry_type"], "filas_totales": meta["features"]})
    attr_df = pd.DataFrame(gdf.drop(columns="geometry", errors="ignore"))
    profile = dataset_profile(attr_df)
    profile["filas"] = len(gdf)
    entry = _fill_from_profile(entry, profile, clasificar_variables(attr_df))
    entry["bbox_fuera_bogota"] = _bbox_fuera_bogota(meta["bbox"])
    entry["problemas_detectados"] = problem_flags(entry)
    return [entry]


def _bbox_fuera_bogota(bbox) -> bool:
    if not bbox or len(bbox) != 4:
        return False
    minx, miny, maxx, maxy = (float(v) for v in bbox)
    if minx < -75.5 or minx > -72.5:
        return False
    return not ((-75.5 < minx < -73.0) and (-75.5 < maxx < -73.0) and (3.5 < miny < 5.5) and (3.5 < maxy < 5.5))


def profile_gpkg(path: Path, raw_dir: Path, smoke: bool, sample_rows: int = 500) -> list[dict]:
    """Perfila cada capa: metadatos siempre; muestra solo en capas pequeñas o de referencia del MR."""
    is_mr = any(m in str(path).lower() for m in MR_MARKERS)
    try:
        layers = list(gpd_list_layers(path))
    except Exception as exc:
        entry = _base_entry(path, raw_dir, "gpkg")
        entry["error_lectura"] = f"{type(exc).__name__}: {exc}"
        entry["problemas_detectados"] = problem_flags(entry)
        return [entry]

    rows = []
    for layer_name in layers:
        entry = _base_entry(path, raw_dir, "gpkg")
        entry["capa_hoja"] = layer_name
        try:
            info = gpkg_layer_info(path, layer_name)
        except Exception as exc:
            entry["error_lectura"] = f"{type(exc).__name__}: {exc}"
            entry["problemas_detectados"] = problem_flags(entry)
            rows.append(entry)
            continue
        entry.update(
            {
                "crs": info["crs"],
                "geometria": info["geometry_type"],
                "filas_totales": info["features"],
                "columnas": len(info["fields"]),
            }
        )
        read_sample = (not is_mr) or layer_name in MR_REFERENCE_LAYERS
        if not read_sample:
            entry["muestra_por_performance"] = True
            entry["problemas_detectados"] = problem_flags(entry)
            rows.append(entry)
            continue
        try:
            gdf, gmeta = read_gpkg_layer(path, layer_name, rows=sample_rows)
            if gmeta["error"] or gdf is None:
                entry["error_lectura"] = gmeta["error"]
                entry["problemas_detectados"] = problem_flags(entry)
                rows.append(entry)
                continue
            attr_df = pd.DataFrame(gdf.drop(columns="geometry", errors="ignore"))
            profile = dataset_profile(attr_df)
            profile["filas"] = len(gdf)
            entry = _fill_from_profile(entry, profile, clasificar_variables(attr_df))
            if is_mr:
                entry["muestra_por_performance"] = True
        except Exception as exc:
            entry["error_lectura"] = f"{type(exc).__name__}: {exc}"
        entry["problemas_detectados"] = problem_flags(entry)
        rows.append(entry)
    return rows


def gpd_list_layers(path: Path) -> list[str]:
    import geopandas as gpd

    info = gpd.list_layers(path)
    names = []
    for _, row in info.iterrows():
        name = row["name"]
        names.append(name.decode("latin-1") if isinstance(name, bytes) else str(name))
    return names


def profile_xlsx(path: Path, raw_dir: Path, smoke: bool, nrows: int | None = 300) -> list[dict]:
    try:
        excel = pd.ExcelFile(path)
        sheets = excel.sheet_names
    except Exception as exc:
        entry = _base_entry(path, raw_dir, "xlsx")
        entry["error_lectura"] = f"{type(exc).__name__}: {exc}"
        entry["problemas_detectados"] = problem_flags(entry)
        return [entry]
    is_validation = VALIDACIONES_MARKER in str(path).lower()
    sheets_to_sample = sheets[:3] if (smoke and is_validation) else sheets
    rows = []
    for sheet in sheets:
        entry = _base_entry(path, raw_dir, "xlsx")
        entry["capa_hoja"] = sheet
        if sheet not in sheets_to_sample:
            entry["muestra_por_performance"] = True
            entry["problemas_detectados"] = problem_flags(entry)
            rows.append(entry)
            continue
        df, meta = read_xlsx_sheet(path, sheet, nrows=nrows)
        if meta["error"]:
            entry["error_lectura"] = meta["error"]
            entry["problemas_detectados"] = problem_flags(entry)
            rows.append(entry)
            continue
        entry.update(
            {
                "n_unnamed": meta["n_unnamed"],
                "n_cols_vacias": meta["n_cols_vacias"],
                "filas_titulo_omitidas": meta["filas_titulo_omitidas"],
            }
        )
        if is_validation:
            entry["muestra_por_performance"] = True
        profile = dataset_profile(df)
        profile["filas"] = profile.pop("filas")
        entry = _fill_from_profile(entry, profile, clasificar_variables(df))
        entry["problemas_detectados"] = problem_flags(entry)
        rows.append(entry)
    return rows


def profile_gtfs_zip(path: Path, raw_dir: Path, nrows: int | None = 2000) -> list[dict]:
    tables, meta = read_gtfs_zip(path, nrows=nrows)
    rows = []
    entry = _base_entry(path, raw_dir, "zip")
    entry["capa_hoja"] = "contenido_zip"
    entry["filas_totales"] = meta.get("n_archivos")
    entry["columnas_territoriales"] = ""
    if meta.get("error"):
        entry["error_lectura"] = meta["error"]
    else:
        entry["problemas_detectados"] = ""
        faltantes = [t for t in ("agency.txt", "routes.txt", "stops.txt", "trips.txt", "calendar.txt", "stop_times.txt") if t not in meta["tablas"]]
        entry["problemas_detectados"] = ", ".join([f"gtfs_faltan:{','.join(faltantes)}"] if faltantes else ["gtfs_completo"])
    entry["problemas_detectados"] = problem_flags(entry) if entry["error_lectura"] else entry["problemas_detectados"]
    rows.append(entry)
    for table, df in tables.items():
        entry = _base_entry(path, raw_dir, "gtfs_txt")
        entry["capa_hoja"] = table
        profile = dataset_profile(df)
        profile["filas"] = profile.pop("filas")
        entry = _fill_from_profile(entry, profile, clasificar_variables(df))
        if table == "stops.txt" and {"stop_lat", "stop_lon"}.issubset(df.columns):
            lat = pd.to_numeric(df["stop_lat"], errors="coerce")
            lon = pd.to_numeric(df["stop_lon"], errors="coerce")
            outside = ~(lat.between(3.5, 5.0) & lon.between(-75.0, -73.0))
            entry["bbox_fuera_bogota"] = bool(outside.mean() > 0.05)
        entry["problemas_detectados"] = problem_flags(entry)
        rows.append(entry)
    return rows


def profile_file(path: Path, raw_dir: Path, smoke: bool = True, nrows: int | None = None) -> list[dict]:
    """Perfila un archivo completo y devuelve una o más entradas (por capa/hoja)."""
    name = path.name.lower()
    if name == "readme.md":
        entry = _base_entry(path, raw_dir, "readme")
        entry["problemas_detectados"] = "readme_only"
        return [entry]
    ext = path.suffix.lower()
    if ext == ".csv":
        return profile_csv(path, raw_dir, nrows=nrows)
    if ext == ".gpkg":
        return profile_gpkg(path, raw_dir, smoke, sample_rows=300 if smoke else 500)
    if ext == ".geojson":
        return profile_geojson(path, raw_dir)
    if ext in (".xlsx", ".xls"):
        return profile_xlsx(path, raw_dir, smoke, nrows=100 if smoke else 300)
    if ext == ".zip":
        return profile_gtfs_zip(path, raw_dir, nrows=1000 if smoke else 2000)
    entry = _base_entry(path, raw_dir, ext.replace(".", "") or "otro")
    entry["problemas_detectados"] = "formato_no_perfilado"
    return [entry]


def load_dataset(path: Path, raw_dir: Path, smoke: bool = True) -> dict:
    """Carga un archivo para exploración profunda: devuelve datos + perfil + metadatos."""
    ext = path.suffix.lower()
    if ext == ".gpkg":
        layers = gpd_list_layers(path)
        loaded = []
        for layer in layers:
            gdf, meta = read_gpkg_layer(path, layer, rows=300 if smoke else None)
            loaded.append({"capa": layer, "gdf": gdf, "meta": meta})
        return {"tipo": "gpkg", "archivo": str(path), "capas": loaded, "error": ""}
    if ext == ".csv":
        df, meta = read_csv_robust(path)
        return {"tipo": "csv", "archivo": str(path), "df": df, "meta": meta, "error": meta["error"]}
    if ext == ".geojson":
        gdf, meta = read_geojson(path)
        return {"tipo": "geojson", "archivo": str(path), "gdf": gdf, "meta": meta, "error": meta["error"]}
    if ext in (".xlsx", ".xls"):
        xl = pd.ExcelFile(path)
        hojas = {}
        for sheet in xl.sheet_names[:1]:
            df, meta = read_xlsx_sheet(path, sheet)
            hojas[sheet] = {"df": df, "meta": meta}
        return {"tipo": "xlsx", "archivo": str(path), "hojas": hojas, "error": ""}
    if ext == ".zip":
        tables, meta = read_gtfs_zip(path, nrows=1000 if smoke else None)
        return {"tipo": "zip", "archivo": str(path), "tablas": tables, "meta": meta, "error": meta.get("error", "")}
    return {"tipo": "otro", "archivo": str(path), "error": "formato no soportado"}


def load_dataset_layer(path: Path, layer: str, smoke: bool = True) -> dict:
    """Carga una capa concreta de un GPKG para exploración profunda."""
    gdf, meta = read_gpkg_layer(path, layer, rows=300 if smoke else None)
    return {"tipo": "gpkg", "archivo": str(path), "capa": layer, "gdf": gdf, "meta": meta, "error": meta.get("error", "")}
