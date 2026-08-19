"""Helpers de visualización para el EDA: matplotlib + seaborn + geopandas."""

from __future__ import annotations

import sys
import matplotlib
if "pytest" in sys.modules or not sys.stdout.isatty():
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    sns = None
    HAS_SEABORN = False

PALETTE = {
    "DEMOGRAFIA_POBLACION": "#2E86AB",
    "SALUD": "#D1495B",
    "EDUCACION": "#2A9D8F",
    "MOVILIDAD": "#F4A261",
    "INFRAESTRUCTURA_ESPACIO_PUBLICO": "#6C757D",
    "FINANZAS_INVERSION_PUBLICA": "#7B2CBF",
    "GAPS": "#ADB5BD",
    "GENERAL": "#2E86AB",
}


def set_style():
    """Configura el tema visual y los rcParams de matplotlib para gráficos premium."""
    # 1. Establecer primero el tema básico si seaborn está disponible
    if HAS_SEABORN and sns is not None:
        sns.set_theme(style="whitegrid", palette="muted")
    
    # 2. Configurar rcParams para lograr un look minimalista, limpio y profesional
    plt.rcParams.update(
        {
            "figure.figsize": (10, 4.5),
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.titlepad": 12,
            "axes.labelsize": 10,
            "axes.labelweight": "semibold",
            "axes.labelpad": 8,
            "xtick.labelsize": 9.5,
            "ytick.labelsize": 9.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": True,
            "axes.spines.bottom": True,
            "axes.edgecolor": "#CCCCCC",
            "axes.linewidth": 0.8,
            "grid.alpha": 0.25,
            "grid.linestyle": "--",
            "font.family": "sans-serif",
            "figure.dpi": 110,
            "legend.fontsize": 9,
            "legend.title_fontsize": 9.5,
            "legend.frameon": True,
            "legend.facecolor": "white",
            "legend.edgecolor": "none",
        }
    )


def _despine(ax):
    """Elimina las espinas superior y derecha de un eje."""
    if HAS_SEABORN and sns is not None:
        sns.despine(ax=ax)
    else:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)


def histograma(series, title=None, bins="auto", color="#2E86AB", ax=None):
    """Dibuja el histograma de una serie numérica, adaptándolo automáticamente si es discreta.

    Evita curvas KDE continuas oscilatorias y barras desalineadas en variables discretas (enteros).
    """
    data = pd.to_numeric(series, errors="coerce").dropna()
    if data.empty:
        print(f"No hay valores numéricos para {series.name}.")
        return None
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4.5))

    # Detectar si la variable es discreta (todos los valores únicos son enteros, rango <= 50 y hay <= 30 valores distintos)
    unique_vals = data.unique()
    is_discrete = (
        len(unique_vals) <= 30
        and all(float(x).is_integer() for x in unique_vals)
        and (data.max() - data.min() <= 50)
    )

    if HAS_SEABORN and sns is not None:
        if is_discrete:
            # Si es discreta, usamos discrete=True y desactivamos KDE (ya que no es continua)
            sns.histplot(
                data,
                discrete=True,
                ax=ax,
                color=color,
                edgecolor="white",
                linewidth=1.2,
                alpha=0.8,
            )
            # Asegurar marcas del eje X solo en números enteros
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        else:
            # Si es continua, dejamos el KDE condicionado al tamaño de los datos y usamos bins auto
            kde = len(data) >= 10
            sns.histplot(
                data,
                kde=kde,
                bins=bins,
                ax=ax,
                color=color,
                edgecolor="white",
                linewidth=0.8,
                alpha=0.75,
            )
    else:
        num_bins = 20 if bins == "auto" else bins
        ax.hist(data, bins=num_bins, color=color, edgecolor="white", linewidth=0.8, alpha=0.75)

    # Añadir líneas estéticas de promedio y mediana
    mean_val = data.mean()
    median_val = data.median()

    ax.axvline(
        mean_val,
        color="#E74C3C",
        linestyle="--",
        linewidth=1.5,
        label=f"Media: {mean_val:,.2f}",
    )
    ax.axvline(
        median_val,
        color="#2C3E50",
        linestyle="-",
        linewidth=1.5,
        label=f"Mediana: {median_val:,.2f}",
    )

    ax.set_title(title or f"Distribución de {series.name}", pad=12)
    ax.set_ylabel("Registros (Frecuencia)")
    ax.set_xlabel(series.name)
    ax.legend(loc="upper right")

    # Limpiar bordes innecesarios
    _despine(ax)
    plt.tight_layout()
    return ax


def boxplot(series, title=None, color="#2E86AB", ax=None):
    """Dibuja un boxplot de una serie numérica, detallando percentiles y número de outliers."""
    data = pd.to_numeric(series, errors="coerce").dropna()
    if data.empty:
        print(f"No hay valores numéricos para {series.name}.")
        return None
    q1, q3 = data.quantile([0.25, 0.75])
    iqr = q3 - q1
    n_out = int(((data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)).sum())
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 3.8))
    
    if HAS_SEABORN and sns is not None:
        sns.boxplot(x=data, ax=ax, color=color, width=0.4, linewidth=1.2, fliersize=4)
    else:
        ax.boxplot(data, vert=False, patch_artist=True, boxprops=dict(facecolor=color, alpha=0.8))
    ax.set_title(title or f"Boxplot de {series.name} | n={len(data)} | outliers={n_out}", pad=12)
    ax.set_xlabel(series.name)
    
    _despine(ax)
    plt.tight_layout()
    return ax


