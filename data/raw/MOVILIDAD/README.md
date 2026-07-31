SIPTA — Guía sectorial: Movilidad
Versión: 1.0 | Fecha: 2026-07-31

1. Objetivo sectorial
Medir accesibilidad y tiempos de viaje por localidad para identificar dónde la conectividad limita el acceso a servicios y oportunidades. ⚠ Pendiente de validar con datos.

2. Pregunta que responde este sector
¿Qué localidades muestran mayores tiempos promedio de viaje y peor conectividad en relación con la necesidad de acceso a servicios básicos?

3. Datos requeridos
Dataset | Fuente esperada | Estado
Tiempos de viaje promedio por trayecto o por red | Encuestas de movilidad / datos de operadores / GTFS | por confirmar
Redes de transporte (estaciones, rutas) | Portal de datos distritales / SITP / operadores | por confirmar
Paraderos, ciclorrutas y micromovilidad | Portal distrital | por confirmar
Población y localización de servicios | DANE / inventario de equipamientos | por confirmar
Geometría de localidades | Portal de datos | por confirmar

4. Indicadores del sector
Código | Indicador | Fórmula | Unidad | Nivel territorial | Fuente esperada
MOV-C1 | Tiempo promedio de viaje al servicio esencial | promedio(tiempo_a_servicio) | minutos | Localidad | Encuesta/GTFS
MOV-C2 | Índice de conectividad | función agregada de cobertura de rutas y acceso a estaciones | índice 0–1 | Localidad | Datos SITP
MOV-C3 | Porcentaje de población >30min a servicios críticos | (pob_en_tiempo>30 / pob_total) *100 | % | Localidad | Modelación con redes

5. Validaciones pendientes
- Confirmar disponibilidad de datos de tiempos de viaje y cobertura de GTFS o datos operadores. ⚠ Pendiente de validar con datos.
- Si no hay series, proponer métricas estáticas y reglas de priorización.

6. Entregable particular del sector
- Outputs: tablas de tiempos y conectividad por localidad, mapas de isócronas (si hay datos) y fichas de indicadores.
- Relación con E01, E02, E05, E06, E08.

7. Rama Git y documentación asociada
- Rama: feature/movilidad-indicadores
- Documentos: README_MOVILIDAD.md, scripts de modelación de redes, tests/test_movilidad.py

8. Checklist de cierre del sector
- [ ] Inventario de datos de movilidad validado.
- [ ] Indicadores MOV-C1..C3 calculables con datos de muestra.
- [ ] Mapas y tablas integradas al dataset curado.
- [ ] Limitaciones documentadas.

-- Fin README Movilidad --
