# PowerShell translation of crear_issues_github.sh
# Requires: GitHub CLI (gh) authenticated: gh auth login
$ErrorActionPreference = 'Stop'
$REPO = 'adansanchezc1-spec/DataJam_DataOlinguitos_Gen'

function Crear-Label($name, $color) {
    gh label create $name --repo $REPO --color $color --force 2>$null
}

Crear-Label 'data-understanding' '1D76DB'
Crear-Label 'trazabilidad-indicadores' '0E8A16'
Crear-Label 'arquitectura-modeling' '5319E7'
Crear-Label 'plan-trabajo-scrum-gitflow' 'FBCA04'
Crear-Label 'riesgos-documentacion-cierre' 'D93F0B'

function Crear-Issue($title, $label, $asanaUrl, $bodyText) {
    $body = @'
'@
    $body = $bodyText + "`n`n---`n🔗 Tarea original en Asana: $asanaUrl"
    gh issue create --repo $REPO --title $title --label $label --body $body
}

# ============ 2. Data Understanding ============

Crear-Issue "Inventario maestro de dominios (10 dominios)" "data-understanding" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002793849860" @'
Dominio | Datos necesarios | Uso en SIPTA | Prioridad
Demografía | Población, edad, género, densidad, área | Normalización y demanda potencial | Alta
Salud | Hospitales, CAPS, camas, cobertura, consultas | Índice de cobertura sanitaria | Alta
Educación | Colegios, cupos, matrícula, docentes, deserción | Brecha educativa | Alta
Movilidad | Tiempos, rutas, estaciones, paraderos, ciclorrutas | Accesibilidad territorial | Alta
Infraestructura | Equipamientos, vías, espacio público, estado físico | Déficit y mantenimiento | Alta
Servicios públicos | Acueducto, alcantarillado, energía, gas, residuos, internet | Cobertura básica | Alta
Ambiente | Aire, ruido, arbolado, zonas verdes, riesgo | Riesgo ambiental | Media
Finanzas | Presupuesto, ejecución, contratos, inversión sectorial | Equidad inversión/necesidad | Alta
Participación | PQR, reportes, presupuestos participativos, encuestas | Evidencia ciudadana y alertas | Media
Seguridad | Delitos, emergencias, violencia, percepción | Vulnerabilidad territorial | Media
'@

Crear-Issue "Matriz de calidad de datos y criterios de aceptación" "data-understanding" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217003044482226" @'
MATRIZ DE CALIDAD:
Dimensión | Pregunta | Métrica
Completitud | ¿Hay valores faltantes? | % nulos
Consistencia | ¿Hay contradicciones? | Registros inconsistentes
Validez | ¿Cumple reglas de tipo/rango? | % válidos
Unicidad | ¿Hay duplicados? | % duplicados
Actualidad | ¿Está actualizado? | Fecha de actualización
Precisión | ¿Los valores son confiables? | Validación cruzada

CRITERIOS PARA ACEPTAR UN DATASET:
- Cobertura territorial identificable.
- Variables relevantes para el objetivo.
- Calidad aceptable.
- Licencia de reutilización.
- Posibilidad de integración con el modelo territorial maestro.
'@

Crear-Issue "Principios de datos y modelo territorial" "data-understanding" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002958176800" @'
PRINCIPIOS:
- Un territorio, una verdad: toda fuente debe asociarse a localidad, UPZ, barrio o coordenadas.
- Datos normalizados: ajustar por población, área, demanda o capacidad cuando corresponda.
- Trazabilidad: cada indicador debe rastrearse hasta su fuente.
- Reproducibilidad: cualquier integrante debe poder reconstruir el modelo de datos.

FLUJO: Demografía, Salud, Educación, Movilidad, Ambiente, Infraestructura, Finanzas Públicas, Participación Ciudadana, Seguridad → Modelo Territorial Maestro → Indicadores → Índices → Priorización y alertas.
'@

Crear-Issue "Definir tabla DIM_TERRITORIO" "data-understanding" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002958175216" @'
Campo | Tipo | Obligatorio | Descripción
id_localidad | Entero | Sí | Identificador único de localidad
nombre_localidad | Texto | Sí | Nombre oficial
codigo_dane | Texto | Sí | Código territorial si está disponible
upz | Texto | Deseable | Unidad de Planeamiento Zonal
barrio | Texto | Opcional | Nombre de barrio
latitud | Decimal | Deseable | Coordenada para análisis espacial
longitud | Decimal | Deseable | Coordenada para análisis espacial
area_km2 | Decimal | Sí | Superficie del territorio
poblacion | Entero | Sí | Habitantes
fecha_actualizacion | Fecha | Sí | Fecha de corte o actualización
'@

