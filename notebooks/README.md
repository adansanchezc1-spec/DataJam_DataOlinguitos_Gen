# Catálogo Maestro de Notebooks SIPTA

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Marco Metodológico**: SDLC / PDCO (Plan, Development, Control, Operations)  
**Estándares**: SWEBOK, DAMA-BOK, ISO/IEC 25010, Clean Code, PEP 8  
**Autoría y Roles**:
- **Persona A**: Adan Sánchez (Scrum Master & Lead Data Engineer / Git Manager)
- **Persona B**: Yesid Bello (Data Scientist & Territorial Analyst)
- **Persona C**: Sofía Hidalgo (Tech Lead & BI Developer / Data Analyst)

---

## Estructura de Notebooks por Fase del Ciclo de Vida

```
notebooks/
├── README.md                           ← Catálogo e índice de ejecución (este documento)
│
├── 01_ingestion/                       ← Ingesta + Análisis Exploratorio de Datos (EDA)
│   ├── 00_ingestion_eda_master.ipynb   ← Consolidado Multi-Sectorial y Brechas (Persona A, B & C)
│   ├── 01_ingestion_demografia.ipynb   ← Ingesta + EDA Demografía (Persona A & B)
│   ├── 02_ingestion_salud.ipynb        ← Ingesta + EDA Salud (Persona B - Yesid)
│   ├── 03_ingestion_educacion.ipynb    ← Ingesta + EDA Educación (Persona B - Yesid)
│   ├── 04_ingestion_movilidad.ipynb    ← Ingesta + EDA Movilidad (Persona A - Adan)
│   ├── 05_ingestion_infraestructura.ipynb ← Ingesta + EDA Infraestructura (Persona A - Adan)
│   ├── 06_ingestion_finanzas.ipynb     ← Ingesta + EDA Finanzas e Inversión (Persona C - Sofía)
│   ├── 07_ingestion_ambiental.ipynb    ← Ingesta + EDA Ambiente (Persona C - Sofía)
│   ├── 08_ingestion_seguridad.ipynb    ← Ingesta + EDA Seguridad (Persona C - Sofía)
│   ├── 09_ingestion_servicios_publicos.ipynb ← Ingesta + EDA Servicios Públicos (Persona A & B)
│   ├── 10_ingestion_empleo_economia.ipynb ← Ingesta + EDA Mercado Laboral y Salarios (Persona B & A)
│   └── 11_ingestion_participacion_pqr.ipynb ← Ingesta + EDA Participación y PQR (Persona A & B)
│
├── 02_validation/                      ← Validación de Calidad, Esquemas y Territorio (ISO 25010)
│   ├── 00_validation_master.ipynb      ← Validación Consolidada Distrital (Persona A, B & C)
│   ├── 01_validation_demografia.ipynb  ← Validación Demografía (Persona A & B)
│   ├── 02_validation_salud.ipynb       ← Validación Salud (Persona B - Yesid)
│   ├── 03_validation_educacion.ipynb   ← Validación Educación (Persona B - Yesid)
│   ├── 04_validation_movilidad.ipynb   ← Validación Movilidad (Persona A - Adan)
│   ├── 05_validation_infraestructura.ipynb ← Validación Infraestructura (Persona A - Adan)
│   ├── 06_validation_finanzas.ipynb    ← Validación Finanzas (Persona C - Sofía & Persona A - Adan)
│   ├── 07_validation_ambiental.ipynb   ← Validación Ambiente (Persona C - Sofía & Persona A - Adan)
│   └── 08_validation_seguridad.ipynb   ← Validación Seguridad (Persona C - Sofía & Persona A - Adan)
│
├── 03_integration/                     ← Integración Territorial
│   └── 01_integration_master.ipynb     ← Construcción de la Tabla Maestra (Persona A & B)
│
├── 04_modeling/                        ← Cálculo de Indicadores e IPT (vínculo con models/)
│   ├── 01_modeling_ipt.ipynb           ← Normalización y Ponderación IPT Multidimensional (Persona B - Yesid)
│   └── 02_diccionario_indicadores_ipt.ipynb ← Catálogo Formal de Indicadores y Gobernanza DAMA-BOK (Persona B & A)
│
└── 05_visualization/                   ← Tableros y Salidas Visuales
    └── 01_visualization_dashboard.ipynb ← Preparación de Visualizaciones (Persona C - Sofía & Persona A - Adan)
```

---

## Matriz de Trazabilidad de Notebooks y Autoría

