# SIPTA — Definición de DIM_TERRITORIO

## 1. Propósito

`DIM_TERRITORIO` es la dimensión territorial maestra del proyecto SIPTA.

Su función es proporcionar una referencia única, estable y reproducible para
relacionar los diferentes dominios de datos con las localidades de Bogotá D.C.

---

## 2. Granularidad

La granularidad de la tabla es:

> **1 fila = 1 localidad de Bogotá D.C.**

Número esperado de registros:

**20 localidades.**

No deben existir dos filas diferentes para una misma localidad.

---

## 3. Clave primaria

La clave primaria será:

`id_localidad`

Debe identificar de manera única cada una de las 20 localidades.

Formato propuesto:

`01` a `20`

El identificador se almacenará como texto de dos caracteres para preservar los
ceros a la izquierda y facilitar la homologación con fuentes sectoriales.

Ejemplos:

`01` → Usaquén  
`08` → Kennedy  
`20` → Sumapaz

---

## 4. Esquema

| Campo | Tipo lógico | Requerido | Descripción |
|---|---|---|---|
| `id_localidad` | Texto | Sí | Identificador territorial único normalizado (`01`–`20`) |
| `nombre_localidad` | Texto | Sí | Nombre oficial de la localidad |
| `codigo_dane` | Texto | Sí* | Código territorial DANE cuando exista una fuente oficial verificable |
| `upz` | Texto | Deseable | Información auxiliar de UPZ cuando aplique |
| `barrio` | Texto | Opcional | Información auxiliar de barrio cuando aplique |
| `latitud` | Decimal | Deseable | Coordenada representativa de la localidad |
| `longitud` | Decimal | Deseable | Coordenada representativa de la localidad |
| `area_km2` | Decimal | Sí | Superficie territorial expresada en km² |
| `poblacion` | Entero | Sí | Población utilizada como referencia analítica |
| `fecha_actualizacion` | Fecha | Sí | Fecha o período de corte de los atributos variables |

\* La columna `codigo_dane` forma parte obligatoria del esquema. Su valor no
debe inventarse ni sustituirse automáticamente por otro código territorial. Si
no existe una correspondencia DANE oficialmente verificada, deberá conservarse
como dato pendiente o nulo hasta disponer de una fuente válida.

---

## 5. Fuentes previstas

### Geometría y nombres territoriales

Fuente oficial de localidades de Bogotá.

Variables esperadas de origen:

- código territorial;
- nombre oficial;
- geometría.

Esta fuente será utilizada como referencia espacial primaria.

### Población

La población deberá obtenerse de una fuente demográfica oficial previamente
validada.

El valor utilizado deberá corresponder a un año o período de referencia
explícitamente documentado.

No se mezclarán poblaciones de diferentes períodos dentro de una misma versión
de `DIM_TERRITORIO`.

---

## 6. Reglas de construcción

### Identificador territorial

`id_localidad` deberá normalizarse a dos caracteres.

Ejemplo:

`1` → `01`

`8` → `08`

`20` → `20`

---

### Nombre oficial

`nombre_localidad` deberá conservar el nombre oficial proveniente de la fuente
territorial maestra.

No deberá depender de variantes ortográficas presentes en datasets sectoriales.

---

### Código DANE

No se asumirá que cualquier código territorial presente en la capa geográfica
equivale automáticamente a un código DANE.

La relación deberá verificarse con una fuente oficial antes de asignarse.

---

### Población

La población será agregada por localidad y deberá corresponder a un período
claramente identificado.

Cuando la fuente demográfica contenga desagregaciones por sexo, edad u otra
característica, estas deberán sumarse evitando doble conteo.

---

### Área

`area_km2` deberá calcularse a partir del polígono oficial utilizando un CRS
proyectado adecuado para mediciones métricas.

Conversión:

`area_km2 = area_m2 / 1_000_000`

El CRS y el procedimiento utilizado deberán quedar registrados en el código de
implementación.

---

### Latitud y longitud

Las coordenadas representan un punto de referencia de la localidad y no su
extensión territorial completa.

Se recomienda utilizar un punto representativo generado a partir del polígono
oficial.

Las coordenadas para intercambio se expresarán en un CRS geográfico
documentado.

No deben confundirse estas coordenadas con la geometría completa de la
localidad.

---

### UPZ y barrio

Debido a que la granularidad primaria es localidad, `upz` y `barrio` no
constituyen claves de esta dimensión.

En la primera versión podrán permanecer sin valor cuando no exista una relación
única:

- una localidad puede contener múltiples UPZ;
- una localidad puede contener múltiples barrios.

No deben almacenarse listas de UPZ o barrios dentro de una celda únicamente
para completar estos campos.

---

## 7. Reglas de calidad

`DIM_TERRITORIO` deberá cumplir como mínimo:

| Regla | Criterio esperado |
|---|---|
| Número de registros | 20 |
| `id_localidad` únicos | 20 |
| `nombre_localidad` únicos | 20 |
| IDs esperados | `01` a `20` |
| IDs nulos | 0 |
| Nombres nulos | 0 |
| Áreas positivas | 20/20 |
| Poblaciones no negativas | 20/20 |
| Geometrías territoriales válidas | 20/20 |
| Duplicados exactos | 0 |

Las reglas relacionadas con campos opcionales dependerán de la disponibilidad
real de las fuentes.

---

## 8. Relación con los dominios

Los datasets sectoriales deberán relacionarse con `DIM_TERRITORIO` mediante una
clave territorial homologada.

Ejemplos:

### Demografía

`CODIGO_LOCALIDAD → id_localidad`

### Educación

`COD_LOCA → id_localidad`

### Salud

`Latitud + Longitud → spatial join → id_localidad`

Las equivalencias de los demás dominios deberán incorporarse cuando sus
respectivas fuentes hayan sido validadas.

---

## 9. Outputs previstos

La implementación podrá generar como mínimo:

`data/processed/dim_territorio.csv`

para análisis tabular.

Cuando se requiera conservar la geometría completa podrá generarse además un
formato geoespacial, por ejemplo:

`data/processed/dim_territorio.geojson`

La generación de ambos artefactos deberá realizarse mediante código
reproducible y no mediante edición manual.

---

## 10. Dependencias para implementación

Para materializar `DIM_TERRITORIO` se requieren como mínimo:

1. capa oficial validada de las 20 localidades;
2. fuente demográfica validada;
3. período de población seleccionado;
4. regla oficial o fuente verificable para `codigo_dane`;
5. procedimiento reproducible para área y coordenadas.

Hasta disponer de esas dependencias en la rama base del proyecto, este
documento constituye la especificación de la dimensión.

---

## 11. Estado

**Diseño conceptual:** completado.  
**Granularidad:** definida.  
**Clave primaria:** definida.  
**Esquema:** definido.  
**Reglas de calidad:** definidas.  
**Fuentes previstas:** definidas.  
**Implementación física:** pendiente.