# SIPTA — Matriz de calidad de datos y criterios de aceptación

## 1. Propósito

Este documento establece el marco común para evaluar la calidad de los
datasets utilizados en SIPTA antes de su integración al modelo territorial
maestro y su utilización en indicadores, índices y mecanismos de priorización.

La evaluación busca identificar limitaciones de los datos de manera
reproducible y trazable, evitando aplicar correcciones arbitrarias sobre las
fuentes originales.

---

## 2. Alcance de la evaluación

La matriz se aplica a los datasets seleccionados para los distintos dominios
del proyecto.

La evaluación de calidad no implica automáticamente:

- limpieza;
- corrección de valores;
- eliminación de registros;
- integración territorial;
- cálculo de indicadores.

Estas operaciones, cuando sean necesarias, corresponden a etapas posteriores.

---

## 3. Dimensiones de calidad

### 3.1. Completitud

**Pregunta:** ¿Hay valores faltantes?

**Métricas principales:**

- número de valores nulos;
- porcentaje de valores nulos por variable;
- número de registros con ausencia de variables críticas.

La ausencia de un valor no implica por sí sola que el dataset deba rechazarse.

La importancia del valor faltante dependerá del uso analítico de la variable.

Ejemplo:

- un teléfono faltante puede ser no crítico para análisis territorial;
- una localidad o coordenada faltante puede ser crítica si constituye el único
  mecanismo de territorialización.

---

### 3.2. Consistencia

**Pregunta:** ¿Existen contradicciones entre los datos?

**Métricas principales:**

- número de registros inconsistentes;
- relaciones lógicas incumplidas;
- contradicciones entre variables;
- inconsistencias entre atributo territorial y geometría.

Ejemplos:

- total diferente a la suma de sus componentes;
- mismo identificador asociado a nombres incompatibles;
- código de localidad diferente a la localidad determinada espacialmente.

Las inconsistencias deben documentarse antes de aplicar cualquier corrección.

---

### 3.3. Validez

**Pregunta:** ¿Los valores cumplen las reglas esperadas de tipo, formato o
rango?

**Métricas principales:**

- porcentaje de valores válidos;
- número de valores fuera de rango;
- número de valores no convertibles al tipo esperado;
- geometrías inválidas cuando corresponda.

Ejemplos:

- coordenadas dentro de rangos geográficos válidos;
- códigos pertenecientes al catálogo esperado;
- fechas interpretables;
- variables numéricas sin valores imposibles;
- geometrías válidas.

---

### 3.4. Unicidad

**Pregunta:** ¿Existen duplicados?

**Métricas principales:**

- número de duplicados exactos;
- porcentaje de duplicados exactos;
- duplicados según claves candidatas;
- cardinalidad de identificadores.

La repetición de un identificador no deberá clasificarse automáticamente como
duplicado.

Antes de eliminar registros se deberá analizar la granularidad real del
dataset.

Ejemplo:

un establecimiento puede aparecer varias veces porque posee diferentes sedes,
niveles, períodos, servicios o características.

---

### 3.5. Actualidad

**Pregunta:** ¿Los datos tienen una fecha de corte adecuada para el análisis?

**Métricas principales:**

- fecha de actualización;
- fecha de corte;
- período cubierto;
- antigüedad respecto al período analítico del proyecto.

La actualidad deberá evaluarse considerando la naturaleza de cada fuente.

No todos los dominios requieren la misma periodicidad de actualización.

---

### 3.6. Precisión

**Pregunta:** ¿Los valores son confiables respecto a otras evidencias
disponibles?

**Métrica principal:**

- validación cruzada.

La precisión podrá evaluarse mediante:

- contraste con otra fuente oficial;
- contraste entre atributos y geometría;
- coherencia con catálogos oficiales;
- comparación con metadatos de la fuente;
- verificación de fórmulas o totales publicados.

La ausencia de una fuente externa de contraste deberá documentarse como una
limitación y no interpretarse automáticamente como falta de precisión.

---

## 4. Variables críticas

No todas las variables de un dataset tienen la misma importancia.

Para cada fuente deberán identificarse las variables necesarias para:

1. territorialización;
2. construcción de indicadores;
3. normalización;
4. identificación de registros;
5. interpretación temporal.

Las reglas de aceptación deberán ser más estrictas para las variables
consideradas críticas.

---

## 5. Matriz de evaluación

La siguiente estructura deberá utilizarse para registrar la evaluación de cada
dataset:

| Dominio | Dataset | Dimensión | Variable/regla | Métrica | Resultado | Criticidad | Observación |
|---|---|---|---|---|---|---|---|
| Ejemplo | Dataset A | Completitud | Localidad | % nulos | Pendiente | Alta | Variable necesaria para territorialización |
| Ejemplo | Dataset A | Unicidad | Fila completa | % duplicados | Pendiente | Media | Revisar granularidad antes de eliminar |
| Ejemplo | Dataset A | Actualidad | Fecha de corte | Fecha | Pendiente | Alta | Comparar con período analítico |

