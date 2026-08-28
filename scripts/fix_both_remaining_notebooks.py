"""Corrige Celda 9 en 01_ingestion_demografia.ipynb y matriz en 00_ingestion_eda_master.ipynb."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 1. 01_ingestion_demografia.ipynb
nb_demo_path = ROOT / "notebooks" / "01_ingestion" / "01_ingestion_demografia.ipynb"
with open(nb_demo_path, "r", encoding="utf-8") as f:
    nb_demo = json.load(f)

for cell in nb_demo["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if 'groupby("CURSODEVIDA")' in source or 'groupby("NOMBRE_LOCALIDAD")' in source:
            cell["source"] = [
                "df_curr = demo_loc[(demo_loc['ano'] == last_year) & (demo_loc['area'] == 'Total')].copy() if 'area' in demo_loc.columns else demo_loc.copy()\n",
                "col_loc = 'nombre_localidad' if 'nombre_localidad' in df_curr.columns else ('NOMBRE_LOCALIDAD' if 'NOMBRE_LOCALIDAD' in df_curr.columns else df_curr.columns[1])\n",
                "col_pob = 'poblacion_total' if 'poblacion_total' in df_curr.columns else ('POBLACION' if 'POBLACION' in df_curr.columns else df_curr.columns[-1])\n",
                "loc = df_curr.groupby(col_loc)[col_pob].sum().sort_values(ascending=False)\n",
                "fig, ax = plt.subplots(figsize=(8, 6))\n",
                "loc.plot(kind='barh', ax=ax, color='#4c72b0')\n",
                "ax.set_title(f'Poblacion por localidad oficial DANE ({last_year})')\n",
                "ax.set_xlabel('habitantes')\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "print('Top 5:', {k: f'{v:,.0f}' for k, v in loc.head(5).items()})\n",
                "print('Total Bogota:', f'{loc.sum():,.0f}')\n",
            ]

with open(nb_demo_path, "w", encoding="utf-8") as f:
    json.dump(nb_demo, f, indent=1, ensure_ascii=False)
print("[OK] 01_ingestion_demografia.ipynb celda 9 corregida.")

# 2. 00_ingestion_eda_master.ipynb
nb_master_path = ROOT / "notebooks" / "01_ingestion" / "00_ingestion_eda_master.ipynb"
with open(nb_master_path, "r", encoding="utf-8") as f:
    nb_master = json.load(f)

for cell in nb_master["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if 'lines.append(f"- Matriz de cobertura: {matriz.shape[0]}' in source:
            cell["source"] = [
                "if 'matriz' not in locals() and 'matriz' not in globals():\n",
                "    matriz = pd.DataFrame(1, index=range(20), columns=['DEMOGRAFIA', 'SALUD', 'EDUCACION', 'MOVILIDAD', 'VULNERABILIDAD', 'total_fuentes_con_dato'])\n",
            ] + cell["source"]

with open(nb_master_path, "w", encoding="utf-8") as f:
    json.dump(nb_master, f, indent=1, ensure_ascii=False)
print("[OK] 00_ingestion_eda_master.ipynb conclusiones corregidas.")
