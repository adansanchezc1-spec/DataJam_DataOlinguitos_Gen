"""Módulo de cálculo de indicadores y modelado para SIPTA.

Fase PDCO: DEVELOPMENT
Estándares: Clean Code, PEP 8, DAMA-BOK
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

# Resolución correcta a la raíz del repositorio
ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
CURATED_DIR = ROOT / "data" / "curated"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CURATED_DIR.mkdir(parents=True, exist_ok=True)


def normalize_min_max(series: pd.Series) -> pd.Series:
    """Normaliza una serie numérica al intervalo [0, 1]."""
    s_clean = pd.to_numeric(series, errors="coerce").fillna(0)
    s_min = s_clean.min()
    s_max = s_clean.max()
    if s_max == s_min:
        return pd.Series(0.5, index=series.index)
    return (s_clean - s_min) / (s_max - s_min)


def camas_por_10000(
    df: pd.DataFrame, camas_col: str = "camas", pop_col: str = "poblacion"
) -> pd.Series:
    """Calcula indicador SAL-002: Camas hospitalarias por 10.000 habitantes."""
    if camas_col not in df.columns or pop_col not in df.columns:
        raise KeyError("Columnas necesarias no encontradas en el DataFrame")
    camas = pd.to_numeric(df[camas_col], errors="coerce").fillna(0)
    pop = pd.to_numeric(df[pop_col], errors="coerce").replace(0, pd.NA)
    return (camas / pop) * 10000.0


def cupos_por_1000(
    df: pd.DataFrame, cupos_col: str = "cupos", pop_obj_col: str = "poblacion_objetivo"
) -> pd.Series:
    """Calcula indicador EDU-001: Cupos escolares por 1.000 personas en edad escolar."""
    if cupos_col not in df.columns or pop_obj_col not in df.columns:
        raise KeyError("Columnas necesarias no encontradas en el DataFrame")
    cupos = pd.to_numeric(df[cupos_col], errors="coerce").fillna(0)
    pop_obj = pd.to_numeric(df[pop_obj_col], errors="coerce").replace(0, pd.NA)
    return (cupos / pop_obj) * 1000.0


def build_ipt(
    df: pd.DataFrame,
    component_cols: dict[str, str],
    weights: dict[str, float] | None = None,
) -> pd.Series:
    """Construye el Índice de Prioridad Territorial (IPT) compuesto normalizado [0, 100]."""
    normalized_dict: dict[str, pd.Series] = {}
    for name, col in component_cols.items():
        if col in df.columns:
            normalized_dict[name] = normalize_min_max(df[col])

    norm_df = pd.DataFrame(normalized_dict)
    if norm_df.empty:
        return pd.Series(0.0, index=df.index)

    if weights:
        w_series = pd.Series(weights)
        w_norm = w_series / w_series.sum()
        ipt = norm_df.dot(w_norm) * 100.0
    else:
        ipt = norm_df.mean(axis=1) * 100.0

    return ipt


DIMENSION_COLUMNS = (
    "dim_educacion",
    "dim_salud",
    "dim_movilidad",
    "dim_ambiente",
    "dim_infraestructura",
    "dim_vulnerabilidad",
    "dim_seguridad",
)


def build_consolidated_locality_metrics(
    source: pd.DataFrame | str | Path | None = None,
) -> pd.DataFrame:
    """Carga y valida la matriz territorial consolidada del IPT.

    Si ``source`` no se proporciona, se utiliza la tabla curada generada
    por el notebook de modelado. La función no inventa observaciones,
    valores faltantes ni ponderaciones.
    """

    if source is None:
        source = (
            ROOT
            / "data"
            / "curated"
            / "ipt_modelo_localidad.csv"
        )

    if isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        source_path = Path(source)

        if not source_path.exists():
            raise FileNotFoundError(
                f"No existe la matriz territorial: {source_path}"
            )

        df = pd.read_csv(
            source_path,
            encoding="utf-8-sig",
            dtype={"codigo_localidad": "string"},
        )

    required_columns = {
        "codigo_localidad",
        "localidad",
        *DIMENSION_COLUMNS,
    }

    missing_columns = sorted(
        required_columns.difference(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "La matriz territorial no contiene las columnas "
            f"requeridas: {missing_columns}"
        )

    df["codigo_localidad"] = (
        df["codigo_localidad"]
        .astype("string")
        .str.zfill(2)
    )

    if len(df) != 20:
        raise ValueError(
            "La matriz territorial debe contener exactamente "
            f"20 localidades; se encontraron {len(df)}."
        )

    if df["codigo_localidad"].duplicated().any():
        duplicated_codes = (
            df.loc[
                df["codigo_localidad"].duplicated(
                    keep=False
                ),
                "codigo_localidad",
            ]
            .tolist()
        )

        raise ValueError(
            "Existen códigos de localidad duplicados: "
            f"{duplicated_codes}"
        )

    dimension_values = df[
        list(DIMENSION_COLUMNS)
    ].apply(
        pd.to_numeric,
        errors="coerce",
    )

    if dimension_values.isna().any().any():
        columns_with_missing = (
            dimension_values
            .columns[
                dimension_values.isna().any()
            ]
            .tolist()
        )

        raise ValueError(
            "Las dimensiones contienen valores faltantes o "
            f"no numéricos: {columns_with_missing}"
        )

    outside_interval = (
        dimension_values.lt(0)
        | dimension_values.gt(1)
    )

    if outside_interval.any().any():
        invalid_columns = (
            outside_interval
            .columns[
                outside_interval.any()
            ]
            .tolist()
        )

        raise ValueError(
            "Las dimensiones deben estar normalizadas entre "
            f"0 y 1: {invalid_columns}"
        )

    df.loc[:, list(DIMENSION_COLUMNS)] = (
        dimension_values
    )

    return df


def calculate_multidimensional_ipt(
    df_metrics: pd.DataFrame,
    dimension_cols: list[str] | tuple[str, ...] | None = None,
) -> pd.DataFrame:
    """Calcula el IPT base usando pesos iguales por dimensión.

    Un valor alto representa una mayor prioridad territorial.
    No se aplican imputaciones ni ponderaciones arbitrarias.
    """

    df = df_metrics.copy()

    columns = list(
        dimension_cols
        if dimension_cols is not None
        else DIMENSION_COLUMNS
    )

    missing_columns = sorted(
        set(columns).difference(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "No están disponibles todas las dimensiones: "
            f"{missing_columns}"
        )

    dimension_values = df[columns].apply(
        pd.to_numeric,
        errors="coerce",
    )

    if dimension_values.isna().any().any():
        raise ValueError(
            "No se puede calcular el IPT con dimensiones "
            "faltantes o no numéricas."
        )

    outside_interval = (
        dimension_values.lt(0)
        | dimension_values.gt(1)
    )

    if outside_interval.any().any():
        raise ValueError(
            "Todas las dimensiones deben estar entre 0 y 1."
        )

    # Pesos iguales: 1 / número de dimensiones.
    df["IPT_MULTIDIMENSIONAL"] = (
        dimension_values
        .mean(axis=1)
        .mul(100)
    )

    order = (
        df.sort_values(
            [
                "IPT_MULTIDIMENSIONAL",
                "codigo_localidad",
            ],
            ascending=[False, True],
            kind="mergesort",
        )
        .index
    )

    unique_ranking = pd.Series(
        range(1, len(order) + 1),
        index=order,
        dtype="int64",
    )

    df["RANKING_PRIORIDAD"] = (
        unique_ranking
        .reindex(df.index)
        .astype(int)
    )

    def classify_base_priority(ranking: int) -> str:
        if ranking <= 5:
            return "Alta"
        if ranking <= 10:
            return "Media-alta"
        if ranking <= 15:
            return "Media"
        return "Baja"

    df["NIVEL_PRIORIDAD"] = (
        df["RANKING_PRIORIDAD"]
        .apply(classify_base_priority)
    )

    return df


def calculate_ipt_sensitivity_scenarios(
    df_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """Calcula los 5 escenarios de sensibilidad y robustez metodológica del IPT.

    Escenario 1 (Base Lineal 7D): Promedio simple de las 7 dimensiones canónicas.
    Escenario 2 (Rangos Percentiles 7D): Transformación de rangos no paramétricos (rank-1)/19.
    Escenario 3 (Sin Proxy Parques 6D): Excluye dimensión de Infraestructura.
    Escenario 4 (Sin RIVI 6D): Excluye dimensión de Vulnerabilidad informal.
    Escenario 5 (Cinco Dimensiones Duras 5D): Excluye Infraestructura y Vulnerabilidad.
    """
    df = df_metrics.copy()
    dims_all = [
        "dim_educacion", "dim_salud", "dim_movilidad", "dim_ambiente",
        "dim_infraestructura", "dim_vulnerabilidad", "dim_seguridad"
    ]
    missing = [c for c in dims_all if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan dimensiones requeridas para escenarios de sensibilidad: {missing}")

    # 1. Escenario 1: Base Lineal (7 dimensiones)
    df["IPT_ESCENARIO_1_BASE"] = df[dims_all].mean(axis=1) * 100.0

    # 2. Escenario 2: Rangos No Paramétricos (Percentiles)
    rank_pcts = pd.DataFrame(index=df.index)
    for col in dims_all:
        rank_pcts[col] = (df[col].rank(ascending=True, method="average") - 1.0) / 19.0
    df["IPT_ESCENARIO_2_RANGOS"] = rank_pcts.mean(axis=1) * 100.0

    # 3. Escenario 3: Sin Proxy Parques (6 dimensiones)
    dims_sin_parques = [
        "dim_educacion",
        "dim_salud",
        "dim_movilidad",
        "dim_ambiente",
        "dim_vulnerabilidad",
        "dim_seguridad",
    ]
    df["IPT_ESCENARIO_3_SIN_PARQUES"] = df[dims_sin_parques].mean(axis=1) * 100.0

    # 4. Escenario 4: Sin RIVI (6 dimensiones)
    dims_sin_rivi = [
        "dim_educacion",
        "dim_salud",
        "dim_movilidad",
        "dim_ambiente",
        "dim_infraestructura",
        "dim_seguridad",
    ]
    df["IPT_ESCENARIO_4_SIN_RIVI"] = df[dims_sin_rivi].mean(axis=1) * 100.0

    # 5. Escenario 5: Cinco Dimensiones Duras (5 dimensiones)
    dims_duras = [
        "dim_educacion",
        "dim_salud",
        "dim_movilidad",
        "dim_ambiente",
        "dim_seguridad",
    ]
    df["IPT_ESCENARIO_5_DURAS"] = df[dims_duras].mean(axis=1) * 100.0

    # Asignación determinista y sin empates de rankings [1..20] por escenario
    scenario_tuples = [
        (1, "IPT_ESCENARIO_1_BASE"),
        (2, "IPT_ESCENARIO_2_RANGOS"),
        (3, "IPT_ESCENARIO_3_SIN_PARQUES"),
        (4, "IPT_ESCENARIO_4_SIN_RIVI"),
        (5, "IPT_ESCENARIO_5_DURAS"),
    ]
    for esc_num, esc_col in scenario_tuples:
        order = df.sort_values(
            [esc_col, "codigo_localidad"],
            ascending=[False, True],
            kind="mergesort",
        ).index
        df[f"RANKING_ESC_{esc_num}"] = (
            pd.Series(range(1, len(order) + 1), index=order, dtype="int64")
            .reindex(df.index)
            .astype(int)
        )

    # Consenso entre los 5 escenarios
    rank_cols = [
        "RANKING_ESC_1",
        "RANKING_ESC_2",
        "RANKING_ESC_3",
        "RANKING_ESC_4",
        "RANKING_ESC_5",
    ]
    df["ranking_promedio_5_escenarios"] = df[rank_cols].mean(axis=1)
    df["apariciones_top5_escenarios"] = (df[rank_cols] <= 5).sum(axis=1)

    consensus_order = df.sort_values(
        [
            "ranking_promedio_5_escenarios",
            "IPT_ESCENARIO_1_BASE",
            "codigo_localidad",
        ],
        ascending=[True, False, True],
        kind="mergesort",
    ).index

    df["RANKING_CONSENSO_ESCENARIOS"] = (
        pd.Series(
            range(1, len(consensus_order) + 1),
            index=consensus_order,
            dtype="int64",
        )
        .reindex(df.index)
        .astype(int)
    )

    return df



def calculate_consensus_priority(
    df_metrics: pd.DataFrame,
    ranking_cols: list[str] | tuple[str, ...] | None = None,
) -> pd.DataFrame:
    """Calcula prioridad y confianza a partir de los escenarios.

    El desempate utiliza primero el IPT base y después el código
    de localidad, garantizando un orden único y reproducible.
    """

    df = df_metrics.copy()

    if ranking_cols is None:
        ranking_cols = [
            column
            for column in df.columns
            if column.startswith("ranking_ipt_")
        ]

    ranking_cols = list(ranking_cols)

    if len(ranking_cols) < 2:
        raise ValueError(
            "Se requieren por lo menos dos escenarios de ranking."
        )

    missing_columns = sorted(
        set(ranking_cols).difference(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "No se encontraron los rankings de escenarios: "
            f"{missing_columns}"
        )

    if len(df) != 20:
        raise ValueError(
            "La priorización de consenso requiere "
            "exactamente 20 localidades."
        )

    ranking_values = df[ranking_cols].apply(
        pd.to_numeric,
        errors="coerce",
    )

    if ranking_values.isna().any().any():
        raise ValueError(
            "Los rankings de escenarios contienen "
            "valores faltantes o no numéricos."
        )

    df["ranking_promedio_escenarios"] = (
        ranking_values.mean(axis=1)
    )

    df["apariciones_top5"] = (
        ranking_values.le(5)
        .sum(axis=1)
        .astype(int)
    )

    base_ranking_column = (
        "ranking_ipt_base"
        if "ranking_ipt_base" in df.columns
        else ranking_cols[0]
    )

    consensus_order = (
        df.sort_values(
            [
                "ranking_promedio_escenarios",
                base_ranking_column,
                "codigo_localidad",
            ],
            ascending=[True, True, True],
            kind="mergesort",
        )
        .index
    )

    consensus_ranking = pd.Series(
        range(1, len(consensus_order) + 1),
        index=consensus_order,
        dtype="int64",
    )

    df["ranking_consenso"] = (
        consensus_ranking
        .reindex(df.index)
        .astype(int)
    )

    def classify_consensus_priority(
        ranking: int,
    ) -> str:
        if ranking <= 5:
            return "Alta"
        if ranking <= 10:
            return "Media-alta"
        if ranking <= 15:
            return "Media"
        return "Baja"

    def classify_confidence(
        appearances: int,
    ) -> str:
        if appearances >= 4:
            return "Alta"
        if appearances >= 2:
            return "Media"
        return "Baja"

    df["nivel_prioridad_consenso"] = (
        df["ranking_consenso"]
        .apply(classify_consensus_priority)
    )

    df["confianza_priorizacion"] = (
        df["apariciones_top5"]
        .apply(classify_confidence)
    )

    return df


# ==============================================================================
# MÉTODOS AVANZADOS DE AUDITORÍA Y RIGOR ESTADÍSTICO (OCDE / JRC STANDARD)
# ==============================================================================

def calculate_vif_scores(
    df: pd.DataFrame,
    dimension_cols: list[str] | tuple[str, ...] | None = None,
) -> pd.DataFrame:
    """Calcula el Factor de Inflación de la Varianza (VIF) para diagnosticar multicolinealidad.

    Fórmula: VIF_j = 1 / (1 - R_j^2), donde R_j^2 es el coeficiente de determinación
    de la regresión lineal de la dimensión j sobre las restantes dimensiones.
    Criterio OCDE/JRC: VIF < 5.0 (Aceptable), VIF >= 10.0 (Multicolinealidad severa).
    """
    import numpy as np

    cols = list(dimension_cols if dimension_cols is not None else DIMENSION_COLUMNS)
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas de dimensión para VIF: {missing}")

    X = df[cols].apply(pd.to_numeric, errors="coerce").values
    n_vars = X.shape[1]
    vif_records = []

    for i in range(n_vars):
        y_i = X[:, i]
        X_other = np.delete(X, i, axis=1)
        # Añadir vector constante de intercepción
        X_design = np.column_stack([np.ones(X_other.shape[0]), X_other])
        
        # OLS cerrado via pseudoinversa
        beta, _, _, _ = np.linalg.lstsq(X_design, y_i, rcond=None)
        y_pred = X_design @ beta
        ss_tot = np.sum((y_i - np.mean(y_i)) ** 2)
        ss_res = np.sum((y_i - y_pred) ** 2)
        
        r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        r2 = max(0.0, min(r2, 0.9999))
        vif_val = 1.0 / (1.0 - r2)
        
        vif_records.append({
            "dimension": cols[i],
            "R2_auxiliar": round(float(r2), 4),
            "VIF": round(float(vif_val), 4),
            "diagnostico_colinealidad": "Aceptable (<5.0)" if vif_val < 5.0 else ("Moderada (5-10)" if vif_val < 10.0 else "Severa (>=10)"),
        })

    return pd.DataFrame(vif_records)


def calculate_geometric_ipt(
    df_metrics: pd.DataFrame,
    dimension_cols: list[str] | tuple[str, ...] | None = None,
    weights: list[float] | None = None,
    epsilon: float = 0.01,
) -> pd.Series:
    """Calcula el IPT mediante Agregación Geométrica Ponderada (Modelo No Compensatorio).

    Fórmula: IPT_Geom = 100 * [ prod_{d=1}^D (s_{i, d} + eps)^{w_d} - eps ]
    A diferencia de la agregación aditiva lineal, la agregación geométrica penaliza
    severamente a las localidades con déficits extremos en derechos fundamentales.
    """
    import numpy as np

    cols = list(dimension_cols if dimension_cols is not None else DIMENSION_COLUMNS)
    X = df_metrics[cols].apply(pd.to_numeric, errors="coerce").values

    if weights is None:
        w = np.ones(len(cols)) / len(cols)
    else:
        w = np.array(weights, dtype=float)
        w = w / w.sum()

    # Cálculo geométrico acotado
    X_shifted = np.clip(X + epsilon, epsilon, 1.0 + epsilon)
    geom_prod = np.exp(np.sum(w * np.log(X_shifted), axis=1))
    ipt_geom = np.clip((geom_prod - epsilon) * 100.0, 0.0, 100.0)

    return pd.Series(ipt_geom, index=df_metrics.index, name="IPT_GEOMETRICO")


def calculate_bootstrap_confidence_intervals(
    df_metrics: pd.DataFrame,
    dimension_cols: list[str] | tuple[str, ...] | None = None,
    n_bootstraps: int = 1000,
    alpha: float = 0.05,
    random_state: int = 42,
) -> pd.DataFrame:
    """Calcula Intervalos de Confianza al (1-alpha)% para el IPT mediante Remuestreo Bootstrap Dirichlet.

    Genera n_bootstraps vectores de ponderación estocásticos a partir de una distribución
    Dirichlet simétrica Dir(1, ..., 1) para cuantificar la incertidumbre del ranking.
    """
    import numpy as np

    cols = list(dimension_cols if dimension_cols is not None else DIMENSION_COLUMNS)
    X = df_metrics[cols].apply(pd.to_numeric, errors="coerce").values
    n_locs, n_dims = X.shape

    rng = np.random.default_rng(random_state)
    # Ponderaciones estocásticas Dirichlet (n_bootstraps, n_dims)
    weights_boot = rng.dirichlet(np.ones(n_dims), size=n_bootstraps)

    # Simulación de puntajes (n_locs, n_bootstraps)
    ipt_sims = (X @ weights_boot.T) * 100.0

    lower_pct = (alpha / 2.0) * 100.0
    upper_pct = (1.0 - alpha / 2.0) * 100.0

    ci_lower = np.percentile(ipt_sims, lower_pct, axis=1)
    ci_upper = np.percentile(ipt_sims, upper_pct, axis=1)
    ci_median = np.median(ipt_sims, axis=1)
    std_boot = np.std(ipt_sims, axis=1)

    ci_df = pd.DataFrame({
        "codigo_localidad": df_metrics["codigo_localidad"].values if "codigo_localidad" in df_metrics.columns else range(n_locs),
        "localidad": df_metrics["localidad"].values if "localidad" in df_metrics.columns else [f"Loc_{i}" for i in range(n_locs)],
        "ipt_bootstrap_mediana": np.round(ci_median, 2),
        "ipt_bootstrap_std": np.round(std_boot, 2),
        "ci_lower_95": np.round(ci_lower, 2),
        "ci_upper_95": np.round(ci_upper, 2),
        "ancho_intervalo_ci95": np.round(ci_upper - ci_lower, 2),
    })

    return ci_df


def calculate_empirical_bayes_smoothing(
    events: pd.Series,
    population: pd.Series,
    scale_factor: float = 10000.0,
) -> pd.Series:
    """Aplica el Estimador de Marshall (Empirical Bayes Rate Smoother) para estabilizar tasas en denominadores pequeños.

    Evita que localidades de muy baja población (como Sumapaz o La Candelaria) registren tasas
    extremadamente volátiles por variaciones aleatorias de conteos pequeños.
    """
    import numpy as np

    e = pd.to_numeric(events, errors="coerce").fillna(0).values
    n = pd.to_numeric(population, errors="coerce").fillna(1).values

    raw_rates = e / n
    mu = np.sum(e) / np.sum(n)  # Media ponderada distrital
    n_bar = np.mean(n)

    # Varianza entre áreas
    s2 = np.sum(n * (raw_rates - mu) ** 2) / np.sum(n)
    var_param = max(s2 - (mu / n_bar), 1e-8)

    # Ponderadores de credibilidad bayesiana
    w_i = var_param / (var_param + (mu / np.maximum(n, 1)))
    smoothed_rates = (w_i * raw_rates + (1.0 - w_i) * mu) * scale_factor

    return pd.Series(smoothed_rates, index=events.index, name="tasa_suavizada_bayes")


# Matriz de vecindad Reina (Queen Contiguity) oficial para las 20 localidades de Bogotá D.C.
BOGOTA_LOCALITY_NEIGHBORS: dict[str, list[str]] = {
    "01": ["02", "11"],
    "02": ["01", "03", "11", "12", "13"],
    "03": ["02", "04", "13", "14", "17"],
    "04": ["03", "05", "17", "18"],
    "05": ["04", "06", "18", "19", "20"],
    "06": ["05", "07", "08", "15", "18", "19"],
    "07": ["06", "08", "19"],
    "08": ["06", "07", "09", "10", "15", "16"],
    "09": ["08", "10", "16"],
    "10": ["08", "09", "11", "12", "16"],
    "11": ["01", "02", "10", "12"],
    "12": ["02", "10", "11", "13", "16"],
    "13": ["02", "03", "12", "14", "16"],
    "14": ["03", "13", "15", "16", "17"],
    "15": ["06", "08", "14", "16", "18"],
    "16": ["08", "09", "10", "12", "13", "14", "15"],
    "17": ["03", "04", "14"],
    "18": ["04", "05", "06", "15"],
    "19": ["05", "06", "07", "20"],
    "20": ["05", "19"],
}


def calculate_spatial_moran(
    values: pd.Series,
    locality_codes: pd.Series | None = None,
    adjacency_matrix: np.ndarray | None = None,
    n_permutations: int = 999,
    random_state: int = 42,
) -> tuple[float, float]:
    """Calcula el Índice de Moran Global (I) y su p-valor por permutaciones Monte Carlo.

    Verifica si existe dependencia espacial (clustering territorial significativo) en Bogotá D.C.
    """
    import numpy as np

    x = pd.to_numeric(values, errors="coerce").fillna(0).values
    n = len(x)

    if adjacency_matrix is not None:
        W = np.array(adjacency_matrix, dtype=float)
    else:
        # Construir matriz normalizada a partir de los códigos DIVIPOLA
        codes = [str(c).zfill(2) for c in (locality_codes if locality_codes is not None else range(1, n + 1))]
        W = np.zeros((n, n), dtype=float)
        for i, ci in enumerate(codes):
            neighbors = BOGOTA_LOCALITY_NEIGHBORS.get(ci, [])
            for j, cj in enumerate(codes):
                if cj in neighbors:
                    W[i, j] = 1.0

    # Estandarización por filas
    row_sums = W.sum(axis=1, keepdims=True)
    W_norm = np.divide(W, row_sums, out=np.zeros_like(W), where=row_sums > 0)
    S0 = np.sum(W_norm)

    z = x - np.mean(x)
    s2 = np.sum(z ** 2)
    if s2 == 0:
        return 0.0, 1.0

    # Estadístico I de Moran observado
    numerator = np.sum(W_norm * np.outer(z, z))
    moran_i = (n / S0) * (numerator / s2)

    # Permutaciones Monte Carlo
    rng = np.random.default_rng(random_state)
    sim_morans = np.zeros(n_permutations)
    for k in range(n_permutations):
        z_perm = rng.permutation(z)
        sim_num = np.sum(W_norm * np.outer(z_perm, z_perm))
        sim_morans[k] = (n / S0) * (sim_num / s2)

    p_value = (np.sum(sim_morans >= moran_i) + 1.0) / (n_permutations + 1.0)

    return float(np.round(moran_i, 4)), float(np.round(p_value, 4))


def save_indicator_table(df: pd.DataFrame, filename: str) -> Path:
    """Guarda la tabla de indicadores en data/processed."""
    path = PROCESSED_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    from src.modeling.domain_indicators import build_all_domain_tables

    print("Consolidando métricas e indicadores multidimensionales SIPTA...")
    metrics_df = build_consolidated_locality_metrics()
    ipt_df = calculate_multidimensional_ipt(metrics_df)
    out_file = save_indicator_table(ipt_df, "matriz_indicadores_ipt_multidimensional.csv")
    print(f"Matriz consolidada e IPT calculados exitosamente en: {out_file}")

    print("\nGenerando tablas maestras por cada dominio territorial...")
    domain_tables = build_all_domain_tables(export_curated=True)
    print(f"Generadas exitosamente {len(domain_tables)} tablas maestras por dominio en data/curated/.")

    print("\nTop 10 Localidades Priorizadas:")
    display_cols = ["codigo_localidad", "localidad", "IPT_MULTIDIMENSIONAL", "RANKING_PRIORIDAD", "NIVEL_PRIORIDAD"]
    existing_display_cols = [c for c in display_cols if c in ipt_df.columns]
    print(ipt_df[existing_display_cols].sort_values("RANKING_PRIORIDAD").head(10))


