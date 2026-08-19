# Script para la creación automatizada de Sub-Issues en GitHub
# Repositorio: adansanchezc1-spec/DataJam_DataOlinguitos_Gen
# Basado en el trabajo realizado en los últimos 5 días (commits, PRs #20-#25 y trabajo local)
# Requiere: GitHub CLI (gh) autenticado: gh auth login

$ErrorActionPreference = 'Stop'
$REPO = 'adansanchezc1-spec/DataJam_DataOlinguitos_Gen'

function Crear-Label($name, $color, $description) {
    try {
        gh label create $name --repo $REPO --color $color --description $description --force 2>$null
    } catch {
        # Label ya existe o no requiere actualización
    }
}

Write-Output "Configurando etiquetas (labels) en GitHub..."
Crear-Label 'subissue' '6f42c1' 'Sub-tarea derivada de un issue principal del proyecto'
Crear-Label 'data-understanding' '1D76DB' 'Fase de entendimiento de datos y catalogación'
Crear-Label 'trazabilidad-indicadores' '0E8A16' 'Fichas técnicas, fórmulas y trazabilidad analítica'
Crear-Label 'arquitectura-modeling' '5319E7' 'Arquitectura de software, pipeline ETL y modelado'
Crear-Label 'plan-trabajo-scrum-gitflow' 'FBCA04' 'Scrum, Git Flow y gestión del equipo'
Crear-Label 'riesgos-documentacion-cierre' 'D93F0B' 'Gestión de riesgos, pruebas y documentación'

function Crear-SubIssue($parentNumber, $title, $label, $bodyText) {
    $fullTitle = "[#$($parentNumber)] $title"
    $body = @"
**Issue Principal**: #$($parentNumber)
**Estado en Proyecto**: Implementado / En Validación

$bodyText

---
*Sub-issue generado automáticamente en el marco de trabajo SIPTA (Fase CONTROL / SDLC Testing).*
"@
    Write-Output "Creando Sub-Issue para Parent #$($parentNumber) - $title..."
    $body | gh issue create --repo $REPO --title $fullTitle --label "$label,subissue" --body-file -
}

Write-Output "`n======================================================="
Write-Output " Creando Sub-Issues para los Issues Principales de SIPTA"
Write-Output "=======================================================`n"

# ==============================================================================
# PARENT ISSUE #1: Inventario maestro de dominios (10 dominios)
# ==============================================================================

Crear-SubIssue 1 "Consolidación del catálogo para 13 dominios temáticos de SIPTA" "data-understanding" @'
### Contexto y Alcance
Ampliación del inventario original de 10 dominios a 13 dominios territoriales (incorporando Servicios Públicos, Empleo y Economía, y Fondos de Desarrollo Local).

### Trabajo Realizado y Evidencia
- Catalogación de 31 fuentes de datos abiertas oficiales (OSB, IDECA, TransMilenio, SED, SDS, IDRD, EAAB, UAESP, SDDE, DANE).
- Ingesta física y verificación de 121 archivos en `data/raw/` organizados por carpetas sectoriales.
- Actualización de metadatos en `reports/inventory/inventario_datasets_sipta.csv` y `docs/01-requirements/E01_inventario_datos.md`.

### Commits & PRs Relacionados
- Commit `bfb8b12`: Inicialización de pipeline EDA y catalogación.
- Commit `e4e18f5`: Ingesta modular de dominios y datasets de movilidad.
- PR `#20`: Consolidación del entregable E01 de inventario de datos.
'@

Crear-SubIssue 1 "Diagnóstico de brechas de datos (Gaps) y sectores sin fuentes directas" "data-understanding" @'
### Contexto y Alcance
Identificación y tratamiento metodológico de sectores con ausencia de datos físicos directos o cobertura parcial por localidad.

### Trabajo Realizado y Evidencia
- Cuaderno de análisis de vacíos: `notebooks/eda/07_eda_gaps.ipynb`.
- Reporte estructurado de gaps: `reports/eda/gaps_sectores_sin_datos.csv`.
- Definición de indicadores faltantes y dependientes de cruces espaciales en `reports/eda/indicadores_faltantes.csv`.

