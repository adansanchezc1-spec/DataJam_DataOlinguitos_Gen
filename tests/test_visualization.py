"""Pruebas unitarias para el módulo de preparación de visualizaciones (src/visualization/prepare_visualization.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
Estándares: IEEE 829 / ISO 25010 / PEP 8
Requerimiento Funcional: RF-007 (Consolidación de ranking e IPT), RF-010 (Preparación de datos para tableros)
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import pytest

from src.visualization.prepare_visualization import (
    build_ranking,
    export_for_dashboard,
    load_curated_dataset,
)


class TestVisualization:
    """Suite de pruebas para funciones de carga curada, ranking y exportación para dashboard."""

    @pytest.fixture
    def sample_ipt_df(self) -> pd.DataFrame:
        """Fixture con localidades y puntajes IPT calculados."""
        return pd.DataFrame(
            {
                "localidad": ["BOSA", "USAQUEN", "CIUDAD BOLIVAR", "SUBA"],
                "ipt": [82.5, 34.0, 89.1, 55.4],
                "nivel_prioridad": ["ALTO", "BAJO", "MUY_ALTO", "MEDIO"],
            }
        )

    def test_build_ranking_sorts_descending_by_score(self, sample_ipt_df: pd.DataFrame) -> None:
        """RF-007: Verifica que build_ranking ordene descendentemente según el puntaje IPT."""
        # Arrange
        df = sample_ipt_df

        # Act
        ranked = build_ranking(df, score_column="ipt")

        # Assert
        assert len(ranked) == 4
        assert ranked["localidad"].iloc[0] == "CIUDAD BOLIVAR"
        assert ranked["localidad"].iloc[1] == "BOSA"
        assert ranked["localidad"].iloc[2] == "SUBA"
        assert ranked["localidad"].iloc[3] == "USAQUEN"
        assert ranked["ipt"].iloc[0] == 89.1

    def test_build_ranking_raises_key_error_if_column_missing(self) -> None:
        """Verifica que se lance KeyError cuando no existe la columna de puntaje especificada."""
        # Arrange
        df = pd.DataFrame({"col_a": [1, 2]})

        # Act & Assert
        with pytest.raises(KeyError, match="No existe la columna"):
            build_ranking(df, score_column="ipt_inexistente")

    def test_export_for_dashboard_writes_file_to_curated(
        self, sample_ipt_df: pd.DataFrame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """RF-010: Verifica que export_for_dashboard guarde el archivo en el directorio curated."""
        # Arrange
        from src.visualization import prepare_visualization

        monkeypatch.setattr(prepare_visualization, "CURATED_DIR", tmp_path)
        filename = "test_dashboard_export.csv"

        # Act
        output_path = export_for_dashboard(sample_ipt_df, filename)

        # Assert
        assert output_path.exists()
        assert output_path.name == filename
        loaded = pd.read_csv(output_path)
        assert len(loaded) == 4
        assert "ipt" in loaded.columns

    def test_load_curated_dataset_reads_existing_file(
        self, sample_ipt_df: pd.DataFrame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """RF-010: Verifica la lectura exitosa de un archivo previamente curado."""
        # Arrange
        from src.visualization import prepare_visualization

        monkeypatch.setattr(prepare_visualization, "CURATED_DIR", tmp_path)
        file_path = tmp_path / "ranking_curated.csv"
        sample_ipt_df.to_csv(file_path, index=False)

        # Act
        loaded = load_curated_dataset("ranking_curated.csv")

        # Assert
        assert len(loaded) == len(sample_ipt_df)
        assert list(loaded.columns) == list(sample_ipt_df.columns)

    def test_load_curated_dataset_raises_file_not_found(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verifica que se lance FileNotFoundError ante un dataset inexistente en data/curated."""
        # Arrange
        from src.visualization import prepare_visualization

        monkeypatch.setattr(prepare_visualization, "CURATED_DIR", tmp_path)

        # Act & Assert
        with pytest.raises(FileNotFoundError, match="No existe el archivo curado"):
            load_curated_dataset("archivo_fantasma.csv")

    def test_multidomain_geodataframe_integrity(self) -> None:
        """RF-007 / RF-010: Verifica que el GeoDataFrame multidominio contenga las 20 localidades canónicas."""
        # Arrange & Act
        from src.visualization.geo_dashboard import build_multidomain_geodataframe

        gdf = build_multidomain_geodataframe()

        # Assert
        assert len(gdf) == 20
        assert gdf.crs is not None and gdf.crs.to_string() == "EPSG:4326"
        assert not gdf.geometry.is_empty.any()
        assert not gdf.geometry.isna().any()
        assert "IPT_MULTIDIMENSIONAL" in gdf.columns
        assert "codigo_localidad" in gdf.columns

    def test_classification_breaks_monotonicity(self) -> None:
        """Verifica que las rupturas de Fisher-Jenks y Cuantiles sean monótonas crecientes."""
        # Arrange
        from src.visualization.geo_dashboard import calculate_classification_breaks

        sample_series = pd.Series([10.5, 23.1, 45.0, 12.0, 89.4, 55.2, 33.1, 67.8, 92.0, 15.4])

        # Act
        breaks_jenks = calculate_classification_breaks(sample_series, method="jenks", k=5)
        breaks_quant = calculate_classification_breaks(sample_series, method="quantiles", k=5)

        # Assert
        assert len(breaks_jenks) >= 2
        assert len(breaks_quant) >= 2
        assert all(x <= y for x, y in zip(breaks_jenks, breaks_jenks[1:]))
        assert all(x <= y for x, y in zip(breaks_quant, breaks_quant[1:]))

    def test_dashboard_html_generation(self, tmp_path: Path) -> None:
        """RF-010: Verifica la compilación y contenido del Dashboard Web GIS autónomo."""
        # Arrange
        from src.visualization.geo_dashboard import generate_interactive_gis_dashboard

        out_html = tmp_path / "test_dashboard.html"

        # Act
        res_path = generate_interactive_gis_dashboard(out_html)

        # Assert
        assert res_path.exists()
        assert res_path.stat().st_size > 10 * 1024  # Mayor a 10 KB
        content = res_path.read_text(encoding="utf-8")
        assert "SIPTA" in content
        assert "00_ipt" in content
        assert "12_participacion_ciudadana" in content
        assert "leaflet" in content.lower()

