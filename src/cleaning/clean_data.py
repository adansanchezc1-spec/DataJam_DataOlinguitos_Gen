"""Plantilla básica de limpieza de datos para SIPTA."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df


def cast_numeric_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


def clean_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for column in columns:
        if column in df.columns:
            df[column] = df[column].astype(str).str.strip()
    return df


def save_processed(df: pd.DataFrame, filename: str) -> Path:
    path = PROCESSED_DIR / filename
    df.to_csv(path, index=False)
    return path


def reproject_geojson_to_wgs84(source: str | Path, destination: str | Path) -> Path:
    """Create an EPSG:4326 GeoJSON copy without modifying the raw source."""
    import geopandas as gpd

    source_path = Path(source)
    destination_path = Path(destination)

    if source_path.resolve() == destination_path.resolve():
        raise ValueError("La salida procesada no puede sobrescribir el archivo raw.")
    if not source_path.is_file():
        raise FileNotFoundError(source_path)

    geodata = gpd.read_file(source_path)
    if geodata.crs is None:
        raise ValueError(f"El archivo no declara un CRS: {source_path}")

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    geodata.to_crs(epsg=4326).to_file(destination_path, driver="GeoJSON")
    return destination_path


if __name__ == '__main__':
    print('Módulo de limpieza SIPTA. Use funciones desde otros scripts.')
