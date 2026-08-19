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


def build_consolidated_locality_metrics() -> pd.DataFrame:
    """Consolida la matriz multidimensional de indicadores para las 20 localidades de Bogotá."""
    # 1. Base territorial
    localidades = [
        (1, "Usaquén", 1100101), (2, "Chapinero", 1100102), (3, "Santa Fe", 1100103),
        (4, "San Cristóbal", 1100104), (5, "Usme", 1100105), (6, "Tunjuelito", 1100106),
        (7, "Bosa", 1100107), (8, "Kennedy", 1100108), (9, "Fontibón", 1100109),
        (10, "Engativá", 1100110), (11, "Suba", 1100111), (12, "Barrios Unidos", 1100112),
        (13, "Teusaquillo", 1100113), (14, "Los Mártires", 1100114), (15, "Antonio Nariño", 1100115),
        (16, "Puente Aranda", 1100116), (17, "La Candelaria", 1100117), (18, "Rafael Uribe Uribe", 1100118),
        (19, "Ciudad Bolívar", 1100119), (20, "Sumapaz", 1100120)
    ]
    df = pd.DataFrame(localidades, columns=["codigo_localidad", "nombre_localidad", "codigo_divipola"])

    # 2. Cruce con Servicios Públicos
    serv_path = ROOT / "data" / "raw" / "SERVICIOS_PUBLICOS" / "eaab_cobertura_acueducto_localidad.csv"
    if serv_path.exists():
        df_serv = pd.read_csv(serv_path)
        df = df.merge(df_serv[["codigo_localidad", "cobertura_acueducto_pct", "cobertura_alcantarillado_pct", "horas_interrupcion_promedio_mes"]], on="codigo_localidad", how="left")

    # 3. Cruce con Inversión FDL
    fdl_path = ROOT / "data" / "raw" / "FINANZAS_INVERSION_PUBLICA" / "inversion_fondos_desarrollo_local_fdl.csv"
    if fdl_path.exists():
        df_fdl = pd.read_csv(fdl_path)
        df = df.merge(df_fdl[["codigo_localidad", "presupuesto_ejecutado_millones", "porcentaje_ejecucion_fdl"]], on="codigo_localidad", how="left")

    # 4. Cruce con Empleo y Conmutación
    emp_path = ROOT / "data" / "raw" / "EMPLEO_ECONOMIA" / "conmutacion_laboral_residencia_trabajo_localidad.csv"
    if emp_path.exists():
        df_emp = pd.read_csv(emp_path)
        df = df.merge(df_emp[["codigo_localidad", "ocupados_trabajan_en_su_localidad_pct", "tiempo_promedio_desplazamiento_laboral_min"]], on="codigo_localidad", how="left")

    sal_path = ROOT / "data" / "raw" / "EMPLEO_ECONOMIA" / "ingreso_promedio_salario_ocupados_localidad.csv"
    if sal_path.exists():
        df_sal = pd.read_csv(sal_path)
        df = df.merge(df_sal[["codigo_localidad", "ingreso_laboral_promedio_ocupados_cop", "tasa_informalidad_laboral_pct", "tasa_desempleo_pct"]], on="codigo_localidad", how="left")

    # 5. Cruce con Seguridad (Delitos)
    seg_path = ROOT / "data" / "raw" / "SEGURIDAD" / "delitos_alto_impacto_localidad_2024_2026.csv"
    if seg_path.exists():
        df_seg = pd.read_csv(seg_path)
        df = df.merge(df_seg[["codigo_localidad", "tasa_delitos_alto_impacto_por_100k_hab", "homicidios_anual"]], on="codigo_localidad", how="left")

    # 6. Cruce con PQR
    pqr_path = ROOT / "data" / "raw" / "PARTICIPACION_CIUDADANA" / "pqr_bogota_te_escucha_por_localidad.csv"
    if pqr_path.exists():
        df_pqr = pd.read_csv(pqr_path)
        df = df.merge(df_pqr[["codigo_localidad", "total_pqr_recibidas", "pqr_resueltas_a_tiempo_pct"]], on="codigo_localidad", how="left")

    # 7. Cruce con Salud y Educación
    salud_path = ROOT / "data" / "raw" / "SALUD" / "capacidad_camas_asistencial_localidad.csv"
    if salud_path.exists():
        df_salud = pd.read_csv(salud_path)
        df = df.merge(df_salud[["codigo_localidad", "camas_por_10000_habitantes"]], on="codigo_localidad", how="left")

    edu_path = ROOT / "data" / "raw" / "EDUCACION" / "calidad_educativa_saber11_retencion_localidad.csv"
    if edu_path.exists():
        df_edu = pd.read_csv(edu_path)
        df = df.merge(df_edu[["codigo_localidad", "puntaje_promedio_saber_11", "tasa_desercion_escolar_pct"]], on="codigo_localidad", how="left")

    return df


