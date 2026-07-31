SIPTA — Guía sectorial: Participación Ciudadana
Versión: 1.0 | Fecha: 2026-07-31

1. Objetivo sectorial
Incorporar evidencia ciudadana (PQR, reportes, presupuestos participativos) para detectar alertas tempranas y validar prioridades por localidad. ⚠ Pendiente de validar con datos.

2. Pregunta que responde este sector
¿Dónde los reportes ciudadanos y mecanismos participativos (PQR, presupuestos participativos) indican necesidades o deterioro que coinciden con otros indicadores de prioridad?

3. Datos requeridos
Dataset | Fuente esperada | Estado
PQR y reportes ciudadana por localidad | Portal de Participación / Ventanilla Única | por confirmar
Resultados de presupuestos participativos | Secretaría de Participación / portales locales | por confirmar
Encuestas y registros de participación | Encuestas distritales / bases | por confirmar
Geometría de localidades | Portal distrital | por confirmar

4. Indicadores del sector
Código | Indicador | Fórmula | Unidad | Nivel territorial | Fuente esperada
PAR-C1 | Reportes ciudadanos por 10.000 hab | (n_PQR / población) *10000 | reportes / 10000 hab | Localidad | Portal PQR
PAR-C2 | Proyectos aprobados en presupuesto participativo | conteo / inversión asociada | conteo / moneda | Localidad | Secretaría de Participación
PAR-C3 | Coincidencia reporte-indicador | % de reportes que coinciden con indicadores de brecha | % | Localidad | Cruce PQR + indicadores

5. Validaciones pendientes
- Confirmar la existencia y formato de PQR por localidad y su disponibilidad para integrarse. ⚠ Pendiente de validar con datos.
- Evaluar calidad y sesgo de la participación (no todas las localidades generan el mismo volumen de PQRs).

6. Entregable particular del sector
- Tabla con indicadores PAR por localidad, análisis de coincidencias con brechas sectoriales y fichas de casos representativos.
- Relación con E01, E02, E05, E06, E08.

7. Rama Git y documentación asociada
- Rama: feature/participacion-indicadores
- Documentos: README_PARTICIPACION_CIUDADANA.md, scripts de cruces PQR-indicadores, tests/test_participacion.py

8. Checklist de cierre del sector
- [ ] Inventario PQR y participación validado.
- [ ] Indicadores PAR calculados y cruzados con otros sectores.
- [ ] Documentación de sesgos y limitaciones.

-- Fin README Participación Ciudadana --
