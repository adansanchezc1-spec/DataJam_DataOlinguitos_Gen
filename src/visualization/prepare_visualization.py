"""Plantilla básica de preparación de visualizaciones para SIPTA.

Fase PDCO: DEVELOPMENT
Estándares: Clean Code, PEP 8, DAMA-BOK
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

# Resolución correcta a la raíz del repositorio
ROOT = Path(__file__).resolve().parents[2]
CURATED_DIR = ROOT / "data" / "curated"
CURATED_DIR.mkdir(parents=True, exist_ok=True)


def load_curated_dataset(filename: str) -> pd.DataFrame:
    """Carga un dataset curado desde data/curated."""
    path = CURATED_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo curado: {path}")
    return pd.read_csv(path)


def build_ranking(df: pd.DataFrame, score_column: str = "ipt") -> pd.DataFrame:
    """Genera un ranking descendente por puntaje de priorización."""
    if score_column not in df.columns:
        raise KeyError(f"No existe la columna {score_column}")
    return df.sort_values(by=score_column, ascending=False).reset_index(drop=True)


def export_for_dashboard(df: pd.DataFrame, filename: str) -> Path:
    """Exporta el DataFrame formateado para el dashboard a data/curated."""
    path = CURATED_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    print("Módulo de visualización SIPTA inicializado correctamente.")
