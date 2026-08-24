# SIPTA — Sistema de Indicadores y Priorización Territorial y Alertas Tempranas

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Tests Passing](https://img.shields.io/badge/tests-193%2F193%20passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A595%25-success.svg)](tests/)
[![Standards](https://img.shields.io/badge/standards-SWEBOK%20%7C%20DAMA--BOK%20%7C%20ISO%2025010%20%7C%20OECD%20JRC-orange.svg)](docs/)
[![Statistical Audit](https://img.shields.io/badge/statistical%20audit-CERTIFIED%20%26%20APPROVED-success.svg)](reports/00_auditoria_estadistica_formal.md)
[![Architecture](https://img.shields.io/badge/architecture-Hexagonal%20%2F%20Modular-informational.svg)](docs/02-architecture/)

Plataforma integral de analítica de datos territoriales, modelado multicriterio de priorización de inversión social, visualización geoespacial interactiva y sistema de alertas tempranas para las **20 localidades de Bogotá D.C.** desarrollada en el marco del **DataJam Bogotá 2026**.

---

## 👥 Equipo de Ingeniería y Ciencia de Datos

- **Persona A — Adan Sánchez**: Scrum Master & Lead Data Engineer / Arquitectura de Pipeline, Gestión Git y Control de Calidad.
- **Persona B — Yesid Bello**: Data Scientist & Territorial Analyst / Modelado Multidimensional e Indicadores Compuestos.
- **Persona C — Sofía Hidalgo**: Tech Lead & BI Developer / Ingesta, QA, Visualización y Análisis Exploratorio de Finanzas (RIVI), Ambiente (SAC/RMCAB) y Seguridad (Cuadrantes).

---

## 🏛️ Fundamentos Normativos e Ingeniería del Software

El sistema implementa de forma exhaustiva los estándares internacionales rectores:
- **SWEBOK v3 / ISO 29148**: Gestión del ciclo de vida del software y especificación formal de requerimientos (IEEE 830).
- **DAMA-BOK**: Gobierno de datos, linaje, diccionario de datos y calidad multivariada sobre 25 datasets oficiales.
- **OECD / JRC Composite Indicators Handbook**: Metodología de 10 etapas para el diseño, ponderación, normalización, agregación no compensatoria y análisis global de sensibilidad del **Índice de Priorización Territorial (IPT)**.
- **ISO/IEC 25010**: Modelo de calidad de producto de software (completitud, exactitud, consistencia, interoperabilidad y mantenibilidad).
- **Clean Code & PEP 8**: Código tipado estáticamente (`Type Hints`), desacoplado, modular y con pruebas unitarias exhaustivas bajo patrón AAA (*Arrange-Act-Assert*).

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           ARQUITECTURA DEL PIPELINE MODULAR SIPTA                       │
├─────────────────┬──────────────────┬─────────────────┬──────────────────┬───────────────┤
│  1. ADQUISICIÓN │   2. INGESTA Y   │  3. INTEGRACIÓN │  4. MODELADO E   │ 5. AUDITORÍA  │
│   Y DESCARGA    │    VALIDACIÓN    │   TERRITORIAL   │   IPT COMPUESTO  │  ESTADÍSTICA  │
├─────────────────┼──────────────────┼─────────────────┼──────────────────┼───────────────┤
│ 25 Datasets     │ ISO 25010 Checks │ Homologación a  │ Normalización    │ VIF < 10.0    │
│ IDECA / EAAB    │ 13 Dominios      │ 20 Localidades  │ 7 Dimensiones    │ Moran's I     │
│ SDIS / DANE     │ Ingestion        │ Spatial Joins   │ 5 Escenarios     │ Bootstrap 95% │
│ MEBOG / SED     │ Manifest JSON    │ Master Table    │ Consenso Ranking │ OCDE Aprobado │
└─────────────────┴──────────────────┴─────────────────┴──────────────────┴───────────────┘
```

---

## 🗺️ Visualización Geoespacial y Dashboard Web GIS

SIPTA integra un subsistema de visualización interactiva y autónoma que no requiere servidores externos ni software GIS comercial:

- **Dashboard Web GIS Interactivo**: [`reports/dashboard_geografico_sipta.html`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/dashboard_geografico_sipta.html) (aplicación web completa basada en Leaflet.js, Chart.js, Tailwind CSS y Lucide Icons).
- **Exploración de 13 Dominios y más de 30 Indicadores**: Selector dinámico con cambio de clasificaciones cartográficas no arbitrarias (**Fisher-Jenks Natural Breaks** y **Cuantiles**).
- **Rigor Estadístico Integrado en Tooltips**: Despliegue en tiempo real de intervalos de confianza Bootstrap al 95% ($\text{IC}_{95\%}$), semáforos de riesgo y gráficos comparativos de radar.
- **Capa Espacial Curada (RFC 7946)**: [`data/curated/sipta_localidades_multidominio.geojson`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/data/curated/sipta_localidades_multidominio.geojson) lista para consumir en QGIS, ArcGIS o Mapbox.
- **Documentación Técnica del Subsistema**: [`docs/03-development/sistema_visualizacion.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/docs/03-development/sistema_visualizacion.md).

---

## 📐 Formulación Matemática del Índice de Priorización Territorial (IPT v1.0.0)

El **Índice de Priorización Territorial (IPT)** sintetiza las brechas estructurales de las 20 localidades en una escala normalizada $[0, 100]$, donde un mayor puntaje refleja mayor privación y urgencia de asignación presupuestal:

### 1. Sub-Índices Dimensionales ($s_{i, d} \in [0, 1]$)
$$\hat{x}_{i, d} = \frac{x_{i, d} - \min(X_d)}{\max(X_d) - \min(X_d)}$$
- **Capacidades e Infraestructura (Polaridad Inversa)**: $s_{i, d} = 1 - \hat{x}_{i, d}$ (Educación, Salud, Movilidad, Infraestructura, Seguridad).
- **Riesgo y Vulnerabilidad (Polaridad Directa)**: $s_{i, d} = \hat{x}_{i, d}$ (Ambiente SAC, Vulnerabilidad RIVI).

### 2. Agregación Lineal y Agregación Geométrica No Compensatoria
- **IPT Base Lineal**:
  $$\text{IPT}_{\text{Base}, i} = \left( \sum_{d=1}^7 w_d \cdot s_{i, d} \right) \times 100, \quad w_d = \frac{1}{7}$$
- **IPT Geométrico (Penalización de Desbalances Críticos)**:
  $$\text{IPT}_{\text{Geom}, i} = 100 \times \left( \prod_{d=1}^7 (s_{i, d} + 0.01)^{w_d} \right) - 1.0$$

### 3. Diagnóstico de Incertidumbre y Sensibilidad
- **Factor de Inflación de la Varianza**: $\text{VIF}_j = \frac{1}{1 - R_j^2} < 10.0 \quad \forall j$ (Promedio distrital: $3.21$).
- **Autocorrelación Espacial Global**: Índice de Moran $I = 0.412$ ($p = 0.008$), corroborando el conglomerado contiguo de vulnerabilidad en el sur.
- **Intervalos de Confianza Bootstrap al 95%**: Remuestreo Dirichlet ($B = 1.000$ réplicas) con estabilidad demostrada en el Top 5 (**Usme, Ciudad Bolívar, San Cristóbal, Rafael Uribe Uribe, Bosa**).

---

## 🤖 Gobernanza de Modelos y Artefactos (`models/`)

El directorio [`models/`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/models/) constituye el núcleo de reproducibilidad, trazabilidad y gobernanza formal del sistema conforme a **DAMA-BOK** y los lineamientos de la **OCDE / JRC**:

- **Ficha Técnica Formal del Modelo ([`models/model_card.json`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/models/model_card.json))**: Especifica el alcance territorial (20 localidades oficiales DIVIPOLA), escala de medición $[0, 100]$, las 7 dimensiones canónicas y los resultados certificados de auditoría cuantitativa (VIF $= 3.21 < 10.0$, Moran's $I = 0.412$, incertidumbre Bootstrap $\text{IC}_{95\%}$ y correlación no compensatoria de Spearman $\rho = 0.962$).
- **Configuración de Ponderaciones y Sensibilidad ([`models/ipt_config_weights.json`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/models/ipt_config_weights.json))**: Define de manera determinista los pesos de las 7 dimensiones y los 5 escenarios metodológicos de sensibilidad (Escenario Base $w_d = 1/7$, Rangos/Percentiles, Sin Parques, Sin RIVI, Sin Proxies y Agregación Geométrica No Compensatoria).
- **Transformadores y Polaridades ([`models/transformers/minmax_scalers_config.json`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/models/transformers/minmax_scalers_config.json))**: Documenta los parámetros de normalización Min-Max $[0, 1]$, fórmulas de asignación y la polaridad analítica (directa vs. inversa) por variable.
- **Guía de Gobernanza ([`models/README.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/models/README.md))**: Documentación técnica para auditores, desarrolladores e instituciones distritales.

---

## 📊 Los 13 Dominios Analíticos Integrados y sus Reportes

| # | Dominio Sectorial | Informe Analítico Formal | Indicador Clave | Visualización 300 DPI |
|---|---|---|---|---|
| **00** | **Priorización Territorial (IPT)** | [`reports/domains/00_reporte_ejecutivo_priorizacion_ipt.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/00_reporte_ejecutivo_priorizacion_ipt.md) | `IPT_Base`, `IPT_Rangos`, `Consenso` | `fig_00_priorizacion_ipt_consenso.png` |
| **01** | **Demografía y Dinámica Espacial** | [`reports/domains/01_reporte_demografia.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/01_reporte_demografia.md) | `DEM-001` (Densidad hab/km²) | `fig_01_demografia_densidad.png` |
| **02** | **Salud y Capacidad Asistencial** | [`reports/domains/02_reporte_salud.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/02_reporte_salud.md) | `SAL-001` (Sedes IPS / 10k hab) | `fig_02_salud_camas_ips.png` |
| **03** | **Educación y Logro Académico** | [`reports/domains/03_reporte_educacion.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/03_reporte_educacion.md) | `EDU-001` (Cupos / 1k pob escolar) | `fig_03_educacion_saber11_cupos.png` |
| **04** | **Movilidad y Accesibilidad** | [`reports/domains/04_reporte_movilidad.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/04_reporte_movilidad.md) | `MOV-001` (Estaciones + Paraderos/km²) | `fig_04_movilidad_estaciones_paraderos.png` |
| **05** | **Infraestructura y Parques** | [`reports/domains/05_reporte_infraestructura.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/05_reporte_infraestructura.md) | `INF-001` (Parques IDRD / 10k hab) | `fig_05_infraestructura_parques_idrd.png` |
| **06** | **Ambiente y Sostenibilidad** | [`reports/domains/06_reporte_ambiente.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/06_reporte_ambiente.md) | `AMB-001` (Conflictos SAC / km²) | `fig_06_ambiente_conflictos_sac.png` |
| **07** | **Finanzas e Inversión FDL** | [`reports/domains/07_reporte_finanzas.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/07_reporte_finanzas.md) | `FIN-001` (Presupuesto FDL / cápita) | `fig_07_finanzas_inversion_fdl_ejecucion.png` |
| **08** | **Vulnerabilidad Social y RIVI** | [`reports/domains/08_reporte_vulnerabilidad_social.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/08_reporte_vulnerabilidad_social.md) | `VUL-001` (Vendedores RIVI / 10k) | `fig_08_vulnerabilidad_rivi_sdis.png` |
| **09** | **Seguridad y Convivencia** | [`reports/domains/09_reporte_seguridad.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/09_reporte_seguridad.md) | `SEG-001` (Cuadrantes MEBOG / 10k) | `fig_09_seguridad_homicidios_cuadrantes.png` |
| **10** | **Servicios Públicos Domiciliarios** | [`reports/domains/10_reporte_servicios_publicos.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/10_reporte_servicios_publicos.md) | `PUB-001` (Índice Riesgo Agua IRCA) | `fig_09_servicios_publicos_irca_acueducto.png` |
| **11** | **Mercado Laboral y Conmutación** | [`reports/domains/11_reporte_empleo_economia.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/11_reporte_empleo_economia.md) | `EMP-001` (Tasa Conmutación Laboral) | `fig_11_empleo_conmutacion_salarios.png` |
| **12** | **Participación Ciudadana y PQR** | [`reports/domains/12_reporte_participacion_ciudadana.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains/12_reporte_participacion_ciudadana.md) | `PAR-001` (Peticiones SDQS / 10k) | `fig_12_participacion_pqr_oportunidad.png` |

---

## 🗂️ Estructura y Navegación del Repositorio

```
DataJam_DataOlinguitos_Gen/
├── data/
│   ├── raw/                 ← Datasets originales inmutables (25 fuentes oficiales)
│   ├── processed/           ← Tablas procesadas y tablón maestro territorial
│   └── curated/             ← 12 Tablas maestras curadas por dominio, IPT y GeoJSON oficial
├── models/                  ← Gobernanza de modelos, ponderaciones deterministas y transformadores
│   ├── model_card.json      ← Ficha técnica formal del modelo IPT (v1.0.0)
│   ├── ipt_config_weights.json ← Ponderaciones dimensionales y 5 escenarios de sensibilidad
│   ├── README.md            ← Guía de gobernanza del modelo
│   └── transformers/        ← Parámetros Min-Max y polaridades por indicador
├── notebooks/
│   ├── 01_ingestion/        ← 12 Notebooks de Ingesta y EDA por sector (00 al 11)
│   ├── 02_validation/       ← 9 Notebooks de validación de calidad ISO 25010
│   ├── 03_integration/      ← Integración y tabla maestra territorial
│   ├── 04_modeling/         ← Modelado formal IPT, Diccionario y Métricas de Rigor
│   └── 05_visualization/   ← Tableros analíticos y visualizaciones interactivas
├── src/
│   ├── ingestion/           ← Ingestión automatizada y extracción de GeoJSON
│   ├── validation/          ← Validadores de reglas de negocio por dominio
│   ├── cleaning/            ← Homologación territorial y tipado de datos
│   ├── integration/         ← Merge territorial y cruces espaciales
│   ├── modeling/            ← Motor del IPT, Bootstrap, VIF, Moran y Marshall
│   └── visualization/       ← Web GIS Dashboard (Leaflet.js/Chart.js), Fisher-Jenks y GeoJSON
├── tests/                   ← 193 Pruebas unitarias automatizadas (pytest)
├── docs/                    ← Gestión Documental Transversal (PDCO / SDLC)
│   ├── 01-requirements/     ← IEEE 830, E01, E02, Casos de uso y Fichas técnicas
│   ├── 02-architecture/     ← Arquitectura Hexagonal, Patrones GoF/GRASP y ADRs
│   ├── 03-development/      ← Dev-log, APIs, Guía de visualización, Formulación IPT
│   ├── 04-testing/          ← Plan de pruebas IEEE 829 y Resultados formales
│   └── 05-maintenance/      ← Changelog SemVer (v1.0.0) y Registro de Refactorizaciones
├── reports/                 ← Informes de dominio, figuras 300 DPI y Dashboard Web GIS
│   ├── dashboard_geografico_sipta.html ← Aplicación Web GIS interactiva autónoma
│   ├── 00_auditoria_estadistica_formal.md ← Certificación y Dictamen OCDE/JRC
│   ├── domains/             ← 13 Informes analíticos sectoriales con recomendaciones
│   └── figures/             ← 13 Figuras científicas multi-panel a 300 DPI
└── metadata.json            ← Metadatos de gobernanza DAMA-BOK y trazabilidad (v1.0.0)
```

---

## ⚙️ Instalación y Verificación

```bash
# 1. Clonar el repositorio
git clone https://github.com/adansanchezc1-spec/DataJam_DataOlinguitos_Gen.git
cd DataJam_DataOlinguitos_Gen

# 2. Crear entorno virtual y activar
python -m venv .venv
.\.venv\Scripts\activate      # Windows
source .venv/bin/activate    # Linux / macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la suite completa de 193 pruebas automatizadas
pytest -v

# 5. Generar y compilar el Dashboard Web GIS y la capa GeoJSON curada
python -c "from src.visualization.geo_dashboard import generate_interactive_gis_dashboard; generate_interactive_gis_dashboard()"
```

