"""Script para alinear completamente 01_ingestion_demografia.ipynb y 00_ingestion_eda_master.ipynb."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update_demografia_nb():
    nb_path = ROOT / "notebooks" / "01_ingestion" / "01_ingestion_demografia.ipynb"
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            if 'demo_loc.groupby("ANO")["POBLACION"]' in source or 'groupby("ANO")' in source:
                cell["source"] = [
                    "df_total = demo_loc[demo_loc['area'] == 'Total'] if 'area' in demo_loc.columns else demo_loc\n",
                    "col_ano = 'ano' if 'ano' in df_total.columns else 'ANO'\n",
                    "col_pob = 'poblacion_total' if 'poblacion_total' in df_total.columns else ('POBLACION' if 'POBLACION' in df_total.columns else df_total.columns[-1])\n",
                    "serie = df_total.groupby(col_ano)[col_pob].sum().sort_index()\n",
                    "serie.plot(kind='bar', figsize=(10, 4), title='Poblacion total de Bogota por ano (DANE/SDP)', color='#1f77b4')\n",
                    "plt.ylabel('habitantes')\n",
                    "plt.show()\n",
                    "print({int(a): f'{v:,.0f}' for a, v in serie.items()})\n",
                    "print(f'Variacion {int(serie.index.min())} -> {int(serie.index.max())}: {serie.iloc[-1] / serie.iloc[0] - 1:+.1%}')\n",
                ]
            elif "demo_loc[demo_loc['ANO']" in source or 'demo_loc["ANO"]' in source:
                cell["source"] = [
                    line.replace('demo_loc["ANO"]', 'demo_loc["ano"]')
                        .replace("demo_loc['ANO']", "demo_loc['ano']")
                        .replace('demo_loc["POBLACION"]', 'demo_loc["poblacion_total"]')
                        .replace("demo_loc['POBLACION']", "demo_loc['poblacion_total']")
                        .replace('demo_loc["CODIGO_LOCALIDAD"]', 'demo_loc["codigo_localidad"]')
                        .replace("demo_loc['CODIGO_LOCALIDAD']", "demo_loc['codigo_localidad']")
                        .replace('demo_loc["NOMBRE_LOCALIDAD"]', 'demo_loc["nombre_localidad"]')
                        .replace("demo_loc['NOMBRE_LOCALIDAD']", "demo_loc['nombre_localidad']")
                    for line in cell["source"]
                ]

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("[OK] 01_ingestion_demografia.ipynb actualizado.")


def update_master_eda_nb():
    nb_path = ROOT / "notebooks" / "01_ingestion" / "00_ingestion_eda_master.ipynb"
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            if "parse_pua_sdis_indicadores" in source or "parse_all_demografia_dane" in source:
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

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("[OK] 00_ingestion_eda_master.ipynb actualizado.")


if __name__ == "__main__":
    update_demografia_nb()
    update_master_eda_nb()
