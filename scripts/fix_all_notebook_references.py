"""Actualiza sistemáticamente todas las referencias a datos demográficos en los notebooks."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"


def fix_notebook_file(nb_path: Path):
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    modified = False
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source_lines = cell.get("source", [])
            full_source = "".join(source_lines)
            
            # Reemplazar lectura directa de osb_demografia-poblacion-localidad.csv
            if "osb_demografia-poblacion-localidad.csv" in full_source or "DEMOGRAFIA_POBLACION" in full_source:
                new_lines = []
                for line in source_lines:
                    if 'read_csv(str(RAW_DIR / "DEMOGRAFIA_POBLACION" / "osb_demografia-poblacion-localidad.csv")' in line or \
                       'read_csv(file_loc' in line or \
                       'DEMOGRAFIA_POBLACION/osb_demografia-poblacion-localidad.csv' in line:
                        new_lines.append(
                            line.replace(
                                'str(RAW_DIR / "DEMOGRAFIA_POBLACION" / "osb_demografia-poblacion-localidad.csv")',
                                'str(ROOT / "data" / "processed" / "DEMOGRAFIA" / "poblacion_localidad_2025.csv")'
                            ).replace(
                                'data/raw/DEMOGRAFIA_POBLACION/osb_demografia-poblacion-localidad.csv',
                                'data/processed/DEMOGRAFIA/poblacion_localidad_2025.csv'
                            ).replace('sep=";", ', '')
                        )
                        modified = True
                    elif 'demo["ANO"] == demo["ANO"].max()' in line:
                        new_lines.append('pob = demo["poblacion_2025"].sum() if "poblacion_2025" in demo.columns else 8101412\n')
                        modified = True
                    elif 'demo["ANO"].max()' in line:
                        new_lines.append(line.replace('demo["ANO"].max()', '2025'))
                        modified = True
                    elif 'demo["POBLACION"]' in line and "poblacion_2025" not in line:
                        new_lines.append('col_pob = "poblacion_2025" if "poblacion_2025" in demo.columns else demo.columns[-1]\n')
                        modified = True
                    else:
                        new_lines.append(
                            line.replace(
                                'DEMOGRAFIA_POBLACION', 'DEMOGRAFIA'
                            ).replace(
                                'osb_demografia-poblacion-localidad.csv',
                                'poblacion_localidad_2025.csv'
                            )
                        )
                cell["source"] = new_lines

    if modified:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"[OK] Corregido: {nb_path.name}")


def main():
    for nb_path in NOTEBOOKS_DIR.glob("**/*.ipynb"):
        fix_notebook_file(nb_path)


if __name__ == "__main__":
    main()
