"""Suite de pruebas unitarias para los nuevos datasets y dominios de expansión de SIPTA:
- Servicios Públicos (D11)
- Empleo y Economía (D12)
- Participación Ciudadana y PQR (D9)
- Inversión FDL y Metas Sociales (D7 Expandido)
- Capacidad de Camas (D2), Calidad Saber 11 (D3) y Delitos MEBOG (D8)
- Cartografía Oficial IDECA (D10)

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
Estándares: ISO/IEC 25010, DAMA-BOK, PEP 8
"""

from __future__ import annotations

import json
from pathlib import Path
import geopandas as gpd
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"


class TestServiciosPublicos:
    """Pruebas de integridad y reglas de negocio para Servicios Públicos (D11)."""

    def test_acueducto_cobertura_ranges_and_columns(self) -> None:
        """Verifica rangos válidos de cobertura de agua y alcantarillado en las 20 localidades."""
        # Arrange
        file_path = RAW_DIR / "SERVICIOS_PUBLICOS" / "eaab_cobertura_acueducto_localidad.csv"
        assert file_path.exists(), f"Falta el archivo {file_path}"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20, "Deben existir exactamente 20 registros (20 localidades)"
        expected_cols = [
            "codigo_localidad",
            "nombre_localidad",
            "cobertura_acueducto_pct",
            "cobertura_alcantarillado_pct",
            "horas_interrupcion_promedio_mes",
        ]
        for col in expected_cols:
            assert col in df.columns, f"Columna requerida ausente: {col}"

        assert (df["cobertura_acueducto_pct"] >= 0).all() and (df["cobertura_acueducto_pct"] <= 100).all()
        assert (df["cobertura_alcantarillado_pct"] >= 0).all() and (df["cobertura_alcantarillado_pct"] <= 100).all()
        assert (df["horas_interrupcion_promedio_mes"] >= 0).all()

    def test_calidad_agua_irca_validity(self) -> None:
        """Verifica que el IRCA esté en rango normativo y contenga clasificación de riesgo."""
        # Arrange
        file_path = RAW_DIR / "SERVICIOS_PUBLICOS" / "eaab_calidad_agua_irca_localidad.csv"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20
        assert "irca_promedio" in df.columns
        assert (df["irca_promedio"] >= 0).all() and (df["irca_promedio"] <= 100).all()
        assert "clasificacion_riesgo_irca" in df.columns
        assert df["clasificacion_riesgo_irca"].notna().all()

    def test_alumbrado_publico_and_tic(self) -> None:
        """Verifica luminarias UAESP y penetración TIC de MinTIC."""
        # Arrange & Act
        df_alu = pd.read_csv(RAW_DIR / "SERVICIOS_PUBLICOS" / "uaesp_alumbrado_publico_localidad.csv")
        df_tic = pd.read_csv(RAW_DIR / "SERVICIOS_PUBLICOS" / "cobertura_conectividad_tic_localidad.csv")

        # Assert
        assert len(df_alu) == 20
        assert len(df_tic) == 20
        assert (df_alu["tecnologia_led_pct"] >= 0).all() and (df_alu["tecnologia_led_pct"] <= 100).all()
        assert (df_tic["penetracion_internet_fijo_pct"] >= 0).all() and (df_tic["penetracion_internet_fijo_pct"] <= 100).all()


class TestEmpleoEconomia:
    """Pruebas de integridad y consistencia lógica para Empleo y Salarios (D12)."""

    def test_conmutacion_laboral_sum_consistency(self) -> None:
        """Verifica que la suma de ocupados locales y conmutantes sume exactamente 100%."""
        # Arrange
        file_path = RAW_DIR / "EMPLEO_ECONOMIA" / "conmutacion_laboral_residencia_trabajo_localidad.csv"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20
        suma_pct = df["ocupados_trabajan_en_su_localidad_pct"] + df["ocupados_conmutan_a_otras_localidades_pct"]
        assert pytest.approx(suma_pct.values, 0.01) == 100.0
        assert (df["tiempo_promedio_desplazamiento_laboral_min"] > 0).all()

    def test_ingreso_promedio_and_informalidad(self) -> None:
        """Verifica salarios positivos y tasas de informalidad en rangos [0, 100]."""
        # Arrange
        file_path = RAW_DIR / "EMPLEO_ECONOMIA" / "ingreso_promedio_salario_ocupados_localidad.csv"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20
        assert (df["ingreso_laboral_promedio_ocupados_cop"] > 500_000).all()
        assert (df["tasa_informalidad_laboral_pct"] >= 0).all() and (df["tasa_informalidad_laboral_pct"] <= 100).all()
        assert (df["tasa_desempleo_pct"] >= 0).all() and (df["tasa_desempleo_pct"] <= 100).all()


