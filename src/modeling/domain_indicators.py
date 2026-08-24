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
                "confianza_priorizacion"
            ]
        ]
        ipt_cols_to_merge = ["codigo_localidad"] + [c for c in ipt_extra_cols if c != "codigo_localidad" and c in df_ipt.columns]
        df_unified = pd.merge(df_master, df_ipt[ipt_cols_to_merge], on="codigo_localidad", how="left").copy()
    else:
        df_unified = df_master.copy()

    df_unified["codigo_localidad_str"] = df_unified["codigo_localidad"].astype(str).str.zfill(2)
    return df_unified


def build_demografia_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Demografía."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "area_km2",
        "poblacion", "densidad_poblacional"
    ]
    existing = [c for c in cols if c in df.columns]
    res = df[existing].copy()
    if "poblacion" in res.columns and "area_km2" in res.columns and "densidad_poblacional" not in res.columns:
        res["densidad_poblacional"] = (res["poblacion"] / res["area_km2"]).round(2)
    return res


def build_salud_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Salud y Capacidad Asistencial."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
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
        "relacion_estudiantes_por_docente", "colegios_jornada_unica_pct"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_movilidad_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Movilidad y Accesibilidad."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "area_km2", "poblacion",
        "total_estaciones_troncales_tm", "total_paraderos_sitp", "paraderos_por_10k_hab",
        "tiempo_promedio_desplazamiento_laboral_min", "modo_transporte_principal_trabajo"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_ambiente_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Ambiente y Sostenibilidad."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "area_km2",
        "conflictos_ambientales_registrados", "conflictos_ambientales_por_km2"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_infraestructura_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Infraestructura y Espacio Público."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "total_parques_idrd", "parques_por_10k_hab"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_finanzas_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Finanzas e Inversión Pública (FDL)."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "presupuesto_aprobado_millones", "presupuesto_ejecutado_millones",
        "porcentaje_ejecucion_fdl", "inversion_fdl_per_capita_millones",
        "proyectos_inversion_activos"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_vulnerabilidad_social_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Vulnerabilidad Social y Gasto SDIS."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "vendedores_informales_promedio", "rivi_por_10000_hab_2017_2019",
        "presupuesto_social_sdis_millones", "beneficiarios_transferencias_monetarias",
        "comedores_comunitarios_activos", "centros_cuidado_primera_infancia"
    ]
    existing = [c for c in cols if c in df.columns]
    return df[existing].copy()


def build_seguridad_master(df: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla maestra del dominio Seguridad y Convivencia."""
    cols = [
        "codigo_localidad", "nombre_localidad", "codigo_divipola", "poblacion",
        "cuadrantes_policiales", "cuadrantes_por_10000_hab_2026",
        "homicidios_anual", "tasa_homicidios_por_100k_hab_calc",
        "hurto_a_personas_anual", "hurto_a_comercio_anual",
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
