"""Pruebas unitarias para el módulo de ingeniería de características (src/features/feature_engineering.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
Estándares: IEEE 829 / ISO 25010 / PEP 8
Requerimiento Funcional: RF-005 (Cálculo de variables e indicadores per cápita y densidad)
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import pytest

from src.features.feature_engineering import (
    add_density,
    add_ratio,
    save_feature_table,
)


class TestFeatureEngineering:
    """Suite de pruebas unitarias para transformaciones y feature engineering."""

    @pytest.fixture
    def sample_territorial_df(self) -> pd.DataFrame:
        """Fixture con métricas territoriales de muestra para cálculo de densidades y ratios."""
        return pd.DataFrame(
            {
                "localidad": ["USAQUEN", "CHAPINERO", "SANTA FE"],
                "poblacion": [500000.0, 150000.0, 100000.0],
                "area_km2": [65.0, 38.0, 37.0],
                "camas": [1200, 800, 450],
                "ips_total": [50, 40, 25],
            }
        )

    def test_add_density_calculates_population_density_correctly(
        self, sample_territorial_df: pd.DataFrame
    ) -> None:
        """RF-005: Verifica el cálculo exacto de la densidad poblacional (hab/km2)."""
        # Arrange
        df = sample_territorial_df.copy()

        # Act
        result = add_density(df, population_col="poblacion", area_col="area_km2")

        # Assert
        assert "densidad_poblacional" in result.columns
        assert pytest.approx(result["densidad_poblacional"].iloc[0], 0.01) == 500000.0 / 65.0
        assert pytest.approx(result["densidad_poblacional"].iloc[1], 0.01) == 150000.0 / 38.0
        assert len(result) == len(df)

    def test_add_density_returns_unmodified_copy_if_columns_missing(self) -> None:
        """Verifica que add_density maneje graciosamente dataframes sin las columnas requeridas."""
        # Arrange
        df = pd.DataFrame({"col_x": [1, 2, 3]})

        # Act
        result = add_density(df, population_col="poblacion", area_col="area_km2")

        # Assert
        assert "densidad_poblacional" not in result.columns
        assert list(result.columns) == ["col_x"]

    def test_add_ratio_computes_custom_quotient(
        self, sample_territorial_df: pd.DataFrame
    ) -> None:
        """RF-005: Verifica el cálculo de ratios y proporciones personalizadas entre columnas."""
        # Arrange
        df = sample_territorial_df.copy()

        # Act
        result = add_ratio(
            df,
            numerator="camas",
            denominator="ips_total",
            output_name="camas_por_ips",
        )

        # Assert
        assert "camas_por_ips" in result.columns
        assert pytest.approx(result["camas_por_ips"].iloc[0], 0.01) == 1200 / 50
        assert pytest.approx(result["camas_por_ips"].iloc[1], 0.01) == 800 / 40

    @pytest.mark.parametrize(
        "missing_numerator,missing_denominator",
        [
            ("col_inexistente", "ips_total"),
            ("camas", "col_inexistente"),
            ("col_a", "col_b"),
        ],
    )
    def test_add_ratio_handles_missing_columns(
        self,
        sample_territorial_df: pd.DataFrame,
        missing_numerator: str,
        missing_denominator: str,
    ) -> None:
        """Verifica la robustez de add_ratio cuando faltan una o ambas columnas."""
        # Arrange
        df = sample_territorial_df.copy()

        # Act
        result = add_ratio(
            df,
            numerator=missing_numerator,
            denominator=missing_denominator,
            output_name="ratio_test",
        )

        # Assert
        assert "ratio_test" not in result.columns

    def test_save_feature_table_exports_csv_to_processed_dir(
        self, sample_territorial_df: pd.DataFrame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """RF-009: Verifica la persistencia adecuada de la tabla de características generada."""
        # Arrange
        from src.features import feature_engineering

        monkeypatch.setattr(feature_engineering, "PROCESSED_DIR", tmp_path)
        filename = "features_test_output.csv"

        # Act
        saved_path = save_feature_table(sample_territorial_df, filename)

        # Assert
        assert saved_path.exists()
        assert saved_path.name == filename
        loaded_df = pd.read_csv(saved_path)
        assert len(loaded_df) == len(sample_territorial_df)
        assert list(loaded_df.columns) == list(sample_territorial_df.columns)
