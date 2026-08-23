# Módulos y Paquetes del Sistema — `src/`

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA)  
**Marco de Trabajo**: Hexagonal / Pipeline Modular (PDCO: DEVELOPMENT)  
**Estándares**: SWEBOK Cap. 2 y 3, Clean Code, PEP 8, Type Hints  

---

## 🏛️ Estructura del Código Fuente

```
src/
├── README.md               ← Guía y catálogo del código fuente (este documento)
│
├── ingestion/              ← Ingesta de datos polimórfica (CSV, XLSX, GPKG, GeoJSON, ZIP)
│   └── ingest_data.py      ← Motor de ingesta y generación de ingestion_manifest.json
│
├── validation/             ← Validación de esquemas, calidad multivariada y reglas territoriales
│   └── validate_data.py    ← Suite de validación ISO 25010 contra 20 localidades D.C.
│
├── cleaning/               ← Limpieza, normalización y homologación geográfica
│   └── clean_data.py       ← Mapeo canónico DIVIPOLA (1100101 a 1100120) y tipado estricto
│
├── integration/            ← Motor de integración territorial y agregaciones
│   └── integrate_data.py   ← Construcción del Tablón Maestro (data/processed/master_localidades.csv)
│
├── features/               ← Feature Engineering territorial
│   └── feature_engineering.py ← Cálculo de densidades, ratios y variables per cápita
│
├── modeling/               ← Motor de indicadores sectoriales y modelado IPT
│   ├── calculate_indicators.py ← Normalización Min-Max e IPT compuesto (7 dimensiones)
│   └── domain_indicators.py   ← Generador modular de 12 tablas maestras curadas por dominio
│
├── evaluation/             ← Diagnóstico de calidad y reporte de nulos
│   └── evaluate_results.py ← Detección de outliers y quality_report
│
└── visualization/          ← Preparación de datos y rankings para tableros
    └── prepare_visualization.py ← Serialización curada para visualizaciones y dashboards
```

---

## ⚙️ Principios de Arquitectura y Buenas Prácticas

1. **Resolución Agnóstica de Rutas**: Ningún módulo usa rutas absolutas `C:/...`; todos resuelven `ROOT = Path(__file__).resolve().parents[2]`.
2. **SOLID & Alta Cohesión**: Cada paquete tiene una responsabilidad única (SRP) y expone contratos tipados.
3. **Persistencia Estructurada**:
   - `data/raw/`: Fuentes crudas inmutables.
   - `data/processed/`: Tablones intermedios y maestro consolidado.
   - `data/curated/`: Tablas temáticas por dominio y salidas de modelado listas para consumo.
