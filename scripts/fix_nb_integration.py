import json
from pathlib import Path

p = Path("notebooks/03_integration/01_integration_master.ipynb")
with open(p, "r", encoding="utf-8") as f:
    nb = json.load(f)

setup_code = [
    "import sys\n",
    "import logging\n",
    "from pathlib import Path\n",
    "\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Configuracion de rutas relativas a la raiz del repositorio\n",
    "ROOT = Path.cwd().resolve()\n",
    'if ROOT.name in ["03_integration", "notebooks"]:\n',
    '    ROOT = ROOT.parents[1] if ROOT.name == "03_integration" else ROOT.parent\n',
    "\n",
    "if str(ROOT) not in sys.path:\n",
    "    sys.path.insert(0, str(ROOT))\n",
    "\n",
    "# Importacion modular de componentes SIPTA\n",
    "from src.integration.integrate_data import (\n",
    "    get_canonical_localities_base,\n",
    "    merge_by_locality,\n",
    "    load_demografia_localidades,\n",
    "    load_vulnerabilidad_social_sdis,\n",
    "    load_movilidad_infraestructura_coverage,\n",
    "    build_master_table,\n",
    "    save_master_table,\n",
    ")\n",
    "from src.cleaning.clean_data import MAPA_HOMOLOGACION_LOCALIDADES, standardize_column_names\n",
    "from src.features.feature_engineering import add_density, add_ratio, save_feature_table\n",
    "from src.evaluation.evaluate_results import quality_report, detect_outliers, save_quality_report\n",
    "\n",
    'print(f"[OK] Entorno configurado correctamente. Directorio raiz: {ROOT}")\n',
]

nb["cells"][2]["source"] = setup_code

with open(p, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("[OK] Celda de setup corregida en 01_integration_master.ipynb.")
