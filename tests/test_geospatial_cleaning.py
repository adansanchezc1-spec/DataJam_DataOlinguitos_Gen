from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from src.cleaning.clean_data import PROCESSED_DIR, ROOT, reproject_geojson_to_wgs84


def test_project_paths_point_to_repository_data_directory() -> None:
    assert (ROOT / "src" / "cleaning" / "clean_data.py").is_file()
    assert PROCESSED_DIR == ROOT / "data" / "processed"


def test_reproject_geojson_to_wgs84_preserves_raw_file(tmp_path: Path) -> None:
    source = tmp_path / "raw" / "sample.geojson"
    destination = tmp_path / "processed" / "sample_wgs84.geojson"
    source.parent.mkdir(parents=True)

    original = gpd.GeoDataFrame(
        {"id": [1], "nombre": ["Bogotá"]},
        geometry=[Point(-8242002.7032, 531131.4316)],
        crs="EPSG:3857",
    )
    original.to_file(source, driver="GeoJSON")
    raw_bytes = source.read_bytes()

    output = reproject_geojson_to_wgs84(source, destination)
    processed = gpd.read_file(output)

    assert output == destination
    assert source.read_bytes() == raw_bytes
    assert processed.crs is not None
    assert processed.crs.to_epsg() == 4326
    pd.testing.assert_frame_equal(
        processed.drop(columns="geometry"),
        original.drop(columns="geometry"),
        check_dtype=False,
    )
