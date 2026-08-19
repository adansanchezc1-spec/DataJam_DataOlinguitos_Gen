"""Reorganización y Concatenación de Notebooks en Carpetas por Fase PDCO / SDLC.

Estándar: AGENTS.md, SWEBOK, DAMA-BOK, Clean Code
Autoría: Persona A (Adan) & Persona B (Yesid)
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"
EDA_DIR = NOTEBOOKS_DIR / "eda"

# Carpetas de fases
INGESTION_DIR = NOTEBOOKS_DIR / "01_ingestion"
VALIDATION_DIR = NOTEBOOKS_DIR / "02_validation"
INTEGRATION_DIR = NOTEBOOKS_DIR / "03_integration"
MODELING_DIR = NOTEBOOKS_DIR / "04_modeling"
VISUALIZATION_DIR = NOTEBOOKS_DIR / "05_visualization"

for d in [INGESTION_DIR, VALIDATION_DIR, INTEGRATION_DIR, MODELING_DIR, VISUALIZATION_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def load_nb(path: Path | str | None) -> dict:
    """Carga un notebook JSON si existe el archivo."""
    if not path:
        return {"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    p = Path(path)
    if not p.is_file():
        return {"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    return json.loads(p.read_text(encoding="utf-8"))


def save_nb(path: Path, nb_data: dict):
    """Guarda un notebook JSON asegurando formato v4."""
    if "nbformat" not in nb_data:
        nb_data["nbformat"] = 4
        nb_data["nbformat_minor"] = 5
    if "metadata" not in nb_data:
        nb_data["metadata"] = {}
    path.write_text(json.dumps(nb_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Notebook guardado en: {path.relative_to(ROOT)} ({len(nb_data.get('cells', []))} celdas)")


def make_header_cell(title: str, phase: str, author: str, objective: str, inputs: str, outputs: str) -> dict:
    """Genera celda de encabezado estándar."""
    text = f"""# SIPTA — {title}
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: {phase} | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: {author}  
**Objetivo**: {objective}  
**Datos de Entrada**: `{inputs}`  
**Datos de Salida**: `{outputs}`  
"""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")],
    }


def make_section_cell(title: str) -> dict:
    """Genera celda markdown de separación de sección."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [f"## {title}\n", "\n"],
    }


def make_ingestion_demografia_cells() -> list[dict]:
    """Genera celdas de ingesta técnica para demografía."""
    return [
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pathlib import Path\n",
                "import pandas as pd\n",
                "\n",
                "ROOT = Path('..').resolve()\n",
                "RAW_DIR = ROOT / 'data' / 'raw' / 'DEMOGRAFIA'\n",
                "PROCESSED_DIR = ROOT / 'data' / 'processed' / 'DEMOGRAFIA'\n",
                "PROCESSED_DIR.mkdir(parents=True, exist_ok=True)\n",
                "\n",
                "# Carga de proyecciones por Localidad (2005-2035)\n",
                "file_loc = RAW_DIR / 'osb_demografia-poblacion-localidad.csv'\n",
                "df_loc = pd.read_csv(file_loc, sep=';', encoding='utf-8')\n",
                "print('Proyecciones por Localidad:', df_loc.shape)\n",
                "display(df_loc.head())\n",
                "\n",
                "# Carga de proyecciones por UPL\n",
                "file_upl = RAW_DIR / 'osb_demografia-poblacion-upl.csv'\n",
                "df_upl = pd.read_csv(file_upl, sep=';', encoding='utf-8')\n",
                "print('Proyecciones por UPL:', df_upl.shape)\n",
                "display(df_upl.head())\n",
                "\n",
                "# Exportación a processed\n",
                "df_loc.to_csv(PROCESSED_DIR / 'osb_demografia-poblacion-localidad.csv', index=False, sep=';')\n",
                "df_upl.to_csv(PROCESSED_DIR / 'osb_demografia-poblacion-upl.csv', index=False, sep=';')\n",
                "print('Datos demográficos persistidos en data/processed/DEMOGRAFIA/')\n"
            ]
        }
    ]


