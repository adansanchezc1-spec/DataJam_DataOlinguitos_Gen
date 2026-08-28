"""Script para actualizar y alinear todos los notebooks de SIPTA con las fuentes oficiales.

Fuentes:
1. DANE / SDP: anexo-proyecciones-poblacion-bogota-desagreacion-loc-2018-2035-UPZ-2018-2024.xlsx
2. SDIS: pua_riesgo_y_anon_20250911_193636-1.xlsx
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"


def update_demografia_notebook():
    nb_path = NOTEBOOKS_DIR / "01_ingestion" / "01_ingestion_demografia.ipynb"
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Actualizar la primera celda de código
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            if "osb_demografia-poblacion-localidad.csv" in source and "RAW_DIR" in source:
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
                    "# Ingesta de la ÚNICA fuente oficial vinculante de población DANE / SDP (2018-2035)\n",
                    "from src.ingestion.parse_demografia_dane import parse_all_demografia_dane\n",
                    "\n",
                    "df_loc_dane, df_2025, df_upz = parse_all_demografia_dane()\n",
                    "print('Proyecciones DANE/SDP por Localidad (2018-2035):', df_loc_dane.shape)\n",
                    "print('Población Oficial 2025 (20 Localidades):', df_2025.shape)\n",
                    "display(df_2025.head())\n",
                    "print('Proyecciones DANE/SDP por UPZ (2018-2024):', df_upz.shape)\n",
                ]
                break

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"[OK] Actualizado {nb_path}")


def update_validation_demografia_notebook():
    nb_path = NOTEBOOKS_DIR / "02_validation" / "01_validation_demografia.ipynb"
    if nb_path.exists():
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = json.load(f)

        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                if "osb_demografia-poblacion-localidad.csv" in source:
                    cell["source"] = [
                        line.replace(
                            "osb_demografia-poblacion-localidad.csv",
                            "poblacion_localidad_2025.csv"
                        )
                        for line in cell["source"]
                    ]

        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"[OK] Actualizado {nb_path}")


def update_modeling_notebook():
    nb_path = NOTEBOOKS_DIR / "04_modeling" / "01_modeling_ipt.ipynb"
    if nb_path.exists():
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = json.load(f)

        # Actualizar celda de cálculo
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                if "build_consolidated_locality_metrics" in source and "calculate_multidimensional_ipt" in source:
                    cell["source"] = [
                        "from src.modeling.calculate_indicators import (\n",
                        "    build_consolidated_locality_metrics,\n",
                        "    calculate_multidimensional_ipt,\n",
                        "    calculate_consensus_priority,\n",
                        "    calculate_geometric_ipt,\n",
                        "    calculate_bootstrap_confidence_intervals,\n",
                        "    DIMENSION_COLUMNS,\n",
                        ")\n",
                        "from scripts.recalculate_ipt_model import run_ipt_modeling_pipeline\n",
                        "\n",
                        "# Ejecutar pipeline integral actualizado con DANE 2025 y PUA SDIS\n",
                        "prioritized_df, model_df = run_ipt_modeling_pipeline()\n",
                        "display(prioritized_df[['codigo_localidad', 'localidad', 'IPT_MULTIDIMENSIONAL', 'IPT_GEOMETRICO', 'ranking_consenso', 'nivel_prioridad_consenso']].head(10))\n",
                    ]
                    break

        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"[OK] Actualizado {nb_path}")


if __name__ == "__main__":
    update_demografia_notebook()
    update_validation_demografia_notebook()
    update_modeling_notebook()
    print("Todos los notebooks actualizados exitosamente.")
