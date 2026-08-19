# Changelog — SIPTA

Todos los cambios notables de este proyecto se documentan en este archivo siguiendo [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
