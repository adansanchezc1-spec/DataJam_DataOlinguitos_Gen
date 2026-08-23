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


