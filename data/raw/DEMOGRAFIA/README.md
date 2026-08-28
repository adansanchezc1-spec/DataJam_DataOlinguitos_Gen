# SIPTA — Guía Sectorial: Demografía
**Versión**: 2.0 | **Fecha**: 2026-08-27 | **Fase PDCO**: DEVELOPMENT -> CONTROL  
**Estándares**: DAMA-BOK, IEEE 830 (RF-018), SWEBOK Cap. 1 & 2  

---

## 1. Objetivo Sectorial
Proveer la base poblacional oficial y única (Proyecciones de Población DANE / Secretaría Distrital de Planeación 2018–2035) y la delimitación espacial oficial (DIVIPOLA) necesaria para construir el modelo territorial unificado y normalizar per cápita los indicadores de los 12 dominios sectoriales.

---

## 2. Fuente Oficial Única Autorizada
- **Dataset Primario**: `data/raw/DEMOGRAFIA/anexo-proyecciones-poblacion-bogota-desagreacion-loc-2018-2035-UPZ-2018-2024.xlsx`
- **Autoridad Emisora**: DANE (Departamento Administrativo Nacional de Estadística) / SDP (Secretaría Distrital de Planeación).
- **Cobertura Temporal**: 2018 a 2035 (Serie histórica y proyecciones oficiales).
- **Corte de Referencia Distrital**: **Año 2025** — **8.101.412 habitantes** en Bogotá D.C.
- **Desagregación**: 20 Localidades oficiales y 112 UPZ.

---

## 3. Artefactos Procesados (`data/processed/DEMOGRAFIA/`)
1. `poblacion_localidad_2025.csv`: Denominador oficial canónico para 2025 (20 localidades).
2. `poblacion_localidad_dane_sdp.csv`: Serie temporal multianual completa 2018–2035 desagregada por sexo y grupos etarios quinquenales.
3. `poblacion_upz_dane_sdp.csv`: Serie temporal por Unidades de Planeamiento Zonal (UPZ).

---

## 4. Indicadores Derivados
| Código | Indicador | Fórmula | Unidad | Nivel Territorial |
|---|---|---|---|---|
| `DEM-001` | Densidad Poblacional | $\text{Población}_{2025} / \text{Área}(\text{km}^2)$ | hab/km² | Localidad |
| `POB-002` | Razón de Dependencia Infantil | $\text{Pob}(0\text{--}14) / \text{Pob}(15\text{--}59) \times 100$ | % | Localidad |
| `POB-003` | Índice de Envejecimiento | $\text{Pob}(60+) / \text{Pob}(0\text{--}14) \times 100$ | % | Localidad |

---

## 5. Checklist de Calidad DAMA-BOK
- [x] Unificación bajo Proyecciones Oficiales DANE / SDP (ADR-006).
- [x] Verificación de coincidencia DIVIPOLA al 100% (20 localidades).
- [x] Parsing automatizado en `src/ingestion/parse_demografia_dane.py`.
- [x] Pruebas unitarias de esquema y sumas de control en `tests/test_validation.py`.