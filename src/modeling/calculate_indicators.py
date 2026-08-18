"""Módulo de cálculo de indicadores y modelado para SIPTA.

Fase PDCO: DEVELOPMENT
Estándares: Clean Code, PEP 8, DAMA-BOK
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

# Resolución correcta a la raíz del repositorio
ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
CURATED_DIR = ROOT / "data" / "curated"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CURATED_DIR.mkdir(parents=True, exist_ok=True)


def normalize_min_max(series: pd.Series) -> pd.Series:
    """Normaliza una serie numérica al intervalo [0, 1]."""
    s_clean = pd.to_numeric(series, errors="coerce").fillna(0)
    s_min = s_clean.min()
    s_max = s_clean.max()
    if s_max == s_min:
        return pd.Series(0.5, index=series.index)
    return (s_clean - s_min) / (s_max - s_min)


def camas_por_10000(
    df: pd.DataFrame, camas_col: str = "camas", pop_col: str = "poblacion"
) -> pd.Series:
    """Calcula indicador SAL-002: Camas hospitalarias por 10.000 habitantes."""
    if camas_col not in df.columns or pop_col not in df.columns:
        raise KeyError("Columnas necesarias no encontradas en el DataFrame")
    camas = pd.to_numeric(df[camas_col], errors="coerce").fillna(0)
    pop = pd.to_numeric(df[pop_col], errors="coerce").replace(0, pd.NA)
    return (camas / pop) * 10000.0


def cupos_por_1000(
    df: pd.DataFrame, cupos_col: str = "cupos", pop_obj_col: str = "poblacion_objetivo"
) -> pd.Series:
    """Calcula indicador EDU-001: Cupos escolares por 1.000 personas en edad escolar."""
    if cupos_col not in df.columns or pop_obj_col not in df.columns:
        raise KeyError("Columnas necesarias no encontradas en el DataFrame")
    cupos = pd.to_numeric(df[cupos_col], errors="coerce").fillna(0)
    pop_obj = pd.to_numeric(df[pop_obj_col], errors="coerce").replace(0, pd.NA)
    return (cupos / pop_obj) * 1000.0


def build_ipt(
    df: pd.DataFrame,
    component_cols: dict[str, str],
    weights: dict[str, float] | None = None,
) -> pd.Series:
    """Construye el Índice de Prioridad Territorial (IPT) compuesto normalizado [0, 100]."""
    normalized_dict: dict[str, pd.Series] = {}
    for name, col in component_cols.items():
        if col in df.columns:
            normalized_dict[name] = normalize_min_max(df[col])

    norm_df = pd.DataFrame(normalized_dict)
    if norm_df.empty:
        return pd.Series(0.0, index=df.index)

    if weights:
        w_series = pd.Series(weights)
        w_norm = w_series / w_series.sum()
        ipt = norm_df.dot(w_norm) * 100.0
    else:
        ipt = norm_df.mean(axis=1) * 100.0

    return ipt


def save_indicator_table(df: pd.DataFrame, filename: str) -> Path:
    """Guarda la tabla de indicadores en data/processed."""
    path = PROCESSED_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    print("Módulo de modelado SIPTA inicializado correctamente.")