# ============ 3. Trazabilidad e Inventario de Indicadores ============

Crear-Issue "Inventario maestro de indicadores + ficha técnica" "trazabilidad-indicadores" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002975232065" @'
CLASIFICACIÓN: DEM, SAL, EDU, MOV, INF, FIN, SOC, AMB, PAR.

FICHA TÉCNICA MÍNIMA: Código, Nombre, Objetivo, Pregunta de negocio, Variables de entrada, Fórmula, Unidad, Nivel geográfico, Frecuencia, Interpretación, Visualización recomendada, Decisión pública que apoya.

INDICADORES BASE:
DEM-001 Densidad poblacional = Población / área_km2
SAL-001 Hospitales por 10.000 hab. = Hospitales / población * 10000
SAL-002 Camas por 10.000 hab. = Camas / población * 10000
EDU-001 Colegios por población objetivo = Colegios / población escolar
EDU-003 Cobertura educativa = Matrícula / población objetivo
MOV-001 Tiempo promedio de viaje = Promedio de tiempo
INF-004 Espacio público por habitante = m2 espacio público / población
FIN-001 Inversión per cápita = Presupuesto ejecutado / población
FIN-002 Ejecución presupuestal = Ejecutado / aprobado
SOC-001 Vulnerabilidad territorial = Índice compuesto

CHECKLIST DE ACEPTACIÓN: definición clara, fórmula documentada, variables disponibles, fuente identificada, resultado reproducible, interpretación consistente, vinculado a una decisión pública, validado por al menos dos integrantes.
'@

Crear-Issue "Matriz de trazabilidad analítica (problema → decisión)" "trazabilidad-indicadores" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217003073011855" @'
Lógica: Problema público → Pregunta estratégica → Objetivo analítico → Datasets → Variables → Indicadores → Índices → Visualización → Recomendación → Decisión pública.

Ejemplos:
- Acceso desigual a salud → ¿Qué localidades tienen menor acceso relativo? → Hospitales por 10.000 hab. → Cobertura en salud → Priorizar infraestructura sanitaria.
- Déficit educativo → ¿Dónde hay mayores brechas educativas? → Cobertura educativa → Índice educativo → Ampliar cupos o colegios.
- Baja cobertura de parques → ¿Qué zonas tienen menor espacio público? → m2 por habitante → Espacio público → Priorizar parques y mantenimiento.
- Baja accesibilidad → ¿Qué territorios tienen mayores tiempos? → Tiempo promedio → Accesibilidad → Mejorar conectividad.
- Inversión insuficiente → ¿La inversión coincide con la necesidad? → Inversión per cápita → Equidad territorial → Redistribuir o focalizar recursos.
- Infraestructura deteriorada → ¿Dónde se requiere mantenimiento preventivo? → % deterioro → Riesgo territorial → Plan preventivo de mantenimiento.

REGLAS DE USO:
- Ningún gráfico se construye sin pregunta estratégica.
- Ningún indicador se acepta sin fórmula, fuente e interpretación.
- Ninguna recomendación se presenta sin evidencia y entidad responsable.
- Toda decisión pública debe conectarse con al menos un indicador de seguimiento.
'@

Crear-Issue "Marco metodológico de priorización territorial (IPT)" "trazabilidad-indicadores" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002775401442" @'
PRINCIPIOS: Objetividad, Transparencia, Comparabilidad, Escalabilidad, Reproducibilidad, Interpretabilidad, Robustez, Accionabilidad.

DIMENSIONES: D1 Salud, D2 Educación, D3 Movilidad, D4 Infraestructura, D5 Ambiente, D6 Finanzas, D7 Desarrollo social — cada una con peso inicial ~14.3%.

NORMALIZACIÓN: Min-Max (rango 0-1), complementable con percentiles si hay valores extremos. Indicadores positivos se mantienen; negativos (tiempo de viaje, deterioro) se invierten.

ÍNDICE DE PRIORIDAD TERRITORIAL (IPT), escala 0-100:
0-20 muy baja, 21-40 baja, 41-60 media, 61-80 alta, 81-100 crítica.

MOTOR DE EXPLICACIÓN: para cada localidad priorizada, mostrar los factores que más contribuyen (ej. baja cobertura educativa, baja inversión per cápita, alta vulnerabilidad, infraestructura deteriorada).

