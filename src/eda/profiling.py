"""Perfilado estadístico de variables y datasets para el EDA de SIPTA."""

from __future__ import annotations

import math
import re
import unicodedata

import numpy as np
import pandas as pd

LOCALIDADES_20 = [
    "Usaquén", "Chapinero", "Santa Fe", "San Cristóbal", "Usme", "Tunjuelito", "Bosa", "Kennedy",
    "Fontibón", "Engativá", "Suba", "Barrios Unidos", "Teusaquillo", "Los Mártires",
    "Antonio Nariño", "Puente Aranda", "La Candelaria", "Rafael Uribe Uribe",
    "Ciudad Bolívar", "Sumapaz",
]
LOCALIDAD_ORDER = ["Bogotá", *LOCALIDADES_20]

_TERRITORIAL_TOKENS = (
    "localidad", "codigo localidad", "cod localidad", "cod_loca", "cod_loc", "loca", "loc_orig",
    "loc_dest", "upl", "upz", "barrio",
)


def strip_accents(value):
    text = "" if pd.isna(value) else str(value)
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def normalize_text(value):
    text = strip_accents(value).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


LOCALIDAD_LOOKUP = {normalize_text(x): x for x in LOCALIDADES_20}
LOCALIDAD_LOOKUP.update(
    {
        "bogota": "Bogotá",
        "bogota d.c.": "Bogotá",
        "bogota, d.c.": "Bogotá",
        "0": "Bogotá",
        "antonio narino": "Antonio Nariño",
        "ciudad bolivar": "Ciudad Bolívar",
        "fontibon": "Fontibón",
        "engativa": "Engativá",
        "los martires": "Los Mártires",
        "martires": "Los Mártires",
        "san cristobal": "San Cristóbal",
        "san cristobal sur": "San Cristóbal",
        "usaquen": "Usaquén",
        "candelaria": "La Candelaria",
        "la candelaria": "La Candelaria",
        "santafe": "Santa Fe",
        "santa fe": "Santa Fe",
        "rafael uribe": "Rafael Uribe Uribe",
        "rafael uribe uribe": "Rafael Uribe Uribe",
        "barrios unidos": "Barrios Unidos",
    }
)


def standardize_locality(value):
    """Convierte un valor de localidad a la forma canónica (20 localidades + Bogotá)."""
    if value is None or pd.isna(value):
        return pd.NA
    norm = normalize_text(value)
    if norm in LOCALIDAD_LOOKUP:
        return LOCALIDAD_LOOKUP[norm]
    try:
        numeric = int(float(str(value)))
        if numeric in CODIGO_LOCALIDAD_A_NOMBRE:
            return CODIGO_LOCALIDAD_A_NOMBRE[numeric]
        if numeric == 0:
            return "Bogotá"
    except Exception:
        pass
    return pd.NA


CODIGO_LOCALIDAD_A_NOMBRE = {
    1: "Usaquén", 2: "Chapinero", 3: "Santa Fe", 4: "San Cristóbal", 5: "Usme",
    6: "Tunjuelito", 7: "Bosa", 8: "Kennedy", 9: "Fontibón", 10: "Engativá",
    11: "Suba", 12: "Barrios Unidos", 13: "Teusaquillo", 14: "Los Mártires",
    15: "Antonio Nariño", 16: "Puente Aranda", 17: "La Candelaria",
    18: "Rafael Uribe Uribe", 19: "Ciudad Bolívar", 20: "Sumapaz",
}


def localidad_de_codigo(value):
    """Mapea un código numérico de localidad (1-20) a su nombre canónico."""
    try:
        return CODIGO_LOCALIDAD_A_NOMBRE.get(int(float(str(value))), pd.NA)
    except Exception:
        return pd.NA


def detect_territorial_columns(df: pd.DataFrame) -> list[str]:
    """Devuelve las columnas que referencian territorio (localidad, UPL, UPZ...)."""
    candidates = []
    for col in df.columns:
        norm = normalize_text(col).replace("_", " ")
        compact = normalize_text(col)
        if any(token in norm or token in compact for token in _TERRITORIAL_TOKENS):
            candidates.append(col)
    return candidates


def classify_variable(series: pd.Series, n: int | None = None) -> str:
    """Clasifica una columna: id, temporal, numérica, categórica, texto o espacial."""
    n = len(series) if n is None else n
    name = normalize_text(str(series.name))
    dtype = str(series.dtype)
    nunique = int(series.nunique(dropna=True))
    pct_unique = (nunique / n * 100) if n else 0

    if series.name == "geometry" or "geometry" in dtype.lower() or name in ("lat", "lon", "latitud", "longitud", "x", "y"):
        return "espacial"
    if any(tok in name for tok in ("objectid", "globalid", "id_", "_id", " id", "codigo", "cod_", "cod ", "llave", "dane12")) or name in ("id", "fid"):
        if nunique >= max(20, n * 0.8):
            return "id/llave"
    temporal_parse = False
    if "fecha" in name or name in ("ano", "año", "year", "fecha_cort"):
        if not pd.api.types.is_numeric_dtype(series):
            temporal_parse = pd.to_datetime(series, errors="coerce").notna().mean() > 0.4 if len(series) else False
        else:
            temporal_parse = name in ("ano", "año", "year")
    if temporal_parse:
        return "temporal"
    if any(tok in name for tok in ("grupoedad", "grupo_edad", "curso", "orden")):
        return "categórica ordinal"
    if pd.api.types.is_numeric_dtype(series):
        return "numérica discreta" if nunique <= max(20, math.sqrt(max(n, 1))) else "numérica continua"
    if nunique <= max(30, n * 0.2):
        return "categórica nominal"
    valid = series.dropna().astype(str)
    if len(valid) and valid.str.len().median() > 35:
        return "texto libre"
    return "categórica nominal"


