# SIPTA — Evaluación Consolidada de Calidad de Datasets

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA — DataJam Bogotá)  
**Fase PDCO**: CONTROL / SDLC: Testing & Quality Assurance  
**Marco Normativo**: ISO/IEC 25010 (Calidad del Producto) / DAMA-BOK (Gobierno de Datos) / IEEE 830  
**Fecha de Evaluación**: 2026-08-18  
**Equipo Evaluador**: 
- Persona A (Adan Sánchez — Lead Data Engineer & Quality Assurance)
- Persona B (Yesid Bello — Data Scientist & Territorial Analyst)
- Persona C (Sofía Hidalgo — Tech Lead & BI Developer)

---

# Índice de Evaluaciones Sectoriales

1. [Dominio 1: Demografía y Población — Localidades (`DEM-01`)](#1-dominio-1-demografía-y-población--localidades)
2. [Dominio 1: Demografía y Población — UPL (`DEM-02`)](#2-dominio-1-demografía-y-población--upl)
3. [Dominio 2: Salud — IPS con Servicios de Urgencias (`SAL-01`)](#3-dominio-2-salud--ips-con-servicios-de-urgencias)
4. [Dominio 2: Salud — Capacidad de Camas Hospitalarias (`SAL-02`)](#4-dominio-2-salud--capacidad-de-camas-hospitalarias)
5. [Dominio 3: Educación — Directorio de Colegios SED (`EDU-01`)](#5-dominio-3-educación--directorio-de-colegios-sed)
6. [Dominio 3: Educación — Oferta de Cupos Escolares (`EDU-02`)](#6-dominio-3-educación--oferta-de-cupos-escolares)
7. [Dominio 3: Educación — Calidad Saber 11 y Retención (`EDU-03`)](#7-dominio-3-educación--calidad-saber-11-y-retención)
8. [Dominio 4: Movilidad — Flota SITP Vinculada (`MOV-01`)](#8-dominio-4-movilidad--flota-sitp-vinculada)
9. [Dominio 4: Movilidad — Estaciones Troncales TransMilenio (`MOV-02`)](#9-dominio-4-movilidad--estaciones-troncales-transmilenio)
10. [Dominio 5: Infraestructura — Inventario de Parques IDRD (`INF-01`)](#10-dominio-5-infraestructura--inventario-de-parques-idrd)
11. [Dominio 6: Ambiente — Situaciones Ambientales Conflictivas SAC (`AMB-01`)](#11-dominio-6-ambiente--situaciones-ambientales-conflictivas-sac)
12. [Dominio 6: Ambiente — Estaciones de Calidad del Aire RMCAB (`AMB-02`)](#12-dominio-6-ambiente--estaciones-de-calidad-del-aire-rmcab)
13. [Dominio 7: Finanzas — Vendedores Informales RIVI (`FIN-01`)](#13-dominio-7-finanzas--vendedores-informales-rivi)
14. [Dominio 7: Finanzas — Puntos de Encuentro IPES (`FIN-02`)](#14-dominio-7-finanzas--puntos-de-encuentro-ipes)
15. [Dominio 7: Finanzas — Inversión Fondos de Desarrollo Local FDL (`FIN-03`)](#15-dominio-7-finanzas--inversión-fondos-de-desarrollo-local-fdl)
16. [Dominio 7: Finanzas — Metas Inversión Social SDIS (`FIN-04`)](#16-dominio-7-finanzas--metas-inversión-social-sdis)
17. [Dominio 8: Seguridad — Cuadrantes de Policía MEBOG (`SEG-01`)](#17-dominio-8-seguridad--cuadrantes-de-policía-mebog)
18. [Dominio 8: Seguridad — Delitos de Alto Impacto (`SEG-02`)](#18-dominio-8-seguridad--delitos-de-alto-impacto)
19. [Dominio 9: Participación — PQR Bogotá Te Escucha (`PAR-01`)](#19-dominio-9-participación--pqr-bogotá-te-escucha)
20. [Dominio 9: Participación — Presupuestos Participativos (`PAR-02`)](#20-dominio-9-participación--presupuestos-participativos)
21. [Dominio 10: Modelo Territorial — Polígonos de Localidades IDECA (`GEO-01`)](#21-dominio-10-modelo-territorial--polígonos-de-localidades-ideca)
22. [Dominio 11: Servicios Públicos — Acueducto y Alcantarillado EAAB (`PUB-01`)](#22-dominio-11-servicios-públicos--acueducto-y-alcantarillado-eaab)
23. [Dominio 11: Servicios Públicos — Calidad del Agua IRCA (`PUB-02`)](#23-dominio-11-servicios-públicos--calidad-del-agua-irca)
24. [Dominio 11: Servicios Públicos — Alumbrado Público UAESP (`PUB-03`)](#24-dominio-11-servicios-públicos--alumbrado-público-uaesp)
25. [Dominio 11: Servicios Públicos — Conectividad TIC (`PUB-04`)](#25-dominio-11-servicios-públicos--conectividad-tic)
26. [Dominio 12: Empleo / Economía — Conmutación Residencia-Trabajo (`EMP-01`)](#26-dominio-12-empleo--economía--conmutación-residencia-trabajo)
27. [Dominio 12: Empleo / Economía — Salarios e Informalidad GEIH (`EMP-02`)](#27-dominio-12-empleo--economía--salarios-e-informalidad-geih)

---

## 1. Dominio 1: Demografía y Población — Localidades

### 1.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Demografía y Población (D1) |
| Dataset | `data/raw/DEMOGRAFIA/osb_demografia-poblacion-localidad.csv` |
| Entidad / fuente | Secretaría Distrital de Planeación (SDP) / Secretaría Distrital de Salud (SaluData) |
| URL de origen | https://saludata.saludcapital.gov.co/osb/index.php/datos-demograficos/ |
| Formato | CSV (Delimitador `;`, Codificación UTF-8) |
| Fecha o período de referencia | 2005 – 2035 (Proyecciones anuales DANE CNPV 2018) |
| Responsable de validación | Persona A (Adan Sánchez) & Persona B (Yesid Bello) |

### 1.2 Capacidad de territorialización
**¿El dataset puede asociarse al modelo territorial?**
- [x] Sí
- [ ] Parcialmente
- [ ] No

**Mecanismo disponible:**
- [x] Código de localidad (`CODIGO_LOCALIDAD`)
- [x] Nombre de localidad (`NOMBRE_LOCALIDAD`)
- [ ] UPZ o barrio homologable
- [ ] Coordenadas
- [ ] Geometría

**Variables utilizadas:** `CODIGO_LOCALIDAD` (Enteros 1 a 20), `NOMBRE_LOCALIDAD`.  
**Observaciones:** Contiene registro adicional con código 0 correspondiente al total distrital de Bogotá D.C., filtrable en pipeline.

### 1.3 Variables críticas
| Variable | Uso analítico | Criticidad | Observación |
|---|---|---|---|
| `CODIGO_LOCALIDAD` | Llave foránea territorial de agregación | Alta | Entero [1, 20], no nulo |
| `ANO` | Filtro temporal de vigencia | Alta | Entero [2005, 2035] |
| `EDAD` | Estructura etaria y población objetivo escolar/asistencial | Alta | Rango [0, 100+] |
| `POBLACION` | Denominador universal per cápita | Alta | Entero $\ge 0$ |

### 1.4 Matriz de calidad
| Dimensión | Pregunta | Métrica | Variable / regla evaluada | Resultado | Criticidad | Observación |
|---|---|---|---|---|---|---|
| Completitud | ¿Hay valores faltantes? | % nulos | Todas las columnas | 0.0% nulos | Alta | 131.502 registros íntegros |
| Consistencia | ¿Hay contradicciones? | Suma por edades vs total | $\sum 	ext{POBLACION}$ | 100% consistente | Alta | Cuadre exacto con proyecciones oficiales |
| Validez | ¿Cumple reglas de tipo/rango? | % válidos | Tipos enteros y rangos | 100% válido | Alta | Tipado numérico correcto |
| Unicidad | ¿Hay duplicados? | % duplicados | Clave (Localidad, Año, Edad, Sexo) | 0.0% duplicados | Media | Registro único por cohorte |
| Actualidad | ¿Está actualizado? | Período cubierto | 2005 - 2035 | Vigente | Alta | Proyección oficial distrital |
| Precisión | ¿Los valores son confiables? | Validación cruzada | Contraste DANE vs SDP | 100% coincidente | Alta | Fuente rectora oficial |

### 1.5 Criterios de aceptación
- [x] **Cobertura territorial identificable**: Cumple (20 de 20 localidades).
- [x] **Variables relevantes para el objetivo**: Cumple (Denominadores per cápita).
- [x] **Calidad aceptable**: Cumple sin observaciones.
- [x] **Licencia de reutilización**: Verificada (Datos Abiertos Bogotá / SaluData).
- [x] **Integración con modelo territorial maestro**: Posible de forma directa por código.

### 1.6 Resultado y Trazabilidad
- **Estado**: **Aceptado**
- **Justificación**: Base maestra fundamental para tasas por habitante en todos los sectores.
- **Trazabilidad**: Alimentación de `DEM-001`, `POB-002`, `SAL-001`, `EDU-001`, `SEG-002`.

---

## 2. Dominio 1: Demografía y Población — UPL

### 2.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Demografía y Población (D1) |
| Dataset | `data/raw/DEMOGRAFIA/osb_demografia-poblacion-upl.csv` |
| Entidad / fuente | Secretaría Distrital de Planeación (SDP) |
| URL de origen | https://saludata.saludcapital.gov.co/osb/index.php/datos-demograficos/ |
| Formato | CSV (Delimitador `;`, Codificación UTF-8) |
| Fecha o período de referencia | 2005 – 2035 |
| Responsable de validación | Persona A (Adan Sánchez) & Persona B (Yesid Bello) |

### 2.2 Capacidad de territorialización
**¿El dataset puede asociarse al modelo territorial?**
- [x] Sí (A nivel de Unidad de Planeamiento Local - UPL)
- **Mecanismo:** `CODIGO_UPL`, `NOMBRE_UPL` (33 UPLs oficiales POT Decreto 555 de 2021).

### 2.3 Matriz de calidad y Criterios
- **Filas**: 175.956 | **Columnas**: 10 | **Nulos**: 0.0% | **Duplicados**: 0.0%.
- **Resultado**: **Aceptado** para desagregaciones submunicipales en tableros analíticos.

---

## 3. Dominio 2: Salud — IPS con Servicios de Urgencias

### 3.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Salud y Capacidad Hospitalaria (D2) |
| Dataset | `data/raw/SALUD/osb_ofertasrv-ips-urgencias.csv` |
| Entidad / fuente | Secretaría Distrital de Salud (SDS) — REPS / SaluData |
| URL de origen | https://saludata.saludcapital.gov.co/osb/ |
| Formato | CSV (Delimitador `,`, Codificación Latin-1) |
| Fecha o período de referencia | 2024 – 2026 |
| Responsable de validación | Persona B (Yesid Bello) |

### 3.2 Capacidad de territorialización
- [x] Sí (Vía Unión Espacial / Point-in-Polygon).
- **Variables:** `Latitud`, `Longitud` (Coordenadas geográficas WGS84).
- **Calidad de Georreferenciación:** 97.62% de coordenadas válidas dentro del perímetro de Bogotá D.C. (2 registros requieren ajuste de signo en longitud).

### 3.3 Resultado de la evaluación
- **Estado**: **Aceptado con observaciones**.
- **Tratamiento**: Ingesta mediante `src/cleaning/clean_data.py` corrigiendo coordenadas negativas y cruzando con polígonos de `dim_territorio.md`.

---

## 4. Dominio 2: Salud — Capacidad de Camas Hospitalarias

### 4.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Salud y Capacidad Hospitalaria (D2) |
| Dataset | `data/raw/SALUD/capacidad_camas_asistencial_localidad.csv` |
| Entidad / fuente | SDS / Registro Especial de Prestadores de Servicios de Salud (REPS) |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona B (Yesid Bello) |

### 4.2 Matriz de calidad
- **Filas**: 20 | **Columnas**: 8 | **Duplicados**: 0 | **Cobertura Territorial**: 100% (20 localidades).
- **Variables Clave**: `total_camas_hospitalarias`, `camas_por_10000_habitantes`, `camas_uci_adultos`.
- **Estado**: **Aceptado**. Sustenta directamente el indicador `SAL-002`.

---

## 5. Dominio 3: Educación — Directorio de Colegios SED

### 5.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Educación y Cobertura (D3) |
| Dataset | `data/raw/EDUCACION/colegios122025.gpkg` |
| Entidad / fuente | Secretaría de Educación del Distrito (SED) / IDECA |
| URL de origen | https://www.ideca.gov.co/ |
| Formato | GeoPackage (Capa vectorial `colegios_122025`, EPSG:3857) |
| Fecha de corte | Diciembre 2025 |
| Responsable | Persona B (Yesid Bello) |

### 5.2 Capacidad de territorialización y Matriz
- **Registros**: 2.211 sedes educativas oficiales y no oficiales.
- **Territorialización**: Código `COD_LOCA` (1 a 20) + Geometría `Point`.
- **Nulos en llaves**: 0.0%.
- **Estado**: **Aceptado**. Sustenta `EDU-001` (Oferta de sedes por localidad).

---

## 6. Dominio 3: Educación — Oferta de Cupos Escolares

### 6.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Educación y Cobertura (D3) |
| Dataset | `data/raw/EDUCACION/ofertacupos_032025.geojson` |
| Entidad / fuente | Secretaría de Educación del Distrito (SED) |
| Formato | GeoJSON (EPSG:3857 / Reproyectado a WGS84 EPSG:4326) |
| Fecha de corte | Marzo 2025 |
| Responsable | Persona B (Yesid Bello) |

### 6.2 Matriz de calidad
- **Registros**: 747 sedes oficiales con oferta de cupos discriminada por nivel (Preescolar, Primaria, Secundaria, Media).
- **Variables Críticas**: `OPreescola`, `OPrimaria`, `OSecundari`, `OMedia`, `OTotal`, `COD_LOCA`.
- **Consistencia**: `OTotal = OPreescola + OPrimaria + OSecundari + OMedia` (100% consistente).
- **Estado**: **Aceptado**.

---

## 7. Dominio 3: Educación — Calidad Saber 11 y Retención

### 7.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Educación y Cobertura (D3) |
| Dataset | `data/raw/EDUCACION/calidad_educativa_saber11_retencion_localidad.csv` |
| Entidad / fuente | SED / Instituto Colombiano para la Evaluación de la Educación (ICFES) |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona B (Yesid Bello) |

### 7.2 Matriz de calidad
- **Filas**: 20 | **Cobertura**: 20 localidades | **Nulos**: 0.0%.
- **Variables**: `puntaje_promedio_saber_11` (Puntaje 239 a 308), `tasa_desercion_escolar_pct` (1.4% a 5.2%).
- **Estado**: **Aceptado**. Alimenta el indicador `EDU-003`.

---

## 8. Dominio 4: Movilidad — Flota SITP Vinculada

### 8.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Movilidad y Transporte (D4) |
| Dataset | `data/raw/MOVILIDAD/flota_vinculada_sitp_2024-12.csv` |
| Entidad / fuente | TransMilenio S.A. / Subgerencia Técnica y de Servicios |
| URL de origen | https://datosabiertos.bogota.gov.co/ |
| Formato | CSV (Delimitador `,`, Codificación UTF-8) |
| Fecha de corte | Diciembre 2024 |
| Responsable | Persona A (Adan Sánchez) |

### 8.2 Matriz de calidad
- **Registros**: 7.420 buses zonales y troncales.
- **Variables Críticas**: `PLACA`, `TIPOLOGIA`, `TIPO_COMBUSTIBLE` (Eléctrico, Gas, Diésel Euro VI), `EMPRESA_OPERADORA`.
- **Estado**: **Aceptado**. Sustenta `MOV-001` y `MOV-002`.

---

## 9. Dominio 4: Movilidad — Estaciones Troncales TransMilenio

### 9.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Movilidad y Transporte (D4) |
| Dataset | `data/raw/MOVILIDAD/estaciones_troncales.geojson` |
| Entidad / fuente | TransMilenio S.A. / IDECA |
| Formato | GeoJSON (Point EPSG:4326) |
| Vigencia | 2024 – 2026 |
| Responsable | Persona A (Adan Sánchez) |

### 9.2 Matriz de calidad
- **Registros**: 151 estaciones y portales troncales georreferenciados.
- **Estado**: **Aceptado**.

---

## 10. Dominio 5: Infraestructura — Inventario de Parques IDRD

### 10.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Infraestructura y Espacio Público (D5) |
| Dataset | `data/raw/INFRAESTRUCTURA_ESPACIO_PUBLICO/5.-parques-idrd.csv` |
| Entidad / fuente | Instituto Distrital de Recreación y Deporte (IDRD) |
| URL de origen | https://datosabiertos.bogota.gov.co/ |
| Formato | CSV (Delimitador `,`, Codificación UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona A (Adan Sánchez) |

### 10.2 Matriz de calidad
- **Registros**: 5.120 parques auditados.
- **Variables Críticas**: `CODIGO_PARQUE`, `NOMBRE_PARQUE`, `LOCALIDAD`, `AREA_M2`, `CLASIFICACION` (Vecinal, Zonal, Metropolitano, Regional).
- **Cobertura Territorial**: 100% de las 20 localidades oficiales.
- **Estado**: **Aceptado**. Sustenta `INF-004` (Espacio público verde per cápita).

---

## 11. Dominio 6: Ambiente — Situaciones Ambientales Conflictivas SAC

### 11.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Ambiente y Sostenibilidad (D6) |
| Dataset | `data/raw/AMBIENTE/situacion_ambiental_conflictiva.csv` |
| Entidad / fuente | Secretaría Distrital de Ambiente (SDA) / IDECA |
| URL de origen | https://ambientebogota.gov.co/ |
| Formato | CSV (Delimitador `,`, Codificación UTF-8) |
| Vigencia | 2020 – 2025 |
| Responsable | Persona C (Sofía Hidalgo) |

### 11.2 Matriz de calidad
- **Registros**: 1.313 situaciones ambientales georreferenciadas.
- **Variables Críticas**: `id`, `tipo_conflicto` (Hídrico, Calidad del Aire, Ruido, Residuos, Suelo), `cod_locali`.
- **Estado**: **Aceptado**. Sustenta `AMB-001`.

---

## 12. Dominio 6: Ambiente — Estaciones de Calidad del Aire RMCAB

### 12.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Ambiente y Sostenibilidad (D6) |
| Dataset | `data/raw/AMBIENTE/estacion_calidad_aire.geojson` |
| Entidad / fuente | SDA — Red de Monitoreo de Calidad del Aire de Bogotá (RMCAB) |
| Formato | GeoJSON (Point EPSG:4326) |
| Vigencia | 2024 – 2026 |
| Responsable | Persona C (Sofía Hidalgo) |

### 12.2 Matriz de calidad
- **Registros**: 20 estaciones de monitoreo continuo (PM2.5, PM10, $O_3$, $NO_2$).
- **Estado**: **Aceptado**. Sustenta `AMB-002`.

---

## 13. Dominio 7: Finanzas — Vendedores Informales RIVI

### 13.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Finanzas e Inversión Pública (D7) |
| Dataset | `data/raw/FINANZAS_INVERSION_PUBLICA/rivi-numero-*.txt` (6 series semestrales) |
| Entidad / fuente | Instituto para la Economía Social (IPES) |
| URL de origen | https://www.ipes.gov.co/ |
| Formato | TXT Tab-Separated (UTF-8 / Latin-1) |
| Período | 2017 a 2019 (Semestres I y II) |
| Responsable | Persona C (Sofía Hidalgo) |

### 13.2 Matriz de calidad
- **Registros Consolidados**: 120 observaciones (20 localidades × 6 periodos).
- **Variables**: `codigo_localidad`, `nombre_localidad`, `numero_vendedores`, `porcentaje`, `fecha_corte`.
- **Estado**: **Aceptado**. Sustenta `FIN-001`.

---

## 14. Dominio 7: Finanzas — Puntos de Encuentro IPES

### 14.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Finanzas e Inversión Pública (D7) |
| Dataset | `data/raw/FINANZAS_INVERSION_PUBLICA/Punto de encuentro vendedores. Bogotá D.C..xlsx` |
| Entidad / fuente | Instituto para la Economía Social (IPES) |
| Formato | XLSX / GeoJSON |
| Vigencia | 2024 – 2025 |
| Responsable | Persona C (Sofía Hidalgo) |

### 14.2 Matriz de calidad
- **Registros**: 85 puntos de encuentro formalizados con coordenadas espaciales.
- **Estado**: **Aceptado**.

---

## 15. Dominio 7: Finanzas — Inversión Fondos de Desarrollo Local FDL

### 15.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Finanzas e Inversión Pública (D7) |
| Dataset | `data/raw/FINANZAS_INVERSION_PUBLICA/inversion_fondos_desarrollo_local_fdl.csv` |
| Entidad / fuente | Secretaría Distrital de Gobierno / CONFIS / Mapa de Inversiones de Bogotá |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona A (Adan Sánchez) & Persona C (Sofía Hidalgo) |

### 15.2 Matriz de calidad
- **Filas**: 20 localidades | **Nulos**: 0.0% | **Duplicados**: 0.
- **Variables**: `presupuesto_aprobado_millones`, `presupuesto_ejecutado_millones`, `porcentaje_ejecucion_fdl`.
- **Consistencia**: $0 \le 	ext{ejecutado} \le 	ext{aprobado} 	imes 1.05$ (100% consistente).
- **Estado**: **Aceptado**. Sustenta `FIN-002` (Desbalance y ejecución presupuestal local).

---

## 16. Dominio 7: Finanzas — Metas Inversión Social SDIS

### 16.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Finanzas e Inversión Pública (D7) |
| Dataset | `data/raw/FINANZAS_INVERSION_PUBLICA/metas_inversion_social_sdis_localidad.csv` |
| Entidad / fuente | Secretaría Distrital de Integración Social (SDIS) |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona A (Adan Sánchez) & Persona C (Sofía Hidalgo) |

### 16.2 Matriz de calidad
- **Filas**: 20 localidades | **Variables**: `presupuesto_social_sdis_millones`, `beneficiarios_transferencias_monetarias`, `comedores_comunitarios_activos`.
- **Estado**: **Aceptado**. Sustenta `FIN-003`.

---

## 17. Dominio 8: Seguridad — Cuadrantes de Policía MEBOG

### 17.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Seguridad y Convivencia (D8) |
| Dataset | `data/raw/SEGURIDAD/Cuadrante de Policía. Bogotá D.C.csv` |
| Entidad / fuente | Policía Metropolitana de Bogotá (MEBOG) / SDSCJ |
| URL de origen | https://oaiee.scj.gov.co/ |
| Formato | CSV (Delimitador `;`, Codificación Latin-1) |
| Vigencia | 2025 – 2026 |
| Responsable | Persona C (Sofía Hidalgo) |

### 17.2 Matriz de calidad
- **Registros**: 599 cuadrantes policiales.
- **Cobertura**: 19 localidades urbanas (Sumapaz opera bajo esquema rural de carabineros).
- **Variables**: `PCUNCUADRA`, `PCUNOMEST`, `PCUIULOCAL` (1-19).
- **Estado**: **Aceptado**. Sustenta `SEG-001`.

---

## 18. Dominio 8: Seguridad — Delitos de Alto Impacto

### 18.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Seguridad y Convivencia (D8) |
| Dataset | `data/raw/SEGURIDAD/delitos_alto_impacto_localidad_2024_2026.csv` |
| Entidad / fuente | MEBOG / SDSCJ — Sistema de Información Estadístico Delincuencial (SIEDCO) |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2026 |
| Responsable | Persona C (Sofía Hidalgo) |

### 18.2 Matriz de calidad
- **Filas**: 20 localidades | **Nulos**: 0.0%.
- **Variables**: `homicidios_anual`, `hurto_a_personas_anual`, `tasa_delitos_alto_impacto_por_100k_hab`.
- **Estado**: **Aceptado**. Sustenta `SEG-002`.

---

## 19. Dominio 9: Participación — PQR Bogotá Te Escucha

### 19.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Participación Ciudadana y Alertas Tempranas (D9) |
| Dataset | `data/raw/PARTICIPACION_CIUDADANA/pqr_bogota_te_escucha_por_localidad.csv` |
| Entidad / fuente | Secretaría General de la Alcaldía Mayor / Sistema Distrital de Quejas SDQS |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona A (Adan Sánchez) & Persona B (Yesid Bello) |

### 19.2 Matriz de calidad
- **Filas**: 20 localidades | **Total PQR Auditadas**: 176.650 solicitudes.
- **Variables**: `total_pqr_recibidas`, `pqr_resueltas_a_tiempo_pct`, `tema_frecuente_1`.
- **Estado**: **Aceptado**. Sustenta `PAR-001`.

---

## 20. Dominio 9: Participación — Presupuestos Participativos

### 20.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Participación Ciudadana (D9) |
| Dataset | `data/raw/FINANZAS_INVERSION_PUBLICA/presupuestos_participativos_propuestas_priorizadas.csv` |
| Entidad / fuente | Secretaría Distrital de Gobierno |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona A (Adan Sánchez) & Persona B (Yesid Bello) |

### 20.2 Matriz de calidad
- **Filas**: 20 localidades | **Variables**: `total_votantes_pp`, `propuestas_priorizadas_aprobadas`, `inversion_presupuesto_participativo_millones`.
- **Estado**: **Aceptado**. Sustenta `PAR-002`.

---

## 21. Dominio 10: Modelo Territorial — Polígonos de Localidades IDECA

### 21.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Modelo Territorial Oficial (D10) |
| Dataset | `data/raw/MODELO_TERRITORIAL/poligonos_localidades.geojson` |
| Entidad / fuente | Unidad Administrativa Especial de Catastro Distrital (UAECD) / IDECA |
| URL de origen | https://serviciosgis.catastrobogota.gov.co/ |
| Formato | GeoJSON (Vector Polygons, CRS WGS84 EPSG:4326) |
| Vigencia | Oficial Vigente |
| Responsable | Persona A (Adan Sánchez) & Persona B (Yesid Bello) |

### 21.2 Matriz de calidad
- **Registros**: 20 polígonos correspondientes a las 20 localidades oficiales de Bogotá D.C.
- **Topología**: 100% de geometrías válidas y cerradas sin solapamientos ilegales.
- **Estado**: **Aceptado** como marco cartográfico base de SIPTA (`GEO-001`).

---

## 22. Dominio 11: Servicios Públicos — Acueducto y Alcantarillado EAAB

### 22.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Servicios Públicos Domiciliarios (D11) |
| Dataset | `data/raw/SERVICIOS_PUBLICOS/eaab_cobertura_acueducto_localidad.csv` |
| Entidad / fuente | Empresa de Acueducto y Alcantarillado de Bogotá (EAAB - ESP) / SSPD |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona A (Adan Sánchez) & Persona B (Yesid Bello) |

### 22.2 Matriz de calidad
- **Filas**: 20 localidades | **Variables**: `cobertura_acueducto_pct`, `cobertura_alcantarillado_pct`, `horas_interrupcion_promedio_mes`.
- **Rango Válido**: $[0.0, 100.0]\%$ (100% conforme).
- **Estado**: **Aceptado**. Sustenta `PUB-001`.

---

## 23. Dominio 11: Servicios Públicos — Calidad del Agua IRCA

### 23.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Servicios Públicos Domiciliarios (D11) |
| Dataset | `data/raw/SERVICIOS_PUBLICOS/eaab_calidad_agua_irca_localidad.csv` |
| Entidad / fuente | Secretaría Distrital de Salud — Laboratorio de Salud Pública / SIVICAP |
| Formato | CSV (UTF-8) |
| Vigencia | 2025 |
| Responsable | Persona A (Adan Sánchez) & Persona B (Yesid Bello) |

### 23.2 Matriz de calidad
- **Filas**: 20 localidades | **Variables**: `irca_promedio`, `clasificacion_riesgo_irca`, `muestras_analizadas`.
- **Estado**: **Aceptado**. Sustenta `PUB-002`.

---

## 24. Dominio 11: Servicios Públicos — Alumbrado Público UAESP

### 24.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Servicios Públicos Domiciliarios (D11) |
| Dataset | `data/raw/SERVICIOS_PUBLICOS/uaesp_alumbrado_publico_localidad.csv` |
| Entidad / fuente | Unidad Administrativa Especial de Servicios Públicos (UAESP) |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona A (Adan Sánchez) & Persona B (Yesid Bello) |

### 24.2 Matriz de calidad
- **Filas**: 20 localidades | **Variables**: `total_luminarias`, `tecnologia_led_pct`, `fallas_reportadas_mes`.
- **Estado**: **Aceptado**. Sustenta `PUB-003`.

---

## 25. Dominio 11: Servicios Públicos — Conectividad TIC

### 25.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Servicios Públicos Domiciliarios (D11) |
| Dataset | `data/raw/SERVICIOS_PUBLICOS/cobertura_conectividad_tic_localidad.csv` |
| Entidad / fuente | MinTIC / Alta Consejería Distrital de TIC |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona A (Adan Sánchez) & Persona B (Yesid Bello) |

### 25.2 Matriz de calidad
- **Filas**: 20 localidades | **Variables**: `penetracion_internet_fijo_pct`, `velocidad_promedio_bajada_mbps`.
- **Estado**: **Aceptado**. Sustenta `PUB-004`.

---

## 26. Dominio 12: Empleo / Economía — Conmutación Residencia-Trabajo

### 26.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Mercado Laboral y Salarios (D12) |
| Dataset | `data/raw/EMPLEO_ECONOMIA/conmutacion_laboral_residencia_trabajo_localidad.csv` |
| Entidad / fuente | Secretaría Distrital de Movilidad (SDM) / DANE |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona B (Yesid Bello) & Persona A (Adan Sánchez) |

### 26.2 Matriz de calidad
- **Filas**: 20 localidades.
- **Regla de Consistencia**: `% Autosuficiencia + % Conmutación Externa = 100.0%` (100% conforme).
- **Variables**: `ocupados_trabajan_en_su_localidad_pct`, `ocupados_conmutan_a_otras_localidades_pct`, `tiempo_promedio_desplazamiento_laboral_min`.
- **Estado**: **Aceptado**. Sustenta `EMP-001`.

---

## 27. Dominio 12: Empleo / Economía — Salarios e Informalidad GEIH

### 27.1 Identificación de la fuente
| Campo | Valor |
|---|---|
| Dominio | Mercado Laboral y Salarios (D12) |
| Dataset | `data/raw/EMPLEO_ECONOMIA/ingreso_promedio_salario_ocupados_localidad.csv` |
| Entidad / fuente | DANE (Gran Encuesta Integrada de Hogares - GEIH) / SDDE |
| Formato | CSV (UTF-8) |
| Vigencia | 2024 – 2025 |
| Responsable | Persona B (Yesid Bello) & Persona A (Adan Sánchez) |

### 27.2 Matriz de calidad
- **Filas**: 20 localidades | **Nulos**: 0.0%.
- **Variables**: `ingreso_laboral_promedio_ocupados_cop` ($1.28M a $4.20M COP), `tasa_informalidad_laboral_pct` (18.2% a 65.4%), `tasa_desempleo_pct`.
- **Estado**: **Aceptado**. Sustenta `EMP-002`.

---

## Síntesis Consolidada de Criterios de Calidad

| Total Datasets Auditados | Aceptados sin Observaciones | Aceptados con Ajuste Espacial | Rechazados | Cobertura Territorial Promedio |
| :---: | :---: | :---: | :---: | :---: |
| **27** | **26 (96.3%)** | **1 (3.7% - IPS Urgencias)** | **0 (0.0%)** | **100.0% (20 Localidades)** |
