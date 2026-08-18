"""Plantilla básica de integración territorial para SIPTA.

Fase PDCO: DEVELOPMENT
Estándares: Clean Code, PEP 8, DAMA-BOK
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

# Resolución correcta a la raíz del repositorio
ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def merge_by_locality(
    base: pd.DataFrame,
    other: pd.DataFrame,
    locality_col: str = "localidad_canonico",
    how: str = "left",
) -> pd.DataFrame:
    """Combina dos DataFrames utilizando la columna de localidad homologada."""
    if locality_col not in base.columns or locality_col not in other.columns:
        # Fallback a 'localidad' si no está 'localidad_canonico'
        if "localidad" in base.columns and "localidad" in other.columns:
            locality_col = "localidad"
        else:
            raise ValueError(f"La columna {locality_col} debe existir en ambas tablas para la integración")
    return base.merge(other, on=locality_col, how=how)


def save_master_table(df: pd.DataFrame, filename: str = "master_localidades.csv") -> Path:
    """Guarda la tabla territorial maestra en data/processed."""
    path = PROCESSED_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    print("Módulo de integración SIPTA inicializado correctamente.")