def make_ingestion_movilidad_cells() -> list[dict]:
    """Genera celdas de ingesta técnica para movilidad."""
    return [
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pathlib import Path\n",
                "import pandas as pd\n",
                "\n",
                "ROOT = Path('..').resolve()\n",
                "RAW_DIR = ROOT / 'data' / 'raw' / 'MOVILIDAD'\n",
                "PROCESSED_DIR = ROOT / 'data' / 'processed' / 'MOVILIDAD'\n",
                "PROCESSED_DIR.mkdir(parents=True, exist_ok=True)\n",
                "\n",
                "# Carga de Flota SITP\n",
                "try:\n",
                "    df_flota = pd.read_csv(RAW_DIR / 'flota_vinculada_sitp_2024-12.csv', sep=',', encoding='utf-8')\n",
                "except UnicodeDecodeError:\n",
                "    df_flota = pd.read_csv(RAW_DIR / 'flota_vinculada_sitp_2024-12.csv', sep=',', encoding='latin1')\n",
                "print('Flota SITP:', df_flota.shape)\n",
                "display(df_flota.head())\n",
                "\n",
                "# Carga de Rutas SITP\n",
                "try:\n",
                "    df_rutas = pd.read_csv(RAW_DIR / 'servicios_rutas_troncales_zonales.csv', sep=',', encoding='utf-8')\n",
                "except UnicodeDecodeError:\n",
                "    df_rutas = pd.read_csv(RAW_DIR / 'servicios_rutas_troncales_zonales.csv', sep=',', encoding='latin1')\n",
                "print('Rutas y Servicios:', df_rutas.shape)\n",
                "\n",
                "# Exportación\n",
                "df_flota.to_csv(PROCESSED_DIR / 'flota_vinculada_sitp_2024-12.csv', index=False)\n",
                "df_rutas.to_csv(PROCESSED_DIR / 'servicios_rutas_troncales_zonales.csv', index=False)\n",
                "print('Datos de movilidad persistidos en data/processed/MOVILIDAD/')\n"
            ]
        }
    ]


def make_ingestion_infraestructura_cells() -> list[dict]:
    """Genera celdas de ingesta técnica para infraestructura."""
    return [
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pathlib import Path\n",
                "import pandas as pd\n",
                "\n",
                "ROOT = Path('..').resolve()\n",
                "RAW_DIR = ROOT / 'data' / 'raw' / 'INFRAESTRUCTURA_ESPACIO_PUBLICO'\n",
                "PROCESSED_DIR = ROOT / 'data' / 'processed' / 'INFRAESTRUCTURA_ESPACIO_PUBLICO'\n",
                "PROCESSED_DIR.mkdir(parents=True, exist_ok=True)\n",
                "\n",
                "# Carga de Parques IDRD\n",
                "df_parques = pd.read_csv(RAW_DIR / '5.-parques-idrd.csv', sep=';', encoding='latin1')\n",
                "print('Parques IDRD Shape:', df_parques.shape)\n",
                "display(df_parques.head())\n",
                "\n",
                "# Exportación\n",
                "df_parques.to_csv(PROCESSED_DIR / '5.-parques-idrd.csv', index=False, sep=';', encoding='utf-8')\n",
                "print('Datos de parques persistidos en data/processed/INFRAESTRUCTURA_ESPACIO_PUBLICO/')\n"
            ]
        }
    ]


