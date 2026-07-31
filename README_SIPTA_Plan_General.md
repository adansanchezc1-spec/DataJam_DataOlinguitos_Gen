SIPTA — Plan Maestro corregido y clarificado
Versión: 1.0 corregida | Fecha: 2026-07-31
Resumen rápido
Documento corregido del Plan Maestro SIPTA (Sistema Inteligente de Priorización Territorial y Alertas Tempranas — DataJam Bogotá). Contiene las modificaciones requeridas por la revisión del profesor: objetivos depurados, sustitución de referencias a UPZ por localidad, validaciones pendientes claramente marcadas, preguntas rectora y estratégicas revisadas, inclusión de la dimensión "Inversión" en los índices y ajuste del motor de recomendaciones y KPIs.

1. Rol y objetivo del documento
Actuar como guía metodológica y técnica para el proyecto DataJam. Este documento define lo esencial que debe implementarse y qué queda pendiente de validar con los datos reales.

2. Objetivos (revisados — máximo 3)
- Objetivo 1: Integrar y normalizar fuentes de datos abiertas del Distrito para construir indicadores comparables a nivel de localidad. ⚠ Pendiente de validar con datos.
  Nota de factibilidad: validar existencia de identificador territorial consistente (localidad y/o otro vigente) y cobertura de variables demográficas.

- Objetivo 2: Construir un Índice de Prioridad Territorial (IPT) que combine necesidad, riesgo e inversión para priorizar acciones en localidades. ⚠ Pendiente de validar con datos.
  Nota de factibilidad: confirmar disponibilidad histórica y granularidad de datos de inversión pública por localidad.

- Objetivo 3: Entregar un dashboard y documentación reproducible que muestre el ranking de prioridades por localidad y explique los factores que llevan a la priorización. (La generación formal de recomendaciones de política se podrá incluir como output, pero no debe figurar como objetivo si no hay evidencia suficiente). ⚠ Pendiente de validar con datos.

3. Unidad territorial
Se reemplazan todas las referencias a "UPZ" por "localidad" como unidad territorial primaria en este documento. Nota: confirmar cuál es la unidad de segmentación territorial oficial vigente en la Alcaldía y adaptar el modelo si los datos usan otra unidad oficial. ⚠ Pendiente de validar con datos (unidad oficial y tablas de homologación).

4. Etiquetas de validación de datos
Todos los componentes que dependen de la disponibilidad y calidad de datos incluyen la etiqueta: "⚠ Pendiente de validar con datos".
Se aplica a: motor de priorización y alertas; construcción del índice de vulnerabilidad; identificación de necesidad territorial; detección de señales tempranas; existencia de series históricas suficientes; y posibilidad de medir capacidad (camas, cupos, m2) por localidad.

5. Pregunta rectora y preguntas estratégicas (redefinidas)
Pregunta rectora (redefinida): ¿En qué localidades la combinación de mayor necesidad y mayor riesgo recibe insuficiente inversión pública, y dónde debería priorizarse la acción? ⚠ Pendiente de validar con datos.
Preguntas estratégicas operativas:
- ¿Qué localidades muestran mayor brecha entre necesidad (necesidad medida por indicadores sectoriales) y la inversión pública ejecutada? ⚠ Pendiente de validar con datos.
- ¿Qué dimensiones (salud, educación, movilidad, ambiente, infraestructura, finanzas, seguridad) contribuyen más a la prioridad en cada localidad? (Explicación por componentes del IPT).
- ¿Cómo medir el impacto relativo de una intervención dada la evidencia de capacidad y cobertura (por ejemplo, camas agregadas o cupos escolares) en la localidad? ⚠ Pendiente de validar con datos.

6. Índices compuestos — dimensiones
Se añade explícitamente la dimensión "Inversión" como una dimensión propia junto a Salud, Educación, Movilidad, Infraestructura, Ambiente, Finanzas/Equidad, Desarrollo Social/Seguridad.
Normalización recomendada: Min-Max (0–1), con análisis de sensibilidad marcado como tarea de validación (ver KPIs). ⚠ Pendiente de validar con datos.

