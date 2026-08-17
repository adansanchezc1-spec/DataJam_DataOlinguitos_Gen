# SIPTA — Inventario maestro de indicadores

## 1. Propósito

Este documento consolida los indicadores definidos para el proyecto SIPTA y
establece una referencia común para su posterior implementación, validación y
uso en el modelo territorial.

El inventario permite identificar:

- qué se desea medir;
- a qué dimensión pertenece cada indicador;
- qué fórmula conceptual lo define;
- qué información se necesita para calcularlo;
- qué decisión pública busca apoyar;
- cuál es su estado actual dentro del proyecto.

La inclusión de un indicador en este inventario no significa que ya se
encuentre calculado o validado.

---

## 2. Clasificación

La clasificación definida para los indicadores del proyecto es:

| Código | Clasificación |
|---|---|
| `DEM` | Demografía |
| `SAL` | Salud |
| `EDU` | Educación |
| `MOV` | Movilidad |
| `INF` | Infraestructura / espacio público |
| `FIN` | Finanzas públicas |
| `SOC` | Componente social / vulnerabilidad |
| `AMB` | Ambiente |
| `PAR` | Participación ciudadana |

> La clasificación se conserva de acuerdo con la planificación actual del
> proyecto. La incorporación de nuevas clasificaciones deberá quedar
> documentada y acordada por el equipo.

---

## 3. Indicadores base

| Código | Indicador | Fórmula conceptual | Unidad esperada | Estado |
|---|---|---|---|---|
| `DEM-001` | Densidad poblacional | Población / área_km2 | habitantes/km² | Pendiente de implementación |
| `SAL-001` | Hospitales por 10.000 habitantes | Hospitales / población × 10.000 | hospitales por 10.000 habitantes | Pendiente de implementación |
| `SAL-002` | Camas por 10.000 habitantes | Camas / población × 10.000 | camas por 10.000 habitantes | Pendiente de fuente validada |
| `EDU-001` | Colegios por población objetivo | Colegios / población escolar | colegios por población objetivo | Pendiente de implementación |
| `EDU-003` | Cobertura educativa | Matrícula / población objetivo | proporción o porcentaje | Pendiente de definición operativa |
| `MOV-001` | Tiempo promedio de viaje | Promedio de tiempo | tiempo promedio | Pendiente de fuente validada |
| `INF-004` | Espacio público por habitante | m² de espacio público / población | m² por habitante | Pendiente de fuente validada |
| `FIN-001` | Inversión per cápita | Presupuesto ejecutado / población | moneda por habitante | Pendiente de fuente validada |
| `FIN-002` | Ejecución presupuestal | Ejecutado / aprobado | proporción o porcentaje | Pendiente de fuente validada |
| `SOC-001` | Vulnerabilidad territorial | Índice compuesto | índice | Pendiente de definición metodológica |

---

## 4. Reglas del inventario

### 4.1. Conservación de códigos

Los códigos definidos en la planificación del proyecto se conservarán sin
renumerarlos arbitrariamente.

Por ejemplo, `EDU-003` no deberá cambiarse a `EDU-002` únicamente porque no
aparezca actualmente un indicador `EDU-002`.

---

### 4.2. Fórmula conceptual frente a fórmula implementada

Las fórmulas registradas inicialmente representan la lógica conceptual del
indicador.

Antes de considerar un indicador implementado deberán definirse con precisión:

- variables de entrada;
- fuente;
- nivel territorial;
- período de referencia;
- tratamiento de valores faltantes;
- denominador;
- unidad;
- transformación necesaria.

---

### 4.3. No inventar variables o fuentes

Cuando una variable requerida no se encuentre disponible o validada, el
indicador deberá permanecer como pendiente.

No deberán sustituirse variables únicamente para lograr producir un resultado.

---

### 4.4. Comparabilidad territorial

Los indicadores deberán permitir comparaciones entre localidades cuando ese sea
su propósito.

Los valores absolutos deberán normalizarse cuando población, área, demanda,
capacidad u otra característica territorial afecte la interpretación.

---

### 4.5. Trazabilidad

Todo indicador implementado deberá mantener relación con:

`Problema público → Pregunta estratégica → Dataset → Variables → Fórmula → Indicador → Interpretación → Decisión pública`

La relación detallada se documentará mediante la matriz de trazabilidad
analítica.

---

## 5. Ficha técnica mínima

Cada indicador deberá disponer como mínimo de los siguientes campos:

| Campo | Descripción |
|---|---|
| Código | Identificador único del indicador |
| Nombre | Nombre descriptivo |
| Objetivo | Qué busca medir |
| Pregunta de negocio | Pregunta estratégica que busca responder |
| Variables de entrada | Variables necesarias para su cálculo |
| Fórmula | Regla matemática o lógica |
| Unidad | Unidad del resultado |
| Nivel geográfico | Nivel territorial del indicador |
| Frecuencia | Periodicidad esperada |
| Interpretación | Significado del valor obtenido |
| Visualización recomendada | Forma sugerida de comunicarlo |
| Decisión pública que apoya | Uso esperado dentro de SIPTA |

---

