# Especificación de Requerimientos de Software (SRS) — SIPTA (v1.0.0)

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA)  
**Versión**: 1.0.0  
**Fecha de Actualización**: 2026-08-24  
**Fase PDCO**: PLAN | **SDLC Stage**: Requirements Engineering  
**Estándares Rectores**: IEEE 830 / ISO/IEC/IEEE 29148 / DAMA-BOK / OECD-JRC / ISO/IEC 25010  
**Autores**: Persona A (Adan Sánchez), Persona B (Yesid Bello), Persona C (Sofía Hidalgo) — Equipo DataJam  

---

## 1. Introducción y Definición del Problema

Bogotá D.C. presenta marcadas disparidades socio-espaciales en acceso y calidad de servicios públicos, tiempos de conmutación laboral, capacidad hospitalaria, calidad educativa y seguridad. Las administraciones distritales y locales requieren un sistema analítico formal, auditable y reproducible que integre fuentes abiertas multivariadas, evalúe su calidad y calcule un **Índice de Priorización Territorial (IPT)** multidimensional y no compensatorio para la asignación eficiente de recursos públicos bajo estándares de la **OCDE / JRC**.

---

## 2. Requerimientos Funcionales (RF)

| ID | Requerimiento Funcional | Prioridad | Dominio / Módulo | Caso de Uso |
| :--- | :--- | :---: | :--- | :---: |
| **RF-001** | Ingestar datasets crudos en formatos CSV, GeoJSON, GPKG y TXT sin alterar su contenido original (`data/raw/`). | Alta | Pipeline / Ingesta | UC-001 |
| **RF-002** | Validar la calidad técnica de cada dataset bajo las dimensiones ISO 25010 (completitud, unicidad, consistencia, validez). | Alta | Calidad / Validación | UC-002 |
| **RF-003** | Homologar y validar la pertenencia de los registros a las 20 localidades canónicas de Bogotá D.C. | Alta | Territorio / Homologación | UC-003 |
| **RF-004** | Ejecutar cruces espaciales (*Point-in-Polygon*) para datasets georreferenciados (IPS, estaciones, cuadrantes). | Alta | Geoespacial | UC-004 |
| **RF-005** | Calcular indicadores sectoriales per cápita utilizando denominadores demográficos específicos por cohorte de edad. | Alta | Modelado / Indicadores | UC-005 |
| **RF-006** | Normalizar variables mediante escalamiento Min-Max $[0, 1]$ e invertir polaridades según criticidad teórica. | Alta | Modelado / IPT | UC-006 |
| **RF-007** | Consolidar el IPT Base ponderando las 7 dimensiones canónicas y evaluar 5 escenarios de sensibilidad. | Alta | Modelado / IPT | UC-007 |
| **RF-008** | Emitir alertas tempranas territoriales basadas en semáforos empíricos (🔴 Crítico, 🟠 Alto, 🟡 Medio, 🟢 Bajo). | Alta | Alertas Tempranas | UC-008 |
| **RF-009** | Generar reportes automáticos de calidad en formatos JSON, CSV y Markdown en `reports/validation/`. | Media | Reportes | UC-002 |
| **RF-010** | Estructurar matrices consolidadas para tableros de visualización en `src/visualization/`. | Alta | Visualización | UC-007 |
| **RF-011** | Calcular el Factor de Inflación de la Varianza ($\text{VIF}_j$) para certificar la no multicolinealidad dimensional ($\text{VIF} < 10.0$). | Alta | Auditoría Cuantitativa | UC-009 |
| **RF-012** | Calcular el IPT mediante Agregación Geométrica Ponderada ($\text{IPT}_{\text{Geom}}$) para evaluar penalización no compensatoria. | Alta | Modelado Avanzado | UC-010 |
| **RF-013** | Estimar Intervalos de Confianza al 95% ($\text{IC}_{95\%}$) para el IPT mediante remuestreo *Bootstrap* Dirichlet ($B = 1.000$). | Alta | Incertidumbre | UC-011 |
| **RF-014** | Aplicar el estimador de Marshall (*Empirical Bayes Rate Smoother*) en localidades con denominadores reducidos ($N < 10.000$). | Alta | Epidemiología | UC-012 |
| **RF-015** | Calcular el Índice de Moran Global ($I$) y su significancia por permutación Monte Carlo para verificar dependencia espacial. | Alta | Econometría Espacial | UC-013 |
| **RF-016** | Generar 13 informes analíticos sectoriales en `reports/domains/` acompañados de figuras multi-panel a 300 DPI. | Alta | Generación de Informes | UC-014 |
| **RF-017** | Compilar la aplicación Web GIS autónoma (`reports/dashboard_geografico_sipta.html`) con selector de 13 dominios, clasificación Fisher-Jenks y exportar la capa GeoJSON curada (`data/curated/sipta_localidades_multidominio.geojson`). | Alta | Visualización Web GIS | UC-015 |
| **RF-018** | Consolidar las Proyecciones Oficiales de Población DANE / SDP (2018-2035) como única fuente demográfica vinculante para el cálculo de tasas y denominadores per cápita distritales. | Alta | Demografía / Ingesta | UC-001 |
| **RF-019** | Procesar los 1.048.575 registros administrativos del Plan Único de Atención (PUA) 2024 de la SDIS para modelar atenciones y transferencias del Ingreso Mínimo Garantizado (IMG), comedores comunitarios y comisarías de familia. | Alta | Vulnerabilidad / Ingesta | UC-001 |