MOTOR DE RECOMENDACIONES: reglas explícitas, ej. baja cobertura sanitaria + alta población + baja inversión relativa → fortalecer infraestructura de salud y revisar asignación presupuestal.
'@

# ============ 4. Arquitectura de Datos, ETL y Modeling ============

Crear-Issue "Organización del repositorio" "arquitectura-modeling" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217003044483811" @'
project/
├── data/ (raw, processed, curated, external)
├── notebooks/
├── src/ (ingestion, validation, cleaning, integration, features, modeling, evaluation, visualization)
├── models/
├── reports/
├── docs/
├── tests/
├── config/
├── scripts/
├── .github/
├── README.md
├── requirements.txt
└── LICENSE

FUNCIÓN DE CARPETAS:
- data: almacenamiento por zonas.
- notebooks: exploración y prototipos, no lógica productiva.
- src: código modular reutilizable.
- models: modelos serializados y metadatos.
- reports: informes y resultados exportados.
- docs: documentación metodológica y técnica.
- tests: pruebas unitarias y de integración.
- config: parámetros, rutas y pesos.
- scripts: utilidades ejecutables.
- .github: plantillas, workflows y configuración colaborativa.
'@

Crear-Issue "Evaluation: niveles y métricas" "arquitectura-modeling" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217017311995470" @'
FLUJO: Calidad de datos → Calidad de indicadores → Calidad de modelos → Calidad de recomendaciones → Valor público.

NIVELES:
1. Datos: completitud, consistencia, validez, unicidad, actualidad, precisión.
2. Indicadores: fórmula, unidad, sentido, comparabilidad, trazabilidad.
3. Modelos: métricas técnicas, estabilidad, interpretabilidad, reproducibilidad.
4. Recomendaciones: pertinencia, factibilidad, impacto, evidencia, escalabilidad.
5. Valor público: capacidad de mejorar decisiones, reducir incertidumbre, transparentar la priorización.

MÉTRICAS: Regresión (RMSE, MAE, R2); Clasificación (precisión, recall, F1, ROC-AUC); Clustering (Silhouette, Davies-Bouldin); Índices (sensibilidad, coherencia territorial, estabilidad ante cambios de pesos).

CRITERIOS DE ACEPTACIÓN: pipeline reproducible, indicadores validados, IPT consistente, recomendaciones justificadas, dashboard operativo, explicación clara para no técnicos.
'@

Crear-Issue "Arquitectura de datos y pipeline ETL" "arquitectura-modeling" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217003072945648" @'
ZONAS DE DATOS: data/raw (originales), data/processed (limpios y normalizados), data/curated (listos para análisis/indicadores/dashboard), data/external (auxiliares como geometría o tablas de homologación).

PIPELINE ETL:
1. Extract: descargar datasets, registrar metadatos y guardar versión.
2. Validate: revisar columnas, tipos, nulos, duplicados y llave territorial.
3. Clean: corregir tipos, fechas, codificación, nombres y duplicados.
4. Standardize: homologar unidades, nombres territoriales y formatos.
5. Integrate: unir datasets por localidad, UPZ, barrio o coordenadas.
6. Feature Engineering: construir variables derivadas.
7. Load: exportar datos curados, indicadores, índices y archivos para dashboard.

LOGGING: cada ejecución registra datasets usados, filas, advertencias, errores, archivos generados y fecha.
'@

Crear-Issue "Motores analíticos (Modeling)" "arquitectura-modeling" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002974855457" @'
SIPTA usa arquitectura híbrida: índices, análisis espacial, clustering, detección de anomalías, modelos predictivos condicionales y reglas de recomendación.

- Motor de índices compuestos: cobertura, infraestructura, equidad, riesgo, prioridad. Determinístico e interpretable.
- Motor espacial: proximidad a equipamientos, densidad de servicios, mapas de calor. Herramientas: GeoPandas, Shapely, Folium, QGIS o Power BI Maps.
- Clustering territorial: agrupa localidades con perfiles semejantes. Algoritmos: K-Means, jerárquico, DBSCAN (si hay coordenadas suficientes).
- Detección de anomalías: casos inusuales (alta inversión con bajo desempeño, alta vulnerabilidad con baja inversión). Métodos: Z-Score multivariable, Isolation Forest, Local Outlier Factor.
- Modelos predictivos: solo si hay datos históricos suficientes. Candidatos: regresión lineal, Random Forest, XGBoost, LightGBM.

