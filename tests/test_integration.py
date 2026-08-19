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
    get_canonical_localities_base,
    merge_by_locality,
    build_master_table,
    save_master_table,
)


class TestIntegrateData:
    """Suite de pruebas para unión de fuentes territoriales y persistencia de la tabla maestra."""

    @pytest.fixture
    def canonical_base_df(self) -> pd.DataFrame:
        """Fixture base con localidades oficiales y población."""
        return pd.DataFrame(
            {
                "codigo_localidad": [1, 2, 3],
                "localidad_canonico": ["USAQUEN", "CHAPINERO", "SANTA FE"],
                "poblacion": [500000, 150000, 100000],
            }
        )

    def test_get_canonical_localities_base_contains_20_localities(self) -> None:
        """RF-003: Verifica que la base canónica contenga exactamente las 20 localidades oficiales."""
        # Act
        base = get_canonical_localities_base()

        # Assert
        assert len(base) == 20
        assert "codigo_localidad" in base.columns
        assert "nombre_localidad" in base.columns
        assert "codigo_divipola" in base.columns
        assert list(base["codigo_localidad"]) == list(range(1, 21))

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
        with pytest.raises(ValueError, match="No se encontró una columna territorial común"):
            merge_by_locality(df1, df2, locality_col="codigo_inexistente")

    def test_build_master_table_integrates_all_sectors_and_features(self) -> None:
        """RF-007: Verifica la integración completa del Tablón Maestro con 20 localidades y features."""
        # Act
        master_df, report_df = build_master_table()

        # Assert
        assert len(master_df) == 20
        assert "codigo_localidad" in master_df.columns
        assert "nombre_localidad" in master_df.columns
        assert "poblacion" in master_df.columns
        assert "densidad_poblacional" in master_df.columns
        assert master_df["poblacion"].isna().sum() == 0
        assert not report_df.empty
        assert "column" in report_df.columns
        assert "pct_null" in report_df.columns

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
