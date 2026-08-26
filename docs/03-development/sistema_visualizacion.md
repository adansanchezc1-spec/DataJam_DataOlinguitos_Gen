# Sistema de Visualización Geoespacial y Dashboard Web GIS — SIPTA (v1.0.0)

**Fase PDCO**: DEVELOPMENT → OPERATIONS  
**Estándares**: Clean Code, PEP 8, ISO/IEC 25010, DAMA-BOK, RFC 7946 (GeoJSON), OGC WGS84  
**Autores**: Adan Sánchez (Persona A), Yesid Bello (Persona B), Sofía Hidalgo (Persona C) — Equipo DataJam  

---

## 1. Propósito y Visión General

El **Sistema de Visualización de SIPTA** es el componente encargado de transformar los datos analíticos multivariados, los indicadores sectoriales y el **Índice de Priorización Territorial (IPT)** en una experiencia interactiva, cartográfica y pedagógica.

### ¿Qué problema resuelve?
Permite a cualquier analista, tomador de decisiones distrital o ciudadano explorar visualmente la situación multidimensional de las **20 localidades de Bogotá D.C.** sin requerir la instalación de software SIG comercial pesado (como ArcGIS) ni depender de servidores backend o bases de datos activas en la nube.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                  ARQUITECTURA DEL SISTEMA DE VISUALIZACIÓN                 │
├────────────────────────────────┬───────────────────────────────────────────┤
│    FUENTES ESPACIALES & TABLAS  │  • Polígonos de 20 Localidades (GeoJSON)  │
│    EN data/processed & curated │  • Capas de Puntos Overlays (Estaciones)  │
│                                │  • Tablón Maestro Territorial (13 dominios)│
├────────────────────────────────┼───────────────────────────────────────────┤
│    MOTOR PYTHON (src/)         │  • Cruce geoespacial determinista         │
│    geo_dashboard.py            │  • Algoritmo Fisher-Jenks & Cuantiles     │
│                                │  • Intervalos Bootstrap & Serialización   │
├────────────────────────────────┼───────────────────────────────────────────┤
│    SALIDA AUTÓNOMA             │  • reports/dashboard_geografico_sipta.html│
│    (Leaflet.js + Chart.js)     │  • data/curated/sipta_localidades...geojson│
└────────────────────────────────┴───────────────────────────────────────────┘
```

---

## 2. Ingesta y Procesamiento de Datos Geoespaciales (GeoJSON)

### A. Capa Poligonal Base de Localidades
- **Archivo de Origen**: `data/processed/MODELO_TERRITORIAL/poligonos_localidades.geojson` (o `data/raw/MODELO_TERRITORIAL/poligonos_localidades.geojson`).
- **Sistema de Referencia Espacial**: Coordenadas geográficas estándar **WGS84 (EPSG:4326)** con geometrías tipo `Polygon` y `MultiPolygon`.
- **Identificador Canónico**: Código DIVIPOLA SDP (`identificador_localidad` del 1 al 20) y nombre oficial (`nombre_localidad`).

### B. Cruce Geoespacial y Tabular Multidominio
La función `build_multidomain_geodataframe()` en `src/visualization/geo_dashboard.py` realiza la integración:
1. Lee los polígonos de las 20 localidades mediante `geopandas.read_file()`.
2. Lee el tablón maestro curado `data/curated/master_indicadores_territoriales.csv` (o genera la agregación de los 13 dominios si no existe).
3. Realiza un *join* determinista usando el código numérico de localidad:
   $$\text{GeoDataFrame} = \text{Polígonos} \bowtie_{\text{codigo\_localidad}} \text{Tablas Sectoriales}$$
4. Limpia geometrías, simplifica atributos nulos y calcula columnas auxiliares para semaforización.

### C. Capas Vectoriales Puntuales (Overlays)
La función `load_point_overlay_layers()` carga 5 capas temáticas de puntos georreferenciados para enriquecer el análisis contextual:
- 🚌 **Estaciones Troncales TransMilenio**: `data/processed/MOVILIDAD/estaciones_troncales.geojson`.
- 🚇 **Estaciones Metro Línea 1**: `data/processed/MOVILIDAD/estaciones_linea1.geojson`.
- 🍃 **Estaciones de Monitoreo de Calidad del Aire**: `data/processed/AMBIENTE/estacion_calidad_aire.geojson`.
- 🍎 **Puntos de Encuentro de Vendedores Informales (IPES)**: `data/processed/EMPLEO_ECONOMIA/Punto de encuentro vendedores. Bogotá D.C..geojson`.
- 🏫 **Oferta de Cupos Escolares Oficiales**: `data/processed/EDUCACION/ofertacupos_032025_wgs84.geojson`.

### D. Exportación de Capa GeoJSON Curada
La función `export_curated_multidomain_geojson()` serializa el GeoDataFrame completo bajo el estándar internacional **RFC 7946 GeoJSON** en:
- `data/curated/sipta_localidades_multidominio.geojson`

Este archivo contiene la geometría vectorial exacta de cada localidad junto con todos los indicadores de los 13 sectores y los puntajes del IPT en las propiedades de cada feature, lo que permite abrirlo directamente en QGIS, ArcGIS, Mapbox, Kepler.gl o Python.

---

## 3. Motor Estadístico Cartográfico: Clasificación no Arbitraria

Para evitar el sesgo visual y la manipulación cartográfica común en mapas temáticos de coropletas, el módulo `geo_dashboard.py` implementa el algoritmo de **Fisher-Jenks Natural Breaks** y la partición por **Cuantiles** en Python puro:

```python
def calculate_classification_breaks(series: pd.Series, method: str = "jenks", k: int = 5) -> list[float]:
    """Calcula los límites de clase para coropletas minimizando la varianza interna."""
