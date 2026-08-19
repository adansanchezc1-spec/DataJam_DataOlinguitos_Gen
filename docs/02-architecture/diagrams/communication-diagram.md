# Diagrama de Comunicación / Colaboración — SIPTA
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas  
**Fase PDCO**: DEVELOPMENT | **SDLC Stage**: System Design  
**Marco Normativo**: SWEBOK Cap. 2 (Software Design)  

---

```mermaid
graph LR
    Orquestador[":PipelineRunner"] -->|1: run_ingest()| Ingesta[":IngestData"]
    Orquestador -->|2: run_validation()| Validador[":ValidateData"]
    Orquestador -->|3: run_cleaning()| Limpiador[":CleanData"]
    Orquestador -->|4: run_integration()| Integrador[":IntegrateData"]
    Orquestador -->|5: calculate_ipt()| Modelador[":CalculateIndicators"]
    Orquestador -->|6: export_viz()| Visualizador[":PrepareVisualization"]

    Ingesta -->|1.1: fetch_raw_data()| RawStore[("(data/raw/)")]
    Validador -->|2.1: audit_iso25010()| RawStore
    Validador -->|2.2: write_reports()| ReportStore[("(reports/validation/)")]
    
    Limpiador -->|3.1: map_canonical_localidades()| RawStore
    Limpiador -->|3.2: save_processed()| ProcessedStore[("(data/processed/)")]
    
    Integrador -->|4.1: merge_by_localidad()| ProcessedStore
    Integrador -->|4.2: save_master_table()| ProcessedStore
    
    Modelador -->|5.1: load_master_localidades()| ProcessedStore
    Modelador -->|5.2: compute_ipt_ranking()| CuratedStore[("(data/curated/)")]
    
    Visualizador -->|6.1: prepare_dashboard_payload()| CuratedStore
    Visualizador -->|6.2: export_geojson_layers()| ReportStore
```
