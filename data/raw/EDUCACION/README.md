# Dominio: Educación

## Dataset principal

**Nombre:** Oferta de cupos sector oficial Bogotá D.C.  
**Fuente:** Portal de Datos Abiertos de Bogotá  
**Formato:** GeoJSON  
**Archivo:** `ofertacupos_032025.geojson`

**URL de origen:**

https://datosabiertos.bogota.gov.co/dataset/oferta-de-cupos-sector-oficial-bogota-d-c

**Recurso utilizado:**

https://datosabiertos.bogota.gov.co/dataset/de12785a-edec-4fe1-b721-da31f213fca1/resource/b167c2db-30a9-4618-908a-64482f794c4d/download/ofertacupos_032025.geojson

---

## Propósito dentro del proyecto

Este dataset se utiliza para analizar la oferta de cupos del sector oficial de Bogotá D.C. y su distribución territorial.

En esta etapa del proyecto se realizan únicamente procesos de:

- ingesta reproducible;
- inspección de estructura y esquema;
- validación de valores nulos;
- validación de duplicados;
- validación de coherencia de las variables de oferta;
- análisis de identificadores de establecimientos;
- validación de códigos de localidad;
- control de consistencia territorial entre `COD_LOCA` y la geometría publicada.

No se realizan correcciones manuales sobre el archivo original.

---

## Características técnicas

- Registros: **747**
- Variables: **14**
- Estructura: `GeoDataFrame`
- CRS original: **EPSG:3857**
- Tipo de geometría: **Point**
- Geometrías nulas: **0**
- Geometrías vacías: **0**
- Valores nulos en el dataset: **0**
- Duplicados exactos: **0**

### Variables observadas

1. `NOMBRE_EST`
2. `GENERO`
3. `COD_LOCA`
4. `CLASE_TIPO`
5. `FECHA`
6. `OPreescola`
7. `OPrimaria`
8. `OSecundari`
9. `OMedia`
10. `OTotal`
11. `Aceleracio`
12. `DANE12_EST`
13. `Educacion_`
14. `geometry`

---

## Validaciones de oferta

La variable `OTotal` fue contrastada contra la suma de:

`OPreescola + OPrimaria + OSecundari + OMedia + Aceleracio + Educacion_`

Resultados:

- Registros evaluados: **747**
- Registros coherentes: **747**
- Registros no coincidentes: **0**
- Diferencia máxima absoluta: **0**
- Valores negativos detectados en las variables de oferta: **0**

---

## Identificadores y granularidad

- Nombres de establecimientos distintos (`NOMBRE_EST`): **408**
- Identificadores `DANE12_EST` distintos: **412**
- Geometrías distintas: **741**
- DANE asociados a más de un nombre: **0**
- DANE asociados a más de una localidad: **1**

El identificador `DANE12_EST = 111001027332`, correspondiente al **COLEGIO GUSTAVO RESTREPO (IED)**, aparece asociado a más de una localidad.

La repetición de un identificador DANE o de una geometría no se considera automáticamente un duplicado, debido a que el dataset contiene registros con diferencias en las variables de oferta y ubicación.

---

## Validación territorial

El dataset contiene los **20 códigos de localidad esperados (`01` a `20`)**, sin códigos faltantes ni valores fuera del rango esperado.

Para realizar un control de calidad territorial se utilizó la capa oficial de localidades almacenada en:

`data/external/loca.json`

La capa contiene:

- **20 localidades**
- CRS: **EPSG:4686**
- **20 geometrías válidas**

Resultados del contraste entre `COD_LOCA` y la geometría:

- Registros evaluados: **747**
- Coincidencia directa entre `COD_LOCA` y localidad espacial: **743**
- Registros ubicados espacialmente en una localidad distinta a la declarada: **3**
- Registros sin asignación directa mediante `within`: **1**

### Casos territoriales documentados

**COLEGIO RURAL LAS MERCEDES (CED)**  
`COD_LOCA = 05` (Usme), mientras la geometría se ubica en la localidad 19 (Ciudad Bolívar).  
Distancia aproximada al polígono de Usme: **401,49 m**.

**COLEGIO DEBORA ARANGO PEREZ (IED)**  
`COD_LOCA = 07` (Bosa), mientras la geometría se ubica en la localidad 08 (Kennedy).  
Distancia aproximada al polígono de Bosa: **30,88 m**.

**COLEGIO INTEGRADA LA CANDELARIA (IED)**  
`COD_LOCA = 17` (La Candelaria), mientras la geometría se ubica en la localidad 03 (Santa Fe).  
Distancia aproximada al polígono de La Candelaria: **0,69 m**.

**COLEGIO CAMPESTRE JAIME GARZON (IED)**  
`COD_LOCA = 20` (Sumapaz). El punto no queda contenido directamente dentro de un polígono mediante `within`; sin embargo, la localidad espacial más cercana es Sumapaz.  
Distancia aproximada: **219,33 m**.

Estos registros se conservan sin modificaciones y quedan documentados para revisión posterior.

---

## Fuente territorial auxiliar

Para la validación espacial se utilizó la capa oficial de localidades de Bogotá:

`data/external/loca.json`

Fuente:

https://datosabiertos.bogota.gov.co/dataset/856cb657-8ca3-4ee8-857f-37211173b1f8/resource/497b8756-0927-4aee-8da9-ca4e32ca3a8a/download/loca.json

La capa se utiliza únicamente como referencia externa de control territorial.

---

## Notebooks asociados

- `notebooks/01_ingestion_educacion.ipynb`
- `notebooks/02_validation_educacion.ipynb`

El primer notebook documenta la ingesta del archivo original.

El segundo notebook documenta las validaciones estructurales, lógicas y territoriales.

---

## Salida procesada para visualización geográfica

El archivo original declara coordenadas proyectadas en **EPSG:3857**. Para que
GitHub y otras herramientas web lo representen sobre Bogotá, se genera una
copia en **EPSG:4326 (WGS84)**:

`data/processed/EDUCACION/ofertacupos_032025_wgs84.geojson`

La transformación es reproducible y no modifica el archivo ubicado en `raw`:

```bash
python scripts/prepare_education_geojson.py
```

La salida conserva los **747 registros**, las **14 variables**, los atributos
de oferta y las geometrías de tipo `Point`; únicamente cambia el sistema de
referencia de coordenadas.

---

## Estado del dominio

**Ingesta:** completada.  
**Validación estructural:** completada.  
**Validación lógica de oferta:** completada.  
**Validación territorial:** completada con cuatro casos documentados.  
**Integración:** pendiente para una fase posterior del proyecto.

> Los archivos ubicados en `data/raw/EDUCACION` deben conservarse sin modificaciones manuales.
