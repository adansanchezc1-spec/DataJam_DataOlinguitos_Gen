## Dominio: Ambiente (D5)

### Dataset: `situacion_ambiental_conflictiva.csv`
- **Fuente / Entidad:** Secretaría Distrital de Ambiente (SDA) / IDECA.
- **Ubicación:** `data/raw/AMBIENTE/situacion_ambiental_conflictiva.csv`
- **Formato crudo:** CSV (delimitador `;`, codificación `latin1`).
- **Registros:** 1.313 filas y 14 columnas.
- **Llave territorial:** `cod_locali` (1 a 20) y `localidad`.
- **Variables principales:**
  - `cod_locali` (object): Código numérico oficial de la localidad.
  - `localidad` (object): Nombre oficial de la localidad.
  - `categoria` (object): Tipología específica de la situación ambiental conflictiva.
  - `grupo_sac` (object): Macrodimensión ambiental (Estructura ecológica principal y espacios del agua, Contaminación, Fauna, Gestión de riesgos, etc.).
  - `sac` (object): Clasificación específica del conflicto reportado.
  - `codigo_sac` (object): Identificador normalizado de la SAC distrital.
  - `direccion` (object): Ubicación o nomenclatura de referencia.
  - `cord_x`, `cord_y` (object): Coordenadas proyectadas del evento.
  - `latitude`, `longitude` (object): Coordenadas geográficas WGS84.
- **⚠ Pendiente de validar con datos:**
  - Se identificaron ~30 filas con desplazamiento de columnas originadas por saltos de línea sin entrecomillar en campos de texto.
  - Las coordenadas numéricas contienen puntos usados como separadores de miles que requieren estandarización en la fase 1.4.

---

### Dataset: `estacion_calidad_aire.geojson`
- **Fuente / Entidad:** Red de Monitoreo de Calidad del Aire de Bogotá (RMCAB) / SDA.
- **Ubicación:** `data/raw/AMBIENTE/estacion_calidad_aire.geojson`
- **Formato crudo:** GeoJSON (geometrías `Point`).
- **Registros:** 19 estaciones de monitoreo.
- **Llave territorial:** `sect_loc` (código de localidad a 2 dígitos).
- **Variables principales:**
  - `cod_estac` (object): Identificador corto de la estación (ej. `KEN`, `GYR`, `USQ`).
  - `estacion` (object): Nombre oficial de la estación de monitoreo.
  - `sect_loc` (object): Código oficial de la localidad en que se ubica.
  - `activo` (object): Estado operativo de la estación (`01` = activa).
  - `lat`, `lon` (float): Coordenadas geográficas de la estación.


## Dominio: Seguridad

### Dataset: `Cuadrante de Policía. Bogotá D.C.csv`
- **Fuente / Entidad:** Policía Metropolitana de Bogotá (MEBOG) / Secretaría Distrital de Seguridad, Convivencia y Justicia.
- **Ubicación:** `data/raw/SEGURIDAD/Cuadrante de Policía. Bogotá D.C.csv`
- **Formato crudo:** CSV tabular exportado desde capa espacial (delimitador `;`, codificación `latin1`).
- **Registros:** 599 cuadrantes de vigilancia comunitaria por cuadrantes.
- **Llave territorial:** `properties/PCUIULOCAL` (código de localidad 1 a 19) y `properties/PCUIUUPLAN` (código UPZ).
- **Variables principales:**
  - `properties/PCUNCUADRA` (object): Identificador único del cuadrante policial (ej. `MEBOGMNVCCC02E19C08000033`).
  - `properties/PCUNOMEST` (object): Nombre de la estación de policía / localidad asociada (ej. `CIUDAD BOLIVAR`, `KENNEDY`).
  - `properties/PCUNOMCAI` (object): CAI al que está adscrito el cuadrante.
  - `properties/PCUDESCRIP` (object): Descripción del cuadrante (ej. `Cuadrante 033`).
  - `properties/PCUIULOCAL` (object): Código oficial de la localidad.
  - `properties/PCUIUUPLAN` (object): Código oficial de la UPZ.
  - `properties/PCUTELEFON` (object): Teléfono de contacto del cuadrante.
- **⚠ Pendiente de validar con datos:**
  - La localidad 20 (Sumapaz) no cuenta con cuadrantes de patrullaje urbano bajo esta estructura; se documentará su particularidad operativa en `docs/manual_tecnico.md`.
