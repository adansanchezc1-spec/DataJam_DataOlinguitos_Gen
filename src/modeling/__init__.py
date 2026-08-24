"""Utilidades públicas para el modelado territorial y el cálculo del IPT."""

from src.modeling.calculate_indicators import (
    build_consolidated_locality_metrics,
    build_ipt,
    camas_por_10000,
    calculate_consensus_priority,
    calculate_multidimensional_ipt,
    cupos_por_1000,
    normalize_min_max,
    save_indicator_table,
)
from src.modeling.domain_indicators import (
    build_all_domain_tables,
    build_ambiente_master,
    build_demografia_master,
    build_educacion_master,
    build_empleo_economia_master,
    build_finanzas_master,
    build_infraestructura_master,
    build_movilidad_master,
    build_participacion_master,
    build_salud_master,
    build_seguridad_master,
    build_servicios_publicos_master,
    build_vulnerabilidad_social_master,
    load_unified_territorial_source,
)

# Alias para compatibilidad
build_ipt_composite_index = build_ipt
calculate_camas_por_10000 = camas_por_10000
calculate_cupos_por_1000 = cupos_por_1000
save_curated_table = save_indicator_table

__all__ = [
    "build_all_domain_tables",
    "build_ambiente_master",
    "build_consolidated_locality_metrics",
    "build_demografia_master",
    "build_educacion_master",
    "build_empleo_economia_master",
    "build_finanzas_master",
    "build_infraestructura_master",
    "build_ipt",
    "build_ipt_composite_index",
    "build_movilidad_master",
    "build_participacion_master",
    "build_salud_master",
    "build_seguridad_master",
    "build_servicios_publicos_master",
    "build_vulnerabilidad_social_master",
    "calculate_camas_por_10000",
    "calculate_cupos_por_1000",
    "calculate_consensus_priority",
    "calculate_multidimensional_ipt",
    "camas_por_10000",
    "cupos_por_1000",
    "load_unified_territorial_source",
    "normalize_min_max",
    "save_curated_table",
    "save_indicator_table",
]

