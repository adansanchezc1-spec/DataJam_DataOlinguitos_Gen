"""Inspecciona archivos de datos crudos y muestra metadatos de esquema."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"


def inspect_gpkg(path: Path) -> None:
    import geopandas as gpd
    import pyogrio

    try:
        layers = gpd.list_layers(path)
    except Exception as exc:
        print(f"[GPKG] {path.relative_to(ROOT)} :: error al listar capas: {exc}")
        return

    if isinstance(layers, pd.DataFrame):
        layer_rows = list(layers.itertuples(index=False))
    else:
        layer_rows = list(layers)

    print(f"[GPKG] {path.relative_to(ROOT)} :: {len(layer_rows)} capas")
    for row in layer_rows:
        if isinstance(row, tuple):
            name = row[0]
            geom = row[1] if len(row) > 1 else None
        else:
            name = getattr(row, "name", None) or getattr(row, "layer", None)
            geom = getattr(row, "geometry_type", None)

        name = name.decode("latin-1") if isinstance(name, bytes) else str(name)
        geom = geom.decode("latin-1") if isinstance(geom, bytes) else str(geom)
        try:
            info = pyogrio.read_info(path, layer=name)
            fields = info["fields"]
            cols = [f[0] for f in fields[:20]] if hasattr(fields, "dtype") and fields.dtype.names else list(fields)[:20]
            print(f"   capa '{name}' | geom={geom} | CRS={info['crs']} | filas={info['features']}")
            print(f"      campos({len(fields)}): {cols}{' ...' if len(fields) > 20 else ''}")
        except Exception:
            gdf = gpd.read_file(path, layer=name)
            print(f"   capa '{name}' | geom={geom} | CRS={gdf.crs} | filas={len(gdf)}")
            print(f"      campos({len(gdf.columns)}): {list(gdf.columns)[:20]}{' ...' if len(gdf.columns) > 20 else ''}")


def inspect_geojson(path: Path) -> None:
    import geopandas as gpd

    gdf = gpd.read_file(path)
    print(f"[GEOJSON] {path.relative_to(ROOT)} :: {len(gdf)} features | CRS={gdf.crs} | geom={gdf.geom_type.drop_duplicates().tolist()}")
    print(f"      campos: {list(gdf.columns)}")


def inspect_csv(path: Path, n: int = 3) -> None:
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            df = pd.read_csv(path, nrows=n, sep=None, engine="python", encoding=enc)
            break
        except Exception:
            continue
    else:
        print(f"[CSV] {path.relative_to(ROOT)} :: no se pudo leer")
        return

    print(f"[CSV] {path.relative_to(ROOT)} :: {len(df.columns)} cols (muestra {n} filas)")
    print(f"      columnas: {list(df.columns)}")
    for i, row in df.head(n).iterrows():
        print(f"      fila{i}: {row.astype(str).tolist()}")


def inspect_xlsx(path: Path) -> None:
    try:
        xl = pd.ExcelFile(path)
    except Exception as exc:
        print(f"[XLSX] {path.relative_to(ROOT)} :: error al abrir: {exc}")
        return

    print(f"[XLSX] {path.relative_to(ROOT)} :: hojas: {xl.sheet_names}")
    for sheet in xl.sheet_names[:3]:
        try:
            df = xl.parse(sheet, nrows=3)
            print(f"   hoja '{sheet}' | {len(df.columns)} cols | filas~{len(df)}")
            print(f"      columnas: {list(df.columns)}")
        except Exception as exc:
            print(f"   hoja '{sheet}' | error: {exc}")


def main() -> None:
    targets = []
    for path in sorted(RAW.rglob("*")):
        if path.suffix.lower() in {".gpkg", ".geojson", ".csv", ".xlsx"}:
            targets.append(path)

    if not targets:
        print("No se encontraron archivos de datos en data/raw.")
        return

    for path in targets:
        if path.suffix.lower() == ".gpkg":
            inspect_gpkg(path)
        elif path.suffix.lower() == ".geojson":
            inspect_geojson(path)
        elif path.suffix.lower() == ".csv":
            inspect_csv(path)
        elif path.suffix.lower() == ".xlsx":
            inspect_xlsx(path)
        print()


if __name__ == "__main__":
    main()
