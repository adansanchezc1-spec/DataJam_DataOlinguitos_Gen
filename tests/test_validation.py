"""Pruebas unitarias para el módulo de validación de datos (src/validation/validate_data.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
Estándares: PEP 8, ISO/IEC 25010, Clean Code
"""

from __future__ import annotations

import pandas as pd
import pytest

from src.validation.validate_data import (
    LOCALIDADES_BOGOTA_CANONICAS,
    detect_territorial_columns,
    inspect_schema,
    run_full_validation_suite,
    validate_ambiente,
    validate_dataset_quality,
    validate_demografia,
    validate_educacion,
    validate_empleo_economia,
    validate_finanzas,
    validate_infraestructura,
    validate_inversion_fdl,
    validate_modelo_territorial,
    validate_movilidad,
    validate_participacion_ciudadana,
    validate_salud,
    validate_seguridad,
    validate_servicios_publicos,
    validate_territorial_column,
)


class TestValidateData:
    """Suite de pruebas de validación de datos y calidad territorial."""

    def test_inspect_schema_calculates_correct_metrics(self) -> None:
        """Verifica que inspect_schema calcule tipos, nulos y únicos adecuadamente."""
        # Arrange
        df = pd.DataFrame(
            {
                "id": [1, 2, 3, None],
                "nombre": ["Usaquén", "Suba", "Bosa", "Bosa"],
                "activo": [True, False, True, True],
            }
        )

        # Act
        summary = inspect_schema(df)

        # Assert
        assert len(summary) == 3
        id_row = summary[summary["column"] == "id"].iloc[0]
        assert id_row["n_null"] == 1
        assert id_row["pct_null"] == 25.0

        nombre_row = summary[summary["column"] == "nombre"].iloc[0]
        assert nombre_row["n_unique"] == 3

    def test_detect_territorial_columns_finds_candidates(self) -> None:
        """Verifica la detección automática de columnas de localidad."""
        # Arrange
        df = pd.DataFrame(
            {
                "codigo": [1, 2],
                "nom_localidad": ["USAQUEN", "BOSA"],
                "matricula": [100, 200],
            }
        )

        # Act
        detected = detect_territorial_columns(df)

        # Assert
        assert "nom_localidad" in detected
        assert "matricula" not in detected

    def test_validate_territorial_column_recognizes_bogota_localities(self) -> None:
        """Verifica el reconocimiento y cobertura de localidades oficiales."""
        # Arrange
        df = pd.DataFrame(
            {
                "localidad": [
                    "01 - USAQUEN",
                    "Chapinero",
                    "Santa Fe",
                    "San Cristóbal",
                    "Ciudad Bolívar",
                    "OTRA CIUDAD",
                ]
            }
        )

        # Act
        result = validate_territorial_column(df, "localidad")

        # Assert
        assert result["exists"] is True
        assert result["total_localidades_detectadas"] == 5
        assert "USAQUEN" in result["localidades_encontradas"]
        assert "CIUDAD BOLIVAR" in result["localidades_encontradas"]
        assert "OTRA CIUDAD" in result["valores_no_reconocidos"]

    def test_validate_dataset_quality_reports_duplicates_and_nulls(self) -> None:
        """Verifica la evaluación global de calidad de un dataset."""
        # Arrange
        df = pd.DataFrame(
            {
                "localidad": ["Suba", "Suba", "Usaquén"],
                "valor": [10, 10, None],
            }
        )

        # Act
        report = validate_dataset_quality(df, "test_dataset")

        # Assert
        assert report["total_rows"] == 3
        assert report["duplicated_rows"] == 1
        assert report["is_valid"] is True
        assert report["validation_status"] == "APROBADO"

    def test_domain_validators_execute_successfully_with_indicators_and_dates(self) -> None:
        """Verifica que los validadores por dominio incluyan temporalidad, vigencia e indicadores respaldados."""
        validators = [
            validate_demografia,
            validate_salud,
            validate_educacion,
            validate_movilidad,
            validate_infraestructura,
            validate_ambiente,
            validate_finanzas,
            validate_seguridad,
            validate_servicios_publicos,
            validate_inversion_fdl,
            validate_empleo_economia,
            validate_participacion_ciudadana,
            validate_modelo_territorial,
        ]

        for validator in validators:
            report = validator()
            assert isinstance(report, dict)
            assert "domain" in report
            assert "author" in report
            assert "total_rows" in report
            assert report["total_rows"] > 0
            assert "is_valid" in report
            assert "temporalidad" in report, f"Falta temporalidad en {report['domain']}"
            assert "indicadores_respaldados" in report, f"Faltan indicadores en {report['domain']}"
            assert len(report["indicadores_respaldados"]) > 0
            # Validar estructura de indicadores
            ind = report["indicadores_respaldados"][0]
            assert "codigo" in ind
            assert "formula_conceptual" in ind
            assert "denominador" in ind
            assert "estado_factibilidad" in ind

    def test_run_full_validation_suite_generates_all_domains(self) -> None:
        """Verifica que la suite completa ejecute todos los dominios y genere el reporte maestro."""
        res = run_full_validation_suite()
        assert res["total_domains_validated"] == 13
        assert len(res["domains"]) == 13
        assert res["all_domains_valid"] is True
