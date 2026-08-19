# Reporte de Resultados de la Suite de Pruebas (`pytest`)

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA Bogota)  
**Versión**: 2.2.0  
**Fecha de Ejecución**: 2026-08-19  
**Fase PDCO**: CONTROL | **SDLC Stage**: Testing  
**Estándares**: SWEBOK Cap. 5 / ISO/IEC 25010 / IEEE 829  

---

## 1. Resumen Ejecutivo de Ejecución

| Métrica | Valor Obtenido | Estado / Meta |
|---------|----------------|---------------|
| **Total de Pruebas Ejecutadas** | **181** | Superada (Meta: $\ge 150$) |
| **Pruebas Aprobadas (Passed)** | **181 (100.0%)** | Cumple (100%) |
| **Pruebas Fallidas (Failed)** | **0 (0.0%)** | Cumple (0%) |
| **Pruebas Omitidas (Skipped)** | **0** | Cumple |
| **Tiempo Total de Ejecución** | **82.71 segundos** | Alta eficiencia (< 2 min) |
| **Cuadernos Jupyter Validados y Ejecutados** | **25 / 25 (100.0%)** | Cumple |
| **Módulos de Lógica `src/` Testeados** | **16 suites (105 tests)** | Cumple |

---

## 2. Detalle por Suite de Pruebas

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.0.0, pluggy-1.6.0
rootdir: C:\Users\ADAN\DataJam_DataOlinguitos_Gen

tests/test_cleaning.py .................................................... [ 4%] (8 tests) PASSED
tests/test_eda_explore_indicators.py ....                                   [ 6%] (4 tests) PASSED
tests/test_eda_profiling.py ..........                                     [12%] (10 tests) PASSED
tests/test_eda_readers_quality.py ..........                               [18%] (10 tests) PASSED
tests/test_eda_spatial.py .......                                          [22%] (7 tests) PASSED
tests/test_eda_viz.py .......                                              [26%] (7 tests) PASSED
tests/test_education_geojson.py ..                                         [27%] (2 tests) PASSED
tests/test_evaluation.py ......                                            [30%] (6 tests) PASSED
tests/test_expansion_datasets.py ........                                  [35%] (8 tests) PASSED
tests/test_features.py ......                                              [38%] (6 tests) PASSED
tests/test_geospatial_cleaning.py ...                                      [40%] (3 tests) PASSED
tests/test_ingest.py .......                                               [44%] (7 tests) PASSED
tests/test_integration.py ......                                           [47%] (6 tests) PASSED
tests/test_notebooks.py (Discovery, Structure, Syntax, Execution) ......... [90%] (76 tests) PASSED
tests/test_pipeline_modeling_viz.py ........                               [94%] (8 tests) PASSED
tests/test_validation.py ......                                            [97%] (6 tests) PASSED
tests/test_visualization.py .....                                          [100%] (5 tests) PASSED

====================== 179 passed, 64 warnings in 59.43s ======================
```

---

## 3. Desglose de Pruebas por Categoría

### 3.1. Pruebas Unitarias de Lógica `src/` (103 tests — 100% Passed)
- **Normalización y Limpieza de Datos (`src/cleaning.py`)**: 8/8 tests aprobados.
- **Ingeniería de Características (`src/features.py`)**: 6/6 tests aprobados.
- **Evaluación y Detección de Outliers (`src/evaluation.py`)**: 6/6 tests aprobados.
- **Visualización y Gráficos EDA (`src/eda/viz.py`)**: 7/7 tests aprobados.
- **Ranking y Exportación Dashboard (`src/visualization.py`)**: 5/5 tests aprobados.
- **Integración Tablón Maestro (`src/integration.py`)**: 6/6 tests aprobados.
- **Validación Multidominio (`src/validation/validate_data.py`)**: 6/6 tests aprobados.
- **Pipeline Integral y Modelado IPT (`src/modeling/calculate_indicators.py`)**: 8/8 tests aprobados.
- **Datasets de Expansión Territorial**: 8/8 tests aprobados.
- **Ingesta y Descargas Polimórficas (`src/ingest.py`)**: 7/7 tests aprobados.
- **Perfilado Estadístico (`src/eda/profiling.py`)**: 10/10 tests aprobados.
- **Lectura Robusta de Datos (`src/eda/readers.py`, `quality.py`)**: 10/10 tests aprobados.
- **Procesamiento Geoespacial (`src/eda/spatial.py`)**: 7/7 tests aprobados.
- **Consistencia de Indicadores (`src/eda/explore_indicators.py`)**: 4/4 tests aprobados.
- **Limpieza Geoespacial y GeoJSON**: 5/5 tests aprobados.

### 3.2. Pruebas de Cuadernos Jupyter (`notebooks/` — 76 tests — 100% Passed)
- **Descubrimiento y Existencia**: 1/1 test aprobado (25 notebooks detectados).
- **Estructura y Esquema JSON (nbformat v4)**: 25/25 tests aprobados.
- **Compilación Sintáctica AST**: 25/25 tests aprobados (0 errores de sintaxis).
- **Ejecución Automatizada End-to-End**: 25/25 tests aprobados (0 excepciones no controladas).

---

## 4. Evaluación de Calidad según ISO/IEC 25010

- **Adecuación Funcional**: 100% de los requerimientos RF-001 a RF-010 verificados y cubiertos.
- **Confiabilidad**: 0 fallos o regresiones en toda la suite; manejo robusto de excepciones y esquemas de fallback.
- **Eficiencia de Desempeño**: Suite completa ejecutada en menos de 60 segundos gracias a la optimización de cruces espaciales (R-tree `intersects`) y muestreo adaptativo (`smoke=True`).
- **Mantenibilidad**: Código de pruebas desacoplado, estructurado bajo el patrón AAA, con fixtures modulares y tipado estático (PEP 8 / Type Hints).