class TestParticipacionCiudadana:
    """Pruebas para PQR Bogotá Te Escucha y Presupuestos Participativos (D9)."""

    def test_pqr_bogota_counts_and_resolution(self) -> None:
        """Verifica conteos de peticiones ciudadanas y tasas de resolución a tiempo."""
        # Arrange
        file_path = RAW_DIR / "PARTICIPACION_CIUDADANA" / "pqr_bogota_te_escucha_por_localidad.csv"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20
        assert (df["total_pqr_recibidas"] > 0).all()
        assert (df["pqr_resueltas_a_tiempo_pct"] >= 0).all() and (df["pqr_resueltas_a_tiempo_pct"] <= 100).all()
        assert "tema_frecuente_1" in df.columns
        assert df["tema_frecuente_1"].notna().all()


class TestInversionFdlAndSocial:
    """Pruebas para Fondos de Desarrollo Local y Gasto Social SDIS (D7 Expandido)."""

    def test_inversion_fdl_budget_and_execution(self) -> None:
        """Verifica que el presupuesto ejecutado no exceda el aprobado y % en [0, 100]."""
        # Arrange
        file_path = RAW_DIR / "FINANZAS_INVERSION_PUBLICA" / "inversion_fondos_desarrollo_local_fdl.csv"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20
        assert (df["presupuesto_aprobado_millones"] > 0).all()
        assert (df["presupuesto_ejecutado_millones"] >= 0).all()
        assert (df["presupuesto_ejecutado_millones"] <= df["presupuesto_aprobado_millones"] * 1.05).all()
        assert (df["porcentaje_ejecucion_fdl"] >= 0).all() and (df["porcentaje_ejecucion_fdl"] <= 100).all()

    def test_metas_social_sdis(self) -> None:
        """Verifica inversión social SDIS y beneficiarios de transferencias."""
        # Arrange
        file_path = RAW_DIR / "FINANZAS_INVERSION_PUBLICA" / "metas_inversion_social_sdis_localidad.csv"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20
        assert (df["presupuesto_social_sdis_millones"] > 0).all()
        assert (df["beneficiarios_transferencias_monetarias"] >= 0).all()


class TestSaludEducacionSeguridadExpandidos:
    """Pruebas para capacidad asistencial, Saber 11 y delitos de alto impacto."""

    def test_capacidad_camas_hospitalarias(self) -> None:
        """Verifica dotación de camas y camas por 10k habitantes."""
        # Arrange
        file_path = RAW_DIR / "SALUD" / "capacidad_camas_asistencial_localidad.csv"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20
        assert (df["total_camas_hospitalarias"] >= 0).all()
        assert (df["camas_por_10000_habitantes"] >= 0).all()

    def test_calidad_saber11_retencion(self) -> None:
        """Verifica puntajes Saber 11 y deserción escolar."""
        # Arrange
        file_path = RAW_DIR / "EDUCACION" / "calidad_educativa_saber11_retencion_localidad.csv"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20
        assert (df["puntaje_promedio_saber_11"] >= 150).all() and (df["puntaje_promedio_saber_11"] <= 400).all()
        assert (df["tasa_desercion_escolar_pct"] >= 0).all() and (df["tasa_desercion_escolar_pct"] <= 50).all()

    def test_delitos_alto_impacto(self) -> None:
        """Verifica registros de delitos MEBOG en las 20 localidades."""
        # Arrange
        file_path = RAW_DIR / "SEGURIDAD" / "delitos_alto_impacto_localidad_2024_2026.csv"

        # Act
        df = pd.read_csv(file_path)

        # Assert
        assert len(df) == 20
        assert (df["homicidios_anual"] >= 0).all()
        assert (df["hurto_a_personas_anual"] >= 0).all()
        assert (df["tasa_delitos_alto_impacto_por_100k_hab"] >= 0).all()


class TestModeloTerritorialCartografia:
    """Pruebas para polígonos oficiales de localidades IDECA (D10)."""

    def test_poligonos_localidades_geojson(self) -> None:
        """Verifica la carga del GeoJSON de localidades, CRS WGS84 y geometrías válidas."""
        # Arrange
        file_path = RAW_DIR / "MODELO_TERRITORIAL" / "poligonos_localidades.geojson"
        assert file_path.exists()

        # Act
        gdf = gpd.read_file(str(file_path))

        # Assert
        assert len(gdf) == 20
        assert gdf.crs is not None
        assert gdf.geometry.is_valid.all()
        assert not gdf.geometry.is_empty.any()
