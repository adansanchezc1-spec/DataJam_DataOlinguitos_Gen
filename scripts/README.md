# Scripts Operacionales y Herramientas de Automatización SIPTA

Este directorio contiene los **scripts de soporte operacional, generación de reportes y mantenimiento del pipeline** del Sistema de Integración y Priorización Territorial de Bogotá (SIPTA).

---

## 🛠️ Catálogo de Scripts Oficiales

| Script | Descripción | Uso / Comando |
| :--- | :--- | :--- |
| [`generate_domain_reports.py`](generate_domain_reports.py) | **Generador Automatizado de Reportes**: Compila los 13 reportes sectoriales detallados en Markdown y genera figuras cartográficas y estadísticas en alta resolución (300 DPI) en `reports/figures/`. | `python scripts/generate_domain_reports.py` |
| [`update_catalogs_and_status.py`](update_catalogs_and_status.py) | **Sincronizador de Catálogos y Estado**: Actualiza `data/status/source_catalog.csv`, `data/status/approved_sources.csv`, `data/processed/ingestion_manifest.json` e inventarios documentales. | `python scripts/update_catalogs_and_status.py` |
| [`recalculate_ipt_model.py`](recalculate_ipt_model.py) | **Motor de Modelado IPT**: Recalcula los 5 escenarios de sensibilidad del IPT, intervalos de confianza Bootstrap Dirichlet al 95% y actualiza los tablones curados. | `python scripts/recalculate_ipt_model.py` |
| [`download_missing_data.py`](download_missing_data.py) | **Gestor de Descarga de Datos**: Automatiza la descarga y verificación de integridad de fuentes de datos abiertas distritales (Datos Abiertos Bogotá, IDECA, SaluData). | `python scripts/download_missing_data.py` |
| [`prepare_education_geojson.py`](prepare_education_geojson.py) | **Procesador Geoespacial**: Homologa y reproyecta capas vectoriales de oferta educativa SED a coordenadas WGS84 (EPSG:4326). | `python scripts/prepare_education_geojson.py` |

---

## 📋 Estándares de Ejecución
- Todos los scripts operan de forma no destructiva sobre las carpetas canónicas `data/raw/`, `data/processed/`, `data/curated/` y `reports/`.
- La ejecución se realiza desde la raíz del repositorio con el entorno virtual activado.
