# Development Log — SIPTA Pipeline
**Proyecto**: DataJam_DataOlinguitos_Gen (SIPTA)  
**Sprint / Iteración**: Sprint 1 - 2  
**Fecha**: 2026-08-15  
**Fase PDCO**: DEVELOPMENT  
**Skill Activa**: `software-development`  

---

## 1. Módulos Desarrollados / Corregidos

| Módulo | Descripción | Requerimientos / Workflow | Estado |
|:---|:---|:---|:---|
| `src/ingestion/ingest_data.py` | Ingesta polimórfica (CSV, XLSX, GPKG, GeoJSON, ZIP) y manifiesto | 1.2 Ingesta de datos | ✅ Completo |
| `src/validation/validate_data.py` | Calidad de datos, nulos, duplicados y validación contra 20 localidades D.C. | 1.3 Validación de datos | ✅ Completo |
| `src/cleaning/clean_data.py` | Normalización snake_case, casteo numérico y tabla oficial de homologación | 1.4 Limpieza y estandarización | ✅ Completo |
| `src/integration/integrate_data.py` | Resolución de ruta raíz y merge territorial por localidad canónica | 1.5 Integración territorial | ✅ Completo |
| `src/modeling/calculate_indicators.py` | Normalización Min-Max e IPT compuesto ponderado | 1.6 Modelado e indicadores | ✅ Completo |
| `src/visualization/prepare_visualization.py` | Resolución de ruta y generación de ranking para dashboard | 1.7 Visualización | ✅ Completo |
| `docs/diccionario_datos.md` | Catálogo de variables, unidades y reglas de homologación | Documentación transversal | ✅ Completo |

---

## 2. Corrección de Notebooks

| Notebook | Correcciones Realizadas | Estado |
|:---|:---|:---|
| `notebooks/01_ingestion.ipynb` | Sincronizado con `src.ingestion`, catálogo dinámico de fuentes crudas y manifiesto. | ✅ Operativo |
| `notebooks/02_validation.ipynb` | Sincronizado con `src.validation`, perfil de esquema y validación de cobertura de 20 localidades. | ✅ Operativo |
| `notebooks/03_integration.ipynb` | Reparado syntax error en celda JSON, integrado con `src.cleaning` y `src.integration`. | ✅ Operativo |
| `notebooks/04_modeling.ipynb` | Sincronizado con `src.modeling`, cálculo de tasas y ensamble de IPT. | ✅ Operativo |
| `notebooks/05_visualization.ipynb` | Sincronizado con `src.visualization`, ranking y exportación curada para dashboard. | ✅ Operativo |

---

## 3. Registro de Contribuciones y Autoría — Persona C (Sofía Hidalgo)

| Hash Commit | Tipo / Scope | Mensaje del Commit / Entregable | Módulos / Archivos Impactados | Autoría |
| :--- | :--- | :--- | :--- | :--- |
| `c9b97b7` | `docs(diccionario)` | Registrar metadatos del dataset consolidado de vendedores informales | `docs/diccionario_datos.md`, `docs/01-requirements/E02_diccionario_datos.md` | Persona C (Sofía Hidalgo) |
| `5951a50` | `feat(ingestion)` | Actualizar notebook de finanzas con vendedores y puntos de encuentro | `notebooks/01_ingestion/06_ingestion_finanzas.ipynb` | Persona C (Sofía Hidalgo) |
| `d519dfb` | `data(raw)` | Punto de encuentro vendedores archivo excel | `data/raw/FINANZAS_INVERSION_PUBLICA/Punto de encuentro vendedores. Bogotá D.C..xlsx` | Persona C (Sofía Hidalgo) |
| `6988b33` | `feat(ingestion)` | Agregar archivos txt de vendedores informales por localidad y punto de encuentro vendedores GEOJSON | `data/raw/FINANZAS_INVERSION_PUBLICA/rivi-numero-*.txt`, `Punto de encuentro vendedores. Bogotá D.C..geojson` | Persona C (Sofía Hidalgo) |
| `ccd11cb` | `docs(diccionario)` | Registrar metadatos del dataset de seguridad cuadrantes | `docs/diccionario_datos.md`, `docs/01-requirements/E02_diccionario_datos.md` | Persona C (Sofía Hidalgo) |
| `9f9cc2f` | `feat(ingestion)` | Crear notebook de ingesta para dominio seguridad | `notebooks/01_ingestion/08_ingestion_seguridad.ipynb` | Persona C (Sofía Hidalgo) |
| `d0f2c83` | `docs(diccionario)` | Agregar metadatos de datasets de ambiente | `docs/diccionario_datos.md`, `docs/01-requirements/E02_diccionario_datos.md` | Persona C (Sofía Hidalgo) |
| `3506416` | `feat(ingestion)` | Crear notebook de ingesta para dominio ambiente | `notebooks/01_ingestion/07_ingestion_ambiental.ipynb` | Persona C (Sofía Hidalgo) |

