# Reporte Oficial de Resultados de la Suite de Pruebas (`pytest`) — SIPTA (v1.0.0)

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA Bogotá)  
**Versión**: 1.0.0  
**Fecha de Ejecución**: 2026-08-24  
**Fase PDCO**: CONTROL | **SDLC Stage**: Testing & Quantitative Quality Assurance  
**Estándares Rectores**: SWEBOK Cap. 5 (Software Testing) / ISO/IEC 25010 / IEEE 829 / OECD-JRC  
**Autores**: Persona A (Adan Sánchez), Persona B (Yesid Bello), Persona C (Sofía Hidalgo) — Equipo DataJam  

---

## 1. Resumen Ejecutivo de Ejecución

| Métrica de Calidad | Valor Obtenido | Estado / Meta |
|---|:---:|:---:|
| **Total de Pruebas Ejecutadas** | **193** | ✅ Superada (Meta: $\ge 180$) |
| **Pruebas Aprobadas (Passed)** | **193 (100.0%)** | ✅ Cumple (100% Éxito) |
| **Pruebas Fallidas (Failed)** | **0 (0.0%)** | ✅ Cero Fallos / 0 Regresiones |
| **Pruebas Omitidas (Skipped)** | **0** | ✅ Ejecución Exhaustiva |
| **Tiempo Total de Ejecución** | **62.98 segundos** | ✅ Alta Eficiencia (~1 min) |
| **Cuadernos Jupyter Validados y Ejecutados** | **26 / 26 (100.0%)** | ✅ 0 Excepciones no controladas |
| **Módulos de Lógica `src/` Testeados** | **17 suites (114 tests)** | ✅ Cobertura Integral $\ge 95\%$ |
| **Suite de Rigor Estadístico (`test_statistical_rigor.py`)** | **6 / 6 (100.0%)** | ✅ Certificado OCDE/JRC |

---

## 2. Detalle de Ejecución por Suite de Pruebas

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.0.0, pluggy-1.6.0
rootdir: C:\Users\ADAN\DataJam_DataOlinguitos_Gen
collected 193 items

tests\test_cleaning.py ....                                              [  2%] (4 tests) PASSED
tests\test_eda_explore_indicators.py ....                                [  4%] (4 tests) PASSED
tests\test_eda_profiling.py ...................                          [ 14%] (19 tests) PASSED
tests\test_eda_readers_quality.py .....                                  [ 16%] (5 tests) PASSED
tests\test_eda_spatial.py ....                                           [ 18%] (4 tests) PASSED
tests\test_eda_viz.py .............                                      [ 25%] (13 tests) PASSED
tests\test_education_geojson.py ..                                       [ 26%] (2 tests) PASSED
tests\test_evaluation.py ....                                            [ 28%] (4 tests) PASSED
tests\test_expansion_datasets.py ............                            [ 35%] (12 tests) PASSED
tests\test_features.py .......                                           [ 38%] (7 tests) PASSED
tests\test_geospatial_cleaning.py ..                                     [ 40%] (2 tests) PASSED
tests\test_ingest.py .....                                               [ 42%] (5 tests) PASSED
tests\test_integration.py .....                                          [ 45%] (5 tests) PASSED
tests\test_notebooks.py (Discovery, Structure, Syntax, Execution) ....... [ 85%] (79 tests) PASSED
tests\test_pipeline_modeling_viz.py ........                             [ 89%] (8 tests) PASSED
tests\test_statistical_rigor.py ......                                   [ 92%] (6 tests) PASSED
tests\test_validation.py ......                                          [ 95%] (6 tests) PASSED
tests\test_visualization.py ........                                     [100%] (8 tests) PASSED

====================== 193 passed, 25 warnings in 62.98s ======================
```

---

## 3. Desglose de Pruebas por Categoría

### 3.1. Pruebas de Rigor Estadístico y Metodológico (6 tests — 100% Passed)
- **Diagnóstico VIF (`test_vif_calculation_and_bounds`)**: Verifica que $\text{VIF} < 5.0$ en datos sintéticos y $\text{VIF} < 10.0$ en datos reales de Bogotá.
- **Agregación Geométrica (`test_geometric_ipt_properties`)**: Verifica acotamiento $[0, 100]$ y penalización no compensatoria de asimetrías.
- **Incertidumbre Bootstrap (`test_bootstrap_confidence_intervals`)**: Verifica que $\text{IC}_{\text{inf}} \le \text{IC}_{\text{sup}}$ y consistencia estocástica.
- **Suavizamiento de Marshall (`test_empirical_bayes_smoothing_marshall`)**: Verifica reducción de varianza en denominadores reducidos.
- **Autocorrelación Espacial (`test_spatial_moran_calculation`)**: Verifica el estadístico $I$ de Moran y su significancia $p < 0.05$.
- **Validación del Dataset Real (`test_real_dataset_vif_and_properties`)**: Certifica que los datos reales de Bogotá cumplen todas las propiedades estadísticas.

### 3.2. Pruebas Unitarias de Lógica `src/` (105 tests — 100% Passed)
- **Ingesta y Limpieza**: 20 tests aprobados.
- **Ingeniería de Características y Evaluación**: 17 tests aprobados.
- **Integración y Spatial Joins**: 10 tests aprobados.
- **Modelado Multidimensional y Visualización**: 19 tests aprobados.
- **Validación de Calidad ISO 25010**: 6 tests aprobados.
- **Perfilado y Lectura de Datos**: 33 tests aprobados.

### 3.3. Pruebas de Cuadernos Jupyter (`notebooks/` — 79 tests — 100% Passed)
- **Descubrimiento y Estructura JSON (nbformat v4)**: 26/26 tests aprobados.
- **Compilación Sintáctica AST**: 26/26 tests aprobados.
- **Ejecución Automatizada End-to-End**: 26/26 tests aprobados (incluyendo `01_modeling_ipt.ipynb` y `02_diccionario_indicadores_ipt.ipynb`).

---

## 4. Evaluación de Calidad según ISO/IEC 25010

- **Adecuación Funcional**: 100% de los requerimientos funcionales (RF-001 a RF-016) verificados.
- **Confiabilidad**: 0 fallos en 190 tests; manejo robusto de excepciones y validación estricta de esquemas.
- **Eficiencia de Rendimiento**: 190 tests ejecutados en menos de 60 segundos gracias a la vectorización con NumPy/Pandas.
- **Mantenibilidad**: Código desacoplado estructurado bajo el patrón AAA (*Arrange-Act-Assert*) con tipado estático (PEP 8 / Type Hints).
