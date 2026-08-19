"""Paquete de Evaluación de Calidad de Datos SIPTA."""

from src.evaluation.evaluate_results import (
    detect_outliers,
    quality_report,
    save_quality_report,
)

__all__ = [
    "detect_outliers",
    "quality_report",
    "save_quality_report",
]
