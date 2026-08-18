"""Pruebas unitarias para el módulo de limpieza de datos (src/cleaning/clean_data.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
"""

import pandas as pd
import pytest

from src.cleaning.clean_data import (
    cast_numeric_columns,
    clean_dataset,
    clean_text_columns,
    homologate_localidad,
    standardize_column_names,
)


class TestCleanData:
    """Suite de pruebas de limpieza, estandarización y homologación."""

    def test_standardize_column_names_converts_to_clean_snake_case(self) -> None:
        """Verifica que los nombres de columnas se transformen a snake_case sin tildes."""
        # Arrange
        df = pd.DataFrame(
            {
                "Código Localidad": [1],
                "Población Total (2025)": [1000],
                "Tasa %": [5.2],
            }
        )

        # Act
        df_std = standardize_column_names(df)

        # Assert
        assert "codigo_localidad" in df_std.columns
        assert "poblacion_total_2025" in df_std.columns
        assert "tasa" in df_std.columns

    def test_homologate_localidad_maps_variations_to_canonical_and_divipola(self) -> None:
        """Verifica la homologación correcta a nombres oficiales y códigos DANE."""
        # Arrange
        localidades_input = pd.Series(
            [
                "01 - USAQUEN",
                "Santafé",
                "Ciudad Bolívar",
                "La Candelaria",
                "Sumapaz",
                11,  # Suba por número
            ]
        )

        # Act
        homo_df = homologate_localidad(localidades_input)

        # Assert
        assert homo_df.loc[0, "localidad_canonico"] == "USAQUEN"
        assert homo_df.loc[0, "codigo_divipola"] == "1100101"

        assert homo_df.loc[1, "localidad_canonico"] == "SANTA FE"
        assert homo_df.loc[1, "codigo_divipola"] == "1100103"

        assert homo_df.loc[2, "localidad_canonico"] == "CIUDAD BOLIVAR"
        assert homo_df.loc[3, "localidad_canonico"] == "LA CANDELARIA"
        assert homo_df.loc[4, "localidad_canonico"] == "SUMAPAZ"
        assert homo_df.loc[5, "localidad_canonico"] == "SUBA"
        assert homo_df.loc[5, "codigo_divipola"] == "1100111"

    def test_cast_numeric_columns_cleans_symbols_and_formats(self) -> None:
        """Verifica la conversión a float/int limpiando $, %, espacios y comas."""
        # Arrange
        df = pd.DataFrame(
            {
                "inversion": ["$1,500,000", "$250,000", "0"],
                "porcentaje": ["15.5%", "82.0%", "0%"],
            }
        )

        # Act
        df_cast = cast_numeric_columns(df, ["inversion", "porcentaje"])

        # Assert
        assert df_cast["inversion"].dtype in ["float64", "int64"]
        assert df_cast["inversion"].iloc[0] == 1500000.0
        assert df_cast["porcentaje"].iloc[0] == 15.5

    def test_clean_dataset_pipeline_executes_end_to_end(self) -> None:
        """Verifica la ejecución del pipeline integral de limpieza sobre un dataset."""
        # Arrange
        df = pd.DataFrame(
            {
                "Nombre Localidad": ["01 - USAQUEN", "Bosa"],
                "Presupuesto $": ["$10,000", "$20,000"],
            }
        )

        # Act
        df_clean = clean_dataset(
            df, locality_col="Nombre Localidad", numeric_cols=["Presupuesto $"]
        )

        # Assert
        assert "localidad_canonico" in df_clean.columns
        assert "codigo_divipola" in df_clean.columns
        assert df_clean["localidad_canonico"].iloc[0] == "USAQUEN"
        assert df_clean["presupuesto"].iloc[0] == 10000.0
