# E01 - Inventario de Datos Analizados 

**Responsable**: Yesid Bello  
**Fase CRISP-DM**: Data Understanding  
**Proyecto**: SIPTA — DataJam Bogotá  

## Resumen Ejecutivo
El presente documento consolida el inventario preliminar de fuentes de datos abiertas para los dominios de Demografía, Salud y Educación. Siguiendo los lineamientos del Plan Maestro, la existencia del identificador territorial primario ("Localidad") se marca como pendiente de validación técnica hasta confirmar los esquemas de datos crudos en la fase de Ingestión[cite: 2, 6].

---

## 1. Dominio: Demografía
**Objetivo Analítico:** Identificar población, edad, género, área y densidad poblacional para normalización de indicadores[cite: 4].

| Dataset / Categoría | URL de Origen | Entidad | Formato | ¿Tiene identificador de Localidad? |
| :--- | :--- | :--- | :--- | :--- |
| **Pirámide Poblacional (1)** | `https://datosabiertos.bogota.gov.co/dataset/piramide-poblacional-bogota-d-c/resource/37e58cb3-c870-4608-8c37-ce45db0eb7c1` | SDP | CSV | ⚠ Pendiente de validar con datos[cite: 2, 6] |
| **Pirámide Poblacional (2)** | `https://datosabiertos.bogota.gov.co/dataset/piramide-poblacional-bogota-d-c/resource/d1743cda-9ff9-4103-87ab-9c038f2f09a3` | SDP | CSV | ⚠ Pendiente de validar con datos[cite: 2, 6] |
| **Límite de Localidad** | `https://www.ideca.gov.co/buscador?search=Pol%C3%ADgonos+de+Localidades` | IDECA / SDP | GeoJSON / SHP | ⚠ Pendiente de validar con datos[cite: 2, 6] |

---

## 2. Dominio: Salud
**Objetivo Analítico:** Medir capacidad instalada, oferta de servicios y cobertura. Indicador clave: Camas por 10.000 hab (SAL-002)[cite: 4, 6].

| Dataset / Categoría | URL de Origen | Entidad | Formato | ¿Tiene identificador de Localidad? |
| :--- | :--- | :--- | :--- | :--- |
| **Tipo y razón de camas** | `https://saludata.saludcapital.gov.co/osb/indicadores/tipo-y-razon-de-camas-en-bogota-d-c/` | SDS (SaluData) | CSV / Tabla | Tipo y razón de camas en Bogotá D.C.
Estado territorial: NO APTO para integración directa por localidad.|
Uso posible: contexto distrital / referencia general de oferta sanitaria.
| **Camas UCI y General** | `https://saludata.saludcapital.gov.co/osb/indicadores/camasuci/` <br> `https://saludata.saludcapital.gov.co/osb/indicadores/uci-general/` | SDS (SaluData) | CSV / Tabla | ⚠ Pendiente de validar con datos[cite: 2, 6] |
| **Instituciones con urgencias** | `https://saludata.saludcapital.gov.co/osb/indicadores/instituciones-de-salud-con-servicios-de-urgencias-en-bogota-d-c/` | SDS (SaluData) | CSV / Tabla | ⚠ Pendiente de validar con datos[cite: 2, 6] |
| **Tipos de prestadores** | `https://saludata.saludcapital.gov.co/osb/indicadores/tipo-de-prestadores-de-servicios-de-salud-en-bogota-d-c/` | SDS (SaluData) | CSV / Tabla | ⚠ Pendiente de validar con datos[cite: 2, 6] |
| **Ocupación y monitoreo** | `https://saludata.saludcapital.gov.co/osb/indicadores/porcentaje-de-ocupacion-de-los-servicios-de-urgencias...` <br> `https://saludata.saludcapital.gov.co/osb/indicadores/monitoreo-indicadores-del-sistema-de-salud/`| SDS (SaluData) | CSV / Tabla | ⚠ Pendiente de validar con datos[cite: 2, 6] |

---

## 3. Dominio: Educación
**Objetivo Analítico:** Mapear colegios, cupos, deserción e inversión. Indicador clave: Cupos escolares por 1.000 niños (EDU-001) y Deserción[cite: 4, 6].

| Dataset / Categoría | URL de Origen | Entidad | Formato | ¿Tiene identificador de Localidad? |
| :--- | :--- | :--- | :--- | :--- |
| **Directorio de Colegios** | `https://datosabiertos.bogota.gov.co/dataset/colegios-bogota-d-c` | SED | CSV / SHP | ⚠ Pendiente de validar con datos[cite: 2, 6] |
| **Oferta y Demanda de Cupos** | `https://datosabiertos.bogota.gov.co/dataset/oferta-de-cupos-sector-oficial-bogota-d-c` <br> `https://datosabiertos.bogota.gov.co/dataset/demanda-de-cupos-sector-oficial-bogota-d-c` | SED | CSV | ⚠ Pendiente de validar con datos[cite: 2, 6] |
| **Matrícula y Cobertura Bruta** | `https://datosabiertos.bogota.gov.co/dataset/matricula-total-en-colegios-oficiales-bogota-d-c` <br> `https://datosabiertos.bogota.gov.co/dataset/tasa-cobertura-bruta-bogota-d-c` | SED | CSV | ⚠ Pendiente de validar con datos[cite: 2, 6] |
| **Tasas de Deserción y Alertas** | `https://datosabiertos.bogota.gov.co/dataset/tasa-de-desercion-escolar-en-colegios-oficiales-por-localidad-bogota-d-c` <br> `https://datosabiertos.bogota.gov.co/dataset/tasa-del-sistema-de-alertas-por-localidad-bogota-d-c` | SED | CSV | ⚠ Pendiente de validar con datos[cite: 2, 6] |
| **Inversión Educativa (Sectorial)** | `https://datosabiertos.bogota.gov.co/dataset/territorializacion-de-la-inversion-en-el-sector-educativo-por-localidad-bogota-d-c` | SED | CSV | ⚠ Pendiente de validar con datos[cite: 2, 6] |