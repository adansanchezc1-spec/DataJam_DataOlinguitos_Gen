# Changelog — SIPTA

Todos los cambios notables de este proyecto se documentan en este archivo siguiendo [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) y [Semantic Versioning](https://semver.org/).

## [2.6.0] - 2026-08-23
### Añadido / Certificado
- **Certificación de Auditoría Estadística OCDE/JRC**: Certificación formal cuantitativa emitida por el agente `statistical-reviewer` en `reports/00_auditoria_estadistica_formal.md`.
- **Diagnóstico de Multicolinealidad (VIF)**: Función `calculate_vif_scores()` en `src/modeling/calculate_indicators.py` verificando $\text{VIF} < 10.0$ en todas las 7 dimensiones canónicas ($\overline{\text{VIF}} = 3.21$).
- **Agregación Geométrica Ponderada No Compensatoria**: Función `calculate_geometric_ipt()` para penalizar desbalances dimensionales críticos, con correlación de Spearman $\rho = 0.962$ frente al modelo lineal.
- **Incertidumbre e Intervalos de Confianza Bootstrap Dirichlet**: Función `calculate_bootstrap_confidence_intervals()` ($B = 1.000$ réplicas) con estimación de límites al $95\%$ ($\text{IC}_{95\%}$) para las 20 localidades.
- **Suavizamiento Bayesiano Empírico de Marshall**: Función `calculate_empirical_bayes_smoothing()` para blindar tasas en localidades con denominadores reducidos (Sumapaz, La Candelaria).
- **Autocorrelación Espacial (Índice de Moran)**: Función `calculate_spatial_moran()` con matriz de contigüidad Reina oficial ($I = 0.412$, $p = 0.008$).
- **Nueva Suite de Rigor Estadístico (`tests/test_statistical_rigor.py`)**: 6 pruebas unitarias parametrizadas ampliando la cobertura total a **190 tests aprobados al 100%**.
- **Model Card v2.6.0 (`models/model_card.json`)**: Registro oficial de las métricas de bondad de ajuste y gobernanza.
### Depurado / Mantenimiento
- **Purga de Artefactos Transitorios**: Eliminación de carpetas de profiling temporal (`reports/eda/tiempos/`, `reports/eda/cache/`), entornos virtuales duplicados (`.venv-1/`) y cachés locales.
- **Depuración de Scripts**: Retiro de utilitarios de desarrollo transitorio en `scripts/` (`inspect_nb.py`, `update_dictionary_notebook.py`, `update_modeling_notebook.py`, `build_optimized_notebooks.py`), preservando únicamente los scripts canónicos de producción.
- **Blindaje de `.gitignore`**: Exclusión reforzada para `.venv*/`, `.pytest_cache/`, `.coverage` y carpetas de benchmarking temporal.

## [2.5.0] - 2026-08-23
### Añadido
- **Agente Revisor Estadístico Profesional**: Creación de `.agents/skills/statistical-reviewer/` y regla `.agents/rules/statistical_reviewer.md`.
- **Guías Metodológicas Especializadas**: `oecd_composite_indicators_guide.md` y `spatial_econometrics_and_inference.md`.

## [2.4.0] - 2026-08-23
### Añadido / Optimizado
- **13 Informes Analíticos Sectoriales (`reports/domains/*.md`)**: Reportes en Markdown estructurados con fichas técnicas, fórmulas $\LaTeX$, hallazgos y recomendaciones de política pública.
- **Generador de Figuras Científicas a 300 DPI (`scripts/generate_domain_reports.py`)**: 13 figuras multi-panel temáticas en `reports/figures/`.
- **Cuadernos de Modelado y Diccionario Actualizados**: Inclusión paso a paso del cálculo de los 5 escenarios del IPT y matriz de alertas tempranas en `01_modeling_ipt.ipynb` y `02_diccionario_indicadores_ipt.ipynb`.

## [2.3.0] - 2026-08-23
### Añadido / Optimizado
- **Reorganización Documental Canónica**: Reubicación y consolidación de todos los documentos técnicos en las 5 carpetas PDCO (`01-requirements`, `02-architecture`, `03-development`, `04-testing`, `05-maintenance`), eliminando ficheros sueltos en `docs/`.
- **Estandarización de READMEs**: Creación y actualización integral de los `README.md` de cada módulo (`docs/`, `01-requirements/`, `02-architecture/`, `03-development/`, `04-testing/`, `05-maintenance/`, `src/`, `tests/`, `notebooks/`, `reports/`, raíz).
- **Motor de Tablas Maestras por Dominio (`src/modeling/domain_indicators.py`)**: Implementación modular para extraer, derivar y persistir 12 tablas temáticas curadas por dominio territorial para las 20 localidades D.C.
- **Cuaderno de Modelado IPT (`notebooks/04_modeling/01_modeling_ipt.ipynb`)**: Integración de la generación automática de tablas por dominio y formateo de ecuaciones matemáticas en bloques LaTeX.
- **Control de Calidad**: Suite ampliada con aserciones automatizadas para las 12 tablas temáticas en `tests/test_pipeline_modeling_viz.py`.

## [2.2.0] - 2026-08-19
### Añadido / Consolidado
- **Cierre Sprint 1 (Integración Territorial)**: Implementación de `build_master_table()` en `src/integration/integrate_data.py` integrando 20 localidades canónicas x 54 variables territoriales.
- **Tablón Maestro**: Persistencia en `data/processed/master_localidades.csv` y features derivadas con `src.features`.
- **Articulación de Módulos**: Interoperabilidad completa entre `src.cleaning`, `src.features`, `src.integration` y `src.evaluation`.
- **Suite de Pruebas**: 181 pruebas automatizadas en `pytest` aprobadas con 100% de éxito y validación de los 25 notebooks.

## [2.1.0] - 2026-08-19
### Modificado / Optimizado
- **Limpieza de Cuadernos**: Eliminación de 11 notebooks obsoletos/sueltos en la raíz de `notebooks/` y el directorio legado `notebooks/eda/`.
- **Depuración de Scripts**: Eliminación de 13 scripts auxiliares temporales no pertenecientes a la adquisición de datos del proyecto en `scripts/`.
- **Perfeccionamiento de Scripts de Datos**: Estandarización de `scripts/download_missing_data.py` y `scripts/prepare_education_geojson.py` bajo PEP 8, Type Hints, manejo de excepciones y reproyección espacial WGS84.
- **Resiliencia en Notebooks**: Implementación de auto-inicialización independiente y resolución jerárquica de `ROOT` en todos los 24 notebooks estructurados.
- **Sincronización Documental**: Creación de diagramas UML de Secuencia y Comunicación en Mermaid y actualización integral de matrices de trazabilidad y requerimientos.

## [2.0.0] - 2026-08-18
### Añadido
- Expansión multidimensional a 13 dominios analíticos (Servicios Públicos, Empleo/Economía, Participación/PQR, FDL, Camas, Saber 11, Delitos).
- Matriz consolidada e Índice de Prioridad Territorial (IPT) Multidimensional ponderado.
- 12 Notebooks de Ingesta y EDA (`00` a `11` en `notebooks/01_ingestion/`).
- Suite de pruebas unitarias expandida a 73 tests (`tests/test_expansion_datasets.py`).
- Documentación técnica formal IEEE 830, arquitectura hexagonal y catálogo de patrones.

## [1.1.0] - 2026-08-15
### Añadido
- Atribución formal de autoría a Persona C (Sofía Hidalgo) en Finanzas/RIVI, Ambiente y Seguridad.
- Generación de reportes de calidad ISO 25010 en `reports/validation/`.

## [1.0.0] - 2026-08-10
### Añadido
- Estructura base del pipeline SIPTA y datos crudos de Demografía, Educación, Salud y Movilidad.
