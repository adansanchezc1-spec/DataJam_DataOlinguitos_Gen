# SIPTA — Fichas técnicas de indicadores base

## 1. Propósito

Este documento contiene las fichas técnicas iniciales de los indicadores base
definidos para SIPTA.

Las fichas establecen la definición conceptual de cada indicador y distinguen
claramente entre:

- elementos ya definidos por la planificación del proyecto;
- elementos respaldados por fuentes conocidas;
- elementos que todavía requieren validación o definición metodológica.

Un indicador no se considera implementado ni validado únicamente por aparecer
en este documento.

---

# DEM-001 — Densidad poblacional

## Identificación

| Campo | Definición |
|---|---|
| Código | `DEM-001` |
| Nombre | Densidad poblacional |
| Clasificación | Demografía |
| Estado | Definido — pendiente de implementación |

## Objetivo

Medir la concentración de población en relación con la superficie territorial
de cada localidad.

## Pregunta de negocio

¿Qué localidades presentan una mayor o menor concentración de población por
unidad de superficie?

## Variables de entrada

- `poblacion`
- `area_km2`

## Fórmula

`Densidad poblacional = población / área_km2`

## Unidad

Habitantes por kilómetro cuadrado (`hab/km²`).

## Nivel geográfico

Localidad.

## Frecuencia

Pendiente de establecer según la periodicidad de actualización de la fuente
demográfica utilizada.

## Interpretación

Valores mayores representan una mayor concentración de habitantes por unidad de
superficie.

El indicador describe densidad territorial y no debe interpretarse de manera
aislada como una medida de bienestar, vulnerabilidad o necesidad.

## Visualización recomendada

- mapa coroplético por localidad;
- ranking de localidades.

## Decisión pública que apoya

Contextualizar demanda territorial, presión sobre infraestructura y comparación
entre localidades.

## Dependencias

- población por localidad;
- área oficial de cada localidad;
- `DIM_TERRITORIO`.

## Estado de fuente

Parcial. Las fuentes necesarias deben encontrarse disponibles e integradas en
la rama base antes de implementar el cálculo definitivo.

---

# SAL-001 — Hospitales por 10.000 habitantes

## Identificación

| Campo | Definición |
|---|---|
| Código | `SAL-001` |
| Nombre | Hospitales por 10.000 habitantes |
| Clasificación | Salud |
| Estado | Definido — pendiente de implementación |

## Objetivo

Medir la disponibilidad relativa de establecimientos de salud respecto a la
población de cada localidad.

## Pregunta de negocio

¿Qué localidades presentan menor disponibilidad relativa de infraestructura
sanitaria respecto a su población?

## Variables de entrada

Conceptualmente:

- número de establecimientos de salud;
- población de la localidad.

La definición exacta de qué registros serán considerados "hospitales" deberá
establecerse antes de implementar el indicador.

## Fórmula

`Hospitales por 10.000 habitantes = hospitales / población × 10.000`

## Unidad

Hospitales por 10.000 habitantes.

## Nivel geográfico

Localidad.

## Frecuencia

Pendiente según las fuentes definitivas de salud y población.

## Interpretación

Valores mayores representan una mayor disponibilidad relativa de
establecimientos incluidos en la definición operacional del indicador.

No representa por sí solo capacidad instalada, calidad del servicio ni acceso
efectivo.

## Visualización recomendada

- mapa coroplético;
- ranking;
- comparación con población.

## Decisión pública que apoya

Apoyar la identificación de localidades con menor oferta relativa y orientar
análisis de infraestructura sanitaria.

## Dependencias

- fuente validada de establecimientos de salud;
- territorialización de cada establecimiento;
- población por localidad;
- `DIM_TERRITORIO`.

## Observación metodológica

El dataset de instituciones con servicios de urgencias validado previamente no
debe equipararse automáticamente con el universo completo de "hospitales".

La definición operacional deberá documentarse antes del cálculo.

---

# SAL-002 — Camas por 10.000 habitantes

## Identificación

| Campo | Definición |
|---|---|
| Código | `SAL-002` |
| Nombre | Camas por 10.000 habitantes |
| Clasificación | Salud |
| Estado | Fuente pendiente |

