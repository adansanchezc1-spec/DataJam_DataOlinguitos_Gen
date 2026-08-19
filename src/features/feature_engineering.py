"""Plantilla básica de feature engineering para SIPTA."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / 'data' / 'processed'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def add_density(df: pd.DataFrame, population_col: str = 'poblacion', area_col: str = 'area_km2') -> pd.DataFrame:
    df = df.copy()
    if population_col in df.columns and area_col in df.columns:
        df['densidad_poblacional'] = df[population_col] / df[area_col]
    return df


def add_ratio(df: pd.DataFrame, numerator: str, denominator: str, output_name: str) -> pd.DataFrame:
    df = df.copy()
    if numerator in df.columns and denominator in df.columns:
        df[output_name] = df[numerator] / df[denominator]
    return df


def save_feature_table(df: pd.DataFrame, filename: str) -> Path:
    path = PROCESSED_DIR / filename
    df.to_csv(path, index=False)
    return path


if __name__ == '__main__':
    print('Módulo de feature engineering SIPTA.')
