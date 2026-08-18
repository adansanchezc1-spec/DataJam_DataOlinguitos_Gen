"""Módulo de validación de calidad y consistencia territorial para SIPTA.

Fase PDCO: DEVELOPMENT
Estándares: Clean Code, PEP 8, ISO/IEC 25010, DAMA-BOK
"""

from __future__ import annotations

import json
import logging
import re
import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Resolución de la raíz del proyecto
ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

# Catálogo canónico de las 20 localidades del Distrito Capital (Bogotá)
LOCALIDADES_BOGOTA_CANONICAS: dict[int, str] = {
    1: "USAQUEN",
    2: "CHAPINERO",
    3: "SANTA FE",
    4: "SAN CRISTOBAL",
    5: "USME",
    6: "TUNJUELITO",
    7: "BOSA",
    8: "KENNEDY",
    9: "FONTIBON",
    10: "ENGATIVA",
    11: "SUBA",
    12: "BARRIOS UNIDOS",
    13: "TEUSAQUILLO",
    14: "LOS MARTIRES",
    15: "ANTONIO NARINO",
    16: "PUENTE ARANDA",
    17: "LA CANDELARIA",
    18: "RAFAEL URIBE URIBE",
    19: "CIUDAD BOLIVAR",
    20: "SUMAPAZ",
}

LOCALIDADES_SET: set[str] = set(LOCALIDADES_BOGOTA_CANONICAS.values())

POSIBLES_COLUMNAS_TERRITORIALES: list[str] = [
    "localidad",
    "cod_localidad",
    "codigo_localidad",
    "nom_localidad",
    "nombre_localidad",
    "loc_nombre",
    "loc_codigo",
    "cod_loc",
    "nom_loc",
    "de_nom_loc",
    "cd_loc",
    "upl",
    "nombre_upl",
]


def _normalizar_texto_simple(texto: str) -> str:
    """Normaliza texto eliminando tildes, mayúsculas y caracteres especiales."""
    if not isinstance(texto, str):
        return ""
    # Quitar acentos
    nfkd = unicodedata.normalize("NFKD", texto)
    sin_tildes = "".join([c for c in nfkd if not unicodedata.combining(c)])
    # Limpiar caracteres especiales y mayúsculas
    limpio = re.sub(r"[^A-Za-z0-9\s]", " ", sin_tildes).strip().upper()
    # Eliminar prefijos comunes tipo "01 - ", "LOC "
    limpio = re.sub(r"^\d+\s*[-_]?\s*", "", limpio).strip()
    return limpio


def inspect_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Genera un perfil detallado del esquema y completitud de un DataFrame.

    Args:
        df: DataFrame a inspeccionar.

    Returns:
        DataFrame con métricas de columnas, tipos, nulos, % nulos y valores únicos.
    """
    total_filas = len(df)
    if total_filas == 0:
        return pd.DataFrame(columns=["column", "dtype", "n_null", "pct_null", "n_unique"])

    return pd.DataFrame(
        {
            "column": list(df.columns),
            "dtype": [str(t) for t in df.dtypes],
            "n_null": [int(df[col].isna().sum()) for col in df.columns],
            "pct_null": [float(df[col].isna().mean() * 100.0) for col in df.columns],
            "n_unique": [int(df[col].nunique(dropna=True)) for col in df.columns],
        }
    )


def detect_territorial_columns(df: pd.DataFrame) -> list[str]:
    """Identifica columnas candidatas a contener identificadores territoriales."""
    cols_encontradas: list[str] = []
    cols_df = [c.lower().strip() for c in df.columns]
    for target in POSIBLES_COLUMNAS_TERRITORIALES:
        for idx, col in enumerate(cols_df):
            if target == col or target in col:
                nombre_real = df.columns[idx]
                if nombre_real not in cols_encontradas:
                    cols_encontradas.append(nombre_real)
    return cols_encontradas


def validate_territorial_column(
    df: pd.DataFrame, column: str = "localidad"
) -> dict[str, Any]:
    """Valida la consistencia de una columna territorial contra las 20 localidades oficiales.

    Args:
        df: DataFrame que contiene los datos.
        column: Nombre de la columna a evaluar.

    Returns:
        Diccionario con estado de existencia, cobertura de localidades y valores no reconocidos.
    """
    if column not in df.columns:
        return {
            "exists": False,
            "column": column,
            "total_localidades_detectadas": 0,
            "cobertura_pct": 0.0,
            "valores_no_reconocidos": [],
        }

    valores_unicos = df[column].dropna().unique()
    reconocidas: set[str] = set()
    no_reconocidos: list[str] = []

    for val in valores_unicos:
        norm = _normalizar_texto_simple(str(val))
        if norm in LOCALIDADES_SET:
            reconocidas.add(norm)
        elif str(val).isdigit() and int(val) in LOCALIDADES_BOGOTA_CANONICAS:
            reconocidas.add(LOCALIDADES_BOGOTA_CANONICAS[int(val)])
        else:
            if val not in ("SIN LOCALIDAD", "BOGOTA", "DISTANCIA", "", "None"):
                no_reconocidos.append(str(val))

    cobertura = (len(reconocidas) / 20.0) * 100.0

    return {
        "exists": True,
        "column": column,
        "localidades_encontradas": sorted(list(reconocidas)),
        "total_localidades_detectadas": len(reconocidas),
        "cobertura_pct": round(cobertura, 2),
        "valores_no_reconocidos": no_reconocidos[:10],
    }


def validate_dataset_quality(df: pd.DataFrame, dataset_name: str = "dataset") -> dict[str, Any]:
    """Evalúa la calidad integral de un dataset: nulos, duplicados y territorio.

    Args:
        df: DataFrame a evaluar.
        dataset_name: Nombre identificador del dataset.

    Returns:
        Diccionario con reporte de calidad.
    """
    total_filas = len(df)
    total_columnas = len(df.columns)
    filas_duplicadas = int(df.duplicated().sum())

    columnas_territoriales = detect_territorial_columns(df)
    validacion_territorial = None
    if columnas_territoriales:
        validacion_territorial = validate_territorial_column(df, columnas_territoriales[0])

    cols_con_alto_nulo = [
        col for col in df.columns if df[col].isna().mean() > 0.50
    ]

    return {
        "dataset": dataset_name,
        "total_rows": total_filas,
        "total_columns": total_columnas,
        "duplicated_rows": filas_duplicadas,
        "pct_duplicated": round((filas_duplicadas / total_filas * 100.0), 2) if total_filas > 0 else 0.0,
        "high_null_columns": cols_con_alto_nulo,
        "territorial_columns_detected": columnas_territoriales,
        "territorial_validation": validacion_territorial,
        "is_valid": total_filas > 0 and len(cols_con_alto_nulo) < total_columnas,
    }


def load_raw_dataset(filename: str) -> pd.DataFrame:
    """Carga un dataset crudo desde data/raw."""
    path = RAW_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo raw: {path}")
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, low_memory=False)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if path.suffix.lower() == ".json":
        return pd.read_json(path)
    raise ValueError(f"Formato no soportado directamente: {path.suffix}")


def export_validation_report(
    reports: list[dict[str, Any]], output_filename: str = "validation_report.json"
) -> Path:
    """Exporta el reporte de validación en JSON a data/processed."""
    out_path = PROCESSED_DIR / output_filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(reports, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    print("Módulo de validación de datos SIPTA inicializado correctamente.")
