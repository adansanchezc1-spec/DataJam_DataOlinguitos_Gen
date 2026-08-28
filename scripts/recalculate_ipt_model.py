"""Script para el cálculo exhaustivo y reproducible del modelo IPT territorial SIPTA.

Fase PDCO: DEVELOPMENT → CONTROL
Estándares: Clean Code, PEP 8, SWEBOK Cap. 2 y 5, DAMA-BOK, ISO/IEC 25010
"""

from __future__ import annotations

import logging
from pathlib import Path
import numpy as np
import pandas as pd

from src.modeling.calculate_indicators import (
    DIMENSION_COLUMNS,
    calculate_bootstrap_confidence_intervals,
    calculate_consensus_priority,
    calculate_geometric_ipt,
    calculate_ipt_sensitivity_scenarios,
    calculate_multidimensional_ipt,
    calculate_spatial_moran,
    calculate_vif_scores,
    normalize_min_max,
)
from src.modeling.domain_indicators import build_all_domain_tables

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
CURATED_DIR = ROOT / "data" / "curated"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_ipt_modeling_pipeline() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Ejecuta el pipeline integral de modelado IPT con las nuevas fuentes oficiales."""
    logger.info("Iniciando pipeline integral de modelado IPT...")

    master_path = PROCESSED_DIR / "master_localidades.csv"
    if not master_path.exists():
        from src.integration.integrate_data import build_master_table
        logger.info("Generando Tablón Maestro Territorial previo al modelado...")
        build_master_table()

    df_master = pd.read_csv(master_path)
    df_master["codigo_localidad"] = df_master["codigo_localidad"].astype(int)

    # 1. Cargar datos de cobertura y oferta base existentes
    ipt_old_path = CURATED_DIR / "ipt_modelo_localidad.csv"
    if ipt_old_path.exists():
        df_old = pd.read_csv(ipt_old_path)
        df_old["codigo_localidad"] = df_old["codigo_localidad"].astype(int)
    else:
        df_old = df_master.copy()

    # Consolidar dataframe base del modelo
    df_model = df_master.copy()
    for col in df_old.columns:
        if col not in df_model.columns:
            df_model[col] = df_old[col]

    # 2. Actualizar denominadores y métricas per cápita con demografía DANE 2025
    df_model["poblacion_2025"] = df_model["poblacion"]
    if "poblacion_5_17_anos" in df_model.columns:
        df_model["poblacion_5_17_2025"] = df_model["poblacion_5_17_anos"]
    elif "poblacion_5_17" in df_model.columns:
        df_model["poblacion_5_17_2025"] = df_model["poblacion_5_17"]

    # 2.1. Educación: Cupos por 1000 niños (5 a 17 años)
    if "oferta_regular_cupos" in df_model.columns and "poblacion_5_17_2025" in df_model.columns:
        df_model["cupos_por_1000_pob_5_17"] = (
            (df_model["oferta_regular_cupos"] / df_model["poblacion_5_17_2025"]) * 1000.0
        ).round(2)

    # 2.2. Salud: Sedes IPS por 10,000 habitantes
    if "sedes_ips_registradas" in df_model.columns:
        df_model["sedes_ips_por_10000_hab"] = (
            (df_model["sedes_ips_registradas"] / df_model["poblacion_2025"]) * 10000.0
        ).round(2)

    # 2.3. Movilidad: Paraderos SITP por 10,000 habitantes
    if "total_paraderos_sitp" in df_model.columns:
        df_model["paraderos_por_10000_hab_proxy"] = (
            (df_model["total_paraderos_sitp"] / df_model["poblacion_2025"]) * 10000.0
        ).round(2)
    elif "paraderos_zonales" in df_model.columns:
        df_model["paraderos_por_10000_hab_proxy"] = (
            (df_model["paraderos_zonales"] / df_model["poblacion_2025"]) * 10000.0
        ).round(2)

    # 2.4. Infraestructura: Parques por 10,000 habitantes
    if "total_parques_idrd" in df_model.columns:
        df_model["parques_por_10000_hab_proxy"] = (
            (df_model["total_parques_idrd"] / df_model["poblacion_2025"]) * 10000.0
        ).round(2)
    elif "parques_registrados" in df_model.columns:
        df_model["parques_por_10000_hab_proxy"] = (
            (df_model["parques_registrados"] / df_model["poblacion_2025"]) * 10000.0
        ).round(2)

    # 2.5. Vulnerabilidad Social: Tasa de Transferencias IMG y PUA SDIS
    if "atenciones_transferencias_img" in df_model.columns:
        df_model["tasa_transferencias_img_por_10k_hab"] = (
            (df_model["atenciones_transferencias_img"] / df_model["poblacion_2025"]) * 10000.0
        ).round(2)
    if "beneficiarios_comedores_comunitarios" in df_model.columns:
        df_model["tasa_comedores_por_10k_hab"] = (
            (df_model["beneficiarios_comedores_comunitarios"] / df_model["poblacion_2025"]) * 10000.0
        ).round(2)

    # 3. Cálculo de Sub-Índices Dimensionales Normalizados [0, 1] (Min-Max)
    df_model["score_educacion"] = normalize_min_max(df_model.get("cupos_por_1000_pob_5_17", df_model.get("oferta_total_por_1000_pob_5_17", 0)))
    df_model["score_salud"] = normalize_min_max(df_model.get("sedes_ips_por_10000_hab", 0))
    df_model["score_estaciones"] = normalize_min_max(df_model.get("estaciones_por_km2", df_model.get("total_estaciones_troncales", 0)))
    df_model["score_paraderos"] = normalize_min_max(df_model.get("paraderos_por_10000_hab_proxy", df_model.get("paraderos_por_10k_hab", 0)))
    df_model["score_ambiente"] = normalize_min_max(df_model.get("conflictos_ambientales_por_km2", df_model.get("conflictos_ambientales", 0)))
    df_model["score_infraestructura"] = normalize_min_max(df_model.get("parques_por_10000_hab_proxy", df_model.get("parques_por_10k_hab", 0)))

    # Score de vulnerabilidad: combinación de transferencias IMG y RIVI
    tasa_img_norm = normalize_min_max(df_model.get("tasa_transferencias_img_por_10k_hab", 0))
    tasa_rivi_norm = normalize_min_max(df_model.get("rivi_por_10000_hab_2017_2019", 0))
    df_model["score_vulnerabilidad"] = (0.7 * tasa_img_norm + 0.3 * tasa_rivi_norm).clip(0, 1)

    df_model["score_seguridad"] = normalize_min_max(df_model.get("cuadrantes_por_10000_hab_2026", df_model.get("cuadrantes_policiales", 0)))

    # 4. Asignación de Polaridades de Necesidad (0 = Menor Carencia, 1 = Mayor Carencia)
    df_model["dim_educacion"] = 1.0 - df_model["score_educacion"]
    df_model["dim_salud"] = 1.0 - df_model["score_salud"]
    df_model["dim_movilidad"] = 1.0 - (0.5 * df_model["score_estaciones"] + 0.5 * df_model["score_paraderos"])
    df_model["dim_infraestructura"] = 1.0 - df_model["score_infraestructura"]
    df_model["dim_seguridad"] = 1.0 - df_model["score_seguridad"]

    df_model["dim_ambiente"] = df_model["score_ambiente"]
    df_model["dim_vulnerabilidad"] = df_model["score_vulnerabilidad"]

    # Normalización de rangos (Escenario 2)
    for dim_col in DIMENSION_COLUMNS:
        df_model[f"{dim_col}_rango"] = (df_model[dim_col].rank(ascending=True, method="average") - 1.0) / 19.0

    # 5. Cálculo de los 5 Escenarios Metodológicos del IPT
    df_model["localidad"] = df_model["nombre_localidad"]
    df_model["codigo_localidad"] = df_model["codigo_localidad"].astype(str).str.zfill(2)

    df_model = calculate_ipt_sensitivity_scenarios(df_model)
    df_model = calculate_multidimensional_ipt(df_model)

    # 6. Cálculo de Priorización de Consenso y Nivel de Confianza
    ranking_cols = [
        "RANKING_ESC_1",
        "RANKING_ESC_2",
        "RANKING_ESC_3",
        "RANKING_ESC_4",
        "RANKING_ESC_5",
    ]
    df_prioritized = calculate_consensus_priority(df_model, ranking_cols=ranking_cols)

    # 7. Cálculo de IPT Geométrico e Intervalos de Confianza Bootstrap (95%)
    ipt_geom = calculate_geometric_ipt(df_prioritized)
    df_prioritized["IPT_GEOMETRICO"] = ipt_geom.values

    ci_df = calculate_bootstrap_confidence_intervals(df_prioritized, n_bootstraps=1000, alpha=0.05)
    df_prioritized["ci_lower_95"] = ci_df["ci_lower_95"].values
    df_prioritized["ci_upper_95"] = ci_df["ci_upper_95"].values
    df_prioritized["ancho_intervalo_ci95"] = ci_df["ancho_intervalo_ci95"].values

    # 8. Identificación de las 2 Dimensiones Prioritarias por Localidad
    dim_dict = {
        "dim_educacion": "Educación",
        "dim_salud": "Salud",
        "dim_movilidad": "Movilidad",
        "dim_ambiente": "Ambiente",
        "dim_infraestructura": "Infraestructura",
        "dim_vulnerabilidad": "Vulnerabilidad",
        "dim_seguridad": "Seguridad",
    }
    dim_cols = list(DIMENSION_COLUMNS)

    for i in df_prioritized.index:
        row_dims = df_prioritized.loc[i, dim_cols].astype(float)
        sorted_dims = row_dims.sort_values(ascending=False)
        top1_dim = sorted_dims.index[0]
        top2_dim = sorted_dims.index[1]
        df_prioritized.loc[i, "dimension_prioritaria_1"] = dim_dict[top1_dim]
        df_prioritized.loc[i, "dimension_prioritaria_2"] = dim_dict[top2_dim]
        df_prioritized.loc[i, "score_dimension_prioritaria_1"] = round(float(sorted_dims.iloc[0]), 4)
        df_prioritized.loc[i, "score_dimension_prioritaria_2"] = round(float(sorted_dims.iloc[1]), 4)

    # 9. Persistencia en data/curated/
    path_modelo = CURATED_DIR / "ipt_modelo_localidad.csv"
    path_priorizacion = CURATED_DIR / "ipt_priorizacion_localidades.csv"
    path_dashboard = CURATED_DIR / "dashboard_ranking.csv"

    df_prioritized.to_csv(path_modelo, index=False, encoding="utf-8-sig")
    df_prioritized.to_csv(path_priorizacion, index=False, encoding="utf-8-sig")

    # Tabla optimizada para Dashboard
    cols_dash = [
        "codigo_localidad", "localidad", "poblacion", "area_km2", "densidad_poblacional",
        "IPT_MULTIDIMENSIONAL", "RANKING_PRIORIDAD", "ranking_consenso", "nivel_prioridad_consenso",
        "confianza_priorizacion", "IPT_GEOMETRICO", "ci_lower_95", "ci_upper_95",
        "dim_educacion", "dim_salud", "dim_movilidad", "dim_ambiente",
        "dim_infraestructura", "dim_vulnerabilidad", "dim_seguridad",
        "dimension_prioritaria_1", "dimension_prioritaria_2",
        "atenciones_totales_sdis", "atenciones_transferencias_img", "beneficiarios_comedores_comunitarios",
    ]
    existing_dash = [c for c in cols_dash if c in df_prioritized.columns]
    df_prioritized[existing_dash].to_csv(path_dashboard, index=False, encoding="utf-8-sig")

    # 10. Regenerar las 12 Tablas de Dominio Curadas
    build_all_domain_tables(export_curated=True)

    logger.info(f"Modelo IPT exportado: {path_modelo}")
    logger.info(f"Priorización IPT exportada: {path_priorizacion}")
    logger.info(f"Dashboard ranking exportado: {path_dashboard}")

    return df_prioritized, df_model


if __name__ == "__main__":
    df_res, _ = run_ipt_modeling_pipeline()
    print("\n=== RESULTADOS DE PRIORIZACIÓN DE CONSENSO TERRITORIAL (20 LOCALIDADES) ===")
    cols_show = [
        "codigo_localidad", "localidad", "poblacion", "IPT_MULTIDIMENSIONAL",
        "IPT_GEOMETRICO", "ranking_consenso", "nivel_prioridad_consenso", "confianza_priorizacion"
    ]
    print(df_res[cols_show].sort_values("ranking_consenso").to_string(index=False))