## 6. Estados de implementación

Para distinguir entre definición conceptual y disponibilidad real se utilizarán
los siguientes estados:

| Estado | Significado |
|---|---|
| `Definido` | El indicador cuenta con definición conceptual |
| `Fuente pendiente` | Se conoce la definición, pero falta validar la fuente necesaria |
| `Variables pendientes` | La fuente existe, pero falta confirmar variables requeridas |
| `Implementable` | Fuente y variables necesarias se encuentran disponibles |
| `Implementado` | Existe código reproducible para su cálculo |
| `Validado` | El resultado fue revisado y cumple los criterios de aceptación |

Un indicador no deberá considerarse validado únicamente porque el código se
ejecute sin errores.

---

## 7. Checklist de aceptación

Antes de aprobar un indicador deberá verificarse:

| Criterio | Estado |
|---|---|
| Definición clara | Pendiente |
| Fórmula documentada | Pendiente |
| Variables disponibles | Pendiente |
| Fuente identificada | Pendiente |
| Resultado reproducible | Pendiente |
| Interpretación consistente | Pendiente |
| Vinculado a una decisión pública | Pendiente |
| Validado por al menos dos integrantes | Pendiente |

---

## 8. Relación preliminar con la trazabilidad

| Indicador | Problema / necesidad relacionada | Decisión pública esperada |
|---|---|---|
| `DEM-001` Densidad poblacional | Concentración territorial de población | Contextualizar demanda y presión territorial |
| `SAL-001` Hospitales por 10.000 habitantes | Acceso desigual a servicios de salud | Priorizar infraestructura sanitaria |
| `SAL-002` Camas por 10.000 habitantes | Capacidad sanitaria desigual | Priorizar capacidad de atención |
| `EDU-001` Colegios por población objetivo | Disponibilidad desigual de infraestructura educativa | Identificar déficit de oferta |
| `EDU-003` Cobertura educativa | Déficit educativo | Ampliar cupos o cobertura |
| `MOV-001` Tiempo promedio de viaje | Baja accesibilidad | Mejorar conectividad |
| `INF-004` Espacio público por habitante | Baja cobertura de espacio público | Priorizar parques y mantenimiento |
| `FIN-001` Inversión per cápita | Distribución desigual de recursos | Redistribuir o focalizar inversión |
| `FIN-002` Ejecución presupuestal | Capacidad desigual de ejecución | Mejorar seguimiento de recursos |
| `SOC-001` Vulnerabilidad territorial | Concentración multidimensional de brechas | Priorizar territorios |

> Estas relaciones son preliminares y deberán consolidarse con la matriz de
> trazabilidad y las fichas técnicas definitivas.

---

## 9. Dependencias principales

Varios indicadores dependen de información común.

### Población

Será necesaria para:

`DEM-001`, `SAL-001`, `SAL-002`, `INF-004`, `FIN-001` y potencialmente otros
indicadores normalizados.

La población deberá provenir de una fuente demográfica validada y utilizar un
período de referencia documentado.

### DIM_TERRITORIO

Permitirá asociar los resultados a una localidad común y aportar atributos
territoriales como área y población.

### Fuentes sectoriales

Cada indicador deberá utilizar únicamente datasets que hayan superado la fase
de entendimiento y validación correspondiente.

---

## 10. Indicadores que requieren definición adicional

### EDU-003 — Cobertura educativa

La fórmula conceptual está definida como:

`Matrícula / población objetivo`

Antes de implementarla deberá precisarse:

- qué variable representa matrícula;
- qué población constituye la población objetivo;
- período de referencia;
- nivel educativo incluido.

---

### SOC-001 — Vulnerabilidad territorial

Se define como un índice compuesto.

Antes de implementarlo deberán establecerse:

- dimensiones componentes;
- indicadores utilizados;
- normalización;
- ponderaciones;
- dirección de cada variable;
- escala final;
- interpretación.

No se asignarán componentes o pesos arbitrariamente.

---

## 11. Estado actual

| Código | Definición conceptual | Fuente validada | Implementación | Validación |
|---|---|---|---|---|
| DEM-001 | Sí | Parcial / depende de integración | Pendiente | Pendiente |
| SAL-001 | Sí | Parcial / depende de integración | Pendiente | Pendiente |
| SAL-002 | Sí | Pendiente | Pendiente | Pendiente |
| EDU-001 | Sí | Parcial / depende de integración | Pendiente | Pendiente |
| EDU-003 | Parcial | Parcial | Pendiente | Pendiente |
| MOV-001 | Sí | Pendiente | Pendiente | Pendiente |
| INF-004 | Sí | Pendiente | Pendiente | Pendiente |
| FIN-001 | Sí | Pendiente | Pendiente | Pendiente |
| FIN-002 | Sí | Pendiente | Pendiente | Pendiente |
| SOC-001 | Parcial | Pendiente | Pendiente | Pendiente |

---

## 12. Próximo paso

El siguiente paso consiste en elaborar la ficha técnica individual de cada
indicador base.

Las fichas deberán conservar como pendientes los campos que aún no puedan
respaldarse con fuentes y variables efectivamente disponibles.