7. Motor de recomendaciones (simplificado)
- Alcance: máximo 3 recomendaciones por localidad priorizada en la versión DataJam. Cada recomendación debe cumplir:
  1) Evidencia: indicador(s) que la justifican.
  2) Efecto esperado: cuál es el efecto cuantificable esperado (p. ej., aumento de X camas por 10.000 hab → mejora estimada en indicador SAL-002).
  3) Responsable sugerido: entidad distrital o instanciación operativa.
- Las recomendaciones se generan por reglas explicitas o plantillas interpretables. No se producirán recomendaciones extensas sin trazabilidad directa y sin marcar: "⚠ Pendiente de validar con datos".

8. KPIs: definición o eliminación
Se revisan los KPIs señalados por el profesor y se definen métodos de medición concretos o se eliminan con justificación.
Tabla resumida (KPI | Método de medición | Estado):
- Nº de datasets integrados | Conteo automático de entradas en E01 Inventario de datos (metadatos + URL) | Medible.
- % variables documentadas | (n_variables_documentadas / n_variables_totales) * 100 sobre E02 Diccionario | Medible.
- % registros válidos | Pipeline valida y reporta % filas que cumplen reglas por dataset | Medible (automatizable).
- Tiempo de procesamiento del pipeline | Cronómetro de ejecución en CI (segundos/minutos) | Medible.
- Cobertura territorial lograda | % localidades con datos mínimos requeridos (según DIM_TERRITORIO) | Medible tras validar identificadores territoriales. ⚠ Pendiente de validar con datos.
- Nº de indicadores calculados | Conteo en E05 Indicadores | Medible.
- Nº de índices generados | Conteo en E06 Índices | Medible.
- Estabilidad del índice ante cambios de pesos | Método: prueba de sensibilidad Monte Carlo (variación aleatoria de pesos en rango razonable y medir varianza del IPT). Esta prueba es recomendada pero su inclusión depende de tiempo. Si no se incluye, mover a tarea posterior. ⚠ Pendiente de confirmar alcance con el equipo.
- Nº de recomendaciones trazables a datos | Conteo de recomendaciones cuya evidencia enlaza a al menos 1 indicador y 1 dataset | Medible.
- Nº de decisiones públicas soportadas | Definición operativa: contar decisiones públicas (actas, resoluciones o comunicados oficiales) que mencionen explícitamente el uso del sistema o que estén vinculadas a entregables. Método sujeto a confirmación con entidades; por ahora marcado como "por validar" y no será KPI obligatorio para DataJam. ⚠ Pendiente de validar con stakeholders.
- Claridad de interpretación para usuarios no técnicos | Método: prueba de usuario con N>=5 participantes no técnicos, encuesta Likert (1–5) sobre comprensión; reportar mediana y %>=4 | Medible como prueba de usabilidad mínima.

9. Medición por capacidad (ajustes de indicadores según punto H)
Se ajustan las fichas técnicas de ejemplo:
- SAL-001: Hospitales por 10.000 hab → sustituir por "Camas por 10.000 hab" (SAL-002) como indicador de capacidad primaria. Ficha: camas / poblacion * 10000. Nivel territorial: localidad. Fuente esperada: datos del portal de salud del Distrito. ⚠ Pendiente de validar con datos.
- EDU-001: Cohorte por capacidad → "Cupos escolares por 1.000 niños en edad escolar" (cupos / poblacion_en_edad * 1000). Nivel: localidad. ⚠ Pendiente de validar con datos.
- INF-004: Espacio público por habitante → mantener pero medir en m2 por habitante (m2 / poblacion). Nivel: localidad. ⚠ Pendiente de validar con datos.

10. Validación con requisitos oficiales del DataJam
Tarea obligatoria: verificar las bases del reto, rúbrica y entregables oficiales. Si hay diferencias, ajustar los entregables (E01–E11) a lo requerido por DataJam. Esta tarea debe hacerse en Sprint 0. ⚠ Pendiente de validar con los materiales oficiales del DataJam.

