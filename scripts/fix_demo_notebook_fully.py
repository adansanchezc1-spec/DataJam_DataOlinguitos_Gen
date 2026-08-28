"""Script para corregir exhaustivamente 01_ingestion_demografia.ipynb."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
nb_path = ROOT / "notebooks" / "01_ingestion" / "01_ingestion_demografia.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "osb_demografia-poblacion-upl.csv" in source or "demo_upl" in source:
            cell["source"] = [
                "demo_loc = pd.read_csv(str(ROOT / 'data' / 'processed' / 'DEMOGRAFIA' / 'poblacion_localidad_dane_sdp.csv'))\n",
                "demo_upz = pd.read_csv(str(ROOT / 'data' / 'processed' / 'DEMOGRAFIA' / 'poblacion_upz_dane_sdp.csv'))\n",
                "print('localidad DANE/SDP:', demo_loc.shape, '| UPZ DANE/SDP:', demo_upz.shape)\n",
                "print('anos localidad:', sorted(demo_loc['ano'].dropna().unique()))\n",
                "print('anos UPZ:', sorted(demo_upz['ano'].dropna().unique()))\n",
                "last_year = int(demo_loc['ano'].max())\n",
                "print('Ultimo ano proyectado:', last_year)\n",
            ]
        elif "SPEC = {" in source and "demografia" in source:
            cell["source"] = [
                "t0('demo_loc')\n",
                "SPEC = {\n",
                "    'id': 'demografia_localidad_dane_2025',\n",
                "    'titulo': 'Poblacion oficial DANE/SDP 2025 por localidad',\n",
                "    'path': 'data/processed/DEMOGRAFIA/poblacion_localidad_2025.csv',\n",
                "}\n",
            ]
        elif "demo_loc = pd.read_csv" in source and "ANO" in source:
            cell["source"] = [
                "demo_loc = pd.read_csv(str(ROOT / 'data' / 'processed' / 'DEMOGRAFIA' / 'poblacion_localidad_dane_sdp.csv'))\n",
                "print('Proyecciones oficiales DANE/SDP:', demo_loc.shape)\n",
                "display(demo_loc.head())\n",
            ]

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("[OK] 01_ingestion_demografia.ipynb corregido totalmente.")
