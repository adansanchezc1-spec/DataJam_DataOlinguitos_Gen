# Documentación Técnica de APIs y Módulos — SIPTA

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas  
**Fase PDCO**: DEVELOPMENT | **Estándares**: PEP 8, Type Hints, Clean Code  

---

## 1. Módulo `src.validation.validate_data`
- `inspect_schema(df: pd.DataFrame) -> pd.DataFrame`: Inspecciona nulos, duplicados, tipos y cardinalidad de columnas.
- `detect_territorial_columns(df: pd.DataFrame) -> list[str]`: Detección automática de columnas territoriales.
- `validate_territorial_column(df: pd.DataFrame, column_name: str) -> dict`: Valida cobertura frente a las 20 localidades oficiales.
- `validate_dataset_quality(df: pd.DataFrame, dataset_name: str) -> dict`: Evaluación integral ISO 25010.
- `run_full_validation_suite() -> dict`: Ejecuta la validación de los 13 dominios y genera el reporte maestro.

---

## 2. Módulo `src.modeling.calculate_indicators`
- `normalize_min_max(series: pd.Series, invert: bool = False) -> pd.Series`: Escalamiento lineal a rango [0, 1].
- `build_consolidated_locality_metrics() -> pd.DataFrame`: Integra las 20 localidades con métricas multidimensionales.
- `calculate_multidimensional_ipt(df: pd.DataFrame) -> pd.DataFrame`: Calcula el Índice de Prioridad Territorial ponderado (0-100) y asigna ranking y nivel de alerta.
