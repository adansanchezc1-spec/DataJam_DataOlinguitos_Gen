# Índice Maestro de Reportes Analíticos y de Calidad — SIPTA

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (DataJam Bogotá)  
**Marco de Trabajo**: SDLC / PDCO (Control & Operations)  
**Estándares**: ISO/IEC 25010, DAMA-BOK  
**Responsables**: Persona A (Adan Sánchez), Persona B (Yesid Bello) & Persona C (Sofía Hidalgo)

---

## Estructura del Directorio `reports/`

```
reports/
├── README.md                            ← Guía y catálogo de reportes (este documento)
├── dashboard_geografico_sipta.html      ← Dashboard Web GIS interactivo y autónomo (Leaflet.js + Chart.js)
├── 00_auditoria_estadistica_formal.md   ← Dictamen de auditoría y certificación cuantitativa OCDE/JRC
│
├── domains/                             ← 13 Informes analíticos sectoriales con recomendaciones
│   ├── README.md                        ← Catálogo de reportes sectoriales
│   ├── 00_reporte_ejecutivo_priorizacion_ipt.md
│   ├── 01_reporte_demografia.md
│   ├── 02_reporte_salud.md
│   ├── 03_reporte_educacion.md
│   ├── 04_reporte_movilidad.md
│   ├── 05_reporte_infraestructura.md
│   ├── 06_reporte_ambiente.md
│   ├── 07_reporte_finanzas.md
│   ├── 08_reporte_vulnerabilidad_social.md
│   ├── 09_reporte_seguridad.md
│   ├── 10_reporte_servicios_publicos.md
│   ├── 11_reporte_empleo_economia.md
│   └── 12_reporte_participacion_ciudadana.md
│
├── figures/                             ← 13 Figuras científicas multi-panel a 300 DPI
│   ├── fig_00_priorizacion_territorial_ipt.png
│   ├── fig_01_demografia_densidad_urbana.png
│   └── ... (figuras 02 a 12)
│
├── validation/                          ← Reportes de validación de calidad y territorio
│   ├── reporte_validacion_maestro.md    ← Informe ejecutivo consolidado de calidad
│   ├── matriz_calidad_resumen.csv       ← Métricas de filas, columnas, nulos y duplicados
│   ├── validacion_territorial.csv       ← Cobertura territorial por localidad
│   ├── reporte_validacion_completo.json ← Salida cruda de la suite de validación
│   └── dominios/                        ← JSONs detallados por sector analítico (13 dominios)
│
├── inventory/                           ← Inventarios estructurados
│   ├── inventario_datasets_sipta.csv    ← Catálogo CSV de fuentes y entidades (25 datasets)
│   └── diccionario_indicadores_sipta.csv ← Diccionario técnico estructurado de variables
│
└── eda/                                 ← Reportes exploratorios y perfiles de datos
    ├── conclusiones_eda.md              ← Síntesis de hallazgos exploratorios
    ├── perfil_datos.csv                 ← Perfilado estadístico multivariado
    ├── resumen_indicadores_eda.csv      ← Matriz resumen de indicadores preliminares
    └── matriz_cobertura_localidad.csv   ← Matriz de presencia de datos por localidad
```
