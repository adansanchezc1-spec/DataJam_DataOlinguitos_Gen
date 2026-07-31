SIPTA — Guía sectorial: Educación
Versión: 1.0 | Fecha: 2026-07-31

1. Objetivo sectorial
Medir la capacidad educativa por localidad (cupos y matrícula) y detectar brechas entre oferta y demanda para guiar priorización de inversión y expansión de cupos. ⚠ Pendiente de validar con datos.

2. Pregunta que responde este sector
¿En qué localidades la oferta educativa (cupos) es insuficiente respecto a la población en edad escolar y la inversión realizada?

3. Datos requeridos
Dataset | Fuente esperada | Estado
Colegios (ubicación y tipo) | Portal de Datos Abiertos / Secretaría de Educación | por confirmar
Cupos por institución | Secretaría de Educación / NIT de colegios | por confirmar ⚠ Pendiente de validar con datos
Matrícula por edad y localidad | DANE / Secretaría de Educación | por confirmar
Inversión en infraestructura educativa | Secretaría de Hacienda / contratos | por confirmar ⚠ Pendiente de validar con datos
Geometría de localidades | Datos abiertos distritales | por confirmar

4. Indicadores del sector (ficha técnica)
Código | Indicador | Fórmula | Unidad | Nivel territorial | Fuente esperada
EDU-C1 | Cupos por 1.000 niños en edad escolar | (n_cupos / población_edad_escolar) * 1000 | cupos / 1000 niños | Localidad | Secretaría de Educación
EDU-C2 | Tasa de cobertura escolar | matrícula / población_edad_escolar | % | Localidad | Secretaría de Educación
EDU-C3 | Inversión por cupo | presupuesto_infra_educativa / n_cupos | moneda / cupo | Localidad | Secretaría de Hacienda

5. Validaciones pendientes
- Confirmar disponibilidad de cupos por institución y su granularidad. ⚠ Pendiente de validar con datos.
- Confirmar si inversión está desagregada por proyecto y localidad.

6. Entregable particular del sector
- CSV/Parquet con indicadores por localidad, fichas técnicas de indicadores y un informe corto (markdown) con priorización preliminar para las localidades con mayor brecha.
- Relación con entregables generales: E01, E02, E05, E06, E08.

7. Rama Git y documentación asociada
- Rama: feature/educacion-indicadores
- Documentos: README_EDUCACION.md, fichas EDU-*.md, tests/test_educacion.py

8. Checklist de cierre del sector
- [ ] Inventario de datos educativos completado.
- [ ] Diccionario EDU con cupos y matrícula.
- [ ] Indicadores implementados y validados con datos de muestra.
- [ ] Output por localidad listo para integrar en índices.
- [ ] Nota de limitaciones sobre datos faltantes.

-- Fin README Educación --
