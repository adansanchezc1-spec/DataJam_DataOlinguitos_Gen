SIPTA — Guía sectorial: Demografía
Versión: 1.0 | Fecha: 2026-08-11

1. Objetivo sectorial
Proveer la base poblacional y la delimitación espacial oficial (geometría) necesaria para construir el modelo territorial unificado y normalizar los indicadores de todos los demás sectores a nivel de localidad. ⚠ Pendiente de validar con datos.

2. Pregunta que responde este sector
¿Cuál es la distribución poblacional (por edad y género) y la delimitación espacial oficial de las localidades de Bogotá para calcular la demanda potencial de servicios y la densidad territorial?

3. Datos requeridos (tabla)
Dataset | Fuente esperada | Estado
Población por localidad (Pirámide) | Portal de Datos Abiertos del Distrito / SDP | descargado (osb_demografia-poblacion-localidad.csv)
Límite de Localidad (Geometría) | Portal de Datos Abiertos del Distrito / IDECA | por confirmar ⚠ Pendiente de validar con datos

4. Indicadores del sector (fichas técnicas — tabla)
Código | Indicador | Fórmula | Unidad | Nivel territorial | Fuente esperada
DEM-001 | Densidad poblacional | Población / area_km2 | hab / km2 | Localidad | SDP / IDECA
*Nota: La demografía actúa principalmente como el denominador (población objetivo) para los indicadores de los sectores de Salud (SAL-002), Educación (EDU-001), Infraestructura (INF-004), y Finanzas (FIN-001).

5. Validaciones pendientes
- Confirmar que el identificador `CODIGO_LOCALIDAD` cruza de forma exacta con los catálogos territoriales de IDECA y de los demás sectores. ⚠ Pendiente de validar con datos.
- Validar la disponibilidad, el sistema de coordenadas (CRS) y el formato del archivo espacial (GeoJSON/Shapefile) de las localidades. ⚠ Pendiente de validar con datos.

6. Entregable particular del sector
- Estructura de salida: Tabla maestra poblacional limpia y archivo geoespacial base procesado.
- Relación con entregables generales: Contribuye directamente a E01 (inventario), E02 (diccionario), y es el pilar absoluto del OE03 (modelo territorial).

7. Rama Git y documentación asociada
- Rama sugerida: feature/demografia-base
- Documentos requeridos: README_DEMOGRAFIA.md (este documento), pruebas de consistencia territorial en tests/test_demografia.py

8. Checklist de cierre del sector (5-8 ítems)
- [x] Inventario de datasets de demografía validado (E01).
- [ ] Diccionario DEM completado (E02).
- [x] Ingesta inicial de la Pirámide Poblacional completada.
- [ ] Geometría de localidades (GeoJSON) descargada y validada (OE03).
- [ ] Limpieza de datos y corrección de codificación (ej. Byte Order Mark) implementadas.
- [ ] Notebook EDA y script reproducible en CI.

-- Fin README Demografía --