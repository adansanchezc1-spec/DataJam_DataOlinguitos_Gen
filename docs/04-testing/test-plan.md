# Plan Maestro de Pruebas Unitarias, Integración y Validación de Notebooks — SIPTA

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA Bogota)  
**Versión**: 2.2.0  
**Fecha de Actualización**: 2026-08-19  
**Fase PDCO**: CONTROL | **SDLC Stage**: Testing  
**Estándares Normativos**: SWEBOK Cap. 5 (Software Testing), IEEE 829 / ISO 29119, ISO/IEC 25010 (Calidad del Producto de Software)  
**Framework de Pruebas**: `pytest` 8.0+ | **Patrón de Diseño de Pruebas**: AAA (Arrange-Act-Assert)

---

## 1. Objetivos del Plan de Pruebas

El presente plan establece la estrategia de verificación y validación (V&V) integral del sistema SIPTA, garantizando:
1. **Calidad y robustez lógica en `src/`**: Cobertura exhaustiva de las operaciones de ingesta, perfilado EDA, limpieza/homologación territorial, integración, cálculo de indicadores (IPT), evaluación de calidad y visualizaciones cartográficas.
2. **Ejecución y reproducibilidad de Notebooks (`notebooks/`)**: Verificación automatizada de esquema JSON (nbformat v4), análisis sintáctico de código (AST) y ejecución end-to-end sin excepciones de todos los 25 cuadernos de análisis y modelado.
3. **Trazabilidad de Requerimientos (RF-001 a RF-010)**: Correspondencia unívoca entre cada requerimiento funcional definido en `docs/01-requirements/requirements.md` y sus suites de pruebas asociadas.
4. **Cumplimiento ISO/IEC 25010**: Validación de adecuación funcional, confiabilidad, mantenibilidad y eficiencia de desempeño.

---

## 2. Alcance y Estrategia de Prueba

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                        ARQUITECTURA DE PRUEBAS SIPTA                              │
├──────────────────────────────────────┬────────────────────────────────────────────┤
│           NIVEL 1: UNIT & LOGIC      │        NIVEL 2: INTEGRATION & EXPANSION    │
├──────────────────────────────────────┼────────────────────────────────────────────┤
│ • test_cleaning.py                   │ • test_integration.py                     │
│ • test_features.py                   │ • test_expansion_datasets.py              │
│ • test_evaluation.py                 │ • test_pipeline_modeling_viz.py           │
│ • test_eda_viz.py                    │ • test_validation.py                      │
│ • test_visualization.py              │ • test_ingest.py                          │
│ • test_geospatial_cleaning.py        │ • test_education_geojson.py               │
│ • test_eda_spatial.py                │ • test_eda_readers_quality.py             │
│ • test_eda_profiling.py              │ • test_eda_explore_indicators.py          │
├──────────────────────────────────────┴────────────────────────────────────────────┤
│           NIVEL 3: AUTOMATED NOTEBOOK TEST RUNNER (25 NOTEBOOKS)                  │
├───────────────────────────────────────────────────────────────────────────────────┤
│ • TestNotebooksDiscovery: Existencia y presencia de los 25 notebooks               │
│ • TestNotebooksStructureAndSchema: Validación JSON nbformat v4                     │
│ • TestNotebooksSyntax: Compilación AST de todas las celdas de código              │
│ • TestNotebooksExecution: Ejecución secuencial end-to-end con namespace aislado   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Matriz de Trazabilidad: Requerimientos vs. Suites de Pruebas

| Requerimiento Funcional | Descripción del Requerimiento | Módulos `src/` | Suites de Pruebas `pytest` | Notebooks Asociados |
|-------------------------|-------------------------------|----------------|----------------------------|---------------------|
| **RF-001** | Ingesta polimórfica y catalogación de fuentes (CSV, GeoJSON, GPKG, XLSX) | `src/ingest.py`, `src/eda/readers.py` | `test_ingest.py`, `test_eda_readers_quality.py`, `test_expansion_datasets.py` | `01_ingestion/*.ipynb` (00 al 11) |
| **RF-002** | Perfilado estadístico multivariado y diagnóstico de calidad de datos | `src/eda/profiling.py`, `src/eda/quality.py`, `src/evaluation.py` | `test_evaluation.py`, `test_eda_profiling.py`, `test_eda_readers_quality.py` | `00_ingestion_eda_master.ipynb`, `00_validation_master.ipynb` |
| **RF-003** | Análisis geoespacial y cruces espaciales (Point-in-Polygon) | `src/eda/spatial.py`, `src/geospatial_cleaning.py` | `test_eda_spatial.py`, `test_geospatial_cleaning.py`, `test_education_geojson.py` | `04_ingestion_movilidad.ipynb`, `05_ingestion_infraestructura.ipynb` |
| **RF-004** | Limpieza, homologación canónica y codificación DIVIPOLA (20 Localidades) | `src/cleaning.py`, `src/validation/validate_data.py` | `test_cleaning.py`, `test_validation.py`, `test_geospatial_cleaning.py` | `02_validation/*.ipynb` (00 al 08) |
| **RF-005** | Validación de reglas de calidad, unicidad, integridad y consistencia temporal | `src/validation/validate_data.py`, `src/evaluation.py` | `test_validation.py`, `test_evaluation.py` | `00_validation.ipynb`, `00_validation_master.ipynb` |
| **RF-006** | Ingeniería de características, ratios per cápita y densidades | `src/features.py`, `src/modeling/calculate_indicators.py` | `test_features.py`, `test_pipeline_modeling_viz.py`, `test_eda_explore_indicators.py` | `04_modeling/01_modeling_ipt.ipynb` |
| **RF-007** | Integración del Tablón Maestro Territorial Multidimensional | `src/integration.py` | `test_integration.py`, `test_pipeline_modeling_viz.py` | `03_integration/01_integration_master.ipynb` |
| **RF-008** | Cálculo del Índice de Priorización Territorial (IPT) y rankings | `src/modeling/calculate_indicators.py`, `src/visualization.py` | `test_pipeline_modeling_viz.py`, `test_visualization.py` | `04_modeling/01_modeling_ipt.ipynb` |
| **RF-009** | Exportación de artefactos para Dashboard y visualizaciones cartográficas | `src/visualization.py`, `src/eda/viz.py` | `test_visualization.py`, `test_eda_viz.py` | `05_visualization/01_visualization_dashboard.ipynb` |
| **RF-010** | Detección de anomalías y reportes estructurados de evaluación | `src/evaluation.py` | `test_evaluation.py` | `00_validation_master.ipynb` |

