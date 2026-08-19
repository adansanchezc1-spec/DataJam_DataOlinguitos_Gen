# Análisis Exploratorio de Datos (EDA) — Dominios de Expansión Territorial SIPTA

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA — DataJam Bogotá)  
**Fase PDCO**: DEVELOPMENT | **SDLC Stage**: Data Understanding & Exploratory Analysis  
**Estándares**: SWEBOK, DAMA-BOK, ISO/IEC 25010  
**Autores**: Persona A (Adan Sánchez), Persona B (Yesid Bello), Persona C (Sofía Hidalgo)  
**Fecha**: 2026-08-18  

---

## 1. Introducción y Contexto Analítico

El presente informe consolida los hallazgos del **Análisis Exploratorio de Datos (EDA)** desarrollado sobre los dominios recién incorporados al sistema SIPTA. La integración de estas nuevas dimensiones responde a la necesidad de superar los enfoques tradicionales basados únicamente en la presencia física de infraestructura, permitiendo evaluar la **calidad en la prestación de los servicios públicos**, la **capacidad asistencial efectiva**, el **costo en tiempo y segregación espacial del mercado laboral**, la **eficiencia del gasto público local (FDL)** y el **pulso directo de insatisfacción ciudadana (PQR)**.

---

## 2. Hallazgos del Sector Servicios Públicos y Calidad (D11)

### 2.1 Cobertura y Discontinuidad del Suministro Hídrico
- **Promedio Distrital de Cobertura de Acueducto**: 98.4%.
- **Promedio Distrital de Cobertura de Alcantarillado**: 96.8%.
- **Disparidad Extrema**:
  - Mientras localidades como Chapinero (100%), Teusaquillo (100%) y Usaquén (99.8%) gozan de cobertura universal y continuidad ininterrumpida ($< 0.5$ horas de corte mensual), la localidad rural de **Sumapaz (20)** registra una cobertura de acueducto del **82.4%** y de alcantarillado del **68.5%**, abastecida a través de acueductos veredales y comunitarios.
  - En la periferia sur urbana (**Usme**, **Ciudad Bolívar**, **San Cristóbal**), la topografía montañosa y la necesidad de estaciones de bombeo escalonadas generan entre **1.8 y 4.5 horas de interrupción promedio mensual**, incidiendo directamente en la calidad de vida de sus habitantes.

### 2.2 Calidad del Agua Potable (IRCA)
- Las 19 localidades urbanas presentan un **IRCA promedio de 0.85 puntos**, catalogado oficialmente por el SIVICAP como **Sin Riesgo (Apta para Consumo Humano)** ($IRCA < 5.0$).
- La localidad de **Sumapaz registra un IRCA de 6.80 puntos (Riesgo Bajo)**, indicando la necesidad de intervenciones prioritarias en la infraestructura de potabilización y cloración de los acueductos comunitarios veredales.

### 2.3 Alumbrado Público y Brecha de Conectividad TIC
- La modernización hacia tecnología LED en Bogotá alcanza un promedio del **97.2%**, con menores niveles de modernización en Sumapaz (88.5%), Usme (94.2%) y Ciudad Bolívar (94.8%).
- La penetración de **Internet Fijo de Banda Ancha** refleja la más marcada brecha de inequidad digital de la ciudad: **Chapinero (92.4%)**, **Teusaquillo (91.8%)** y **Usaquén (89.5%)** frente a **Usme (41.5%)**, **Ciudad Bolívar (44.8%)** y **Sumapaz (18.2%)**.

---

## 3. Hallazgos de Mercado Laboral, Salarios y Conmutación (D12)

### 3.1 Dependencia y Conmutación Laboral Externa
- Bogotá presenta una marcada **segregación funcional entre zonas residenciales dormitorio y centralidades de empleo**:
  - **Localidades Expulsoras (Alta Dependencia Externa)**:
    - **Usme**: 85.8% de los ocupados conmutan fuera de la localidad (Tiempo medio de viaje: 82.1 min).
    - **Ciudad Bolívar**: 84.5% conmutan a otras localidades (Tiempo medio de viaje: 85.2 min).
    - **Bosa**: 82.4% conmutan a otras localidades (Tiempo medio de viaje: 76.4 min).
    - **San Cristóbal**: 81.2% conmutan a otras localidades (Tiempo medio de viaje: 68.5 min).
  - **Localidades Receptoras / Autosuficientes**:
    - **Chapinero**: 45.2% de ocupados trabajan en la misma localidad (Tiempo medio de viaje: 32.4 min).
    - **Teusaquillo**: 42.1% de autosuficiencia (Tiempo medio de viaje: 30.5 min).
    - **Fontibón**: 38.5% de autosuficiencia debido a zonas francas y polos logísticos (Tiempo medio de viaje: 38.2 min).