### Criticidad

Se utilizarán tres niveles:

- **Alta:** puede impedir el uso del dataset para el objetivo analítico.
- **Media:** afecta parcialmente la calidad o requiere tratamiento documentado.
- **Baja:** no impide el análisis principal, aunque debe registrarse.

---

## 6. Criterios de aceptación de un dataset

Un dataset candidato debe evaluarse considerando los siguientes criterios.

### 6.1. Cobertura territorial identificable

Debe existir una forma reproducible de asociar los registros con el territorio
analizado.

Puede realizarse mediante:

- código de localidad;
- nombre de localidad;
- unidad territorial homologable;
- coordenadas geográficas;
- relación espacial con una fuente territorial oficial.

---

### 6.2. Variables relevantes para el objetivo

El dataset debe contener variables que contribuyan de manera directa al
problema, indicador, índice o análisis para el cual fue seleccionado.

La existencia de muchas variables no implica mayor utilidad analítica.

---

### 6.3. Calidad aceptable

El dataset deberá superar los controles de calidad necesarios para su uso
previsto.

No se establece un único porcentaje universal de aceptación para todos los
datasets.

La aceptación deberá considerar:

- dimensión de calidad afectada;
- variable afectada;
- criticidad;
- porcentaje o cantidad de registros involucrados;
- posibilidad de tratamiento reproducible;
- impacto sobre el objetivo analítico.

---

### 6.4. Licencia de reutilización

La fuente debe permitir su utilización dentro del proyecto conforme a las
condiciones publicadas por el proveedor de datos.

La fuente y URL de origen deberán quedar documentadas.

---

### 6.5. Integración con el modelo territorial maestro

El dataset debe permitir una relación directa o derivada con
`DIM_TERRITORIO`.

Cuando esto no sea posible, deberá justificarse su utilidad dentro de SIPTA
antes de incorporarlo al flujo analítico.

---

## 7. Estados de evaluación

Después de aplicar los criterios anteriores, cada dataset podrá documentarse
con uno de los siguientes estados:

### Aceptado

El dataset cumple las condiciones necesarias para el uso analítico previsto y
no presenta problemas críticos sin tratamiento.

### Aceptado con observaciones

El dataset presenta anomalías o limitaciones documentadas, pero estas no
impiden su utilización para el objetivo definido.

Las observaciones deben mantenerse visibles en las etapas posteriores.

### No aceptado para el uso previsto

El dataset presenta limitaciones críticas que impiden utilizarlo de forma
confiable para el objetivo analítico definido.

Este estado no implica que la fuente sea incorrecta en términos generales,
sino que no cumple las condiciones necesarias para el uso específico de SIPTA.

---

## 8. Regla contra correcciones arbitrarias

La matriz de calidad identifica problemas; no los corrige automáticamente.

Ante una anomalía se deberá:

1. conservar el dato original;
2. documentar el hallazgo;
3. evaluar su impacto;
4. verificar si existe una fuente oficial de contraste;
5. definir, si corresponde, una transformación reproducible;
6. conservar trazabilidad entre valor original y valor tratado.

---

## 9. Relación con el pipeline

La matriz se ubica conceptualmente antes de la integración territorial:

`Fuente → Ingesta → Validación → Matriz de calidad → Limpieza/Estandarización → Integración territorial → Indicadores → Índices`

Un dataset aceptado puede requerir transformaciones posteriores sin que esto
signifique modificar su versión original almacenada en `data/raw`.

---

## 10. Aplicación a los dominios

La matriz deberá poder aplicarse a todos los dominios incorporados al proyecto.

Cada responsable de dominio deberá aportar los resultados de validación de sus
fuentes.

Posteriormente, dichos resultados podrán consolidarse para determinar qué
datasets están en condiciones de alimentar el modelo territorial y los
indicadores.

---

## 11. Evidencia mínima por dataset

Para considerar documentada la evaluación de una fuente deberá existir, como
mínimo:

- nombre del dataset;
- dominio;
- fuente;
- fecha o período de referencia cuando exista;
- dimensiones evaluadas;
- métricas calculadas;
- anomalías detectadas;
- variables críticas;
- capacidad de territorialización;
- estado de aceptación;
- observaciones o limitaciones.

---

## 12. Estado

- Dimensiones de calidad: definidas.
- Métricas base: definidas.
- Criterios de aceptación: definidos.
- Niveles de criticidad: definidos.
- Estados de evaluación: definidos.
- Plantilla de evaluación: definida.
- Aplicación consolidada a los datasets del proyecto: pendiente.