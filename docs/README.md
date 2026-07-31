SIPTA — Guía de documentación

Propósito
Esta carpeta agrupa la documentación oficial del proyecto, con énfasis en trazabilidad, reproducibilidad y claridad para usuarios no técnicos.

Documentos esperados
- docs/manual_tecnico.md
  - Arquitectura del pipeline.
  - Estructura de carpetas.
  - Requisitos de software y ejecución.
  - Descripción de cada módulo en src/.

- docs/manual_usuario.md
  - Cómo interpretar el dashboard.
  - Qué indicadores y gráficas mirar.
  - Qué significa cada dimensión del IPT.

- docs/diccionario_datos.md
  - Lista de variables.
  - Nombre, tipo, unidad, descripción, fuente.
  - Reglas de transformación.

- docs/bitacora_decisiones.md
  - Cambios metodológicos.
  - Justificación de decisiones clave.
  - Fecha y autor de cada cambio.

- docs/registro_cambios.md
  - Versiones del proyecto.
  - Mejora y corrección.

- docs/arquitectura.md
  - Diagramas de flujo del pipeline.
  - Zonas raw/processed/curated.
  - Modelo territorial y conexiones.

- docs/crispdm_report.md
  - Resumen de cada fase CRISP-DM.
  - Hallazgos y resultados.

Plantillas recomendadas
- Mantener cada documento corto y directo.
- Usar secciones claras y tablas cuando haya datos estructurados.
- Incluir siempre una sección de "Limitaciones".
- Marcar con "⚠ Pendiente de validar con datos" cualquier asunción que dependa de datos no confirmados.

Instrucciones rápidas
1. Antes de escribir un documento, crea el archivo con el nombre sugerido.
2. Añade un índice básico con encabezados.
3. Completa las tablas de variables o entregables según el contenido.
4. Actualiza el README raíz con nuevos documentos si se agrega alguno.

Estructura de carpetas
- docs/
  - README.md (este documento)
  - manual_tecnico.md
  - manual_usuario.md
  - diccionario_datos.md
  - bitacora_decisiones.md
  - registro_cambios.md
  - arquitectura.md
  - crispdm_report.md

-- Fin del README de docs --
