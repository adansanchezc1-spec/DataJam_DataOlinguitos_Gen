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


## Dominio: Finanzas / Economía (D6)

### Dataset: `vendedores_informales_consolidado.csv`
- **Fuente / Entidad:** Instituto para la Economía Social (IPES) / Registro Individual de Vendedores Informales (RIVI).
- **Ubicación:** `data/raw/FINANZAS/vendedores_informales_consolidado.csv`
- **Formato procesado:** CSV consolidado (codificación `utf-8`).
- **Registros:** 126 filas (21 categorías territoriales × 6 semestres).
- **Cobertura temporal:** Semestral (2017-06-30, 2017-12-31, 2018-06-30, 2018-12-31, 2019-06-30, 2019-12-30).
- **Llave territorial:** `codigo_localidad` (1 a 20 y 160) y `nombre_localidad`.
- **Variables principales:**
  - `codigo_localidad` (int): Código numérico oficial de la localidad.
  - `nombre_localidad` (str): Nombre oficial de la localidad.
  - `numero_vendedores` (int): Cantidad total de vendedores informales registrados en el RIVI.
  - `porcentaje` (float): Participación porcentual de la localidad sobre el total distrital.
  - `fecha_corte` (str): Fecha de corte del reporte semestral (`YYYY-MM-DD`).
  - `archivo_origen` (str): Nombre del archivo original `.txt` de procedencia.
- **⚠ Pendiente de validar con datos:** El registro con `codigo_localidad = 160` ('metropolitana o no definida') contiene vendedores informales sin localidad fija; se definirá en la fase 1.5 si se excluye o se redistribuye proporcionalmente.
  
### Dataset: `puntos_encuentro_vendedores.csv` (o `.xlsx` / `.geojson`)
- **Fuente / Entidad:** Instituto para la Economía Social (IPES).
- **Ubicación:** `data/raw/FINANZAS/Punto de encuentro vendedores. Bogotá D.C..xlsx`.
- **Formato crudo:** Excel / GeoJSON.
- **Registros:** 4 puntos de encuentro fijos para reubicación y formalización comercial.
- **Llave territorial:** `properties/CPUNLOC` (Nombre de localidad).
- **Variables principales:**
  - `properties/CPUNNOM` (str): Nombre del punto de encuentro (Alcalá, Aguas, Mundo Aventura, Tintal).
  - `properties/CPUNDIR` (str): Dirección de localización.
  - `properties/CPUNLOC` (str): Nombre de la localidad.
  - `properties/CPUNBARRIO` (str): Barrio catastral.
  - `properties/CPUNHORAPV` (str): Horario de atención al público.
  - `properties/CPUNNUMLOC` (str): Código de localidad crudo.
- **⚠ Pendiente de validar con datos:**
  - La columna `CPUNNUMLOC` presenta códigos erróneos en el archivo crudo original (ej. Alcalá en Usaquén figura con código 18 en lugar de 1); la llave oficial se derivará a partir del nombre de localidad `CPUNLOC` en la fase 1.4 de estandarización.
  - En la exportación a Excel las coordenadas geográficas perdieron el punto decimal; se recuperarán con la escala adecuada ($\div 10^{14}$).
