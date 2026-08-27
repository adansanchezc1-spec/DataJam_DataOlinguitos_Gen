# Sistema de Visualización Geoespacial y Dashboard Web GIS — SIPTA (v1.2.0)

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
│    (WGS84 EPSG:4326)           │  • Tablón Maestro Territorial (13 dominios)│
├────────────────────────────────┼───────────────────────────────────────────┤
│    MOTOR PYTHON (src/)         │  • Cruce geoespacial determinista         │
│    geo_dashboard.py            │  • Algoritmo Fisher-Jenks & Cuantiles     │
│                                │  • 5 Escenarios de Sensibilidad IPT       │
│                                │  • Serialización JSON optimizada (RFC 7946)│
├────────────────────────────────┼───────────────────────────────────────────┤
│    SALIDA AUTÓNOMA             │  • reports/dashboard_geografico_sipta.html│
│    (Leaflet.js + Chart.js)     │  • data/curated/sipta_localidades...geojson│
└────────────────────────────────┴───────────────────────────────────────────┘
```

---

## 2. Ingesta y Procesamiento de Datos Geoespaciales (GeoJSON)

### A. Capa Poligonal Base de Localidades
- **Archivo de Origen**: `data/processed/MODELO_TERRITORIAL/poligonos_localidades.geojson`.
- **Sistema de Referencia Espacial**: Coordenadas geográficas estándar **WGS84 (EPSG:4326)** con geometrías tipo `Polygon` y `MultiPolygon`.
- **Identificador Canónico**: Código DIVIPOLA SDP (`identificador_localidad` del 1 al 20) y nombre oficial (`nombre_localidad`).

### B. Cruce Geoespacial y Tabular Multidominio
La función `build_multidomain_geodataframe()` en `src/visualization/geo_dashboard.py` realiza la integración:
1. Lee los polígonos de las 20 localidades mediante `geopandas.read_file()`.
2. Lee el tablón maestro curado `data/curated/master_indicadores_territoriales.csv` (13 dominios).
3. Realiza un *join* determinista usando el código numérico de localidad:
   $$\text{GeoDataFrame} = \text{Polígonos} \bowtie_{\text{codigo\_localidad}} \text{Tablas Sectoriales}$$
4. Limpia geometrías, simplifica atributos nulos y calcula columnas auxiliares para semaforización.

### C. Capas Vectoriales Puntuales (Overlays) con Reproyección Garantizada
La función `load_point_overlay_layers()` carga 5 capas temáticas de puntos georreferenciados para enriquecer el análisis contextual:
- 🚌 **Estaciones Troncales TransMilenio** (`#ef4444`): `data/processed/MOVILIDAD/estaciones_troncales.geojson`.
- 🚇 **Estaciones Metro Línea 1** (`#06b6d4`): `data/processed/MOVILIDAD/estaciones_linea1.geojson` (reproyectada desde EPSG:6247 MAGNA-SIRGAS Bogotá Urban Grid a WGS84 EPSG:4326).
- 🍃 **Estaciones de Monitoreo de Calidad del Aire** (`#0284c7`): `data/processed/AMBIENTE/estacion_calidad_aire.geojson`.
- 🍎 **Puntos de Encuentro de Vendedores Informales (IPES)** (`#f97316`): `data/processed/FINANZAS_INVERSION_PUBLICA/Punto de encuentro vendedores. Bogotá D.C..geojson`.
- 🏫 **Oferta de Cupos Escolares Oficiales SED** (`#059669`): `data/processed/EDUCACION/ofertacupos_032025_wgs84.geojson`.

### D. Exportación de Capa GeoJSON Curada
La función `export_curated_multidomain_geojson()` serializa el GeoDataFrame completo bajo el estándar internacional **RFC 7946 GeoJSON** en:
- `data/curated/sipta_localidades_multidominio.geojson`

---

## 3. Auditoría Cromática y Clasificación no Arbitraria

### A. Política Estricta de Colorimetría (Cero Negros)
Siguiendo las directrices de diseño cartográfico y accesibilidad visual, queda estrictamente prohibido el uso de tonos negros puros (`#000000` o `#000004`) en cualquier indicador o escala secuencial. Todas las paletas emplean gradientes perceptualmente uniformes:
- **Seguridad**: Paleta `Reds` (carmesí y vino profundo: `#fee2e2` a `#881337`).
- **Mercado Laboral**: Paleta `YlOrBr` (ámbar y ocre tostado: `#fef3c7` a `#78350f`).
- **Educación / Infraestructura**: Paleta `Greens` (esmeralda bosque: `#ecfdf5` a `#064e3b`).
- **Salud**: Paleta `Blues` (azul cielo a azul noche: `#eff3ff` a `#1e3a8a`).
- **Modo Daltónico**: Paletas `Viridis` y `Cividis` con gradientes sin zonas oscuras opacas.

