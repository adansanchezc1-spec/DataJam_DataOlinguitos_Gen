# Development Log — SIPTA Pipeline
**Proyecto**: DataJam_DataOlinguitos_Gen (SIPTA)  
**Sprint / Iteración**: Sprint 1 - 2  
**Fecha**: 2026-08-15  
**Fase PDCO**: DEVELOPMENT  
**Skill Activa**: `software-development`  

---

## 1. Módulos Desarrollados / Corregidos

| Módulo | Descripción | Requerimientos / Workflow | Estado |
|:---|:---|:---|:---|
| `src/ingestion/ingest_data.py` | Ingesta polimórfica (CSV, XLSX, GPKG, GeoJSON, ZIP) y manifiesto | 1.2 Ingesta de datos | ✅ Completo |
| `src/validation/validate_data.py` | Calidad de datos, nulos, duplicados y validación contra 20 localidades D.C. | 1.3 Validación de datos | ✅ Completo |
| `src/cleaning/clean_data.py` | Normalización snake_case, casteo numérico y tabla oficial de homologación | 1.4 Limpieza y estandarización | ✅ Completo |
| `src/integration/integrate_data.py` | Resolución de ruta raíz y merge territorial por localidad canónica | 1.5 Integración territorial | ✅ Completo |
| `src/modeling/calculate_indicators.py` | Normalización Min-Max e IPT compuesto ponderado | 1.6 Modelado e indicadores | ✅ Completo |
| `src/visualization/prepare_visualization.py` | Resolución de ruta y generación de ranking para dashboard | 1.7 Visualización | ✅ Completo |
| `docs/diccionario_datos.md` | Catálogo de variables, unidades y reglas de homologación | Documentación transversal | ✅ Completo |

---

## 2. Corrección de Notebooks

| Notebook | Correcciones Realizadas | Estado |
|:---|:---|:---|
| `notebooks/01_ingestion.ipynb` | Sincronizado con `src.ingestion`, catálogo dinámico de fuentes crudas y manifiesto. | ✅ Operativo |
| `notebooks/02_validation.ipynb` | Sincronizado con `src.validation`, perfil de esquema y validación de cobertura de 20 localidades. | ✅ Operativo |
| `notebooks/03_integration.ipynb` | Reparado syntax error en celda JSON, integrado con `src.cleaning` y `src.integration`. | ✅ Operativo |
| `notebooks/04_modeling.ipynb` | Sincronizado con `src.modeling`, cálculo de tasas y ensamble de IPT. | ✅ Operativo |
| `notebooks/05_visualization.ipynb` | Sincronizado con `src.visualization`, ranking y exportación curada para dashboard. | ✅ Operativo |

---

## 3. Decisiones de Arquitectura e Implementación (ADR Breve)

- **DI-001**: Estandarización de `ROOT` en todos los módulos de `src/` a `Path(__file__).resolve().parents[2]` para eliminar la creación no deseada de `src/data/` y consolidar la lectura/escritura en la raíz `data/`.
- **DI-002**: Catálogo explícito de las 20 localidades de Bogotá con código de orden y código oficial DIVIPOLA (`1100101` a `1100120`) para desacoplar el pipeline de variaciones tipográficas en las fuentes originales.
- **DI-003**: Ingesta agnóstica de encoding con fallback ordenado (`utf-8` $\rightarrow$ `latin-1` $\rightarrow$ `cp1252`) y separadores (`comma`, `semicolon`, `tab`).
