"""Actualiza 01_validation_demografia.ipynb."""

import json
from pathlib import Path

nb_path = Path("notebooks/02_validation/01_validation_demografia.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "Demostracion de denominadores demograficos" in source or "col_anio" in source:
            cell["source"] = [
                "# 1. Poblacion oficial DANE 2025 por Localidad\n",
                "if 'ano' in df_loc.columns and 'area' in df_loc.columns:\n",
                "    df_2025 = df_loc[(df_loc['ano'] == 2025) & (df_loc['area'] == 'Total')].copy()\n",
                "else:\n",
                "    df_2025 = df_loc.copy()\n",
                "col_pob = 'poblacion_total' if 'poblacion_total' in df_2025.columns else ('poblacion_2025' if 'poblacion_2025' in df_2025.columns else df_2025.columns[-1])\n",
                "print('Demostracion de denominadores demograficos oficiales DANE / SDP (2025):')\n",
                "print(f'Total Poblacion Bogota 2025: {df_2025[col_pob].sum():,}')\n",
                "display(df_2025.head(10))\n",
            ]
            print("Updated cell in 01_validation_demografia.ipynb")

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
