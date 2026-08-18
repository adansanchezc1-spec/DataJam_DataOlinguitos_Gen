"""Pruebas unitarias para orquestación de exploración e indicadores del EDA (src/eda/explore.py, src/eda/indicators.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import pytest

from src.eda.explore import (
    _resolve_path,
    explorar_dataset,
)
from src.eda.indicators import (
    indicator_status,
    load_catalog,
)


class TestEDAExploreIndicators:
    """Suite de pruebas para exploración automatizada y monitoreo de indicadores."""

    @pytest.fixture
    def setup_eda_dirs(self, tmp_path: Path) -> tuple[Path, Path, Path]:
        """Crea directorios y archivo CSV para probar exploración."""
        raw_dir = tmp_path / "data" / "raw"
        raw_dir.mkdir(parents=True)
        perfiles_dir = tmp_path / "reports" / "perfiles"
        perfiles_dir.mkdir(parents=True)

        sample_csv = raw_dir / "demografia.csv"
        sample_csv.write_text(
            "localidad,poblacion,estrato\nUsaquén,500000,4\nSuba,1200000,3\nBosa,700000,2\n",
            encoding="utf-8",
        )
        return raw_dir, perfiles_dir, sample_csv

    def test_resolve_path_finds_relative_subpaths(
        self, setup_eda_dirs: tuple[Path, Path, Path]
    ) -> None:
        """Verifica que _resolve_path resuelva rutas con prefijos relativos o absolutos."""
        # Arrange
        raw_dir, _, sample_csv = setup_eda_dirs

        # Act & Assert
        assert _resolve_path(sample_csv, raw_dir).exists()
        assert _resolve_path("demografia.csv", raw_dir).exists()
        assert _resolve_path("data/raw/demografia.csv", raw_dir).exists()

    def test_explorar_dataset_executes_end_to_end(
        self, setup_eda_dirs: tuple[Path, Path, Path]
    ) -> None:
        """Verifica la ejecución de explorar_dataset generando perfiles y métricas."""
        # Arrange
        raw_dir, perfiles_dir, sample_csv = setup_eda_dirs
        spec = {
            "id": "demografia_test",
            "titulo": "Demografía Test",
            "path": sample_csv.name,
            "origen": "DANE",
        }

        # Act
        res = explorar_dataset(spec, raw_dir, perfiles_dir, smoke=True)

        # Assert
        assert res["id"] == "demografia_test"
        assert res["filas"] == 3
        assert res["columnas"] == 3
        assert res["error"] == ""
        assert (perfiles_dir / "demografia_test.csv").exists()
        assert (perfiles_dir / "demografia_test__meta.json").exists()

    def test_load_catalog_loads_valid_entries(self) -> None:
        """Verifica la carga del catálogo maestro de fuentes."""
        # Act
        catalog = load_catalog()

        # Assert
        assert isinstance(catalog, pd.DataFrame)
        assert len(catalog) > 0
        assert "id" in catalog.columns
        assert "archivo" in catalog.columns

    def test_indicator_status_evaluates_sector_readiness(self) -> None:
        """Verifica que indicator_status calcule el estado de los indicadores SIPTA."""
        # Act
        df_status = indicator_status()

        # Assert
        assert isinstance(df_status, pd.DataFrame)
        assert len(df_status) > 0
        assert "indicador" in df_status.columns
        assert "dimension" in df_status.columns
        assert "estado" in df_status.columns