## Objetivo

Medir la capacidad relativa de camas disponibles respecto a la población de
cada localidad.

## Pregunta de negocio

¿Qué localidades presentan menor capacidad relativa de camas respecto a su
población?

## Variables de entrada

- número de camas;
- población.

La variable exacta de camas y su definición todavía deben verificarse con una
fuente oficial adecuada.

## Fórmula

`Camas por 10.000 habitantes = camas / población × 10.000`

## Unidad

Camas por 10.000 habitantes.

## Nivel geográfico

Localidad.

## Frecuencia

Pendiente.

## Interpretación

Valores mayores representan mayor disponibilidad relativa de camas según la
definición de la fuente utilizada.

## Visualización recomendada

- mapa coroplético;
- ranking territorial.

## Decisión pública que apoya

Apoyar análisis de capacidad sanitaria y necesidades territoriales de atención.

## Dependencias

- fuente oficial de camas;
- territorialización;
- población;
- `DIM_TERRITORIO`.

## Estado de fuente

Pendiente de validación.

No debe implementarse sustituyendo "camas" por otra variable sanitaria.

---

# EDU-001 — Colegios por población objetivo

## Identificación

| Campo | Definición |
|---|---|
| Código | `EDU-001` |
| Nombre | Colegios por población objetivo |
| Clasificación | Educación |
| Estado | Definido — requiere definición de denominador |

## Objetivo

Medir la disponibilidad relativa de establecimientos educativos frente a la
población que potencialmente demanda el servicio.

## Pregunta de negocio

¿Qué localidades presentan menor disponibilidad relativa de colegios respecto a
su población objetivo?

## Variables de entrada

- número de colegios;
- población objetivo.

## Fórmula conceptual

`Colegios por población objetivo = colegios / población objetivo`

## Unidad

Razón de colegios por población objetivo.

La escala definitiva deberá establecerse antes de la implementación, por
ejemplo por cada 1.000, 10.000 u otra base técnicamente justificada.

## Nivel geográfico

Localidad.

## Frecuencia

Pendiente según las fuentes definitivas.

## Interpretación

Valores mayores representarían mayor disponibilidad relativa de
establecimientos frente a la población objetivo definida.

## Visualización recomendada

- mapa;
- ranking;
- comparación oferta-demanda.

## Decisión pública que apoya

Identificar territorios con menor disponibilidad relativa de infraestructura
educativa.

## Dependencias

- identificación de establecimientos;
- definición de población objetivo;
- fuente demográfica compatible;
- `DIM_TERRITORIO`.

## Observación metodológica

La fuente de oferta de cupos contiene establecimientos educativos, pero la
población objetivo todavía debe definirse de forma explícita y compatible con
el indicador.

No se debe utilizar población total como sustituto automático.

---

# EDU-003 — Cobertura educativa

## Identificación

| Campo | Definición |
|---|---|
| Código | `EDU-003` |
| Nombre | Cobertura educativa |
| Clasificación | Educación |
| Estado | Definición operativa pendiente |

## Objetivo

Medir la relación entre la matrícula o cobertura observada y la población
objetivo correspondiente.

## Pregunta de negocio

¿Dónde existen mayores brechas de cobertura educativa?

## Variables de entrada

Conceptualmente:

- matrícula;
- población objetivo.

Las variables exactas deberán establecerse antes del cálculo.

## Fórmula conceptual

`Cobertura educativa = matrícula / población objetivo`

## Unidad

Proporción o porcentaje.

## Nivel geográfico

Localidad.

## Frecuencia

Pendiente.

## Interpretación

Valores mayores representarían una mayor cobertura relativa respecto a la
población objetivo definida.

La interpretación dependerá de la definición exacta de matrícula, población
objetivo y nivel educativo incluido.

## Visualización recomendada

- mapa coroplético;
- ranking;
- radar territorial cuando forme parte de una dimensión educativa.

## Decisión pública que apoya

Apoyar decisiones relacionadas con ampliación de cobertura, cupos o capacidad
educativa.

## Dependencias

- fuente de matrícula;
- definición de población objetivo;
- período común de referencia;
- territorialización.

## Observación metodológica