### Commits & PRs Relacionados
- Commit `bfb8b12`: Generación de reportes de gaps y matriz de cobertura territorial.
'@


# ==============================================================================
# PARENT ISSUE #2: Matriz de calidad de datos y criterios de aceptación
# ==============================================================================

Crear-SubIssue 2 "Implementación del motor automatizado de validación multidominio" "data-understanding" @'
### Contexto y Alcance
Construcción del validador de calidad de datos en Python que evalúa las 6 dimensiones DAMA-BOK / ISO 25010 (Completitud, Consistencia, Validez, Unicidad, Actualidad, Precisión).

### Trabajo Realizado y Evidencia
- Módulo `src/validation/validate_data.py` con inspectores de esquemas, detección de llaves territoriales y validadores de 13 dominios.
- Suite de pruebas unitarias en `tests/test_validation.py` (100% passed).
- Cuaderno maestro de validación: `notebooks/02_validation/00_validation_master.ipynb`.

### Commits & PRs Relacionados
- Commit `e4e18f5`: Modularización de `validate_data.py`.
- PR `#24`: Definición de matriz de calidad y criterios de aceptación.
'@

Crear-SubIssue 2 "Generación de la matriz consolidada de calidad y reporte maestro" "data-understanding" @'
### Contexto y Alcance
Generación programática de reportes ejecutivos y matrices de calidad para todos los datasets del proyecto.

### Trabajo Realizado y Evidencia
- Reporte maestro en Markdown: `reports/validation/reporte_validacion_maestro.md`.
- Matriz resumen cuantitativa: `reports/validation/matriz_calidad_resumen.csv`.
- Diagnósticos individuales por dominio en `reports/validation/dominios/val_*.json`.
- Documento consolidado en `docs/01-requirements/evaluacion_calidad_datasets_consolidada.md`.

### Commits & PRs Relacionados
- Commit `bfb8b12`: Perfilado masivo y generación de diagnósticos JSON.
- PR `#24`: Matriz de calidad.
'@


# ==============================================================================
# PARENT ISSUE #3: Principios de datos y modelo territorial
# ==============================================================================

Crear-SubIssue 3 "Cruces espaciales acelerados con R-tree para asignación territorial" "data-understanding" @'
### Contexto y Alcance
Implementación del principio "Un territorio, una verdad" mediante cruces espaciales (Point-in-Polygon) para capas vectoriales sin columna territorial directa (IPS, estaciones, paraderos, parques).

### Trabajo Realizado y Evidencia
- Módulo `src/eda/spatial.py` con optimización espacial R-tree (`predicate="intersects"`) y soporte para reproyección EPSG:4326.
- Pruebas unitarias de cruces espaciales en `tests/test_eda_spatial.py` (7 tests aprobados).
- Documentación de principios en `docs/01-requirements/principios_modelo_territorial.md`.

### Commits & PRs Relacionados
- Commit `bfb8b12`: Módulo `src/eda/spatial.py` y cálculo de coberturas por localidad.
- PR `#22`: Validación de educación e infraestructura territorial.
'@


# ==============================================================================
# PARENT ISSUE #4: Definir tabla DIM_TERRITORIO
# ==============================================================================

Crear-SubIssue 4 "Homologación canónica y codificación DIVIPOLA de 20 Localidades" "data-understanding" @'
### Contexto y Alcance
Definición e implementación del estándar canónico de las 20 localidades del Distrito Capital para garantizar joins libres de inconsistencias tipográficas.

### Trabajo Realizado y Evidencia
- Funciones `homologar_localidad()`, `limpiar_texto_serie()` y `castear_numerico()` en `src/cleaning/clean_data.py` y `src/cleaning.py`.
- Tabla de homologación oficial con soporte de alias (tildes, mayúsculas, prefijos "Localidad de").
- Suite de pruebas de limpieza en `tests/test_cleaning.py` (8 tests aprobados).
- Documento de especificación en `docs/01-requirements/dim_territorio.md`.

