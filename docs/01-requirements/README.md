# Fase 01 — Análisis de Requerimientos y Datos (PLAN)

**Fase PDCO**: PLAN | **SDLC Stage**: Requirements & Data Architecture  
**Estándares**: IEEE 830 / ISO 29148, DAMA-BOK, ISO/IEC 25010  

---

## 📋 Propósito de la Fase

La fase de **Requerimientos y Datos** formaliza las necesidades de negocio, los casos de uso territoriales, el catálogo de 25 datasets oficiales estructurados en 13 dominios analíticos y el inventario maestro de indicadores de SIPTA.

---

## 🗂️ Índice de Documentos de la Fase

| Documento | Descripción | Estándar / Metodología |
| :--- | :--- | :--- |
| [`requirements.md`](requirements.md) | Especificación formal de Requerimientos Funcionales (RF), No Funcionales (RNF) y Restricciones. | IEEE 830 / ISO 29148 |
| [`use-cases.md`](use-cases.md) | Casos de uso estructurados por entidad y actores del sistema. | SWEBOK Cap. 1 |
| [`entity-map.md`](entity-map.md) | Mapa de entidades de negocio y modelo entidad-relación (ER). | DAMA-BOK |
| [`E01_inventario_datos.md`](E01_inventario_datos.md) | Inventario maestro de las 25 fuentes y datasets crudos oficiales. | DAMA-BOK |
| [`E02_diccionario_datos.md`](E02_diccionario_datos.md) | Diccionario exhaustivo de datos, tipos, rangos y descripciones de los 13 dominios. | DAMA-BOK / ISO 25010 |
| [`fichas_tecnicas_indicadores_base.md`](fichas_tecnicas_indicadores_base.md) | Fichas técnicas conceptuales de los indicadores base del proyecto. | DAMA-BOK |
| [`fichas_tecnicas_nuevos_dominios.md`](fichas_tecnicas_nuevos_dominios.md) | Fichas técnicas de los dominios de expansión (Servicios, Empleo, PQR, etc.). | DAMA-BOK |
| [`evaluacion_calidad_datasets_consolidada.md`](evaluacion_calidad_datasets_consolidada.md) | Evaluación multivariada de calidad de datos consolidada. | ISO/IEC 25010 / DAMA-BOK |
| [`matriz_calidad_datos.md`](matriz_calidad_datos.md) | Matriz de diagnóstico de completitud, consistencia y validez por dataset. | DAMA-BOK |
| [`matriz_trazabilidad_analitica.md`](matriz_trazabilidad_analitica.md) | Matriz de trazabilidad Requerimiento $\rightarrow$ Fuente $\rightarrow$ Indicador $\rightarrow$ Modelo. | SWEBOK |
| [`inventario_maestro_indicadores.md`](inventario_maestro_indicadores.md) | Catálogo maestro de indicadores clasificados por código sectorial. | SWEBOK |
| [`dim_territorio.md`](dim_territorio.md) | Marco canónico de homologación de las 20 localidades y códigos DIVIPOLA. | Marco Territorial D.C. |
| [`principios_modelo_territorial.md`](principios_modelo_territorial.md) | Principios de diseño del modelado territorial e indicadores compuestos. | DAMA-BOK |
| [`alcance_supuestos_restricciones.md`](alcance_supuestos_restricciones.md) | Delimitación del alcance analítico, supuestos y restricciones del sistema. | IEEE 830 |
| [`plantilla_evaluacion_calidad.md`](plantilla_evaluacion_calidad.md) | Formato estándar de evaluación de calidad de datos para nuevas fuentes. | ISO/IEC 25010 |
| [`diagrams/`](diagrams/) | Diagramas UML de Casos de Uso y Diagramas de Actividad en Mermaid. | UML 2.5 |