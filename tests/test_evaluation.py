"""Pruebas unitarias para el módulo de evaluación y calidad de resultados (src/evaluation/evaluate_results.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
Estándares: IEEE 829 / ISO 25010 / PEP 8
Requerimiento Funcional: RF-002 (Validación de calidad técnica de datasets), RF-009 (Generación de reportes)
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.evaluation.evaluate_results import (
    detect_outliers,
    quality_report,
    save_quality_report,
)


class TestEvaluateResults:
    """Suite de pruebas para funciones de diagnóstico de calidad y detección de anomalías."""

    @pytest.fixture
    def sample_eval_dataframe(self) -> pd.DataFrame:
        """Crea un DataFrame representativo con nulos, duplicados y tipos mixtos."""
        return pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5],
                "localidad": ["USAQUEN", "SUBA", None, "BOSA", "USAQUEN"],
                "tasa_cobertura": [95.5, 80.2, 45.0, np.nan, 99.1],
                "categoria": ["A", "B", "A", "B", "A"],
            }
        )

    def test_quality_report_calculates_correct_metrics(
        self, sample_eval_dataframe: pd.DataFrame
    ) -> None:
        """RF-002: Verifica el cálculo de columnas, tipos, nulos absolutos, porcentajes y cardinalidad."""
        # Arrange
        df = sample_eval_dataframe

        # Act
        report = quality_report(df)

        # Assert
        assert len(report) == 4
        assert list(report.columns) == ["column", "dtype", "n_null", "pct_null", "n_unique"]

        # Verificar reporte para la columna 'localidad'
        loc_row = report[report["column"] == "localidad"].iloc[0]
        assert loc_row["n_null"] == 1
        assert loc_row["pct_null"] == 20.0
        assert loc_row["n_unique"] == 3

        # Verificar reporte para la columna 'id'
        id_row = report[report["column"] == "id"].iloc[0]
        assert id_row["n_null"] == 0
        assert id_row["pct_null"] == 0.0
        assert id_row["n_unique"] == 5

    def test_detect_outliers_identifies_extreme_values_via_z_score(self) -> None:
        """RF-002: Verifica la detección estadística de anomalías y outliers con umbral Z."""
        # Arrange
        # Serie con 10 valores normales y 1 valor extremo (+10 desviaciones estándar)
        normal_data = [10.0] * 20
        normal_data.append(1000.0)  # Outlier
        series = pd.Series(normal_data)

        # Act
        outliers = detect_outliers(series, z_threshold=3.0)

        # Assert
        assert len(outliers) == 21
        assert not outliers.iloc[0]
        assert outliers.iloc[-1]  # El valor 1000.0 debe ser clasificado como outlier

    def test_detect_outliers_returns_all_false_for_constant_series(self) -> None:
        """Verifica que una serie constante no genere errores ni falsos positivos."""
        # Arrange
        series = pd.Series([5.0, 5.0, 5.0, 5.0])

        # Act
        outliers = detect_outliers(series, z_threshold=3.0)

        # Assert
        assert not outliers.any()

    def test_save_quality_report_persists_csv_file(
        self, sample_eval_dataframe: pd.DataFrame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """RF-009: Verifica que el reporte de calidad se exporte correctamente en CSV."""
        # Arrange
        from src.evaluation import evaluate_results

        monkeypatch.setattr(evaluate_results, "PROCESSED_DIR", tmp_path)
        report = quality_report(sample_eval_dataframe)
        filename = "test_quality_report.csv"

        # Act
        saved_file = save_quality_report(report, filename)

        # Assert
        assert saved_file.exists()
        assert saved_file.name == filename
        loaded = pd.read_csv(saved_file)
        assert len(loaded) == 4
        assert "column" in loaded.columns
