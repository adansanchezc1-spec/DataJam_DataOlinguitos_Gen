SIPTA — Guía sectorial: Ambiente
Versión: 1.0 | Fecha: 2026-07-31

1. Objetivo sectorial
Medir calidad ambiental y disponibilidad de espacio público verde por localidad, para incluir riesgo ambiental y acceso a espacios en el IPT. ⚠ Pendiente de validar con datos.

2. Pregunta que responde este sector
¿Qué localidades tienen mayor riesgo ambiental y menor área de espacio público por habitante en relación con la necesidad y la inversión en mitigación?

3. Datos requeridos
Dataset | Fuente esperada | Estado
Áreas de parques y zonas verdes (m2) | Portal distrital / IDE | por confirmar
Datos de calidad del aire y ruido | IDEAM / estaciones locales | por confirmar
Mapas de riesgo (inundación, deslizamiento) | Portal distrital / IDE | por confirmar
Población por localidad | DANE | por confirmar
Inversión en mitigación ambiental | Secretaría de Hacienda / contratos | por confirmar

4. Indicadores del sector
Código | Indicador | Fórmula | Unidad | Nivel territorial | Fuente esperada
AMB-C1 | m2 de espacio público por habitante | m2_parques / población | m2 / hab | Localidad | Catálogo parques
AMB-C2 | Índice de riesgo ambiental compuesto | normalización de capas de riesgo | 0–1 | Localidad | Mapas de riesgo
AMB-C3 | Inversión ambiental per cápita | presupuesto_ambiental / población | moneda / hab | Localidad | Secretaría de Hacienda

5. Validaciones pendientes
- Confirmar cobertura y formato de las geometrías de parques y su superficie. ⚠ Pendiente de validar con datos.
- Verificar frecuencia y cobertura espacial de estaciones de calidad del aire.

6. Entregable particular del sector
- Tabla con m2 por habitante por localidad, índice de riesgo ambiental y mapas de riesgo; fichas técnicas.
- Relación con E01, E02, E05, E06, E08.

7. Rama Git y documentación asociada
- Rama: feature/ambiente-indicadores
- Documentos: README_AMBIENTE.md, scripts de cálculo de áreas, tests/test_ambiente.py

8. Checklist de cierre del sector
- [ ] Inventario de parques y áreas validado.
- [ ] Indicadores AMB-C1..C3 calculados y verificados.
- [ ] Mapas y limitaciones documentadas.

-- Fin README Ambiente --
