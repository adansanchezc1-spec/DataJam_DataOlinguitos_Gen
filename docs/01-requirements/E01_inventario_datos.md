# E01 — Inventario Maestro de Datos Analizados
**Proyecto**: SIPTA (Sistema de Indicadores y Priorización Territorial y Alertas Tempranas) — DataJam Bogotá  
**Fase PDCO**: PLAN → DEVELOPMENT | **SDLC Stage**: Requirements / Data Understanding  
**Estándar**: IEEE 830 / ISO 29148 / DAMA-BOK  
**Responsables**: 
- Persona A (Adan Sánchez — Scrum Master & Lead Data Engineer)
- Persona B (Yesid Bello — Data Scientist & Territorial Analyst)  
- Persona C (Sofía Hidalgo — Tech Lead & BI Developer / Ingesta & QA)
**Última Actualización**: 2026-08-18  

---

## 1. Resumen Ejecutivo y Alcance del Inventario

El presente documento consolida el **Inventario Maestro de Datos (Entregable E01)** del proyecto SIPTA. Reúne la totalidad de fuentes de datos abiertos distritales y sectoriales evaluadas, organizadas en los **12 dominios temáticos** que alimentan el cálculo del **Índice de Prioridad Territorial (IPT)**, los tableros analíticos y los motores de alertas tempranas a nivel de las **20 localidades de Bogotá D.C.**

Siguiendo las directrices del **Plan Maestro SIPTA** y la normativa **DAMA-BOK**, cada fuente ha sido catalogada con su entidad rectora, ruta de almacenamiento en el repositorio, formato crudo, volumen de registros, dimensiones temporales, y el estado de validación de su identificador territorial canónico (`localidad` / `cod_localidad`).

---

## 2. Matriz General de Fuentes por Dominio

| Dominio | Código | Sector Distrital | Entidad Rectora | Formato Crudo | Nivel Territorial | Estado de Validación | Responsable |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Demografía y Población** | D1 | Planeación / Salud | SDP / SDS (SaluData) | CSV | Localidad / UPL | Confirmado (1-20) | Persona A & B |
| **Salud y Capacidad** | D2 | Salud Pública | SDS (SaluData) / IDECA | CSV / GPKG | Institucional / Localidad | Confirmado (1-20) | Persona B |
| **Educación y Calidad** | D3 | Educación | SED / SIMAT / ICFES | GPKG / GeoJSON / CSV | Sede / Localidad (1-20) | Confirmado (1-20) | Persona B |
| **Movilidad y Transporte** | D4 | Movilidad | TransMilenio / SDM / EMB | GeoJSON / GPKG / CSV / GTFS | ZAT / Estación / Troncal | Confirmado (Spatial Join) | Persona A |
| **Infraestructura y Espacio** | D5 | Recreación y Deporte | IDRD / DADEP / IDECA | CSV / GPKG | Parque / Localidad (1-20) | Confirmado (1-20) | Persona A |
| **Ambiente y Sostenibilidad**| D6 | Ambiente | SDA / RMCAB / IDECA | GeoJSON / CSV | Estación / Punto / Localidad | Confirmado (1-20) | Persona C (Sofía) |
| **Finanzas e Inversión FDL** | D7 | Gobierno / Hacienda / IPES | IPES / SDH / SED / SDIS | TXT / XLSX / GPKG / CSV | Localidad (1-20) | Confirmado (1-20) | Persona C & Persona A |
| **Seguridad y Delitos** | D8 | Seguridad y Convivencia | MEBOG / SDSCJ | CSV | Cuadrante / Localidad (1-20) | Confirmado (1-20) | Persona C (Sofía) |
| **Participación y PQR** | D9 | Gobierno Local | Secretaría General / SDQS | CSV | Localidad (1-20) | Confirmado (1-20) | Persona A & B |
| **Modelo Territorial Base** | D10 | Catastro / Cartografía | IDECA / SDP | GeoJSON / GPKG | 20 Localidades D.C. | Confirmado (Base Canónica) | Persona A & B |
| **Servicios Públicos** | D11 | Hábitat / Servicios | EAAB / UAESP / MinTIC / SDS | CSV | Localidad (1-20) | Confirmado (1-20) | Persona A & B |
| **Mercado Laboral y Salarios**| D12 | Desarrollo Económico | DANE (GEIH) / SDM (EMB) | CSV | Localidad (1-20) | Confirmado (1-20) | Persona B & A |

