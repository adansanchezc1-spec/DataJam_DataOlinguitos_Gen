"""Pruebas unitarias para el módulo de visualización exploratoria (src/eda/viz.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
Estándares: IEEE 829 / ISO 25010 / PEP 8
Requerimiento Funcional: RF-010 (Estructuración y renderizado visual para EDA y tableros)
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import pytest

from src.eda.viz import (
    PALETTE,
    barras,
    boxplot,
    heatmap_nulos,
    histograma,
    mapa,
    serie_temporal,
    set_style,
)


class TestEDAViz:
    """Suite de pruebas unitarias para funciones de visualización gráfica en EDA."""

    @pytest.fixture(autouse=True)
    def setup_matplotlib_clean(self):
        """Limpia figuras de matplotlib antes y después de cada test."""
        plt.close("all")
        yield
        plt.close("all")

    def test_set_style_configures_rcparams(self) -> None:
        """RF-010: Verifica que set_style configure correctamente las fuentes y propiedades de matplotlib."""
        # Act
        set_style()

        # Assert
        assert plt.rcParams["figure.dpi"] == 110
        assert plt.rcParams["axes.spines.top"] is False
        assert plt.rcParams["axes.spines.right"] is False

    def test_histograma_renders_continuous_variable(self) -> None:
        """RF-010: Verifica el renderizado de histogramas para variables numéricas continuas."""
        # Arrange
        series = pd.Series(np.random.normal(50, 10, 100), name="variable_continua")

        # Act
        ax = histograma(series, title="Test Histograma Continuo")

        # Assert
        assert ax is not None
        assert "Test Histograma Continuo" in ax.get_title()
        assert ax.get_xlabel() == "variable_continua"

    def test_histograma_renders_discrete_variable(self) -> None:
        """RF-010: Verifica que histograma adapte la visualización para enteros discretos."""
        # Arrange
        series = pd.Series([1, 2, 2, 3, 3, 3, 4, 4, 5], name="variable_discreta")

        # Act
        ax = histograma(series, title="Test Histograma Discreto")

        # Assert
        assert ax is not None
        assert ax.get_title() == "Test Histograma Discreto"

    def test_histograma_handles_empty_or_non_numeric_series(self) -> None:
        """Verifica que histograma retorne None de manera segura para series vacías o no numéricas."""
        # Arrange
        empty_series = pd.Series([], name="vacio", dtype=float)
        non_numeric_series = pd.Series(["a", "b", "c"], name="texto")

        # Act & Assert
        assert histograma(empty_series) is None
        assert histograma(non_numeric_series) is None

    def test_boxplot_renders_distribution_and_outliers(self) -> None:
        """RF-010: Verifica el cálculo y dibujo de boxplots descriptivos."""
        # Arrange
        series = pd.Series([10, 12, 14, 15, 16, 18, 20, 100], name="metrica_boxplot")

        # Act
        ax = boxplot(series, title="Test Boxplot")

        # Assert
        assert ax is not None
        assert "Test Boxplot" in ax.get_title()
        assert ax.get_xlabel() == "metrica_boxplot"

    def test_boxplot_handles_empty_series(self) -> None:
        """Verifica que boxplot retorne None ante una serie sin valores válidos."""
        assert boxplot(pd.Series([], dtype=float)) is None

    def test_barras_renders_categorical_frequencies(self) -> None:
        """RF-010: Verifica la visualización de frecuencias por categoría con etiquetas de porcentaje."""
        # Arrange
        series = pd.Series(["Usaquén", "Suba", "Suba", "Bosa", "Bosa", "Bosa"], name="localidades")

        # Act
        ax = barras(series, title="Frecuencia por Localidad", top_n=5)

        # Assert
        assert ax is not None
        assert ax.get_title() == "Frecuencia por Localidad"

    def test_heatmap_nulos_renders_null_percentages(self) -> None:
        """RF-002: Verifica que el gráfico de nulos reporte correctamente las columnas con datos faltantes."""
        # Arrange
        df = pd.DataFrame(
            {
                "col_completa": [1, 2, 3, 4],
                "col_con_nulos": [1, None, None, 4],
                "col_muy_nula": [None, None, None, 4],
            }
        )

        # Act
        ax = heatmap_nulos(df, title="Auditoría de Nulos")

        # Assert
        assert ax is not None
        assert ax.get_title() == "Auditoría de Nulos"

    def test_heatmap_nulos_returns_none_when_no_nulls(self) -> None:
        """Verifica que heatmap_nulos retorne None cuando no hay valores nulos en el dataset."""
        df_clean = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        assert heatmap_nulos(df_clean) is None

    def test_mapa_renders_point_geodataframe(self) -> None:
        """RF-004: Verifica el trazado de geometrías de puntos en el mapa territorial."""
        # Arrange
        gdf_points = gpd.GeoDataFrame(
            {"id": [1, 2], "nombre": ["P1", "P2"]},
            geometry=[Point(-74.05, 4.65), Point(-74.10, 4.60)],
            crs="EPSG:4326",
        )

        # Act
        ax = mapa(gdf_points, title="Puntos Territoriales")

        # Assert
        assert ax is not None
        assert ax.get_title() == "Puntos Territoriales"

    def test_mapa_renders_polygon_choropleth(self) -> None:
        """RF-004: Verifica el trazado de mapas coropléticos para polígonos distritales."""
        # Arrange
        poly1 = Polygon([(-74.05, 4.65), (-74.04, 4.65), (-74.04, 4.66), (-74.05, 4.65)])
        poly2 = Polygon([(-74.10, 4.60), (-74.09, 4.60), (-74.09, 4.61), (-74.10, 4.60)])
        gdf_polys = gpd.GeoDataFrame(
            {"localidad": ["L1", "L2"], "ipt": [45.0, 85.0]},
            geometry=[poly1, poly2],
            crs="EPSG:4326",
        )

        # Act
        ax = mapa(gdf_polys, title="Coroplético IPT", column="ipt")

        # Assert
        assert ax is not None
        assert ax.get_title() == "Coroplético IPT"

    def test_mapa_returns_none_for_invalid_or_empty_geodataframe(self) -> None:
        """Verifica que mapa retorne None si el GeoDataFrame es nulo, vacío o sin geometría."""
        assert mapa(None, "Mapa Nulo") is None
        assert mapa(pd.DataFrame({"a": [1]}), "Sin Geometria") is None

    def test_serie_temporal_renders_line_plot(self) -> None:
        """RF-010: Verifica el renderizado de series de tiempo multivariadas."""
        # Arrange
        df_time = pd.DataFrame(
            {
                "fecha": pd.date_range("2024-01-01", periods=6, freq="ME"),
                "demanda_validaciones": [100, 120, 115, 140, 135, 150],
                "sector": ["Troncal", "Troncal", "Troncal", "Zonal", "Zonal", "Zonal"],
            }
        )

        # Act
        ax = serie_temporal(
            df_time,
            x="fecha",
            y="demanda_validaciones",
            hue="sector",
            title="Evolución Mensual de Demanda",
        )

        # Assert
        assert ax is not None
        assert ax.get_title() == "Evolución Mensual de Demanda"
