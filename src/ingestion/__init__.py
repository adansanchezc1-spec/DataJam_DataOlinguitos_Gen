"""Paquete de Ingesta Territorial SIPTA."""

from src.ingestion.ingest_data import (
    build_output_path,
    discover_raw_files,
    ingest_all_datasets,
    ingest_dataset,
)

__all__ = [
    "build_output_path",
    "discover_raw_files",
    "ingest_all_datasets",
    "ingest_dataset",
]
