---
name: statistical-reviewer-rule
description: Regla de oro para revisión cuantitativa y rigor estadístico absoluto en análisis de datos, modelos territoriales, índices sintéticos y visualizaciones.
always_on: true
---

# Regla: Revisor Estadístico Profesional (Statistical Reviewer Rigor Standard)

Cualquier análisis cuantitativo, modelo matemático, índice sintético, contraste de hipótesis o visualización estadística generada en el proyecto debe someterse a este estándar de rigor:

1. **Formulación Matemática en $\LaTeX$**:
   - Cada indicador, sub-índice y función de agregación debe escribirse en notación matemática formal $\LaTeX$ con definición explícita de sus variables, dominios ($[0, 1]$, $[0, 100]$, etc.) y unidades.

2. **Validación de Supuestos Estadísticos**:
   - No asumir normalidad en muestras pequeñas ($N \le 30$) sin contrastes formales (Shapiro-Wilk) o análisis de asimetría/curtosis.
   - En índices territoriales con unidades geográficas de gran disparidad (e.g. Sumapaz vs Bosa), evaluar siempre la compresión de escala Min-Max frente a valores extremos.

3. **Auditoría de Índices Compuestos (Directrices OCDE/JRC)**:
   - Declarar siempre la polaridad de necesidad:
     - **Inversa** ($s_{i, d} = 1 - \hat{x}_{i, d}$) para capacidades, coberturas y dotaciones.
     - **Directa** ($s_{i, d} = \hat{x}_{i, d}$) para riesgos, delitos, pobreza o conflictos.
   - Todo ranking compuesto debe acompañarse de análisis de sensibilidad frente a esquemas alternativos (percentiles, exclusión de proxies, pesos).
   - Los empates deben resolverse mediante reglas determinísticas documentadas.

4. **Honestidad y Rigor Gráfico**:
   - Los ejes cuantitativos en gráficos de barras deben comenzar en $0$.
   - Los gráficos de dispersión deben incluir intervalos de confianza del 95% o líneas de referencia de promedios distritales.
   - Utilizar paletas continuas perceptualmente uniformes (`Blues`, `Viridis`, `Mako`, `Rocket`).

5. **Acompañar siempre Tendencia Central con Dispersión**:
   - Para distribuciones simétricas: Media ($\mu$) $\pm$ Desviación Estándar ($\sigma$).
   - Para distribuciones asimétricas / sesgadas: Mediana $\pm$ Rango Intercuartílico ($\text{IQR} = Q_3 - Q_1$).