### B. Algoritmo Fisher-Jenks y Cuantiles
- **Fisher-Jenks (Natural Breaks)**: Minimiza la varianza interna en 5 clases: $\min \sum_{j=1}^5 \sum_{i \in C_j} (x_i - \bar{x}_j)^2$.
- **Cuantiles**: Distribuye exactamente 4 localidades por quintil ($20/5 = 4$).

---

## 4. Escenarios de Sensibilidad y Robustez del IPT

El módulo `src/modeling/calculate_indicators.py` y el visualizador integran los **5 escenarios metodológicos de robustez**:

| Escenario $k$ | Nombre | Dimensiones ($D_k$) | Ecuación / Formulación |
|---|---|---|---|
| **Escenario 1** | Base Lineal | 7 dimensiones canónicas | $IPT_1 = \frac{1}{7} \sum_{d=1}^7 s_{i,d} \times 100$ |
| **Escenario 2** | Rangos (Percentiles) | 7 dimensiones con orden no paramétrico | $IPT_2 = \frac{1}{7} \sum_{d=1}^7 \left(\frac{\text{rank}(x_{i,d}) - 1}{N - 1}\right) \times 100$ |
| **Escenario 3** | Sin Proxy Parques | 6 dimensiones (excluye IDRD) | $IPT_3 = \frac{1}{6} \sum_{d \neq \text{parques}} s_{i,d} \times 100$ |
| **Escenario 4** | Sin RIVI | 6 dimensiones (excluye vendedores informales) | $IPT_4 = \frac{1}{6} \sum_{d \neq \text{vendedores}} s_{i,d} \times 100$ |
| **Escenario 5** | Cinco Dimensiones Duras | 5 dimensiones canónicas duras | $IPT_5 = \frac{1}{5} \sum_{d \in \{\text{pob, ips, cupos, paraderos, luminarias}\}} s_{i,d} \times 100$ |

Cada escenario cuenta con su respectiva columna de puntaje (`IPT_ESC_1_SCORE` a `IPT_ESC_5_SCORE`) y ranking territorial (`RANKING_ESC_1` a `RANKING_ESC_5`), además del consenso ponderado global.

---

## 5. Contraste Demográfico en Tooltips e Inspectores

Para evitar sesgos de interpretación de escala en indicadores de tasa por 10.000 habitantes, los tooltips e inspectores muestran la capacidad absoluta contrastada con la población:
- **Salud**: Sedes IPS habilitadas (REPS), total de camas hospitalarias, camas UCI contrastadas con la población proyectada 2025 (`poblacion_2025`).
- **Infraestructura y Parques**: Área total de parques en metros cuadrados (`area_total_parques_m2`), superficie en hectáreas (`area_parques_ha`) y $m^2$ de parque por habitante (`m2_parque_por_habitante`).
- **Seguridad**: Total anual de hurtos a personas (MEBOG/SIEDCO), homicidios y tasa de hurtos por 10.000 habitantes (`tasa_hurto_personas_por_10k_hab`).

---

## 6. Módulo de Cruce Analítico Bivariado: 4 Cuadrantes Estratégicos

El modal bivariado (`openInvestmentModal`) implementa la evaluación de progresividad y focalización presupuestal:

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

### Funcionalidades del Módulo Bivariado:
1. **4 Tarjetas KPI Simultáneas**: Muestran en tiempo real el conteo de localidades en cada uno de los 4 cuadrantes ($Q_1, Q_2, Q_3, Q_4$).
2. **Barra de Chips de Filtrado Interactivo**: Permite filtrar instantáneamente la tabla comparativa (`[Todos (20)]`, `[🔵 Q1 Atendida]`, `[🔴 Q2 Brecha Crítica]`, `[🟢 Q3 Autosuficiencia]`, `[🟠 Q4 Eficiencia]`).
3. **Métricas de Correlación**: Pearson $r$ y Spearman $\rho$ en tiempo real con diagnóstico fiscal (*Progresivo*, *Regresivo*, *Focalización Moderada*).
4. **Scatter Plot 2D Interactivo**: Con líneas de corte en medianas y tooltips con valores exactos en pesos colombianos ($ COP/hab).
5. **Exportación CSV**: Descarga directa de la matriz de cruce bivariada.

---

## 7. Pruebas y Reproducibilidad

```bash
# Compilar dashboard interactivo
python -c "from src.visualization.geo_dashboard import generate_interactive_gis_dashboard; p = generate_interactive_gis_dashboard(); print('Dashboard HTML compilado en:', p)"

# Ejecutar suite de pruebas unitarias
python -m pytest tests/test_pipeline_modeling_viz.py tests/test_visualization.py -v
```



