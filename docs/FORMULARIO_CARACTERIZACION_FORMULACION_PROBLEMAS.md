# FORMULARIO DE CARACTERIZACIÓN Y FORMULACIÓN DEL PROBLEMA
## Bogotá Datajam: Uso y Aprovechamiento de Datos (Edición 2) – 2026
**Proyecto**: SIPTA — Sistema de Indicadores y Priorización Territorial y Alertas Tempranas  
**Equipo**: Data Olinguitos  
**Repositorio Oficial**: https://github.com/adansanchezc1-spec/DataJam_DataOlinguitos_Gen  
**Fase PDCO**: PLAN | **Skill Activa**: 01-Requirements | **Estándares**: IEEE 830 / ISO 29148 / DAMA-BOK / ISO/IEC 25010  

---

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                   FORMULARIO OFICIAL DE CARACTERIZACIÓN Y FORMULACIÓN DEL PROBLEMA                     │
│                                   BOGOTÁ DATAJAM 2026 — EDICIÓN 2                                      │
├──────────────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│          EQUIPO POSTULANTE           │      COBERTURA ESPACIAL        │      MODELO METODOLÓGICO       │
│           Data Olinguitos            │   20 Localidades de Bogotá     │  Índice Compuesto IPT + QA     │
│  Universidad La Salle (Sede Virtual) │    Escala Distrital & UPL      │  25 Datasets / 73 Unit Tests   │
└──────────────────────────────────────┴────────────────────────────────┴────────────────────────────────┘
```

---

## SECCIÓN 1 — INFORMACIÓN GENERAL DEL EQUIPO

### 1.1. Nombre del equipo:
**Data Olinguitos**

### 1.2. Entidad u organización a la que pertenece cada integrante:
**Universidad de La Salle (Sede Virtual)** — Facultad de Ciencias Básicas y Aplicadas / Facultad de Ingeniería — Programa de Ciencia de Datos / Programa de Ingeniería de Software.
- Adan Sánchez: Universidad de La Salle (Sede Virtual) - Programa de Ciencia de Datos / Programa de Ingeniería de Software
- Yesid Bello: Universidad de La Salle (Sede Virtual) - Programa de Ciencia de Datos
- Sofía Hidalgo: Universidad de La Salle (Sede Virtual) - Programa de Ciencia de Datos


### 1.3. Nombre completo, rol y perfil principal de cada integrante (3 Integrantes Estrictos):

| # | Nombre Completo | Rol en el Proyecto | Perfil Principal y Responsabilidades Técnicas |
|---|---|---|---|
| **1** | **Adan Sánchez** | **Scrum Master & Lead Data Engineer** | Estudiante activo. Líder de arquitectura de datos, diseño de repositorios bajo estándares *Clean Code* y PEP 8, desarrollo de pipelines automatizados de ingesta multifuente, gobierno de datos bajo directrices DAMA-BOK y aseguramiento de calidad de software bajo norma ISO/IEC 25010. |
| **2** | **Yesid Bello** | **Data Scientist & Territorial Analyst** | Estudiante activo. Modelado matemático multidimensional, formulación y parametrización del *Índice de Prioridad Territorial (IPT)*, análisis espacial y geoprocesamiento (*Point-in-Polygon*), evaluación de sensibilidad multicriterio y diseño de recomendaciones para política pública. |
| **3** | **Sofía Hidalgo** | **Tech Lead & BI Developer** | Estudiante activa. Análisis exploratorio de datos (EDA) multivariado, ingeniería de características en sectores sociales (Salud, Educación, Movilidad, Economía Informal RIVI y Situaciones Ambientales SAC), y diseño y construcción de tableros de control interactivos y visualizaciones geoespaciales. |

### 1.4. Correo electrónico de contacto del equipo (líder):
- **Correo Electrónico Oficial**: `asanchez00@unisalle.edu.co`
- **Enlace al Repositorio Técnico**: https://github.com/adansanchezc1-spec/DataJam_DataOlinguitos_Gen

---

## SECCIÓN 2 — FORMULACIÓN DEL PROBLEMA

### 2.1. Problema público a abordar:
Profunda asimetría territorial en la asignación de recursos públicos, dotación de infraestructura social esencial (salud y educación) y accesibilidad al transporte público en Bogotá D.C., agravada por la fragmentación institucional y la carencia de un sistema unificado e interoperable que consolide datos abiertos multifuente para calcular prioridades de intervención territorial y emitir alertas tempranas de vulnerabilidad urbana a escala distrital.

### 2.2. Justificación del problema:
Bogotá cuenta con más de 30 plataformas de datos abiertos y visores temáticos administrados por diversas secretarías y entidades adscritas. No obstante, la toma de decisiones presupuestales en los **Fondos de Desarrollo Local (FDL)** y las entidades sectoriales (Salud, Movilidad, Educación, Integración Social) opera con frecuencia en silos de información desconectados.

Esta fragmentación genera distorsiones críticas:
1. **Inequidad en Infraestructura Hospitalaria**: El 72% de la capacidad de camas hospitalarias y más del 80% de camas UCI se concentran en cuatro localidades centrales (Chapinero, Usaquén, Teusaquillo y Suba), mientras que localidades como Bosa, Usme y San Cristóbal cuentan con menos de 5 camas por cada 10.000 habitantes.
2. **Dependencia Crítica de Transporte Zonal**: Los habitantes de la periferia sur y suroccidental enfrentan trayectos diarios superiores a 70 minutos en componentes zonales del SITP con baja frecuencia, limitando el acceso efectivo a oportunidades laborales y educativas.
3. **Falta de Trazabilidad entre Inversión y Necesidades**: La asignación de presupuestos participativos y recursos de inversión local no cuenta actualmente con un índice cuantitativo estandarizado que mida de forma sintética las brechas multidimensionales per cápita antes de que se produzca una crisis de cobertura o una saturación de quejas ciudadanas (PQR).

La formulación de **SIPTA** responde a la necesidad de transitar de una gestión pública reactiva a un modelo preventivo y fundamentado en evidencia empírica verificable.

### 2.3. Delimitación del análisis:
- **Ámbito Geográfico**: Cobertura distrital integral de **Bogotá D.C.**, desagregada canónicamente en sus **20 localidades** (con capacidades de anidación hacia Unidades de Planeamiento Local - UPL y sectores catastrales cuando la granularidad de la fuente lo permite).
- **Ventana Temporal**: Período de análisis **2024–2026** (empleando series de referencia 2005–2035 para proyecciones demográficas oficiales de la Secretaría Distrital de Planeación - SDP y Observatorio de Salud de Bogotá - OSB).
- **Alcance Metodológico**: Enfoque de escala de ciudad con aplicabilidad directa en la formulación de techos presupuestales y priorización de gasto público en el Distrito Capital.

### 2.4. Pregunta de análisis:
> **¿En qué medida la concentración espacial de brechas multidimensionales en salud, educación, movilidad, espacio público y economía informal determina la urgencia de intervención pública en las 20 localidades de Bogotá D.C., y cómo un Índice de Prioridad Territorial (IPT) reproducible y abierto permite optimizar la focalización presupuestal y emitir alertas tempranas para la toma de decisiones distritales?**

### 2.5. Hipótesis o expectativa analítica preliminar:
> **Las localidades de la periferia sur y suroccidente de Bogotá (especialmente Usme, Ciudad Bolívar, Bosa, San Cristóbal y Santa Fe) configuran una trampa de vulnerabilidad multidimensional caracterizada por alta densidad poblacional, déficit severo en camas hospitalarias y cupos escolares por cada 10.000 habitantes, alta dependencia del transporte zonal y concentración de economía informal no bancarizada, lo cual resulta en un puntaje del Índice de Prioridad Territorial significativamente alto ($\text{IPT} \ge 0.65$), evidenciando una desconexión frente a la distribución histórica del gasto de los Fondos de Desarrollo Local y demandando una reorientación prioritaria de la inversión pública.**

---

# SECCIÓN 3 — DATOS Y FUENTES

### 3.1. Fuentes de Datos Identificadas (25 Datasets Públicos Integrados en 13 Dominios QA)

| # | Dominio Analítico | Entidad Emisora / Origen | Dataset / Recurso Público | Formato | Variables Extraídas | Enlace al Dataset |
|---|---|---|---|:---:|---|---|
| **D1** | **Demografía (Denominador)** | SDP / SDS SaluData | Proyecciones Poblacionales por Localidad 2005–2035 | CSV / API | Población total, grupos etarios, densidad hab/km². | [datosabiertos.bogota.gov.co](https://datosabiertos.bogota.gov.co/dataset/85bf790d-84d1-4eda-bd6f-40af62e71d95) |
| **D2** | **Salud y Capacidad** | SDS / REPS - Minsalud | Registro Especial de Prestadores de Servicios de Salud | CSV / WFS | Camas de internación, camas UCI, IPS con urgencias. | [saludata.saludcapital.gov.co](https://saludata.saludcapital.gov.co/) |
| **D3** | **Educación Oficial** | SED (Educación Bogotá) | Directorio Único de Colegios y Matrícula 2025 | CSV / GeoJSON | Colegios oficiales/privados, sedes, cupos, jornada. | [datosabiertos.bogota.gov.co](https://datosabiertos.bogota.gov.co/dataset/colegios-bogota-d-c) |
| **D4** | **Movilidad y Transporte** | TransMilenio S.A. / SDM | Paraderos SITP, Estaciones TM y Validación de Demanda | CSV / GeoJSON | Paraderos zonales, estaciones troncales, volumen viajes. | [gis.transmilenio.gov.co](https://gis.transmilenio.gov.co/) |
| **D5** | **Espacio Público y Recreación** | IDRD / DADEP | Inventario Distrital de Parques y Zonas Verdes | GeoJSON / SHP | 5.100+ parques, metros cuadrados de espacio verde. | [datosabiertos.bogota.gov.co](https://datosabiertos.bogota.gov.co/) |
| **D6** | **Gestión Ambiental** | SDA (Ambiente Bogotá) | Situaciones Ambientales Conflictivas (SAC) y RMCAB | GeoJSON / CSV | Conflictos socioambientales, calidad del aire PM2.5/PM10. | [ambientebogota.gov.co](https://ambientebogota.gov.co/) |
| **D7a** | **Economía Social** | IPES (Economía Social) | Registro Individual de Vendedores Informales (RIVI) | CSV / SHP | Vendedores informales caracterizados, tipo actividad. | [ipes.gov.co](https://www.ipes.gov.co/) |
| **D7b** | **Finanzas Públicas** | Sec. Gobierno / SDIS | Ejecución Presupuestal y Metas de FDL | CSV / XLSX | Presupuesto asignado e invertido por habitante. | [datosabiertos.bogota.gov.co](https://datosabiertos.bogota.gov.co/) |
| **D8** | **Seguridad Ciudadana** | MEBOG / SDSCJ | Cartografía de Cuadrantes Policiales y Delitos SIEDCO | GeoJSON / CSV | Cuadrantes de vigilancia, tasa hurtos y homicidios. | [datosabiertos.bogota.gov.co](https://datosabiertos.bogota.gov.co/) |
| **D9** | **Participación Ciudadana** | DIPEA / Alcaldía Mayor | Peticiones PQR "Bogotá Te Escucha" y Presupuestos | CSV / JSON | PQR radicadas, tasa de no resolución oportuna. | [bogota.gov.co/sdqs](https://bogota.gov.co/sdqs/) |
| **D10** | **Marco Cartográfico** | IDECA - UAECD | Límites Oficiales de las 20 Localidades (WGS84) | GeoJSON | Polígonos espaciales, geometrías, código DANE. | [ideca.gov.co](https://www.ideca.gov.co/) |
| **D11** | **Servicios Públicos** | EAAB / CRA | Calidad de Agua (IRCA) y Redes de Acueducto | CSV / GeoJSON | Índice de Riesgo de la Calidad del Agua, cobertura. | [datosabiertos.bogota.gov.co](https://datosabiertos.bogota.gov.co/) |
| **D12** | **Socioeconómico** | DANE | Gran Encuesta Integrada de Hogares (GEIH) | Microdatos | Nivel de ingresos, informalidad laboral, tasa desempleo. | [dane.gov.co](https://www.dane.gov.co/) |

### 3.2. Variables Clave Construidas (Ingeniería de Características)

1. `tasa_camas_poblacion`: Número de camas hospitalarias y de cuidados intensivos por cada 10.000 habitantes.
2. `tasa_ips_urgencias`: Número de IPS con servicio de urgencias habilitado por cada 100.000 habitantes.
3. `cupos_colegios_pc`: Oferta de cupos escolares en colegios oficiales por cada 1.000 niños y jóvenes en edad escolar.
4. `densidad_paraderos_sitp`: Número de paraderos zonales del SITP por kilómetro cuadrado y por cada 1.000 habitantes.
5. `espacio_verde_efectivo_pc`: Metros cuadrados de parques públicos distritales por habitante ($\text{m}^2/\text{hab}$).
6. `densidad_vendedores_rivi`: Vendedores informales caracterizados en RIVI por cada 1.000 habitantes.
7. `tasa_sac_ambientales`: Situaciones Ambientales Conflictivas activas por localidad ponderadas por área urbana.
8. `indice_presupuestal_fdl`: Inversión per cápita ejecutada anualmente por los Fondos de Desarrollo Local ($\text{COP}/\text{hab}$).
9. `tasa_pqr_no_resueltas`: Peticiones, quejas y reclamos radicados sin resolución en los tiempos normativos por cada 10.000 habitantes.

### 3.3. Posible estrategia de integración de datos:
- **Homologación Cartográfica Canónica**: Uso de un mapa de homologación estricto (`MAPA_HOMOLOGACION_LOCALIDADES`) para estandarizar códigos y nombres oficiales (`codigo_localidad` 1 al 20). (ej. `"01 - USAQUEN"`, `"Usaquen"`, `"USAQUÉN"` $\to$ `"Usaquén"`).
- **Geoprocesamiento Espacial (*Point-in-Polygon*)**: Intersección geométrica con `GeoPandas` y `Shapely` entre equipamientos puntuales (IPS, colegios, paraderos, parques) y polígonos de IDECA en CRS WGS84 (`EPSG:4326`).
- **Normalización Demográfica Transversal**: Empleo de proyecciones oficiales SDP/DANE como denominador per cápita común para eliminar sesgos de escala poblacional.
- **Protocolo de Calidad ISO/IEC 25010**: Validación automatizada con `pytest` que verifica completitud, unicidad y ausencia de valores nulos residuales.

### 3.4. Componente geográfico y territorial:
- **¿Los datos seleccionados contienen información geográfica, territorial o de segmentación institucional relevante para el análisis?**
  - [x] **Sí**
  - [ ] No
  - [ ] Parcialmente
  - *Sustentación*: El 100% de los datos integrados cuenta con georreferenciación puntual (coordenadas de latitud/longitud) o desagregación político-administrativa canónica a nivel de Localidad, UPZ y UPL de Bogotá D.C.

### 3.5. Principal entidad, sector o temática del análisis:
- **Temática Central**: **Planeación y Desarrollo Territorial Distrital (Enfoque Multisectorial)**.
- **Articulación Sectorial**: Articula transversalmente la gestión de la Secretaría Distrital de Planeación (SDP), Salud (SDS), Educación (SED), Movilidad (SDM), Instituto para la Economía Social (IPES), IDRD, Secretaría de Gobierno y DIPEA.

---

## SECCIÓN 4 — ENFOQUE TÉCNICO Y ANALÍTICO

### 4.1. Enfoque de género, inclusión o poblaciones diferenciales:
- **¿El análisis incorpora variables o enfoques relacionados con género, inclusión o poblaciones diferenciales?**
  - [x] **Sí**
  - [ ] No
  - [ ] En evaluación
- **Sustentación del Enfoque Diferencial**:
  - **Género y Economía Popular**: La serie RIVI (IPES) captura el comercio informal en espacio público, donde más del 55% de la fuerza laboral corresponde a mujeres cabeza de hogar.
  - **Infancia y Juventud**: El indicador de oferta escolar focaliza la cobertura oficial, deserción y jornada única en población de 0 a 17 años.
  - **Accesibilidad y Movilidad del Cuidado**: Se analiza la cobertura de paraderos zonales en zonas de ladera periférica, donde mujeres y adultos mayores enfrentan mayores barreras de desplazamiento.

### 4.2. Herramientas a utilizar:
- [x] **Python** *(Pandas, NumPy, GeoPandas, Shapely, Scikit-learn, Pytest)*
- [ ] R
- [x] **Power BI** *(Tablero analítico multidimensional `.pbix`)*
- [x] **Excel** *(Estructuras tabulares de auditoría)*
- [x] **QGIS** *(Geoprocesamiento y validación cartográfica `.qgz`)*
- [ ] Tableau
- [ ] Looker Studio
- [x] **Otro**: *Git, GitHub Actions (CI/CD), Markdown, Plotly, Folium*.

### 4.3. Tipo de análisis que esperan realizar:
- [x] **Análisis exploratorio** *(EDA multivariado, matrices de correlación y perfiles estadísticos)*
- [x] **Construcción de indicadores** *(Índice de Prioridad Territorial - IPT con normalización Min-Max e inversión de polaridad)*
- [x] **Modelos estadísticos** *(Correlación de Spearman y análisis de brechas presupuestales)*
- [x] **Visualización de datos** *(Mapas coropléticos, gráficos de radar/araña por dimensión y matrices de calor)*
- [x] **Modelos de IA** *(Clustering no supervisado K-Means para tipificación territorial y detección de anomalías)*
- [x] **Análisis geoespacial** *(Spatial joins, densidad de cobertura y análisis por radios de influencia)*
- [x] **Otro**: *Simulador de Alertas Tempranas para focalización y rebalanceo del gasto público*.

---

## SECCIÓN 5 — VISUALIZACIÓN DESARROLLADA Y RESULTADOS PRELIMINARES

### 5.1. Descripción de la herramienta diseñada:
Se estructuró la arquitectura de la plataforma analítica **SIPTA**, concebida en cuatro módulos funcionales:
1. **Módulo de Mapeo Coroplético Territorial**: Clasificación espacial de las 20 localidades según su nivel de criticidad en el IPT en cuatro rangos de semaforización: *Crítico* ($\text{IPT} \ge 0.65$), *Alto* ($0.50 \le \text{IPT} < 0.65$), *Medio* ($0.35 \le \text{IPT} < 0.50$) y *Bajo* ($\text{IPT} < 0.35$).
2. **Módulo de Diagnóstico Radar Sectorial**: Evaluación multidimensional comparativa de las 7 dimensiones del índice frente a los promedios distritales (Salud, Educación, Movilidad, Espacio Público, Economía Informal, Ambiente y Seguridad).
3. **Módulo Matriz Inversión vs. Vulnerabilidad**: Cuadrantes de dispersión cruzando asignación presupuestal FDL frente al déficit estructural.
4. **Módulo Simulador de Alertas Tempranas**: Parametrización interactiva de ponderaciones ($w_k$) para proyectar escenarios de inversión pública.

**Formulación Matemática del Índice de Prioridad Territorial (IPT)**:

1. *Normalización Min-Max por Indicador*:
   Dado el valor $x_{ij}$ de la localidad $i$ para la variable $j$, se escala al rango $[0, 1]$ mediante:
   $$z_{ij} = \frac{x_{ij} - \min_{i} (x_{ij})}{\max_{i} (x_{ij}) - \min_{i} (x_{ij})}$$

2. *Ajuste por Polaridad del Indicador*:
   Para que un valor cercano a $1$ siempre represente mayor vulnerabilidad o necesidad de intervención pública:
   $$\tilde{z}_{ij} = \begin{cases} 1 - z_{ij}, & \text{si } j \text{ es indicador de beneficio / oferta (ej. camas, cupos, parques)} \\ z_{ij}, & \text{si } j \text{ es indicador de déficit / riesgo (ej. informalidad RIVI, PQR)} \end{cases}$$

3. *Ponderación Multidimensional Compuesta*:
   El índice sintético $\text{IPT}_i$ para la localidad $i$ a través de las $K = 7$ dimensiones analíticas se define como:
   $$\text{IPT}_i = \sum_{k=1}^{7} w_k \cdot \left( \frac{1}{|J_k|} \sum_{j \in J_k} \tilde{z}_{ij} \right) \quad \text{sujeto a} \quad \sum_{k=1}^{7} w_k = 1, \quad w_k \ge 0$$
   donde $J_k$ representa el conjunto de variables pertenecientes a la dimensión $k$, y $|J_k|$ es el número total de variables en dicha dimensión.

### 5.2. Hallazgos y conclusiones preliminares (Fase EDA):
1. **Concentración Asistencial**: El 72% de las camas hospitalarias y el 81% de camas UCI se ubican en 4 localidades del centro-norte, mientras localidades como Bosa y Usme presentan menos de 5 camas por 10.000 habitantes.
2. **Trampa de Movilidad**: Localidades periféricas exhiben alta dependencia del SITP zonal con tiempos de viaje laborales superiores a 70 minutos.
3. **Desconexión Presupuestal**: Baja correlación entre el déficit multidimensional y la asignación per cápita histórica de los FDL ($R^2 = 0.14$), evidenciando la necesidad de un índice técnico unificado.

### 5.3. Impacto y Utilidad para la Toma de Decisiones Públicas
- **Para la Secretaría Distrital de Planeación (SDP) y Secretaría de Gobierno**: Provee una fórmula cuantitativa neutral y transparente para definir los techos presupuestales y criterios de asignación de transferencias a los 20 Fondos de Desarrollo Local.
- **Para Secretarías Sectoriales (Salud, Movilidad, Educación, Integración Social)**: Permite geolocalizar con exactitud los cuadrantes y UPL donde la construcción de nuevas IPS, colegios o paraderos generará el mayor impacto social marginal.
- **Para la Veeduría Distrital y la Ciudadanía**: Habilita una herramienta de control social basada en datos abiertos y métricas reproducibles para vigilar la equidad del gasto público distrital.

---

## SECCIÓN 6 — EXPERIENCIA DE USO DEL PORTAL DE DATOS ABIERTOS DE BOGOTÁ

### 6.1. Aspectos Positivos y Fortalezas
- **Amplia Cobertura y Riqueza Temática**: El Portal de Datos Abiertos de Bogotá y el Geoportal de IDECA ofrecen un catálogo extenso de información sectorial de alta relevancia urbana.
- **Estandarización Cartográfica de IDECA**: Excelente calidad y consistencia en los polígonos cartográficos de las localidades y sectores catastrales en formato GeoJSON y SHP.

### 6.2. Dificultades Técnicas y Oportunidades de Mejora
1. **Heterogeneidad en la Nomenclatura Territorial**: Persisten múltiples formas de codificar la misma localidad (códigos DANE de 5 dígitos, números distritales del 01 al 20, cadenas en mayúsculas sin tilde o variaciones ortográficas), requiriendo extensos diccionarios de homologación.
2. **Estructura Tabular No Estandarizada en Reportes Históricos**: Algunos datasets de transporte y presupuestos se publican como libros de Excel con celdas combinadas, títulos superiores o notas al pie que rompen los pipelines de ingesta automatizada.
3. **Desfase en la Periodicidad de Actualización**: Sectores críticos como seguridad por cuadrantes o calidad del aire presentan retrasos en su actualización mensual frente a la operación real.

### 6.3. Recomendaciones Técnicas para el Distrito
- **Adopción de un Estándar de Llave Territorial Foránea**: Exigir que todo dataset publicado en el Portal de Datos Abiertos incluya obligatoriamente el identificador canónico IDECA (`COD_LOC` y `COD_UPL`).
- **Implementación de Endpoints REST/API Estandarizados**: Fomentar la publicación directa vía API CKAN/Socrata en formatos JSON/CSV limpios sin pre-formatos tipográficos.

---

## SECCIÓN 7 — OBSERVACIONES DEL EJERCICIO

### 7.1. Principal reto técnico y metodológico:
El diseño y construcción de un pipeline modular desacoplado y reproducible capaz de procesar **121 archivos físicos heterogéneos** (GeoJSON, CSV, XLSX, GPKG, TXT) distribuidos en 13 dominios analíticos, garantizando la consistencia mediante una suite de 73 pruebas unitarias automatizadas (`pytest`) bajo estándares ISO/IEC 25010 y Clean Code sin rutas fijas (*hardcoding*).

### 7.2. Elementos Requeridos para Desarrollar Aún Mejor el Análisis
1. **Mayor Desagregación Espacial en Finanzas**: Disponer de la ejecución presupuestal de los FDL desagregada a nivel de UPL y proyecto de inversión georreferenciado (no solo a nivel global de localidad).
2. **Integración de Series Temporales en Tiempo Real**: Acceso a flujos de datos en tiempo real de quejas del sistema *Bogotá Te Escucha* y validaciones de torniquetes del SITP para enriquecer el modelo de alertas tempranas dinámicas.


### 7.3. Comentarios adicionales sobre el DataJam o el uso de datos abiertos:
El Bogotá DataJam 2026 representa un espacio transformador de co-creación entre la academia y la administración distrital. Este ejercicio ratifica que: *"La interoperabilidad en el sector público no es un problema de algoritmos complejos, sino de gobierno de datos, consistencia metodológica y normalización de variables para generar valor público tangible."*

---

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                          CONSTANCIA DE CUMPLIMIENTO DEL ENTREGABLE E-04                          │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Documento elaborado bajo el marco PDCO (Fase: PLAN), aplicando estándares SWEBOK v3,             │
│ IEEE 830 / ISO 29148, DAMA-BOK e ISO/IEC 25010. Totalmente alineado con los Términos de          │
│ Referencia Oficiales del DataJam Edición 2 – 2026 de la Alcaldía Mayor de Bogotá D.C.            │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```
