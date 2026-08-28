"""Módulo de Integración Territorial y Construcción del Tablón Maestro Multidominio SIPTA.

Fase PDCO: DEVELOPMENT → CONTROL
Estándares: Clean Code, PEP 8, SWEBOK Cap. 2 y 5, DAMA-BOK, ISO/IEC 25010
Requerimientos Funcionales: RF-003, RF-005, RF-007, RF-009
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
REPORTS_DIR = ROOT / "reports" / "eda"
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
    """Carga y procesa la población proyectada oficial por localidad desde DANE / SDP (2025)."""
    demo_2025_path = processed_dir / "DEMOGRAFIA" / "poblacion_localidad_2025.csv"
    demo_path = processed_dir / "DEMOGRAFIA" / "poblacion_localidad_dane_sdp.csv"

    if demo_2025_path.exists():
        df_2025 = pd.read_csv(demo_2025_path)
        df_2025 = df_2025.rename(
            columns={
                "poblacion_total": "poblacion",
                "poblacion_5_17": "poblacion_5_17_anos",
                "poblacion_60_mas": "poblacion_60_mas_anos",
            }
        )
        df_2025["codigo_localidad"] = df_2025["codigo_localidad"].astype(int)
        return df_2025[[
            "codigo_localidad", "poblacion", "poblacion_hombres", "poblacion_mujeres",
            "poblacion_0_5", "poblacion_6_11", "poblacion_12_17", "poblacion_5_17_anos",
            "poblacion_18_59", "poblacion_60_mas_anos"
        ]]

    if demo_path.exists():
        df = pd.read_csv(demo_path)
        df = df[(df["ano"] == 2025) & (df["area"] == "Total")].copy()
        df = df.rename(
            columns={
                "poblacion_total": "poblacion",
                "poblacion_5_17": "poblacion_5_17_anos",
                "poblacion_60_mas": "poblacion_60_mas_anos",
            }
        )
        df["codigo_localidad"] = df["codigo_localidad"].astype(int)
        return df[[
            "codigo_localidad", "poblacion", "poblacion_hombres", "poblacion_mujeres",
            "poblacion_0_5", "poblacion_6_11", "poblacion_12_17", "poblacion_5_17_anos",
            "poblacion_18_59", "poblacion_60_mas_anos"
        ]]

    # Fallback si no existen procesados
    return pd.DataFrame(
        {
            "codigo_localidad": list(range(1, 21)),
            "poblacion": [500000.0] * 20,
        }
    )


def load_movilidad_infraestructura_coverage(reports_dir: Path | None = None) -> pd.DataFrame | None:
    """Carga paraderos SITP, estaciones troncales y parques desde la matriz territorial."""
    rep_dir = reports_dir or REPORTS_DIR
    cov_file = rep_dir / "matriz_cobertura_localidad.csv"
    if cov_file.exists():
        try:
            df = pd.read_csv(cov_file)
            first_col = df.columns[0]
            homo = homologate_localidad(df[first_col])
            df["codigo_localidad"] = homo["codigo_localidad"]

            cols_map = {
                "estaciones_troncales": "total_estaciones_troncales",
                "paraderos_sitp": "total_paraderos_sitp",
                "parques_idrd": "total_parques_idrd",
                "conflictos_ambientales_registrados": "conflictos_ambientales",
            }
            df = df.rename(columns=cols_map)
            df = df.dropna(subset=["codigo_localidad"]).copy()
            df["codigo_localidad"] = df["codigo_localidad"].astype(int)
            keep_cols = ["codigo_localidad"] + [c for c in cols_map.values() if c in df.columns]
            return df[keep_cols]
        except Exception as e:
            logger.warning(f"No se pudo cargar matriz_cobertura_localidad.csv: {e}")
    return None


def load_vulnerabilidad_social_sdis(processed_dir: Path | None = None) -> pd.DataFrame | None:
    """Carga indicadores de vulnerabilidad social y transferencias monetarias PUA SDIS."""
    proc_dir = processed_dir or PROCESSED_DIR
    vuln_path = proc_dir / "VULNERABILIDAD" / "pua_sdis_indicadores_localidad.csv"
    if vuln_path.exists():
        try:
            df = pd.read_csv(vuln_path)
            df["codigo_localidad"] = df["codigo_localidad"].astype(int)
            return df
        except Exception as e:
            logger.warning(f"No se pudo cargar pua_sdis_indicadores_localidad.csv: {e}")
    return None


def build_master_table(
    processed_dir: Path | None = None,
    reports_dir: Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Construye el Tablón Maestro Multidominio Territorial SIPTA unificando los 7 sectores.

    Pasos:
    1. Inicializa con la base canónica oficial de 20 localidades (DIVIPOLA / SDP).
    2. Cruza demografía oficial DANE/SDP 2025.
    3. Cruza infraestructura y movilidad.
    4. Cruza indicadores sectoriales procesados (Salud, Educación, Finanzas, PUA SDIS, etc.).
    5. Realiza Feature Engineering (densidades, tasas por 10k/100k hab, coberturas).
    6. Aplica evaluación de calidad de datos DAMA-BOK.
    7. Persiste `master_localidades.csv` y reportes asociados.
    """
    proc_dir = processed_dir or PROCESSED_DIR
    rep_dir = reports_dir or REPORTS_DIR

    logger.info("Iniciando construcción del Tablón Maestro Territorial SIPTA (Todos los Dominios)...")

    # 1. Base Canónica (20 Localidades)
    master = get_canonical_localities_base()

    # 2. Dominio Demografía (DANE / SDP 2025)
    demo_df = load_demografia_localidades(proc_dir)
    master = merge_by_locality(master, demo_df, locality_col="codigo_localidad")

    # 3. Dominio Movilidad e Infraestructura (Matriz Cobertura)
    mov_infra_df = load_movilidad_infraestructura_coverage(rep_dir)
    if mov_infra_df is not None:
        master = merge_by_locality(master, mov_infra_df, locality_col="codigo_localidad")
        logger.info("Datos de Movilidad e Infraestructura (Parques, Paraderos, Estaciones) integrados.")

    # 4. Integración de Sectores Procesados
    sector_datasets = [
        ("SALUD", "capacidad_camas_asistencial_localidad.csv"),
        ("EDUCACION", "calidad_educativa_saber11_retencion_localidad.csv"),
        ("FINANZAS_INVERSION_PUBLICA", "inversion_fondos_desarrollo_local_fdl.csv"),
        ("FINANZAS_INVERSION_PUBLICA", "metas_inversion_social_sdis_localidad.csv"),
        ("FINANZAS_INVERSION_PUBLICA", "presupuestos_participativos_propuestas_priorizadas.csv"),
        ("VULNERABILIDAD", "pua_sdis_indicadores_localidad.csv"),
        ("SERVICIOS_PUBLICOS", "eaab_cobertura_acueducto_localidad.csv"),
        ("SERVICIOS_PUBLICOS", "eaab_calidad_agua_irca_localidad.csv"),
        ("SERVICIOS_PUBLICOS", "uaesp_alumbrado_publico_localidad.csv"),
        ("SERVICIOS_PUBLICOS", "cobertura_conectividad_tic_localidad.csv"),
        ("PARTICIPACION_CIUDADANA", "pqr_bogota_te_escucha_por_localidad.csv"),
        ("SEGURIDAD", "delitos_alto_impacto_localidad_2024_2026.csv"),
        ("EMPLEO_ECONOMIA", "conmutacion_laboral_residencia_trabajo_localidad.csv"),
        ("EMPLEO_ECONOMIA", "ingreso_promedio_salario_ocupados_localidad.csv"),
    ]

    for sector, filename in sector_datasets:
        file_path = proc_dir / sector / filename
        if not file_path.exists():
            # Fallback a data/raw si no está en processed
            file_path = ROOT / "data" / "raw" / sector / filename
        if file_path.exists():
            try:
                sector_df = pd.read_csv(file_path)
                sector_df = standardize_column_names(sector_df)
                master = merge_by_locality(master, sector_df, locality_col="codigo_localidad")
                logger.info(f"Sector {sector} ({filename}) integrado exitosamente.")
            except Exception as e:
                logger.warning(f"Error al integrar {sector}/{filename}: {e}")

    # 4.1. Integración de Inversión SED Educación (GPKG)
    sed_gpkg_path = ROOT / "data" / "raw" / "FINANZAS_INVERSION_PUBLICA" / "inversion_educacion_por_localidad_12_2025.gpkg"
    if sed_gpkg_path.exists():
        try:
            import geopandas as gpd
            sed_gdf = gpd.read_file(sed_gpkg_path)
            sed_gdf["codigo_localidad"] = pd.to_numeric(sed_gdf["COD_LOCA"], errors="coerce").astype(int)
            sed_cols = sed_gdf[["codigo_localidad", "R_ASIGNADOS", "R_EJECUTADOS", "R_GIRADOS"]].copy()
            sed_cols = sed_cols.rename(
                columns={
                    "R_ASIGNADOS": "inversion_educacion_asignada_cop",
                    "R_EJECUTADOS": "inversion_educacion_ejecutada_cop",
                    "R_GIRADOS": "inversion_educacion_girada_cop",
                }
            )
            master = merge_by_locality(master, sed_cols, locality_col="codigo_localidad")
            logger.info("Inversión SED Educación (GPKG) integrada exitosamente.")
        except Exception as e:
            logger.warning(f"Error al integrar SED GPKG: {e}")

    # 5. Feature Engineering Multidominio (src.features)
    # 5.1. Densidad Poblacional (hab/km2)
    master = add_density(master, population_col="poblacion", area_col="area_km2")

    # 5.2. Ratios per cápita - Salud
    if "total_camas_hospitalarias" in master.columns:
        master = add_ratio(master, "total_camas_hospitalarias", "poblacion", "camas_por_10k_hab_calc")
        master["camas_por_10k_hab_calc"] = master["camas_por_10k_hab_calc"] * 10000

    # 5.3. Ratios per cápita - Movilidad e Infraestructura
    if "total_paraderos_sitp" in master.columns:
        master = add_ratio(master, "total_paraderos_sitp", "poblacion", "paraderos_por_10k_hab")
        master["paraderos_por_10k_hab"] = master["paraderos_por_10k_hab"] * 10000

    if "total_parques_idrd" in master.columns:
        master = add_ratio(master, "total_parques_idrd", "poblacion", "parques_por_10k_hab")
        master["parques_por_10k_hab"] = master["parques_por_10k_hab"] * 10000

    if "total_luminarias" in master.columns and "area_km2" in master.columns:
        master["luminarias_por_km2"] = (master["total_luminarias"] / master["area_km2"]).round(2)
        master["luminarias_por_10k_hab"] = ((master["total_luminarias"] / master["poblacion"]) * 10000).round(2)

    # 5.4. Vulnerabilidad Social y Asistencia SDIS
    if "beneficiarios_transferencias_monetarias_img" in master.columns:
        master["beneficiarios_transferencias_monetarias"] = master["beneficiarios_transferencias_monetarias_img"]
        master["tasa_beneficiarios_transferencias_pct"] = ((master["beneficiarios_transferencias_monetarias_img"] / master["poblacion"]) * 100).round(2)
        master["tasa_transferencias_img_por_10k_hab"] = ((master["atenciones_transferencias_img"] / master["poblacion"]) * 10000).round(2)
    elif "beneficiarios_transferencias_monetarias" in master.columns:
        master["tasa_beneficiarios_transferencias_pct"] = ((master["beneficiarios_transferencias_monetarias"] / master["poblacion"]) * 100).round(2)

    if "beneficiarios_comedores_comunitarios" in master.columns:
        master["comedores_por_10k_hab"] = ((master["beneficiarios_comedores_comunitarios"] / master["poblacion"]) * 10000).round(2)
    elif "comedores_comunitarios_activos" in master.columns:
        master["comedores_por_10k_hab"] = ((master["comedores_comunitarios_activos"] / master["poblacion"]) * 10000).round(3)

    if "atenciones_totales_sdis" in master.columns:
        master["tasa_atenciones_sdis_por_10k_hab"] = ((master["atenciones_totales_sdis"] / master["poblacion"]) * 10000).round(2)

    if "atenciones_comisarias_familia" in master.columns:
        master["tasa_comisarias_por_10k_hab"] = ((master["atenciones_comisarias_familia"] / master["poblacion"]) * 10000).round(2)

    # 5.5. Participación Ciudadana y Presupuestos Participativos
    if "total_votantes_pp" in master.columns:
        master["tasa_votantes_pp_por_10k_hab"] = ((master["total_votantes_pp"] / master["poblacion"]) * 10000).round(2)
    if "propuestas_ciudadanas_radicadas" in master.columns:
        master["propuestas_ciudadanas_por_10k_hab"] = ((master["propuestas_ciudadanas_radicadas"] / master["poblacion"]) * 10000).round(2)
    if "inversion_presupuesto_participativo_millones" in master.columns:
        master["inversion_pp_per_capita_cop"] = ((master["inversion_presupuesto_participativo_millones"] * 1e6) / master["poblacion"]).round(0)

    # 5.6. Inversión Pública Consolidada y Ratios per Cápita
    if "presupuesto_ejecutado_millones" in master.columns:
        master = add_ratio(master, "presupuesto_ejecutado_millones", "poblacion", "inversion_fdl_per_capita_millones")
        master["inversion_fdl_per_capita_cop"] = ((master["presupuesto_ejecutado_millones"] * 1e6) / master["poblacion"]).round(0)

    if "presupuesto_social_sdis_millones" in master.columns:
        master["inversion_social_sdis_per_capita_cop"] = ((master["presupuesto_social_sdis_millones"] * 1e6) / master["poblacion"]).round(0)

    if "inversion_educacion_ejecutada_cop" in master.columns:
        master["inversion_educacion_per_capita_cop"] = (master["inversion_educacion_ejecutada_cop"] / master["poblacion"]).round(0)
        master["inversion_educacion_ejecutada_millones"] = (master["inversion_educacion_ejecutada_cop"] / 1e6).round(2)

    # Inversión Total Distrital Consolidada per Cápita (COP)
    inv_fdl = master.get("inversion_fdl_per_capita_cop", 0)
    inv_sdis = master.get("inversion_social_sdis_per_capita_cop", 0)
    inv_pp = master.get("inversion_pp_per_capita_cop", 0)
    inv_sed = master.get("inversion_educacion_per_capita_cop", 0)
    master["inversion_total_consolidada_per_capita_cop"] = (inv_fdl + inv_sdis + inv_pp + inv_sed).round(0)

    # 5.7. Ratios per cápita - Seguridad
    if "homicidios_anual" in master.columns:
        master = add_ratio(master, "homicidios_anual", "poblacion", "tasa_homicidios_por_100k_hab_calc")
        master["tasa_homicidios_por_100k_hab_calc"] = master["tasa_homicidios_por_100k_hab_calc"] * 100000

    # 5.8. Ratios per cápita - Participación PQR
    if "total_pqr_recibidas" in master.columns:
        master = add_ratio(master, "total_pqr_recibidas", "poblacion", "pqr_por_10k_hab")
        master["pqr_por_10k_hab"] = master["pqr_por_10k_hab"] * 10000

    # Imputación residual para columnas numéricas con mediana
    num_cols = master.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if master[col].isna().any():
            master[col] = master[col].fillna(master[col].median())

    # 6. Evaluación de Calidad (src.evaluation)
    report_df = quality_report(master)

    # 7. Persistencia
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
    print("=== TABLÓN MAESTRO SIPTA GENERADO (TODOS LOS DOMINIOS) ===")
    print(f"Dimensiones: {master_df.shape}")
    print("\nPrimeras 5 localidades:")
    print(master_df[["codigo_localidad", "nombre_localidad", "poblacion", "densidad_poblacional"]].head())
