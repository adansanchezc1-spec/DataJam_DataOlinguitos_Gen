# SIPTA — Dominio Salud

## 1. Fuente de datos

**Dataset:** Instituciones de Salud con servicios de urgencias en Bogotá D.C.  
**Entidad:** Secretaría Distrital de Salud — Bogotá D.C.  
**Fuente:** Portal de Datos Abiertos de Bogotá  
**Archivo utilizado:** `osb_ofertasrv-ips-urgencias.csv`  
**Ubicación local:** `data/raw/SALUD/osb_ofertasrv-ips-urgencias.csv`

Fuente oficial:

https://datosabiertos.bogota.gov.co/dataset/instituciones-de-salud-con-servicios-de-urgencias-en-bogota-d-c

---

## 2. Propósito dentro de SIPTA

Este dataset permite identificar las sedes de Instituciones Prestadoras de Servicios de Salud (IPS) que ofrecen servicios de urgencias en Bogotá D.C.

Su utilidad dentro del proyecto consiste en disponer de información sobre la localización de la oferta de servicios de urgencias y preparar posteriormente su asociación con la unidad territorial primaria definida por SIPTA: `Localidad`.

---

## 3. Características del archivo

- Formato: CSV.
- Codificación utilizada para lectura: `cp1252`.
- Registros: **84**.
- Variables: **11**.
- IPS diferentes: **44**.
- Sedes identificadas: **84**.
- Granularidad observada: una fila representa una sede de una IPS con servicio de urgencias.

La combinación:

`Código IPS + Número sede`

identifica de forma única los 84 registros.

---

## 4. Variables principales

Entre las variables disponibles se encuentran:

- `OBJECTID`
- `Código IPS`
- `Nombre IPS`
- `Nombre sede`
- `Número sede`
- `Dirección`
- `Telefono contacto`
- `Correo electrónico`
- `Tipo de naturaleza`
- `Latitud`
- `Longitud`

El dataset no contiene una variable `Localidad` de forma explícita.

---

## 5. Resultados de validación

La validación reproducible se encuentra en:

`notebooks/02_validation_salud.ipynb`

Principales resultados:

- Duplicados exactos: **0**.
- Duplicados según `Código IPS + Número sede`: **0**.
- Valores nulos:
  - `Telefono contacto`: **1 registro (1,19 %)**.
  - Variables restantes: **0**.
- Valores nulos en `Latitud`: **0**.
- Valores nulos en `Longitud`: **0**.
- Coordenadas no convertibles a formato numérico: **0**.
- Pares de coordenadas distintos: **84**.
- Pares de coordenadas repetidos: **0**.
- Coordenadas fuera de los rangos geográficos universales válidos: **0**.

Rangos observados:

- Latitud aproximada: **4.029 a 4.761**.
- Longitud aproximada: **-74.315 a -74.023**.

---

## 6. Consideraciones territoriales

El dataset no dispone directamente de la variable `Localidad`.

Sin embargo, sus 84 registros contienen coordenadas completas y convertibles, por lo que el dataset se considera técnicamente apto para una futura asociación territorial con las localidades de Bogotá.

La asignación efectiva de cada sede a una localidad no se realiza durante esta etapa de validación. Esta operación corresponde a una fase posterior de integración territorial.

---

## 7. Estado

**Estado de validación: APTO PARA CONTINUAR EL PIPELINE.**

El único valor nulo identificado corresponde a `Telefono contacto` y no afecta la identificación de las sedes ni la futura territorialización.

El archivo almacenado en `data/raw/SALUD` debe conservarse sin modificaciones manuales.

---

## 8. Notebooks asociados

- Ingesta: `notebooks/01_ingestion_salud.ipynb`
- Validación: `notebooks/02_validation_salud.ipynb`

Las etapas de limpieza, estandarización, integración territorial y cálculo de indicadores se realizarán posteriormente.
