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
├── validation/                          ← Reportes de validación de calidad y territorio
│   ├── reporte_validacion_maestro.md    ← Informe ejecutivo consolidado de calidad
│   ├── matriz_calidad_resumen.csv       ← Métricas de filas, columnas, nulos y duplicados
│   ├── validacion_territorial.csv       ← Cobertura territorial por localidad
│   ├── reporte_validacion_completo.json ← Salida cruda de la suite de validación
│   └── dominios/                        ← JSONs detallados por sector analítico (13 dominios)
│       ├── val_demografia.json
│       ├── val_salud.json
│       ├── val_educacion.json
│       ├── val_movilidad.json
│       ├── val_infraestructura.json
│       ├── val_finanzas.json
│       ├── val_inversion_fdl.json
│       ├── val_servicios_publicos.json
│       ├── val_empleo_economia.json
│       ├── val_participacion_ciudadana.json
│       ├── val_modelo_territorial.json
│       ├── val_ambiente.json
│       └── val_seguridad.json
├── inventory/                           ← Inventarios estructurados
│   └── inventario_datasets_sipta.csv    ← Catálogo CSV de fuentes y entidades (25 datasets)
└── eda/                                 ← Reportes exploratorios y perfiles de datos
    ├── conclusiones_eda.md              ← Síntesis de hallazgos exploratorios
    ├── perfil_datos.csv                 ← Perfilado estadístico multivariado
    ├── resumen_indicadores_eda.csv      ← Matriz resumen de indicadores preliminares
    ├── matriz_cobertura_localidad.csv   ← Matriz de presencia de datos por localidad
    └── perfiles/                        ← Perfiles específicos por dataset
```
