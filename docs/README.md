# Índice Maestro de Documentación Técnica — SIPTA (v1.0.0)

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA — DataJam Bogotá 2026)  
**Marco de Trabajo**: SDLC / PDCO (Plan, Development, Control, Operations)  
**Estándares Rectores**: SWEBOK v3, DAMA-BOK, IEEE 830 / ISO 29148, ISO/IEC 25010, OECD/JRC, Clean Code, PEP 8  
**Autores**: Adan Sánchez (Persona A), Yesid Bello (Persona B), Sofía Hidalgo (Persona C) — Equipo DataJam  

---

## 🏛️ Estructura Documental por Fase del Ciclo de Vida (PDCO)

Toda la documentación técnica del proyecto se organiza estrictamente en las cinco fases del marco de trabajo:

```
docs/
├── README.md                               ← Índice general de documentación (este documento)
│
├── 01-requirements/                        ← FASE PLAN: Requerimientos, Datos e Indicadores
│   ├── README.md                           ← Guía y catálogo de la fase de Requerimientos
│   ├── requirements.md                     ← Especificación formal IEEE 830 (RF-001..017, RNF-001..008)
│   ├── use-cases.md                        ← Casos de uso estructurados por entidad
│   ├── entity-map.md                       ← Mapa de entidades y modelo entidad-relación
│   ├── FORMULARIO_CARACTERIZACION_FORMULACION_PROBLEMAS.md ← Caracterización de necesidades públicas
│   ├── E01_inventario_datos.md             ← Inventario maestro de fuentes y 25 datasets oficiales
│   ├── E02_diccionario_datos.md            ← Diccionario de datos y metadatos técnicos (13 dominios)
│   ├── fichas_tecnicas_indicadores_base.md ← Fichas técnicas conceptuales de indicadores base
│   ├── fichas_tecnicas_nuevos_dominios.md  ← Fichas técnicas de los dominios de expansión
│   ├── evaluacion_calidad_datasets_consolidada.md ← Evaluación de calidad DAMA-BOK consolidada
│   ├── matriz_calidad_datos.md             ← Matriz multivariada de calidad de datos
│   ├── matriz_trazabilidad_analitica.md    ← Matriz de trazabilidad requerimiento-indicador-modelo
│   ├── inventario_maestro_indicadores.md   ← Catálogo maestro de indicadores por dimensión
│   ├── dim_territorio.md                   ← Marco de referencia territorial y homologación DIVIPOLA
│   ├── principios_modelo_territorial.md    ← Principios rectores del modelado territorial
│   ├── alcance_supuestos_restricciones.md  ← Alcance, supuestos y restricciones del sistema
│   ├── plantilla_evaluacion_calidad.md     ← Formato estándar de evaluación de calidad de datos
│   └── diagrams/                           ← Diagramas UML de Casos de Uso y Actividad (Mermaid)
│
├── 02-architecture/                        ← FASE PLAN → DEVELOPMENT: Diseño del Sistema
│   ├── README.md                           ← Guía y catálogo de la fase de Arquitectura
│   ├── architecture.md                     ← Documento principal de Arquitectura de Software SAD v1.0.0
│   ├── NOTA_TECNICA_INTEGRACION_DATOS_PUBLICOS.md ← Arquitectura de integración territorial multidominio
│   ├── patterns.md                         ← Catálogo de patrones GoF y GRASP aplicados
│   ├── ADR/                                ← Architecture Decision Records (ADR-001..005)
│   │   ├── ADR-001.md                      ← Arquitectura Modular Hexagonal
│   │   ├── ADR-002.md                      ← Modelo Compuesto IPT y 10 Pasos OCDE/JRC
│   │   ├── ADR-003.md                      ← Sistema de Homologación Territorial Canónica
│   │   ├── ADR-004.md                      ← Bootstrap Dirichlet y Factor de Inflación VIF
│   │   └── ADR-005.md                      ← Estandarización Canónica y pyproject.toml
│   └── diagrams/                           ← Diagramas UML de Clases, Secuencia, Componentes y Comunicación
│
├── 03-development/                         ← FASE DEVELOPMENT: Implementación, Modelado y APIs
│   ├── README.md                           ← Guía y catálogo de la fase de Desarrollo
│   ├── dev-log.md                          ← Bitácora de desarrollo, autoría y trazabilidad Git
│   ├── sistema_visualizacion.md            ← Guía técnica del sistema de visualización Web GIS y GeoJSON
│   ├── manual_calculo_indices_territoriales.md ← Manual técnico de formulación matemática de indicadores
│   ├── formulacion_matematica_ipt.md       ← Formulación matemática y metodológica del IPT v1.0.0
│   ├── api-docs.md                         ← Documentación técnica de módulos y paquetes en src/
│   ├── analisis_exploratorio_nuevos_dominios.md ← Síntesis exploratoria y brechas territoriales
│   └── technical-debt.md                   ← Análisis de deuda técnica y buenas prácticas
│
├── 04-testing/                             ← FASE CONTROL: Aseguramiento de Calidad y Tests
│   ├── README.md                           ← Guía y catálogo de la fase de Pruebas
│   ├── test-plan.md                        ← Plan maestro de pruebas unitarias y de integración
│   └── test-results.md                     ← Reporte formal de ejecución (194/194 tests passed, 100%)
│
└── 05-maintenance/                         ← FASE OPERATIONS: Mantenimiento y Evolución
    ├── README.md                           ← Guía y catálogo de la fase de Mantenimiento
    ├── changelog.md                        ← Registro de cambios y versiones SemVer (v1.3.0)
    ├── refactoring-log.md                  ← Bitácora de optimizaciones y refactorización continua
    └── migration_manifest.md               ← Manifiesto de migración y trazabilidad de datasets
```

