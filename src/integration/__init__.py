"""Paquete de Integración Territorial SIPTA."""

from src.integration.integrate_data import (
    AREAS_LOCALIDADES_KM2,
    build_master_table,
    get_canonical_localities_base,
    load_demografia_localidades,
    load_movilidad_infraestructura_coverage,
    merge_by_locality,
    save_master_table,
)

__all__ = [
    "AREAS_LOCALIDADES_KM2",
    "build_master_table",
    "get_canonical_localities_base",
    "load_demografia_localidades",
    "load_movilidad_infraestructura_coverage",
    "merge_by_locality",
    "save_master_table",
]
