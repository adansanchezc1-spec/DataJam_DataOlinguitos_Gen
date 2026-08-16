"""Módulo de ingesta para los datasets crudos del proyecto SIPTA."""

from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2
from typing import Any

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


IGNORED_FILES = {".gitkeep", "README.md", "README.txt", "README"}
SUPPORTED_TEXT_SUFFIXES = {".csv", ".json", ".geojson", ".xlsx", ".xls", ".gpkg", ".zip"}


def discover_raw_files(raw_dir: Path | None = None) -> list[Path]:
    """Devuelve los archivos de datos disponibles en la carpeta raw."""
    base_dir = (raw_dir or RAW_DIR).resolve()
    files = [
        path
        for path in base_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_TEXT_SUFFIXES
    ]
    return sorted(files)


def build_output_path(
    source_path: Path,
    raw_dir: Path | None = None,
    processed_dir: Path | None = None,
    suffix: str | None = None,
) -> Path:
    """Construye la ruta destino preservando la estructura relativa."""
    base_raw_dir = (raw_dir or RAW_DIR).resolve()
    base_processed_dir = (processed_dir or PROCESSED_DIR).resolve()
    relative_path = source_path.relative_to(base_raw_dir)
    if suffix is None:
        return base_processed_dir / relative_path
    return base_processed_dir / relative_path.with_suffix(suffix)


def _read_csv_with_fallback(source_path: Path) -> pd.DataFrame:
    for encoding in ("utf-8", "latin-1", "cp1252"):
        for sep in (",", ";"):
            try:
                return pd.read_csv(source_path, low_memory=False, encoding=encoding, sep=sep)
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
    raise ValueError(f"No se pudo leer como CSV: {source_path}")


def _ingest_tabular_file(source_path: Path, output_path: Path) -> dict[str, Any]:
    suffix = source_path.suffix.lower()
    if suffix == ".csv":
        df = _read_csv_with_fallback(source_path)
        df.to_csv(output_path, index=False)
        return {"status": "ingested", "rows": int(len(df)), "format": "csv", "output": str(output_path)}
    if suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(source_path)
        df.to_csv(output_path.with_suffix(".csv"), index=False)
        return {"status": "ingested", "rows": int(len(df)), "format": "excel", "output": str(output_path.with_suffix(".csv"))}
    if suffix == ".json":
        df = pd.read_json(source_path)
        df.to_csv(output_path.with_suffix(".csv"), index=False)
        return {"status": "ingested", "rows": int(len(df)), "format": "json", "output": str(output_path.with_suffix(".csv"))}
    raise ValueError(f"Formato no soportado para ingesta tabular: {source_path}")


def _ingest_geospatial_file(source_path: Path, output_path: Path) -> dict[str, Any]:
    gdf = gpd.read_file(source_path)
    if output_path.suffix.lower() == ".geojson":
        gdf.to_file(output_path, driver="GeoJSON")
    else:
        gdf.to_file(output_path, driver="GPKG")
    return {"status": "ingested", "rows": int(len(gdf)), "format": "geospatial", "output": str(output_path)}


def ingest_dataset(
    source_path: Path,
    raw_dir: Path | None = None,
    processed_dir: Path | None = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Ingesta un archivo del raw y lo deja disponible en processed."""
    base_raw_dir = (raw_dir or RAW_DIR).resolve()
    base_processed_dir = (processed_dir or PROCESSED_DIR).resolve()
    source_path = source_path.resolve()
    output_path = build_output_path(source_path, raw_dir=base_raw_dir, processed_dir=base_processed_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not overwrite:
        return {"status": "skipped", "output": str(output_path)}

    suffix = source_path.suffix.lower()
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

    return payload


def ingest_all_datasets(
    raw_dir: Path | None = None,
    processed_dir: Path | None = None,
    manifest_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Ejecuta la ingesta inicial para todos los archivos disponibles."""
    base_raw_dir = (raw_dir or RAW_DIR).resolve()
    base_processed_dir = (processed_dir or PROCESSED_DIR).resolve()
    base_processed_dir.mkdir(parents=True, exist_ok=True)

    files = discover_raw_files(base_raw_dir)
    results: list[dict[str, Any]] = []
    for path in files:
        result = ingest_dataset(path, raw_dir=base_raw_dir, processed_dir=base_processed_dir, overwrite=False)
        result["source"] = str(path.relative_to(base_raw_dir))
        results.append(result)

    manifest_file = manifest_path or base_processed_dir / "ingestion_manifest.json"
    manifest_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    return results


def load_raw_csv(filename: str) -> pd.DataFrame:
    path = RAW_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo raw: {path}")
    return pd.read_csv(path, low_memory=False)


def save_raw_copy(df: pd.DataFrame, output_name: str) -> Path:
    destination = RAW_DIR / output_name
    df.to_csv(destination, index=False)
    return destination


def save_processed_csv(df: pd.DataFrame, output_name: str) -> Path:
    destination = PROCESSED_DIR / output_name
    df.to_csv(destination, index=False)
    return destination


if __name__ == "__main__":
    results = ingest_all_datasets()
    print(f"Se procesaron {len(results)} datasets.")
    for item in results:
        print(f"- {item['source']}: {item['status']} ({item.get('format', 'n/a')})")
