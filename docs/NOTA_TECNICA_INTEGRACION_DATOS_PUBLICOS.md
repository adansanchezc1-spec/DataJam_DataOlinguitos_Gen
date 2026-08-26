# NOTA TÉCNICA: EXPERIENCIA DE INTEGRACIÓN E INTEROPERABILIDAD DE DATOS PÚBLICOS
**Proyecto**: SIPTA — Sistema de Indicadores y Priorización Territorial y Alertas Tempranas  
**Equipo**: Data Olinguitos — Bogotá DataJam (Edición 2) – 2026
**Marco Metodológico**: DAMA-BOK / ISO/IEC 25010 / Pipeline Modular SIPTA

---

### 1. Síntesis de Fuentes y Flujo de Integración
El proyecto procesó **25 conjuntos de datos oficiales** (121 archivos físicos) a través de un pipeline automatizado y reproducible estructurado en 4 etapas:
$$\text{data/raw} \xrightarrow{\text{Ingesta}} \text{Validación QA (ISO 25010)} \xrightarrow{\text{src/cleaning}} \text{data/processed} \xrightarrow{\text{src/integration}} \text{Tablón Maestro} \xrightarrow{\text{src/modeling}} \text{Motor IPT}$$

| Dominio / Dimensión | Entidades Fuente | Formatos | Granularidad Original | Estrategia de Homologación |
|---|---|:---:|---|---|
| **Demografía (Denominador)** | SDP / SaluData | CSV | Localidad / UPL (2005–2035) | Denominador per cápita universal |
| **Salud, Educación, Movilidad** | SDS, SED, TransMilenio | GPKG, GeoJSON, CSV | Coordenadas puntuales | *Spatial Join* WGS84 (`EPSG:4326`) |
| **Espacio Público y Ambiente** | IDRD, SDA (SAC/RMCAB) | CSV, GeoJSON | Puntos e inventarios | Agregación vectorial a 20 localidades |
| **Finanzas, Seguridad, Empleo** | Sec. Gobierno, MEBOG, DANE | CSV, XLSX, TXT | Tabular por entidad | Mapeo canónico (`codigo_localidad`) |

---

### 2. Disponibilidad y Complejidad Técnica Enfrentada
* **Heterogeneidad de formatos**: Tratamiento de datos espaciales vectoriales, microdatos tabulares y feeds GTFS comprimidos en `.zip`.
* **Discrepancias en nomenclatura territorial**: Concurrencia de códigos DANE de 5 dígitos, números 1–20 y nombres con variaciones ortográficas. Se resolvió implementando un diccionario canónico (`MAPA_HOMOLOGACION_LOCALIDADES`) para asegurar la cobertura del 100% distrital.
* **Ventanas temporales**: Coexistencia de coberturas en tiempo real/vigentes (Movilidad, Cartografía IDECA v3.26) con registros censales periódicos (RIVI IPES 2017–2019) y reportes fiscales anuales (FDL).
* **Tratamiento de nulos y atipicidades**: Imputación residual controlada por mediana en localidades rurales (Sumapaz en cuadrantes urbanos) para mantener la completitud de la matriz final sin sesgar el ranking del IPT.

---

### 3. Observaciones sobre Interoperabilidad Distrital
1. **Estructuras tabulares administrativas**: Reportes oficiales en Excel con celdas combinadas y encabezados múltiples que rompen la ingesta automatizada por código y exigen parsers dedicados.
2. **Ausencia de identificadores foráneos estándar**: Falta de obligatoriedad en el uso de identificadores espaciales canónicos IDECA (`COD_LOC` y `COD_UPL`) en tablas sectoriales no geográficas.

---

### 4. Recomendaciones para el Ecosistema de Datos Abiertos
* **Estandarización vinculante de llaves territoriales**: Exigir los campos `codigo_localidad` (1–20) y `codigo_upl` en todo dataset publicado con nivel de agregación espacial.
* **Publicación en formatos planos vía API**: Exponer endpoints directos (CKAN/Socrata) en `.csv`, `.json` o `.parquet` limpios de formato tipográfico.
* **Desagregación georreferenciada del gasto público**: Publicar la ejecución presupuestal de los Fondos de Desarrollo Local a nivel de proyecto específico y coordenada geográfica para evaluar el retorno social barrial.