def make_validation_notebook(dom_key: str, dom_title: str, author: str, raw_file_code: str) -> dict:
    """Crea un notebook de validación estructurado con reporte visual."""
    cells = [
        make_header_cell(
            title=f"Validación de Calidad: {dom_title}",
            phase="CONTROL",
            author=author,
            objective=f"Validación formal de esquemas, tipos, nulos, duplicados y llaves territoriales para {dom_title} bajo normas ISO/IEC 25010 y DAMA-BOK.",
            inputs="data/raw/*",
            outputs="reports/validation/*",
        ),
        make_section_cell("1. Inicialización y Carga de Funciones de Validación"),
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "ROOT = Path('..').resolve()\n",
                "sys.path.insert(0, str(ROOT))\n",
                "\n",
                "import pandas as pd\n",
                "from src.validation.validate_data import (\n",
                "    inspect_schema,\n",
                "    validate_dataset_quality,\n",
                "    validate_territorial_column,\n",
                "    export_validation_report,\n",
                f"    validate_{dom_key}\n",
                ")\n",
                "\n",
                f"# Ejecutar validador oficial del dominio {dom_key}\n",
                f"report = validate_{dom_key}()\n",
                "print('=== REPORTE EJECUTIVO DE VALIDACIÓN ===')\n",
                "for k, v in report.items():\n",
                "    if k != 'territorial_validation':\n",
                "        print(f'{k}: {v}')\n"
            ]
        },
        make_section_cell("2. Inspección Detallada de Esquema y Calidad"),
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                raw_file_code,
                "schema_df = inspect_schema(df)\n",
                "display(schema_df)\n"
            ]
        },
        make_section_cell("3. Evaluación de Consistencia Territorial (20 Localidades)"),
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "terr_eval = report.get('territorial_validation')\n",
                "if terr_eval:\n",
                "    print(f\"Columna Territorial: {terr_eval['column']}\")\n",
                "    print(f\"Cobertura: {terr_eval['cobertura_pct']}%\")\n",
                "    print(f\"Localidades Encontradas ({terr_eval['total_localidades_detectadas']}): {terr_eval['localidades_encontradas']}\")\n",
                "else:\n",
                "    print('Validación territorial delegada a cruce espacial (Spatial Join EPSG:4326).')\n"
            ]
        }
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.13.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def merge_and_generate_all():
    """Ejecuta la consolidación completa."""
    print("Iniciando consolidación y estructuración de notebooks...")

    # =========================================================================
    # FASE 1: INGESTION + EDA (notebooks/01_ingestion/)
    # =========================================================================

    # 1.0 Ingesta & EDA Master
    nb_ing_master = load_nb(NOTEBOOKS_DIR / "01_ingestion.ipynb")
    nb_eda_master = load_nb(EDA_DIR / "00_eda_maestro.ipynb")
    nb_eda_gaps = load_nb(EDA_DIR / "07_eda_gaps.ipynb")

    cells_00 = [
        make_header_cell(
            "Ingesta y EDA Maestro: Consolidado Distrital Multi-Sectorial",
            "DEVELOPMENT",
            "Persona A (Adan — Lead Data Engineer) & Persona B (Yesid — Data Scientist)",
            "Orquestación general de ingesta, auditoría exploratoria multi-sectorial y detección de brechas (Gaps).",
            "data/raw/*",
            "data/processed/* / reports/eda/*"
        ),
        make_section_cell("1. Ingesta y Descubrimiento de Datos Crudos"),
    ] + nb_ing_master.get("cells", []) + [
        make_section_cell("2. Análisis Exploratorio Multi-Sectorial"),
    ] + nb_eda_master.get("cells", []) + [
        make_section_cell("3. Análisis de Brechas y Factibilidad Territorial"),
    ] + nb_eda_gaps.get("cells", [])

    save_nb(INGESTION_DIR / "00_ingestion_eda_master.ipynb", {"cells": cells_00, "metadata": nb_ing_master.get("metadata", {})})

    # 1.1 Demografia
    nb_eda_demo = load_nb(EDA_DIR / "01_eda_demografia.ipynb")
    cells_01 = [
        make_header_cell(
            "Ingesta y EDA: Demografía y Población (Localidad & UPL)",
            "DEVELOPMENT",
            "Persona A (Adan) & Persona B (Yesid)",
            "Ingesta técnica de proyecciones 2005-2035 y análisis exploratorio demográfico y pirámides etarias.",
            "data/raw/DEMOGRAFIA/*",
            "data/processed/DEMOGRAFIA/*"
        ),
        make_section_cell("1. Ingesta y Carga de Proyecciones de Población"),
    ] + make_ingestion_demografia_cells() + [
        make_section_cell("2. Análisis Exploratorio de Datos (EDA) Demográfico"),
    ] + nb_eda_demo.get("cells", [])
    save_nb(INGESTION_DIR / "01_ingestion_demografia.ipynb", {"cells": cells_01, "metadata": nb_eda_demo.get("metadata", {})})

    # 1.2 Salud
    nb_ing_salud = load_nb(NOTEBOOKS_DIR / "01_ingestion_salud.ipynb")
    nb_eda_salud = load_nb(EDA_DIR / "02_eda_salud.ipynb")
    cells_02 = [
        make_header_cell(
            "Ingesta y EDA: Salud y Capacidad Hospitalaria",
            "DEVELOPMENT",
            "Persona B (Yesid Bello — Data Scientist)",
            "Carga de IPS con urgencias, razón de camas hospitalarias y análisis exploratorio asistencial.",
            "data/raw/SALUD/*",
            "data/processed/SALUD/*"
        ),
        make_section_cell("1. Ingesta y Carga de Fuentes de Salud (SaluData / SDS)"),
    ] + nb_ing_salud.get("cells", []) + [
        make_section_cell("2. Análisis Exploratorio de Datos (EDA) del Sector Salud"),
    ] + nb_eda_salud.get("cells", [])
    save_nb(INGESTION_DIR / "02_ingestion_salud.ipynb", {"cells": cells_02, "metadata": nb_ing_salud.get("metadata", {})})

    # 1.3 Educacion
    nb_ing_edu = load_nb(NOTEBOOKS_DIR / "01_ingestion_educacion.ipynb")
    nb_eda_edu = load_nb(EDA_DIR / "03_eda_educacion.ipynb")
    cells_03 = [
        make_header_cell(
            "Ingesta y EDA: Educación y Cobertura Escolar",
            "DEVELOPMENT",
            "Persona B (Yesid Bello — Data Scientist)",
            "Ingesta de oferta de cupos, colegios SED, matrícula oficial y análisis exploratorio educativo.",
            "data/raw/EDUCACION/*",
            "data/processed/EDUCACION/*"
        ),
        make_section_cell("1. Ingesta y Carga de Sedes, Matrícula y Oferta de Cupos"),
    ] + nb_ing_edu.get("cells", []) + [
        make_section_cell("2. Análisis Exploratorio de Datos (EDA) del Sector Educación"),
    ] + nb_eda_edu.get("cells", [])
    save_nb(INGESTION_DIR / "03_ingestion_educacion.ipynb", {"cells": cells_03, "metadata": nb_ing_edu.get("metadata", {})})

    # 1.4 Movilidad
    nb_eda_mov = load_nb(EDA_DIR / "04_eda_movilidad.ipynb")
    cells_04 = [
        make_header_cell(
            "Ingesta y EDA: Movilidad y Transporte Masivo (SITP / TransMilenio)",
            "DEVELOPMENT",
            "Persona A (Adan Sánchez — Lead Data Engineer)",
            "Ingesta de flota SITP, rutas, estaciones troncales, paraderos zonales, GTFS y análisis exploratorio espacial y de demanda.",
            "data/raw/MOVILIDAD/*",
            "data/processed/MOVILIDAD/*"
        ),
        make_section_cell("1. Ingesta y Estructuración de Flota y Redes de Transporte"),
    ] + make_ingestion_movilidad_cells() + [
        make_section_cell("2. Análisis Exploratorio de Movilidad y Accesibilidad Espacial"),
    ] + nb_eda_mov.get("cells", [])
    save_nb(INGESTION_DIR / "04_ingestion_movilidad.ipynb", {"cells": cells_04, "metadata": nb_eda_mov.get("metadata", {})})

    # 1.5 Infraestructura
    nb_eda_infra = load_nb(EDA_DIR / "05_eda_infraestructura.ipynb")
    cells_05 = [
        make_header_cell(
            "Ingesta y EDA: Infraestructura y Espacio Público (Parques IDRD)",
            "DEVELOPMENT",
            "Persona A (Adan Sánchez — Lead Data Engineer)",
            "Ingesta de parques distritales IDRD, equipamientos asistenciales y análisis exploratorio de espacio público.",
            "data/raw/INFRAESTRUCTURA_ESPACIO_PUBLICO/*",
            "data/processed/INFRAESTRUCTURA_ESPACIO_PUBLICO/*"
        ),
        make_section_cell("1. Ingesta y Normalización de Parques y Equipamientos"),
    ] + make_ingestion_infraestructura_cells() + [
        make_section_cell("2. Análisis Exploratorio de Espacio Verde y Recreación"),
    ] + nb_eda_infra.get("cells", [])
    save_nb(INGESTION_DIR / "05_ingestion_infraestructura.ipynb", {"cells": cells_05, "metadata": nb_eda_infra.get("metadata", {})})

    # 1.6 Finanzas
    nb_ing_fin = load_nb(NOTEBOOKS_DIR / "01_ingestion_finanzas.ipynb")
    nb_eda_fin = load_nb(EDA_DIR / "06_eda_finanzas.ipynb")
    cells_06 = [
        make_header_cell(
            "Ingesta y EDA: Finanzas, Economía Informal (RIVI) e Inversión",
            "DEVELOPMENT",
            "Persona A (Adan Sánchez — Lead Data Engineer)",
            "Consolidación de series semestrales RIVI (2017-2019), puntos de encuentro IPES, inversión educativa SED y análisis exploratorio.",
            "data/raw/FINANZAS_INVERSION_PUBLICA/*",
            "data/processed/FINANZAS_INVERSION_PUBLICA/*"
        ),
        make_section_cell("1. Ingesta y Consolidación de Series RIVI y Puntos de Encuentro"),
    ] + nb_ing_fin.get("cells", []) + [
        make_section_cell("2. Análisis Exploratorio de Economía Informal e Inversión"),
    ] + nb_eda_fin.get("cells", [])
    save_nb(INGESTION_DIR / "06_ingestion_finanzas.ipynb", {"cells": cells_06, "metadata": nb_ing_fin.get("metadata", {})})

    # 1.7 Ambiente
    nb_ing_amb = load_nb(NOTEBOOKS_DIR / "01_ingestion_ambiental.ipynb")
    cells_07 = [
        make_header_cell(
            "Ingesta y EDA: Ambiente, Calidad del Aire y Conflictos SAC",
            "DEVELOPMENT",
            "Persona A (Adan Sánchez — Lead Data Engineer)",
            "Ingesta y análisis de estaciones RMCAB y Situaciones Ambientales Conflictivas (SAC) de la Secretaría Distrital de Ambiente.",
            "data/raw/AMBIENTE/*",
            "data/processed/AMBIENTE/*"
        ),
        make_section_cell("1. Ingesta y Análisis Exploratorio de Datos Ambientales"),
    ] + nb_ing_amb.get("cells", [])
    save_nb(INGESTION_DIR / "07_ingestion_ambiental.ipynb", {"cells": cells_07, "metadata": nb_ing_amb.get("metadata", {})})

    # 1.8 Seguridad
    nb_ing_seg = load_nb(NOTEBOOKS_DIR / "01_ingestion_seguridad.ipynb")
    cells_08 = [
        make_header_cell(
            "Ingesta y EDA: Seguridad y Convivencia (Cuadrantes MEBOG)",
            "DEVELOPMENT",
            "Persona A (Adan Sánchez — Lead Data Engineer)",
            "Ingesta y análisis exploratorio de los 599 cuadrantes policiales del MNVCC y cobertura territorial distrital.",
            "data/raw/SEGURIDAD/*",
            "data/processed/SEGURIDAD/*"
        ),
        make_section_cell("1. Ingesta y Análisis Exploratorio de Seguridad Ciudadana"),
    ] + nb_ing_seg.get("cells", [])
    save_nb(INGESTION_DIR / "08_ingestion_seguridad.ipynb", {"cells": cells_08, "metadata": nb_ing_seg.get("metadata", {})})

    # =========================================================================
    # FASE 2: VALIDATION (notebooks/02_validation/)
    # =========================================================================

    # 2.0 Master Validation
    nb_val_master = load_nb(NOTEBOOKS_DIR / "02_validation.ipynb")
    save_nb(VALIDATION_DIR / "00_validation_master.ipynb", nb_val_master)

    # 2.1 Demografia
    save_nb(
        VALIDATION_DIR / "01_validation_demografia.ipynb",
        make_validation_notebook(
            "demografia",
            "Demografía y Población",
            "Persona A & Persona B",
            "df = pd.read_csv(ROOT / 'data' / 'raw' / 'DEMOGRAFIA' / 'osb_demografia-poblacion-localidad.csv', sep=';', encoding='utf-8')\n"
        )
    )

    # 2.2 Salud (Refactor)
    nb_val_salud = load_nb(NOTEBOOKS_DIR / "02_validation_salud.ipynb")
    cells_val_salud = [
        make_header_cell(
            "Validación de Calidad: Salud y Capacidad Hospitalaria",
            "CONTROL",
            "Persona B (Yesid Bello — Data Scientist)",
            "Validación de calidad estructural, unicidad de IPS de urgencias, coordenadas geográficas y razón de camas.",
            "data/raw/SALUD/*",
            "reports/validation/dominios/val_salud.json"
        )
    ] + [c for c in nb_val_salud.get("cells", []) if not (c.get("cell_type") == "markdown" and "# SIPTA" in "".join(c.get("source", [])))]
    save_nb(VALIDATION_DIR / "02_validation_salud.ipynb", {"cells": cells_val_salud, "metadata": nb_val_salud.get("metadata", {})})

    # 2.3 Educacion (Refactor)
    nb_val_edu = load_nb(NOTEBOOKS_DIR / "02_validation_educacion.ipynb")
    cells_val_edu = [
        make_header_cell(
            "Validación de Calidad: Educación y Oferta de Cupos",
            "CONTROL",
            "Persona B (Yesid Bello — Data Scientist)",
            "Validación de coherencia de cupos escolares oficiales, unicidad DANE, códigos de localidad y proyección WGS84.",
            "data/raw/EDUCACION/*",
            "reports/validation/dominios/val_educacion.json"
        )
    ] + [c for c in nb_val_edu.get("cells", []) if not (c.get("cell_type") == "markdown" and "# SIPTA" in "".join(c.get("source", [])))]
    save_nb(VALIDATION_DIR / "03_validation_educacion.ipynb", {"cells": cells_val_edu, "metadata": nb_val_edu.get("metadata", {})})

    # 2.4 Movilidad
    save_nb(
        VALIDATION_DIR / "04_validation_movilidad.ipynb",
        make_validation_notebook(
            "movilidad",
            "Movilidad y Flota SITP",
            "Persona A (Adan Sánchez)",
            "flota_p = ROOT / 'data' / 'raw' / 'MOVILIDAD' / 'flota_vinculada_sitp_2024-12.csv'\ntry:\n    df = pd.read_csv(flota_p, sep=',', encoding='utf-8')\nexcept UnicodeDecodeError:\n    df = pd.read_csv(flota_p, sep=',', encoding='latin1')\n"
        )
    )

    # 2.5 Infraestructura
    save_nb(
        VALIDATION_DIR / "05_validation_infraestructura.ipynb",
        make_validation_notebook(
            "infraestructura",
            "Infraestructura y Parques IDRD",
            "Persona A (Adan Sánchez)",
            "df = pd.read_csv(ROOT / 'data' / 'raw' / 'INFRAESTRUCTURA_ESPACIO_PUBLICO' / '5.-parques-idrd.csv', sep=';', encoding='latin1')\n"
        )
    )

    # 2.6 Finanzas
    save_nb(
        VALIDATION_DIR / "06_validation_finanzas.ipynb",
        make_validation_notebook(
            "finanzas",
            "Finanzas y Vendedores Informales RIVI",
            "Persona A (Adan Sánchez)",
            "files = sorted(list((ROOT / 'data' / 'raw' / 'FINANZAS_INVERSION_PUBLICA').glob('rivi-numero-*.txt')))\ndfs = [pd.read_csv(f, sep=None, engine='python', encoding='latin1') for f in files]\ndf = pd.concat(dfs, ignore_index=True)\n"
        )
    )

    # 2.7 Ambiente
    save_nb(
        VALIDATION_DIR / "07_validation_ambiental.ipynb",
        make_validation_notebook(
            "ambiente",
            "Ambiente y Conflictos SAC",
            "Persona A (Adan Sánchez)",
            "df = pd.read_csv(ROOT / 'data' / 'raw' / 'AMBIENTE' / 'situacion_ambiental_conflictiva.csv', sep=';', encoding='latin1')\n"
        )
    )

    # 2.8 Seguridad
    save_nb(
        VALIDATION_DIR / "08_validation_seguridad.ipynb",
        make_validation_notebook(
            "seguridad",
            "Seguridad y Cuadrantes Policiales MEBOG",
            "Persona A (Adan Sánchez)",
            "df = pd.read_csv(ROOT / 'data' / 'raw' / 'SEGURIDAD' / 'Cuadrante de Policía. Bogotá D.C.csv', sep=';', encoding='latin1')\n"
        )
    )

    # =========================================================================
    # FASE 3, 4, 5: INTEGRATION, MODELING, VISUALIZATION
    # =========================================================================
    save_nb(INTEGRATION_DIR / "01_integration_master.ipynb", load_nb(NOTEBOOKS_DIR / "03_integration.ipynb"))
    save_nb(MODELING_DIR / "01_modeling_ipt.ipynb", load_nb(NOTEBOOKS_DIR / "04_modeling.ipynb"))
    save_nb(VISUALIZATION_DIR / "01_visualization_dashboard.ipynb", load_nb(NOTEBOOKS_DIR / "05_visualization.ipynb"))

    # =========================================================================
    # LIMPIEZA DE ARCHIVOS SUELTOS EN RAIZ DE NOTEBOOKS Y EDA
    # =========================================================================
    for loose in list(NOTEBOOKS_DIR.glob("*.ipynb")):
        loose.unlink()
        print(f"Eliminado notebook suelto de raíz: {loose.name}")

    if EDA_DIR.exists():
        shutil.rmtree(EDA_DIR, ignore_errors=True)
        print("Directorio temporal notebooks/eda/ consolidado.")

    print("Reorganización completa ejecutada con éxito.")


if __name__ == "__main__":
    merge_and_generate_all()
