"""Script para corregir con precisión las celdas de ingesta demográfica en los notebooks."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 1. Corregir 01_ingestion_demografia.ipynb
nb_demo_path = ROOT / "notebooks" / "01_ingestion" / "01_ingestion_demografia.ipynb"
with open(nb_demo_path, "r", encoding="utf-8") as f:
    nb_demo = json.load(f)

for cell in nb_demo["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "PROCESSED_DIR" in source and "RAW_DIR" in source:
            cell["source"] = [
                "import sys\n",
                "from pathlib import Path\n",
                "import pandas as pd\n",
                "\n",
                "for p in [Path('.').resolve(), Path('.').resolve().parent, Path('.').resolve().parent.parent]:\n",
                "    if (p / 'src').exists():\n",
                "        ROOT = p\n",
                "        if str(ROOT) not in sys.path:\n",
                "            sys.path.insert(0, str(ROOT))\n",
                "        break\n",
                "\n",
                "from src.ingestion.parse_demografia_dane import parse_all_demografia_dane\n",
                "\n",
                "# Ingesta oficial DANE / SDP (2018-2035)\n",
                "df_loc_dane, df_2025, df_upz = parse_all_demografia_dane()\n",
                "print('Proyecciones DANE/SDP por Localidad (2018-2035):', df_loc_dane.shape)\n",
                "print('Poblacion Oficial 2025 (20 Localidades):', df_2025.shape)\n",
                "display(df_2025.head())\n",
                "print('Proyecciones DANE/SDP por UPZ (2018-2024):', df_upz.shape)\n",
            ]
            break

with open(nb_demo_path, "w", encoding="utf-8") as f:
    json.dump(nb_demo, f, indent=1, ensure_ascii=False)
print("[OK] 01_ingestion_demografia.ipynb celda 1 corregida")

# 2. Corregir 02_ingestion_salud.ipynb
nb_salud_path = ROOT / "notebooks" / "01_ingestion" / "02_ingestion_salud.ipynb"
with open(nb_salud_path, "r", encoding="utf-8") as f:
    nb_salud = json.load(f)

for cell in nb_salud["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "pob = demo" in source or "Camas por 1.000 habitantes" in source:
            cell["source"] = [
                "demo = pd.read_csv(str(ROOT / 'data' / 'processed' / 'DEMOGRAFIA' / 'poblacion_localidad_2025.csv'))\n",
                "pob = demo['poblacion_2025'].sum() if 'poblacion_2025' in demo.columns else 8101412\n",
                "print(f'Poblacion de Bogota (2025 DANE/SDP): {pob:,.0f}')\n",
                "print(f'Camas por 1.000 habitantes: {total_camas / pob * 1000:.2f}')\n",
            ]
            break

with open(nb_salud_path, "w", encoding="utf-8") as f:
    json.dump(nb_salud, f, indent=1, ensure_ascii=False)
print("[OK] 02_ingestion_salud.ipynb celda de camas corregida")

# 3. Corregir 00_ingestion_eda_master.ipynb
nb_master_path = ROOT / "notebooks" / "01_ingestion" / "00_ingestion_eda_master.ipynb"
with open(nb_master_path, "r", encoding="utf-8") as f:
    nb_master = json.load(f)

for cell in nb_master["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "url_poblacion" in source or "osb_demografia-poblacion-localidad.csv" in source:
            cell["source"] = [
                "# Ingesta oficial de Demografia DANE/SDP y PUA SDIS\n",
                "from src.ingestion.parse_demografia_dane import parse_all_demografia_dane\n",
                "from src.ingestion.parse_pua_sdis import parse_pua_sdis_indicadores\n",
                "\n",
                "df_loc_dane, df_2025, df_upz = parse_all_demografia_dane()\n",
                "print('Poblacion oficial DANE 2025:', df_2025.shape)\n",
                "df_pua = parse_pua_sdis_indicadores()\n",
                "print('Atenciones y Beneficiarios PUA SDIS 2024:', df_pua.shape)\n",
            ]
        elif "demo = pd.read_csv" in source and "DEMOGRAFIA" in source:
            cell["source"] = [
                "demo = pd.read_csv(str(ROOT / 'data' / 'processed' / 'DEMOGRAFIA' / 'poblacion_localidad_2025.csv'))\n",
                "display(demo.head())\n",
            ]

with open(nb_master_path, "w", encoding="utf-8") as f:
    json.dump(nb_master, f, indent=1, ensure_ascii=False)
print("[OK] 00_ingestion_eda_master.ipynb corregido")
