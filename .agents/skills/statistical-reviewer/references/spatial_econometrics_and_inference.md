# Guía de Econometría Espacial, Inferencia y Control de Sesgos

**Uso**: Manual de referencia técnica para el Revisor Estadístico Profesional.

---

## 1. Dependencia Espacial y Matrices de Ponderación Espacial ($W$)

Toda unidad territorial $i$ está influenciada por sus vecinas $j$ (Primera Ley de la Geografía de Tobler: *"Todo está relacionado con todo lo demás, pero las cosas cercanas están más relacionadas que las distantes"*).

### A. Construcción de la Matriz $W$
- **Contigüidad Reina (Queen)**: $w_{ij} = 1$ si las localidades $i$ y $j$ comparten al menos un punto fronterizo común.
- **Estandarización por Filas**:
  $$w_{ij}^* = \frac{w_{ij}}{\sum_{k=1}^N w_{ik}}, \quad \sum_{j=1}^N w_{ij}^* = 1$$

### B. Índices de Autocorrelación Espacial
- **Índice de Moran Global ($I$)**:
  $$I = \frac{N}{\sum_{i} \sum_{j} w_{ij}} \frac{\sum_{i=1}^N \sum_{j=1}^N w_{ij} (x_i - \bar{x})(x_j - \bar{x})}{\sum_{i=1}^N (x_i - \bar{x})^2}$$
  - $p\text{-valor}$ obtenido por permutación Monte Carlo ($999$ iteraciones).
- **LISA (Local Indicators of Spatial Association)**:
  $$I_i = \frac{x_i - \bar{x}}{m_2} \sum_{j=1}^N w_{ij} (x_j - \bar{x}), \quad m_2 = \frac{\sum_i (x_i - \bar{x})^2}{N}$$
  - Identifica cuadrantes: **Alto-Alto** (Hotspots de vulnerabilidad), **Bajo-Bajo** (Coldspots), **Alto-Bajo** y **Bajo-Alto** (Outliers espaciales).

---

## 2. Detección de Falacias y Antipatrones Estadísticos

### A. Falacia Ecológica vs. Falacia Atomística
- **Falacia Ecológica**: Inferir relaciones a nivel de individuos a partir de datos agregados por localidad (e.g. correlacionar tasa de desempleo local con delincuencia y concluir que los desempleados cometen delitos).
- **Falacia Atomística**: Generalizar un comportamiento macro a partir de observaciones individuales sin considerar la estructura contextual.

### B. Efecto MAUP (*Modifiable Areal Unit Problem*)
- **Efecto de Escala**: La agregación de datos puntuales a UPZ vs Localidades altera la magnitud de las correlaciones y la varianza observada.
- **Efecto de Zonificación**: Cambiar los límites geográficos de las unidades manteniendo la misma escala puede revertir signos de correlación.

### C. Sesgo de Denominadores Pequeños (*Small Numbers Problem*)
- En unidades territoriales de muy baja población ($N < 10.000$ habitantes como Sumapaz o La Candelaria), un único evento adicional genera picos artificiales en tasas por 100k habitantes.
- **Solución Recomendada**: Estimador Bayesiano Empírico (*Empirical Bayes Smoothed Rates*) o contrastes no paramétricos de robustez.
