"""Módulo de ingestión y procesamiento de proyecciones oficiales DANE / SDP.

Fase PDCO: DEVELOPMENT
Estándares: PEP 8, Clean Code, DAMA-BOK
Fuente: Anexo Proyecciones de Población de Bogotá (DANE / SDP 2018-2035)
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

# Resolución dinámica de rutas relativas a la raíz del repositorio
ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_FILE = (
    ROOT_DIR
    / "data"
    / "raw"
    / "DEMOGRAFIA"
    / "anexo-proyecciones-poblacion-bogota-desagreacion-loc-2018-2035-UPZ-2018-2024.xlsx"
)
PROCESSED_DIR = ROOT_DIR / "data" / "processed" / "DEMOGRAFIA"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


LOCALIDAD_MAP = {
    "01": "USAQUEN",
    "02": "CHAPINERO",
    "03": "SANTA FE",
    "04": "SAN CRISTOBAL",
    "05": "USME",
    "06": "TUNJUELITO",
    "07": "BOSA",
    "08": "KENNEDY",
    "09": "FONTIBON",
    "10": "ENGATIVA",
    "11": "SUBA",
    "12": "BARRIOS UNIDOS",
    "13": "TEUSAQUILLO",
    "14": "LOS MARTIRES",
    "15": "ANTONIO NARIÑO",
    "16": "PUENTE ARANDA",
    "17": "LA CANDELARIA",
    "18": "RAFAEL URIBE URIBE",
    "19": "CIUDAD BOLIVAR",
    "20": "SUMAPAZ",
}


def parse_demografia_localidades(
    file_path: Path | str | None = None,
) -> pd.DataFrame:
    """Procesa la hoja 'Localidades' de proyecciones DANE/SDP (2018-2035).

    Extrae la población total, por sexo y grupos de edad específicos
    (0-5, 6-11, 12-17, 5-17, 18-59, 60+).
    """
    path = Path(file_path) if file_path else RAW_FILE
    if not path.exists():
        raise FileNotFoundError(f"Archivo de demografía no encontrado: {path}")

    # La fila de encabezados en el Excel es la fila 11 (0-indexed)
    df_raw = pd.read_excel(path, sheet_name="Localidades", header=11)
    df_raw = df_raw.dropna(subset=["COD_LOC", "AÑO"]).copy()

    df_raw = df_raw.rename(
        columns={
            "COD_LOC": "codigo_localidad",
            "NOM_LOC": "nombre_localidad",
            "AREA": "area",
            "AÑO": "ano",
            "TOTAL": "poblacion_total",
            "TOTAL HOMBRES": "poblacion_hombres",
            "TOTAL MUJERES": "poblacion_mujeres",
        }
    )

    df_raw["codigo_localidad"] = (
        df_raw["codigo_localidad"].astype(str).str.split(".").str[0].str.zfill(2)
    )
    df_raw["ano"] = pd.to_numeric(df_raw["ano"], errors="coerce").astype(int)

    # Columnas de edad por sexo
    h_cols = [c for c in df_raw.columns if str(c).startswith("Hombres_")]
    m_cols = [c for c in df_raw.columns if str(c).startswith("Mujeres_")]

    # Grupos funcionales etarios calculados en un diccionario para evitar fragmentación
    h_0_5 = [f"Hombres_{i}" for i in range(6) if f"Hombres_{i}" in df_raw.columns]
    m_0_5 = [f"Mujeres_{i}" for i in range(6) if f"Mujeres_{i}" in df_raw.columns]

    h_6_11 = [f"Hombres_{i}" for i in range(6, 12) if f"Hombres_{i}" in df_raw.columns]
    m_6_11 = [f"Mujeres_{i}" for i in range(6, 12) if f"Mujeres_{i}" in df_raw.columns]

    h_12_17 = [f"Hombres_{i}" for i in range(12, 18) if f"Hombres_{i}" in df_raw.columns]
    m_12_17 = [f"Mujeres_{i}" for i in range(12, 18) if f"Mujeres_{i}" in df_raw.columns]

    h_5_17 = [f"Hombres_{i}" for i in range(5, 18) if f"Hombres_{i}" in df_raw.columns]
    m_5_17 = [f"Mujeres_{i}" for i in range(5, 18) if f"Mujeres_{i}" in df_raw.columns]

    h_18_59 = [f"Hombres_{i}" for i in range(18, 60) if f"Hombres_{i}" in df_raw.columns]
    m_18_59 = [f"Mujeres_{i}" for i in range(18, 60) if f"Mujeres_{i}" in df_raw.columns]

    h_60_plus = [f"Hombres_{i}" for i in range(60, 101) if f"Hombres_{i}" in df_raw.columns] + [
        c for c in h_cols if "más" in str(c) or "mas" in str(c)
    ]
    m_60_plus = [f"Mujeres_{i}" for i in range(60, 101) if f"Mujeres_{i}" in df_raw.columns] + [
        c for c in m_cols if "más" in str(c) or "mas" in str(c)
    ]
    h_60_plus = list(dict.fromkeys(h_60_plus))
    m_60_plus = list(dict.fromkeys(m_60_plus))

    engineered_series = {
        "poblacion_0_5": df_raw[h_0_5 + m_0_5].apply(pd.to_numeric, errors="coerce").sum(axis=1),
        "poblacion_6_11": df_raw[h_6_11 + m_6_11].apply(pd.to_numeric, errors="coerce").sum(axis=1),
        "poblacion_12_17": df_raw[h_12_17 + m_12_17].apply(pd.to_numeric, errors="coerce").sum(axis=1),
        "poblacion_5_17": df_raw[h_5_17 + m_5_17].apply(pd.to_numeric, errors="coerce").sum(axis=1),
        "poblacion_18_59": df_raw[h_18_59 + m_18_59].apply(pd.to_numeric, errors="coerce").sum(axis=1),
        "poblacion_60_mas": df_raw[h_60_plus + m_60_plus].apply(pd.to_numeric, errors="coerce").sum(axis=1),
    }

    df_engineered = pd.DataFrame(engineered_series, index=df_raw.index)
    df_result = pd.concat([df_raw, df_engineered], axis=1)

    output_cols = [
        "codigo_localidad",
        "nombre_localidad",
        "area",
        "ano",
        "poblacion_total",
        "poblacion_hombres",
        "poblacion_mujeres",
        "poblacion_0_5",
        "poblacion_6_11",
        "poblacion_12_17",
        "poblacion_5_17",
        "poblacion_18_59",
        "poblacion_60_mas",
    ]

    return df_result[output_cols].sort_values(["ano", "codigo_localidad", "area"]).reset_index(drop=True)


def parse_demografia_upz(
    file_path: Path | str | None = None,
) -> pd.DataFrame:
    """Procesa la hoja 'UPZ Bogota 2018_2024' de proyecciones DANE/SDP."""
    path = Path(file_path) if file_path else RAW_FILE
    if not path.exists():
        raise FileNotFoundError(f"Archivo de demografía no encontrado: {path}")

    df_upz_raw = pd.read_excel(path, sheet_name="UPZ Bogota 2018_2024", header=7)
    df_upz_raw = df_upz_raw.dropna(subset=["UPZ", "AÑO"]).copy()

    df_upz_raw = df_upz_raw.rename(
        columns={
            "AREA GEOGRÁFICA": "nombre_upz",
            "AÑO": "ano",
            "UPZ": "codigo_upz",
            "LOC": "codigo_localidad",
            "Total": "poblacion_total",
            "Total_Hombres": "poblacion_hombres",
            "Total_Mujeres": "poblacion_mujeres",
        }
    )

    df_upz_raw["codigo_upz"] = df_upz_raw["codigo_upz"].astype(str).str.split(".").str[0].str.zfill(3)
    df_upz_raw["codigo_localidad"] = df_upz_raw["codigo_localidad"].astype(str).str.split(".").str[0].str.zfill(2)
    df_upz_raw["ano"] = pd.to_numeric(df_upz_raw["ano"], errors="coerce").astype(int)

    # Identificar grupos de edad quinquenales
    cols = df_upz_raw.columns.tolist()
    h_0_14 = [c for c in cols if str(c).startswith("Hombres_") and any(k in str(c) for k in ["0-4", "5-9", "10-14"])]
    m_0_14 = [c for c in cols if str(c).startswith("Mujeres_") and any(k in str(c) for k in ["0-4", "5-9", "10-14"])]
    pob_0_14 = df_upz_raw[h_0_14 + m_0_14].apply(pd.to_numeric, errors="coerce").sum(axis=1)

    h_60_plus = [c for c in cols if str(c).startswith("Hombres_") and any(f"{i}-" in str(c) or f"{i} " in str(c) for i in range(60, 90))]
    m_60_plus = [c for c in cols if str(c).startswith("Mujeres_") and any(f"{i}-" in str(c) or f"{i} " in str(c) for i in range(60, 90))]
    pob_60_plus = df_upz_raw[h_60_plus + m_60_plus].apply(pd.to_numeric, errors="coerce").sum(axis=1)

    pob_total = pd.to_numeric(df_upz_raw["poblacion_total"], errors="coerce").fillna(0)
    pob_15_59 = pob_total - pob_0_14 - pob_60_plus

    df_upz_raw["poblacion_0_14"] = pob_0_14
    df_upz_raw["poblacion_60_mas"] = pob_60_plus
    df_upz_raw["poblacion_15_59"] = pob_15_59

    output_cols = [
        "codigo_upz",
        "nombre_upz",
        "codigo_localidad",
        "ano",
        "poblacion_total",
        "poblacion_hombres",
        "poblacion_mujeres",
        "poblacion_0_14",
        "poblacion_15_59",
        "poblacion_60_mas",
    ]

    return df_upz_raw[output_cols].sort_values(["ano", "codigo_localidad", "codigo_upz"]).reset_index(drop=True)


def parse_all_demografia_dane(
    file_path: Path | str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Procesa todas las hojas de proyecciones oficiales DANE / SDP y retorna (df_loc, df_2025, df_upz)."""
    df_loc = parse_demografia_localidades(file_path)
    df_loc_2025 = df_loc[(df_loc["ano"] == 2025) & (df_loc["area"] == "Total")].copy().reset_index(drop=True)
    df_upz = parse_demografia_upz(file_path)
    return df_loc, df_loc_2025, df_upz


