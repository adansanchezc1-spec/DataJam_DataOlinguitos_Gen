SIPTA — Guía sectorial: Seguridad
Versión: 1.0 | Fecha: 2026-07-31

1. Objetivo sectorial
Incluir la dimensión de seguridad en el IPT: medir vulnerabilidad territorial ligada a delitos, emergencias y percepción, por localidad. ⚠ Pendiente de validar con datos.

2. Pregunta que responde este sector
¿Qué localidades muestran mayor vulnerabilidad por seguridad (incidencia de delitos, emergencias y percepción) en relación con inversión y capacidad institucional?

3. Datos requeridos
Dataset | Fuente esperada | Estado
Registro de delitos por localidad | Secretaría de Seguridad / Policía / Observatorio | por confirmar
Emergencias y reportes | Bomberos / emergencias distritales | por confirmar
Encuestas de percepción o PQRs relevantes | Encuestas distritales / participación ciudadana | por confirmar
Población por localidad | DANE | por confirmar

4. Indicadores del sector
Código | Indicador | Fórmula | Unidad | Nivel territorial | Fuente esperada
SEG-C1 | Incidencia de delitos por 10.000 hab | (n_delitos / población) *10000 | delitos / 10000 hab | Localidad | Secretaría de Seguridad
SEG-C2 | Reportes de emergencias por 10.000 hab | (n_emergencias / población) *10000 | reportes / 10000 hab | Localidad | Registros emergencias
SEG-C3 | Índice de percepción de inseguridad | encuesta agregada | 0–1 | Localidad | Encuestas / PQR

5. Validaciones pendientes
- Verificar precisión espacial de registros de delito y posibilidad de agregación por localidad. ⚠ Pendiente de validar con datos.
- Confirmar acceso a encuestas o PQR que permitan medir percepción.

6. Entregable particular del sector
- Tabla de indicadores SEG por localidad, mapas de incidencia y nota metodológica sobre limitaciones en datos de seguridad.
- Relación con E01, E02, E05, E06, E08.

7. Rama Git y documentación asociada
- Rama: feature/seguridad-indicadores
- Documentos: README_SEGURIDAD.md, scripts de agregación de delitos, tests/test_seguridad.py

8. Checklist de cierre del sector
- [ ] Inventario de delitos y emergencias validado.
- [ ] Indicadores calculados y verificados.
- [ ] Limitaciones y recomendaciones documentadas.

-- Fin README Seguridad --
