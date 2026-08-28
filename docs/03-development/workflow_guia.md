SIPTA — Flujo de trabajo

Propósito
Este documento describe el flujo de trabajo recomendado para ejecutar el proyecto SIPTA, desde la recepción de datos hasta la entrega de resultados. Está diseñado para un equipo de DataJam que trabaja con Git Flow, notebooks y un pipeline de datos modular.

1. Etapas del flujo de trabajo

1.1 Preparación inicial
- Revisar el plan general y los documentos sectoriales.
- Confirmar la unidad territorial vigente (localidad o la unidad oficial alternativa).
- Configurar el repositorio y crear las ramas según Git Flow.
- Definir el inventario de datasets y la lista inicial de archivos en `data/raw`.

1.2 Ingesta de datos
- Usar `notebooks/01_ingestion.ipynb` para probar la lectura de los datos.
- Registrar cada dataset en `data/raw` con su nombre y versión.
- Guardar copias de seguridad de los archivos originales.
- Trasladar la lógica de carga a `src/ingestion/ingest_data.py`.

1.3 Validación de datos
- Ejecutar `notebooks/02_validation.ipynb` para revisar esquemas y calidad.
- Validar identificador territorial `localidad` o su equivalente.
- Documentar problemas de calidad y columnas faltantes.
- Implementar reglas de validación en `src/validation/validate_data.py`.

1.4 Limpieza y estandarización
- Normalizar nombres de columnas y formatos de valores.
- Convertir columnas numéricas y limpiar texto en `src/cleaning/clean_data.py`.
- Guardar datasets limpios en `data/processed`.
- Documentar transformaciones en `docs/diccionario_datos.md`.

1.5 Integración territorial
- Crear la tabla maestra de localidades en `src/integration/integrate_data.py`.
- Unir datos sectoriales por `localidad`.
- Agregar población y geometría mínima.
- Guardar la tabla maestra en `data/processed/master_localidades.csv`.

1.6 Feature engineering y cálculo de indicadores
- Agregar variables derivadas en `src/features/feature_engineering.py`.
- Calcular indicadores básicos en `src/modeling/calculate_indicators.py`.
- Construir el Índice de Prioridad Territorial (IPT) con las dimensiones clave.
- Guardar resultados parciales en `data/processed` y finales en `data/curated`.

1.7 Visualización y exportación
- Preparar rankings y tablas para el dashboard en `src/visualization/prepare_visualization.py`.
- Usar `notebooks/05_visualization.ipynb` para validar las salidas.
- Exportar tablas finales a `data/curated`.

1.8 Evaluación y documentación
- Revisar calidad y consistencia de resultados en `src/evaluation/evaluate_results.py`.
- Completar `docs/manual_tecnico.md`, `docs/diccionario_datos.md` y `docs/registro_cambios.md`.
- Actualizar los README sectoriales con el estado real de los datos.

2. Flujo de trabajo con Git

2.1 Ramas principales
- `main`: versión estable lista para entrega.
- `develop`: integración de trabajo aprobado.
- `feature/*`: desarrollo de tareas concretas.
- `release/*`: preparación de versiones.
- `hotfix/*`: correcciones urgentes.

2.2 Convenciones
- Commits con Conventional Commits: `feat(...)`, `fix(...)`, `docs(...)`, `chore(...)`.
- Cada feature debe tener PR revisado por otro integrante.
- No aprobar PR propio.

2.3 Ejemplo de ciclo
- Crear rama `feature/etl` para ingesta y limpieza.
- Hacer cambios y pruebas locales.
- Abrir PR hacia `develop` con descripción clara.
- Una vez aprobado, merge a `develop`.
- Al final de un sprint, crear `release/v1.0.0` y fusionar a `main`.

