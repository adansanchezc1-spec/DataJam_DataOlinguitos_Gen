SIPTA — Guía de la carpeta src

Propósito
Esta carpeta contiene todo el código fuente del pipeline de datos de SIPTA. Cada subcarpeta cumple una función específica en la cadena de procesamiento, desde la ingesta hasta la generación de indicadores y la evaluación.

Estructura y responsabilidades
- src/ingestion
  - Código para descargar, leer y guardar datasets en data/raw.
  - Registrar metadatos básicos: fuente, fecha, formato y versión.

- src/validation
  - Validaciones de esquema y calidad: columnas esperadas, tipos, nulos, duplicados.
  - Reglas territoriales: localización por localidad y consistencia de identificadores.

- src/cleaning
  - Limpieza de valores, normalización de formatos y corrección de nombres.
  - Conversión de fechas, codificación y limpieza de textos.

- src/integration
  - Unificación de datasets por localidad y creación del modelo territorial maestro.
  - Homologación de identificadores territoriales y carga de geometría.

- src/features
  - Construcción de variables derivadas necesarias para indicadores e índices.
  - Agregaciones por localidad, tasas y razones.

- src/modeling
  - Cálculo de indicadores, índices compuestos e IPM (Índice de Prioridad Territorial).
  - Motor de alertas y reglas de recomendación simplificadas.

- src/evaluation
  - Reglas de evaluación de calidad de datos y resultados.
  - Métricas de validación del pipeline y del modelo de priorización.

- src/visualization
  - Scripts de soporte para exportar resultados y generar gráficos básicos.
  - Preparación de datos para el dashboard.

Convenciones
- Cada script o módulo debe ser reutilizable y no depender de rutas absolutas.
- El código debe guardar salidas en data/processed o data/curated según su etapa.
- Las funciones críticas deben contar con pruebas en tests/.
- No usar notebooks como única versión productiva: los notebooks van en notebooks/ y pueden prototipar, pero el código definitivo debe vivir en src/.

Cómo avanzar
1. Empieza en src/ingestion con funciones que lean y versionen cada dataset.
2. Valida cada dataset en src/validation antes de limpiar.
3. Usa src/integration para crear la tabla maestra de localidades.
4. Construye indicadores en src/modeling y prueba su salida en src/evaluation.
5. Usa src/visualization para preparar los resultados mínimos para el dashboard.

Notas
- Marca claramente las dependencias entre módulos.
- Mantén el pipeline legible y comentado.
- No implementes recomendaciones complejas si no hay datos suficientes; deja reglas simples y trazables.

-- Fin del README de src --
