# SIPTA — Matriz de trazabilidad analítica

## 1. Propósito

La matriz de trazabilidad analítica garantiza que cada análisis realizado en
SIPTA responda a una necesidad de política pública y pueda rastrearse desde el
problema identificado hasta la decisión que pretende apoyar.

Su función es evitar la construcción de indicadores, visualizaciones o
recomendaciones aisladas que no tengan una relación explícita con una pregunta
estratégica y con evidencia proveniente de los datos.

---

## 2. Cadena de trazabilidad

La lógica definida para SIPTA es:

`Problema público → Pregunta estratégica → Objetivo analítico → Datasets → Variables → Indicadores → Índices → Visualización → Recomendación → Decisión pública`

Cada elemento deberá conservar relación explícita con el anterior.

---

## 3. Componentes

### Problema público

Situación territorial que requiere comprensión, seguimiento o intervención.

### Pregunta estratégica

Pregunta que transforma el problema público en una necesidad concreta de
análisis.

### Objetivo analítico

Resultado específico que se busca obtener mediante el análisis de los datos.

### Datasets

Fuentes de información utilizadas para responder la pregunta estratégica.

### Variables

Campos concretos requeridos de los datasets seleccionados.

### Indicadores

Medidas calculadas a partir de las variables para representar el fenómeno
analizado.

### Índices

Medidas compuestas que permiten sintetizar varios indicadores cuando el
problema lo requiera.

### Visualización

Representación utilizada para comunicar el resultado analítico.

### Recomendación

Acción sugerida a partir de la evidencia obtenida.

### Decisión pública

Decisión de planeación, inversión, intervención o seguimiento que puede ser
soportada por el análisis.

---

## 4. Matriz base definida para SIPTA

Los siguientes casos corresponden a los ejemplos definidos para la matriz de
trazabilidad del proyecto.

| Problema público | Pregunta estratégica | Indicador | Índice / dimensión | Decisión pública |
|---|---|---|---|---|
| Acceso desigual a salud | ¿Qué localidades tienen menor acceso relativo? | Hospitales por 10.000 habitantes | Cobertura en salud | Priorizar infraestructura sanitaria |
| Déficit educativo | ¿Dónde hay mayores brechas educativas? | Cobertura educativa | Índice educativo | Ampliar cupos o colegios |
| Baja cobertura de parques | ¿Qué zonas tienen menor espacio público? | m² por habitante | Espacio público | Priorizar parques y mantenimiento |
| Baja accesibilidad | ¿Qué territorios tienen mayores tiempos? | Tiempo promedio | Accesibilidad | Mejorar conectividad |
| Inversión insuficiente | ¿La inversión coincide con la necesidad? | Inversión per cápita | Equidad territorial | Redistribuir o focalizar recursos |
| Infraestructura deteriorada | ¿Dónde se requiere mantenimiento preventivo? | % deterioro | Riesgo territorial | Plan preventivo de mantenimiento |

> Esta tabla conserva los ejemplos establecidos en la planificación del
> proyecto. Los componentes que aún no se encuentran especificados no deben
> completarse mediante supuestos.

---

## 5. Matriz completa de trazabilidad

La implementación definitiva deberá documentar cada análisis mediante la
siguiente estructura:

| Campo | Descripción |
|---|---|
| `problema_publico` | Problema territorial que motiva el análisis |
| `pregunta_estrategica` | Pregunta que se busca responder |
| `objetivo_analitico` | Resultado analítico esperado |
| `datasets` | Fuentes utilizadas |
| `variables` | Variables requeridas |
| `indicadores` | Indicadores calculados |
| `indices` | Índices o dimensiones asociadas |
| `visualizacion` | Representación utilizada |
| `recomendacion` | Acción propuesta a partir de los resultados |
| `decision_publica` | Decisión que el análisis busca apoyar |
| `indicador_seguimiento` | Indicador utilizado para evaluar posteriormente la decisión |

---

## 6. Matriz de Aplicación Consolidada

