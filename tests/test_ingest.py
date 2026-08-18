"""Pruebas unitarias para el módulo de ingesta de datos (src/ingestion/ingest_data.py).

Fase PDCO: CONTROL | Framework: pytest / unittest | Patrón: AAA (Arrange-Act-Assert)
"""

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.ingestion import ingest_data


class TestIngestData(unittest.TestCase):
    """Suite de pruebas unitarias para el pipeline de ingesta."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.raw_dir = self.root / "data" / "raw"
        self.processed_dir = self.root / "data" / "processed"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_csv(self, path: Path, df: pd.DataFrame) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)

    def test_discover_raw_files_returns_supported_files(self) -> None:
        """Verifica que el descubrimiento ignore .txt y detecte .csv y .json."""
        # Arrange
        salud_dir = self.raw_dir / "SALUD"
        salud_dir.mkdir(parents=True, exist_ok=True)

        csv_file = salud_dir / "osb_tiporazoncamas.csv"
        self._write_csv(csv_file, pd.DataFrame({"id": [1], "nombre": ["Ejemplo"]}))

        json_file = self.raw_dir / "sample.json"
        json_file.write_text('{"a": 1}', encoding="utf-8")

        txt_file = self.raw_dir / "ignore.txt"
        txt_file.write_text("ignore me", encoding="utf-8")

        # Act
        result = ingest_data.discover_raw_files(self.raw_dir)
        found = {path.name for path in result}

        # Assert
        self.assertIn("osb_tiporazoncamas.csv", found)
        self.assertIn("sample.json", found)
        self.assertNotIn("ignore.txt", found)

    def test_build_output_path_preserves_relative_structure(self) -> None:
        """Verifica la construcción de la ruta de salida preservando subdirectorios."""
        # Arrange
        source = self.raw_dir / "SALUD" / "osb_tiporazoncamas.csv"
        source.parent.mkdir(parents=True, exist_ok=True)
        expected = self.processed_dir / "SALUD" / "osb_tiporazoncamas.csv"

        # Act
        got = ingest_data.build_output_path(
            source,
            raw_dir=self.raw_dir,
            processed_dir=self.processed_dir,
        )

        # Assert
        self.assertEqual(got, expected)

    def test_ingest_dataset_ingests_csv(self) -> None:
        """Verifica la ingesta correcta de un archivo CSV."""
        # Arrange
        source = self.raw_dir / "SALUD" / "osb_tiporazoncamas.csv"
        df = pd.DataFrame({"id": [1, 2], "nombre": ["a", "b"]})
        self._write_csv(source, df)

        # Act
        result = ingest_data.ingest_dataset(
            source,
            raw_dir=self.raw_dir,
            processed_dir=self.processed_dir,
        )

        output = self.processed_dir / "SALUD" / "osb_tiporazoncamas.csv"

        # Assert
        self.assertEqual(result["status"], "ingested")
        self.assertTrue(output.exists())
        pd.testing.assert_frame_equal(pd.read_csv(output), df)

    def test_ingest_dataset_skips_existing_file_without_overwrite(self) -> None:
        """Verifica que no se sobreescriba si overwrite=False."""
        # Arrange
        source = self.raw_dir / "SALUD" / "osb_tiporazoncamas.csv"
        self._write_csv(source, pd.DataFrame({"id": [1]}))

        # Act
        first = ingest_data.ingest_dataset(
            source,
            raw_dir=self.raw_dir,
            processed_dir=self.processed_dir,
        )
        second = ingest_data.ingest_dataset(
            source,
            raw_dir=self.raw_dir,
            processed_dir=self.processed_dir,
        )

        # Assert
        self.assertEqual(first["status"], "ingested")
        self.assertEqual(second["status"], "skipped")

    def test_ingest_all_datasets_creates_manifest(self) -> None:
        """Verifica la creación del manifiesto JSON de ingesta."""
        # Arrange
        csv_a = self.raw_dir / "A" / "file_a.csv"
        csv_b = self.raw_dir / "B" / "file_b.csv"
        self._write_csv(csv_a, pd.DataFrame({"x": [1]}))
        self._write_csv(csv_b, pd.DataFrame({"y": [2]}))

        manifest = self.processed_dir / "ingestion_manifest.json"

        # Act
        results = ingest_data.ingest_all_datasets(
            raw_dir=self.raw_dir,
            processed_dir=self.processed_dir,
            manifest_path=manifest,
        )

        # Assert
        self.assertEqual(len(results), 2)
        self.assertTrue(manifest.exists())
        self.assertIn("source", results[0])
        self.assertIn("status", results[0])


if __name__ == "__main__":
    unittest.main()