La fuente de oferta de cupos validada no debe interpretarse automáticamente como
matrícula.

La variable `OTotal` representa oferta dentro de esa fuente y no será utilizada
como matrícula sin respaldo documental.

---

# MOV-001 — Tiempo promedio de viaje

## Identificación

| Campo | Definición |
|---|---|
| Código | `MOV-001` |
| Nombre | Tiempo promedio de viaje |
| Clasificación | Movilidad |
| Estado | Fuente pendiente |

## Objetivo

Medir el tiempo promedio requerido para los desplazamientos asociados a cada
territorio.

## Pregunta de negocio

¿Qué territorios presentan mayores tiempos promedio de viaje?

## Variables de entrada

Pendientes de identificar en la fuente validada de movilidad.

Como mínimo será necesaria una variable de duración o tiempo de desplazamiento
y una regla territorial claramente definida.

## Fórmula conceptual

`Tiempo promedio de viaje = promedio(tiempo de viaje)`

## Unidad

Pendiente según la unidad de la fuente, previsiblemente una unidad de tiempo.

## Nivel geográfico

Localidad, sujeto a la granularidad y territorialización de la fuente.

## Frecuencia

Pendiente.

## Interpretación

Valores mayores indicarían mayor duración promedio de los desplazamientos bajo
la definición utilizada.

## Visualización recomendada

- mapa;
- ranking;
- distribución territorial.

## Decisión pública que apoya

Apoyar análisis de accesibilidad y decisiones relacionadas con conectividad.

## Dependencias

- fuente validada de movilidad;
- variable de tiempo;
- definición del origen territorial del indicador.

---

# INF-004 — Espacio público por habitante

## Identificación

| Campo | Definición |
|---|---|
| Código | `INF-004` |
| Nombre | Espacio público por habitante |
| Clasificación | Infraestructura / espacio público |
| Estado | Fuente pendiente |

## Objetivo

Medir la disponibilidad relativa de espacio público respecto a la población de
cada localidad.

## Pregunta de negocio

¿Qué localidades presentan menor disponibilidad de espacio público por
habitante?

## Variables de entrada

- superficie de espacio público en m²;
- población.

## Fórmula

`Espacio público por habitante = m² de espacio público / población`

## Unidad

Metros cuadrados por habitante (`m²/hab`).

## Nivel geográfico

Localidad.

## Frecuencia

Pendiente.

## Interpretación

Valores mayores representan mayor superficie de espacio público disponible por
habitante según las categorías incluidas en la fuente.

## Visualización recomendada

- mapa coroplético;
- ranking.

## Decisión pública que apoya

Priorizar intervenciones relacionadas con parques, espacio público y
mantenimiento territorial.

## Dependencias

- fuente oficial de espacio público;
- regla de agregación territorial;
- población;
- `DIM_TERRITORIO`.

---

# FIN-001 — Inversión per cápita

## Identificación

| Campo | Definición |
|---|---|
| Código | `FIN-001` |
| Nombre | Inversión per cápita |
| Clasificación | Finanzas públicas |
| Estado | Fuente pendiente |

## Objetivo

Medir los recursos de inversión ejecutados en relación con la población del
territorio.

## Pregunta de negocio

¿La distribución territorial de la inversión guarda relación con la población
y las necesidades observadas?

## Variables de entrada

- presupuesto o inversión ejecutada;
- población.

La definición exacta del numerador deberá conservar la terminología de la
fuente financiera seleccionada.

## Fórmula

`Inversión per cápita = presupuesto ejecutado / población`

## Unidad

Unidad monetaria por habitante.

La moneda y escala deberán documentarse según la fuente.

## Nivel geográfico

Localidad cuando la fuente permita territorialización a ese nivel.

## Frecuencia

Pendiente según periodicidad presupuestal.

## Interpretación

Valores mayores indican mayor inversión ejecutada por habitante.

No representa por sí solo eficiencia, suficiencia ni equidad.

## Visualización recomendada

- mapa;
- ranking;
- comparación con índices de necesidad territorial.

## Decisión pública que apoya

Apoyar análisis de focalización y distribución territorial de recursos.

## Dependencias

- fuente financiera validada;
- territorialización del gasto;
- población;
- período presupuestal compatible.

