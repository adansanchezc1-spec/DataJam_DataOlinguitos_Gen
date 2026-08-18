"""Pruebas unitarias para el módulo espacial del EDA (src/eda/spatial.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
"""

from __future__ import annotations

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, Polygon

from src.eda.spatial import (
    count_points_by_locality,
    coverage_matrix,
    load_loca,
    localidades_base,
)


class TestEDASpatial:
    """Suite de pruebas para funciones de cruce espacial y matrices de cobertura."""

    @pytest.fixture
    def mock_loca_gdf(self) -> gpd.GeoDataFrame:
        """Fixture con dos polígonos sintéticos representando localidades."""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
        poly2 = Polygon([(2, 0), (4, 0), (4, 2), (2, 2)])
        return gpd.GeoDataFrame(
            {
                "LocCodigo": [1, 2],
                "LocNombre": ["USAQUEN", "CHAPINERO"],
                "localidad": ["Usaquén", "Chapinero"],
            },
            geometry=[poly1, poly2],
            crs="EPSG:4326",
        )

    @pytest.fixture
    def mock_points_gdf(self) -> gpd.GeoDataFrame:
        """Fixture con puntos georreferenciados."""
        pt1 = Point(1, 1)  # Dentro de Usaquén
        pt2 = Point(1.5, 1.5)  # Dentro de Usaquén
        pt3 = Point(3, 1)  # Dentro de Chapinero
        pt4 = Point(10, 10)  # Fuera de polígonos
        return gpd.GeoDataFrame(
            {"id": [101, 102, 103, 104], "nombre": ["IPS 1", "IPS 2", "IPS 3", "IPS 4"]},
            geometry=[pt1, pt2, pt3, pt4],
            crs="EPSG:4326",
        )

    def test_count_points_by_locality_computes_accurate_intersections(
        self, mock_points_gdf: gpd.GeoDataFrame, mock_loca_gdf: gpd.GeoDataFrame
    ) -> None:
        """Verifica que count_points_by_locality asigne puntos a sus localidades correspondientes."""
        # Act
        counts = count_points_by_locality(mock_points_gdf, mock_loca_gdf)

        # Assert
        assert len(counts) == 2
        usaquen_row = counts[counts["localidad"] == "Usaquén"].iloc[0]
        chapinero_row = counts[counts["localidad"] == "Chapinero"].iloc[0]
        assert usaquen_row["n"] == 2
        assert chapinero_row["n"] == 1

    def test_count_points_by_locality_handles_empty_inputs(
        self, mock_loca_gdf: gpd.GeoDataFrame
    ) -> None:
        """Verifica que entradas vacías retornen un DataFrame con estructura correcta."""
        # Arrange
        empty_pts = gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

        # Act
        res_empty = count_points_by_locality(empty_pts, mock_loca_gdf)
        res_none = count_points_by_locality(None, mock_loca_gdf)

        # Assert
        assert res_empty.empty
        assert "localidad" in res_empty.columns
        assert "n" in res_empty.columns
        assert res_none.empty

    def test_coverage_matrix_merges_multiple_indicators(self) -> None:
        """Verifica que coverage_matrix integre múltiples fuentes a la base de localidades."""
        # Arrange
        base = pd.DataFrame({"localidad": ["Usaquén", "Chapinero", "Suba"]})
        ips_count = pd.DataFrame({"localidad": ["Usaquén", "Chapinero"], "n": [10, 5]})
        colegios_count = pd.DataFrame({"localidad": ["Usaquén", "Suba"], "n": [20, 30]})
        counts = {"salud": ips_count, "educacion": colegios_count}

        # Act
        matrix = coverage_matrix(base, counts, col_name="total")

        # Assert
        assert len(matrix) == 3
        assert "salud::total" in matrix.columns
        assert "educacion::total" in matrix.columns
        usaquen = matrix[matrix["localidad"] == "Usaquén"].iloc[0]
        assert usaquen["salud::total"] == 10
        assert usaquen["educacion::total"] == 20

    def test_localidades_base_returns_21_canonical_entities(self) -> None:
        """Verifica que localidades_base retorne Bogotá + 20 localidades oficiales."""
        # Act
        base = localidades_base()

        # Assert
        assert len(base) == 21
        assert base["localidad"].iloc[0] == "Bogotá"
        assert "Suba" in base["localidad"].values
        assert "Sumapaz" in base["localidad"].values