---

## 📊 Informes Analíticos, Modelos y Aplicación Web GIS

Adicionalmente, el repositorio incluye los siguientes directorios clave de entrega:

- 🏛️ **Gobernanza de Modelos (`models/`) y Configuración (`config/`)**:
  - `config/ipt_weights.json`: Ponderaciones declarativas de los 5 escenarios de sensibilidad y 7 dimensiones canónicas.
  - `models/model_card.json`: Ficha técnica de gobernanza del modelo IPT (v1.0.0).
  - `models/transformers/minmax_scalers_config.json`: Parámetros de normalización y polaridad por indicador.
- 🗺️ **Aplicación Web GIS Autónoma**: [`reports/dashboard_geografico_sipta.html`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/dashboard_geografico_sipta.html) (Leaflet.js + Chart.js para exploración multicapa de 13 dominios).
- 📑 **Informe Maestro de Auditoría Estadística**: [`reports/00_auditoria_estadistica_formal.md`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/00_auditoria_estadistica_formal.md) (Dictamen cuantitativo OCDE/JRC, VIF, Bootstrap, Moran).
- 📑 **13 Informes Analíticos Sectoriales**: [`reports/domains/`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/domains) con recomendaciones de política pública estructuradas y semáforos de alertas tempranas.
- 📈 **13 Figuras Científicas Multi-Panel**: [`reports/figures/`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/reports/figures) renderizadas a 300 DPI.
- 🗃️ **Capa Espacial Curada**: [`data/curated/sipta_localidades_multidominio.geojson`](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/data/curated/sipta_localidades_multidominio.geojson) bajo estándar RFC 7946 GeoJSON.

---

## 🔗 Navegación Rápida por Fase PDCO

| Fase PDCO | Directorio | Documento Clave | Estándar Aplicado |
| :--- | :--- | :--- | :--- |
| **PLAN** | [`01-requirements/`](01-requirements/README.md) | [`requirements.md`](01-requirements/requirements.md) | IEEE 830 / ISO 29148 / DAMA-BOK |
| **DESIGN** | [`02-architecture/`](02-architecture/README.md) | [`architecture.md`](02-architecture/architecture.md) | SWEBOK Cap. 2 / SOLID / ADR |
| **DEVELOPMENT** | [`03-development/`](03-development/README.md) | [`api-docs.md`](03-development/api-docs.md) | Clean Code / PEP 8 / Type Hints |
| **CONTROL** | [`04-testing/`](04-testing/README.md) | [`test-results.md`](04-testing/test-results.md) | IEEE 829 / ISO 29119 / 194 tests |
| **OPERATIONS** | [`05-maintenance/`](05-maintenance/README.md) | [`changelog.md`](05-maintenance/changelog.md) | SemVer / Keep a Changelog |
