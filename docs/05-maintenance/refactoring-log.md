# Registro de Refactorizaciones y Optimización de Código

**Proyecto**: SIPTA | **Fase PDCO**: OPERATIONS  
**Marco Normativo**: SWEBOK Cap. 6 (Software Maintenance) / ISO/IEC 25010 (Mantenibilidad) / Clean Code / PEP 8  
**Versión**: `v1.0.0`  

---

### Refactorización 1: Resolución Jerárquica y Dinámica de Rutas (`ROOT` y `sys.path`)
- **Problema**: La dependencia de rutas relativas fijas como `../` o `../../` provocaba fallos de importación (`ModuleNotFoundError: No module named 'src'`) al ejecutar cuadernos desde distintas ubicaciones o subdirectorios de trabajo.
- **Solución**: Implementación de una resolución dinámica jerárquica con `Path('.').resolve()` inspeccionando la presencia de las carpetas `src/` y `data/`.

### Refactorización 2: Auto-Inicialización Resiliente en Cuadernos de Validación
- **Problema**: La ejecución aislada o fuera de secuencia de celdas secundarias arrojaba `NameError: name 'res' is not defined` si la primera celda no se había corrido en la sesión interactiva activa.
- **Solución**: Incorporación de bloques condicionales `if 'res' not in globals() or res is None:` en cada celda dependiente para auto-invocar la suite de validación sin interrumpir el flujo del analista.

### Refactorización 3: Depuración y Limpieza Arquitectural del Repositorio
- **Problema**: Existían 11 cuadernos sueltos preliminares en la raíz de `notebooks/` y 13 scripts auxiliares temporales en `scripts/` que generaban ambigüedad y deuda técnica.
- **Solución**: Eliminación total de stubs residuales y carpetas legadas (`notebooks/eda/`), conservando exclusivamente los 26 notebooks estructurados por fase y los scripts productivos de adquisición y reproyección de datos (`download_missing_data.py`, `generate_domain_reports.py` y `prepare_education_geojson.py`).

### Refactorización 4: Fallback de Visualización y Manejo Headless
- **Problema**: Bloqueos en ejecuciones por lotes de scripts o pruebas unitarias debido a llamadas interactivas a `plt.show()`.
- **Solución**: Configuración del backend headless `matplotlib.use('Agg')` y mockeo de ventanas interactivas en suites de integración.

### Refactorización 5: Estandarización de Esquemas y Reproyección Geoespacial
- **Problema**: GeoJSON de oferta educativa con sistemas de coordenadas proyectadas locales incompatibles con capas WGS84.
- **Solución**: Pipeline de reproyección automática en `src/cleaning/clean_data.py` y script determinista `scripts/prepare_education_geojson.py` a `EPSG:4326`.

### Refactorización 6: Higiene, Purga de Artefactos y Depuración Pre-Entrega
- **Problema**: Presencia de carpetas de profiling transitorio (`reports/eda/tiempos/`, `reports/eda/cache/`), entornos virtuales duplicados (`.venv-1/`), cachés de pruebas (`.pytest_cache/`) y scripts utilitarios de desarrollo puntual en `scripts/` que agregaban ruido y sobrepeso al repositorio final.
- **Solución**: Depuración exhaustiva de carpetas temporales, blindaje de exclusiones en `.gitignore` y consolidación exclusiva de los scripts productivos reproducibles (`download_missing_data.py`, `generate_domain_reports.py`, `prepare_education_geojson.py`).

### Refactorización 7: Estandarización Canónica, Empaquetado `pyproject.toml` y Desacoplamiento Declarativo (ADR-005)
- **Problema**: Documentos sueltos en `docs/` fuera de las fases PDCO, parámetros numéricos de ponderación IPT acoplados en código y dependencia exclusiva de hacks de `sys.path`.
- **Solución**:
  1. Reubicación canónica de `FORMULARIO_CARACTERIZACION_FORMULACION_PROBLEMAS.md` a `docs/01-requirements/` y `NOTA_TECNICA_INTEGRACION_DATOS_PUBLICOS.md` a `docs/02-architecture/`.
  2. Implementación de `pyproject.toml` bajo PEP 621 para empaquetado editable universal (`pip install -e .`).
  3. Centralización declarativa de los 5 escenarios de sensibilidad del IPT en `config/ipt_weights.json` y desacoplamiento en `src/modeling/calculate_indicators.py` con función `load_ipt_weights_config()`.
  4. Exclusión de `scratch/` y logs en `.gitignore`.
