# Casos de Uso del Sistema SIPTA

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas  
**Fase PDCO**: PLAN | **Estándar**: IEEE 830  

---

### UC-001: Ingesta Reproducible de Datasets Sectoriales
- **Actor Principal**: Data Engineer / Persona A
- **Precondición**: Archivos crudos descargados en `data/raw/` en formatos soportados.
- **Flujo Principal**:
  1. El sistema lee el dataset crudo identificando codificación y delimitador automáticamente.
  2. Extrae dimensiones, nombres de columnas y tipos de datos.
  3. Registra el archivo procesado en `data/processed/` y emite log en `ingestion_manifest.json`.
- **Postcondición**: Dataset disponible en memoria para auditoría de calidad.

---

### UC-002: Auditoría y Validación de Calidad ISO 25010
- **Actor Principal**: QA Specialist / Lead Data Engineer
- **Precondición**: Dataset ingestor cargado.
- **Flujo Principal**:
  1. El sistema audita la completitud calculando el ratio de valores nulos por columna.
  2. Evalúa la presencia de filas duplicadas y consistencia de tipos.
  3. Valida la llave foránea territorial contra la lista canónica de 20 localidades.
  4. Exporta el reporte técnico a `reports/validation/dominios/val_<dominio>.json`.
- **Postcondición**: Dictamen de calidad emitido (`APROBADO` / `RECHAZADO`).

---

### UC-003: Cálculo del Índice de Prioridad Territorial (IPT)
- **Actor Principal**: Data Scientist / Persona B
- **Precondición**: Matriz consolidada de 20 localidades construida con métricas de los 13 dominios.
- **Flujo Principal**:
  1. El sistema aplica normalización Min-Max [0, 1] a cada métrica sectorial.
  2. Invierte la polaridad en indicadores donde menor valor representa mayor carencia.
  3. Pondera las 7 dimensiones teóricas y genera el puntaje compuesto IPT (0 a 100).
  4. Asigna el ranking territorial (1 a 20) y clasifica en niveles de prioridad (Crítica, Alta, Moderada, Baja).
- **Postcondición**: Matriz `data/processed/matriz_indicadores_ipt_multidimensional.csv` persistida.
