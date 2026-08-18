"""Genera la copia WGS84 del GeoJSON de oferta de cupos de Educación."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.cleaning.clean_data import reproject_geojson_to_wgs84

SOURCE = ROOT / "data" / "raw" / "EDUCACION" / "ofertacupos_032025.geojson"
DESTINATION = (
    ROOT / "data" / "processed" / "EDUCACION" / "ofertacupos_032025_wgs84.geojson"
)


def main() -> None:
    output = reproject_geojson_to_wgs84(SOURCE, DESTINATION)
    print(f"GeoJSON WGS84 generado en: {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
