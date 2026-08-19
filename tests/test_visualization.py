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