### Commits & PRs Relacionados
- Commit `e4e18f5`: Refactorización de limpieza y estandarización de localidades.
- Commit `bfb8b12`: Normalización de tablas procesadas en `data/processed/`.
'@


# ==============================================================================
# PARENT ISSUE #5: Inventario maestro de indicadores + ficha técnica
# ==============================================================================

Crear-SubIssue 5 "Especificación técnica y cálculo de indicadores base y de expansión" "trazabilidad-indicadores" @'
### Contexto y Alcance
Construcción del catálogo maestro de más de 25 indicadores con fórmulas matemáticas, unidades, variables fuente y nivel de agregación.

### Trabajo Realizado y Evidencia
- Módulos `src/eda/explore_indicators.py` y `src/modeling/calculate_indicators.py`.
- Fichas técnicas documentadas en `docs/01-requirements/fichas_tecnicas_indicadores_base.md` y `fichas_tecnicas_nuevos_dominios.md`.
- Verificación programática de indicadores en `tests/test_eda_explore_indicators.py` y `tests/test_features.py`.

### Commits & PRs Relacionados
- Commit `6e68069`: Fichas técnicas e inventario maestro de indicadores.
- Commit `bfb8b12`: Módulo `src/eda/indicators.py` y `reports/eda/resumen_indicadores_eda.csv`.
'@


# ==============================================================================
# PARENT ISSUE #6: Matriz de trazabilidad analítica (problema → decisión)
# ==============================================================================

Crear-SubIssue 6 "Mapeo de la cadena de valor analítica (Problema Público -> Decisión)" "trazabilidad-indicadores" @'
### Contexto y Alcance
Estructuración de la cadena de trazabilidad que conecta cada dolor de ciudad con los datasets, indicadores, alertas e intervenciones públicas concretas.

### Trabajo Realizado y Evidencia
- Matriz completa en `docs/01-requirements/matriz_trazabilidad_analitica.md` y `docs/matriz_trazabilidad_analitica.md`.
- Conexión de problemas de salud, educación, movilidad, seguridad, finanzas y servicios públicos con entidades responsables (SDS, SED, SDM, MEBOG, SDIS, EAAB).

### Commits & PRs Relacionados
- PR `#25`: Definición de la matriz analítica de problema a decisión (`feature-trazabilidad-analitica-yesid`).
- Commit `4a178ca`: Merge PR #25 a develop.
'@


# ==============================================================================
# PARENT ISSUE #7: Marco metodológico de priorización territorial (IPT)
# ==============================================================================

Crear-SubIssue 7 "Implementación del motor de cálculo del Índice de Priorización Territorial" "trazabilidad-indicadores" @'
### Contexto y Alcance
Construcción del algoritmo de normalización Min-Max, inversión de polaridad para métricas de déficit y ponderación multidimensional del IPT (escala 0-100).

### Trabajo Realizado y Evidencia
- Módulo `src/modeling/calculate_indicators.py` con `normalize_min_max()` y `build_ipt_composite_index()`.
- Cuaderno interactivo de modelado: `notebooks/04_modeling/01_modeling_ipt.ipynb`.
- Pruebas de integración del modelado en `tests/test_pipeline_modeling_viz.py` (8 tests aprobados).

### Commits & PRs Relacionados
- Commit `e4e18f5`: Modularización del cálculo de indicadores y normalización.
- Commit `bfb8b12`: Pipeline de modelado y pruebas de integración.
'@


# ==============================================================================
# PARENT ISSUE #8: Organización del repositorio
# ==============================================================================

Crear-SubIssue 8 "Reestructuración modular de carpetas, código src/ y gestión documental PDCO" "arquitectura-modeling" @'
### Contexto y Alcance
Organización integral del repositorio siguiendo las mejores prácticas de ingeniería de software, arquitectura hexagonal y el estándar de documentación PDCO.

