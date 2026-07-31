SIPTA — Guía sectorial: Infraestructura y Espacio Público
Versión: 1.0 | Fecha: 2026-07-31

1. Objetivo sectorial
Evaluar estado físico, capacidad y cobertura del equipamiento urbano por localidad para priorizar mantenimiento y nuevas inversiones. ⚠ Pendiente de validar con datos.

2. Pregunta que responde este sector
¿Qué localidades presentan mayor déficit de equipamientos (por capacidad y estado) y requieren intervención preventiva o inversión?

3. Datos requeridos
Dataset | Fuente esperada | Estado
Inventario de equipamientos (tipo, capacidad, estado) | Portal distrital / dependencia sectorial | por confirmar
Registro de PQR y obras | Secretaría de Infraestructura / PQR | por confirmar
Superficie de espacio público (m2) | IDE / catastro | por confirmar
Inversión en obras y mantenimiento por localidad | Secretaría de Hacienda | por confirmar
Geometría de localidades | Portal distrital | por confirmar

4. Indicadores del sector
Código | Indicador | Fórmula | Unidad | Nivel territorial | Fuente esperada
INF-C1 | Equipamientos por 10.000 hab (ajustado por capacidad) | sum(capacidad_equipamientos) / población *10000 | capacidad / 10000 hab | Localidad | Inventario equipamientos
INF-C2 | % de equipamientos en estado crítico | (n_criticos / n_total) *100 | % | Localidad | Inventario / PQR
INF-C3 | Mantenimiento pendiente per cápita (estimado) | costo_estimado_mantenimiento / población | moneda / hab | Localidad | PQR / obras

5. Validaciones pendientes
- Verificar que el inventario incluya capacidad (no solo conteo) y codificación de estado. ⚠ Pendiente de validar con datos.
- Confirmar que PQRs puedan agregarse por localidad.

6. Entregable particular del sector
- Tabla de riesgo-infraestructura por localidad, lista priorizada de mantenimientos sugeridos (con estimación de costo) y fichas técnicas.
- Relación con E01, E02, E05, E06, E08.

7. Rama Git y documentación asociada
- Rama: feature/infraestructura-indicadores
- Documentos: README_INFRAESTRUCTURA_ESPACIO_PUBLICO.md, scripts de agregación de PQR, tests/test_infraestructura.py

8. Checklist de cierre del sector
- [ ] Inventario de equipamientos con capacidad validado.
- [ ] Indicadores INF-C1..C3 calculados y probados.
- [ ] Estimaciones de mantenimiento documentadas.

-- Fin README Infraestructura y Espacio Público --