```

### 1. Algoritmo Fisher-Jenks (Natural Breaks)
Busca particiones en los datos que minimicen la varianza al interior de cada clase (*Goodness of Absolute Deviation Fit*) y maximicen la varianza entre diferentes clases:
$$\min \sum_{j=1}^k \sum_{i \in C_j} (x_i - \bar{x}_j)^2$$

### 2. Cuantiles (Quantiles)
Divide las 20 localidades en 5 grupos con igual número de observaciones (4 localidades por quintil), ideal para variables con asimetría pronunciada o datos ordinales.

---

## 4. Generación de la Aplicación Web GIS (`reports/dashboard_geografico_sipta.html`)

La función `generate_interactive_gis_dashboard()` compila la aplicación web completa en un único archivo HTML estático e independiente.

### ¿Cómo funciona la compilación en Python?
1. **Extracción y Cálculo**: Se calcula la matriz de rupturas estadísticas (`breaks_dict`) para cada uno de los más de 30 indicadores disponibles en los 13 dominios.
2. **Serialización JSON**: Se convierten a cadenas JSON los siguientes objetos:
   - `geojson_dict`: Las geometrías y propiedades de las 20 localidades.
   - `catalog_json`: El catálogo de dominios, metadatos, unidades y polaridades (`DOMAIN_CATALOG`).
   - `breaks_json`: Las rupturas estadísticas precalculadas (Jenks y Cuantiles) por variable.
   - `overlays_json`: Las capas de puntos geográficos complementarias.
3. **Inyección en Plantilla HTML/JS**: Los objetos JSON se incrustan como variables JavaScript globales dentro del bloque `<script>` de una plantilla HTML moderna y reactiva.
4. **Escritura en Disco**: Se guarda el archivo en `reports/dashboard_geografico_sipta.html`.

### Tecnologías Frontend Utilizadas en el Cliente:
- 🗺️ **Leaflet.js (v1.9.4)**: Renderizado de mapas interactivos, capas vectoriales SVG, eventos de ratón (`hover`, `click`, `zoom`) y tooltips contextuales.
- 📊 **Chart.js**: Renderizado dinámico en tiempo real de gráficos de barras de distribución territorial y gráficos de radar comparativo (localidad seleccionada vs. promedio distrital).
- 🎨 **Tailwind CSS & Plus Jakarta Sans / JetBrains Mono**: Interfaz estética tipo *Dark Mode Glassmorphism* con tipografía moderna y paleta de colores armónica.
- ⚡ **Lucide Icons**: Iconografía SVG vectorial ligera para dominios y herramientas.

---

## 5. Funcionalidades del Dashboard para el Usuario

1. **Selector Dinámico de Dominios (13 Sectores)**:
   - IPT Multidimensional (Base, Geométrico, Ranking, Incertidumbre Bootstrap).
   - Demografía y Espacio.
   - Salud y Capacidad Asistencial.
   - Educación y Logro Escolar.
   - Movilidad y Accesibilidad.
   - Infraestructura Urbana.
   - Ambiente y Sostenibilidad.
   - Finanzas y Capacidad Fiscal.
   - Vulnerabilidad Social.
   - Seguridad y Convivencia.
   - Servicios Públicos y Hábitat.
   - Mercado Laboral y Conmutación.
   - Participación Ciudadana y PQR.

2. **Selector de Indicadores Específicos**: Al cambiar de dominio, el selector de indicadores se actualiza dinámicamente mostrando unidades de medida (p. ej. `hab/km²`, `sedes/10k hab`, `pts`, `t/ha`).

3. **Selector de Método Cartográfico**: Permite alternar al instante entre **Fisher-Jenks Natural Breaks** y **Cuantiles (Quintiles)**, recalculando la leyenda y los colores de las 20 localidades.

4. **Inspector Analítico Lateral**:
   - Al hacer clic en cualquier localidad en el mapa, el panel derecho muestra:
     - Nombre y código DIVIPOLA de la localidad.
     - Valor del indicador seleccionado con su semáforo de riesgo (Verde / Ámbar / Rojo).
     - **Intervalo de Confianza Bootstrap al 95%** ($\text{IC}_{95\%}$ derivado de remuestreo Dirichlet).
     - Puesto en el Ranking Distrital.
     - Radar dimensional comparando la localidad contra el promedio distrital.

5. **Activación de Capas Puntuales (Overlays)**: Casillas de verificación para superponer estaciones de TransMilenio, Metro, sensores ambientales, puntos de venta o cupos educativos.

6. **Exportación GeoJSON Directa**: Botón en la barra superior que permite al usuario descargar en su navegador el GeoJSON curado completo en tiempo real.

---

## 6. Guía de Ejecución y Reproducción

### Opción A: Desde Python / Línea de Comandos
```bash
# Ejecutar la generación del dashboard y exportación del GeoJSON
python -c "from src.visualization.geo_dashboard import generate_interactive_gis_dashboard; p = generate_interactive_gis_dashboard(); print('Dashboard generado exitosamente en:', p)"
```

### Opción B: Mediante Cuaderno Jupyter Pedagógico
Abrir y ejecutar paso a paso el cuaderno:
- `notebooks/05_visualization/01_visualization_dashboard.ipynb`

### Opción C: Ver el Resultado en el Navegador
Abrir el archivo resultante con cualquier navegador web moderno:
```bash
# En Windows (PowerShell)
Start-Process "reports\dashboard_geografico_sipta.html"
```

---

## 7. Pruebas Automatizadas del Subsistema

El sistema de visualización cuenta con validación continua en `tests/test_visualization.py`:
- `test_multidomain_geodataframe_integrity`: Valida que el GeoDataFrame contenga exactamente las 20 localidades oficiales sin geometrías nulas.
- `test_classification_breaks_monotonicity`: Valida que las rupturas de Fisher-Jenks y Cuantiles sean estrictamente monótonas crecientes.
- `test_dashboard_html_generation`: Valida la compilación del archivo HTML y la inclusión de todas las variables JSON requeridas.

---

## 8. Cumplimiento de Protocolos de Interacción Humano-Computador (IHC / HCI)

El diseño y la arquitectura interactiva del dashboard Web GIS implementan de forma rigurosa los estándares internacionales de **Interacción Humano-Computador (IHC)**: **ISO 9241-110** (Principios de diálogo ergonómico), **ISO 9241-210** (Diseño centrado en el humano), las **10 Heurísticas de Usabilidad de Nielsen**, las **8 Reglas Doradas de Shneiderman** y las pautas de accesibilidad **WCAG 2.1 Nivel AA**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               ARQUITECTURA DE INTERACCIÓN HUMANO-COMPUTADOR (IHC / HCI)                │
├───────────────────┬───────────────────┬────────────────────┬───────────────────────────┤
│ 1. VISIBILIDAD Y  │ 2. CONTROL Y      │ 3. RECONOCIMIENTO  │ 4. ACCESIBILIDAD          │
│    RETROALIMENTACIÓN│    LIBERTAD       │    ANTES DE RECUERDO│   UNIVERSAL (WCAG AA)     │
├───────────────────┼───────────────────┼────────────────────┼───────────────────────────┤
│ • Breadcrumbs     │ • Paneles         │ • Buscador         │ • Modo Daltónicos         │
│   contextuales    │   colapsables     │   predictivo con   │   (Paleta Viridis)        │
│ • Toast alerts    │   ([ y ])         │   autocomplete     │ • Semáforos redundantes   │
│ • Semáforos con   │ • Modo Mapa Zen   │ • Guía de ayuda    │   (Ícono + Texto + Color) │
│   etiqueta textual│ • Centrado rápido │   interactiva (?)  │ • Navegación por teclado  │
│ • Diagnósticos IC │ • Zoom a polígono │ • Tooltips con     │ • Anillos de foco visibles│
│   Bootstrap 95%   │ • Exportación CSV │   metadatos y rango│ • Skip link para lectores │
└───────────────────┴───────────────────┴────────────────────┴───────────────────────────┘
```

