"""Módulo de limpieza, estandarización y homologación territorial para SIPTA.

Fase PDCO: DEVELOPMENT
Estándares: Clean Code, PEP 8, DAMA-BOK
"""

from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd

<<<<<<< Updated upstream
<<<<<<< Updated upstream
ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'
=======
=======
>>>>>>> Stashed changes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Resolución de la raíz del proyecto
ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Tabla oficial de homologación de las 20 localidades del Distrito Capital
MAPA_HOMOLOGACION_LOCALIDADES: dict[str, dict[str, Any]] = {
    "USAQUEN": {"codigo": 1, "nombre_canonico": "USAQUEN", "divipola": "1100101"},
    "CHAPINERO": {"codigo": 2, "nombre_canonico": "CHAPINERO", "divipola": "1100102"},
    "SANTA FE": {"codigo": 3, "nombre_canonico": "SANTA FE", "divipola": "1100103"},
    "SANTAFE": {"codigo": 3, "nombre_canonico": "SANTA FE", "divipola": "1100103"},
    "SAN CRISTOBAL": {"codigo": 4, "nombre_canonico": "SAN CRISTOBAL", "divipola": "1100104"},
    "SAN CRISTOBAL SUR": {"codigo": 4, "nombre_canonico": "SAN CRISTOBAL", "divipola": "1100104"},
    "USME": {"codigo": 5, "nombre_canonico": "USME", "divipola": "1100105"},
    "TUNJUELITO": {"codigo": 6, "nombre_canonico": "TUNJUELITO", "divipola": "1100106"},
    "BOSA": {"codigo": 7, "nombre_canonico": "BOSA", "divipola": "1100107"},
    "KENNEDY": {"codigo": 8, "nombre_canonico": "KENNEDY", "divipola": "1100108"},
    "FONTIBON": {"codigo": 9, "nombre_canonico": "FONTIBON", "divipola": "1100109"},
    "ENGATIVA": {"codigo": 10, "nombre_canonico": "ENGATIVA", "divipola": "1100110"},
    "SUBA": {"codigo": 11, "nombre_canonico": "SUBA", "divipola": "1100111"},
    "BARRIOS UNIDOS": {"codigo": 12, "nombre_canonico": "BARRIOS UNIDOS", "divipola": "1100112"},
    "TEUSAQUILLO": {"codigo": 13, "nombre_canonico": "TEUSAQUILLO", "divipola": "1100113"},
    "LOS MARTIRES": {"codigo": 14, "nombre_canonico": "LOS MARTIRES", "divipola": "1100114"},
    "MARTIRES": {"codigo": 14, "nombre_canonico": "LOS MARTIRES", "divipola": "1100114"},
    "ANTONIO NARINO": {"codigo": 15, "nombre_canonico": "ANTONIO NARINO", "divipola": "1100115"},
    "PUENTE ARANDA": {"codigo": 16, "nombre_canonico": "PUENTE ARANDA", "divipola": "1100116"},
    "LA CANDELARIA": {"codigo": 17, "nombre_canonico": "LA CANDELARIA", "divipola": "1100117"},
    "CANDELARIA": {"codigo": 17, "nombre_canonico": "LA CANDELARIA", "divipola": "1100117"},
    "RAFAEL URIBE URIBE": {"codigo": 18, "nombre_canonico": "RAFAEL URIBE URIBE", "divipola": "1100118"},
    "RAFAEL URIBE": {"codigo": 18, "nombre_canonico": "RAFAEL URIBE URIBE", "divipola": "1100118"},
    "CIUDAD BOLIVAR": {"codigo": 19, "nombre_canonico": "CIUDAD BOLIVAR", "divipola": "1100119"},
    "SUMAPAZ": {"codigo": 20, "nombre_canonico": "SUMAPAZ", "divipola": "1100120"},
}


def _limpiar_texto(valor: Any) -> str:
    """Normaliza cadenas eliminando tildes y caracteres no alfanuméricos."""
    if valor is None or pd.isna(valor):
        return ""
    texto = str(valor).strip()
    nfkd = unicodedata.normalize("NFKD", texto)
    sin_tildes = "".join([c for c in nfkd if not unicodedata.combining(c)])
    limpio = re.sub(r"[^A-Za-z0-9\s]", " ", sin_tildes).strip().upper()
    # Eliminar prefijos de numeración como "01 - " o "01_"
    limpio = re.sub(r"^\d+\s*[-_]?\s*", "", limpio).strip()
    return limpio