def calculate_multidimensional_ipt(df_metrics: pd.DataFrame) -> pd.DataFrame:
    """Calcula el Índice de Prioridad Territorial (IPT) Multidimensional en escala 0 a 100."""
    df = df_metrics.copy()

    # Dimensiones de Carencia y Vulnerabilidad (Mayor valor = Mayor prioridad de intervención)
    carencias = {
        "carencia_servicios": (100.0 - df["cobertura_acueducto_pct"].fillna(99.0)) + df["horas_interrupcion_promedio_mes"].fillna(0) * 5,
        "vulnerabilidad_laboral": df["tasa_informalidad_laboral_pct"].fillna(40.0) + df["tasa_desempleo_pct"].fillna(10.0),
        "inseguridad": df["tasa_delitos_alto_impacto_por_100k_hab"].fillna(50.0),
        "tiempo_conmutacion": df["tiempo_promedio_desplazamiento_laboral_min"].fillna(45.0),
        "rezago_educativo": (320.0 - df["puntaje_promedio_saber_11"].fillna(260.0)) + df["tasa_desercion_escolar_pct"].fillna(3.0) * 10,
        "deficit_salud": 70.0 - df["camas_por_10000_habitantes"].fillna(15.0).clip(upper=70.0),
        "alertas_ciudadanas_pqr": df["total_pqr_recibidas"].fillna(5000) / 200.0,
    }

    # Normalizar cada dimensión al rango [0, 1]
    norm_dims = pd.DataFrame({k: normalize_min_max(v) for k, v in carencias.items()})

    # Ponderaciones estratégicas
    weights = {
        "carencia_servicios": 0.20,
        "vulnerabilidad_laboral": 0.20,
        "inseguridad": 0.15,
        "tiempo_conmutacion": 0.15,
        "rezago_educativo": 0.10,
        "deficit_salud": 0.10,
        "alertas_ciudadanas_pqr": 0.10,
    }
    w_series = pd.Series(weights)
    w_norm = w_series / w_series.sum()

    df["IPT_MULTIDIMENSIONAL"] = (norm_dims.dot(w_norm) * 100.0).round(2)
    df["RANKING_PRIORIDAD"] = df["IPT_MULTIDIMENSIONAL"].rank(ascending=False, method="min").astype(int)
    
    # Categorización del nivel de prioridad
    df["NIVEL_PRIORIDAD"] = pd.cut(
        df["IPT_MULTIDIMENSIONAL"],
        bins=[-0.1, 30.0, 50.0, 70.0, 100.0],
        labels=["Baja Prioridad", "Prioridad Moderada", "Alta Prioridad", "Prioridad Crítica"]
    )
    return df


def save_indicator_table(df: pd.DataFrame, filename: str) -> Path:
    """Guarda la tabla de indicadores en data/processed."""
    path = PROCESSED_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    print("Consolidando métricas e indicadores multidimensionales SIPTA...")
    metrics_df = build_consolidated_locality_metrics()
    ipt_df = calculate_multidimensional_ipt(metrics_df)
    out_file = save_indicator_table(ipt_df, "matriz_indicadores_ipt_multidimensional.csv")
    print(f"Matriz consolidada e IPT calculados exitosamente en: {out_file}")
    print(ipt_df[["codigo_localidad", "nombre_localidad", "IPT_MULTIDIMENSIONAL", "RANKING_PRIORIDAD", "NIVEL_PRIORIDAD"]].sort_values("RANKING_PRIORIDAD").head(10))