### 3.2 Brecha Salarial e Informalidad
- **Disparidad Salarial**: El ingreso laboral promedio en Chapinero (**$4,200,000 COP**) y Usaquén (**$3,650,000 COP**) supera en más de 3 veces al observado en Ciudad Bolívar (**$1,340,000 COP**) y Sumapaz (**$1,280,000 COP**).
- **Correlación Directa con la Informalidad**:
  - Ciudad Bolívar (62.1% de informalidad) y Usme (59.2% de informalidad) presentan los mayores niveles de desprotección social y precarización laboral, mientras que Chapinero registra tan solo 18.2% de informalidad.

---

## 4. Hallazgos de Participación Ciudadana y Alertas Tempranas (D9)

### 4.1 Reclamaciones Ciudadanas (PQR Bogotá Te Escucha)
- Durante el periodo auditado, el sistema procesó **176,650 requerimientos ciudadanos** en las 20 localidades.
- **Puntos Críticos de Demanda**:
  - Mayor volumen bruto: **Suba (19,800 PQR)**, **Kennedy (18,900 PQR)** y **Ciudad Bolívar (16,400 PQR)**.
  - Menor tasa de resolución institucional a tiempo: **Ciudad Bolívar (74.5%)**, **Usme (76.2%)** y **San Cristóbal (79.5%)**, acumulando pasivos de atención ciudadana.
- **Causas Principales de Insatisfacción**:
  - **Malla vial y presencia de huecos**: 65% de las localidades urbanas la señalan como la causa número 1 de quejas.
  - **Aseo, gestión de basuras y puntos críticos de residuos**: Causa número 2 predominante en Kennedy, Bosa y Suba.
  - **Inseguridad y espacio público**: Causa número 3 distrital.

---

## 5. Integración en el Índice de Prioridad Territorial (IPT) Multidimensional

Los resultados de estas dimensiones fueron normalizados (Min-Max $[0, 1]$) e integrados en el cálculo del IPT con las siguientes ponderaciones teóricas sustentadas en el marco conceptual de vulnerabilidad territorial:

| Dimensión Analítica | Código Indicador | Peso Ponderado (%) | Justificación Metodológica |
| :--- | :--- | :---: | :--- |
| **Carencia de Servicios y Continuidad** | `PUB-001` + `PUB-004` | **20%** | Garantía constitucional de acceso a agua potable, saneamiento e inclusión digital. |
| **Vulnerabilidad Laboral e Informalidad** | `EMP-002` | **20%** | Medición directa de la capacidad de generación de ingresos y trampa de pobreza. |
| **Inseguridad y Delitos de Alto Impacto**| `SEG-002` | **15%** | Preservación de la vida e integridad física comunitaria. |
| **Dependencia y Conmutación Laboral** | `EMP-001` | **15%** | Costo de transporte, pérdida de tiempo productivo y segregación urbana. |
| **Rezago en Calidad Educativa** | `EDU-003` | **10%** | Disparidad en pruebas Saber 11 y riesgo de deserción escolar temprana. |
| **Déficit de Capacidad Asistencial** | `SAL-002` | **10%** | Insuficiencia de camas hospitalarias por habitante ante emergencias. |
| **Alertas Ciudadanas (PQR sin resolver)**| `PAR-001` | **10%** | Barómetro ciudadano en tiempo real de fallas operativas en el territorio. |
| **TOTAL** | - | **100%** | **Índice Compuesto SIPTA** |

---

## 6. Conclusiones y Recomendaciones para la Toma de Decisiones

1. **Intervención Prioritaria en el Eje Sur (Ciudad Bolívar, Sumapaz, Usme, Bosa)**:
   - Este grupo de localidades presenta una convergencia crítica de alta informalidad (> 52%), conmutación laboral agobiante (> 75 min de viaje), brecha digital y rezago en resolución de PQR.
2. **Descentralización del Empleo y Equipamientos Productivos**:
   - Para mitigar la conmutación masiva hacia el centro ampliado, los Fondos de Desarrollo Local (FDL) deben focalizar inversión en distritos de desarrollo económico local y centros de formación técnica vinculados a la SED.
3. **Monitoreo Continuo de Alertas Tempranas**:
   - El cruce entre peticiones PQR por malla vial y retrasos en la ejecución de presupuestos locales constituye un sensor preventivo clave antes de la generación de protestas o bloqueos viales.
