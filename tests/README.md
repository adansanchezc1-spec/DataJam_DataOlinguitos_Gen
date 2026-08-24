# Suite de Pruebas Automatizadas — `tests/`

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA)  
**Marco de Trabajo**: SWEBOK Cap. 5 / IEEE 829 / ISO 29119 / ISO/IEC 25010  
**Framework**: `pytest 8.0+`, `pytest-cov`  
**Patrón de Pruebas**: AAA (Arrange-Act-Assert)  

---

## 🧪 Estructura de Suites de Prueba

| Archivo de Prueba | Componente Evaluado | Casos / Aserciones Clave |
| :--- | :--- | :--- |
| [`test_pipeline_modeling_viz.py`](test_pipeline_modeling_viz.py) | `src.modeling` & `src.visualization` | Cálculo de IPT, 7 dimensiones, tablas por dominio, ranking de consenso. |
| [`test_integration.py`](test_integration.py) | `src.integration` | Integración territorial, cobertura de las 20 localidades, Tablón Maestro. |
| [`test_cleaning.py`](test_cleaning.py) | `src.cleaning` | Homologación canónica DIVIPOLA, snake_case, tipado numérico. |
| [`test_features.py`](test_features.py) | `src.features` | Densidades poblacionales, ratios per cápita. |
| [`test_validation.py`](test_validation.py) | `src.validation` | Esquemas de datos, nulos, duplicados, validación territorial. |
| [`test_ingest.py`](test_ingest.py) | `src.ingestion` | Ingesta polimórfica de archivos y manifiesto JSON. |
| [`test_evaluation.py`](test_evaluation.py) | `src.evaluation` | Reportes de calidad y detección de anomalías. |
| [`test_visualization.py`](test_visualization.py) | `src.visualization` | Generación de matrices para dashboard. |
| [`test_eda_*.py`](.) | `src.eda.*` | Lectores, perfilado estadístico, calidad y visualizaciones EDA. |

---

## 🚀 Ejecución de Pruebas

```bash
# Ejecutar todas las pruebas unitarias
python -m pytest tests/ --ignore=tests/test_notebooks.py

# Ejecutar pruebas con detalle y reporte de cobertura
python -m pytest tests/ --ignore=tests/test_notebooks.py -v --cov=src

# Ejecutar únicamente la suite de modelado
python -m pytest tests/test_pipeline_modeling_viz.py -v
```
