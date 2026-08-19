"""Genera los notebooks de ingesta y EDA para los nuevos dominios expandidos:
- 09_ingestion_servicios_publicos.ipynb
- 10_ingestion_empleo_economia.ipynb
- 11_ingestion_participacion_pqr.ipynb
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = ROOT / "notebooks" / "01_ingestion"
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


def make_nb(cells):
    return {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.11"},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }


def md_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(True)}


def code_cell(source):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": source.splitlines(True)}


def build_notebooks():
    # 1. Notebook 09: Servicios Públicos y Calidad
    nb_09 = make_nb([
        md_cell("""# SIPTA — Ingesta y EDA: Servicios Públicos Domiciliarios y Calidad del Servicio
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona A (Adan Sánchez)** & **Persona B (Yesid Bello)**  
**Objetivo**: Ingesta, perfilado y análisis de cobertura de acueducto, alcantarillado, calidad del agua (IRCA), alumbrado público y conectividad TIC.  
**Datos de Entrada**: `data/raw/SERVICIOS_PUBLICOS/*`  
**Datos de Salida**: `data/processed/SERVICIOS_PUBLICOS/*`"""),
        code_cell("""import sys
from pathlib import Path
ROOT = Path('..').resolve().parent
sys.path.append(str(ROOT))

import pandas as pd
import matplotlib.pyplot as plt
from src.validation.validate_data import validate_servicios_publicos, inspect_schema

rep = validate_servicios_publicos()
print("Validación de Calidad ISO 25010:", rep['validation_status'])

df_acu = pd.read_csv(ROOT / 'data' / 'raw' / 'SERVICIOS_PUBLICOS' / 'eaab_cobertura_acueducto_localidad.csv')
display(df_acu.head(10))

schema = inspect_schema(df_acu)
display(schema)"""),
        code_cell("""fig, ax = plt.subplots(figsize=(10, 5))
df_acu.sort_values('cobertura_acueducto_pct').plot.barh(x='nombre_localidad', y=['cobertura_acueducto_pct', 'cobertura_alcantarillado_pct'], ax=ax, color=['#2E86AB', '#D1495B'])
ax.set_title("Cobertura de Acueducto y Alcantarillado por Localidad (%)", fontsize=12, fontweight='bold')
ax.set_xlabel("Porcentaje (%)")
ax.set_xlim(60, 105)
plt.tight_layout()
plt.show()""")
    ])
    (NOTEBOOKS_DIR / "09_ingestion_servicios_publicos.ipynb").write_text(json.dumps(nb_09, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2. Notebook 10: Mercado Laboral y Salarios
    nb_10 = make_nb([
        md_cell("""# SIPTA — Ingesta y EDA: Mercado Laboral, Salarios y Conmutación Residencia-Trabajo
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona B (Yesid Bello)** & **Persona A (Adan Sánchez)**  
**Objetivo**: Ingesta y análisis de la matriz de conmutación origen-destino laboral, ingresos de ocupados e informalidad.  
**Datos de Entrada**: `data/raw/EMPLEO_ECONOMIA/*`  
**Datos de Salida**: `data/processed/EMPLEO_ECONOMIA/*`"""),
        code_cell("""import sys
from pathlib import Path
ROOT = Path('..').resolve().parent
sys.path.append(str(ROOT))

import pandas as pd
import matplotlib.pyplot as plt
from src.validation.validate_data import validate_empleo_economia

rep = validate_empleo_economia()
print("Validación de Calidad ISO 25010:", rep['validation_status'])

df_emp = pd.read_csv(ROOT / 'data' / 'raw' / 'EMPLEO_ECONOMIA' / 'conmutacion_laboral_residencia_trabajo_localidad.csv')
df_sal = pd.read_csv(ROOT / 'data' / 'raw' / 'EMPLEO_ECONOMIA' / 'ingreso_promedio_salario_ocupados_localidad.csv')
display(df_emp.head(10))
display(df_sal.head(10))"""),
        code_cell("""fig, ax = plt.subplots(figsize=(10, 5))
df_sal.sort_values('ingreso_laboral_promedio_ocupados_cop').plot.barh(x='nombre_localidad', y='ingreso_laboral_promedio_ocupados_cop', ax=ax, color='#2A9D8F', legend=False)
ax.set_title("Ingreso Laboral Promedio de los Ocupados por Localidad (COP)", fontsize=12, fontweight='bold')
ax.set_xlabel("Salario Promedio Mensual ($ COP)")
plt.tight_layout()
plt.show()""")
    ])
    (NOTEBOOKS_DIR / "10_ingestion_empleo_economia.ipynb").write_text(json.dumps(nb_10, indent=2, ensure_ascii=False), encoding="utf-8")

    # 3. Notebook 11: Participación Ciudadana y PQR
    nb_11 = make_nb([
        md_cell("""# SIPTA — Ingesta y EDA: Participación Ciudadana y PQR Bogotá Te Escucha
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **Fase CRISP-DM**: Data Understanding / Data Preparation  
**Autoría**: **Persona A (Adan Sánchez)** & **Persona B (Yesid Bello)**  
**Objetivo**: Ingesta y análisis de peticiones ciudadanas PQR, tasas de resolución y presupuestos participativos.  
**Datos de Entrada**: `data/raw/PARTICIPACION_CIUDADANA/*`  
**Datos de Salida**: `data/processed/PARTICIPACION_CIUDADANA/*`"""),
        code_cell("""import sys
from pathlib import Path
ROOT = Path('..').resolve().parent
sys.path.append(str(ROOT))

import pandas as pd
import matplotlib.pyplot as plt
from src.validation.validate_data import validate_participacion_ciudadana

rep = validate_participacion_ciudadana()
print("Validación de Calidad ISO 25010:", rep['validation_status'])

df_pqr = pd.read_csv(ROOT / 'data' / 'raw' / 'PARTICIPACION_CIUDADANA' / 'pqr_bogota_te_escucha_por_localidad.csv')
display(df_pqr.head(10))"""),
        code_cell("""fig, ax = plt.subplots(figsize=(10, 5))
df_pqr.sort_values('total_pqr_recibidas').plot.barh(x='nombre_localidad', y='total_pqr_recibidas', ax=ax, color='#E76F51', legend=False)
ax.set_title("Total Solicitudes y PQR Bogotá Te Escucha por Localidad", fontsize=12, fontweight='bold')
ax.set_xlabel("Número de PQR Registradas")
plt.tight_layout()
plt.show()""")
    ])
    (NOTEBOOKS_DIR / "11_ingestion_participacion_pqr.ipynb").write_text(json.dumps(nb_11, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Notebooks 09, 10 y 11 generados exitosamente.")


if __name__ == "__main__":
    build_notebooks()
