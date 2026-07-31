"""Plantilla básica de evaluación para SIPTA."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / 'data' / 'processed'


def quality_report(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        'column': df.columns,
        'dtype': [str(t) for t in df.dtypes],
        'n_null': df.isna().sum().values,
        'pct_null': df.isna().mean().values * 100,
        'n_unique': df.nunique().values,
    })


def detect_outliers(series: pd.Series, z_threshold: float = 3.0) -> pd.Series:
    z_scores = (series - series.mean()) / series.std(ddof=0)
    return z_scores.abs() > z_threshold


def save_quality_report(report: pd.DataFrame, filename: str) -> Path:
    path = PROCESSED_DIR / filename
    report.to_csv(path, index=False)
    return path


if __name__ == '__main__':
    print('Módulo de evaluación SIPTA.')
