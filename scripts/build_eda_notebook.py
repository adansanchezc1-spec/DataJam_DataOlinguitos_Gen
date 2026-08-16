"""Genera un notebook de EDA para las fuentes descubiertas en data/raw."""

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks"
OUT = OUT_DIR / "01_eda_descubrimiento.ipynb"


def main() -> None:
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    }

    cells = []
    md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
    code = lambda s: cells.append(nbf.v4.new_code_cell(s))

    md("""# EDA - Descubrimiento de fuentes de datos\n\nEste notebook genera una guía de exploración de los datos en `data/raw`.\n\nUsa `scripts/inventory_data.py` para generar un inventario reproducible y `scripts/inspect_discovered.py` para inspeccionar esquemas y metadatos.\n""")

    code("""import warnings\nfrom pathlib import Path\n\nimport geopandas as gpd\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\nwarnings.filterwarnings('ignore')\n\nROOT = Path.cwd()\nRAW = ROOT / 'data' / 'raw'\nprint('RAW directory:', RAW)\n""")

    md("""## 1. Revisar archivos de `data/raw`\n\nEjecuta el siguiente bloque para listar los archivos detectados en el directorio de datos crudos.\n""")

    code("""files = sorted(RAW.rglob('*'))\nfor f in files:\n    if f.is_file():\n        print(f.relative_to(ROOT))\n""")

    md("""## 2. Primer vistazo a los datasets\n\nCarga y muestra los primeros registros de los principales archivos tabulares y espaciales.\n""")

    code("""sample_csv = next(RAW.rglob('*.csv'), None)\nif sample_csv is not None:\n    df = pd.read_csv(sample_csv, low_memory=False)\n    print(sample_csv.name, '->', df.shape)\n    display(df.head())\nelse:\n    print('No se encontró CSV en data/raw.')\n""")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as handle:
        nbf.write(nb, handle)

    print(f"Notebook generado: {OUT}")


if __name__ == "__main__":
    main()
