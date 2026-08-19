"""Script para probar la ejecución real de todos los notebooks de validación y detectar errores en src."""

import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAL_DIR = ROOT / "notebooks" / "02_validation"

sys.path.insert(0, str(ROOT))


def run_notebook_cells(nb_path: Path):
    print(f"\n--- Probando ejecucion de {nb_path.name} ---")
    data = json.loads(nb_path.read_text(encoding="utf-8"))
    
    # Crear un namespace local para la ejecución del notebook
    nb_globals = {
        "__name__": "__main__",
        "__file__": str(nb_path),
        "ROOT": ROOT,
    }
    
    for idx, cell in enumerate(data.get("cells", [])):
        if cell.get("cell_type") == "code":
            code = "".join(cell.get("source", []))
            try:
                # Reemplazar display por print si no estamos en entorno interactivo
                exec_code = code.replace("display(", "print(")
                exec(exec_code, nb_globals)
            except Exception as e:
                print(f"[ERROR] en celda {idx} de {nb_path.name}:")
                traceback.print_exc()
                return False
    print(f"[OK] {nb_path.name} ejecutado con exito.")
    return True


def test_all():
    failed = []
    for nb in sorted(VAL_DIR.glob("*.ipynb")):
        ok = run_notebook_cells(nb)
        if not ok:
            failed.append(nb.name)
    
    print("\n===============================")
    if failed:
        print(f"[FALLO] Notebooks con errores: {failed}")
    else:
        print("[EXITO] Todos los notebooks de validacion se ejecutaron sin errores.")


if __name__ == "__main__":
    test_all()
