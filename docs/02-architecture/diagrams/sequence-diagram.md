# Diagrama de Secuencia — Flujo Principal de Ejecución SIPTA
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas  
**Fase PDCO**: DEVELOPMENT | **SDLC Stage**: System Design  
**Marco Normativo**: SWEBOK Cap. 2 (Software Design) / ISO/IEC 25010  

---

```mermaid
sequenceDiagram
    autonumber
    actor Operador as Usuario / Orquestador
    participant Ingestion as IngestionModule (src/ingestion)
    participant Validation as ValidationFacade (src/validation)
    participant Cleaning as CleaningPipeline (src/cleaning)
    participant Integration as TerritorialIntegrator (src/integration)
    participant Modeling as IndicatorModel (src/modeling)
    participant Visualization as DashboardExporter (src/visualization)
    participant Storage as DataStorage (data/ & reports/)

    Operador->>Ingestion: run_full_ingestion()
    Ingestion->>Storage: Descargar & Almacenar en data/raw/
    Storage-->>Ingestion: Archivos raw listos (13 dominios)
    Ingestion-->>Operador: Resumen de Ingesta (25 datasets)

    Operador->>Validation: run_full_validation_suite()
    Validation->>Storage: Leer esquemas, nulos, duplicados & localidades
    Validation->>Validation: Evaluar ISO 25010 (Completitud, Consistencia, Unicidad)
    Validation->>Storage: Exportar reporte_validacion_completo.json
    Validation-->>Operador: ValidationSummary (13 dominios válidos)

    Operador->>Cleaning: clean_and_harmonize_all()
    Cleaning->>Storage: Aplicar Canonical Territorial Mapper (20 Localidades)
    Cleaning->>Storage: Reproyectar capas vectoriales a EPSG:4326 (WGS84)
    Cleaning->>Storage: Guardar data/processed/
    Cleaning-->>Operador: Datasets limpios y homologados

    Operador->>Integration: integrate_all_domains()
    Integration->>Storage: Leer tablas sectoriales procesadas
    Integration->>Integration: Join por ID canónico de Localidad
    Integration->>Storage: Guardar master_localidades.csv & master_localidades.parquet
    Integration-->>Operador: Master Territorial Consolidado (20 filas x 48 col)

    Operador->>Modeling: compute_ipt_model()
    Modeling->>Storage: Leer master_localidades
    Modeling->>Modeling: Normalización Min-Max & Inversión de Polaridad
    Modeling->>Modeling: Cálculo de 24 Indicadores & Ponderación Multidimensional IPT
    Modeling->>Storage: Guardar ipt_localidades_ranking.csv & ipt_localidades_ranking.parquet
    Modeling-->>Operador: Ranking IPT Final y Alertas Tempranas

    Operador->>Visualization: generate_interactive_gis_dashboard()
    Visualization->>Storage: Leer polígonos GeoJSON y tablas curadas
    Visualization->>Visualization: Calcular Fisher-Jenks Natural Breaks y Cuantiles
    Visualization->>Storage: Exportar data/curated/sipta_localidades_multidominio.geojson
    Visualization->>Storage: Compilar reports/dashboard_geografico_sipta.html
    Visualization-->>Operador: Dashboard Web GIS autónomo y Capa GeoJSON listos
```
