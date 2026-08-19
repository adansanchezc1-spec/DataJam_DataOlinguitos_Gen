# SIPTA — Índice Maestro de Documentación del Proyecto

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Marco de Trabajo**: SDLC / PDCO (Plan, Development, Control, Operations)  
**Estándares**: SWEBOK, DAMA-BOK, IEEE 830 / ISO 29148, ISO/IEC 25010, Clean Code, PEP 8  
**Liderazgo y Autoría**:
- **Persona A**: Adan Sánchez (Scrum Master + Lead Data Engineer / Git Manager)
- **Persona B**: Yesid Bello (Data Scientist / Territorial Analyst)
- **Persona C**: Sofía Hidalgo (Tech Lead & BI Developer / Data Analyst)

---

## 1. Estructura Transversal de Documentación (`docs/`)

```
docs/
├── README.md                                 ← Índice maestro (este documento)
├── 01-requirements/                          ← Fase PLAN (IEEE 830 / ISO 29148)
│   ├── E01_inventario_datos.md               ← Entregable E01: Catálogo exhaustivo de fuentes
│   ├── E02_diccionario_datos.md              ← Entregable E02: Diccionario de datos maestro
│   ├── alcance_supuestos_restricciones.md    ← Límites y supuestos metodológicos
│   ├── dim_territorio.md                     ← Catálogo canónico de las 20 localidades
│   ├── principios_modelo_territorial.md      ← Jerarquía territorial e interoperabilidad
│   ├── matriz_calidad_datos.md               ← Criterios de aceptación ISO 25010
│   ├── matriz_trazabilidad_analitica.md      ← Trazabilidad problema → indicador → decisión
│   ├── inventario_maestro_indicadores.md     ← Catálogo de indicadores sectoriales
│   └── fichas_tecnicas_indicadores_base.md   ← Fichas técnicas (SAL-002, EDU-001, INF-004, etc.)
├── 02-architecture/                          ← Fase PLAN → DEVELOPMENT (SWEBOK)
│   ├── architecture.md                       ← Arquitectura hexagonal y pipeline modular
│   └── patterns.md                           ← Patrones GoF y GRASP aplicados
├── 03-development/                           ← Fase DEVELOPMENT
│   ├── dev-log.md                            ← Registro de desarrollo y commits
│   └── diccionario_datos.md                  ← Diccionario de datos canónico
├── 04-testing/                               ← Fase CONTROL (pytest / coverage)
│   └── test-plan.md                          ← Plan de pruebas unitarias y de validación
└── 05-maintenance/                           ← Fase OPERATIONS
    └── changelog.md                          ← Registro de cambios y refactorización
```

---

## 2. Mapa de Entregables Oficiales (E01 a E11)

| Entregable | Título / Documento | Fase PDCO | Estado | Responsables |
| :--- | :--- | :--- | :--- | :--- |
| **E01** | [Inventario de Datos](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/docs/01-requirements/E01_inventario_datos.md) | PLAN | Completo | Persona A, Persona B & Persona C |
| **E02** | [Diccionario de Datos](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/docs/01-requirements/E02_diccionario_datos.md) | PLAN | Completo | Persona A, Persona B & Persona C |
| **E03** | [Dimensión Territorial](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/docs/01-requirements/dim_territorio.md) | PLAN | Completo | Persona B & Persona A |
| **E04** | [Matriz de Calidad de Datos](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/docs/01-requirements/matriz_calidad_datos.md) | PLAN / CONTROL | Completo | Persona B & Persona A |
| **E05** | [Inventario de Indicadores](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/docs/01-requirements/inventario_maestro_indicadores.md) | PLAN | Completo | Persona A & Persona B |
| **E06** | [Fichas Técnicas de Indicadores](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/docs/01-requirements/fichas_tecnicas_indicadores_base.md) | PLAN | Completo | Persona A & Persona B |
| **E07** | [Matriz de Trazabilidad Analítica](file:///c:/Users/ADAN/DataJam_DataOlinguitos_Gen/docs/01-requirements/matriz_trazabilidad_analitica.md) | PLAN | Completo | Persona B & Persona A |
| **E08** | Arquitectura y Pipeline ETL | DEVELOPMENT | En Progreso | Persona A (Adan) |
| **E09** | Suite de Validación y Reportes | CONTROL | En Progreso | Persona A, Persona B & Persona C |
| **E10** | Cálculo de Índices e IPT | DEVELOPMENT | Diseñado | Persona B (Yesid) |
| **E11** | Visualización y Dashboard | DEVELOPMENT | Diseñado | Persona C (Sofía) & Persona A (Adan) |