### Principios y Mecanismos IHC Específicos

1. **Visibilidad del Estado del Sistema (*System Status Visibility*)**:
   - **Migas de Pan Contextuales (*Breadcrumbs*)**: El encabezado muestra en todo momento la ruta de exploración: `Bogotá D.C. › [Sector] › [Indicador Activo]`.
   - **Notificaciones Toast no Intrusivas**: Cada acción (cambio de sector, exportación, activación de capas, selección territorial o atajo de teclado) emite una confirmación visual accesible.
   - **Contador de Cobertura**: Indicador en tiempo real de 20 de 20 localidades analizadas con valores normalizados.

2. **Control y Libertad del Usuario (*User Control and Freedom*)**:
   - **Paneles Laterales Colapsables**: El usuario puede ocultar los paneles izquierdo y derecho mediante los botones en pantalla o las teclas `[` y `]`, habilitando un **Modo Pantalla Completa de Mapa (*Zen Mode*)**.
   - **Restablecimiento Global**: Botón de "Centrar Bogotá" (tecla `R`) y opción de zoom directo al polígono de la localidad seleccionada.

3. **Reconocimiento antes que Recuerdo (*Recognition rather than Recall*)**:
   - **Buscador Predictivo con Autocomplete (`Ctrl + K` / `/`)**: Menú desplegable instantáneo que lista las 20 localidades con su código DIVIPOLA y posición en el ranking mientras el usuario escribe, permitiendo selección inmediata con teclado o ratón.
   - **Guía de Ayuda y Atajos de Teclado (`?` / `H`)**: Diálogo modal accesible que detalla las funciones del sistema, la interpretación de las alertas tempranas y la fundamentación matemática de Fisher-Jenks frente a Cuantiles.

