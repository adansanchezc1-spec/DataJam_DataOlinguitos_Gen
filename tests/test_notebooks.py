"""Suite de pruebas automatizadas para validación y ejecución de todos los Notebooks de SIPTA.

Fase PDCO: CONTROL | Framework: pytest | Patrón: AAA (Arrange-Act-Assert)
Estándares: IEEE 829 / ISO 25010 / SWEBOK Cap. 4
Cobertura: 100% de los 25 Notebooks del repositorio (01_ingestion, 02_validation, 03_integration, 04_modeling, 05_visualization)
"""

from __future__ import annotations

import ast
import os
from pathlib import Path
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat
import pytest

# Directorio raíz del repositorio
ROOT_DIR = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"

# Descubrimiento determinista de todos los cuadernos .ipynb
ALL_NOTEBOOK_PATHS = sorted(list(NOTEBOOKS_DIR.glob("**/*.ipynb")))
ALL_NOTEBOOK_IDS = [p.relative_to(ROOT_DIR).as_posix() for p in ALL_NOTEBOOK_PATHS]


class TestNotebooksDiscovery:
    """Valida el catálogo e inventario completo de los cuadernos de la solución."""

    def test_all_25_notebooks_discovered(self) -> None:
        """Verifica que los 25 notebooks del catálogo maestro existan en el repositorio."""
        # Assert
        assert len(ALL_NOTEBOOK_PATHS) == 25, f"Se esperaban 25 notebooks, se encontraron {len(ALL_NOTEBOOK_PATHS)}"


class TestNotebooksStructureAndSchema:
    """Valida la integridad de esquema JSON y nbformat v4 para cada cuaderno."""

    @pytest.mark.parametrize("nb_path", ALL_NOTEBOOK_PATHS, ids=ALL_NOTEBOOK_IDS)
    def test_notebook_json_and_nbformat_schema(self, nb_path: Path) -> None:
        """Verifica que el notebook sea un JSON válido y cumpla con el estándar nbformat v4."""
        # Arrange & Act
        nb = nbformat.read(str(nb_path), as_version=4)

        # Assert
        assert nb.nbformat >= 4
        assert len(nb.cells) > 0, f"El notebook {nb_path.name} no contiene celdas"
        assert "metadata" in nb


class TestNotebooksSyntax:
    """Valida estáticamente que todas las celdas de código de cada cuaderno tengan sintaxis Python válida."""

    @pytest.mark.parametrize("nb_path", ALL_NOTEBOOK_PATHS, ids=ALL_NOTEBOOK_IDS)
    def test_notebook_code_cells_have_valid_syntax(self, nb_path: Path) -> None:
        """Verifica que todas las celdas de código compilen mediante AST sin errores de sintaxis."""
        # Arrange
        nb = nbformat.read(str(nb_path), as_version=4)
        code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]

        # Act & Assert
        for idx, cell in enumerate(code_cells, start=1):
            source = cell.source
            # Filtrar comandos mágicos de IPython (% y !) para análisis AST
            lines = [
                line
                for line in source.splitlines()
                if not line.strip().startswith(("%", "!"))
            ]
            clean_code = "\n".join(lines)
            if not clean_code.strip():
                continue

            try:
                ast.parse(clean_code)
            except SyntaxError as e:
                pytest.fail(f"Error de sintaxis en {nb_path.name} celda #{idx}: {e}")


class TestNotebooksExecution:
    """Ejecuta de manera automatizada celda por celda todos y cada uno de los 25 notebooks."""

    @pytest.mark.parametrize("nb_path", ALL_NOTEBOOK_PATHS, ids=ALL_NOTEBOOK_IDS)
    def test_notebook_executes_end_to_end_without_errors(self, nb_path: Path) -> None:
        """Ejecuta secuencialmente el cuaderno completo garantizando 0 excepciones no controladas."""
        # Arrange
        nb = nbformat.read(str(nb_path), as_version=4)
        code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]

        # Asegurar sys.path con la raíz del proyecto
        if str(ROOT_DIR) not in sys.path:
            sys.path.insert(0, str(ROOT_DIR))

        # Espacio de nombres aislado para la ejecución del notebook
        namespace = {
            "__file__": str(nb_path),
            "__name__": "__main__",
            "display": lambda *args, **kwargs: None,
            "get_ipython": lambda: None,
            "SMOKE": True,
        }

        orig_cwd = os.getcwd()
        plt.close("all")
        os.environ["EDA_SMOKE"] = "1"

        # Act & Assert
        try:
            # Establecer el directorio de trabajo en la carpeta del notebook
            os.chdir(str(nb_path.parent))

            for idx, cell in enumerate(code_cells, start=1):
                source = cell.source
                # Filtrar líneas mágicas de IPython
                lines = [
                    line
                    for line in source.splitlines()
                    if not line.strip().startswith(("%", "!"))
                ]
                code = "\n".join(lines)
                if not code.strip():
                    continue

                try:
                    exec(code, namespace)
                except Exception as ex:
                    pytest.fail(
                        f"Fallo en {nb_path.relative_to(ROOT_DIR).as_posix()} | Celda #{idx}:\n"
                        f"Tipo: {type(ex).__name__}\n"
                        f"Mensaje: {ex}\n"
                        f"Código fuente de la celda:\n{code}"
                    )
        finally:
            os.chdir(orig_cwd)
            plt.close("all")
