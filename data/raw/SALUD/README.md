SIPTA — Guía sectorial: Salud
Versión: 1.0 | Fecha: 2026-07-31

1. Objetivo sectorial
Adaptar el objetivo general de SIPTA al sector Salud: medir capacidad y cobertura sanitaria por localidad para identificar dónde la inversión y la capacidad son insuficientes frente a la necesidad. ⚠ Pendiente de validar con datos.

2. Pregunta que responde este sector
¿En qué localidades la capacidad sanitaria (camas y servicios) y la cobertura son insuficientes en relación con la necesidad poblacional y la inversión ejecutada?

3. Datos requeridos (tabla)
Dataset | Fuente esperada | Estado
Camas por establecimiento (detalle) | Portal de Datos Abiertos del Distrito / Secretaría de Salud | por confirmar
Hospitales y CAPS (ubicación y servicios) | Portal de Datos Abiertos del Distrito | por confirmar
Consultas y atención (serie histórica si existe) | Secretaría de Salud / bases distritales | por confirmar ⚠ Pendiente de validar con datos
Población por localidad | DANE o registro distrital | disponible / por confirmar
Inversión en salud por localidad / contrato | Secretaría de Hacienda / Presupuesto distrital | por confirmar ⚠ Pendiente de validar con datos
Geometría de localidades (polígonos) | Datos abiertos distritales (GeoJSON/shapefile) | por confirmar

4. Indicadores del sector (fichas técnicas — tabla)
Código | Indicador | Fórmula | Unidad | Nivel territorial | Fuente esperada
SAL-C1 | Camas por 10.000 hab | (n_camas / población) * 10000 | camas / 10000 hab | Localidad | Portal de Salud
SAL-C2 | Servicios de urgencias por localidad | conteo de centros con servicio de urgencias | conteo | Localidad | Portal de Salud
SAL-C3 | Cobertura de atención primaria | consultas_atencion_primaria / población | % | Localidad | Portal de Salud
SAL-C4 | Inversión en salud per cápita | presupuesto_ejecutado_salud / población | moneda / hab | Localidad | Secretaría de Hacienda

5. Validaciones pendientes
- Verificar existencia y granularidad de datos de inversión por localidad. ⚠ Pendiente de validar con datos.
- Confirmar si las camas se reportan por establecimiento y si incluyen tipo de servicio (UCI, cirugía, hospitalización). ⚠ Pendiente de validar con datos.
- Confirmar series históricas para construir tendencias o alertas. Si no existen, usar reglas.

6. Entregable particular del sector
- Estructura de salida: tabla de indicadores por localidad (CSV + Parquet), fichas técnicas en formato markdown y un notebook reproducible con EDA y scripts de cálculo.
- Relación con entregables generales: contribuye a E01 (inventario), E02 (diccionario), E05 (indicadores), E06 (índices), E07 (alertas si aplica), E08 (dashboard).

7. Rama Git y documentación asociada
- Rama sugerida: feature/salud-indicadores
- Documentos requeridos: README_SALUD.md (este documento), fichas SAL-*.md, pruebas unitarias para funciones de cálculo en tests/test_salud.py

8. Checklist de cierre del sector (5–8 ítems)
- [ ] Inventario de datasets de salud validado (E01).
- [ ] Diccionario SAL completado (E02).
- [ ] Indicadores SAL-C1..C4 implementados y probados con datos de muestra (E05).
- [ ] Tabla de output por localidad disponible (CSV/Parquet) (E05/E06).
- [ ] Validación de capacidad (camas/cupos) y documento de limitaciones si faltan datos.
- [ ] Notebook EDA y script reproducible en CI.

-- Fin README Salud --