def _normalize_col_name(col: Any) -> str:
    """Normaliza un nombre de columna a snake_case alfanumérico sin acentos."""
    c_str = str(col).strip()
    nfkd = unicodedata.normalize("NFKD", c_str)
    sin_tildes = "".join([c for c in nfkd if not unicodedata.combining(c)])
    limpio = re.sub(r"[^A-Za-z0-9_]+", "_", sin_tildes).strip("_").lower()
    return limpio or "col"


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza los nombres de columnas a snake_case sin acentos ni caracteres especiales.

    Args:
        df: DataFrame original.

    Returns:
        DataFrame con nombres de columnas estandarizados.
    """
    df = df.copy()
    df.columns = [_normalize_col_name(col) for col in df.columns]
    return df


def homologate_localidad(series: pd.Series) -> pd.DataFrame:
    """Homologa una serie con nombres o códigos de localidad a la nomenclatura oficial distrital.

    Args:
        series: Serie de pandas con nombres o identificadores de localidades.

    Returns:
        DataFrame con columnas: `localidad_canonico`, `codigo_localidad`, `codigo_divipola`.
    """
    nombres_canonicos: list[str | None] = []
    codigos_loc: list[int | None] = []
    codigos_divipola: list[str | None] = []

    for val in series:
        if pd.isna(val) or val is None or str(val).strip() == "":
            nombres_canonicos.append(None)
            codigos_loc.append(None)
            codigos_divipola.append(None)
            continue

        # Si viene como número entero de localidad (1 a 20)
        s_val = str(val).strip()
        if s_val.isdigit():
            c_num = int(s_val)
            # Buscar por código directo
            match_found = False
            for entry in MAPA_HOMOLOGACION_LOCALIDADES.values():
                if entry["codigo"] == c_num:
                    nombres_canonicos.append(entry["nombre_canonico"])
                    codigos_loc.append(entry["codigo"])
                    codigos_divipola.append(entry["divipola"])
                    match_found = True
                    break
            if match_found:
                continue

        texto_limpio = _limpiar_texto(val)
        if texto_limpio in MAPA_HOMOLOGACION_LOCALIDADES:
            entry = MAPA_HOMOLOGACION_LOCALIDADES[texto_limpio]
            nombres_canonicos.append(entry["nombre_canonico"])
            codigos_loc.append(entry["codigo"])
            codigos_divipola.append(entry["divipola"])
        else:
            nombres_canonicos.append(texto_limpio or None)
            codigos_loc.append(None)
            codigos_divipola.append(None)

    return pd.DataFrame(
        {
            "localidad_canonico": nombres_canonicos,
            "codigo_localidad": codigos_loc,
            "codigo_divipola": codigos_divipola,
        },
        index=series.index,
    )


def cast_numeric_columns(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Limpia y convierte columnas de texto a tipo numérico (float/int), limpiando $, %, comas.

    Args:
        df: DataFrame original.
        columns: Lista de nombres de columnas a castear. Si es None, analiza automáticament columnas tipo object.

    Returns:
        DataFrame con las columnas convertidas.
    """
    df = df.copy()
    target_cols = columns or [c for c in df.columns if df[c].dtype == "object"]

    for col in target_cols:
        if col in df.columns:
            # Si ya es numérico, continuar
            if pd.api.types.is_numeric_dtype(df[col]):
                continue
            # Limpieza de caracteres de moneda, porcentaje y separadores
            cleaned_series = (
                df[col]
                .astype(str)
                .str.replace("$", "", regex=False)
                .str.replace("%", "", regex=False)
                .str.replace(" ", "", regex=False)
                .str.replace(",", "", regex=False)
            )
            df[col] = pd.to_numeric(cleaned_series, errors="coerce")

    return df


def clean_text_columns(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Limpia columnas de texto eliminando espacios sobrantes y valores vacíos.

    Args:
        df: DataFrame original.
        columns: Columnas de texto a procesar.

    Returns:
        DataFrame con strings saneados.
    """
    df = df.copy()
    target_cols = columns or [c for c in df.columns if df[c].dtype == "object"]

    for col in target_cols:
        if col in df.columns and df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
            df.loc[df[col].isin(["nan", "None", "", "N/A", "null"]), col] = None

    return df


def clean_dataset(
    df: pd.DataFrame,
    locality_col: str | None = None,
    numeric_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Ejecuta el pipeline completo de limpieza y estandarización para un dataset.

    Args:
        df: DataFrame a limpiar.
        locality_col: Columna territorial opcional a homologar.
        numeric_cols: Columnas numéricas a convertir.

    Returns:
        DataFrame limpio y homologado.
    """
    df_clean = standardize_column_names(df)
    df_clean = clean_text_columns(df_clean)

    if numeric_cols:
        norm_numeric_cols = [_normalize_col_name(c) for c in numeric_cols]
        df_clean = cast_numeric_columns(df_clean, norm_numeric_cols)

    if locality_col:
        norm_loc_col = _normalize_col_name(locality_col)
        if norm_loc_col in df_clean.columns:
            homo_df = homologate_localidad(df_clean[norm_loc_col])
            df_clean["localidad_canonico"] = homo_df["localidad_canonico"]
            df_clean["codigo_localidad"] = homo_df["codigo_localidad"]
            df_clean["codigo_divipola"] = homo_df["codigo_divipola"]

    return df_clean


def save_processed(df: pd.DataFrame, filename: str) -> Path:
    """Guarda un DataFrame limpio en data/processed."""
    path = PROCESSED_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def reproject_geojson_to_wgs84(source: str | Path, destination: str | Path) -> Path:
    """Create an EPSG:4326 GeoJSON copy without modifying the raw source."""
    import geopandas as gpd

    source_path = Path(source)
    destination_path = Path(destination)

    if source_path.resolve() == destination_path.resolve():
        raise ValueError("La salida procesada no puede sobrescribir el archivo raw.")
    if not source_path.is_file():
        raise FileNotFoundError(source_path)

    geodata = gpd.read_file(source_path)
    if geodata.crs is None:
        raise ValueError(f"El archivo no declara un CRS: {source_path}")

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    geodata.to_crs(epsg=4326).to_file(destination_path, driver="GeoJSON")
    return destination_path


if __name__ == "__main__":
    print("Módulo de limpieza y estandarización SIPTA inicializado.")
