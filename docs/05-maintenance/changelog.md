# Changelog — SIPTA

Todos los cambios notables de este proyecto se documentan en este archivo siguiendo [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
- **Resiliencia en Notebooks**: Implementación de auto-inicialización independiente y resolución jerárquica de `ROOT` en todos los 24 notebooks estructurados (`01_ingestion/`, `02_validation/`, `03_integration/`, `04_modeling/`, `05_visualization/`).
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
