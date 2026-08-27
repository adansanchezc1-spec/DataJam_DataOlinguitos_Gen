"""Módulo generador de tablas maestras de indicadores por dominio territorial para SIPTA.

Fase PDCO: DEVELOPMENT
Estándares: Clean Code, PEP 8, DAMA-BOK, ISO/IEC 25010
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
import pandas as pd

# Resolución de rutas canónicas
ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
CURATED_DIR = ROOT / "data" / "curated"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CURATED_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


MAPA_AREA_PARQUES_M2 = {
    1: 2840000.0,   # Usaquén (~4.9 m²/hab)
    2: 3120000.0,   # Chapinero (~23.8 m²/hab)
    3: 3850000.0,   # Santa Fe (~34.5 m²/hab)
    4: 2410000.0,   # San Cristóbal (~5.8 m²/hab)
    5: 1820000.0,   # Usme (~4.5 m²/hab)
    6: 1910000.0,   # Tunjuelito (~9.5 m²/hab)
    7: 1650000.0,   # Bosa (~2.3 m²/hab)
    8: 3250000.0,   # Kennedy (~3.1 m²/hab)
    9: 2150000.0,   # Fontibón (~5.0 m²/hab)
    10: 3620000.0,  # Engativá (~4.3 m²/hab)
    11: 4250000.0,  # Suba (~3.4 m²/hab)
    12: 1850000.0,  # Barrios Unidos (~11.8 m²/hab)
    13: 4520000.0,  # Teusaquillo (~28.5 m²/hab)
    14: 410000.0,   # Los Mártires (~4.2 m²/hab)
    15: 820000.0,   # Antonio Nariño (~7.3 m²/hab)
    16: 1520000.0,  # Puente Aranda (~6.3 m²/hab)
    17: 210000.0,   # La Candelaria (~9.1 m²/hab)
    18: 1620000.0,  # Rafael Uribe Uribe (~4.1 m²/hab)
    19: 2650000.0,  # Ciudad Bolívar (~3.4 m²/hab)
    20: 50000000.0, # Sumapaz (Parque Nacional Natural Sumapaz)
}


def load_unified_territorial_source(
    master_path: str | Path | None = None,
    ipt_model_path: str | Path | None = None,
) -> pd.DataFrame:
    """Carga y combina el tablón maestro y las variables modeladas para las 20 localidades."""
    if master_path is None:
        master_path = PROCESSED_DIR / "master_localidades.csv"
    if ipt_model_path is None:
        ipt_model_path = CURATED_DIR / "ipt_modelo_localidad.csv"

    master_path = Path(master_path)
    if not master_path.exists():
        raise FileNotFoundError(f"No existe el tablón maestro en {master_path}")

    df_master = pd.read_csv(master_path, encoding="utf-8-sig")
    df_master["codigo_localidad"] = df_master["codigo_localidad"].astype(int)

    ipt_path = Path(ipt_model_path)
    if ipt_path.exists():
        df_ipt = pd.read_csv(ipt_path, encoding="utf-8-sig")
        df_ipt["codigo_localidad"] = df_ipt["codigo_localidad"].astype(int)
        # Columnas a enriquecer que no estén o agreguen valor
        ipt_extra_cols = [
            c for c in df_ipt.columns
            if c not in df_master.columns or c in [
                "oferta_regular_cupos", "oferta_modalidades_complementarias",
                "cupos_por_1000_pob_5_17", "sedes_ips_registradas", "sedes_ips_por_10000_hab",
                "conflictos_ambientales_registrados", "conflictos_ambientales_por_km2",
                "vendedores_informales_promedio", "rivi_por_10000_hab_2017_2019",
                "cuadrantes_policiales", "cuadrantes_por_10000_hab_2026",
                "score_educacion", "score_salud", "score_estaciones", "score_paraderos",
                "score_ambiente", "score_infraestructura", "score_vulnerabilidad", "score_seguridad",
                "dim_educacion", "dim_salud", "dim_movilidad", "dim_ambiente",
                "dim_infraestructura", "dim_vulnerabilidad", "dim_seguridad",
                "ipt_base", "ranking_ipt_base", "ranking_consenso", "nivel_prioridad_consenso",
                "confianza_priorizacion",
                "IPT_ESCENARIO_1_BASE", "IPT_ESCENARIO_2_RANGOS", "IPT_ESCENARIO_3_SIN_PARQUES",
                "IPT_ESCENARIO_4_SIN_RIVI", "IPT_ESCENARIO_5_DURAS",
                "RANKING_ESC_1", "RANKING_ESC_2", "RANKING_ESC_3", "RANKING_ESC_4", "RANKING_ESC_5"
            ]
        ]
        ipt_cols_to_merge = ["codigo_localidad"] + [c for c in ipt_extra_cols if c != "codigo_localidad" and c in df_ipt.columns]
        df_unified = pd.merge(df_master, df_ipt[ipt_cols_to_merge], on="codigo_localidad", how="left").copy()
    else:
        df_unified = df_master.copy()

    # Cálculo y normalización de áreas de parques e infraestructura
    df_unified["area_total_parques_m2"] = df_unified["codigo_localidad"].map(MAPA_AREA_PARQUES_M2).fillna(1500000.0)
    df_unified["area_parques_ha"] = (df_unified["area_total_parques_m2"] / 10000.0).round(1)
    df_unified["m2_parque_por_habitante"] = (df_unified["area_total_parques_m2"] / df_unified["poblacion"]).round(2)

    # Cálculo de tasas de hurtos por habitante en seguridad
    if "hurto_a_personas_anual" in df_unified.columns:
        df_unified["tasa_hurto_personas_por_10k_hab"] = ((df_unified["hurto_a_personas_anual"] / df_unified["poblacion"]) * 10000.0).round(2)
        df_unified["tasa_hurto_personas_por_100k_hab"] = ((df_unified["hurto_a_personas_anual"] / df_unified["poblacion"]) * 100000.0).round(1)
    if "hurto_a_comercio_anual" in df_unified.columns:
        df_unified["tasa_hurto_comercio_por_10k_hab"] = ((df_unified["hurto_a_comercio_anual"] / df_unified["poblacion"]) * 10000.0).round(2)

    # Contraste demográfico en salud
    if "sedes_ips_registradas" in df_unified.columns and "sedes_ips_por_10000_hab" not in df_unified.columns:
        df_unified["sedes_ips_por_10000_hab"] = ((df_unified["sedes_ips_registradas"] / df_unified["poblacion"]) * 10000.0).round(2)

    # Cálculo de los 5 escenarios de sensibilidad si están presentes las 7 dimensiones
    dims = ["dim_educacion", "dim_salud", "dim_movilidad", "dim_ambiente", "dim_infraestructura", "dim_vulnerabilidad", "dim_seguridad"]
    if all(d in df_unified.columns for d in dims):
        from src.modeling.calculate_indicators import calculate_ipt_sensitivity_scenarios
        df_unified = calculate_ipt_sensitivity_scenarios(df_unified)

    df_unified["codigo_localidad_str"] = df_unified["codigo_localidad"].astype(str).str.zfill(2)
    return df_unified


def build_demografia_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Demografía."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "area_km2",
        "poblacion", "densidad_poblacional", "poblacion_2025", "poblacion_5_17_2025"
    ]
    existing = [c for c in cols if c in df.columns]
    res = df[existing].copy()
    if "poblacion" in res.columns and "area_km2" in res.columns and "densidad_poblacional" not in res.columns:
        res["densidad_poblacional"] = (res["poblacion"] / res["area_km2"]).round(2)
    return res


def build_salud_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Salud y Capacidad Asistencial con contraste demográfico."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion", "poblacion_2025",
        "sedes_ips_registradas", "sedes_ips_por_10000_hab", "total_camas_hospitalarias",
        "camas_por_10000_habitantes", "camas_uci_adultos", "medicos_generales_por_1000_hab"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_educacion_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Educación y Cobertura."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "oferta_regular_cupos", "oferta_modalidades_complementarias", "cupos_por_1000_pob_5_17",
        "puntaje_promedio_saber_11", "tasa_desercion_escolar_pct",
        "relacion_estudiantes_por_docente", "colegios_jornada_unica_pct",
        "inversion_educacion_ejecutada_millones", "inversion_educacion_per_capita_cop"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_movilidad_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Movilidad y Accesibilidad."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "area_km2", "poblacion",
        "total_estaciones_troncales_tm", "total_paraderos_sitp", "paraderos_por_10k_hab",
        "estaciones_por_km2", "paraderos_por_km2",
        "tiempo_promedio_desplazamiento_laboral_min", "modo_transporte_principal_trabajo"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_ambiente_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Ambiente y Sostenibilidad."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "area_km2",
        "conflictos_ambientales_registrados", "conflictos_ambientales_por_km2",
        "consumo_promedio_m3_suscriptor", "irca_promedio"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_infraestructura_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Infraestructura y Espacio Público."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion", "area_km2",
        "total_parques_idrd", "area_total_parques_m2", "area_parques_ha", "m2_parque_por_habitante",
        "parques_por_10k_hab", "total_luminarias", "luminarias_por_km2", "luminarias_por_10k_hab",
        "fallas_reportadas_mes", "tecnologia_led_pct", "tiempo_medio_reparacion_horas"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_finanzas_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Finanzas e Inversión Pública (FDL y Distrital)."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "presupuesto_aprobado_millones", "presupuesto_ejecutado_millones",
        "porcentaje_ejecucion_fdl", "inversion_fdl_per_capita_millones", "inversion_fdl_per_capita_cop",
        "presupuesto_social_sdis_millones", "inversion_social_sdis_per_capita_cop",
        "inversion_educacion_ejecutada_millones", "inversion_educacion_per_capita_cop",
        "inversion_presupuesto_participativo_millones", "inversion_pp_per_capita_cop",
        "inversion_total_consolidada_per_capita_cop", "proyectos_inversion_activos"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_vulnerabilidad_social_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Vulnerabilidad Social y Gasto SDIS."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "vendedores_informales_promedio", "rivi_por_10000_hab_2017_2019",
        "presupuesto_social_sdis_millones", "inversion_social_sdis_per_capita_cop",
        "beneficiarios_transferencias_monetarias", "tasa_beneficiarios_transferencias_pct",
        "comedores_comunitarios_activos", "comedores_por_10k_hab", "centros_cuidado_primera_infancia"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_seguridad_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Seguridad y Convivencia."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "cuadrantes_policiales", "cuadrantes_por_10000_hab_2026",
        "homicidios_anual", "tasa_homicidios_por_100k_hab_calc",
        "hurto_a_personas_anual", "tasa_hurto_personas_por_10k_hab", "tasa_hurto_personas_por_100k_hab",
        "hurto_a_comercio_anual", "tasa_hurto_comercio_por_10k_hab",
        "tasa_delitos_alto_impacto_por_100k_hab", "tiempo_medio_respuesta_cuadrante_min"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_servicios_publicos_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Servicios Públicos y Calidad del Agua."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "cobertura_acueducto_pct", "cobertura_alcantarillado_pct", "consumo_promedio_m3_suscriptor",
        "horas_interrupcion_promedio_mes", "irca_promedio", "clasificacion_riesgo_irca",
        "total_luminarias", "tecnologia_led_pct", "penetracion_internet_fijo_pct",
        "velocidad_promedio_bajada_mbps", "zonas_wifi_publicas"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_empleo_economia_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Mercado Laboral, Salarios y Conmutación."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "ocupados_trabajan_en_su_localidad_pct", "ocupados_conmutan_a_otras_localidades_pct",
        "conmutacion_hacia_centro_ampliado_pct", "tiempo_promedio_desplazamiento_laboral_min",
        "ingreso_laboral_promedio_ocupados_cop", "tasa_informalidad_laboral_pct",
        "tasa_desempleo_pct", "poblacion_en_edad_trabajar_estimada"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_participacion_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Participación Ciudadana y PQR."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "total_pqr_recibidas", "pqr_por_10k_hab", "pqr_resueltas_a_tiempo_pct",
        "total_votantes_pp", "tasa_votantes_pp_por_10k_hab",
        "propuestas_ciudadanas_radicadas", "propuestas_ciudadanas_por_10k_hab",
        "inversion_presupuesto_participativo_millones", "inversion_pp_per_capita_cop",
        "tema_frecuente_1", "tema_frecuente_2", "tema_frecuente_3"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_all_domain_tables(
    source_df: pd.DataFrame | None = None,
    export_curated: bool = True,
) -> dict[str, pd.DataFrame]:
    """Genera y persiste las 12 tablas maestras por dominio y el consolidado territorial."""
    if source_df is None:
        source_df = load_unified_territorial_source()

    domain_builders = {
        "master_demografia": build_demografia_master,
        "master_salud": build_salud_master,
        "master_educacion": build_educacion_master,
        "master_movilidad": build_movilidad_master,
        "master_ambiente": build_ambiente_master,
        "master_infraestructura": build_infraestructura_master,
        "master_finanzas": build_finanzas_master,
        "master_vulnerabilidad_social": build_vulnerabilidad_social_master,
        "master_seguridad": build_seguridad_master,
        "master_servicios_publicos": build_servicios_publicos_master,
        "master_empleo_economia": build_empleo_economia_master,
        "master_participacion": build_participacion_master,
    }

    tables: dict[str, pd.DataFrame] = {}

    for name, builder_func in domain_builders.items():
        df_domain = builder_func(source_df)
        tables[name] = df_domain

        if export_curated:
            out_file = CURATED_DIR / f"{name}.csv"
            df_domain.to_csv(out_file, index=False, encoding="utf-8-sig")
            logger.info(f"Guardada tabla de dominio: {out_file} ({len(df_domain)} filas, {len(df_domain.columns)} columnas)")

    if export_curated:
        master_out = CURATED_DIR / "master_indicadores_territoriales.csv"
        source_df.to_csv(master_out, index=False, encoding="utf-8-sig")
        logger.info(f"Guardada tabla maestra consolidada de indicadores: {master_out}")

    return tables


if __name__ == "__main__":
    logger.info("Ejecutando generador de tablas maestras por dominio...")
    created_tables = build_all_domain_tables()
    print(f"Generadas exitosamente {len(created_tables)} tablas maestras por dominio en {CURATED_DIR}.")
