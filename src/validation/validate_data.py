"""Plantilla básica de validación de datos para SIPTA."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / 'data' / 'raw'


def inspect_schema(df: pd.DataFrame) -> pd.DataFrame:
    summary = pd.DataFrame({
        'column': df.columns,
        'dtype': [str(t) for t in df.dtypes],
        'n_null': df.isna().sum().values,
        'pct_null': df.isna().mean().values * 100,
        'n_unique': df.nunique().values,
    })
    return summary


def validate_territorial_column(df: pd.DataFrame, column: str = 'localidad') -> bool:
    return column in df.columns and df[column].notna().any()


def load_raw_dataset(filename: str) -> pd.DataFrame:
    path = RAW_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f'No existe el archivo raw: {path}')
    return pd.read_csv(path, low_memory=False)


if __name__ == '__main__':
    print('Módulo de validación SIPTA. Importa y ejecuta las funciones desde otros scripts.')