---

## 3. Inventario Detallado de Fuentes (Catálogo de 25 Datasets)

### 3.1 Servicios Públicos Domiciliarios y Calidad (D11)
- `SERVICIOS_PUBLICOS/eaab_cobertura_acueducto_localidad.csv` (EAAB / SSPD): Cobertura acueducto, alcantarillado, m3 de consumo y cortes por localidad.
- `SERVICIOS_PUBLICOS/eaab_calidad_agua_irca_localidad.csv` (SDS / SIVICAP): Índice de Riesgo de la Calidad del Agua (IRCA) por localidad.
- `SERVICIOS_PUBLICOS/uaesp_alumbrado_publico_localidad.csv` (UAESP): Luminarias totales, % tecnología LED y fallas.
- `SERVICIOS_PUBLICOS/cobertura_conectividad_tic_localidad.csv` (MinTIC / Alta Consejería TIC): Penetración internet banda ancha y zonas WiFi.

### 3.2 Inversión Pública, FDL y Gasto Social (D7)
- `FINANZAS_INVERSION_PUBLICA/inversion_fondos_desarrollo_local_fdl.csv` (Secretaría de Gobierno / Confis): Presupuesto aprobado, ejecutado y % cumplimiento de los 20 FDL.
- `FINANZAS_INVERSION_PUBLICA/metas_inversion_social_sdis_localidad.csv` (SDIS): Presupuesto social, transferencias monetarias, comedores comunitarios y centros de primera infancia.
- `FINANZAS_INVERSION_PUBLICA/presupuestos_participativos_propuestas_priorizadas.csv` (Secretaría de Gobierno / Plataforma Participación): Votación ciudadana y proyectos priorizados.
- `FINANZAS_INVERSION_PUBLICA/inversion_educacion_por_localidad_12_2025.gpkg` (SED): Inversión educativa territorializada 2025.
- `FINANZAS_INVERSION_PUBLICA/rivi-numero-*.txt` (IPES): Censos semestrales RIVI de vendedores informales.

### 3.3 Mercado Laboral, Salarios y Conmutación (D12)
- `EMPLEO_ECONOMIA/conmutacion_laboral_residencia_trabajo_localidad.csv` (SDM / DANE): Matriz de conmutación origen-destino laboral, autosuficiencia de empleo y tiempos de viaje.
- `EMPLEO_ECONOMIA/ingreso_promedio_salario_ocupados_localidad.csv` (DANE GEIH / SDDE): Salario promedio de ocupados, tasa de informalidad laboral y tasa de desempleo.

### 3.4 Participación Ciudadana y PQR (D9)
- `PARTICIPACION_CIUDADANA/pqr_bogota_te_escucha_por_localidad.csv` (Secretaría General / SDQS): Total solicitudes, % resolución a tiempo y temas frecuentes (malla vial, aseo, seguridad).

### 3.5 Modelo Territorial Oficial (D10)
- `MODELO_TERRITORIAL/poligonos_localidades.geojson` (IDECA): Geometría vectorial oficial de las 20 localidades en WGS84 (EPSG:4326).

### 3.6 Salud, Educación y Seguridad Expandidos (D2, D3, D8)
- `SALUD/capacidad_camas_asistencial_localidad.csv` (SDS): Total camas hospitalarias, camas por 10k hab y camas UCI por localidad.
- `EDUCACION/calidad_educativa_saber11_retencion_localidad.csv` (SED / ICFES): Puntaje promedio Saber 11 y tasa de deserción escolar.
- `SEGURIDAD/delitos_alto_impacto_localidad_2024_2026.csv` (MEBOG / SDSCJ): Homicidios, hurto a personas, hurto a comercio y tasa por 100k hab.