---

# FIN-002 — Ejecución presupuestal

## Identificación

| Campo | Definición |
|---|---|
| Código | `FIN-002` |
| Nombre | Ejecución presupuestal |
| Clasificación | Finanzas públicas |
| Estado | Fuente pendiente |

## Objetivo

Medir la proporción del presupuesto aprobado que ha sido ejecutado.

## Pregunta de negocio

¿Qué territorios o componentes presentan menores niveles relativos de ejecución
presupuestal?

## Variables de entrada

- presupuesto ejecutado;
- presupuesto aprobado.

## Fórmula

`Ejecución presupuestal = ejecutado / aprobado`

Si se expresa como porcentaje:

`Ejecución presupuestal (%) = ejecutado / aprobado × 100`

## Unidad

Proporción o porcentaje.

## Nivel geográfico

Localidad cuando la fuente permita una asignación territorial consistente.

## Frecuencia

Pendiente según la periodicidad de la fuente presupuestal.

## Interpretación

Valores mayores representan una mayor proporción de ejecución respecto al
presupuesto aprobado.

Este indicador no evalúa por sí solo la pertinencia ni el impacto del gasto.

## Visualización recomendada

- ranking;
- barras;
- mapa cuando exista territorialización válida.

## Decisión pública que apoya

Apoyar seguimiento de ejecución y detección de territorios o componentes que
requieren revisión.

## Dependencias

- presupuesto aprobado;
- presupuesto ejecutado;
- período de referencia;
- territorialización cuando aplique.

---

# SOC-001 — Vulnerabilidad territorial

## Identificación

| Campo | Definición |
|---|---|
| Código | `SOC-001` |
| Nombre | Vulnerabilidad territorial |
| Clasificación | Social / vulnerabilidad |
| Estado | Definición metodológica pendiente |

## Objetivo

Construir una medida compuesta que sintetice múltiples dimensiones de
vulnerabilidad territorial.

## Pregunta de negocio

¿Qué localidades concentran mayores condiciones relativas de vulnerabilidad?

## Variables de entrada

Pendientes.

Las variables dependerán de las dimensiones e indicadores finalmente
seleccionados.

## Fórmula

Índice compuesto.

La fórmula definitiva está pendiente de definición.

## Unidad

Índice adimensional.

La escala final deberá definirse metodológicamente.

## Nivel geográfico

Localidad.

## Frecuencia

Pendiente según la periodicidad de los indicadores componentes.

## Interpretación

Pendiente de la definición de:

- variables componentes;
- sentido de cada indicador;
- normalización;
- ponderaciones;
- escala.

## Visualización recomendada

- mapa;
- ranking;
- radar de brechas.

## Decisión pública que apoya

Apoyar la priorización de territorios con concentración multidimensional de
brechas.

## Dependencias

- indicadores componentes validados;
- método de normalización;
- pesos;
- reglas de agregación.

## Restricción metodológica

No se asignarán pesos, variables ni dimensiones por conveniencia.

La construcción de este índice deberá justificarse y validarse antes de su
implementación.

---

# Checklist general de aceptación

Cada indicador deberá superar, antes de considerarse validado:

| Criterio | Requisito |
|---|---|
| Definición clara | Obligatorio |
| Fórmula documentada | Obligatorio |
| Variables disponibles | Obligatorio |
| Fuente identificada | Obligatorio |
| Resultado reproducible | Obligatorio |
| Interpretación consistente | Obligatorio |
| Vinculado a una decisión pública | Obligatorio |
| Validado por al menos dos integrantes | Obligatorio |

---

# Estado general

## Definición conceptual disponible

- `DEM-001`
- `SAL-001`
- `SAL-002`
- `EDU-001`
- `EDU-003`
- `MOV-001`
- `INF-004`
- `FIN-001`
- `FIN-002`
- `SOC-001`

## Pendiente para fase de implementación

- confirmar fuentes definitivas;
- confirmar variables reales;
- definir períodos compatibles;
- implementar territorialización;
- completar `DIM_TERRITORIO`;
- ejecutar las fórmulas de manera reproducible;
- validar resultados;
- obtener revisión de al menos dos integrantes.