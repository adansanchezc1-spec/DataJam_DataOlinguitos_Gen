# Conclusiones del EDA — SIPTA Bogotá

Generado: 2026-08-27 21:01 | modo smoke: True

## 1. Inventario y calidad

- **119** archivos físicos en `data/raw` en 14 sectores.
- % de nulos medio por fuente: **5.8%** (mediana 0.0%).

## 2. Cobertura territorial

- Matriz de cobertura: 20 localidades x 5 fuentes; en promedio cada fuente cubre **100%** de las localidades.
- Fuentes con dato en las 20 localidades: 5.

## 3. Indicadores

- **construible_ahora**: 11
- **construible_con_cruce_espacial**: 2
- **construible_parcial**: 2
- **faltante**: 5
- **faltante_territorial**: 1

## 4. Hallazgos clave

- La población por localidad (OSB, serie anual) permite calcular denominadores per cápita para todos los sectores: es la fuente más transversal del proyecto.
- Los sectores AMBIENTE, PARTICIPACIÓN CIUDADANA, SEGURIDAD y SERVICIOS PÚBLICOS no tienen datos físicos: sus indicadores (AMB-01, PAR-01, SEG-01, SER-01) quedan como faltantes.
- El conteo territorial de IPS y estaciones se resolvió con cruce espacial contra la capa Loca del mapa de referencia (antes 0/20 localidades).
- Los XLSX de validaciones de TransMilenio tienen filas de título arriba del encabezado: el lector robusto las omite y el % de nulos reportado es real.
- El mapa de referencia (MR, 41 capas) se usa como base cartográfica para cruces, no como fuente de indicadores.
- Los 62 archivos mensuales de validaciones TM permiten construir series diarias y mensuales de demanda por modo.

## 5. Siguientes pasos

- Priorizar la consecución de fuentes de los sectores vacíos (ver `07_eda_gaps.ipynb`).
- Construir los indicadores marcados como `construible_ahora` (ver `resumen_indicadores_eda.csv`).
- Validar las unidades monetarias de inversión (R_ASIGNADOS) con la SED antes de publicar.