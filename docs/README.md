# Índice Maestro de Documentación Técnica — SIPTA

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Marco de Trabajo**: SDLC / PDCO (Plan, Development, Control, Operations)  
**Estándares**: SWEBOK, DAMA-BOK, IEEE 830 / ISO 29148, ISO/IEC 25010  

---

## Estructura Documental por Fase del Ciclo de Vida

```
docs/
├── README.md                               ← Índice general de documentación (este documento)
│
├── 01-requirements/                        ← FASE PLAN: Requerimientos y Datos
│   ├── requirements.md                     ← Especificación formal IEEE 830 (RF, RNF, Restricciones)
│   ├── use-cases.md                        ← Casos de uso estructurados por entidad
│   ├── entity-map.md                       ← Mapa de entidades y modelo entidad-relación
│   ├── E01_inventario_datos.md             ← Inventario maestro de fuentes y datasets
│   ├── E02_diccionario_datos.md            ← Diccionario de datos y metadatos técnicos
│   ├── fichas_tecnicas_nuevos_dominios.md  ← Fichas técnicas de los 13 dominios
│   ├── evaluacion_calidad_datasets_consolidada.md ← Evaluación de calidad DAMA-BOK (27 datasets)
│   └── diagrams/                           ← Diagramas UML de Casos de Uso y Actividad
│
├── 02-architecture/                        ← FASE PLAN → DEVELOPMENT: Diseño del Sistema
│   ├── architecture.md                     ← Documento de Arquitectura de Software
│   ├── patterns.md                         ← Catálogo de patrones GoF y GRASP aplicados
│   ├── ADR/                                ← Architecture Decision Records (ADR-001..003)
│   └── diagrams/                           ← Diagramas UML de Clases, Secuencia y Componentes
│
├── 03-development/                         ← FASE DEVELOPMENT: Implementación y EDA
│   ├── dev-log.md                          ← Bitácora de desarrollo y atribución Git
│   ├── formulacion_matematica_ipt.md       ← Formulación matemática y metodológica del IPT
│   ├── api-docs.md                         ← Documentación técnica de módulos src/
│   ├── analisis_exploratorio_nuevos_dominios.md ← Síntesis exploratoria y brechas territoriales
│   └── technical-debt.md                   ← Análisis de deuda técnica y buenas prácticas
│
├── 04-testing/                             ← FASE CONTROL: Aseguramiento de Calidad
│   ├── test-plan.md                        ← Plan maestro de pruebas unitarias y de calidad
│   └── test-results.md                     ← Resultados de ejecución de la suite (73 tests)
│
└── 05-maintenance/                         ← FASE OPERATIONS: Mantenimiento y Evolución
    ├── changelog.md                        ← Registro de cambios (Keep a Changelog)
    └── refactoring-log.md                  ← Bitácora de optimizaciones y refactorización
```
