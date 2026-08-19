"""Reorganización y Actualización de Autoría de EDA en Notebooks de Ingesta.

Estándar: AGENTS.md, SWEBOK, DAMA-BOK, Clean Code
Autoría EDA: Persona A (Adan Sánchez — Lead Data Engineer)
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ING_DIR = ROOT / "notebooks" / "01_ingestion"


def update_notebook_author(nb_path: Path, new_header_text: str):
    """Actualiza la celda de encabezado del notebook."""
    if not nb_path.exists():
        return
    data = json.loads(nb_path.read_text(encoding="utf-8"))
    
    header_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in new_header_text.strip().split("\n")]
    }
    
    # Reemplazar la primera celda si es markdown de encabezado
    if data.get("cells") and data["cells"][0].get("cell_type") == "markdown" and "# SIPTA" in "".join(data["cells"][0].get("source", [])):
        data["cells"][0] = header_cell
    else:
        data["cells"].insert(0, header_cell)
        
    nb_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Actualizado autor en: {nb_path.name}")


def update_all_ingestion_eda_authorship():
    # 00 Master
    update_notebook_author(
        ING_DIR / "00_ingestion_eda_master.ipynb",
        """# SIPTA — Ingesta y EDA Maestro: Consolidado Distrital Multi-Sectorial
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona A (Adan Sánchez — Lead Data Engineer & Autor de EDA)**  
**Colaboración en fuentes**: Persona B (Yesid Bello — Data Scientist)  
**Objetivo**: Orquestación general de ingesta, auditoría exploratoria multi-sectorial y análisis de brechas de datos (EDA).  
**Datos de Entrada**: `data/raw/*`  
**Datos de Salida**: `data/processed/* / reports/eda/*`"""
    )

    # 01 Demografia
    update_notebook_author(
        ING_DIR / "01_ingestion_demografia.ipynb",
        """# SIPTA — Ingesta y EDA: Demografía y Población (Localidad & UPL)
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona A (Adan Sánchez — Lead Data Engineer & Autor de EDA)**  
**Objetivo**: Ingesta técnica de proyecciones 2005-2035 y análisis exploratorio demográfico y pirámides etarias (EDA).  
**Datos de Entrada**: `data/raw/DEMOGRAFIA/*`  
**Datos de Salida**: `data/processed/DEMOGRAFIA/*`"""
    )

    # 02 Salud
    update_notebook_author(
        ING_DIR / "02_ingestion_salud.ipynb",
        """# SIPTA — Ingesta y EDA: Salud y Capacidad Hospitalaria
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona A (Adan Sánchez — Análisis Exploratorio de Datos / EDA)**  
**Relevamiento de fuentes**: Persona B (Yesid Bello — Data Scientist)  
**Objetivo**: Carga de IPS con urgencias, razón de camas hospitalarias y análisis exploratorio asistencial (EDA).  
**Datos de Entrada**: `data/raw/SALUD/*`  
**Datos de Salida**: `data/processed/SALUD/*`"""
    )

    # 03 Educacion
    update_notebook_author(
        ING_DIR / "03_ingestion_educacion.ipynb",
        """# SIPTA — Ingesta y EDA: Educación y Cobertura Escolar
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona A (Adan Sánchez — Análisis Exploratorio de Datos / EDA)**  
**Relevamiento de fuentes**: Persona B (Yesid Bello — Data Scientist)  
**Objetivo**: Ingesta de oferta de cupos, colegios SED, matrícula oficial y análisis exploratorio educativo (EDA).  
**Datos de Entrada**: `data/raw/EDUCACION/*`  
**Datos de Salida**: `data/processed/EDUCACION/*`"""
    )

    # 04 Movilidad
    update_notebook_author(
        ING_DIR / "04_ingestion_movilidad.ipynb",
        """# SIPTA — Ingesta y EDA: Movilidad y Transporte Masivo (SITP / TransMilenio)
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona A (Adan Sánchez — Lead Data Engineer & Autor de EDA)**  
**Objetivo**: Ingesta de flota SITP, rutas, estaciones troncales, paraderos zonales, GTFS y análisis exploratorio espacial (EDA).  
**Datos de Entrada**: `data/raw/MOVILIDAD/*`  
**Datos de Salida**: `data/processed/MOVILIDAD/*`"""
    )

    # 05 Infraestructura
    update_notebook_author(
        ING_DIR / "05_ingestion_infraestructura.ipynb",
        """# SIPTA — Ingesta y EDA: Infraestructura y Espacio Público (Parques IDRD)
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona A (Adan Sánchez — Lead Data Engineer & Autor de EDA)**  
**Objetivo**: Ingesta de parques distritales IDRD, equipamientos asistenciales y análisis exploratorio de espacio público (EDA).  
**Datos de Entrada**: `data/raw/INFRAESTRUCTURA_ESPACIO_PUBLICO/*`  
**Datos de Salida**: `data/processed/INFRAESTRUCTURA_ESPACIO_PUBLICO/*`"""
    )

    # 06 Finanzas
    update_notebook_author(
        ING_DIR / "06_ingestion_finanzas.ipynb",
        """# SIPTA — Ingesta y EDA: Finanzas, Economía Informal (RIVI) e Inversión
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona C (Sofía Hidalgo — Ingesta & EDA)**  
**Colaboración / Integración**: Persona A (Adan Sánchez — Lead Data Engineer)  
**Objetivo**: Consolidación de series semestrales RIVI, puntos de encuentro IPES, inversión educativa SED y análisis exploratorio (EDA).  
**Datos de Entrada**: `data/raw/FINANZAS_INVERSION_PUBLICA/*`  
**Datos de Salida**: `data/processed/FINANZAS_INVERSION_PUBLICA/*`"""
    )

    # 07 Ambiente
    update_notebook_author(
        ING_DIR / "07_ingestion_ambiental.ipynb",
        """# SIPTA — Ingesta y EDA: Ambiente, Calidad del Aire y Conflictos SAC
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona C (Sofía Hidalgo — Ingesta & EDA)**  
**Colaboración / Integración**: Persona A (Adan Sánchez — Lead Data Engineer)  
**Objetivo**: Ingesta y análisis exploratorio (EDA) de estaciones RMCAB y Situaciones Ambientales Conflictivas (SAC).  
**Datos de Entrada**: `data/raw/AMBIENTE/*`  
**Datos de Salida**: `data/processed/AMBIENTE/*`"""
    )

    # 08 Seguridad
    update_notebook_author(
        ING_DIR / "08_ingestion_seguridad.ipynb",
        """# SIPTA — Ingesta y EDA: Seguridad y Convivencia (Cuadrantes MEBOG)
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona C (Sofía Hidalgo — Ingesta & EDA)**  
**Colaboración / Integración**: Persona A (Adan Sánchez — Lead Data Engineer)  
**Objetivo**: Ingesta y análisis exploratorio (EDA) de los 599 cuadrantes policiales del MNVCC y cobertura distrital.  
**Datos de Entrada**: `data/raw/SEGURIDAD/*`  
**Datos de Salida**: `data/processed/SEGURIDAD/*`"""
    )

    print("Autoría de EDA actualizada formalmente para todo el equipo (Persona A, Persona B, Persona C).")


if __name__ == "__main__":
    update_all_ingestion_eda_authorship()

