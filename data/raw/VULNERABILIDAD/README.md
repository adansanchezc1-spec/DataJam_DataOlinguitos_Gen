# SIPTA — Guía Sectorial: Vulnerabilidad Social y Asistencia Distrital (PUA SDIS)
**Versión**: 2.0 | **Fecha**: 2026-08-27 | **Fase PDCO**: DEVELOPMENT -> CONTROL  
**Estándares**: DAMA-BOK, IEEE 830 (RF-019), SWEBOK Cap. 1 & 2  

---

## 1. Objetivo Sectorial
Procesar e integrar los microdatos administrativos reales del Plan Único de Atención (PUA) de la Secretaría Distrital de Integración Social (SDIS) y el Registro de Vendedores Informales (RIVI - IPES) para cuantificar la demanda real de transferencias monetarias, subsidios alimentarios, atención en crisis familiares y comercio informal.

---

## 2. Fuente Oficial de Microdatos Administrativos
- **Dataset Primario**: `data/raw/VULNERABILIDAD/pua_riesgo_y_anon_20250911_193636-1.xlsx`
- **Autoridad Emisora**: SDIS (Secretaría Distrital de Integración Social).
- **Volumen**: **1.048.575 registros individuales anonimizados** con coordenadas y localidad de atención.
- **Cobertura Temática**:
  - **Ingreso Mínimo Garantizado (IMG)**: 666.711 atenciones / 173.056 beneficiarios únicos.
  - **Comedores Comunitarios y Apoyo Nutricional**: 136.216 atenciones / 43.626 beneficiarios únicos.
  - **Comisarías de Familia**: 88.544 atenciones de violencia intrafamiliar y protección.
  - **Habitante de Calle**: 9.510 atenciones integrales.

---

## 3. Artefactos Procesados (`data/processed/VULNERABILIDAD/`)
1. `pua_sdis_indicadores_localidad.csv`: Tabla agregada canónica por localidad (20 filas) con conteos de atenciones, beneficiarios únicos y tasas per cápita por 10.000 habitantes.

---

## 4. Indicadores Derivados
| Código | Indicador | Fórmula | Unidad | Nivel Territorial |
|---|---|---|---|---|
| `VUL-001` | Tasa de Atenciones IMG | $\text{Atenciones IMG} / \text{Población}_{2025} \times 10.000$ | por 10k hab | Localidad |
| `VUL-002` | Tasa de Beneficiarios Comedores | $\text{Beneficiarios Comedores} / \text{Población}_{2025} \times 10.000$ | por 10k hab | Localidad |
| `VUL-003` | Tasa de Atenciones en Comisarías | $\text{Atenciones Comisarías} / \text{Población}_{2025} \times 10.000$ | por 10k hab | Localidad |
| `VUL-004` | Atenciones Habitante de Calle | $\sum \text{Atenciones Habitante Calle}$ | atenciones | Localidad |

---

## 5. Checklist de Calidad DAMA-BOK
- [x] Parsing de microdatos PUA en `src/ingestion/parse_pua_sdis.py`.
- [x] Imputación espacial canónica y homologación DIVIPOLA (20 localidades).
- [x] Integración en dimensión de Vulnerabilidad Social del IPT ($s_{i, \text{vuln}}$).
- [x] Validación en `tests/test_validation.py`.