11. Glosario mínimo (términos ambiguos)
- Geometría: se refiere a la representación vectorial del límite territorial (polígono), por ejemplo GeoJSON / shapefile del polígono de la localidad o del barrio.
- Localidad: unidad administrativa vigente en Bogotá (reemplaza UPZ en este documento). Confirmar unidad oficial.
- Índice compuesto: indicador construido a partir de varias dimensiones normalizadas y ponderadas.
- Trazabilidad: capacidad de rastrear cada indicador hasta su dataset y fecha de extracción.

12. Entregables ajustados (resumen)
Mantener E01–E11 pero con las siguientes notas:
- OE03 Modelo territorial → eliminar mención a UPZ; usar localidad. Agregar tabla de homologación territorial si la unidad oficial difiere. ⚠ Pendiente de validar con datos.
- E06 Índices → incluir dimensión Inversión explícita.
- E07 Alertas → marcar como "⚠ Pendiente de validar con datos" (series históricas).
- E08 Dashboard → Priorizar Mapa + Ranking + Radar por localidad como mínimo.

13. Motor de priorización y ETL
- El motor de priorización debe documentarse como "reglas + índice compuesto" y siempre incluir la etiqueta de validación de datos si parte de sus insumos no se confirma.
- ETL: mantener zonas raw/processed/curated y registro de metadatos por ejecución.

14. Reglas operativas y alcance de sprint
- No prometer modelos predictivos si no hay series históricas suficientes. Diseñar alertas basadas en reglas como alternativa.

15. Checklist mínimo de puesta en marcha (extracto)
- [ ] Confirmar unidad territorial oficial y crear tabla de homologación. ⚠ Pendiente de validar con datos.
- [ ] Inventario E01 completado con metadatos. (Sprint 1)
- [ ] Diccionario E02 con variables y unidades. (Sprint 2)
- [ ] Pipeline ETL reproducible con logs. (Sprint 3)
- [ ] Indicadores E05 con fichas técnicas (incluida inversión). (Sprint 4)
- [ ] Dashboard mínimo: mapa, ranking, radar. (Sprint 6)

16. Notas finales
Todo lo propuesto está supeditado a la verificación contra los datasets reales. Donde exista incertidumbre se ha marcado con "⚠ Pendiente de validar con datos". No se agregaron nuevos alcances más allá de los comentarios del profesor. El lenguaje se mantiene directo y las acciones son concretas.

Anexos: referencias breves
- Repositorio: convención Git Flow (main/develop/feature/*).
- Cronograma: sprints 0–7 (ver Plan maestro original).
- Responsables y RACI: mantener matriz definida en el plan original.

Documentos sectoriales y estructura de carpetas
- Salud: SALUD/README.md
- Educación: EDUCACION/README.md
- Movilidad: MOVILIDAD/README.md
- Ambiente: AMBIENTE/README.md
- Infraestructura y Espacio Público: INFRAESTRUCTURA_ESPACIO_PUBLICO/README.md
- Finanzas e Inversión Pública: FINANZAS_INVERSION_PUBLICA/README.md
- Seguridad: SEGURIDAD/README.md
- Participación Ciudadana: PARTICIPACION_CIUDADANA/README.md
- Carpeta de datos: data/raw, data/processed, data/curated, data/external
- Carpeta de código: src/ingestion, src/validation, src/cleaning, src/integration, src/features, src/modeling, src/evaluation, src/visualization
- Notebooks base: notebooks/01_ingestion.ipynb, notebooks/02_validation.ipynb, notebooks/03_integration.ipynb, notebooks/04_modeling.ipynb, notebooks/05_visualization.ipynb
- Plantillas de código base: src/ingestion/ingest_data.py, src/validation/validate_data.py, src/cleaning/clean_data.py, src/integration/integrate_data.py, src/features/feature_engineering.py, src/modeling/calculate_indicators.py, src/evaluation/evaluate_results.py, src/visualization/prepare_visualization.py

-- Fin del README del plan general --
