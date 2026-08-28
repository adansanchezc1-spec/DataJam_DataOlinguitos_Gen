"""Corrige celda 4 en 00_ingestion_eda_master.ipynb."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
nb_path = ROOT / "notebooks" / "01_ingestion" / "00_ingestion_eda_master.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "df_poblacion = load_raw_csv(archivo_poblacion" in source or "archivo_poblacion" in source:
            cell["source"] = [
                "df_poblacion = pd.read_csv(str(ROOT / 'data' / 'processed' / 'DEMOGRAFIA' / 'poblacion_localidad_2025.csv'))\n",
                "print('Dataset poblacional oficial DANE 2025 cargado correctamente:', df_poblacion.shape)\n",
                "display(df_poblacion.head())\n",
            ]

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("[OK] 00_ingestion_eda_master.ipynb celda 4 corregida.")