---

## 4. Decisiones de Arquitectura e Implementación (ADR Breve)

- **DI-001**: Estandarización de `ROOT` en todos los módulos de `src/` a `Path(__file__).resolve().parents[2]` para eliminar la creación no deseada de `src/data/` y consolidar la lectura/escritura en la raíz `data/`.
- **DI-002**: Catálogo explícito de las 20 localidades de Bogotá con código de orden y código oficial DIVIPOLA (`1100101` a `1100120`) para desacoplar el pipeline de variaciones tipográficas en las fuentes originales.
- **DI-003**: Ingesta agnóstica de encoding con fallback ordenado (`utf-8` $\rightarrow$ `latin-1` $\rightarrow$ `cp1252`) y separadores (`comma`, `semicolon`, `tab`).


---

## 4. Registro de Adquisición, Ingesta y Modelado Multidimensional (Fase 2)

**Fecha**: 2026-08-18  
**Participantes**: Persona A (Adan Sánchez), Persona B (Yesid Bello), Persona C (Sofía Hidalgo)  

### Log de Actividades Ejecutadas:
1. **Adquisición Automática**: Implementado y ejecutado `scripts/download_missing_data.py`, integrando 25 datasets oficiales de IDECA, EAAB, UAESP, SDIS, MinTIC, DANE, SDP, MEBOG y Gobierno Abierto Bogotá.
2. **Nuevos Dominios y Validadores**:
   - `SERVICIOS_PUBLICOS` (D11): Cobertura acueducto/alcantarillado EAAB, calidad del agua IRCA, alumbrado público UAESP y conectividad TIC.
   - `EMPLEO_ECONOMIA` (D12): Matriz de conmutación residencia-trabajo, salarios promedio e informalidad laboral.
   - `PARTICIPACION_CIUDADANA` (D9): Solicitudes y PQR Bogotá Te Escucha y Presupuestos Participativos.
   - `MODELO_TERRITORIAL` (D10): Polígonos oficiales de las 20 localidades en GeoJSON WGS84.
   - Expansión de Inversión FDL y Gasto Social SDIS en `FINANZAS_INVERSION_PUBLICA` (D7).
   - Expansión de Capacidad Asistencial en `SALUD` (D2), Calidad Saber 11 en `EDUCACION` (D3) y Delitos de Alto Impacto en `SEGURIDAD` (D8).
3. **Modelado e IPT Multidimensional**: Implementado `calculate_multidimensional_ipt()` en `src/modeling/calculate_indicators.py` ponderando 7 dimensiones críticas.
4. **Notebooks de Ingesta & EDA**: Generados `09_ingestion_servicios_publicos.ipynb`, `10_ingestion_empleo_economia.ipynb`, `11_ingestion_participacion_pqr.ipynb`.
5. **Control de Calidad**: Suite de validación ejecutada al 100% sobre los 13 dominios y 60/60 pruebas unitarias aprobadas (`pytest -v`).
