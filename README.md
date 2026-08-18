SIPTA — Proyecto DataJam Bogotá

Este repositorio contiene el Plan Maestro corregido de SIPTA y la infraestructura básica del proyecto. El proyecto se organiza por sector y por etapas del pipeline de datos.

Documentos principales
- Plan general: [README_SIPTA_Plan_General.md](README_SIPTA_Plan_General.md)
- Salud: [SALUD/README.md](data/raw/SALUD/README.md)
- Educación: [EDUCACION/README.md](data/raw/EDUCACION/README.md)
- Movilidad: [MOVILIDAD/README.md](data/raw/MOVILIDAD/README.md)
- Ambiente: [AMBIENTE/README.md](data/raw/AMBIENTE/README.md)
- Infraestructura y Espacio Público: [INFRAESTRUCTURA_ESPACIO_PUBLICO/README.md](data/raw/INFRAESTRUCTURA_ESPACIO_PUBLICO/README.md)
- Finanzas e Inversión Pública: [FINANZAS_INVERSION_PUBLICA/README.md](data/raw/FINANZAS_INVERSION_PUBLICA/README.md)
- Seguridad: [SEGURIDAD/README.md](data/raw/SEGURIDAD/README.md)
- Participación Ciudadana: [PARTICIPACION_CIUDADANA/README.md](data/raw/PARTICIPACION_CIUDADANA/README.md)

Estructura de carpetas creada
- data/raw
- data/processed
- data/curated
- data/external
- notebooks
- src/ingestion
- src/validation
- src/cleaning
- src/integration
- src/features
- src/modeling
- src/evaluation
- src/visualization
- models
- reports
- docs
- tests
- config
- scripts
- .github
- notebooks/01_ingestion.ipynb
- notebooks/02_validation.ipynb
- notebooks/03_integration.ipynb
- notebooks/04_modeling.ipynb
- notebooks/05_visualization.ipynb
- src/ingestion/ingest_data.py
- src/validation/validate_data.py
- src/cleaning/clean_data.py
- src/integration/integrate_data.py
- src/features/feature_engineering.py
- src/modeling/calculate_indicators.py
- src/evaluation/evaluate_results.py
- src/visualization/prepare_visualization.py
- Flujo de trabajo: [README_WORKFLOW.md](README_WORKFLOW.md)

Objetivo del repositorio
1. Mantener la trazabilidad del plan y los entregables.
2. Separar la documentación sectorial en carpetas autónomas.
3. Soportar la ejecución del pipeline de datos y la integración de indicadores.

Siguientes pasos
- Confirmar la unidad territorial oficial vigente y ajustar el modelo territorial.
- Cargar los datos en data/raw y completar el inventario en E01.
- Registrar los datasets y variables en E02.
- Usar las carpetas src y notebooks para implementar el pipeline.

-- Fin del README raíz --