| Problema público | Pregunta estratégica | Objetivo analítico | Datasets | Variables | Indicador | Índice | Visualización | Recomendación | Decisión pública | Indicador de seguimiento |
|---|---|---|---|---|---|---|---|---|---|---|
| Capacidad sanitaria desigual | ¿Qué localidades tienen menor dotación de camas hospitalarias por habitante? | Medir la disponibilidad de camas por cada 10.000 habitantes | `SALUD/osb_tiporazoncamas.csv`, `DEMOGRAFIA/osb_demografia-poblacion-localidad.csv` | `camas_totales`, `poblacion` | `SAL-002`: Camas por 10.000 hab. | D1 Salud | Mapa de calor + Radar | Fortalecer y expandir la red de CAPS e infraestructura hospitalaria intermedia | Asignar recursos para ampliación de capacidad hospitalaria distrital | `SAL-002` interanual |
| Déficit de oferta educativa oficial | ¿Dónde existe menor disponibilidad de cupos escolares respecto a la población infantil y juvenil? | Calcular la tasa de cupos escolares por cada 1.000 personas en edad escolar | `EDUCACION/ofertacupos_032025.geojson`, `DEMOGRAFIA/osb_demografia-poblacion-localidad.csv` | `cupos_ofertados`, `poblacion_5_17_anos` | `EDU-001`: Cupos por 1.000 hab. en edad escolar | D2 Educación | Barras ordenadas por localidad + Mapa | Focalizar ampliación de cobertura y convenios de infraestructura educativa | Priorizar construcción o ampliación de colegios distritales | Tasa de cobertura neta (`EDU-003`) |
| Inaccesibilidad a transporte público masivo | ¿Qué localidades presentan menor densidad de estaciones y paraderos SITP por km²? | Evaluar la cobertura física y accesibilidad al sistema troncal y zonal | `MOVILIDAD/estaciones_troncales.geojson`, `MOVILIDAD/paraderos_zonales_sitp.gpkg`, `dim_territorio.csv` | `estaciones_count`, `paraderos_count`, `area_km2` | `MOV-002`: Densidad de puntos de acceso SITP/km² | D3 Movilidad | Mapa de isócronas y puntos de acceso | Reconfigurar rutas zonales y construir nuevas paradas de integración | Reestructurar malla de rutas zonales y alimentadoras | Tiempo promedio de viaje (`MOV-001`) |
| Déficit de espacio público y recreación | ¿Qué zonas urbanas tienen menor área verde y parques por habitante? | Determinar los m² de parques efectivos por habitante según estándar OMS/POT | `INFRAESTRUCTURA_ESPACIO_PUBLICO/5.-parques-idrd.csv`, `DEMOGRAFIA/osb_demografia-poblacion-localidad.csv` | `area_parque_m2`, `poblacion` | `INF-004`: m² de espacio público por habitante | D4 Infraestructura | Mapa coroplético por cuartiles | Priorizar intervención en parques vecinales y cesiones públicas | Ejecutar planes de adquisición y adecuación de espacio público | m² habilitados por año |
| Conflictividad ambiental y calidad del aire | ¿Qué localidades concentran mayores situaciones ambientales conflictivas y estaciones críticas de RMCAB? | Cuantificar el número de SAC y nivel de exposición por localidad | `AMBIENTE/situacion_ambiental_conflictiva.geojson`, `AMBIENTE/estacion_calidad_aire.geojson` | `codigo_sac`, `grupo_sac`, `cod_locali` | `AMB-001`: Densidad de conflictos ambientales/km² | D5 Ambiente | Mapa de calor de eventos SAC | Implementar operativos de control de emisiones y gestión comunitaria de residuos | Planes de choque de descontaminación y control ambiental | Reducción en reporte de SACs |
| Vulnerabilidad económica y comercio informal | ¿En qué localidades se concentra la población vendedora informal sin infraestructura de apoyo? | Medir la intensidad de vendedores informales por cada 10.000 habitantes | `FINANZAS/vendedores_informales_consolidado.csv`, `FINANZAS/Punto de encuentro vendedores.xlsx`, `DEMOGRAFIA/osb_demografia-poblacion-localidad.csv` | `numero_vendedores`, `puntos_encuentro_count`, `poblacion` | `FIN-003`: Vendedores informales por 10.000 hab. | D6 Finanzas / Equidad | Gráfico de dispersión (Vendedores vs. Puntos IPES) | Habilitar nuevos puntos de encuentro fijos y microcréditos productivos | Construir ferias institucionales y centros de formalización comercial | Tasa de formalización y uso de puntos IPES |
| Presencia y cobertura de seguridad preventiva | ¿Qué localidades cuentan con menor cantidad de cuadrantes de vigilancia por habitante? | Evaluar la ratio de cuadrantes policiales por cada 10.000 habitantes | `SEGURIDAD/Cuadrante de Policía. Bogotá D.C.csv`, `DEMOGRAFIA/osb_demografia-poblacion-localidad.csv` | `cuadrantes_count`, `poblacion` | `SEG-001`: Cuadrantes por 10.000 habitantes | D7 Seguridad | Mapa territorial de cobertura policial | Reasignar cuadrantes y fortalecer equipamientos de vigilancia comunitaria | Redistribuir pie de fuerza y cámaras de videovigilancia | Tasa de respuesta policial a cuadrantes |
| Desbalance entre necesidad e inversión pública | ¿En qué localidades la vulnerabilidad multidimensional no se corresponde con los recursos invertidos? | Integrar el IPT multidimensional y contrastarlo con la inversión ejecutada | `data/curated/master_localidades.csv`, `EDUCACION/inversion_educacion_por_localidad_12_2025.gpkg` | `ipt_score`, `inversion_per_capita` | `IPT-001`: Índice de Prioridad Territorial (0–100) | IPT General | Cuadrante de Priorización (Necesidad vs. Inversión) | Redireccionar partidas presupuestales a las localidades en cuadrante crítico | Rebalanceo presupuestal en el Plan de Desarrollo Distrital | Variación del IPT en el siguiente cuatrienio |

