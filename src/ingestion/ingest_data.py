"""Plantilla básica de ingesta para SIPTA."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_csv(filename: str) -> pd.DataFrame:
    path = RAW_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f'No existe el archivo raw: {path}')
    return pd.read_csv(path, low_memory=False)


def save_raw_copy(df: pd.DataFrame, output_name: str) -> Path:
    destination = RAW_DIR / output_name
    df.to_csv(destination, index=False)
    return destination


def save_processed_csv(df: pd.DataFrame, output_name: str) -> Path:
    destination = PROCESSED_DIR / output_name
    df.to_csv(destination, index=False)
    return destination


if __name__ == '__main__':
    print('Módulo de ingesta SIPTA. Usa funciones desde otros scripts.')
