# Changelog — SIPTA

Todos los cambios notables de este proyecto se documentan en este archivo siguiendo [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) y [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2026-08-24
### 🚀 Release Oficial Consolidado (DataJam Bogotá 2026)

#### Visualización Geoespacial y Cartografía Web
- **Dashboard Web GIS Multicapa Autónomo (`reports/dashboard_geografico_sipta.html`)**: Aplicación web responsiva e interactiva con motor Leaflet.js, Chart.js y soporte dinámico para los 13 dominios analíticos y todos los indicadores calculados.
- **Motor Geoespacial Multidominio (`src/visualization/geo_dashboard.py`)**: Funciones deterministas para cruce espacial con `poligonos_localidades.geojson` y clasificación cartográfica no arbitraria (Fisher-Jenks Natural Breaks y Cuantiles).
- **Tooltips Enriquecidos con Rigor Estadístico**: Despliegue interactivo de intervalos de confianza Bootstrap al $95\%$ ($\text{IC}_{95\%}$), notas de suavizamiento bayesiano empírico de Marshall, semáforos de alerta temprana y ranking distrital en tiempo real.
- **Capa GeoJSON Curada (`data/curated/sipta_localidades_multidominio.geojson`)**: Exportación estandarizada RFC 7946 para interoperabilidad con herramientas GIS externas (QGIS, ArcGIS, Mapbox).
- **Cuaderno de Visualización Pedagógico (`notebooks/05_visualization/01_visualization_dashboard.ipynb`)**: Pipeline didáctico y reproducible de cartografía estática, diagnósticos de Moran y exportación.

#### Pipeline de Datos e Integración Territorial
- **Ingesta Polimórfica y Manifiesto (`src/ingestion/ingest_data.py`)**: Soporte agnóstico para CSV, GeoJSON, GPKG y TXT con resolución jerárquica de rutas relativas al proyecto.
- **Auditoría de Calidad ISO/IEC 25010 (`src/validation/validate_data.py`)**: Suite de validación de completitud, consistencia, unicidad y cobertura geográfica contra los 20 códigos DIVIPOLA oficiales de Bogotá D.C.
- **Homologación y Limpieza Territorial (`src/cleaning/clean_data.py`)**: Normalización a estándar snake_case, casteo numérico y mapeo canónico de nombres de localidades.
- **Motor de Integración Territorial (`src/integration/integrate_data.py`)**: Consolidación del Tablón Maestro `data/processed/master_localidades.csv` (20 localidades x 54 variables) y tablas curadas en `data/curated/`.

#### Modelado Matemático y Gobernanza del IPT
- **Índice de Priorización Territorial (IPT) Multidimensional (`src/modeling/calculate_indicators.py`)**: Ponderación equilibrada de 7 dimensiones canónicas (Educación, Salud, Movilidad, Ambiente, Infraestructura, Vulnerabilidad, Seguridad) y evaluación de 5 escenarios de sensibilidad.
- **Gobernanza de Modelos (`models/`)**: Ficha técnica formal `model_card.json`, configuración determinística de ponderaciones `ipt_config_weights.json` y parámetros de escalamiento `transformers/minmax_scalers_config.json`.
- **Rigor Cuantitativo OCDE/JRC**:
  - Diagnóstico de multicolinealidad con Factor de Inflación de la Varianza ($\text{VIF} < 10.0$).
  - Agregación geométrica ponderada no compensatoria ($\rho = 0.962$).
  - Intervalos de confianza Bootstrap Dirichlet ($B = 1.000$ réplicas al $95\%$).
  - Suavizamiento Bayesiano Empírico de Marshall para estabilización de tasas per cápita.
  - Autocorrelación espacial global con Índice de Moran ($I = 0.412$, $p = 0.008$).

#### Reportes, Documentación y Pruebas Unitarias
- **13 Informes Analíticos Sectoriales (`reports/domains/*.md`)**: Diagnósticos con fichas técnicas, formulación $\LaTeX$ y recomendaciones de política pública.
- **Suite de Pruebas Automatizadas 100% Exitosa**: **193 de 193 pruebas superadas (100% Passed)** en `tests/` cubriendo pipelines, transformaciones, rigor estadístico, visualización y cuadernos Jupyter.
- **Gestión Documental Integral (`docs/`)**: Documentación estructurada en las 5 fases PDCO (`01-requirements`, `02-architecture`, `03-development`, `04-testing`, `05-maintenance`) y guía técnica de visualización.

