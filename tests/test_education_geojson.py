import geopandas as gpd
import pandas as pd

from src.cleaning.clean_data import PROCESSED_DIR, RAW_DIR

SOURCE = RAW_DIR / "EDUCACION" / "ofertacupos_032025.geojson"
PROCESSED = PROCESSED_DIR / "EDUCACION" / "ofertacupos_032025_wgs84.geojson"
OFFER_COLUMNS = [
    "OPreescola",
    "OPrimaria",
    "OSecundari",
    "OMedia",
    "Aceleracio",
    "Educacion_",
]


def test_education_processed_geojson_is_wgs84_and_preserves_data() -> None:
    raw = gpd.read_file(SOURCE)
    processed = gpd.read_file(PROCESSED)

    assert raw.crs is not None and raw.crs.to_epsg() == 3857
    assert processed.crs is not None and processed.crs.to_epsg() == 4326
    assert len(processed) == len(raw) == 747
    assert set(processed.geometry.geom_type) == {"Point"}
    assert not processed.geometry.isna().any()
    assert not processed.geometry.is_empty.any()
    pd.testing.assert_frame_equal(
        processed.drop(columns="geometry").reset_index(drop=True),
        raw.drop(columns="geometry").reset_index(drop=True),
        check_dtype=False,
    )


def test_education_total_matches_offer_components() -> None:
    processed = gpd.read_file(PROCESSED)
    calculated_total = processed[OFFER_COLUMNS].sum(axis=1)

    pd.testing.assert_series_equal(
        processed["OTotal"], calculated_total, check_names=False, check_dtype=False
    )
