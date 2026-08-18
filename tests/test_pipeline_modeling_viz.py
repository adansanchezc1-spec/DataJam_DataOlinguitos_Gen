"""Pruebas unitarias para integración, modelado y visualización de SIPTA (src/integration, src/modeling, src/visualization).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import pytest

from src.integration.integrate_data import (
    merge_by_locality,
    save_master_table,
)
from src.modeling.calculate_indicators import (
    build_ipt,
    camas_por_10000,
    cupos_por_1000,
    normalize_min_max,
)
from src.visualization.prepare_visualization import (
    build_ranking,
    export_for_dashboard,
)


class TestPipelineModelingViz:
    """Suite de pruebas para consolidación territorial, cálculo de IPT y exportación."""

    @pytest.fixture
    def sample_integration_dfs(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Crea dos DataFrames homologados para probar integración territorial."""
        df_base = pd.DataFrame(
            {
                "localidad_canonico": ["USAQUEN", "SUBA", "BOSA"],
                "poblacion": [500000, 1200000, 700000],
            }
        )
        df_salud = pd.DataFrame(
            {
                "localidad_canonico": ["USAQUEN", "SUBA", "BOSA"],
                "total_ips": [560, 312, 46],
                "camas": [1500, 800, 120],
            }
        )
        return df_base, df_salud

    def test_merge_by_locality_combines_sector_data(
        self, sample_integration_dfs: tuple[pd.DataFrame, pd.DataFrame]
    ) -> None:
        """Verifica la unión exitosa de datasets por columna territorial homologada."""
        # Arrange
        df_base, df_salud = sample_integration_dfs

        # Act
        df_merged = merge_by_locality(df_base, df_salud, locality_col="localidad_canonico")

        # Assert
        assert len(df_merged) == 3
        assert "poblacion" in df_merged.columns
        assert "total_ips" in df_merged.columns
        assert df_merged["total_ips"].iloc[0] == 560

    def test_merge_by_locality_raises_error_if_col_missing(self) -> None:
        """Verifica que se lance ValueError si no se encuentra la columna de unión."""
        # Arrange
        df1 = pd.DataFrame({"col_a": [1, 2]})
        df2 = pd.DataFrame({"col_b": [3, 4]})

        # Act & Assert
        with pytest.raises(ValueError):
            merge_by_locality(df1, df2, locality_col="localidad_canonico")

    def test_normalize_min_max_scales_series_to_unit_interval(self) -> None:
        """Verifica que normalize_min_max escale los valores numéricos entre 0 y 1."""
        # Arrange
        series = pd.Series([10, 20, 30, 40, 50])

        # Act
        norm = normalize_min_max(series)

        # Assert
        assert norm.min() == 0.0
        assert norm.max() == 1.0
        assert norm.iloc[2] == 0.5

    def test_camas_por_10000_calculates_correct_ratios(self) -> None:
        """Verifica el cálculo de camas por 10.000 habitantes."""
        # Arrange
        df = pd.DataFrame({"camas": [100, 250], "poblacion": [500000, 1000000]})

        # Act
        ratios = camas_por_10000(df, camas_col="camas", pop_col="poblacion")

        # Assert
        assert pytest.approx(ratios.iloc[0], 0.01) == 2.0
        assert pytest.approx(ratios.iloc[1], 0.01) == 2.5

    def test_cupos_por_1000_calculates_correct_ratios(self) -> None:
        """Verifica el cálculo de cupos escolares por 1.000 personas en edad escolar."""
        # Arrange
        df = pd.DataFrame({"cupos": [5000, 8000], "poblacion_objetivo": [50000, 100000]})

        # Act
        ratios = cupos_por_1000(df, cupos_col="cupos", pop_obj_col="poblacion_objetivo")

        # Assert
        assert pytest.approx(ratios.iloc[0], 0.01) == 100.0
        assert pytest.approx(ratios.iloc[1], 0.01) == 80.0

    def test_build_ipt_composite_index_and_weights(self) -> None:
        """Verifica la construcción del Índice de Priorización Territorial ponderado."""
        # Arrange
        df = pd.DataFrame(
            {
                "deficit_salud": [10, 50, 90],
                "deficit_educacion": [20, 60, 80],
            }
        )
        component_cols = {"salud": "deficit_salud", "educacion": "deficit_educacion"}
        weights = {"salud": 0.5, "educacion": 0.5}

        # Act
        ipt = build_ipt(df, component_cols=component_cols, weights=weights)

        # Assert
        assert len(ipt) == 3
        assert ipt.min() >= 0.0
        assert ipt.max() <= 100.0

    def test_build_ranking_sorts_descending(self) -> None:
        """Verifica el ordenamiento descendente para el ranking territorial."""
        # Arrange
        df = pd.DataFrame(
            {
                "localidad": ["Usaquén", "Suba", "Bosa"],
                "ipt": [25.5, 80.2, 45.0],
            }
        )

        # Act
        ranked = build_ranking(df, score_column="ipt")

        # Assert
        assert ranked["localidad"].iloc[0] == "Suba"
        assert ranked["localidad"].iloc[1] == "Bosa"
        assert ranked["localidad"].iloc[2] == "Usaquén"
