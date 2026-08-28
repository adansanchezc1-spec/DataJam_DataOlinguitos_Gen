"""Corrige las celdas restantes de 00_ingestion_eda_master.ipynb y 01_ingestion_demografia.ipynb."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 1. Corregir 00_ingestion_eda_master.ipynb
nb_master_path = ROOT / "notebooks" / "01_ingestion" / "00_ingestion_eda_master.ipynb"
with open(nb_master_path, "r", encoding="utf-8") as f:
    nb_master = json.load(f)

for cell in nb_master["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if 'df_poblacion["CODIGO_LOCALIDAD"]' in source or 'df_poblacion["NOMBRE_LOCALIDAD"]' in source:
            cell["source"] = [
                "col_cod = 'codigo_localidad' if 'codigo_localidad' in df_poblacion.columns else 'CODIGO_LOCALIDAD'\n",
                "col_nom = 'nombre_localidad' if 'nombre_localidad' in df_poblacion.columns else 'NOMBRE_LOCALIDAD'\n",
                "print('=== CODIGOS DE LOCALIDAD ===')\n",
                "print(sorted(df_poblacion[col_cod].dropna().unique()))\n",
                "\n",
                "print('\\n=== NOMBRES DE LOCALIDAD ===')\n",
                "print(sorted(df_poblacion[col_nom].dropna().unique()))\n",
                "\n",
                "print('\\n=== CANTIDAD DE CODIGOS UNICOS ===')\n",
                "print(df_poblacion[col_cod].nunique())\n",
                "\n",
                "print('\\n=== CANTIDAD DE NOMBRES UNICOS ===')\n",
                "print(df_poblacion[col_nom].nunique())\n",
                "\n",
                "print('\\n=== RELACION CODIGO - LOCALIDAD ===')\n",
                "display(df_poblacion[[col_cod, col_nom]].drop_duplicates().sort_values(col_cod))\n",
            ]
        elif 'df_poblacion["ANO"]' in source or "df_poblacion['ANO']" in source:
            cell["source"] = [
                "col_ano = 'ano' if 'ano' in df_poblacion.columns else ('ANO' if 'ANO' in df_poblacion.columns else None)\n",
                "if col_ano:\n",
                "    print('Anos disponibles:', sorted(df_poblacion[col_ano].dropna().unique()))\n",
                "else:\n",
                "    print('Dataset poblacional 2025 consolidado para las 20 localidades.')\n",
            ]

with open(nb_master_path, "w", encoding="utf-8") as f:
    json.dump(nb_master, f, indent=1, ensure_ascii=False)
print("[OK] 00_ingestion_eda_master.ipynb corregido totalmente.")

# 2. Corregir 01_ingestion_demografia.ipynb
nb_demo_path = ROOT / "notebooks" / "01_ingestion" / "01_ingestion_demografia.ipynb"
with open(nb_demo_path, "r", encoding="utf-8") as f:
    nb_demo = json.load(f)

for cell in nb_demo["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if 'py["EDAD"]' in source or 'Piramide de edades' in source or 'piv.pivot_table' in source:
            cell["source"] = [
                "py = demo_loc[(demo_loc['ano'] == last_year) & (demo_loc['area'] == 'Total')].copy() if 'area' in demo_loc.columns else demo_loc.copy()\n",
                "age_cols = ['poblacion_0_5', 'poblacion_6_11', 'poblacion_12_17', 'poblacion_18_59', 'poblacion_60_mas']\n",
                "existing_age = [c for c in age_cols if c in py.columns]\n",
                "if existing_age:\n",
                "    age_labels = ['0 a 5 anos', '6 a 11 anos', '12 a 17 anos', '18 a 59 anos', '60+ anos'][:len(existing_age)]\n",
                "    sums = [py[c].sum() for c in existing_age]\n",
                "    fig, ax = plt.subplots(figsize=(8, 4.5))\n",
                "    ax.barh(age_labels, sums, color='#4c72b0')\n",
                "    ax.set_xlabel('Habitantes')\n",
                "    ax.set_title(f'Estructura por Curso de Vida de Bogota DANE/SDP ({last_year})')\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "    print({lbl: f'{val:,.0f}' for lbl, val in zip(age_labels, sums)})\n",
            ]

with open(nb_demo_path, "w", encoding="utf-8") as f:
    json.dump(nb_demo, f, indent=1, ensure_ascii=False)
print("[OK] 01_ingestion_demografia.ipynb corregido totalmente.")
