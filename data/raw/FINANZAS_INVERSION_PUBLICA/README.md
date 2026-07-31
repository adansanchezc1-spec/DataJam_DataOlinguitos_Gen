SIPTA — Guía sectorial: Finanzas e Inversión Pública
Versión: 1.0 | Fecha: 2026-07-31

1. Objetivo sectorial
Medir la inversión pública ejecutada por localidad y compararla con la necesidad estimada para identificar desvíos y brechas de equidad. ⚠ Pendiente de validar con datos.

2. Pregunta que responde este sector
¿La inversión pública ejecutada por localidad coincide con las necesidades detectadas y cuáles son las localidades subfinanciadas en relación con la prioridad territorial?

3. Datos requeridos
Dataset | Fuente esperada | Estado
Presupuesto y ejecución por proyecto / obra | Secretaría de Hacienda / Portal de Transparencia | por confirmar ⚠ Pendiente de validar con datos
Contratos y montos por localidad | Plataforma de contratación pública / distrital | por confirmar
Asignación de inversión sectorial (salud, educación, etc.) | Secretaría de Hacienda | por confirmar
Población por localidad | DANE | por confirmar
Geometría de localidades | Portal distrital | por confirmar

4. Indicadores del sector
Código | Indicador | Fórmula | Unidad | Nivel territorial | Fuente esperada
FIN-C1 | Inversión per cápita | presupuesto_ejecutado / población | moneda / hab | Localidad | Secretaría de Hacienda
FIN-C2 | % ejecución presupuestal | ejecutado / aprobado *100 | % | Localidad / proyecto | Secretaría de Hacienda
FIN-C3 | Desbalance inversión-necesidad | inversión_perc - necesidad_perc | puntos porcentuales | Localidad | Agregación sectorial

5. Validaciones pendientes
- Confirmar si la información de ejecución está georreferenciada o asociable a localidades (proyectos sin localización precisa obligarán a reglas de asignación). ⚠ Pendiente de validar con datos.
- Confirmar periodicidad y fechas de corte.

6. Entregable particular del sector
- Tabla con inversión por localidad, indicadores FIN-C1..C3, y un informe corto que identifique localidades subfinanciadas para el IPT.
- Relación con E01, E02, E05, E06, E08.

7. Rama Git y documentación asociada
- Rama: feature/finanzas-inversion
- Documentos: README_FINANZAS_INVERSION.md, scripts de asignación de inversión, tests/test_finanzas.py

8. Checklist de cierre del sector
- [ ] Datos de inversión descargados y asociados a localidades o homologados.
- [ ] Indicadores FIN calculados y validados.
- [ ] Reglas de asignación documentadas si aplica.

-- Fin README Finanzas e Inversión Pública --
