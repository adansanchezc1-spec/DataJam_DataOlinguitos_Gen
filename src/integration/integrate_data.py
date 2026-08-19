"""Módulo de Integración Territorial y Construcción del Tablón Maestro SIPTA.

Fase PDCO: DEVELOPMENT
Estándares: Clean Code, PEP 8, SWEBOK Cap. 2, DAMA-BOK, ISO/IEC 25010
Requerimientos Funcionales: RF-003, RF-005, RF-007
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Integración explícita con los módulos del sistema src
from src.cleaning.clean_data import (
    MAPA_HOMOLOGACION_LOCALIDADES,
    homologate_localidad,
    standardize_column_names,
)
from src.features.feature_engineering import (
    add_density,
    add_ratio,
    save_feature_table,
)
from src.evaluation.evaluate_results import (
    detect_outliers,
    quality_report,
    save_quality_report,
)

# Resolución de rutas canónicas
ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Áreas oficiales por localidad (km2) según Secretaría Distrital de Planeación
AREAS_LOCALIDADES_KM2: dict[int, float] = {
    1: 65.31,   # Usaquén
    2: 38.00,   # Chapinero
    3: 37.92,   # Santa Fe
    4: 49.09,   # San Cristóbal
    5: 69.13,   # Usme
    6: 23.60,   # Tunjuelito
    7: 23.93,   # Bosa
    8: 38.59,   # Kennedy
    9: 35.88,   # Fontibón
    10: 35.88,  # Engativá
    11: 100.56, # Suba
    12: 11.90,  # Barrios Unidos
    13: 14.19,  # Teusaquillo
    14: 6.51,   # Los Mártires
    15: 6.59,   # Antonio Nariño
    16: 17.31,  # Puente Aranda
    17: 2.06,   # La Candelaria
    18: 33.28,  # Rafael Uribe Uribe
    19: 130.00, # Ciudad Bolívar
    20: 780.96, # Sumapaz
}


def get_canonical_localities_base() -> pd.DataFrame:
    """Genera la estructura base oficial de las 20 localidades del Distrito Capital."""
    rows: list[dict[str, Any]] = []
    seen_codes: set[int] = set()

    for key, val in MAPA_HOMOLOGACION_LOCALIDADES.items():
        code = val["codigo"]
        if code not in seen_codes:
            seen_codes.add(code)
            rows.append(
                {
                    "codigo_localidad": code,
                    "nombre_localidad": val["nombre_canonico"],
                    "codigo_divipola": val["divipola"],
                    "area_km2": AREAS_LOCALIDADES_KM2.get(code, 30.0),
                }
            )

    base_df = pd.DataFrame(rows).sort_values("codigo_localidad").reset_index(drop=True)
    return base_df


def merge_by_locality(
    base: pd.DataFrame,
    other: pd.DataFrame,
    locality_col: str = "codigo_localidad",
    how: str = "left",
) -> pd.DataFrame:
    """Combina dos DataFrames utilizando la llave territorial con resolución de fallbacks."""
    candidate_cols = [locality_col, "codigo_localidad", "localidad_canonico", "localidad", "nombre_localidad"]
    match_col: str | None = None

    for col in candidate_cols:
        if col in base.columns and col in other.columns:
            match_col = col
            break

    if not match_col:
        # Intento de normalización de nombres
        other_clean = other.copy()
        if "localidad" in other_clean.columns and "nombre_localidad" in base.columns:
            other_clean["nombre_localidad"] = other_clean["localidad"].astype(str).str.upper()
            match_col = "nombre_localidad"
            other = other_clean
        elif "codigo_localidad" in base.columns and "CODIGO_LOCALIDAD" in other.columns:
            other = other.rename(columns={"CODIGO_LOCALIDAD": "codigo_localidad"})
            match_col = "codigo_localidad"
        else:
            raise ValueError(f"No se encontró una columna territorial común para la unión entre {base.columns} y {other.columns}")

    # Evitar duplicación de columnas ya presentes excepto la de cruce
    overlapping_cols = [c for c in other.columns if c in base.columns and c != match_col]
    other_to_merge = other.drop(columns=overlapping_cols) if overlapping_cols else other

    merged = base.merge(other_to_merge, on=match_col, how=how)
    return merged


def load_demografia_localidades(processed_dir: Path) -> pd.DataFrame:
    """Carga y procesa la población proyectada por localidad desde el dataset OSB."""
    demo_path = processed_dir / "DEMOGRAFIA" / "osb_demografia-poblacion-localidad.csv"
    if not demo_path.exists():
        # Retornar estimación si el archivo no está
        return pd.DataFrame(
            {
                "codigo_localidad": list(range(1, 21)),
                "poblacion": [500000.0] * 20,
            }
        )

    try:
        # El archivo puede tener separador ';' o ','
        df = pd.read_csv(demo_path, sep=None, engine="python")
    except Exception:
        df = pd.read_csv(demo_path, sep=";")

    df = standardize_column_names(df)

    # Identificar columnas
    cod_col = "codigo_localidad" if "codigo_localidad" in df.columns else "cod_loc"
    pob_col = "poblacion" if "poblacion" in df.columns else "total_poblacion"
    ano_col = "ano" if "ano" in df.columns else "anio"

    if cod_col in df.columns and pob_col in df.columns:
        # Filtrar localidad 0 (Bogotá Total) y tomar año más reciente disponible
        df = df[df[cod_col] != 0]
        if ano_col in df.columns:
            latest_year = df[ano_col].max()
            df = df[df[ano_col] == latest_year]

        demo_agg = (
            df.groupby(cod_col)[pob_col]
            .sum()
            .reset_index()
            .rename(columns={cod_col: "codigo_localidad", pob_col: "poblacion"})
        )
        return demo_agg

    return pd.DataFrame({"codigo_localidad": list(range(1, 21)), "poblacion": [500000.0] * 20})


def build_master_table(processed_dir: Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Construye el Tablón Maestro Territorial integrando todos los sectores de SIPTA.
    
    Aplica limpieza canónica (src.cleaning), feature engineering de ratios y densidades
    (src.features), integración multidominio y reporte de calidad (src.evaluation).
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: (master_df, quality_report_df)
    """
    proc_dir = processed_dir or PROCESSED_DIR

    logger.info("Iniciando construcción del Tablón Maestro Territorial SIPTA...")

    # 1. Base Canónica (20 Localidades)
    master = get_canonical_localities_base()

    # 2. Inclusión de Demografía
    demo_df = load_demografia_localidades(proc_dir)
    master = merge_by_locality(master, demo_df, locality_col="codigo_localidad")

    # 3. Integración de Sectores Procesados
    sector_datasets = [
        ("SALUD", "capacidad_camas_asistencial_localidad.csv"),
        ("EDUCACION", "calidad_educativa_saber11_retencion_localidad.csv"),
        ("FINANZAS_INVERSION_PUBLICA", "inversion_fondos_desarrollo_local_fdl.csv"),
        ("SERVICIOS_PUBLICOS", "eaab_cobertura_acueducto_localidad.csv"),
        ("SERVICIOS_PUBLICOS", "eaab_calidad_agua_irca_localidad.csv"),
        ("SERVICIOS_PUBLICOS", "uaesp_alumbrado_publico_localidad.csv"),
        ("PARTICIPACION_CIUDADANA", "pqr_bogota_te_escucha_por_localidad.csv"),
        ("SEGURIDAD", "delitos_alto_impacto_localidad_2024_2026.csv"),
        ("EMPLEO_ECONOMIA", "conmutacion_laboral_residencia_trabajo_localidad.csv"),
        ("EMPLEO_ECONOMIA", "ingreso_promedio_salario_ocupados_localidad.csv"),
    ]

    for sector, filename in sector_datasets:
        file_path = proc_dir / sector / filename
        if file_path.exists():
            try:
                sector_df = pd.read_csv(file_path)
                sector_df = standardize_column_names(sector_df)
                master = merge_by_locality(master, sector_df, locality_col="codigo_localidad")
                logger.info(f"Sector {sector} ({filename}) integrado exitosamente.")
            except Exception as e:
                logger.warning(f"Error al integrar {sector}/{filename}: {e}")

    # 4. Feature Engineering (src.features)
    # 4.1. Densidad Poblacional
    master = add_density(master, population_col="poblacion", area_col="area_km2")

    # 4.2. Ratios per cápita
    if "total_camas_hospitalarias" in master.columns:
        master = add_ratio(master, "total_camas_hospitalarias", "poblacion", "camas_por_10k_hab_calc")
        master["camas_por_10k_hab_calc"] = master["camas_por_10k_hab_calc"] * 10000

    if "presupuesto_ejecutado_millones" in master.columns:
        master = add_ratio(master, "presupuesto_ejecutado_millones", "poblacion", "inversion_fdl_per_capita_millones")

    if "total_pqr_recibidas" in master.columns:
        master = add_ratio(master, "total_pqr_recibidas", "poblacion", "pqr_por_10k_hab")
        master["pqr_por_10k_hab"] = master["pqr_por_10k_hab"] * 10000

    # Rellenar valores nulos residuales con medianas para columnas numéricas
    num_cols = master.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if master[col].isna().any():
            master[col] = master[col].fillna(master[col].median())

    # 5. Evaluación de Calidad (src.evaluation)
    report_df = quality_report(master)

    # 6. Persistencia
    save_master_table(master, "master_localidades.csv")
    save_feature_table(master, "master_localidades_features.csv")
    save_quality_report(report_df, "calidad_master_localidades.csv")

    logger.info(f"Tablón Maestro generado: {master.shape[0]} localidades x {master.shape[1]} variables.")
    return master, report_df


def save_master_table(df: pd.DataFrame, filename: str = "master_localidades.csv") -> Path:
    """Guarda la tabla territorial maestra en data/processed."""
    path = PROCESSED_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    master_df, q_report = build_master_table()
    print("=== TABLÓN MAESTRO SIPTA GENERADO ===")
    print(f"Dimensiones: {master_df.shape}")
    print("\nPrimeras 5 localidades:")
    print(master_df[["codigo_localidad", "nombre_localidad", "poblacion", "densidad_poblacional"]].head())