4. **Flexibilidad y Eficiencia de Uso (*Flexibility and Efficiency of Use*)**:
   - **Atajos de Teclado Universales**:
     - `Ctrl + K` o `/`: Enfocar buscador predictivo de localidades.
     - `R`: Restablecer y centrar mapa en Bogotá D.C.
     - `J` / `Q`: Alternar entre clasificación de Fisher-Jenks y Cuantiles.
     - `[` / `]`: Colapsar/expandir paneles izquierdo y derecho.
     - `E` / `C`: Exportar capa espacial GeoJSON o tabla en formato CSV.
     - `?` o `H`: Abrir guía de interacción y protocolos IHC.
     - `Esc`: Cerrar modales, menú de sugerencias o deseleccionar elementos.
   - **Visualización Multimodal**: Pestañas intercambiables para alternar entre el **Ranking Distrital de Barras** y el **Radar Multidimensional de las 7 Dimensiones Canónicas**.
   - **Copia Rápida**: Botón para copiar la ficha analítica de la localidad al portapapeles en formato estructurado para informes ejecutivos.

5. **Accesibilidad Universal e Inclusión (WCAG 2.1 AA)**:
   - **Modo Accesible para Daltonismo**: Alternador a paleta perceptual uniforme **Viridis / Cividis**, eliminando la ambigüedad para usuarios con protanopia, deuteranopia o tritanopia.
   - **Codificación Redundante (Principio de No Dependencia Exclusiva del Color)**: Los semáforos de alerta utilizan simultáneamente color, icono y etiqueta textual (🔴 Muy Alta Prioridad, 🟠 Alta Prioridad, 🟡 Media Prioridad, 🟢 Baja Prioridad).
   - **Navegabilidad Asistida**: Enlace accesible invisible para lectores de pantalla (*Skip Link*), etiquetas `aria-label`, roles semánticos WAI-ARIA (`dialog`, `region`, `status`, `tab`) y contornos de foco de alto contraste (`focus-visible`).

