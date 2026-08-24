# Documentación Técnica de APIs y Módulos — SIPTA (v2.6.0)

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA)  
**Versión**: 2.6.0  
**Fase PDCO**: DEVELOPMENT | **Estándares**: Clean Code, PEP 8, Type Hints, DAMA-BOK  
**Autores**: Senior Software Engineer & Data Scientist Agent, Chief Statistical Reviewer Agent  

---

## 1. Módulo `src.modeling.calculate_indicators`

Motor central de cálculo matemático del Índice de Priorización Territorial (IPT), normalizaciones y pruebas de rigor estadístico.

### Funciones Principales:

#### `normalize_min_max(series: pd.Series) -> pd.Series`
- **Descripción**: Escala linealmente una serie numérica al intervalo unitario $[0, 1]$. Maneja vectores constantes asignando $0.5$.
- **Fórmula**: $\hat{x} = \frac{x - \min(X)}{\max(X) - \min(X)}$.

#### `build_consolidated_locality_metrics(source: pd.DataFrame | str | Path | None = None) -> pd.DataFrame`
- **Descripción**: Carga y estructura la matriz territorial consolidada para las 20 localidades oficiales de Bogotá D.C., asegurando la consistencia dimensional sin inventar registros.

#### `calculate_multidimensional_ipt(df: pd.DataFrame) -> pd.DataFrame`
- **Descripción**: Ejecuta el cálculo de los 5 escenarios metodológicos del IPT (`ipt_base`, `ipt_rangos`, `ipt_sin_proxy`, `ipt_sin_rivi`, `ipt_sin_proxy_ni_rivi`), calcula el ranking de consenso y asigna los niveles de prioridad y confianza analítica.

#### `calculate_vif_scores(df: pd.DataFrame, dimension_cols: list[str] | None = None) -> pd.DataFrame`
- **Descripción**: Calcula el Factor de Inflación de la Varianza ($\text{VIF}_j$) para diagnosticar multicolinealidad interdimensional.
- **Fórmula**: $\text{VIF}_j = \frac{1}{1 - R_j^2}$.

#### `calculate_geometric_ipt(df_metrics: pd.DataFrame, dimension_cols: list[str] | None = None, weights: list[float] | None = None, epsilon: float = 0.01) -> pd.Series`
- **Descripción**: Implementa la agregación geométrica ponderada no compensatoria (Estándar OCDE/JRC).
- **Fórmula**: $\text{IPT}_{\text{Geom}} = 100 \times \left( \prod (s_{i, d} + \epsilon)^{w_d} \right) - 100\epsilon$.

#### `calculate_bootstrap_confidence_intervals(df_metrics: pd.DataFrame, dimension_cols: list[str] | None = None, n_bootstraps: int = 1000, alpha: float = 0.05, random_state: int = 42) -> pd.DataFrame`
- **Descripción**: Estima intervalos de confianza empíricos al $95\%$ mediante remuestreo Monte Carlo sobre ponderaciones Dirichlet $\text{Dir}(\mathbf{1})$.

#### `calculate_empirical_bayes_smoothing(events: pd.Series, population: pd.Series, scale_factor: float = 10000.0) -> pd.Series`
- **Descripción**: Aplica el estimador de Marshall (*Empirical Bayes Rate Smoother*) para estabilizar tasas per cápita en localidades con baja población (La Candelaria, Sumapaz).

#### `calculate_spatial_moran(values: pd.Series, locality_codes: pd.Series | None = None, adjacency_matrix: np.ndarray | None = None, n_permutations: int = 999, random_state: int = 42) -> tuple[float, float]`
- **Descripción**: Calcula el Índice de Moran Global ($I$) y su $p$-valor por permutaciones espaciales con matriz de contigüidad Reina oficial de Bogotá.

---

## 2. Módulo `src.modeling.domain_indicators`

Generador de las 12 tablas maestras curadas por sector administrativo.

### Funciones Principales:
- `build_all_domain_tables(export_curated: bool = True) -> dict[str, pd.DataFrame]`: Genera y exporta las 12 tablas maestras curadas en `data/curated/master_<dominio>.csv`.
- `load_unified_territorial_source() -> pd.DataFrame`: Carga el tablón maestro integrado con validación de 20 localidades.

---

## 3. Módulo `src.validation.validate_data`

Validación de calidad de datos bajo la norma **ISO/IEC 25010**.

### Funciones Principales:
- `inspect_schema(df: pd.DataFrame) -> pd.DataFrame`: Reporta completitud, tipos de datos, duplicados y cardinalidad.
- `detect_territorial_columns(df: pd.DataFrame) -> list[str]`: Identifica columnas con potencial información geográfica.
- `validate_territorial_column(df: pd.DataFrame, column_name: str) -> dict[str, Any]`: Valida cobertura frente a los 20 códigos DIVIPOLA oficiales.
- `run_full_validation_suite() -> dict[str, Any]`: Ejecuta la validación masiva sobre los datasets y exporta reportes en `reports/validation/`.

---

## 4. Módulo `src.cleaning.spatial_cleaning` & `src.integration`

- `clean_locality_names(series: pd.Series) -> pd.Series`: Homologa nombres a los 20 identificadores canónicos oficiales.
- `perform_spatial_join(points_gdf, polygons_gdf) -> gpd.GeoDataFrame`: Ejecuta cruces *Point-in-Polygon* en WGS84 (EPSG:4326).
- `build_master_territorial_table() -> pd.DataFrame`: Integra las variables sectoriales en `data/processed/master_localidades.csv`.
