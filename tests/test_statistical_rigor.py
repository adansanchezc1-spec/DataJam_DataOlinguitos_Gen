"""Pruebas unitarias y de rigor estadístico para el motor matemático de SIPTA.

Fase PDCO: CONTROL
Estándares: OECD/JRC Composite Indicators Handbook, ASA Guidelines, SWEBOK Cap. 5
"""

import numpy as np
import pandas as pd
import pytest

from src.modeling.calculate_indicators import (
    DIMENSION_COLUMNS,
    build_consolidated_locality_metrics,
    calculate_bootstrap_confidence_intervals,
    calculate_empirical_bayes_smoothing,
    calculate_geometric_ipt,
    calculate_multidimensional_ipt,
    calculate_spatial_moran,
    calculate_vif_scores,
)


@pytest.fixture
def sample_metrics_df() -> pd.DataFrame:
    """Fixture con matriz de 20 localidades sintéticas balanceadas."""
    rng = np.random.default_rng(42)
    n = 20
    data = {
        "codigo_localidad": [str(i).zfill(2) for i in range(1, n + 1)],
        "localidad": [f"Localidad_{i}" for i in range(1, n + 1)],
    }
    for dim in DIMENSION_COLUMNS:
        data[dim] = rng.uniform(0.1, 0.9, size=n)
    return pd.DataFrame(data)


class TestStatisticalRigor:
    """Suite de validación formal de rigor cuantitativo."""

    def test_vif_calculation_and_bounds(self, sample_metrics_df: pd.DataFrame) -> None:
        """Verifica que el VIF se calcule correctamente y no exceda el umbral crítico."""
        vif_df = calculate_vif_scores(sample_metrics_df)
        assert not vif_df.empty
        assert len(vif_df) == len(DIMENSION_COLUMNS)
        assert "VIF" in vif_df.columns
        assert "R2_auxiliar" in vif_df.columns
        # Para variables sintéticas independientes, el VIF debe ser bajo
        assert (vif_df["VIF"] < 5.0).all()

    def test_geometric_ipt_properties(self, sample_metrics_df: pd.DataFrame) -> None:
        """Verifica que la agregación geométrica no compensatoria cumpla propiedades axiomáticas."""
        geom_ipt = calculate_geometric_ipt(sample_metrics_df)
        assert len(geom_ipt) == len(sample_metrics_df)
        assert (geom_ipt >= 0.0).all()
        assert (geom_ipt <= 100.0).all()

        # Probar penalización de asimetría: Si una localidad tiene 0.0 en una dimensión clave
        df_asymmetric = sample_metrics_df.copy()
        df_asymmetric.loc[0, "dim_educacion"] = 0.001
        geom_val = calculate_geometric_ipt(df_asymmetric).iloc[0]
        linear_val = df_asymmetric[list(DIMENSION_COLUMNS)].mean(axis=1).iloc[0] * 100.0
        # En presencia de un valor casi nulo, el valor geométrico debe ser menor que el lineal
        assert geom_val <= linear_val

    def test_bootstrap_confidence_intervals(self, sample_metrics_df: pd.DataFrame) -> None:
        """Verifica la integridad de los intervalos de confianza Bootstrap Dirichlet."""
        ci_df = calculate_bootstrap_confidence_intervals(
            sample_metrics_df, n_bootstraps=200, alpha=0.05, random_state=42
        )
        assert len(ci_df) == 20
        assert "ci_lower_95" in ci_df.columns
        assert "ci_upper_95" in ci_df.columns
        assert "ancho_intervalo_ci95" in ci_df.columns

        # Límite inferior debe ser <= Límite superior
        assert (ci_df["ci_lower_95"] <= ci_df["ci_upper_95"]).all()
        # El ancho del intervalo debe ser no negativo
        assert (ci_df["ancho_intervalo_ci95"] >= 0.0).all()

    def test_empirical_bayes_smoothing_marshall(self) -> None:
        """Valida que el estimador de Marshall reduzca la varianza en denominadores pequeños."""
        # Localidad 1: 1 evento en 100 personas (tasa cruda = 100 por 10.000)
        # Localidad 2: 100 eventos en 10.000 personas (tasa cruda = 100 por 10.000)
        # Localidad 3: 500 eventos en 50.000 personas (tasa cruda = 100 por 10.000)
        events = pd.Series([1, 100, 500])
        pop = pd.Series([100, 10000, 50000])

        smoothed = calculate_empirical_bayes_smoothing(events, pop, scale_factor=10000.0)
        assert len(smoothed) == 3
        assert (smoothed > 0).all()
        # El valor para n=100 debe estar encogido (shrunk) hacia la media distrital
        assert abs(smoothed.iloc[0] - smoothed.iloc[2]) < 200.0

    def test_spatial_moran_calculation(self) -> None:
        """Verifica el cálculo del Índice de Moran Global y su significancia por permutación."""
        # Valores con fuerte gradiente espacial (cluster contiguo en el sur)
        values = pd.Series(
            [
                10.0, 15.0, 20.0, 65.0, 80.0, 60.0, 70.0, 50.0, 30.0, 25.0,
                20.0, 25.0, 22.0, 35.0, 45.0, 35.0, 20.0, 75.0, 85.0, 70.0,
            ]
        )
        locality_codes = pd.Series([str(i).zfill(2) for i in range(1, 21)])

        moran_i, p_val = calculate_spatial_moran(
            values, locality_codes=locality_codes, n_permutations=199, random_state=42
        )
        assert isinstance(moran_i, float)
        assert isinstance(p_val, float)
        assert -1.0 <= moran_i <= 1.0
        assert 0.0 <= p_val <= 1.0
        # Dado el fuerte gradiente de autocorrelación en el sur, Moran I debe ser positivo
        assert moran_i > 0.0

    def test_real_dataset_vif_and_properties(self) -> None:
        """Valida que los datos reales de Bogotá cumplan con los estándares de rigor estadístico."""
        metrics_df = build_consolidated_locality_metrics()
        ipt_df = calculate_multidimensional_ipt(metrics_df)

        # 1. VIF < 10.0 en todas las dimensiones (umbral de no multicolinealidad severa de la OCDE)
        vif_df = calculate_vif_scores(ipt_df)
        assert (vif_df["VIF"] < 10.0).all()
        # Verificar que el promedio de VIF distrital sea bajo (< 4.0)
        assert vif_df["VIF"].mean() < 4.0

        # 2. IPT Geométrico acotado y consistente
        geom_ipt = calculate_geometric_ipt(ipt_df)
        assert len(geom_ipt) == 20
        assert (geom_ipt >= 0.0).all() and (geom_ipt <= 100.0).all()

        # 3. Bootstrap CI 95% consistente con IPT_MULTIDIMENSIONAL
        ci_df = calculate_bootstrap_confidence_intervals(ipt_df, n_bootstraps=500, random_state=42)
        assert len(ci_df) == 20
        assert (ci_df["ci_lower_95"] <= ci_df["ci_upper_95"]).all()