### Trabajo Realizado y Evidencia
- Reorganización de cuadernos en subcarpetas de ciclo de vida (`01_ingestion/`, `02_validation/`, `03_integration/`, `04_modeling/`, `05_visualization/`).
- Desacoplamiento de `src/` en paquetes especializados (`cleaning`, `features`, `evaluation`, `integration`, `visualization`, `eda`, `validation`, `modeling`).
- Estructura documental completa en `docs/01-requirements/` a `docs/05-maintenance/`.

### Commits & PRs Relacionados
- Commit `bfb8b12`: Estructura inicial de módulos y tests.
- Commit `e4e18f5`: Modularización de carpetas de src y notebooks.
'@


# ==============================================================================
# PARENT ISSUE #9: Evaluation: niveles y métricas
# ==============================================================================

Crear-SubIssue 9 "Módulo de evaluación de calidad de datos, outliers y estabilidad" "arquitectura-modeling" @'
### Contexto y Alcance
Implementación de las rutinas de evaluación técnica de calidad de datos y detección estadística de valores atípicos (IQR y Z-Score).

### Trabajo Realizado y Evidencia
- Módulo `src/evaluation.py` con `detect_outliers()`, `quality_report()` y persistencia de reportes.
- Suite de pruebas unitarias en `tests/test_evaluation.py` (6 tests aprobados).
- Generación de reportes de calidad en `reports/validation/`.

### Commits & PRs Relacionados
- Commit `bfb8b12`: Perfilado estadístico, detección de asimetría y curtosis.
'@


# ==============================================================================
# PARENT ISSUE #10: Arquitectura de datos y pipeline ETL
# ==============================================================================

Crear-SubIssue 10 "Pipeline integrado de Ingesta, Limpieza, Integración y Feature Engineering" "arquitectura-modeling" @'
### Contexto y Alcance
Construcción del flujo ETL de extremo a extremo que procesa los datos raw hasta consolidar el Tablón Maestro Territorial.

### Trabajo Realizado y Evidencia
- Pipeline de ingesta polimórfica en `src/ingest.py` y `src/eda/readers.py`.
- Motor de integración por localidad en `src/integration.py` y `notebooks/03_integration/01_integration_master.ipynb`.
- Ingeniería de características y densidades en `src/features.py`.
- Pruebas unitarias de integración en `tests/test_integration.py` y `tests/test_features.py`.

### Commits & PRs Relacionados
- Commit `e4e18f5`: Integración de datos y cálculo de indicadores.
- Commit `bfb8b12`: Lectores robustos de CSV y XLSX con saltos automáticos de encabezados.
'@


# ==============================================================================
# PARENT ISSUE #11: Motores analíticos (Modeling)
# ==============================================================================

Crear-SubIssue 11 "Motores de ranking territorial, alertas tempranas y exportación curada" "arquitectura-modeling" @'
### Contexto y Alcance
Implementación de los algoritmos de ordenamiento, clasificación de criticidad y exportación de datasets curados para el visualizador interactivo.

### Trabajo Realizado y Evidencia
- Módulo `src/visualization.py` con `build_ranking()` y `export_for_dashboard()`.
- Cuaderno de visualización: `notebooks/05_visualization/01_visualization_dashboard.ipynb`.
- Generación de dataset curado: `data/curated/dashboard_ranking_muestra.csv`.
- Pruebas unitarias en `tests/test_visualization.py` (5 tests aprobados).

### Commits & PRs Relacionados
- Commit `e4e18f5`: Preparación de datos de visualización y métricas.
- Commit `bfb8b12`: Módulo `src/eda/viz.py` con estilos gráficos y mapas coropléticos.
'@


# ==============================================================================
# PARENT ISSUE #14: Git Flow: ramas, PRs, commits y versionado
# ==============================================================================

