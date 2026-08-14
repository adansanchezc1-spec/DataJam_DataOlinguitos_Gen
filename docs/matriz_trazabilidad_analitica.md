# SIPTA — Matriz de trazabilidad analítica

## 1. Propósito

La matriz de trazabilidad analítica garantiza que cada análisis realizado en
SIPTA responda a una necesidad de política pública y pueda rastrearse desde el
problema identificado hasta la decisión que pretende apoyar.

Su función es evitar la construcción de indicadores, visualizaciones o
recomendaciones aisladas que no tengan una relación explícita con una pregunta
estratégica y con evidencia proveniente de los datos.

---

## 2. Cadena de trazabilidad

La lógica definida para SIPTA es:

`Problema público → Pregunta estratégica → Objetivo analítico → Datasets → Variables → Indicadores → Índices → Visualización → Recomendación → Decisión pública`

Cada elemento deberá conservar relación explícita con el anterior.

---

## 3. Componentes

### Problema público

Situación territorial que requiere comprensión, seguimiento o intervención.

### Pregunta estratégica

Pregunta que transforma el problema público en una necesidad concreta de
análisis.

### Objetivo analítico

Resultado específico que se busca obtener mediante el análisis de los datos.

### Datasets

Fuentes de información utilizadas para responder la pregunta estratégica.

### Variables

Campos concretos requeridos de los datasets seleccionados.

### Indicadores

Medidas calculadas a partir de las variables para representar el fenómeno
analizado.

### Índices

Medidas compuestas que permiten sintetizar varios indicadores cuando el
problema lo requiera.

### Visualización

Representación utilizada para comunicar el resultado analítico.

### Recomendación

Acción sugerida a partir de la evidencia obtenida.

### Decisión pública

Decisión de planeación, inversión, intervención o seguimiento que puede ser
soportada por el análisis.

---

## 4. Matriz base definida para SIPTA

Los siguientes casos corresponden a los ejemplos definidos para la matriz de
trazabilidad del proyecto.

| Problema público | Pregunta estratégica | Indicador | Índice / dimensión | Decisión pública |
|---|---|---|---|---|
| Acceso desigual a salud | ¿Qué localidades tienen menor acceso relativo? | Hospitales por 10.000 habitantes | Cobertura en salud | Priorizar infraestructura sanitaria |
| Déficit educativo | ¿Dónde hay mayores brechas educativas? | Cobertura educativa | Índice educativo | Ampliar cupos o colegios |
| Baja cobertura de parques | ¿Qué zonas tienen menor espacio público? | m² por habitante | Espacio público | Priorizar parques y mantenimiento |
| Baja accesibilidad | ¿Qué territorios tienen mayores tiempos? | Tiempo promedio | Accesibilidad | Mejorar conectividad |
| Inversión insuficiente | ¿La inversión coincide con la necesidad? | Inversión per cápita | Equidad territorial | Redistribuir o focalizar recursos |
| Infraestructura deteriorada | ¿Dónde se requiere mantenimiento preventivo? | % deterioro | Riesgo territorial | Plan preventivo de mantenimiento |

> Esta tabla conserva los ejemplos establecidos en la planificación del
> proyecto. Los componentes que aún no se encuentran especificados no deben
> completarse mediante supuestos.

---

## 5. Matriz completa de trazabilidad

La implementación definitiva deberá documentar cada análisis mediante la
siguiente estructura:

| Campo | Descripción |
|---|---|
| `problema_publico` | Problema territorial que motiva el análisis |
| `pregunta_estrategica` | Pregunta que se busca responder |
| `objetivo_analitico` | Resultado analítico esperado |
| `datasets` | Fuentes utilizadas |
| `variables` | Variables requeridas |
| `indicadores` | Indicadores calculados |
| `indices` | Índices o dimensiones asociadas |
| `visualizacion` | Representación utilizada |
| `recomendacion` | Acción propuesta a partir de los resultados |
| `decision_publica` | Decisión que el análisis busca apoyar |
| `indicador_seguimiento` | Indicador utilizado para evaluar posteriormente la decisión |

---

## 6. Plantilla de aplicación

| Problema público | Pregunta estratégica | Objetivo analítico | Datasets | Variables | Indicador | Índice | Visualización | Recomendación | Decisión pública | Indicador de seguimiento |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

Esta plantilla deberá completarse progresivamente a medida que los datasets,
indicadores y productos analíticos sean definidos y validados.

---

## 7. Reglas de uso

### Regla 1 — Pregunta antes que visualización

Ningún gráfico se construye sin una pregunta estratégica.

Una visualización debe existir para comunicar una respuesta analítica y no
solamente porque una variable pueda graficarse.

---

### Regla 2 — Indicadores documentados

Ningún indicador se acepta sin:

- fórmula;
- fuente;
- interpretación.

La definición detallada de estos elementos se realizará en el
**Inventario Maestro de Indicadores y fichas técnicas**.

---

### Regla 3 — Recomendaciones con evidencia

Ninguna recomendación se presenta sin:

- evidencia proveniente de datos;
- relación con uno o más indicadores;
- entidad o actor responsable cuando corresponda.

---

### Regla 4 — Seguimiento de decisiones

Toda decisión pública debe conectarse con al menos un indicador que permita
evaluar posteriormente su comportamiento o impacto.

---

## 8. Relación con el inventario maestro de indicadores

La matriz de trazabilidad define **por qué** se necesita un indicador.

El Inventario Maestro de Indicadores definirá posteriormente **cómo** se
construye.

La relación conceptual es:

`Problema → Pregunta → Indicador necesario`

y posteriormente:

`Indicador → Variables → Fórmula → Fuente → Unidad → Interpretación`

Por esta razón, la matriz de trazabilidad debe preceder a la formalización
definitiva del inventario de indicadores.

---

## 9. Relación con los dominios

La matriz puede requerir información procedente de más de un dominio.

Ejemplo conceptual:

`Cobertura sanitaria`

puede requerir:

`Salud + Demografía`

mientras que:

`Inversión per cápita`

puede requerir:

`Finanzas públicas + Demografía`

Esto no implica que un responsable deba repetir la validación de los dominios
de otro integrante.

Los resultados validados de cada dominio serán consumidos posteriormente por
la capa analítica común.

---

## 10. Trazabilidad mínima requerida

Para considerar un análisis completamente trazable deberán conocerse como
mínimo:

1. problema público;
2. pregunta estratégica;
3. objetivo analítico;
4. datasets utilizados;
5. variables utilizadas;
6. indicador y su fórmula;
7. fuente de los datos;
8. interpretación del resultado;
9. producto o visualización;
10. recomendación;
11. decisión pública que apoya;
12. indicador de seguimiento.

---

## 11. Estado actual

- Lógica de trazabilidad: definida.
- Problemas públicos iniciales: definidos.
- Preguntas estratégicas iniciales: definidas.
- Indicadores candidatos iniciales: definidos.
- Índices o dimensiones iniciales: definidos.
- Decisiones públicas iniciales: definidas.
- Datasets definitivos por análisis: pendiente.
- Variables definitivas por análisis: pendiente.
- Objetivos analíticos específicos por fila: pendiente de formalización.
- Visualizaciones definitivas: pendientes.
- Indicadores de seguimiento: pendientes.