| Carpeta | Notebook | Sector | Fase PDCO | Autoría y Responsabilidad Principal |
| :--- | :--- | :--- | :--- | :--- |
| `01_ingestion/` | `00_ingestion_eda_master.ipynb` | Consolidado | DEVELOPMENT | **Persona A (Adan Sánchez — Lead Data Engineer)** / Insumos: Persona B & Persona C |
| `01_ingestion/` | `01_ingestion_demografia.ipynb` | Demografía | DEVELOPMENT | **Persona A (Adan Sánchez — Autor de EDA)** |
| `01_ingestion/` | `02_ingestion_salud.ipynb` | Salud | DEVELOPMENT | **Persona A (Adan Sánchez — Análisis Exploratorio / EDA)** / Fuentes: Persona B (Yesid) |
| `01_ingestion/` | `03_ingestion_educacion.ipynb` | Educación | DEVELOPMENT | **Persona A (Adan Sánchez — Análisis Exploratorio / EDA)** / Fuentes: Persona B (Yesid) |
| `01_ingestion/` | `04_ingestion_movilidad.ipynb` | Movilidad | DEVELOPMENT | **Persona A (Adan Sánchez — Lead Data Engineer & Autor de EDA)** |
| `01_ingestion/` | `05_ingestion_infraestructura.ipynb` | Infraestructura | DEVELOPMENT | **Persona A (Adan Sánchez — Lead Data Engineer & Autor de EDA)** |
| `01_ingestion/` | `06_ingestion_finanzas.ipynb` | Finanzas / RIVI | DEVELOPMENT | **Persona C (Sofía Hidalgo — Ingesta & EDA)** / Colaboración: Persona A (Adan) |
| `01_ingestion/` | `07_ingestion_ambiental.ipynb` | Ambiente | DEVELOPMENT | **Persona C (Sofía Hidalgo — Ingesta & EDA)** / Colaboración: Persona A (Adan) |
| `01_ingestion/` | `08_ingestion_seguridad.ipynb` | Seguridad | DEVELOPMENT | **Persona C (Sofía Hidalgo — Ingesta & EDA)** / Colaboración: Persona A (Adan) |
| `01_ingestion/` | `09_ingestion_servicios_publicos.ipynb` | Servicios Públicos | DEVELOPMENT | **Persona A (Adan Sánchez)** & **Persona B (Yesid Bello)** |
| `01_ingestion/` | `10_ingestion_empleo_economia.ipynb` | Empleo & Salarios | DEVELOPMENT | **Persona B (Yesid Bello)** & **Persona A (Adan Sánchez)** |
| `01_ingestion/` | `11_ingestion_participacion_pqr.ipynb` | Participación & PQR | DEVELOPMENT | **Persona A (Adan Sánchez)** & **Persona B (Yesid Bello)** |
| `02_validation/`| `00_validation_master.ipynb` | Consolidado | CONTROL | Persona A, Persona B & Persona C |
| `02_validation/`| `01_validation_demografia.ipynb` | Demografía | CONTROL | Persona A & Persona B |
| `02_validation/`| `02_validation_salud.ipynb` | Salud | CONTROL | Persona B (Yesid Bello) |
| `02_validation/`| `03_validation_educacion.ipynb` | Educación | CONTROL | Persona B (Yesid Bello) |
| `02_validation/`| `04_validation_movilidad.ipynb` | Movilidad | CONTROL | Persona A (Adan Sánchez) |
| `02_validation/`| `05_validation_infraestructura.ipynb` | Infraestructura | CONTROL | Persona A (Adan Sánchez) |
| `02_validation/`| `06_validation_finanzas.ipynb` | Finanzas | CONTROL | Persona C (Sofía Hidalgo) & Persona A (Adan Sánchez) |
| `02_validation/`| `07_validation_ambiental.ipynb` | Ambiente | CONTROL | Persona C (Sofía Hidalgo) & Persona A (Adan Sánchez) |
| `02_validation/`| `08_validation_seguridad.ipynb` | Seguridad | CONTROL | Persona C (Sofía Hidalgo) & Persona A (Adan Sánchez) |
| `03_integration/`| `01_integration_master.ipynb` | Integración | DEVELOPMENT | Persona A & Persona B |
| `04_modeling/`  | `01_modeling_ipt.ipynb` | Indicadores IPT | DEVELOPMENT | Persona B (Yesid Bello) |
| `04_modeling/`  | `02_diccionario_indicadores_ipt.ipynb` | Diccionario IPT | DEVELOPMENT | Persona B (Yesid Bello) & Persona A (Adan Sánchez) |
| `05_visualization/`| `01_visualization_dashboard.ipynb` | Dashboard | DEVELOPMENT | Persona C (Sofía Hidalgo) & Persona A (Adan Sánchez) |

