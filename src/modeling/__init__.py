"""Paquete de Modelado Territorial e Indicadores SIPTA."""

from src.modeling.calculate_indicators import (
    build_ipt_composite_index,
    calculate_camas_por_10000,
    calculate_cupos_por_1000,
    calculate_multidimensional_ipt,
    normalize_min_max,
    save_curated_table,
)

__all__ = [
    "build_ipt_composite_index",
    "calculate_camas_por_10000",
    "calculate_cupos_por_1000",
    "calculate_multidimensional_ipt",
    "normalize_min_max",
    "save_curated_table",
]