---

## 7. Reglas de uso

### Regla 1 — Pregunta antes que visualización

Ningún gráfico se construye sin una pregunta estratégica.

Una visualización debe existir para comunicar una respuesta analítica y no
solamente porque una variable pueda graficarse.

---

### Regla 2 — Indicadores documentados

Ningún indicador se acepta sin:

- fórmula;
- fuente;
- interpretación.

La definición detallada de estos elementos se realizará en el
**Inventario Maestro de Indicadores y fichas técnicas**.

---

### Regla 3 — Recomendaciones con evidencia

Ninguna recomendación se presenta sin:

- evidencia proveniente de datos;
- relación con uno o más indicadores;
- entidad o actor responsable cuando corresponda.

---

### Regla 4 — Seguimiento de decisiones

Toda decisión pública debe conectarse con al menos un indicador que permita
evaluar posteriormente su comportamiento o impacto.

---

## 8. Relación con el inventario maestro de indicadores

La matriz de trazabilidad define **por qué** se necesita un indicador.

El Inventario Maestro de Indicadores definirá posteriormente **cómo** se
construye.

La relación conceptual es:

`Problema → Pregunta → Indicador necesario`

y posteriormente:

`Indicador → Variables → Fórmula → Fuente → Unidad → Interpretación`

Por esta razón, la matriz de trazabilidad debe preceder a la formalización
definitiva del inventario de indicadores.

---

## 9. Relación con los dominios

La matriz puede requerir información procedente de más de un dominio.

Ejemplo conceptual:

`Cobertura sanitaria`

puede requerir:

`Salud + Demografía`

mientras que:

`Inversión per cápita`

puede requerir:

`Finanzas públicas + Demografía`

Esto no implica que un responsable deba repetir la validación de los dominios
de otro integrante.

Los resultados validados de cada dominio serán consumidos posteriormente por
la capa analítica común.

---

## 10. Trazabilidad mínima requerida

Para considerar un análisis completamente trazable deberán conocerse como
mínimo:

1. problema público;
2. pregunta estratégica;
3. objetivo analítico;
4. datasets utilizados;
5. variables utilizadas;
6. indicador y su fórmula;
7. fuente de los datos;
8. interpretación del resultado;
9. producto o visualización;
10. recomendación;
11. decisión pública que apoya;
12. indicador de seguimiento.

---

---

## 11. Estado actual y Cadena de Trazabilidad Expandida (12 Dominios)

- Lógica de trazabilidad: **Completada y formalizada bajo normas DAMA-BOK / ISO 25010.**
- Problemas públicos priorizados: **12 problemas sectoriales formalizados**, incorporando:
  - Discontinuidad hídrica y brecha digital (`SERVICIOS_PUBLICOS`).
  - Segregación espacial y conmutación laboral agobiante (`EMPLEO_ECONOMIA`).
  - Puntos críticos de insatisfacción y quejas ciudadanas (`PARTICIPACION_CIUDADANA`).
  - Desbalance y rezago en ejecución de presupuestos locales (`FINANZAS_INVERSION_PUBLICA`).
- Preguntas estratégicas operativas: **Definidas para los 12 dominios temáticos.**
- Indicadores base e IPT Multidimensional: **Fórmulas y variables de entrada asociadas a 25 datasets reales en las 20 localidades.**
- Dimensiones del IPT Multidimensional: **Salud (D2), Educación (D3), Movilidad (D4), Infraestructura (D5), Ambiente (D6), Finanzas y FDL (D7), Seguridad (D8), Participación (D9), Servicios Públicos (D11), Empleo y Salarios (D12).**
- Decisiones públicas e indicadores de seguimiento: **Formalizados en la Matriz de Aplicación y tableros analíticos.**
- Implementación en pipeline: **Módulos `src/validation/`, `src/modeling/` y `notebooks/01_ingestion/` 100% integrados y verificados con 72 pruebas unitarias.**