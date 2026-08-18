"""Módulo de exploración de datos (EDA) para el proyecto SIPTA.

Provee lectores robustos, perfilado estadístico, reglas de calidad,
catálogo de indicadores, visualizaciones y helpers espaciales que
los notebooks de `notebooks/eda/` reutilizan.
"""

from src.eda.readers import (
    read_any,
    read_csv_robust,
    read_geojson,
    read_gpkg_layer,
    read_gtfs_zip,
    read_xlsx_sheet,
)
from src.eda.profiling import (
    clasificar_variables,
    column_profile,
    dataset_profile,
    detect_territorial_columns,
    standardize_locality,
    variables_profile,
)
from src.eda.quality import profile_file, load_dataset, load_dataset_layer
from src.eda.indicators import indicator_status, load_approved, load_catalog
from src.eda.explore import explorar_dataset

__all__ = [
    "read_any",
    "read_csv_robust",
    "read_geojson",
    "read_gpkg_layer",
    "read_gtfs_zip",
    "read_xlsx_sheet",
    "clasificar_variables",
    "column_profile",
    "dataset_profile",
    "detect_territorial_columns",
    "standardize_locality",
    "variables_profile",
    "profile_file",
    "load_dataset",
    "load_dataset_layer",
    "indicator_status",
    "load_approved",
    "load_catalog",
    "explorar_dataset",
]
