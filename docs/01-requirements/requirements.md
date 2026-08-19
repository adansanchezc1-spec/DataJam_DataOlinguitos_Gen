# Especificación de Requerimientos de Software (SRS) — SIPTA
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas  
**Versión**: 2.0.0  
**Fecha**: 2026-08-18  
**Fase PDCO**: PLAN | **SDLC Stage**: Requirements Engineering  
**Estándar**: IEEE 830 / ISO/IEC/IEEE 29148  
**Autores**: Persona A (Adan Sánchez), Persona B (Yesid Bello), Persona C (Sofía Hidalgo)  

---

## 1. Introducción y Definición del Problema
Bogotá D.C. presenta marcadas brechas territoriales en acceso y calidad de servicios públicos, tiempos de conmutación laboral, capacidad hospitalaria, calidad educativa y seguridad. Las administraciones locales y distritales requieren un sistema analítico reproducible que integre fuentes abiertas multivariadas, evalúe su calidad y calcule un **Índice de Prioridad Territorial (IPT)** para la asignación eficiente de recursos públicos.

---

## 2. Requerimientos Funcionales (RF)

| ID | Requerimiento | Prioridad | Entidad / Dominio | Caso de Uso |
| :--- | :--- | :---: | :--- | :---: |
| **RF-001** | El sistema debe descargar e ingestar datasets crudos en formatos CSV, GeoJSON, GPKG y TXT sin alterar su contenido original. | Alta | Pipeline / Ingesta | UC-001 |
| **RF-002** | El sistema debe validar la calidad técnica de cada dataset bajo las dimensiones ISO 25010 (completitud, unicidad, consistencia, validez). | Alta | Calidad / Validación | UC-002 |
| **RF-003** | El sistema debe homologar y validar la pertenencia de los registros a las 20 localidades canónicas de Bogotá D.C. | Alta | Territorio / Homologación | UC-003 |
| **RF-004** | El sistema debe ejecutar cruces espaciales (Point-in-Polygon) para datasets georreferenciados (IPS, estaciones, cuadrantes). | Alta | Geoespacial | UC-004 |
| **RF-005** | El sistema debe calcular indicadores sectoriales per cápita utilizando las proyecciones de población oficiales D1. | Alta | Modelado / Indicadores | UC-005 |
| **RF-006** | El sistema debe normalizar variables mediante escalamiento Min-Max [0, 1] e invertir polaridades según criticidad. | Alta | Modelado / IPT | UC-006 |
| **RF-007** | El sistema debe consolidar el Índice de Prioridad Territorial (IPT) ponderando las 7 dimensiones multidimensionales. | Alta | Modelado / IPT | UC-007 |
| **RF-008** | El sistema debe emitir alertas tempranas territoriales basadas en peticiones PQR no resueltas e interrupciones de servicios. | Media | Alertas Tempranas | UC-008 |
| **RF-009** | El sistema debe generar reportes automáticos de calidad en formatos JSON, CSV y Markdown en `reports/validation/`. | Media | Reportes | UC-002 |
| **RF-010** | El sistema debe estructurar matrices consolidadas para el consumo de tableros de visualización en `src/visualization/`. | Alta | Visualización | UC-007 |

---

## 3. Requerimientos No Funcionales (RNF)

| ID | Categoría ISO 25010 | Descripción del Requerimiento | Métrica de Aceptación |
| :--- | :--- | :--- | :--- |
| **RNF-001** | **Fiabilidad / Calidad** | La suite automatizada de pruebas debe validar el 100% de los módulos sin fallos. | $\ge 70$ tests aprobados en pytest |
| **RNF-002** | **Cobertura de Pruebas** | La cobertura de código en módulos críticos de validación y modelado debe superar el 90%. | Cobertura $\ge 90\%$ |
| **RNF-003** | **Eficiencia / Rendimiento**| El pipeline completo de validación y cálculo del IPT de los 13 dominios debe tardar menos de 30 segundos. | Tiempo $< 30$ s |
| **RNF-004** | **Mantenibilidad** | Todo el código debe cumplir estrictamente con el estándar PEP 8 y contener Type Hints en funciones públicas. | 0 errores flake8 / mypy |
| **RNF-005** | **Reproducibilidad** | Cualquier miembro del equipo debe poder regenerar los artefactos y datasets procesados mediante comandos CLI deterministas. | `python -m src...` determinista |
| **RNF-006** | **Trazabilidad de Datos**| Cada indicador y registro en la tabla maestra debe referenciar su fuente original, año y autoría técnica. | Trazabilidad 100% en DAMA-BOK |

---

## 4. Restricciones Técnicas (R)
- **R-001**: Stack de desarrollo exclusivo en **Python 3.11+**, utilizando **Pandas**, **GeoPandas**, **NumPy** y **Pytest**.
- **R-002**: Sistema de referencia espacial oficial: **WGS84 (EPSG:4326)** para capas vectoriales GeoJSON.
- **R-003**: Inmutabilidad de los datos crudos en `data/raw/` (nunca se sobrescriben en su ubicación de origen).
