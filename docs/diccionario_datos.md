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
