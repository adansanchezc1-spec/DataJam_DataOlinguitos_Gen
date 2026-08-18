"""Catálogo de indicadores objetivo del IPT y su factibilidad con datos actuales."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
STATUS_DIR = ROOT / "data" / "status"

# id -> especificación del indicador objetivo
INDICATOR_SPECS: dict[str, dict] = {
    "POB-01": {
        "nombre": "Población total por localidad",
        "formula": "suma de POBLACION por localidad (año de corte)",
        "inputs": ["osb_demografia-poblacion-localidad.csv"],
        "dimension": "Demografía",
        "estado": "construible_ahora",
        "que_falta": "Nada: fuente por localidad 2005-2035.",
    },
    "POB-02": {
        "nombre": "Población 0-17 años por localidad",
        "formula": "suma de POBLACION con EDAD 0-17 por localidad",
        "inputs": ["osb_demografia-poblacion-localidad.csv"],
        "dimension": "Demografía",
        "estado": "construible_ahora",
        "que_falta": "Nada: EDAD viene desagregada.",
    },
    "POB-03": {
        "nombre": "Población 60+ por localidad",
        "formula": "suma de POBLACION con EDAD >= 60 por localidad",
        "inputs": ["osb_demografia-poblacion-localidad.csv"],
        "dimension": "Demografía",
        "estado": "construible_ahora",
        "que_falta": "Nada.",
    },
    "POB-04": {
        "nombre": "Índice de dependencia y envejecimiento por localidad",
        "formula": "(pob <15 + pob 60+) / pob 15-59; pob 60+ / pob <15",
        "inputs": ["osb_demografia-poblacion-localidad.csv"],
        "dimension": "Demografía",
        "estado": "construible_ahora",
        "que_falta": "Nada.",
    },
    "SAL-01": {
        "nombre": "IPS por localidad (acceso a salud)",
        "formula": "conteo espacial de IPS dentro de cada localidad (cruce con capa Loca)",
        "inputs": ["ips_sds.gpkg", "gpkg_mr_v03.26.gpkg (capa Loca)"],
        "dimension": "Salud",
        "estado": "construible_con_cruce_espacial",
        "que_falta": "IPS no trae localidad explícita; requiere sjoin con Loca del MR.",
    },
    "SAL-02": {
        "nombre": "Camas hospitalarias por 10.000 habitantes",
        "formula": "camas / población * 10000",
        "inputs": ["osb_tiporazoncamas.csv", "población"],
        "dimension": "Salud",
        "estado": "faltante_territorial",
        "que_falta": "Fuente distrital sin desagregación por localidad; falta REPS territorializado.",
    },
    "EDU-01": {
        "nombre": "Sedes educativas por localidad",
        "formula": "conteo de colegios por COD_LOCA",
        "inputs": ["colegios122025.gpkg"],
        "dimension": "Educación",
        "estado": "construible_ahora",
        "que_falta": "Nada: COD_LOCA presente.",
    },
    "EDU-02": {
        "nombre": "Matrícula oficial por localidad y por 1.000 niños 0-17",
        "formula": "suma TMATRIC_GE por COD_LOCA; / población 0-17 * 1000",
        "inputs": ["matricula_total_colegios_oficiales.gpkg", "población 0-17"],
        "dimension": "Educación",
        "estado": "construible_ahora",
        "que_falta": "Nada: COD_LOCA y TMATRIC_GE presentes.",
    },
    "MOV-01": {
        "nombre": "Paraderos SITP por 10.000 habitantes",
        "formula": "conteo de paraderos por localidad_ / población * 10000",
        "inputs": ["paraderos_zonales_sitp.gpkg", "población"],
        "dimension": "Movilidad",
        "estado": "construible_ahora",
        "que_falta": "Nada: campo localidad_ con 20 localidades.",
    },
    "MOV-02": {
        "nombre": "Estaciones troncales por localidad",
        "formula": "conteo espacial de estaciones dentro de cada localidad",
        "inputs": ["estaciones_troncales.geojson", "gpkg_mr_v03.26.gpkg (capa Loca)"],
        "dimension": "Movilidad",
        "estado": "construible_con_cruce_espacial",
        "que_falta": "Estaciones sin localidad explícita; requiere sjoin con Loca.",
    },
    "MOV-03": {
        "nombre": "Demanda mensual por estación/paradero (validaciones tullave)",
        "formula": "parseo de XLSX mensuales: transacciones por estación y día",
        "inputs": ["Validaciones/*.xlsx (62 archivos 2024-2026)"],
        "dimension": "Movilidad",
        "estado": "construible_parcial",
        "que_falta": "Formato de hoja irregular por archivo; requiere parser dedicado por layout.",
    },
    "MOV-04": {
        "nombre": "Flota vinculada y accesibilidad por zona",
        "formula": "conteo de buses por zona y componente",
        "inputs": ["flota_vinculada_sitp_2024-12.csv"],
        "dimension": "Movilidad",
        "estado": "construible_ahora",
        "que_falta": "Nada.",
    },
    "FIN-01": {
        "nombre": "Inversión educativa per cápita por localidad",
        "formula": "R_EJECUTADOS / población total",
        "inputs": ["inversion_educacion_por_localidad_12_2025.gpkg", "población"],
        "dimension": "Finanzas",
        "estado": "construible_ahora",
        "que_falta": "Solo inversión educativa (SED), no inversión multisectorial.",
    },
    "FIN-02": {
        "nombre": "% de ejecución y giro de inversión por localidad",
        "formula": "R_EJECUTADOS/R_ASIGNADOS*100; R_GIRADOS/R_ASIGNADOS*100",
        "inputs": ["inversion_educacion_por_localidad_12_2025.gpkg"],
        "dimension": "Finanzas",
        "estado": "construible_ahora",
        "que_falta": "Nada.",
    },
    "INF-01": {
        "nombre": "Parques por localidad",
        "formula": "conteo por Nombre Localidad",
        "inputs": ["5.-parques-idrd.csv"],
        "dimension": "Infraestructura",
        "estado": "construible_ahora",
        "que_falta": "Nada.",
    },
    "INF-02": {
        "nombre": "m² de parque por habitante",
        "formula": "área total de parques / población",
        "inputs": ["5.-parques-idrd.csv", "área de parques", "población"],
        "dimension": "Infraestructura",
        "estado": "faltante",
        "que_falta": "El CSV IDRD no incluye área; requiere geometría de parques (fuente externa o MR).",
    },
    "INF-03": {
        "nombre": "Estado superficial de vías",
        "formula": "distribución de ESTADO_SUPERFICIAL por vía (CalCodigo)",
        "inputs": ["estado/Estado.csv", "malla vial (MR capa MVI)"],
        "dimension": "Infraestructura",
        "estado": "construible_parcial",
        "que_falta": "Estado por CalCodigo; para territorializar se necesita cruce con malla vial del MR.",
    },
    "AMB-01": {
        "nombre": "Indicadores ambientales por localidad",
        "formula": "por definir",
        "inputs": [],
        "dimension": "Ambiente",
        "estado": "faltante",
        "que_falta": "Sector sin datos analíticos en data/raw (solo README).",
    },
    "PAR-01": {
        "nombre": "Indicadores de participación ciudadana",
        "formula": "por definir",
        "inputs": [],
        "dimension": "Participación",
        "estado": "faltante",
        "que_falta": "Sector sin datos analíticos (solo README).",
    },
    "SEG-01": {
        "nombre": "Indicadores de seguridad por localidad",
        "formula": "por definir",
        "inputs": [],
        "dimension": "Seguridad",
        "estado": "faltante",
        "que_falta": "Sector sin datos analíticos (solo README).",
    },
    "SER-01": {
        "nombre": "Indicadores de servicios públicos",
        "formula": "por definir",
        "inputs": [],
        "dimension": "Servicios Públicos",
        "estado": "faltante",
        "que_falta": "Sector sin datos analíticos (carpeta vacía).",
    },
}


def load_catalog() -> pd.DataFrame:
    path = STATUS_DIR / "source_catalog.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_approved() -> pd.DataFrame:
    path = STATUS_DIR / "approved_sources.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def indicator_status() -> pd.DataFrame:
    """Tabla de estado de todos los indicadores objetivo, con inputs y qué falta."""
    rows = []
    for iid, spec in INDICATOR_SPECS.items():
        rows.append(
            {
                "id": iid,
                "indicador": spec["nombre"],
                "dimension": spec["dimension"],
                "formula": spec["formula"],
                "inputs_necesarios": "; ".join(spec["inputs"]),
                "estado": spec["estado"],
                "que_falta": spec["que_falta"],
            }
        )
    return pd.DataFrame(rows)


def indicator_status_by_dimension(dimension: str) -> pd.DataFrame:
    df = indicator_status()
    if dimension:
        df = df[df["dimension"].eq(dimension)]
    return df.reset_index(drop=True)
