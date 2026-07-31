"""Plantilla básica de cálculo de indicadores para SIPTA."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / 'data' / 'processed'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def normalize_min_max(series: pd.Series) -> pd.Series:
    if series.max() == series.min():
        return pd.Series(0.5, index=series.index)
    return (series - series.min()) / (series.max() - series.min())


def camas_por_10000(df: pd.DataFrame, camas_col: str = 'camas', pop_col: str = 'poblacion') -> pd.Series:
    if camas_col not in df.columns or pop_col not in df.columns:
        raise KeyError('Columnas necesarias no encontradas')
    return (df[camas_col] / df[pop_col]) * 10000


def cupos_por_1000(df: pd.DataFrame, cupos_col: str = 'cupos', pop_obj_col: str = 'poblacion_objetivo') -> pd.Series:
    if cupos_col not in df.columns or pop_obj_col not in df.columns:
        raise KeyError('Columnas necesarias no encontradas')
    return (df[cupos_col] / df[pop_obj_col]) * 1000


def build_ipt(df: pd.DataFrame, component_cols: dict[str, str]) -> pd.Series:
    normalized = pd.DataFrame({name: normalize_min_max(df[col]) for name, col in component_cols.items()})
    return normalized.mean(axis=1) * 100


def save_indicator_table(df: pd.DataFrame, filename: str) -> Path:
    path = PROCESSED_DIR / filename
    df.to_csv(path, index=False)
    return path


if __name__ == '__main__':
    print('Módulo de modelado SIPTA. Define las columnas reales según los datos.')
