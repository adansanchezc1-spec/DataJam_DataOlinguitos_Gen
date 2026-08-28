# SIPTA — Capa Gold / Datos Curados Contractuales (`data/curated/`)

**Propósito**: Datasets finales, normalizados y estructurados listos para modelado estadístico, auditoría cuantitativa y visualización geoespacial.

---

## Artefactos Curados Contractuales

| Archivo | Filas | Columnas | Descripción |
|---|---|---|---|
| `master_indicadores_territoriales.csv` | 20 | ~50 | Indicadores estandarizados, sub-índices dimensionales $[0, 1]$ y variables de contexto. |
| `dashboard_ranking.csv` | 20 | ~25 | Escenarios del IPT (Base, Rangos, Sin Parques, Sin RIVI, Sin Proxies, Geométrico), IC 95% Bootstrap y Prioridad de Consenso. |
| `sipta_localidades_multidominio.geojson` | 20 | ~55 | Capa vectorial geoespacial oficial (EPSG:4326 / RFC 7946) con métricas del IPT y 13 dominios integrados. |
| `domain_00_priorizacion_ipt.csv` a `domain_12_participacion_ciudadana.csv` | 20 c/u | ~8-15 | Tablas temáticas curadas por dominio analítico. |
