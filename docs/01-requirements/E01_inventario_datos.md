# E01 — Inventario Maestro de Datos Analizados
**Proyecto**: SIPTA (Sistema de Indicadores y Priorización Territorial y Alertas Tempranas) — DataJam Bogotá  
**Fase PDCO**: PLAN → DEVELOPMENT | **SDLC Stage**: Requirements / Data Understanding  
**Estándar**: IEEE 830 / ISO 29148 / DAMA-BOK  
**Responsables**: 
- Persona A (Adan Sánchez — Scrum Master & Lead Data Engineer)
- Persona B (Yesid Bello — Data Scientist & Territorial Analyst)  
- Persona C (Sofía Hidalgo — Tech Lead & BI Developer / Ingesta & QA)
**Última Actualización**: 2026-08-27 (Sprint 5)

---

## 1. Resumen Ejecutivo y Alcance del Inventario

El presente documento consolida el **Inventario Maestro de Datos (Entregable E01)** del proyecto SIPTA. Reúne la totalidad de fuentes de datos abiertos distritales y sectoriales evaluadas, organizadas en los **12 dominios temáticos** que alimentan el cálculo del **Índice de Priorización Territorial (IPT)**, los tableros analíticos y los motores de alertas tempranas a nivel de las **20 localidades de Bogotá D.C.**

Siguiendo las directrices del **Plan Maestro SIPTA** y la normativa **DAMA-BOK**, cada fuente ha sido catalogada con su entidad rectora, ruta de almacenamiento en el repositorio, formato crudo, volumen de registros, dimensiones temporales, y el estado de validación de su identificador territorial canónico (`localidad` / `codigo_localidad`).

---

## 2. Matriz General de Fuentes por Dominio

| Dominio | Código | Sector Distrital | Entidad Rectora | Formato Crudo | Nivel Territorial | Estado de Validación | Responsable |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Demografía y Población Oficial** | D1 | Planeación | DANE / SDP | XLSX | Localidad (1-20) y UPZ | Confirmado (8.101.412 hab a 2025) | Persona A & B |
| **Vulnerabilidad Social y PUA** | D1-PUA | Integración Social | SDIS | XLSX | Microdatos individuales | Confirmado (1.048.575 registros) | Persona A & B |
| **Salud y Capacidad** | D2 | Salud Pública | SDS (SaluData) / REPS | CSV / GPKG | Institucional / Localidad | Confirmado (1-20) | Persona B |
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

### 3.1 Demografía y Vulnerabilidad Social (D1, D1-PUA)
- `DEMOGRAFIA/anexo-proyecciones-poblacion-bogota-desagreacion-loc-2018-2035-UPZ-2018-2024.xlsx` (DANE / SDP): Proyecciones oficiales de población por localidad (2018–2035) y por UPZ (2018–2024). Corte 2025: **8.101.412 habitantes**.
- `VULNERABILIDAD/pua_riesgo_y_anon_20250911_193636-1.xlsx` (SDIS): Microdatos administrativos del Plan Único de Atención 2024 (**1.048.575 registros** anonimizados con transferencias IMG, comedores, comisarías y habitabilidad en calle).

### 3.2 Servicios Públicos Domiciliarios y Calidad (D11)
- `SERVICIOS_PUBLICOS/eaab_cobertura_acueducto_localidad.csv` (EAAB / SSPD): Cobertura acueducto, alcantarillado, m3 de consumo y cortes por localidad.
- `SERVICIOS_PUBLICOS/eaab_calidad_agua_irca_localidad.csv` (SDS / SIVICAP): Índice de Riesgo de la Calidad del Agua (IRCA) por localidad.
- `SERVICIOS_PUBLICOS/uaesp_alumbrado_publico_localidad.csv` (UAESP): Luminarias totales, % tecnología LED y fallas.
- `SERVICIOS_PUBLICOS/cobertura_conectividad_tic_localidad.csv` (MinTIC / Alta Consejería TIC): Penetración internet banda ancha y zonas WiFi.

### 3.3 Inversión Pública, FDL y Gasto Social (D7)
- `FINANZAS_INVERSION_PUBLICA/inversion_fondos_desarrollo_local_fdl.csv` (Secretaría de Gobierno / Confis): Presupuesto aprobado, ejecutado y % cumplimiento de los 20 FDL.
- `FINANZAS_INVERSION_PUBLICA/metas_inversion_social_sdis_localidad.csv` (SDIS): Presupuesto social, transferencias monetarias, comedores comunitarios y centros de primera infancia.
- `FINANZAS_INVERSION_PUBLICA/presupuestos_participativos_propuestas_priorizadas.csv` (Secretaría de Gobierno / Plataforma Participación): Votación ciudadana y proyectos priorizados.
- `FINANZAS_INVERSION_PUBLICA/inversion_educacion_por_localidad_12_2025.gpkg` (SED): Inversión educativa territorializada 2025.
- `FINANZAS_INVERSION_PUBLICA/rivi-numero-*.txt` (IPES): Censos semestrales RIVI de vendedores informales.

### 3.4 Mercado Laboral, Salarios y Conmutación (D12)
- `EMPLEO_ECONOMIA/conmutacion_laboral_residencia_trabajo_localidad.csv` (SDM / DANE): Matriz de conmutación origen-destino laboral, autosuficiencia de empleo y tiempos de viaje.
- `EMPLEO_ECONOMIA/ingreso_promedio_salario_ocupados_localidad.csv` (DANE GEIH / SDDE): Salario promedio de ocupados, tasa de informalidad laboral y tasa de desempleo.

### 3.5 Participación Ciudadana y PQR (D9)
- `PARTICIPACION_CIUDADANA/pqr_bogota_te_escucha_por_localidad.csv` (Secretaría General / SDQS): Total solicitudes, % resolución a tiempo y temas frecuentes (malla vial, aseo, seguridad).

### 3.6 Modelo Territorial Oficial (D10)
- `MODELO_TERRITORIAL/poligonos_localidades.geojson` (IDECA): Geometría vectorial oficial de las 20 localidades en WGS84 (EPSG:4326).

### 3.7 Salud, Educación, Movilidad, Ambiente y Seguridad (D2, D3, D4, D5, D6, D8)
- `SALUD/capacidad_camas_asistencial_localidad.csv` (SDS / REPS): Camas hospitalarias y camas UCI por localidad.
- `SALUD/osb_ofertasrv-ips-urgencias.csv` (SDS): IPS con servicios de urgencias.
- `EDUCACION/calidad_educativa_saber11_retencion_localidad.csv` (SED / ICFES): Puntaje promedio Saber 11 y retención escolar.
- `EDUCACION/ofertacupos_032025.geojson` y `colegios122025.gpkg` (SED): Sedes y oferta de cupos oficiales.
- `MOVILIDAD/estaciones_troncales.geojson` y `paraderos_zonales_sitp.gpkg` (TransMilenio): Cobertura masiva y zonal.
- `INFRAESTRUCTURA_ESPACIO_PUBLICO/5.-parques-idrd.csv` (IDRD): Parques y espacio público.
- `AMBIENTE/situacion_ambiental_conflictiva.csv` y `estacion_calidad_aire.geojson` (SDA): Situación ambiental conflictiva y RMCAB.
- `SEGURIDAD/delitos_alto_impacto_localidad_2024_2026.csv` y `Cuadrante de Policía. Bogotá D.C.csv` (MEBOG / SDSCJ): Criminalidad y vigilancia policial.
