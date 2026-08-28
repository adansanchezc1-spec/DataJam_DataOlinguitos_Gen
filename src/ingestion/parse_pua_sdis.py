"""Módulo de ingestión y procesamiento del dataset administrativo PUA SDIS.

Fase PDCO: DEVELOPMENT
Estándares: PEP 8, Clean Code, DAMA-BOK
Fuente: Secretaría Distrital de Integración Social (SDIS) - PUA Anónimo (1.04M registros)
"""

from __future__ import annotations

from pathlib import Path
import re
import numpy as np
import openpyxl
import pandas as pd

# Resolución dinámica de rutas relativas a la raíz del repositorio
ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_FILE = (
    ROOT_DIR
    / "data"
    / "raw"
    / "VULNERABILIDAD"
    / "pua_riesgo_y_anon_20250911_193636-1.xlsx"
)
PROCESSED_DIR = ROOT_DIR / "data" / "processed" / "VULNERABILIDAD"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


LOCALIDAD_CLEAN_MAP = {
    "USAQUEN": "01",
    "CHAPINERO": "02",
    "SANTA FE": "03",
    "SAN CRISTOBAL": "04",
    "USME": "05",
    "TUNJUELITO": "06",
    "BOSA": "07",
    "KENNEDY": "08",
    "FONTIBON": "09",
    "ENGATIVA": "10",
    "SUBA": "11",
    "BARRIOS UNIDOS": "12",
    "TEUSAQUILLO": "13",
    "LOS MARTIRES": "14",
    "ANTONIO NARIÑO": "15",
    "ANTONIO NARINO": "15",
    "PUENTE ARANDA": "16",
    "CANDELARIA": "17",
    "LA CANDELARIA": "17",
    "RAFAEL URIBE": "18",
    "RAFAEL URIBE URIBE": "18",
    "CIUDAD BOLIVAR": "19",
    "SUMAPAZ": "20",
}

CANONICAL_LOCALIDADES = [
    ("01", "USAQUEN"),
    ("02", "CHAPINERO"),
    ("03", "SANTA FE"),
    ("04", "SAN CRISTOBAL"),
    ("05", "USME"),
    ("06", "TUNJUELITO"),
    ("07", "BOSA"),
    ("08", "KENNEDY"),
    ("09", "FONTIBON"),
    ("10", "ENGATIVA"),
    ("11", "SUBA"),
    ("12", "BARRIOS UNIDOS"),
    ("13", "TEUSAQUILLO"),
    ("14", "LOS MARTIRES"),
    ("15", "ANTONIO NARIÑO"),
    ("16", "PUENTE ARANDA"),
    ("17", "LA CANDELARIA"),
    ("18", "RAFAEL URIBE URIBE"),
    ("19", "CIUDAD BOLIVAR"),
    ("20", "SUMAPAZ"),
]


def load_raw_pua(file_path: Path | str | None = None) -> pd.DataFrame:
    """Carga el dataset PUA SDIS de forma optimizada en streaming con openpyxl."""
    path = Path(file_path) if file_path else RAW_FILE
    if not path.exists():
        raise FileNotFoundError(f"Archivo PUA no encontrado: {path}")

    # Verificar si ya existe versión serializada en parquet para aceleración
    parquet_cache = PROCESSED_DIR / "pua_anon_optimizado.parquet"
    if parquet_cache.exists():
        print(f"Cargando PUA desde caché optimizado: {parquet_cache}")
        return pd.read_parquet(parquet_cache)

    print(f"Leyendo Excel PUA en streaming (puede tomar ~20-30s): {path}")
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["PUA_ANON"]

    rows = []
    headers = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            headers = [str(col).strip() if col is not None else f"col_{idx}" for idx, col in enumerate(row)]
        else:
            rows.append(row)
    wb.close()

    df = pd.DataFrame(rows, columns=headers)
    print(f"Registros PUA cargados exitosamente: {len(df):,}")

    # Estandarizar tipos
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    # Guardar en parquet para futuros accesos instantáneos
    try:
        df.to_parquet(parquet_cache, index=False)
        print(f"Caché Parquet generado: {parquet_cache}")
    except Exception as e:
        print(f"Advertencia al guardar caché parquet: {e}")

    return df


