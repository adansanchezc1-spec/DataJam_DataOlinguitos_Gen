"""Plantilla básica de integración territorial para SIPTA."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / 'data' / 'processed'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def merge_by_locality(base: pd.DataFrame, other: pd.DataFrame, locality_col: str = 'localidad', how: str = 'left') -> pd.DataFrame:
    if locality_col not in base.columns or locality_col not in other.columns:
        raise ValueError(f'La columna {locality_col} debe existir en ambas tablas')
    return base.merge(other, on=locality_col, how=how)


def save_master_table(df: pd.DataFrame, filename: str = 'master_localidades.csv') -> Path:
    path = PROCESSED_DIR / filename
    df.to_csv(path, index=False)
    return path


if __name__ == '__main__':
    print('Módulo de integración SIPTA. Ejecutar desde scripts/external o notebooks.')