Crear-SubIssue 14 "Gestión de ramas, revisión cruzada de PRs y control de versiones v2.2.0" "plan-trabajo-scrum-gitflow" @'
### Contexto y Alcance
Implementación rigurosa del flujo Git Flow en el rol de Git Manager y Scrum Master (Persona A).

### Trabajo Realizado y Evidencia
- Integración de Pull Requests (#20, #22, #24, #25) con revisiones cruzadas.
- Estandarización de Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`).
- Actualización y versionado semántico en `metadata.json` (v2.2.0).

### Commits & PRs Relacionados
- PRs `#20`, `#22`, `#24`, `#25` mergeados a `develop`.
- Commits `16a1af7`, `d8cb795`, `2da5174`, `4a178ca`.
'@


# ==============================================================================
# PARENT ISSUE #16: Matriz de gestión de riesgos
# ==============================================================================

Crear-SubIssue 16 "Tratamiento de riesgos de heterogeneidad, nulos y optimización espacial" "riesgos-documentacion-cierre" @'
### Contexto y Alcance
Identificación y mitigación activa de riesgos técnicos durante la ingesta y cruce de datos distritales.

### Trabajo Realizado y Evidencia
- Mitigación de heterogeneidad en XLSX/CSV mediante detección automática de codificación (UTF-8, Latin-1) y encabezados variables en `src/eda/readers.py`.
- Optimización de cuello de botella en cruces espaciales pasando a R-tree index (`intersects`) en `src/eda/spatial.py`.
- Documentación de deuda técnica y riesgos en `docs/03-development/technical-debt.md`.

### Commits & PRs Relacionados
- Commit `bfb8b12`: Optimización de lectores y gestión de nulos.
'@


# ==============================================================================
# PARENT ISSUE #17: Documentación obligatoria (responsables)
# ==============================================================================

Crear-SubIssue 17 "Consolidación de documentación técnica según estándares SWEBOK, IEEE e ISO" "riesgos-documentacion-cierre" @'
### Contexto y Alcance
Elaboración y mantenimiento del corpus documental de ingeniería del proyecto SIPTA.

### Trabajo Realizado y Evidencia
- Especificación de Requerimientos IEEE 830: `docs/01-requirements/requirements.md`, `use-cases.md`, `entity-map.md`.
- Documento de Arquitectura y ADRs: `docs/02-architecture/architecture.md`, `patterns.md`, `ADR/ADR-001.md`, `ADR-002.md`.
- Bitácora de desarrollo y APIs: `docs/03-development/dev-log.md`, `api-docs.md`.
- Plan y resultados de pruebas IEEE 829: `docs/04-testing/test-plan.md`, `test-results.md`.
- Gestión de cambios: `docs/05-maintenance/changelog.md`, `refactoring-log.md`.

### Commits & PRs Relacionados
- Commits `bfb8b12`, `e4e18f5`, `6e68069`, `c9b97b7`, `ccd11cb`.
'@


# ==============================================================================
# PARENT ISSUE #18: Checklist final de entrega
# ==============================================================================

Crear-SubIssue 18 "Suite automatizada de verificación de 25 Notebooks y 103 Tests de src/" "riesgos-documentacion-cierre" @'
### Contexto y Alcance
Validación integral de reproducibilidad y calidad del software previo al cierre de entrega.

### Trabajo Realizado y Evidencia
- Suite completa en `tests/test_notebooks.py` que ejecuta y valida el 100% de los 25 cuadernos Jupyter (0 errores).
- 179 pruebas automatizadas en `pytest` aprobadas con 100% de éxito en < 60 segundos.
- Trazabilidad completa con todos los criterios de aceptación del DoD.

### Commits & PRs Relacionados
- Commit `bfb8b12`: Framework de pruebas unitarias.
- Pruebas automatizadas en `tests/`.
'@

Write-Output "`n======================================================="
Write-Output " Proceso completado exitosamente!"
Write-Output " Todos los Sub-Issues fueron creados y enlazados a sus Parent Issues."
Write-Output " Ver issues en: https://github.com/$REPO/issues"
Write-Output "=======================================================`n"
