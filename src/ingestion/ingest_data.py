"""Módulo de ingesta para los datasets crudos del proyecto SIPTA.

Fase PDCO: DEVELOPMENT
Estándares: Clean Code, PEP 8, DAMA-BOK
Autoría: Persona A (Adan Sánchez), Persona B (Yesid Bello) & Persona C (Sofía Hidalgo — Ingesta Ambiente, Finanzas/RIVI, Seguridad)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from shutil import copy2
from typing import Any

import geopandas as gpd
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Resolución de la raíz del proyecto
ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

IGNORED_FILES: set[str] = {".gitkeep", "README.md", "README.txt", "README"}
SUPPORTED_TEXT_SUFFIXES: set[str] = {
    ".csv",
    ".json",
    ".geojson",
    ".xlsx",
    ".xls",
    ".gpkg",
    ".zip",
}


def get_project_root() -> Path:
    """Retorna la ruta absoluta a la raíz del repositorio."""
    return ROOT


def discover_raw_files(raw_dir: Path | None = None) -> list[Path]:
    """Descubre y devuelve todos los archivos de datos soportados en la carpeta raw.

    Args:
        raw_dir: Directorio raíz de datos crudos (por defecto data/raw).

    Returns:
        Lista ordenada de rutas Path a los archivos encontrados.
    """
    base_dir = (raw_dir or RAW_DIR).resolve()
    if not base_dir.exists():
        logger.warning("El directorio raw no existe: %s", base_dir)
        return []

    files = [
        path
        for path in base_dir.rglob("*")
        if path.is_file()
        and path.name not in IGNORED_FILES
        and path.suffix.lower() in SUPPORTED_TEXT_SUFFIXES
    ]
    return sorted(files)


def build_output_path(
    source_path: Path,
    raw_dir: Path | None = None,
    processed_dir: Path | None = None,
    suffix: str | None = None,
) -> Path:
    """Construye la ruta destino preservando la estructura relativa respecto a data/raw.

    Args:
        source_path: Ruta del archivo fuente.
        raw_dir: Directorio base de origen.
        processed_dir: Directorio base de destino.
        suffix: Extensión opcional para cambiar la del archivo destino.

    Returns:
        Ruta Path correspondiente en data/processed.
    """
    base_raw_dir = (raw_dir or RAW_DIR).resolve()
    base_processed_dir = (processed_dir or PROCESSED_DIR).resolve()
    relative_path = source_path.resolve().relative_to(base_raw_dir)
    if suffix is None:
        return base_processed_dir / relative_path
    return base_processed_dir / relative_path.with_suffix(suffix)


def _read_csv_with_fallback(source_path: Path) -> pd.DataFrame:
    """Lee un archivo CSV probando diferentes codificaciones y delimitadores."""
    for encoding in ("utf-8", "latin-1", "cp1252"):
        for sep in (",", ";", "\t"):
            try:
                df = pd.read_csv(source_path, low_memory=False, encoding=encoding, sep=sep)
                if len(df.columns) > 1 or len(df) <= 1:
                    return df
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
    # Intento final por defecto con motor python
    return pd.read_csv(source_path, low_memory=False, encoding="utf-8", on_bad_lines="skip")


def _ingest_tabular_file(source_path: Path, output_path: Path) -> dict[str, Any]:
    """Procesa e ingesta archivos tabulares (.csv, .xlsx, .xls, .json)."""
    suffix = source_path.suffix.lower()
    if suffix == ".csv":
        df = _read_csv_with_fallback(source_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        return {
            "status": "ingested",
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "format": "csv",
            "output": str(output_path),
        }
    if suffix in {".xlsx", ".xls"}:
        out_csv = output_path.with_suffix(".csv")
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        df = pd.read_excel(source_path)
        df.to_csv(out_csv, index=False)
        return {
            "status": "ingested",
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "format": "excel_to_csv",
            "output": str(out_csv),
        }
    if suffix == ".json":
        out_csv = output_path.with_suffix(".csv")
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        df = pd.read_json(source_path)
        df.to_csv(out_csv, index=False)
        return {
            "status": "ingested",
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "format": "json_to_csv",
            "output": str(out_csv),
        }
    raise ValueError(f"Formato no soportado para ingesta tabular: {source_path}")


def _ingest_geospatial_file(source_path: Path, output_path: Path) -> dict[str, Any]:
    """Procesa e ingesta archivos vectoriales geoespaciales (.gpkg, .geojson)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    gdf = gpd.read_file(source_path)
    if output_path.suffix.lower() == ".geojson":
        gdf.to_file(output_path, driver="GeoJSON")
    else:
        gdf.to_file(output_path, driver="GPKG")
    return {
        "status": "ingested",
        "rows": int(len(gdf)),
        "columns": int(len(gdf.columns)),
        "crs": str(gdf.crs) if gdf.crs else "None",
        "format": "geospatial",
        "output": str(output_path),
    }


