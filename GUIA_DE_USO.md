# 📖 Guía de Uso Rápido y Manual del Usuario — SIPTA

Bienvenido a la **Guía de Uso Oficial** del **Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA)** de Bogotá D.C., desarrollado en el marco del **DataJam Bogotá 2026**.

Esta guía proporciona instrucciones paso a paso para **instalar, ejecutar, explorar el Dashboard Web GIS, reproducir los análisis en notebooks y correr la suite de pruebas**.

---

## 🧭 Índice de Contenidos
1. [Requisitos Previos e Instalación](#1-requisitos-previos-e-instalación)
2. [Estructura del Proyecto y Dónde Encontrar Cada Recurso](#2-estructura-del-proyecto)
3. [Cómo Abrir y Utilizar el Dashboard Web GIS](#3-cómo-abrir-y-utilizar-el-dashboard-web-gis)
4. [Cómo Interpretar el Semáforo y los 4 Cuadrantes de Inversión](#4-cómo-interpretar-el-semáforo-y-los-cuadrantes)
5. [Cómo Ejecutar los Cuadernos Interactivos (Notebooks)](#5-cómo-ejecutar-los-cuadernos-interactivos-notebooks)
6. [Cómo Regenerar los 13 Reportes Sectoriales y Mapas 300 DPI](#6-cómo-regenerar-los-reportes-sectoriales)
7. [Cómo Ejecutar la Suite de Pruebas Automatizadas](#7-cómo-ejecutar-la-suite-de-pruebas-automatizadas)
8. [Formulación del Índice de Priorización Territorial (IPT)](#8-formulación-del-índice-ipt)

---

## 1. Requisitos Previos e Instalación

### Requisitos del Sistema
- **Python**: Versión 3.9 o superior (recomendado Python 3.11+).
- **Navegador Web Moderno**: Chrome, Firefox, Edge o Safari (para el Dashboard Web GIS).
- **Git** instalado.

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/adansanchezc1-spec/DataJam_DataOlinguitos_Gen.git
cd DataJam_DataOlinguitos_Gen
```

### Paso 2: Crear y Activar el Entorno Virtual
En Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Linux / macOS (Bash):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias del Paquete Canónico
Instala el paquete en modo editable con soporte para desarrollo y pruebas:
```bash
pip install -e .
```
O utilizando el archivo de requerimientos:
```bash
pip install -r requirements.txt
```

---

## 2. Estructura del Proyecto

El repositorio está organizado conforme al estándar canónico **SWEBOK** y la arquitectura **Hexagonal**:

```
DataJam_DataOlinguitos_Gen/
├── config/              # Parámetros declarativos y pesos dimensionales del IPT
├── data/
│   ├── raw/             # Microdatos y anexos originales (DANE 2025, PUA SDIS 2024, etc.)
│   ├── processed/       # Datos normalizados, tablas sectoriales e ingestion manifest
│   ├── curated/         # Tablones analíticos maestros y capa espacial GeoJSON
│   └── status/          # Catálogos de fuentes aprobadas (source_catalog.csv)
├── docs/                # Documentación formal PDCO (Requerimientos, Arquitectura ADRs, etc.)
├── models/              # Gobernanza de modelos, Model Card y transformadores Min-Max
├── notebooks/           # 26 Cuadernos Jupyter reproducibles (Ingesta, Validación, Modelado, Viz)
├── reports/
│   ├── dashboard_geografico_sipta.html # 🌟 Dashboard Web GIS interactivo autónomo
│   ├── domains/         # 13 Informes analíticos sectoriales en Markdown
│   └── figures/         # 13 Figuras cartográficas y estadísticas en alta resolución (300 DPI)
├── scripts/
│   └── generate_domain_reports.py      # Generador automatizado de reportes y figuras
├── src/                 # Código fuente empaquetado (ingestion, validation, cleaning, modeling, etc.)
├── tests/               # 194 pruebas unitarias y de integración end-to-end
├── GUIA_DE_USO.md       # 📖 Este manual de usuario
├── README.md            # Documento principal del repositorio
└── pyproject.toml       # Especificación de empaquetado y configuración de pytest
```

---

## 3. Cómo Abrir y Utilizar el Dashboard Web GIS

El **Dashboard Web GIS** es una aplicación cliente interactiva, 100% autónoma (no requiere bases de datos activas ni servidores Node/Python para su visualización).

### ¿Cómo abrirlo?
1. Navega hasta el archivo [`reports/dashboard_geografico_sipta.html`](reports/dashboard_geografico_sipta.html).
2. Haz doble clic sobre él para abrirlo en cualquier navegador web moderno, o ejecútalo localmente:
   ```bash
   # En Windows:
   start reports/dashboard_geografico_sipta.html
   # En Linux:
   xdg-open reports/dashboard_geografico_sipta.html
   # En macOS:
   open reports/dashboard_geografico_sipta.html
   ```

### Funcionalidades Principales del Dashboard:
- **Mapa Coroplético Interactivo (Leaflet)**: Muestra las 20 localidades de Bogotá con polígonos coloreados según el nivel de privación o capacidad.
- **Selector de 13 Dominios y más de 35 Indicadores**: Permite alternar entre el IPT Multidimensional, Demografía, Salud, Educación, Movilidad, Infraestructura, Finanzas, Vulnerabilidad Social PUA SDIS, Seguridad, Servicios Públicos, etc.
- **Métodos de Clasificación Cartográfica**: Alterna entre **Fisher-Jenks (Cortes Naturales)** y **Cuantiles** para análisis no sesgados.
- **Gráfica de Radar y Análisis Bivariado**: Haz clic en cualquier localidad para ver su perfil multidimensional de 7 ejes y su comparación contra la media distrital.
- **Modal de Cruce Macro: IPT vs. Inversión**: Haz clic en el botón superior *"📊 Matriz de Inversión y Semáforo"* para abrir el cruce estratégico de toma de decisiones.

---

## 4. Cómo Interpretar el Semáforo y los Cuadrantes

El sistema clasifica las 20 localidades mediante un **Semáforo Institucional de 4 Niveles** y una **Matriz Estratégica de 4 Cuadrantes**:

### 🚦 Semáforo de Alertas Tempranas Territorial

| Nivel Semáforo | Rango IPT / Score | Significado Territorial | Acción Recomendada de Política Pública |
| :---: | :---: | :--- | :--- |
| 🔴 **Rojo (Crítica)** | $IPT \ge 60$ o $s \ge 0.75$ | **Déficit agudo y vulnerabilidad severa**. Concentración de carencias en salud, espacio público y transferencias. | **Intervención prioritaria inmediata**: Reasignación presupuestal FDL / SDIS y refuerzo de infraestructura. |
| 🟠 **Naranja (Alta)** | $45 \le IPT < 60$ o $0.50 \le s < 0.75$ | **Carencia sectorial significativa**. Brechas estructurales focalizadas en dimensiones clave. | **Focalización presupuestal y monitoreo**: Proyectos de inversión específica y seguimiento trimestral. |
| 🟡 **Amarillo (Media)** | $30 \le IPT < 45$ o $0.25 \le s < 0.50$ | **Cobertura media**. Oferta de servicios adecuada con oportunidades de optimización operativa. | **Mantenimiento preventivo**: Conservación de dotaciones existentes y mejora de eficiencia. |
| 🟢 **Verde (Baja)** | $IPT < 30$ o $s < 0.25$ | **Alta disponibilidad relativa**. Mayor oferta institucional y baja privación multidimensional. | **Sostenibilidad y buenas prácticas**: Transferencia metodológica y preservación de niveles de servicio. |

### 🔲 Los 4 Cuadrantes Estratégicos (IPT vs. Inversión per Cápita)

1. 🔵 **Cuadrante I: Prioridad Atendida** (Alto IPT $\ge 60$, Alta Inversión): Localidades con alta vulnerabilidad que reciben respaldo presupuestal significativo (Ej. *Usme, Ciudad Bolívar*).
2. 🔴 **Cuadrante II: Brecha Crítica** (Alto IPT $\ge 60$, Baja Inversión): Localidades con alta privación pero baja inversión per cápita. **Foco urgente de intervención** (Ej. *Rafael Uribe Uribe, Bosa, Suba, Kennedy*).
3. 🟢 **Cuadrante III: Autosuficiencia** (Bajo IPT $< 60$, Baja Inversión): Territorios consolidados con baja carencia relativa (Ej. *Barrios Unidos, Puente Aranda*).
4. 🟠 **Cuadrante IV: Eficiencia a Revisar** (Bajo IPT $< 60$, Alta Inversión): Localidades centrales con baja carencia pero alta inversión per cápita debido a baja base poblacional (Ej. *La Candelaria, Santa Fe, Teusaquillo*).

---

## 5. Cómo Ejecutar los Cuadernos Interactivos (Notebooks)

El repositorio incluye **26 cuadernos Jupyter organizados por fases**:

```bash
notebooks/
├── 01_ingestion/     # Ingesta y EDA exploratorio de los 12 sectores (00 a 11)
├── 02_validation/    # Validación de esquemas, calidad DAMA-BOK y reglas territoriales
├── 03_integration/   # Construcción de la tabla maestra master_localidades.csv
├── 04_modeling/      # Cálculo del IPT, 5 escenarios de sensibilidad y ranking de consenso
└── 05_visualization/ # Generación del dashboard Web GIS y exportación GeoJSON
```

### Ejecutar Jupyter Lab / Notebook:
```bash
jupyter lab
```
O ejecutar cualquier notebook de forma no interactiva:
```bash
jupyter nbconvert --to notebook --execute notebooks/04_modeling/01_modeling_ipt.ipynb
```

---

## 6. Cómo Regenerar los Reportes Sectoriales y Figuras 300 DPI

Para compilar automáticamente los **13 informes Markdown** en [`reports/domains/`](reports/domains/) y generar las **13 figuras cartográficas multi-panel en alta resolución (300 DPI)** en [`reports/figures/`](reports/figures/):

```bash
python scripts/generate_domain_reports.py
```

El script procesará los datos maestros de `data/curated/` y generará automáticamente:
- Mapas coropléticos oficiales de Bogotá D.C.
- Rankings con intervalos de confianza $\text{IC}_{95\%}$ Bootstrap.
- Estadísticas descriptivas completas bajo estándar **DAMA-BOK**.

---

## 7. Cómo Ejecutar la Suite de Pruebas Automatizadas

El proyecto cuenta con **194 pruebas automatizadas** que garantizan la integridad de los datos, el cálculo de los índices, la sintaxis y ejecución de notebooks, y la consistencia espacial.

### Ejecutar todas las pruebas con reporte resumido:
```bash
pytest
```

### Ejecutar pruebas con reporte de cobertura de código:
```bash
pytest --cov=src --cov-report=term-missing
```

### Ejecutar módulos específicos de pruebas:
```bash
# Probar solo validación de datos:
pytest tests/test_validation.py

# Probar rigor estadístico (VIF, Moran's I, Bootstrap, Agregación Geométrica):
pytest tests/test_statistical_rigor.py

# Probar pipeline de modelado y visualización:
pytest tests/test_pipeline_modeling_viz.py

# Probar ejecución de notebooks:
pytest tests/test_notebooks.py
```

---

## 8. Formulación del Índice de Priorización Territorial (IPT)

El **Índice de Priorización Territorial (IPT)** se calcula siguiendo la metodología de 10 pasos de la **OCDE / JRC**:

1. **Normalización Min-Max**: Escalamiento de indicadores a $[0, 1]$.
2. **Inversión de Polaridad**: Las capacidades e infraestructura se invierten ($s = 1 - \hat{x}$) para que $1.0$ siempre represente máxima privación.
3. **Agregación Multidimensional**:
   $$\text{IPT}_{\text{Base}, i} = \left( \frac{1}{7} \sum_{d=1}^7 s_{i, d} \right) \times 100$$
4. **Agregación Geométrica No Compensatoria** ($\rho = 0.962$):
   $$\text{IPT}_{\text{Geom}, i} = 100 \times \left( \prod_{d=1}^7 (s_{i, d} + 0.01)^{1/7} \right) - 1.0$$
5. **Evaluación de Incertidumbre**: $B = 1.000$ réplicas Bootstrap Dirichlet para determinar los límites inferior y superior al 95% de confianza ($\text{IC}_{\text{inf}}^{95\%}$, $\text{IC}_{\text{sup}}^{95\%}$).

---

## 📞 Soporte y Contacto

Para inquietudes metodológicas, técnicas o de reproducibilidad, consulte:
- [Documentación Técnica de Arquitectura](docs/02-architecture/architecture.md)
- [Catálogo de Decisiones de Arquitectura (ADRs)](docs/02-architecture/ADR/)
- [Manual de Cálculo de Indicadores Territoriales](docs/03-development/manual_calculo_indices_territoriales.md)