---

## 9. Módulo de Cruce Analítico con Inversión Pública y Nuevos Ratios Territoriales

Atendiendo a las recomendaciones del comité evaluador y requerimientos analíticos distritales, el sistema incorpora el **Módulo de Análisis Bivariado de Inversión Pública Distrital**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             MATRIZ DE CUADRANTES ESTRATÉGICOS: PRIVACIÓN VS. INVERSIÓN PÚBLICA          │
├───────────────────────────────────────────┬────────────────────────────────────────────┤
│   CUADRANTE II: 🔴 BRECHA CRÍTICA         │   CUADRANTE I: 🔵 PRIORIDAD ATENDIDA       │
│   • Alta Privación / Déficit              │   • Alta Privación / Déficit               │
│   • Baja Inversión per Cápita             │   • Alta Inversión per Cápita              │
│   → Urgencia máxima de reasignación fiscal│   → Asignación focalizada y progresiva     │
├───────────────────────────────────────────┼────────────────────────────────────────────┤
│   CUADRANTE III: 🟢 AUTOSUFICIENCIA        │   CUADRANTE IV: 🟠 EFICIENCIA A REVISAR    │
│   • Baja Privación (Buena cobertura)      │   • Baja Privación (Buena cobertura)       │
│   • Baja Inversión per Cápita             │   • Alta Inversión per Cápita              │
│   → Equilibrio socioeconómico sostenible  │   → Revisión de costo-eficiencia y retornos│
└───────────────────────────────────────────┴────────────────────────────────────────────┘
```

### A. Funcionalidades del Módulo de Inversión
1. **Botón de Cruce Bivariado**: Ubicado junto a la selección de clasificación cartográfica (Atajo: `I`).
2. **Correlación Bivariada de Pearson ($r$) y Spearman ($\rho$)**: Calculada dinámicamente en tiempo real entre la variable activa y la inversión correspondiente al sector.
3. **Scatter Plot 2D Interactivo**: Visualiza las 20 localidades en los cuatro cuadrantes estratégicos, permitiendo resaltar o hacer zoom directo a la localidad seleccionada.
4. **Tabla de Brechas Fiscales**: Ordena automáticamente las localidades en *Brecha Crítica* con acceso directo al mapa.

### B. Indicadores Normalizados Per Cápita y por 10.000 Habitantes
- **Vulnerabilidad Social**: Comedores comunitarios por 10.000 hab. (`comedores_por_10k_hab`) y Tasa de beneficiarios de transferencias monetarias (`tasa_beneficiarios_transferencias_pct`).
- **Infraestructura**: Densidad de luminarias por km² (`luminarias_por_km2`) y oferta por 10.000 hab. (`luminarias_por_10k_hab`).
- **Ambiente y Servicios**: Consumo promedio residencial de agua por 10.000 hab. (`consumo_agua_por_10k_hab_m3`).
- **Mercado Laboral**: Clarificación metodológica del ingreso laboral promedio mensual ($ COP por trabajador ocupado).
- **Participación Ciudadana**: Votantes en presupuestos participativos por 10.000 hab. (`tasa_votantes_pp_por_10k_hab`) y Propuestas ciudadanas priorizadas por 10.000 hab. (`propuestas_ciudadanas_por_10k_hab`).
- **Finanzas e Inversión Pública**: Inversión presupuestos participativos per cápita (`inversion_pp_per_capita_cop`), Inversión en educación SED per cápita (`inversion_educacion_per_capita_cop`) e Inversión total consolidada per cápita (`inversion_total_consolidada_per_capita_cop`).

### C. Ranking Reactivo Dinámico
El puesto del ranking en el inspector territorial y el gráfico de barras se computa dinámicamente en memoria según la polaridad de la variable seleccionada (`#X / 20`), manteniendo el puesto global IPT consenso como badge secundario de referencia.


