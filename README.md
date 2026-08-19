# SIPTA — Sistema de Indicadores y Priorización Territorial y Alertas Tempranas

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Tests Passing](https://img.shields.io/badge/tests-73%2F73%20passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A592%25-success.svg)](reports/validation/)
[![Standards](https://img.shields.io/badge/standards-SWEBOK%20%7C%20DAMA--BOK%20%7C%20ISO%2025010-orange.svg)](docs/)
[![Architecture](https://img.shields.io/badge/architecture-Hexagonal%20%2F%20Modular-informational.svg)](docs/02-architecture/)

Plataforma de analítica de datos, priorización territorial multicriterio y monitoreo de alertas tempranas para las **20 localidades de Bogotá D.C.** desarrollada en el marco del **DataJam Bogotá 2026**.

---

## 👥 Equipo de Desarrollo y Roles

- **Persona A — Adan Sánchez**: Scrum Master & Lead Data Engineer / Arquitectura de Pipeline, Gestión Git y Validaciones.
- **Persona B — Yesid Bello**: Data Scientist & Territorial Analyst / Modelado Multidimensional e Indicadores Compuestos.
- **Persona C — Sofía Hidalgo**: Tech Lead & BI Developer / Ingesta, QA y Análisis Exploratorio de Finanzas (RIVI), Ambiente (SAC/RMCAB) y Seguridad (Cuadrantes).

---

## 🏛️ Marco Normativo y Arquitectura

El proyecto se rige por los más altos estándares internacionales de ingeniería de software y gestión de datos:
- **SWEBOK v3 / ISO 29148**: Gestión del ciclo de vida del software y especificación formal de requerimientos.
- **DAMA-BOK**: Gobierno, calidad multivariada y metadatos sobre 25 datasets oficiales.
- **ISO/IEC 25010**: Modelo de calidad de software (completitud, exactitud, consistencia y eficiencia).
- **Clean Code & PEP 8**: Tipado estático con `Type Hints`, funciones puras y alta cohesión.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ARQUITECTURA DEL PIPELINE SIPTA                     │
├─────────────────┬──────────────────┬─────────────────┬──────────────────────┤
│  1. ADQUISICIÓN │   2. INGESTA Y   │  3. INTEGRACIÓN │    4. MODELADO E     │
│   Y DESCARGA    │    VALIDACIÓN    │   TERRITORIAL   │   IPT COMPUESTO      │
├─────────────────┼──────────────────┼─────────────────┼──────────────────────┤
│ 25 Datasets     │ ISO 25010 Checks │ Homologación a  │ Normalización Min-Max│
│ IDECA / EAAB    │ 13 Dominios      │ 20 Localidades  │ 7 Dimensiones        │
│ SDIS / DANE     │ Ingestion        │ Spatial Joins   │ Ranking Territorial  │
│ MEBOG / SED     │ Manifest JSON    │ Master Table    │ Alertas Tempranas    │
└─────────────────┴──────────────────┴─────────────────┴──────────────────────┘
```

---

## 📊 Los 13 Dominios Analíticos Integrados

1. **Demografía y Población (D1)**: Proyecciones poblacionales por localidad y UPL (SDP / SDS SaluData 2005–2035).
2. **Salud y Capacidad Asistencial (D2)**: IPS de urgencias, dotación de camas hospitalarias y camas UCI (SDS / REPS).
3. **Educación y Cobertura (D3)**: Sedes escolares, oferta de cupos, calidad Saber 11 y retención escolar (SED / ICFES).
4. **Movilidad y Transporte (D4)**: Flota SITP vinculada, paraderos zonales, estaciones troncales y viajes (TransMilenio / SDM).
5. **Infraestructura y Espacio Público (D5)**: Inventario de 5.120 parques IDRD y espacio verde per cápita.
6. **Ambiente y Sostenibilidad (D6)**: Situaciones Ambientales Conflictivas (SAC) y estaciones de calidad del aire RMCAB (SDA).
7. **Finanzas y Economía Informal (D7a)**: Series censales RIVI de vendedores informales y puntos de encuentro (IPES).
8. **Inversión FDL y Gasto Social (D7b)**: Presupuesto y ejecución de los 20 Fondos de Desarrollo Local y metas SDIS (Sec. Gobierno).
9. **Seguridad y Convivencia (D8)**: Cuadrantes policiales MEBOG y cifras de delitos de alto impacto (SDSCJ - SIEDCO).
10. **Participación y Alertas Tempranas (D9)**: Requerimientos ciudadanos PQR Bogotá Te Escucha y Presupuestos Participativos.
11. **Modelo Territorial Oficial (D10)**: Capa cartográfica oficial de las 20 localidades en GeoJSON WGS84 (IDECA).
12. **Servicios Públicos Domiciliarios (D11)**: Cobertura acueducto EAAB, calidad del agua (IRCA), alumbrado LED y conectividad TIC.
13. **Mercado Laboral y Salarios (D12)**: Conmutación residencia-trabajo, tiempos de viaje, salarios promedio e informalidad (DANE).

---

## 🚀 Estructura del Repositorio

```
DataJam_DataOlinguitos_Gen/
├── data/
│   ├── raw/                 ← Datasets originales inmutables (25 fuentes)
│   └── processed/           ← Tablas procesadas y normalizadas
├── notebooks/
│   ├── 01_ingestion/        ← 12 Notebooks de Ingesta y EDA por sector (00 al 11)
│   ├── 02_validation/       ← 9 Notebooks de validación de calidad ISO 25010
│   ├── 03_integration/      ← Integración y tabla maestra territorial
│   ├── 04_modeling/         ← Modelado y cálculo del IPT Multidimensional
│   └── 05_visualization/   ← Visualizaciones y tableros interactivos
├── src/
│   ├── ingestion/           ← Descarga y extracción automatizada
│   ├── validation/          ← Validadores de calidad por dominio
│   ├── cleaning/            ← Homologación territorial y tipado
│   ├── integration/         ← Merge territorial y agregaciones
│   ├── modeling/            ← Motor del Índice de Prioridad Territorial (IPT)
│   └── visualization/       ← Preparación de datos para dashboards
├── tests/                   ← 73 Pruebas unitarias automatizadas (pytest)
├── docs/                    ← Documentación técnica formal (PDCO / SDLC)
│   ├── 01-requirements/     ← E01, E02, requerimientos y casos de uso
│   ├── 02-architecture/     ← Arquitectura, patrones GoF/GRASP y diagramas UML
│   ├── 03-development/      ← Dev-log, APIs, EDA y deuda técnica
│   ├── 04-testing/          ← Plan y reporte de resultados de pruebas
│   └── 05-maintenance/      ← Changelog y registro de refactorizaciones
├── reports/                 ← Reportes analíticos, de validación y perfiles EDA
└── metadata.json            ← Metadatos de gobernanza y trazabilidad del proyecto
```

---

## ⚙️ Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/adansanchezc1-spec/DataJam_DataOlinguitos_Gen.git
cd DataJam_DataOlinguitos_Gen

# 2. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scriptsctivate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la suite completa de pruebas unitarias
pytest -v

# 5. Ejecutar la suite de validación y cálculo del IPT
python -m src.validation.validate_data
python -m src.modeling.calculate_indicators
```