---

## 4. Detalle de los Módulos de Prueba

### 4.1. Suites Unitarias y Lógicas de `src/` (103 Tests)

1. `tests/test_cleaning.py` (8 tests): Normalización snake_case, eliminación de tildes y caracteres especiales, homologación DIVIPOLA de las 20 localidades de Bogotá, conversión segura de tipos numéricos.
2. `tests/test_features.py` (6 tests): Ratios de densidad poblacional, cálculo de tasas por 10k y 1k habitantes, persistencia en formato parquet/csv.
3. `tests/test_evaluation.py` (6 tests): Detección de outliers (IQR y Z-Score), reporte de nulos/duplicados/cardinalidad, generación y serialización de reportes de calidad.
4. `tests/test_eda_viz.py` (7 tests): Configuración de estilo editorial visual, generación de histogramas, boxplots, gráficos de barras, heatmaps de completitud, mapas coropléticos y series temporales.
5. `tests/test_visualization.py` (5 tests): Algoritmo de ranking descendente por score, control de columnas faltantes (`KeyError`), exportación curada para dashboard y carga de datasets curados.
6. `tests/test_integration.py` (6 tests): Algoritmo de merge por localidad con resolución de columnas alternativas (`COD_LOCALIDAD`, `NOMBRE_LOCALIDAD`), validación de esquema maestro y persistencia.
7. `tests/test_validation.py` (6 tests): Inspección de esquema, detección automática de columnas territoriales, validación de pertenencia territorial, suite completa de validación por dominios temáticos.
8. `tests/test_pipeline_modeling_viz.py` (8 tests): Pipeline integral de modelado, normalización Min-Max, cálculo de subíndices sectoriales y composición ponderada del IPT.
9. `tests/test_expansion_datasets.py` (8 tests): Integridad de datos para dominios de expansión (servicios públicos, empleo, PQR, fondos de desarrollo local).
10. `tests/test_ingest.py` (7 tests): Descarga robusta con reintentos y timeouts, detección de mime types y descompresión de archivos.
11. `tests/test_eda_profiling.py` (10 tests): Perfilado estadístico exhaustivo de series numéricas, categóricas y temporales.
12. `tests/test_eda_readers_quality.py` (10 tests): Lector robusto de CSV/XLSX con saltos automáticos de encabezados sucios y detección de codificación (UTF-8, Latin-1).
13. `tests/test_eda_spatial.py` (7 tests): Cruces espaciales acelerados con indexación R-tree (`intersects`), conteo de puntos por localidad y validación de CRS.
14. `tests/test_eda_explore_indicators.py` (4 tests): Consistencia de nombres y fórmulas de los 25 indicadores del catálogo.
15. `tests/test_geospatial_cleaning.py` (3 tests): Homologación de geometrías y corrección de topología en capas vectoriales.
16. `tests/test_education_geojson.py` (2 tests): Generación y validación de la capa GeoJSON de infraestructura educativa.

### 4.2. Suite Automatizada de Notebooks (76 Tests)

1. `tests/test_notebooks.py::TestNotebooksDiscovery` (1 test): Descubrimiento y verificación de presencia de los 25 cuadernos en la estructura de directorios.
2. `tests/test_notebooks.py::TestNotebooksStructureAndSchema` (25 tests): Verificación de cumplimiento del estándar JSON nbformat v4 en los 25 cuadernos.
3. `tests/test_notebooks.py::TestNotebooksSyntax` (25 tests): Compilación sintáctica mediante `ast.parse` garantizando 0 errores de sintaxis en todas las celdas de código.
4. `tests/test_notebooks.py::TestNotebooksExecution` (25 tests): Ejecución end-to-end de cada cuaderno de principio a fin en un namespace aislado y directorio de trabajo contextual.

---

## 5. Procedimiento de Ejecución

Para ejecutar la suite completa de pruebas:
```powershell
.venv\Scripts\python.exe -m pytest -v
```

Para ejecutar únicamente los tests unitarios de `src/`:
```powershell
.venv\Scripts\python.exe -m pytest tests/test_*.py --ignore=tests/test_notebooks.py -v
```

Para ejecutar la validación y ejecución automatizada de los 25 notebooks:
```powershell
.venv\Scripts\python.exe -m pytest tests/test_notebooks.py -v
```

---

## 6. Criterios de Aceptación

- [x] 100% de pruebas aprobadas (0 fallos, 0 errores).
- [x] Cobertura de todas las funciones críticas en `src/`.
- [x] Todos los 25 cuadernos ejecutables de manera reproducible sin intervención manual.
- [x] Trazabilidad completa con la especificación de requerimientos IEEE 830 (RF-001 a RF-010).
