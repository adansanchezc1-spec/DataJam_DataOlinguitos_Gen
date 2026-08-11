from pathlib import Path

from src.ingestion.ingest_data import build_output_path, discover_raw_files, ingest_dataset


def test_discover_raw_files_excludes_non_data_files(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    (raw_dir / "subdir").mkdir(parents=True)
    (raw_dir / "README.md").write_text("ignore")
    (raw_dir / ".gitkeep").write_text("")
    (raw_dir / "subdir" / "dataset.csv").write_text("a,b\n1,2\n")
    (raw_dir / "subdir" / "map.geojson").write_text('{"type":"FeatureCollection","features":[]}')

    files = discover_raw_files(raw_dir)

    assert [p.name for p in files] == ["dataset.csv", "map.geojson"]
    assert all(p.is_file() for p in files)


def test_build_output_path_preserves_relative_structure(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    source = raw_dir / "demo" / "sample.csv"

    output_path = build_output_path(source, raw_dir, processed_dir, suffix=".csv")

    assert output_path == processed_dir / "demo" / "sample.csv"


def test_ingest_dataset_handles_latin1_csv(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    raw_dir.mkdir(parents=True)
    processed_dir.mkdir(parents=True)
    source = raw_dir / "latin1.csv"
    source.write_bytes("nombre,valor\nBogotá,1\nSeñor,2\n".encode("latin-1"))

    result = ingest_dataset(source, raw_dir=raw_dir, processed_dir=processed_dir, overwrite=True)

    assert result["status"] == "ingested"
    assert (processed_dir / "latin1.csv").exists()