def ingest_dataset(
    source_path: Path,
    raw_dir: Path | None = None,
    processed_dir: Path | None = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Ingesta un archivo individual desde raw hacia processed.

    Args:
        source_path: Ruta del archivo en data/raw.
        raw_dir: Directorio base de origen.
        processed_dir: Directorio base de destino.
        overwrite: Si es True, sobreescribe archivos existentes en destino.

    Returns:
        Diccionario con metadatos del resultado de la ingesta.
    """
    base_raw_dir = (raw_dir or RAW_DIR).resolve()
    base_processed_dir = (processed_dir or PROCESSED_DIR).resolve()
    source_path = source_path.resolve()
    output_path = build_output_path(
        source_path, raw_dir=base_raw_dir, processed_dir=base_processed_dir
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not overwrite:
        return {"status": "skipped", "output": str(output_path), "format": source_path.suffix.lower()}

    suffix = source_path.suffix.lower()
    try:
        if suffix in {".csv", ".json", ".xlsx", ".xls"}:
            payload = _ingest_tabular_file(source_path, output_path)
        elif suffix in {".geojson", ".gpkg"}:
            payload = _ingest_geospatial_file(source_path, output_path)
        elif suffix == ".zip":
            copy2(source_path, output_path)
            payload = {"status": "copied", "format": "zip", "output": str(output_path)}
        else:
            copy2(source_path, output_path)
            payload = {"status": "copied", "format": "binary", "output": str(output_path)}
    except Exception as exc:
        logger.error("Error al ingestar %s: %s", source_path, exc)
        payload = {"status": "error", "error": str(exc), "output": str(output_path)}

    return payload


def ingest_all_datasets(
    raw_dir: Path | None = None,
    processed_dir: Path | None = None,
    manifest_path: Path | None = None,
    overwrite: bool = False,
) -> list[dict[str, Any]]:
    """Ejecuta la ingesta completa para todos los datasets crudos disponibles.

    Args:
        raw_dir: Directorio raw personalizado.
        processed_dir: Directorio processed personalizado.
        manifest_path: Ruta del manifiesto JSON de salida.
        overwrite: Forzar sobreescritura si ya existe en destino.

    Returns:
        Lista de diccionarios con el estado de cada archivo procesado.
    """
    base_raw_dir = (raw_dir or RAW_DIR).resolve()
    base_processed_dir = (processed_dir or PROCESSED_DIR).resolve()
    base_processed_dir.mkdir(parents=True, exist_ok=True)

    files = discover_raw_files(base_raw_dir)
    results: list[dict[str, Any]] = []

    for path in files:
        result = ingest_dataset(
            path, raw_dir=base_raw_dir, processed_dir=base_processed_dir, overwrite=overwrite
        )
        result["source"] = str(path.relative_to(base_raw_dir))
        result["size_bytes"] = path.stat().st_size
        results.append(result)

    manifest_file = manifest_path or base_processed_dir / "ingestion_manifest.json"
    manifest_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Manifiesto de ingesta generado en: %s (%d fuentes)", manifest_file, len(results))
    return results


def load_raw_csv(filename: str) -> pd.DataFrame:
    """Carga un archivo CSV directamente desde data/raw."""
    path = RAW_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo raw: {path}")
    return _read_csv_with_fallback(path)


def save_raw_copy(df: pd.DataFrame, output_name: str) -> Path:
    """Guarda una copia de DataFrame en data/raw."""
    destination = RAW_DIR / output_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    return destination


def save_processed_csv(df: pd.DataFrame, output_name: str) -> Path:
    """Guarda un DataFrame en data/processed."""
    destination = PROCESSED_DIR / output_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    return destination


if __name__ == "__main__":
    results = ingest_all_datasets()
    print(f"Ingesta finalizada: {len(results)} datasets procesados.")