2.4 Roles, ramas y modo de trabajo
- Roles y responsabilidades (resumen):
  - Persona A — Scrum Master + Data Engineer (Git Manager):
    - Ramas principales a usar: `feature/*` para ETL (`feature/etl`, `feature/data-ingestion`), `bugfix/*`, `release/*`, `hotfix/*`.
    - Responsabilidades sobre ramas: crear y coordinar `release/*`, gestionar merges desde `develop` a `main`, resolver conflictos críticos, revisar PRs técnicos de integración de datos.
    - Flujo: trabaja sobre `develop` como base; crea `feature/<tarea>` desde `develop`; cuando la feature está lista abre PR hacia `develop` y asigna revisor (no autoaprobación). Tras aprobación, merge a `develop`.

  - Persona B — Data Scientist / Analista:
    - Ramas principales a usar: `feature/eda`, `feature/territorial-index`, `feature/modeling`.
    - Responsabilidades sobre ramas: desarrollo de notebooks y código reproducible para EDA, definición y pruebas de indicadores y del IPT; escribir tests para indicadores.
    - Flujo: crear `feature/<tarea>` desde `develop`; mantener notebooks en `notebooks/` y portar lógica a `src/` antes de merge; abrir PR a `develop` con evidencia (notebook + tests + salida de ejemplo).

  - Persona C — Tech Lead + BI Developer:
    - Ramas principales a usar: `feature/dashboard`, `feature/visualization`, `feature/recommendation-engine`.
    - Responsabilidades sobre ramas: diseño y entrega del dashboard mínimo, exportación de datos curados, preparación de artefactos para presentación y QA final.
    - Flujo: crear `feature/<tarea>` desde `develop`; validar que los artefactos (CSV/Parquet, visualizaciones) estén en `data/curated`; abrir PR a `develop` y coordinar pruebas de integración y visualización.

- Reglas operativas sobre ramas y PRs:
  - Todas las ramas feature se crean desde `develop` y se nombran `feature/<descripcion>` (usar guiones bajos o guiones según convención del equipo).
  - Cada PR debe incluir: descripción corta, checklist de pruebas realizadas, archivos de salida de ejemplo (si aplica), y tests automatizados si aplica.
  - No se aprueba un PR propio. Al menos una revisión de otro miembro es obligatoria.
  - Antes de merge a `develop`: ejecutar pruebas locales unitarias, validar que los notebooks reproducen los pasos clave y que `data/processed` se actualiza correctamente en entorno de prueba.
  - Releases: cuando `develop` contiene el conjunto de entregables del sprint, crear `release/vX.Y.Z` para estabilización, realizar QA y luego merge a `main` y `develop` (tag en `main`).
  - Hotfixes: crear `hotfix/<descripcion>` desde `main`, aplicar corrección, abrir PR hacia `main` y `develop` según el caso.

- Coordinación y revisiones:
  - Persona A actúa como Git Manager para resolver conflictos y coordinar merges complejos.
  - La asignación de revisores se hace en el PR (preferir el rol que no sea autor: por ejemplo, A revisa trabajo de B/C en ETL; B revisa cálculos/estadísticas; C revisa visualizaciones y documentación).
  - Mantener PRs pequeños y atómicos para facilitar la revisión (ideal < 500 líneas de cambio).

- Consejos prácticos:
  - Mantener la rama `develop` sincronizada con `main` regularmente.
  - Etiquetar commits relevantes con Conventional Commits para facilitar el changelog.
  - Documentar en la descripción del PR las decisiones metodológicas importantes y marcar con "⚠ Pendiente de validar con datos" cualquier resultado que dependa de datos no confirmados.

3. Uso de notebooks y código

- Los notebooks son prototipos y documentación de exploración.
- El código definitivo se escribe en `src/`.
- Los notebooks deben referenciar las funciones del código cuando sea posible.
- Mantener `notebooks/` como apoyo, no como única fuente productiva.

4. Entregables de cada sprint

Sprint 0
- Repositorio y estructura.
- `README.md` y `README_WORKFLOW.md`.
- Inventario inicial de datasets.

Sprint 1
- Inventario de datos completo.
- Validaciones iniciales.
- Tabla maestra de localidades en desarrollo.

Sprint 2
- Datasets limpios y procesados.
- Indicadores iniciales por localidad.
- Documentación de variables.

Sprint 3
- IPT preliminar.
- Ranking territorial.
- Dashboard mínimo con mapas y tablas.

5. Reglas prácticas

- Marca con "⚠ Pendiente de validar con datos" todas las asunciones.
- Si falta información para un indicador, documenta la limitación en `docs/`.
- Prioriza productos entregables sobre modelos complejos.
- Mantén cada módulo pequeño y fácil de revisar.

-- Fin del flujo de trabajo --