def generate_canonical_processed_demografia() -> dict[str, Path]:
    """Ejecuta el procesamiento completo y exporta los archivos curados a data/processed/DEMOGRAFIA/."""
    print("Iniciando procesamiento de proyecciones oficiales DANE / SDP...")

    df_loc, df_loc_2025, df_upz = parse_all_demografia_dane()

    out_loc = PROCESSED_DIR / "poblacion_localidad_dane_sdp.csv"
    df_loc.to_csv(out_loc, index=False, encoding="utf-8")
    print(f"Exportado: {out_loc} ({len(df_loc)} registros)")

    # Archivo canónico 2025 para integración y modelado IPT
    out_2025 = PROCESSED_DIR / "poblacion_localidad_2025.csv"
    df_loc_2025.to_csv(out_2025, index=False, encoding="utf-8")
    print(f"Exportado: {out_2025} ({len(df_loc_2025)} localidades para 2025)")

    out_upz = PROCESSED_DIR / "poblacion_upz_dane_sdp.csv"
    df_upz.to_csv(out_upz, index=False, encoding="utf-8")
    print(f"Exportado: {out_upz} ({len(df_upz)} registros)")

    return {
        "localidades_historico": out_loc,
        "localidades_2025": out_2025,
        "upz_historico": out_upz,
    }


if __name__ == "__main__":
    generate_canonical_processed_demografia()

