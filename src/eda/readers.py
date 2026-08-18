"""Lectores robustos de datos crudos para el EDA de SIPTA.

Cada lector devuelve (contenido, metadatos) y nunca lanza excepciones:
los errores quedan registrados en los metadatos. El perfilado de nulos
se hace sobre filas de datos reales, sin contar filas de título o
encabezados duplicados.
"""

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
import pyogrio

CSV_ENCODINGS = ("utf-8", "utf-8-sig", "latin-1", "cp1252")
CSV_SEPARATORS = (",", ";")

GTFS_TABLES = [
    "agency.txt",
    "routes.txt",
    "stops.txt",
    "trips.txt",
    "stop_times.txt",
    "calendar.txt",
    "calendar_dates.txt",
    "shapes.txt",
    "frequencies.txt",
    "fare_attributes.txt",
    "feed_info.txt",
]


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de columnas (BOM y espacios)."""
    df = df.copy()
    df.columns = [str(c).replace("\ufeff", "").strip() for c in df.columns]
    return df


def _looks_numeric(value: Any) -> bool:
    try:
        float(str(value).replace(",", ".").replace("$", "").replace(" ", ""))
        return True
    except Exception:
        return False


def _csv_score(df: pd.DataFrame) -> float:
    """Puntúa la calidad de un parseo de CSV: más columnas reales = mejor."""
    if df is None or df.shape[1] == 0:
        return -1.0
    if df.shape[1] < 2 or len(df) == 0:
        return -1.0
    unnamed = sum(str(c).lower().startswith("unnamed") for c in df.columns)
    empty_cols = int((df.isna().mean() >= 0.99).sum())
    null_ratio = float(df.isna().mean().mean())
    return 100.0 + df.shape[1] * 2 - unnamed * 10 - empty_cols * 15 - null_ratio * 25


def read_csv_robust(path: Path | str, nrows: int | None = None) -> tuple[pd.DataFrame, dict]:
    """Lee un CSV probando encoding y separador, y eligiendo el parseo con mejor score."""
    attempts: list[str] = []
    best: tuple[float, pd.DataFrame, dict] | None = None
    for enc in CSV_ENCODINGS:
        for sep in CSV_SEPARATORS:
            try:
                df = clean_columns(pd.read_csv(path, encoding=enc, sep=sep, nrows=nrows, low_memory=False))
                score = _csv_score(df)
                meta = {
                    "encoding": enc,
                    "sep": sep,
                    "n_filas": len(df),
                    "n_columnas": df.shape[1],
                    "n_unnamed": sum(str(c).lower().startswith("unnamed") for c in df.columns),
                    "n_cols_vacias": int((df.isna().mean() >= 0.99).sum()) if len(df) else 0,
                    "error": "",
                }
                if best is None or score > best[0]:
                    best = (score, df, meta)
            except Exception as exc:
                attempts.append(f"{enc}/{sep}: {type(exc).__name__}")
    try:
        sniff = clean_columns(pd.read_csv(path, sep=None, engine="python", nrows=nrows, low_memory=False))
        score = _csv_score(sniff)
        meta = {
            "encoding": "sniff",
            "sep": "auto",
            "n_filas": len(sniff),
            "n_columnas": sniff.shape[1],
            "n_unnamed": sum(str(c).lower().startswith("unnamed") for c in sniff.columns),
            "n_cols_vacias": int((sniff.isna().mean() >= 0.99).sum()) if len(sniff) else 0,
            "error": "",
        }
        if best is None or score > best[0]:
            best = (score, sniff, meta)
    except Exception as exc:
        attempts.append(f"sniff: {type(exc).__name__}")
    if best is None or best[0] <= 0:
        return pd.DataFrame(), {"encoding": "", "sep": "", "n_filas": 0, "n_columnas": 0, "n_unnamed": 0, "n_cols_vacias": 0, "error": " | ".join(attempts[-3:])}
    return best[1], best[2]


def _find_header_row(raw: pd.DataFrame) -> int:
    """Busca la fila de encabezados real en un bloque leído con header=None."""
    best_row, best_score = 0, -1
    for i in range(min(30, len(raw))):
        row = raw.iloc[i]
        n_vals = int(row.notna().sum())
        if n_vals < 2:
            continue
        text_frac = row.dropna().astype(str).apply(lambda s: not _looks_numeric(s)).mean() if n_vals else 0
        score = n_vals + text_frac * 3
        if score > best_score:
            best_score, best_row = score, i
    return best_row


def read_xlsx_sheet(path: Path | str, sheet: str, nrows: int | None = None) -> tuple[pd.DataFrame, dict]:
    """Lee una hoja XLSX detectando encabezados reales y descartando filas de título.

    Primera pasada con el comportamiento por defecto de pandas. Si quedan
    columnas 'Unnamed' o casi vacías (típico de reportes con títulos arriba),
    se busca la fila de encabezado real y se relee la hoja.
    """
    try:
        xl = pd.ExcelFile(path)
    except Exception as exc:
        return pd.DataFrame(), {"sheet": sheet, "error": f"{type(exc).__name__}: {exc}"}
    meta: dict = {"sheet": sheet, "header_detectado": False, "filas_titulo_omitidas": 0, "n_unnamed": 0, "n_cols_vacias": 0, "error": ""}
    try:
        df = clean_columns(pd.read_excel(xl, sheet_name=sheet, nrows=nrows))
    except Exception as exc:
        return pd.DataFrame(), {**meta, "error": f"{type(exc).__name__}: {exc}"}

    unnamed = sum(str(c).lower().startswith("unnamed") for c in df.columns)
    empty_cols = int((df.isna().mean() >= 0.99).sum()) if len(df) else 0
    meta.update({"n_unnamed": unnamed, "n_cols_vacias": empty_cols})

    if unnamed <= 1 and empty_cols <= 1 and len(df) > 0:
        return df, meta

    try:
        raw = pd.read_excel(xl, sheet_name=sheet, header=None, nrows=40)
        hrow = _find_header_row(raw)
        if hrow > 0:
            df2 = clean_columns(pd.read_excel(xl, sheet_name=sheet, header=hrow, nrows=nrows))
            df2 = df2.dropna(axis=1, how="all")
            unnamed2 = sum(str(c).lower().startswith("unnamed") for c in df2.columns)
            empty2 = int((df2.isna().mean() >= 0.99).sum()) if len(df2) else 0
            if unnamed2 <= unnamed or empty2 <= empty_cols:
                return df2, {**meta, "header_detectado": True, "filas_titulo_omitidas": int(hrow), "n_unnamed": unnamed2, "n_cols_vacias": empty2}
    except Exception:
        pass
    return df, meta


def gpkg_layer_info(path: Path | str, layer: str) -> dict:
    """Metadatos de una capa GPKG vía pyogrio (sin cargar datos)."""
    info = pyogrio.read_info(path, layer=layer)
    bbox = info.get("bbox")
    if isinstance(bbox, (tuple, list)) and len(bbox) == 4:
        bbox = tuple(round(float(x), 6) for x in bbox)
    return {
        "capa": layer,
        "features": info.get("features"),
        "fields": [str(f) for f in info.get("fields", [])],
        "crs": str(info.get("crs") or ""),
        "geometry_type": str(info.get("geometry_type") or ""),
        "bbox": bbox,
    }


def read_gpkg_layer(
    path: Path | str, layer: str, rows: int | None = None, read_geometry: bool = True
) -> tuple[gpd.GeoDataFrame | pd.DataFrame | None, dict]:
    """Lee una capa GPKG con muestra opcional y metadatos. Nunca lanza."""
    try:
        info = gpkg_layer_info(path, layer)
    except Exception as exc:
        return None, {"capa": layer, "error": f"{type(exc).__name__}: {exc}"}
    try:
        gdf = gpd.read_file(path, layer=layer, rows=rows)
        if not read_geometry and "geometry" in gdf.columns:
            gdf = gdf.drop(columns="geometry")
        info["error"] = ""
        return gdf, info
    except Exception as exc:
        return None, {**info, "error": f"{type(exc).__name__}: {exc}"}


def read_geojson(path: Path | str) -> tuple[gpd.GeoDataFrame | None, dict]:
    """Lee un GeoJSON completo. Nunca lanza."""
    try:
        gdf = gpd.read_file(path)
        geom = ", ".join(sorted(str(x) for x in gdf.geometry.geom_type.dropna().unique())) if "geometry" in gdf and len(gdf) else ""
        bbox = tuple(round(float(x), 6) for x in gdf.total_bounds) if len(gdf) and "geometry" in gdf else ""
        meta = {
            "features": len(gdf),
            "fields": [str(c) for c in gdf.columns if c != "geometry"],
            "crs": str(gdf.crs or ""),
            "geometry_type": geom,
            "bbox": bbox,
            "error": "",
        }
        return gdf, meta
    except Exception as exc:
        return None, {"features": 0, "fields": [], "crs": "", "geometry_type": "", "bbox": "", "error": f"{type(exc).__name__}: {exc}"}


def read_gtfs_zip(path: Path | str, nrows: int | None = None) -> tuple[dict[str, pd.DataFrame], dict]:
    """Lee las tablas GTFS de un ZIP sin extraerlo. Nunca lanza."""
    out: dict[str, pd.DataFrame] = {}
    meta: dict = {"n_archivos": 0, "tablas": [], "errores": {}}
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            meta["n_archivos"] = len(names)
            for table in GTFS_TABLES:
                if table not in names:
                    continue
                meta["tablas"].append(table)
                try:
                    with zf.open(table) as fh:
                        out[table] = clean_columns(pd.read_csv(fh, nrows=nrows, low_memory=False))
                except Exception as exc:
                    meta["errores"][table] = f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        meta["error"] = f"{type(exc).__name__}: {exc}"
    return out, meta


def read_any(path: Path | str, nrows: int | None = None) -> tuple[Any, dict]:
    """Despacho por extensión. Devuelve (df | gdf | dict_de_tablas | None, metadatos)."""
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".csv":
        return read_csv_robust(path, nrows=nrows)
    if ext == ".geojson":
        return read_geojson(path)
    if ext == ".xlsx":
        return read_xlsx_sheet(path, path.stem, nrows=nrows)
    if ext == ".zip":
        return read_gtfs_zip(path, nrows=nrows)
    return None, {"error": f"formato no soportado por read_any: {ext}"}