def barras(series, title=None, top_n=15, color="#2E86AB", ax=None):
    """Dibuja un gráfico de barras horizontales mostrando conteo y porcentaje para cada categoría."""
    counts = series.astype("string").fillna("(sin dato)").value_counts().head(top_n)
    if counts.empty:
        print(f"No hay categorías para {series.name}.")
        return None
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, max(4.2, len(counts) * 0.35)))

    # Dibujar las barras horizontales
    if HAS_SEABORN and sns is not None:
        sns.barplot(x=counts.values, y=counts.index, ax=ax, color=color, alpha=0.85)
    else:
        ax.barh(counts.index, counts.values, color=color, alpha=0.85)

    # Añadir etiquetas con el valor numérico y el porcentaje exacto al lado de cada barra
    total = series.notna().sum()
    if ax.containers:
        container = ax.containers[0]
        labels = []
        for val in counts.values:
            pct = (val / total * 100) if total > 0 else 0
            labels.append(f"  {val:,} ({pct:.1f}%)")
            
        ax.bar_label(
            container,
            labels=labels,
            padding=4,
            fontsize=9.5,
            color="#2C3E50",
            fontweight="semibold",
        )

    # Ajustar límite derecho del eje X para que las etiquetas no se recorten
    ax.set_xlim(right=ax.get_xlim()[1] * 1.18)

    ax.set_title(title or f"Frecuencia de {series.name}", pad=12)
    ax.set_xlabel("Registros")
    ax.set_ylabel("")

    # Desactivar la rejilla vertical para mejorar la limpieza visual
    ax.grid(False, axis="x")
    ax.grid(True, axis="y", linestyle="--", alpha=0.25)

    _despine(ax)
    plt.tight_layout()
    return ax


def heatmap_nulos(df, title="Nulos por columna", ax=None):
    """Dibuja barras horizontales con el porcentaje de nulos de cada columna, mostrando etiquetas de porcentaje."""
    pct = df.isna().mean().sort_values(ascending=False) * 100
    pct = pct[pct > 0]
    if pct.empty:
        print("Sin columnas con nulos.")
        return None
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, max(3, len(pct) * 0.38)))

    if HAS_SEABORN and sns is not None:
        sns.barplot(x=pct.values, y=pct.index, ax=ax, color="#E74C3C", alpha=0.85)
    else:
        ax.barh(pct.index, pct.values, color="#E74C3C", alpha=0.85)

    # Añadir etiquetas con el porcentaje exacto de nulos
    if ax.containers:
        container = ax.containers[0]
        labels = [f"  {val:.2f}%" for val in pct.values]
        ax.bar_label(
            container,
            labels=labels,
            padding=4,
            fontsize=9.5,
            color="#2C3E50",
            fontweight="semibold",
        )

    # Ajustar límite del eje X sin superar el 100%
    ax.set_xlim(right=min(100.0, ax.get_xlim()[1] * 1.15))

    ax.set_title(title, pad=12)
    ax.set_xlabel("% nulos (sobre filas de datos)")
    ax.set_ylabel("")

    ax.grid(False, axis="x")
    ax.grid(True, axis="y", linestyle="--", alpha=0.25)

    _despine(ax)
    plt.tight_layout()
    return ax


def mapa(gdf, title, column=None, markersize=4, cmap="viridis", ax=None):
    """Mapa simple con geopandas; soporta puntos y polígonos con diseño limpio."""
    if gdf is None or len(gdf) == 0 or "geometry" not in gdf:
        print(f"No hay geometría para mapa: {title}")
        return None
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    geom_types = set(gdf.geometry.geom_type.dropna())
    
    if any(t in geom_types for t in ("Point", "MultiPoint")):
        # Dibujar puntos geográficos
        gdf.plot(ax=ax, markersize=markersize, linewidth=0.5, color="#2E86AB", alpha=0.7)
    elif column is not None:
        # Dibujar mapas coropléticos
        gdf.plot(
            ax=ax,
            column=column,
            cmap=cmap,
            legend=True,
            legend_kwds={"shrink": 0.6, "label": column},
            linewidth=0.4,
            edgecolor="#ffffff",
        )
    else:
        # Dibujar polígonos con color neutro
        gdf.plot(
            ax=ax,
            linewidth=0.5,
            edgecolor="#ffffff",
            color="#D1D5DB",
            alpha=0.8,
        )
        
    ax.set_title(title, pad=12, fontweight="bold")
    ax.set_axis_off()
    plt.tight_layout()
    return ax


def serie_temporal(df, x, y, hue=None, title=None, ax=None):
    """Dibuja una serie temporal en línea con marcadores circulares y diseño premium."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(11, 4.5))
    
    sns.lineplot(data=df, x=x, y=y, hue=hue, marker="o", markersize=6, linewidth=2, ax=ax)
    ax.set_title(title or f"Serie temporal de {y}", pad=12)
    ax.tick_params(axis="x", rotation=30)
    
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    
    sns.despine(ax=ax)
    plt.tight_layout()
    return ax