def clean_and_normalize_pua(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza códigos territoriales y variables demográficas del PUA."""
    df_clean = df.copy()

    def normalize_loc_name(name: str) -> str:
        s = str(name).upper().strip()
        s = re.sub(r"[ÁÀÄ]", "A", s)
        s = re.sub(r"[ÉÈË]", "E", s)
        s = re.sub(r"[ÍÌÏ]", "I", s)
        s = re.sub(r"[ÓÒÖ]", "O", s)
        s = re.sub(r"[ÚÙÜ]", "U", s)
        s = re.sub(r"[Ñ]", "N", s)
        return s

    df_clean["loc_norm"] = df_clean["LOCALIDAD_ATENCION"].apply(normalize_loc_name)
    df_clean["codigo_localidad"] = df_clean["loc_norm"].map(LOCALIDAD_CLEAN_MAP)

    # Si no mapea por nombre, intentar por CODLOCALIDAD_ATENCION numérico
    if "CODLOCALIDAD_ATENCION" in df_clean.columns:
        cod_series = (
            pd.to_numeric(df_clean["CODLOCALIDAD_ATENCION"], errors="coerce")
            .fillna(0)
            .astype(int)
        )
        mask_missing = df_clean["codigo_localidad"].isna()
        valid_cods = cod_series.between(1, 20)
        df_clean.loc[mask_missing & valid_cods, "codigo_localidad"] = (
            cod_series[mask_missing & valid_cods].astype(str).str.zfill(2)
        )

    # Normalizar variables booleanas/condición
    df_clean["es_img"] = df_clean["TEMATICA"].str.upper().str.contains("INGRESO MINIMO", na=False)
    df_clean["es_comedor"] = (
        df_clean["TEMATICA"].str.upper().str.contains("ALIMENTARIO", na=False)
        | df_clean["SERVICIO"].str.upper().str.contains("COMEDOR", na=False)
    )
    df_clean["es_comisaria"] = (
        df_clean["TEMATICA"].str.upper().str.contains("COMISARIA", na=False)
        | df_clean["SERVICIO"].str.upper().str.contains("COMISARIA", na=False)
    )
    df_clean["es_vejez"] = df_clean["TEMATICA"].str.upper().str.contains("VEJEZ", na=False)
    df_clean["es_infancia"] = df_clean["TEMATICA"].str.upper().str.contains("INFANCIA", na=False)
    df_clean["es_habitante_calle"] = df_clean["TEMATICA"].str.upper().str.contains("CALLE", na=False)
    df_clean["es_discapacidad"] = df_clean["SITUACION_DISCAPACIDAD_ACTUAL"].str.upper() == "SI"
    df_clean["es_victima"] = df_clean["VICTIMA_ACTUAL"].str.upper() == "SI"
    df_clean["es_migrante"] = df_clean["MIGRANTE_ACTUAL"].str.upper() == "SI"

    return df_clean


def calculate_pua_locality_indicators(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores consolidados de vulnerabilidad y atención social por localidad."""
    # Filtrar registros asignados a las 20 localidades oficiales
    df_locs = df_clean[df_clean["codigo_localidad"].isin([f"{i:02d}" for i in range(1, 21)])].copy()

    records = []
    for cod_loc, nom_loc in CANONICAL_LOCALIDADES:
        sub = df_locs[df_locs["codigo_localidad"] == cod_loc]
        if sub.empty:
            records.append({
                "codigo_localidad": cod_loc,
                "localidad": nom_loc,
                "atenciones_totales_sdis": 0,
                "beneficiarios_unicos_total_sdis": 0,
                "beneficiarios_transferencias_monetarias_img": 0,
                "atenciones_transferencias_img": 0,
                "beneficiarios_comedores_comunitarios": 0,
                "atenciones_comisarias_familia": 0,
                "beneficiarios_vejez_sdis": 0,
                "beneficiarios_infancia_sdis": 0,
                "atenciones_habitante_calle_sdis": 0,
                "beneficiarios_discapacidad_sdis": 0,
                "beneficiarios_victimas_sdis": 0,
                "beneficiarios_migrantes_sdis": 0,
            })
            continue

        atenciones_totales = len(sub)
        beneficiarios_totales = sub["ID_ANON"].nunique()

        # Transferencias Monetarias IMG
        sub_img = sub[sub["es_img"]]
        ben_img = sub_img["ID_ANON"].nunique()
        aten_img = len(sub_img)

        # Comedores Comunitarios
        sub_com = sub[sub["es_comedor"]]
        ben_com = sub_com["ID_ANON"].nunique()

        # Comisarías de Familia
        sub_comis = sub[sub["es_comisaria"]]
        aten_comis = len(sub_comis)

        # Grupos de Atención
        ben_vejez = sub[sub["es_vejez"]]["ID_ANON"].nunique()
        ben_infancia = sub[sub["es_infancia"]]["ID_ANON"].nunique()
        aten_calle = len(sub[sub["es_habitante_calle"]])
        ben_discapacidad = sub[sub["es_discapacidad"]]["ID_ANON"].nunique()
        ben_victimas = sub[sub["es_victima"]]["ID_ANON"].nunique()
        ben_migrantes = sub[sub["es_migrante"]]["ID_ANON"].nunique()

        records.append({
            "codigo_localidad": cod_loc,
            "localidad": nom_loc,
            "atenciones_totales_sdis": atenciones_totales,
            "beneficiarios_unicos_total_sdis": beneficiarios_totales,
            "beneficiarios_transferencias_monetarias_img": ben_img,
            "atenciones_transferencias_img": aten_img,
            "beneficiarios_comedores_comunitarios": ben_com,
            "atenciones_comisarias_familia": aten_comis,
            "beneficiarios_vejez_sdis": ben_vejez,
            "beneficiarios_infancia_sdis": ben_infancia,
            "atenciones_habitante_calle_sdis": aten_calle,
            "beneficiarios_discapacidad_sdis": ben_discapacidad,
            "beneficiarios_victimas_sdis": ben_victimas,
            "beneficiarios_migrantes_sdis": ben_migrantes,
        })

    df_res = pd.DataFrame(records).sort_values("codigo_localidad").reset_index(drop=True)
    return df_res


def calculate_pua_upz_indicators(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores agregados a nivel de UPZ a partir del PUA SDIS."""
    # Filtrar registros con código UPZ válido
    df_upz = df_clean[
        df_clean["CODUPZ_UNDOPE"].notna()
        & (df_clean["CODUPZ_UNDOPE"].astype(str) != "999")
        & (df_clean["CODUPZ_UNDOPE"].astype(str) != "0")
    ].copy()

    df_upz["codigo_upz"] = (
        pd.to_numeric(df_upz["CODUPZ_UNDOPE"], errors="coerce")
        .fillna(0)
        .astype(int)
        .astype(str)
        .str.zfill(3)
    )

    grouped = df_upz.groupby(["codigo_upz", "NOMUPZ_UNDOPE", "codigo_localidad"])

    agg_df = grouped.agg(
        atenciones_totales=("ID_ANON", "count"),
        beneficiarios_totales=("ID_ANON", "nunique"),
        atenciones_img=("es_img", "sum"),
        atenciones_comedores=("es_comedor", "sum"),
        atenciones_comisarias=("es_comisaria", "sum"),
        atenciones_discapacidad=("es_discapacidad", "sum"),
        atenciones_victimas=("es_victima", "sum"),
        atenciones_migrantes=("es_migrante", "sum"),
    ).reset_index()

    agg_df = agg_df.rename(
        columns={
            "NOMUPZ_UNDOPE": "nombre_upz",
        }
    )

    return agg_df.sort_values(["codigo_localidad", "codigo_upz"]).reset_index(drop=True)


def generate_canonical_processed_pua() -> dict[str, Path]:
    """Ejecuta el pipeline completo de PUA y exporta archivos procesados."""
    print("Iniciando procesamiento integral de PUA SDIS (1.04M registros)...")
    df_raw = load_raw_pua()
    df_clean = clean_and_normalize_pua(df_raw)

    # 1. Resumen distrital de temáticas
    resumen_tematicas = (
        df_clean.groupby("TEMATICA")
        .agg(
            atenciones=("ID_ANON", "count"),
            beneficiarios_unicos=("ID_ANON", "nunique"),
        )
        .reset_index()
        .sort_values("atenciones", ascending=False)
    )
    out_tematicas = PROCESSED_DIR / "pua_resumen_tematicas_distrital.csv"
    resumen_tematicas.to_csv(out_tematicas, index=False, encoding="utf-8")
    print(f"Exportado: {out_tematicas}")

    # 2. Indicadores por localidad
    df_loc_ind = calculate_pua_locality_indicators(df_clean)
    out_loc = PROCESSED_DIR / "pua_sdis_indicadores_localidad.csv"
    df_loc_ind.to_csv(out_loc, index=False, encoding="utf-8")
    print(f"Exportado: {out_loc} ({len(df_loc_ind)} localidades)")

    # 3. Indicadores por UPZ
    df_upz_ind = calculate_pua_upz_indicators(df_clean)
    out_upz = PROCESSED_DIR / "pua_sdis_indicadores_upz.csv"
    df_upz_ind.to_csv(out_upz, index=False, encoding="utf-8")
    print(f"Exportado: {out_upz} ({len(df_upz_ind)} UPZs)")

    return {
        "resumen_tematicas": out_tematicas,
        "indicadores_localidad": out_loc,
        "indicadores_upz": out_upz,
    }


def parse_pua_sdis_indicadores() -> pd.DataFrame:
    """Retorna el DataFrame procesado de indicadores PUA SDIS por localidad."""
    out_loc = PROCESSED_DIR / "pua_sdis_indicadores_localidad.csv"
    if not out_loc.exists():
        generate_canonical_processed_pua()
    return pd.read_csv(out_loc)


if __name__ == "__main__":
    generate_canonical_processed_pua()
