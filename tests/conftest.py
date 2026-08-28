import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en sys.path para pytest y VS Code Test Explorer
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