CRITERIOS DE SELECCIÓN: interpretabilidad, robustez, facilidad de explicar al jurado, tiempo de entrenamiento, reproducibilidad, capacidad de soportar una decisión pública.
'@

# ============ 5. Plan de Trabajo, Scrum y Git Flow ============

Crear-Issue "Roles del equipo (3 personas) y matriz RACI" "plan-trabajo-scrum-gitflow" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217003044343687" @'
ROLES:
Persona A — Scrum Master + Data Engineer (secundario: Git Manager). Responsabilidades: backlog, ETL, calidad de datos, integración, ramas y merges.
Persona B — Data Scientist (secundario: Data Analyst). Responsabilidades: EDA, indicadores, feature engineering, modelos, validación estadística.
Persona C — Tech Lead + BI Developer (secundario: QA y documentación). Responsabilidades: arquitectura, dashboard, visualizaciones, pruebas funcionales, presentación.

MATRIZ RACI (R=Responsible, A=Accountable, C=Consulted, I=Informed):
Gestión del backlog: A=R, B=C, C=A
Ingesta de datos: A=A/R, B=C, C=I
EDA: A=C, B=A/R, C=I
Diccionario de datos: A=R, B=A, C=C
ETL: A=A/R, B=C, C=C
Indicadores: A=C, B=A/R, C=C
Modelos: A=C, B=A/R, C=C
Dashboard: A=I, B=C, C=A/R
Pruebas: A=R, B=C, C=A/R
Documentación final: A=C, B=R, C=A/R

REGLA OPERATIVA: cada sprint tiene un responsable principal por entregable y un revisor cruzado. Nadie aprueba su propio Pull Request.
'@

Crear-Issue "Cronograma por sprints (0–7, CRISP-DM)" "plan-trabajo-scrum-gitflow" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217003073075480" @'
Sprint 0 — Planeación: preparar proyecto (repo, Git Flow, estructura / README y convenciones / tablero Scrum y plantillas) → Entregable: Repositorio base.
Sprint 1 — Business Understanding: definir problema (stakeholders y riesgos / hipótesis y KPIs / diagramas y docs) → Project Charter.
Sprint 2 — Data Understanding: inventariar datos (descarga y catálogo / EDA inicial / diccionario y modelo territorial) → Catálogo de datos.
Sprint 3 — Data Preparation I: limpiar datos (ETL base / variables iniciales / calidad de datos) → Datos procesados.
Sprint 4 — Data Preparation II: integrar y crear features (pipeline integrado / índices territoriales / geoanalytics) → Dataset curado.
Sprint 5 — Modeling: modelar prioridad y alertas (clustering / modelo predictivo condicional / recomendaciones) → Motores analíticos.
Sprint 6 — Evaluation: validar resultados (pruebas ETL / validación modelos / testing dashboard) → Informe evaluación.
Sprint 7 — Deployment: entrega final (manual técnico / informe CRISP-DM / dashboard y presentación) → Producto final.
'@

