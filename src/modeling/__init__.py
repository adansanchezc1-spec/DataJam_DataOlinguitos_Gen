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

# Alias para compatibilidad
build_ipt_composite_index = build_ipt
calculate_camas_por_10000 = camas_por_10000
calculate_cupos_por_1000 = cupos_por_1000
save_curated_table = save_indicator_table

__all__ = [
    "build_consolidated_locality_metrics",
    "build_ipt",
    "build_ipt_composite_index",
    "calculate_camas_por_10000",
    "calculate_cupos_por_1000",
    "calculate_consensus_priority",
    "calculate_multidimensional_ipt",
    "camas_por_10000",
    "cupos_por_1000",
    "normalize_min_max",
    "save_curated_table",
    "save_indicator_table",
]

