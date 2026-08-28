# Herramientas de Automatización SIPTA

Este directorio contiene las herramientas automatizadas de generación de reportes del Sistema de Integración y Priorización Territorial de Bogotá (SIPTA).

---

## 🛠️ Script Operacional

| Script | Descripción | Uso / Comando |
| :--- | :--- | :--- |
| [`generate_domain_reports.py`](generate_domain_reports.py) | **Generador Automatizado de Reportes**: Compila los 13 reportes sectoriales en Markdown y genera figuras cartográficas y estadísticas en alta resolución (300 DPI) en `reports/figures/`. | `python scripts/generate_domain_reports.py` |

---

## 📋 Estándares de Ejecución
- El script opera de forma no destructiva sobre las carpetas canónicas `data/curated/` y `reports/`.
- La ejecución se realiza desde la raíz del repositorio con el entorno virtual activado.
