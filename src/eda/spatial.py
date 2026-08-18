"""Helpers espaciales: cruces con la capa Loca del MR para conteos por localidad."""

from __future__ import annotations

import geopandas as gpd
import pandas as pd

from src.eda.profiling import CODIGO_LOCALIDAD_A_NOMBRE, LOCALIDAD_ORDER, standardize_locality


def load_loca(mr_path, layer="Loca") -> gpd.GeoDataFrame:
    """Carga la capa de localidades del MR (20 polígonos, EPSG:4686)."""
    gdf = gpd.read_file(mr_path, layer=layer)
    if "LocCodigo" in gdf.columns:
        gdf["localidad"] = pd.to_numeric(gdf["LocCodigo"], errors="coerce").map(CODIGO_LOCALIDAD_A_NOMBRE)
    elif "LocNombre" in gdf.columns:
        gdf["localidad"] = gdf["LocNombre"].map(standardize_locality)
    elif "LocAAdmini" in gdf.columns:
        gdf["localidad"] = gdf["LocAAdmini"].map(standardize_locality)
    return gdf


def count_points_by_locality(points_gdf: gpd.GeoDataFrame, loca_gdf: gpd.GeoDataFrame, crs: str | None = None) -> pd.DataFrame:
    """Cuenta puntos dentro de cada localidad mediante cruce espacial.

    Re-proyecta ambos a un CRS común (el de localidades por defecto) y
    devuelve una tabla localidad -> n ordenada descendentemente por conteo.
    """
    if points_gdf is None or len(points_gdf) == 0:
        return pd.DataFrame(columns=["localidad", "n"])
    if loca_gdf is None or len(loca_gdf) == 0:
        return pd.DataFrame(columns=["localidad", "n"])
    target_crs = crs or loca_gdf.crs or "EPSG:4326"
    pts = points_gdf.to_crs(target_crs) if points_gdf.crs else points_gdf
    loc = loca_gdf.to_crs(target_crs)
    joined = gpd.sjoin(pts, loc[["geometry", "localidad"]], how="inner", predicate="within")
    counts = (
        joined.groupby("localidad")
        .size()
        .reset_index(name="n")
        .sort_values("n", ascending=False)
        .reset_index(drop=True)
    )
    return counts


def coverage_matrix(base: pd.DataFrame, counts: dict[str, pd.DataFrame], col_name: str) -> pd.DataFrame:
    """Une conteos por localidad a la matriz base de 21 filas (Bogotá + 20)."""
    out = base.copy()
    for key, table in counts.items():
        label = f"{key}::{col_name}" if "::" not in key else key
        localidad_col = "localidad"
        if localidad_col in table.columns and "n" in table.columns:
            out = out.merge(
                table.rename(columns={"n": label}),
                on="localidad",
                how="left",
            )
    return out


def localidades_base() -> pd.DataFrame:
    return pd.DataFrame({"localidad": LOCALIDAD_ORDER})
