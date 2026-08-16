# SIPTA — Principios de datos y modelo territorial

## 1. Propósito

Este documento establece los principios que orientan la organización,
territorialización, transformación e integración de las fuentes de datos del
proyecto SIPTA.

Estos principios deben aplicarse antes de construir indicadores, índices y
mecanismos de priorización territorial.

---

## 2. Principios fundamentales

### 2.1. Un territorio, una verdad

Toda fuente utilizada por SIPTA debe poder asociarse a una referencia
territorial común.

Para el MVP del proyecto, la unidad territorial primaria es la
**localidad de Bogotá D.C.**

La territorialización podrá realizarse mediante:

- código de localidad;
- nombre oficial de localidad;
- otra unidad territorial homologable;
- coordenadas geográficas;
- relaciones espaciales con polígonos oficiales.

La existencia de diferentes nombres, códigos o granularidades en las fuentes
no debe generar múltiples definiciones del mismo territorio.

`DIM_TERRITORIO` constituye la referencia maestra para resolver estas
diferencias.

---

### 2.2. Granularidad territorial común

El modelo analítico principal utilizará:

> **1 registro territorial = 1 localidad de Bogotá D.C.**

Se esperan **20 localidades**.

Las fuentes con información a una granularidad más detallada deberán agregarse
u homologarse al nivel de localidad cuando sea necesario para su integración.

UPZ y barrio pueden conservarse como atributos auxiliares cuando una fuente los
contenga, pero no reemplazan la localidad como unidad primaria del MVP.

---

### 2.3. Normalización para comparabilidad

Los valores absolutos no siempre permiten comparar correctamente territorios
con tamaños o poblaciones diferentes.

Cuando corresponda, los indicadores deberán normalizarse utilizando
denominadores como:

- población;
- área territorial;
- capacidad instalada;
- demanda;
- población objetivo;
- otra magnitud técnicamente justificada.

Toda normalización deberá documentar:

- numerador;
- denominador;
- unidad;
- período de referencia;
- fuente;
- interpretación.

---

### 2.4. Trazabilidad

Toda variable utilizada por el modelo deberá poder rastrearse hasta su fuente
original.

El flujo esperado es:

`Fuente → archivo raw → validación → transformación → variable → indicador → índice → priorización`

No deben introducirse valores, correcciones o transformaciones sin dejar
registro de su origen y justificación.

---

### 2.5. Preservación del dato original

Los archivos almacenados en `data/raw` representan los datos originales
obtenidos de las fuentes oficiales.

Estos archivos no deben modificarse manualmente.

Las operaciones de limpieza, homologación, normalización, agregación,
territorialización e integración deberán producir nuevos artefactos en las
etapas correspondientes.

---

### 2.6. Reproducibilidad

Cualquier integrante del equipo debe poder reconstruir los resultados a partir
de:

- las fuentes documentadas;
- los archivos disponibles en el repositorio;
- los notebooks o scripts;
- las reglas metodológicas;
- las versiones correspondientes.

Las transformaciones críticas no deben depender exclusivamente de operaciones
manuales.

---

### 2.7. Calidad antes de integración

Una fuente no debe incorporarse directamente al modelo territorial sin evaluar
previamente su calidad.

Como mínimo deben revisarse, cuando apliquen:

- estructura;
- completitud;
- validez;
- consistencia;
- unicidad;
- actualidad;
- coherencia territorial.

Las anomalías detectadas deben documentarse antes de decidir si requieren
corrección, exclusión o conservación.

---

## 3. Modelo territorial maestro

El modelo territorial maestro tiene como objetivo proporcionar una referencia
común para integrar los distintos dominios del proyecto.

Flujo conceptual:

`Dominios → validación → estandarización → DIM_TERRITORIO → indicadores → índices → priorización`

Los dominios sectoriales no deberán definir de manera independiente sus propias
versiones de una localidad.

Todos deberán asociarse, directa o indirectamente, con la referencia contenida
en `DIM_TERRITORIO`.

---

## 4. Reglas para territorialización

### Fuente con código de localidad

Se homologará el código publicado con la clave territorial maestra.

### Fuente con nombre de localidad

El nombre deberá normalizarse y contrastarse con el nombre oficial.

### Fuente con coordenadas

La localidad podrá determinarse mediante relación espacial contra los
polígonos oficiales.

### Fuente con UPZ o barrio

La unidad deberá homologarse a su localidad correspondiente antes de utilizarse
en análisis comparativos a nivel distrital.

### Conflicto entre atributo y geometría

Cuando el código o nombre territorial declarado no coincida con la geometría:

1. no se modificará automáticamente el dato original;
2. se documentará la discrepancia;
3. se conservarán los valores de origen;
4. cualquier corrección deberá tener una regla reproducible y una fuente de
   referencia explícita.

---

## 5. Sistemas de referencia espacial

Cada fuente conservará documentado su CRS original.

Para operaciones espaciales las capas deberán transformarse explícitamente a un
CRS compatible.

Las operaciones de distancia y área deberán realizarse sobre un CRS proyectado
adecuado para Bogotá.

Las coordenadas destinadas a intercambio o visualización podrán expresarse en
latitud y longitud, dejando documentado el CRS utilizado.

No deberán calcularse distancias o superficies directamente sobre un CRS
geográfico sin una transformación apropiada.

---

## 6. Separación de responsabilidades

El entendimiento y validación de cada dominio puede realizarse de manera
independiente.

La integración territorial ocurre posteriormente utilizando una referencia
maestra común.

Por esta razón:

- validar un dominio no equivale a integrarlo;
- territorializar una fuente para comprobar su calidad no equivale todavía a
  construir el modelo integrado;
- `DIM_TERRITORIO` debe existir antes de consolidar los dominios en una tabla
  analítica conjunta.

---

## 7. Resultado esperado

El modelo territorial deberá permitir que información procedente de distintos
dominios termine asociada a una misma clave territorial.

Ejemplo conceptual:

`Educación → COD_LOCA → DIM_TERRITORIO`

`Demografía → código de localidad → DIM_TERRITORIO`

`Salud → coordenadas → localidad → DIM_TERRITORIO`

Esto permitirá posteriormente construir indicadores comparables e integrar
variables sectoriales sin perder trazabilidad.

---

## 8. Estado

- Unidad territorial primaria: **Localidad**.
- Número esperado de unidades: **20**.
- Principios de trazabilidad: definidos.
- Principios de reproducibilidad: definidos.
- Regla de preservación de datos raw: definida.
- Reglas generales de territorialización: definidas.
- `DIM_TERRITORIO`: pendiente de especificación e implementación.