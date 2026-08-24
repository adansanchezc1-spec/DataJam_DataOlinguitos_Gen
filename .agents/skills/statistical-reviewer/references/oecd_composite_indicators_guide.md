# Guía de Auditoría de Índices Compuestos (OECD / JRC Standard)

**Referencia**: OECD / European Commission JRC *Handbook on Constructing Composite Indicators: Methodology and User Guide*  
**Uso**: Manual de consulta técnica para el Revisor Estadístico Profesional.

---

## Las 10 Etapas de Construcción y Auditoría de la OCDE

```
┌──────────────────────────────────────────────────────────────────┐
│             LAS 10 ETAPAS DE CONSTRUCCIÓN DE ÍNDICES OCDE         │
├──────┬───────────────────────────────┬───────────────────────────┤
│ Paso │ Etapa                         │ Criterio de Auditoría     │
├──────┼───────────────────────────────┼───────────────────────────┤
│ 1    │ Marco Conceptual              │ Claridad del fenómeno     │
│ 2    │ Selección de Indicadores      │ Relevancia y disponibilidad│
│ 3    │ Tratamiento de Datos          │ Missing & Outliers        │
│ 4    │ Análisis Multivariado         │ Correlación, PCA, VIF     │
│ 5    │ Normalización                 │ Min-Max, Z, Percentiles   │
│ 6    │ Ponderación                   │ AHP, Pesos iguales, PCA   │
│ 7    │ Agregación                    │ Lineal vs Geométrica      │
│ 8    │ Sensibilidad e Incertidumbre  │ Sobol, Monte Carlo        │
│ 9    │ Vínculo con Otros Indicadores │ Validez de constructo     │
│ 10   │ Visualización y Comunicación  │ Honestidad gráfica Tufte   │
└──────┴───────────────────────────────┴───────────────────────────┘
```

---

## 1. Esquemas de Normalización y Comportamiento Matemático

### A. Estandarización Min-Max
$$\hat{x}_{i, j} = \frac{x_{i, j} - \min(X_j)}{\max(X_j) - \min(X_j)} \in [0, 1]$$
- **Ventaja**: Mapeo exacto y acotado al intervalo unitario.
- **Riesgo**: Extremadamente sensible a valores atípicos (*outliers*). Un único valor atípico comprime el 95% de las observaciones en un rango infinitesimal.

### B. Estandarización Z-Score
$$z_{i, j} = \frac{x_{i, j} - \mu_j}{\sigma_j}$$
- **Ventaja**: Centrado en cero y varianza unitaria.
- **Riesgo**: No está acotado; variables con distribuciones asimétricas conservan la asimetría original.

### C. Normalización por Rangos / Percentiles
$$r_{i, j} = \frac{\text{Rank}(x_{i, j}) - 1}{N - 1} \in [0, 1]$$
- **Ventaja**: Inmune a *outliers*, distribución uniforme garantizada, no paramétrico.
- **Riesgo**: Pierde la información de las distancias cardinales entre observaciones.

---

## 2. Ponderación y Compensabilidad

### A. Ponderaciones Iguales vs Ponderaciones Estadísticas
- Si $w_j = \frac{1}{D}$, se asume implícitamente que todas las dimensiones tienen igual valor intrínseco.
- Si se usa **Análisis de Componentes Principales (PCA)**:
  $$w_j = \sum_{k=1}^K \frac{\lambda_k}{\sum \lambda_m} \cdot \left( \frac{L_{j, k}^2}{\sum_{l} L_{l, k}^2} \right)$$
  donde $\lambda_k$ es el autovalor del componente $k$ y $L_{j, k}$ es la carga factorial.

### B. Efecto de Compensabilidad (Sustituibilidad)
- **Agregación Lineal Aditiva** ($\sum w_j s_j$): Asume **compensabilidad perfecta** (un déficit catastrófico en Salud puede compensarse totalmente con un excelente puntaje en Educación).
- **Agregación Geométrica Multiplicativa** ($\prod s_j^{w_j}$): Penaliza fuertemente el desbalance dimensional y no permite que una localidad con carencia extrema en un derecho fundamental obtenga un puntaje favorable.

---

## 3. Análisis de Incertidumbre y Sensibilidad Global (GSA)

Para auditar la estabilidad del ranking $R_i$:
1. Variar la normalización: $\text{Min-Max} \leftrightarrow \text{Rangos}$.
2. Variar las ponderaciones: $w_j \pm 20\%$ mediante simulación Monte Carlo con distribución Dirichlet.
3. Excluir sistemáticamente un indicador a la vez ($Jackknife$).
4. Evaluar el coeficiente de correlación de Spearman $\rho$ y el promedio de saltos de posición:
   $$\overline{|\Delta R|} = \frac{1}{N} \sum_{i=1}^N |R_{\text{Base}, i} - R_{\text{Sim}, i}|$$