def clasificar_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla por columna: dtype, tipo, nulos, únicos y ejemplos."""
    df = df.copy()
    rows = []
    n = len(df)
    for col in df.columns:
        s = df[col]
        nunique = int(s.nunique(dropna=True))
        sample_values = [x for x in s.dropna().astype(str).unique()[:3]]
        rows.append(
            {
                "columna": col,
                "dtype": str(s.dtype),
                "tipo_variable": classify_variable(s, n),
                "n_nulos": int(s.isna().sum()),
                "pct_nulos": round(float(s.isna().mean() * 100), 2) if n else 0,
                "n_unicos": nunique,
                "ejemplo_1": sample_values[0] if len(sample_values) > 0 else "",
                "ejemplo_2": sample_values[1] if len(sample_values) > 1 else "",
                "ejemplo_3": sample_values[2] if len(sample_values) > 2 else "",
            }
        )
    return pd.DataFrame(rows)


def _as_numeric(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return series.astype("float64")
    return pd.to_numeric(series, errors="coerce")


def column_profile(series: pd.Series) -> dict:
    """Estadísticos completos de una columna (skew, curtosis, desv, cuartiles, outliers...)."""
    s = _as_numeric(series)
    valid = s.dropna()
    if valid.empty:
        return {"columna": str(series.name), "n": int(s.notna().sum()), "n_nulos": int(s.isna().sum()), "sin_valores_numericos": True}
    q1, q3 = valid.quantile([0.25, 0.75])
    iqr = q3 - q1
    mask_out = (valid < q1 - 1.5 * iqr) | (valid > q3 + 1.5 * iqr)
    mean = float(valid.mean())
    std = float(valid.std())
    mode = valid.mode()
    return {
        "columna": str(series.name),
        "n": int(valid.size),
        "n_nulos": int(s.isna().sum()),
        "pct_nulos": round(float(s.isna().mean() * 100), 2),
        "n_unicos": int(valid.nunique()),
        "media": round(mean, 4),
        "mediana": round(float(valid.median()), 4),
        "moda": round(float(mode.iloc[0]), 4) if not mode.empty else np.nan,
        "desv_est": round(std, 4),
        "min": round(float(valid.min()), 4),
        "max": round(float(valid.max()), 4),
        "rango": round(float(valid.max() - valid.min()), 4),
        "Q1": round(float(q1), 4),
        "Q3": round(float(q3), 4),
        "IQR": round(float(iqr), 4),
        "asimetria_skew": round(float(valid.skew()), 4),
        "curtosis": round(float(valid.kurt()), 4),
        "CV_pct": round(float(std / mean * 100), 4) if mean not in (0, np.nan) and std == std else np.nan,
        "n_outliers_iqr": int(mask_out.sum()),
        "pct_outliers": round(float(mask_out.mean() * 100), 2),
        "sin_valores_numericos": False,
    }


def categorical_profile(series: pd.Series, top_n: int = 5) -> dict:
    """Resumen de una columna categórica: frecuencia y top valores."""
    counts = series.astype("string").fillna("(nulo)").value_counts()
    top = counts.head(top_n)
    return {
        "columna": str(series.name),
        "n": int(series.notna().sum()),
        "n_nulos": int(series.isna().sum()),
        "n_categorias": int(counts.size),
        "dominante": str(top.index[0]) if len(top) else "",
        "pct_dominante": round(float(top.iloc[0] / series.size * 100), 2) if len(top) and series.size else np.nan,
        "top_5": " | ".join(f"{k}={v}" for k, v in top.items()),
    }


def variables_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Perfil de todas las columnas: numéricas con estadísticos, categóricas con frecuencias."""
    rows = []
    for col in df.columns:
        s = df[col]
        if pd.api.types.is_numeric_dtype(s) and s.notna().any():
            rows.append(column_profile(s))
        else:
            numeric = _as_numeric(s)
            if numeric.notna().mean() > 0.6 and numeric.notna().nunique() > 1:
                rows.append(column_profile(s))
            else:
                rows.append(categorical_profile(s))
    return pd.DataFrame(rows)


def dataset_profile(df: pd.DataFrame) -> dict:
    """Resumen a nivel dataset: filas, columnas, duplicados, memoria y nulos totales."""
    df = df.copy()
    total_cells = df.shape[0] * df.shape[1]
    null_total = int(df.isna().sum().sum()) if total_cells else 0
    return {
        "filas": int(df.shape[0]),
        "columnas": int(df.shape[1]),
        "duplicados": int(df.duplicated().sum()),
        "pct_nulos_total": round(null_total / total_cells * 100, 2) if total_cells else 0.0,
        "memoria_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 3),
        "columnas_territoriales": detect_territorial_columns(df),
        "num_cols": [c for c in df.columns if classify_variable(df[c], len(df)).startswith("numérica")],
        "cat_cols": [c for c in df.columns if classify_variable(df[c], len(df)).startswith("categórica")],
        "temp_cols": [c for c in df.columns if classify_variable(df[c], len(df)) == "temporal"],
    }
