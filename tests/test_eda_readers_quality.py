"""Pruebas unitarias para lectores y evaluación de calidad del EDA (src/eda/readers.py, src/eda/quality.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
"""

from __future__ import annotations

from pathlib import Path
import json
import pandas as pd
import pytest

from src.eda.quality import (
    load_dataset,
    load_dataset_layer,
    problem_flags,
    profile_csv,
    profile_file,
    profile_geojson,
)
from src.eda.readers import (
    read_csv_robust,
    read_geojson,
)


class TestEDAReadersQuality:
    """Suite de pruebas para lectores polimórficos y generación de metadatos de calidad."""

    @pytest.fixture
    def sample_csv(self, tmp_path: Path) -> Path:
        """Fixture que crea un archivo CSV con encoding latin-1 y delimitador punto y coma."""
        csv_file = tmp_path / "test_sample.csv"
        csv_file.write_text(
            "Localidad;Población;Índice\nUsaquén;500000;8.5\nSuba;1200000;9.2\n",
            encoding="latin-1",
        )
        return csv_file

    @pytest.fixture
    def sample_geojson(self, tmp_path: Path) -> Path:
        """Fixture que crea un archivo GeoJSON válido."""
        geo_file = tmp_path / "test_sample.geojson"
        geojson_content = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"nombre": "Punto A", "valor": 100},
                    "geometry": {"type": "Point", "coordinates": [-74.05, 4.65]},
                }
            ],
        }
        geo_file.write_text(json.dumps(geojson_content), encoding="utf-8")
        return geo_file

    def test_read_csv_robust_detects_delimiters_and_encodings(self, sample_csv: Path) -> None:
        """Verifica la detección automática de separador ';' y decodificación correcta."""
        # Act
        df, meta = read_csv_robust(sample_csv)

        # Assert
        assert len(df) == 2
        assert df.shape[1] == 3
        assert "Localidad" in df.columns
        assert meta["n_filas"] == 2
        assert meta["sep"] == ";"

    def test_read_geojson_loads_valid_geodataframe(self, sample_geojson: Path) -> None:
        """Verifica la carga de geometrías GeoJSON."""
        # Act
        gdf, meta = read_geojson(sample_geojson)

        # Assert
        assert len(gdf) == 1
        assert "geometry" in gdf.columns
        assert meta["geometry_type"] == "Point"

    def test_profile_file_returns_consistent_metadata_dict(
        self, tmp_path: Path, sample_csv: Path
    ) -> None:
        """Verifica que profile_file inspeccione atributos básicos de archivo."""
        # Act
        entries = profile_file(sample_csv, raw_dir=tmp_path)

        # Assert
        assert isinstance(entries, list)
        assert len(entries) == 1
        entry = entries[0]
        assert entry["formato"] == "csv"
        assert entry["columnas"] == 3
        assert entry["error_lectura"] == ""

    def test_load_dataset_handles_missing_file_gracefully(self, tmp_path: Path) -> None:
        """Verifica que un archivo inexistente retorne un reporte de error en vez de crashear."""
        # Arrange
        non_existent = tmp_path / "archivo_fantasma.csv"

        # Act
        res = load_dataset(non_existent, tmp_path)

        # Assert
        assert res.get("error") != ""
        assert res.get("df") is not None
        assert res["df"].empty

    def test_problem_flags_identifies_quality_alerts(self) -> None:
        """Verifica que problem_flags traduzca métricas de calidad en alertas legibles."""
        # Arrange
        clean_entry = {"n_unnamed": 0, "n_cols_vacias": 0, "pct_nulos_total": 5.0}
        dirty_entry = {
            "error_lectura": "FileNotFound",
            "n_unnamed": 3,
            "pct_nulos_total": 60.0,
            "duplicados": 10,
        }

        # Act & Assert
        assert problem_flags(clean_entry) == "sin_columna_territorial"
        dirty_flags = problem_flags(dirty_entry)
        assert "error_lectura" in dirty_flags
        assert "columnas_unnamed" in dirty_flags
        assert "nulos_altos" in dirty_flags
