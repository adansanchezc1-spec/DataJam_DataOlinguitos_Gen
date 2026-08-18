"""Pruebas unitarias para el módulo de perfilado estadístico del EDA (src/eda/profiling.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
"""

from __future__ import annotations

import pandas as pd
import pytest

from src.eda.profiling import (
    CODIGO_LOCALIDAD_A_NOMBRE,
    LOCALIDADES_20,
    clasificar_variables,
    dataset_profile,
    localidad_de_codigo,
    normalize_text,
    standardize_locality,
    strip_accents,
    variables_profile,
)


class TestEDAProfiling:
    """Suite de pruebas para funciones de perfilado y estandarización textual/territorial."""

    def test_strip_accents_removes_diacritics_correctly(self) -> None:
        """Verifica que strip_accents remueva tildes y caracteres combinados."""
        # Arrange
        texto = "Bogotá - Usaquén, Engativá y San Cristóbal"

        # Act
        resultado = strip_accents(texto)

        # Assert
        assert resultado == "Bogota - Usaquen, Engativa y San Cristobal"

    def test_strip_accents_handles_na_and_none(self) -> None:
        """Verifica que strip_accents maneje valores nulos sin lanzar excepción."""
        # Arrange & Act
        res_none = strip_accents(None)
        res_nan = strip_accents(pd.NA)

        # Assert
        assert res_none == ""
        assert res_nan == ""

    def test_normalize_text_removes_spaces_and_converts_lowercase(self) -> None:
        """Verifica la normalización de espacios múltiples y mayúsculas."""
        # Arrange
        texto = "   CIUDAD    BOLÍVAR   "

        # Act
        resultado = normalize_text(texto)

        # Assert
        assert resultado == "ciudad bolivar"

    @pytest.mark.parametrize(
        ("input_val", "expected_canonico"),
        [
            ("Usaquén", "Usaquén"),
            ("usaquen", "Usaquén"),
            ("candelaria", "La Candelaria"),
            ("La Candelaria", "La Candelaria"),
            ("SAN CRISTOBAL SUR", "San Cristóbal"),
            ("santafe", "Santa Fe"),
            ("RAFAEL URIBE", "Rafael Uribe Uribe"),
            ("1", "Usaquén"),
            (11, "Suba"),
            (20, "Sumapaz"),
            ("0", "Bogotá"),
        ],
    )
    def test_standardize_locality_maps_known_and_numeric_values(
        self, input_val: str | int, expected_canonico: str
    ) -> None:
        """Verifica que standardize_locality resuelva nombres con variantes y códigos numéricos."""
        # Act
        resultado = standardize_locality(input_val)

        # Assert
        assert resultado == expected_canonico

    def test_standardize_locality_invalid_returns_na(self) -> None:
        """Verifica que valores desconocidos retornen pd.NA."""
        # Arrange & Act
        resultado = standardize_locality("Municipio Inexistente 99")

        # Assert
        assert pd.isna(resultado)

    def test_localidad_de_codigo_maps_integers(self) -> None:
        """Verifica que localidad_de_codigo mapee códigos 1-20 a nombres canónicos."""
        # Arrange & Act & Assert
        assert localidad_de_codigo(1) == "Usaquén"
        assert localidad_de_codigo("11") == "Suba"
        assert localidad_de_codigo(20) == "Sumapaz"
        assert pd.isna(localidad_de_codigo(99))

    def test_dataset_profile_computes_accurate_metrics(self) -> None:
        """Verifica el cálculo de filas, columnas, duplicados y porcentaje de nulos."""
        # Arrange
        df = pd.DataFrame(
            {
                "localidad": ["Suba", "Suba", "Usaquén", "Kennedy"],
                "valor": [10.0, 10.0, None, 25.0],
                "categoria": ["A", "A", "B", "C"],
            }
        )

        # Act
        profile = dataset_profile(df)

        # Assert
        assert profile["filas"] == 4
        assert profile["columnas"] == 3
        assert profile["duplicados"] == 1
        assert "localidad" in profile["columnas_territoriales"]
        assert profile["pct_nulos_total"] > 0

    def test_clasificar_variables_detects_data_types(self) -> None:
        """Verifica la clasificación de variables en numéricas, categóricas y territoriales."""
        # Arrange
        df = pd.DataFrame(
            {
                "localidad_nombre": ["Suba", "Bosa"],
                "matricula": [1200, 3400],
                "fecha": pd.date_range("2025-01-01", periods=2),
                "sector": ["Oficial", "Privado"],
            }
        )

        # Act
        clasif = clasificar_variables(df)

        # Assert
        assert len(clasif) == 4
        cols = clasif["columna"].tolist()
        assert "localidad_nombre" in cols
        assert "matricula" in cols

    def test_variables_profile_computes_descriptive_stats(self) -> None:
        """Verifica que variables_profile genere estadísticas resumen por variable."""
        # Arrange
        df = pd.DataFrame(
            {
                "edad": [10, 20, 30, 40, None],
                "genero": ["M", "F", "F", "M", "F"],
            }
        )

        # Act
        stats = variables_profile(df)

        # Assert
        assert len(stats) == 2
        edad_stats = stats[stats["columna"] == "edad"].iloc[0]
        assert edad_stats["n_nulos"] == 1
        assert edad_stats["media"] == 25.0
