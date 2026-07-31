"""Plantilla básica de preparación de visualizaciones para SIPTA."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CURATED_DIR = ROOT / 'data' / 'curated'
CURATED_DIR.mkdir(parents=True, exist_ok=True)


def load_curated_dataset(filename: str) -> pd.DataFrame:
    path = CURATED_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f'No existe el archivo curado: {path}')
    return pd.read_csv(path)


def build_ranking(df: pd.DataFrame, score_column: str = 'ipt') -> pd.DataFrame:
    if score_column not in df.columns:
        raise KeyError(f'No existe la columna {score_column}')
    return df.sort_values(by=score_column, ascending=False).reset_index(drop=True)


def export_for_dashboard(df: pd.DataFrame, filename: str) -> Path:
    path = CURATED_DIR / filename
    df.to_csv(path, index=False)
    return path


if __name__ == '__main__':
    print('Módulo de visualización SIPTA.')
