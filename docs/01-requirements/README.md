# 01 - Requerimientos y descubrimiento de datos

Este directorio contiene los artefactos de la fase de descubrimiento de datos y el inventario inicial de `data/raw`.

Archivos y comandos principales:

- `scripts/inventory_data.py` — escanea `data/raw` y genera `docs/01-requirements/01-data-inventory.md`.
- `scripts/inspect_discovered.py` — inspecciona archivos crudos para mostrar capas, esquemas y metadatos.
- `scripts/build_eda_notebook.py` — genera un notebook de EDA prototipo en `notebooks/01_eda_descubrimiento.ipynb`.

Uso recomendado:

```powershell
cd c:\Users\ADAN\DataJam_DataOlinguitos_Gen
python scripts\inventory_data.py
python scripts\inspect_discovered.py
python scripts\build_eda_notebook.py
```

Requisitos:

- `pandas`
- `geopandas`
- `pyogrio`
- `nbformat`
- `openpyxl`
"