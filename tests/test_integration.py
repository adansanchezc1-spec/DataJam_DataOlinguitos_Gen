"""Pruebas unitarias para el módulo de integración territorial (src/integration/integrate_data.py).

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
Estándares: IEEE 829 / ISO 25010 / PEP 8
Requerimiento Funcional: RF-003 (Homologación y unión territorial por 20 localidades canónicas)
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import pytest

from src.integration.integrate_data import (
    merge_by_locality,
    save_master_table,
)


class TestIntegrateData:
    """Suite de pruebas para unión de fuentes territoriales y persistencia de la tabla maestra."""

    @pytest.fixture
    def canonical_base_df(self) -> pd.DataFrame:
        """Fixture base con localidades oficiales y población."""
        return pd.DataFrame(
            {
                "localidad_canonico": ["USAQUEN", "CHAPINERO", "SANTA FE"],
                "poblacion": [500000, 150000, 100000],
            }
        )

    def test_merge_by_locality_with_fallback_column(self) -> None:
        """RF-003: Verifica que merge_by_locality use 'localidad' si no existe 'localidad_canonico'."""
        # Arrange
        df1 = pd.DataFrame({"localidad": ["USAQUEN", "SUBA"], "val1": [10, 20]})
        df2 = pd.DataFrame({"localidad": ["USAQUEN", "SUBA"], "val2": [100, 200]})

        # Act
        merged = merge_by_locality(df1, df2, locality_col="localidad_canonico")

        # Assert
        assert len(merged) == 2
        assert "val1" in merged.columns
        assert "val2" in merged.columns
        assert merged["val2"].iloc[0] == 100

    def test_merge_by_locality_raises_value_error_if_no_common_column(self) -> None:
        """Verifica que se lance ValueError cuando no existe ninguna columna territorial común."""
        # Arrange
        df1 = pd.DataFrame({"col_x": [1, 2]})
        df2 = pd.DataFrame({"col_y": [3, 4]})

        # Act & Assert
        with pytest.raises(ValueError, match="debe existir en ambas tablas"):
            merge_by_locality(df1, df2, locality_col="localidad_canonico")

    def test_save_master_table_writes_to_disk(
        self, canonical_base_df: pd.DataFrame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """RF-009: Verifica la correcta exportación de la tabla territorial integrada a CSV."""
        # Arrange
        from src.integration import integrate_data

        monkeypatch.setattr(integrate_data, "PROCESSED_DIR", tmp_path)
        filename = "master_test_localidades.csv"

        # Act
        saved_path = save_master_table(canonical_base_df, filename=filename)

        # Assert
        assert saved_path.exists()
        assert saved_path.name == filename
        loaded = pd.read_csv(saved_path)
        assert len(loaded) == 3
        assert list(loaded.columns) == list(canonical_base_df.columns)