---

## 3. Requerimientos No Funcionales (RNF)

| ID | Categoría ISO 25010 | Descripción del Requerimiento | Métrica de Aceptación |
| :--- | :--- | :--- | :--- |
| **RNF-001** | **Fiabilidad / Calidad** | La suite automatizada de pruebas debe validar el 100% de los módulos sin fallos. | $\ge 190$ tests aprobados (100% Passing) |
| **RNF-002** | **Cobertura de Pruebas** | La cobertura de código en módulos críticos de validación, modelado y rigor debe superar el 90%. | Cobertura $\ge 90\%$ |
| **RNF-003** | **Eficiencia / Rendimiento**| El pipeline completo de validación y cálculo del IPT de los 12 dominios debe tardar menos de 60 segundos. | Tiempo $< 60$ s |
| **RNF-004** | **Mantenibilidad** | Todo el código debe cumplir estrictamente con PEP 8 y contener Type Hints en funciones públicas. | 0 errores en flake8 / mypy |
| **RNF-005** | **Reproducibilidad** | Cualquier investigador debe poder regenerar los artefactos y datasets procesados mediante CLI determinista. | Scripts 100% deterministas |
| **RNF-006** | **Trazabilidad de Datos**| Cada indicador y registro en la tabla maestra debe referenciar su fuente original, año y entidad rectora. | Trazabilidad 100% DAMA-BOK |
| **RNF-007** | **Estándar OCDE / JRC** | El modelo compuesto debe cumplir las 10 etapas metodológicas del Manual de la OCDE para índices sintéticos. | Certificación aprobada |
| **RNF-008** | **Honestidad Gráfica** | Las visualizaciones deben cumplir con la gramática de gráficos de Tufte/Wilke (origen en 0, paletas uniformes). | 100% figuras auditadas |

---

## 4. Restricciones Técnicas (R)

- **R-001**: Stack de desarrollo en **Python 3.11+**, utilizando **Pandas**, **GeoPandas**, **NumPy**, **SciPy**, **Matplotlib**, **Seaborn** y **Pytest**.
- **R-002**: Sistema de referencia espacial oficial: **WGS84 (EPSG:4326)** para capas vectoriales GeoJSON.
- **R-003**: Inmutabilidad de los datos crudos en `data/raw/` (nunca se sobrescriben en su ubicación de origen).
- **R-004**: Desempate determinístico jerárquico para el ranking territorial: $(\overline{R}_i \text{ ASC}, \text{IPT}_{\text{Base}} \text{ DESC}, \text{DIVIPOLA ASC})$.