Crear-Issue "Git Flow: ramas, PRs, commits y versionado" "plan-trabajo-scrum-gitflow" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002958248000" @'
RAMAS PRINCIPALES:
- main: versiones estables y entregables finales.
- develop: integra el trabajo aprobado de cada sprint.
- feature/*: desarrollo de funcionalidades o documentos.
- bugfix/*: correcciones antes del release.
- release/*: estabilización previa a entrega.
- hotfix/*: correcciones urgentes sobre main.

CONVENCIONES: feature/data-ingestion, feature/eda, feature/territorial-index, feature/recommendation-engine, bugfix/fix-locality-join, release/v1.0.0, hotfix/fix-dashboard-filter.

PULL REQUESTS: todo cambio hacia develop requiere PR, descripción de cambios, evidencia de prueba y revisión de otro integrante.

CONVENTIONAL COMMITS: feat(etl), feat(model), fix(validation), docs(crispdm), refactor(pipeline), test(indicators), chore(github).

VERSIONADO SEMÁNTICO: v0.1.0 estructura inicial, v0.5.0 pipeline e indicadores base, v0.8.0 modelos y dashboard preliminar, v1.0.0 entrega final.
'@

Crear-Issue "Scrum: ceremonias, Kanban, DoR y DoD" "plan-trabajo-scrum-gitflow" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002975216087" @'
CEREMONIAS:
- Sprint Planning: inicio de sprint, 60-120 min.
- Daily Scrum: diario, 15 min. Preguntas: ¿Qué hice ayer? ¿Qué haré hoy? ¿Tengo bloqueos?
- Backlog Refinement: mitad del sprint, 45-60 min.
- Sprint Review: cierre del sprint, 60 min.
- Retrospective: cierre del sprint, 45 min.

TABLERO KANBAN: Backlog (ideas no priorizadas) → To Do (listas para ejecutar) → In Progress (trabajo activo) → Code Review (PR abierto) → Testing (validación en curso) → Done (cumple DoD).

DEFINITION OF READY: descripción clara, responsable, criterio de aceptación, rama Git asociada si aplica, dependencia identificada.

DEFINITION OF DONE: código o documento terminado, pruebas ejecutadas, PR aprobado, merge a develop, documentación actualizada, sin bloqueos críticos.
'@

# ============ 6. Riesgos, Documentación y Cierre ============

Crear-Issue "Matriz de gestión de riesgos" "riesgos-documentacion-cierre" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002975148098" @'
Riesgo | Probabilidad | Impacto | Prioridad | Mitigación | Contingencia
Datos incompletos | Media | Alta | Alta | Evaluar calidad temprano | Usar indicadores alternativos o reglas
Sin series históricas | Media | Media | Media | Diseñar alertas por reglas | No prometer predicción robusta
Tiempo limitado | Alta | Alta | Crítica | MVP por sprints | Reducir alcance a localidades
Llaves territoriales inconsistentes | Media | Alta | Alta | Tabla de homologación | Agregación a localidad
Conflictos Git | Media | Media | Media | PRs pequeños y frecuentes | Resolver con Git Manager
Dashboard incompleto | Media | Alta | Alta | Prototipo temprano | Entregar mapa + ranking + recomendaciones
Modelo no interpretable | Baja | Alta | Media | Priorizar índices explicables | Excluir modelo complejo

POLÍTICA: los riesgos se revisan en cada Sprint Review. Si un riesgo pasa a prioridad crítica, el equipo ajusta el alcance antes de continuar con nuevas funcionalidades.
'@

Crear-Issue "Documentación obligatoria (responsables)" "riesgos-documentacion-cierre" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217002958452347" @'
Documento | Responsable | Contenido mínimo
README | Persona B | Objetivo, instalación, ejecución, estructura, uso
Manual técnico | Persona A | Arquitectura, pipeline, dependencias, ejecución
Manual de usuario | Persona C | Cómo interpretar dashboard e índices
Diccionario de datos | Persona C | Variables, tipos, unidades y fuente
Bitácora de decisiones | Persona A | Cambios metodológicos y justificación
Registro de cambios | Persona B | Versiones, mejoras y fixes
Arquitectura | Persona C | Diagramas, capas, modelo de datos
CRISP-DM Report | Persona B | Fases, hallazgos, modelos y evaluación
Modelo de datos | Persona A | Tablas, llaves y relaciones
Actas de reunión | Scrum Master | Acuerdos, bloqueos, acciones
Checklist de despliegue | Persona C | Pruebas, archivos, entrega y demo

BUENAS PRÁCTICAS: mantener documentación junto al código, documentar decisiones no solo resultados, nombres consistentes, evitar notebooks como única fuente de verdad, mantener datos raw intactos, registrar origen/fecha/versión de cada dataset, automatizar validaciones, revisar código por pares, mantener trazabilidad objetivo→dato→indicador→modelo→recomendación.
'@

Crear-Issue "Checklist final de entrega" "riesgos-documentacion-cierre" "https://app.asana.com/1/1216996162427896/project/1217017347499129/task/1217003044484050" @'
ANTES DE PRESENTAR:
[ ] Repositorio organizado y ejecutable
[ ] README actualizado
[ ] Datos raw separados de datos procesados
[ ] Diccionario de datos completo
[ ] Indicadores con ficha técnica
[ ] Índice de prioridad documentado
[ ] Pipeline ejecutable de principio a fin
[ ] Dashboard funcional
[ ] Recomendaciones trazables a datos
[ ] Presentación ejecutiva preparada
[ ] Riesgos y limitaciones declarados

MENSAJE EJECUTIVO DE CIERRE:
SIPTA permite que Bogotá priorice intervenciones territoriales con evidencia integrada. El sistema no reemplaza la decisión pública: la hace más transparente, comparable y medible. Su valor central es transformar datos abiertos dispersos en decisiones concretas de inversión, mantenimiento preventivo y cierre de brechas de servicios e infraestructura.
'@

Write-Output "Creando labels e issues en: https://github.com/$REPO/issues"

# End of script
