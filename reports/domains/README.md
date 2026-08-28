# Catálogo de Informes Analíticos Sectoriales — SIPTA

**Sistema**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA)  
**Fase PDCO**: DEVELOPMENT → OPERATIONS  
**Estándares**: DAMA-BOK / SWEBOK Cap. 2 y 4 / ISO/IEC 25010 / RFC 7946 GeoJSON  

---

## 📑 Índice de Reportes Analíticos por Dominio

Cada informe contiene la ficha técnica con formulaciones matemáticas de todos los indicadores calculados, visualizaciones multi-panel geoespaciales en alta resolución (300 DPI con mapas coropléticos oficiales de Bogotá), análisis de brechas de las 20 localidades oficiales y recomendaciones estructuradas de política pública:

| # | Dominio Sectorial | Archivo de Informe | Indicadores Principales | Visualización Multi-Panel Geoespacial (3 Paneles) |
|---|---|---|---|---|
| **00** | **Resumen Ejecutivo Multidominio** | [`00_resumen_ejecutivo_multidominio.md`](00_resumen_ejecutivo_multidominio.md) | `IPT_Base`, `IPT_Geom`, `Consenso` | Mapa IPT + Ranking Bootstrap 95% + Dispersión Multidominio |
| **01** | **Demografía y Dinámica Espacial** | [`01_reporte_demografia.md`](01_reporte_demografia.md) | `DEM-001` (Densidad), `DEM-002` (Población DANE 2025) | Mapa Densidad + Ranking hab/km² + Población vs Área |
| **02** | **Salud y Capacidad Asistencial** | [`02_reporte_salud.md`](02_reporte_salud.md) | `SAL-001` (IPS/10k), `SAL-002` (Camas/10k) | Mapa Camas + Ranking IPS/10k + Población vs Camas |
| **03** | **Educación y Logro Académico** | [`03_reporte_educacion.md`](03_reporte_educacion.md) | `EDU-001` (Cupos/1k), `EDU-002` (Saber 11) | Mapa Saber 11 + Ranking Saber 11 + Cupos vs Saber 11 |
| **04** | **Movilidad y Accesibilidad** | [`04_reporte_movilidad.md`](04_reporte_movilidad.md) | `MOV-001` (TM), `MOV-002` (SITP), `MOV-003` (Tiempo) | Mapa Tiempo Viaje + Ranking Minutos + Estaciones vs Tiempo |
| **05** | **Infraestructura y Parques** | [`05_reporte_infraestructura.md`](05_reporte_infraestructura.md) | `INF-001` (m²/hab), `INF-002` (Área Total) | Mapa m²/hab + Ranking m²/hab + Población vs Área Parques |
| **06** | **Ambiente y Sostenibilidad** | [`06_reporte_ambiente.md`](06_reporte_ambiente.md) | `AMB-001` (SAC/km²), `AMB-002` (Eventos) | Mapa SAC + Ranking SAC/km² + Consumo Hídrico vs SAC |
| **07** | **Finanzas e Inversión FDL** | [`07_reporte_finanzas.md`](07_reporte_finanzas.md) | `FIN-001` (FDL/hab), `FIN-002` (Ejecución %) | Mapa FDL/hab + Ranking M COP/hab + Aprobado vs Ejecutado |
| **08** | **Vulnerabilidad Social y PUA SDIS** | [`08_reporte_vulnerabilidad_social.md`](08_reporte_vulnerabilidad_social.md) | `VUL-001` (IMG/10k), `VUL-002` (Comedores), `VUL-003` (RIVI) | Mapa Transferencias IMG + Ranking Vulnerabilidad + Subsidios vs RIVI |
| **09** | **Seguridad y Convivencia** | [`09_reporte_seguridad.md`](09_reporte_seguridad.md) | `SEG-001` (Hurtos/10k), `SEG-002` (Homicidios) | Mapa Hurtos/10k + Ranking Hurtos + Cuadrantes vs Homicidios |
| **10** | **Servicios Públicos** | [`10_reporte_servicios_publicos.md`](10_reporte_servicios_publicos.md) | `PUB-001` (IRCA), `PUB-002` (Acueducto %) | Mapa Acueducto + Ranking Cobertura + Interrupciones vs IRCA |
| **11** | **Mercado Laboral y Salarios** | [`11_reporte_empleo_economia.md`](11_reporte_empleo_economia.md) | `EMP-001` (Conmutación), `EMP-002` (Salario) | Mapa Conmutación + Ranking Conmutación + Informalidad vs Salario |
| **12** | **Participación y PQR** | [`12_reporte_participacion_ciudadana.md`](12_reporte_participacion_ciudadana.md) | `PAR-001` (PQR/10k), `PAR-002` (Oportunidad) | Mapa Votantes PP + Ranking PQR + Votantes vs Oportunidad |

---

## 🎨 Galería de Figuras Geoespaciales
Todas las figuras multi-panel de alta resolución (300 DPI) generadas para estos informes se encuentran disponibles en [`reports/figures/`](../figures/).
