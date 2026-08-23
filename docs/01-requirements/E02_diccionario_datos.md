# E02 — Diccionario Maestro de Datos Analizados
**Proyecto**: SIPTA (Sistema de Indicadores y Priorización Territorial y Alertas Tempranas) — DataJam Bogotá  
**Fase PDCO**: PLAN → DEVELOPMENT → CONTROL | **SDLC Stage**: Requirements / Data Architecture  
**Estándar**: IEEE 830 / ISO 29148 / DAMA-BOK / ISO/IEC 25010  
**Responsables**: 
- Persona A (Adan Sánchez — Scrum Master & Lead Data Engineer)
- Persona B (Yesid Bello — Data Scientist & Territorial Analyst)  
- Persona C (Sofía Hidalgo — Tech Lead & BI Developer / Ingesta & QA)
**Última Actualización**: 2026-08-19  

---

## 0. Dimensión Canónica Territorial (Claves Primarias y Geográficas)

| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código numérico oficial de la localidad (1 a 20) | Entero [1, 20] | Clave primaria (`PK`), no nulo, $> 0$ |
| `nombre_localidad` | `object` | Nombre canónico oficial en mayúsculas sostenidas | 20 nombres oficiales | Homologado con `MAPA_HOMOLOGACION_LOCALIDADES` |
| `codigo_divipola` | `int64` | Código DANE DIVIPOLA para Bogotá D.C. | [1100101, 1100120] | Integridad geoespacial distrital |
| `area_km2` | `float64` | Superficie territorial oficial en $km^2$ | Real [2.06, 780.96] | Fuente SDP / IDECA (`AREAS_LOCALIDADES_KM2`) |

---

## 1. Esquema Técnico de Demografía y Población (D1)

### 1.1 Dataset: `DEMOGRAFIA/osb_demografia-poblacion-localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | Clave foránea, no nulo |
| `poblacion` | `float64` | Población total proyectada para el año objetivo | Real $> 0$ | SDP-DANE CNPV 2018 |
| `densidad_poblacional` | `float64` | Densidad de habitantes por $km^2$ | Real $> 0$ | Calculado: `poblacion / area_km2` |
| `pob_infanto_juvenil_pct` | `float64` | Proporción de población de 0 a 17 años | Real [0.0, 100.0] % | Base para cálculo de demanda escolar |

---

## 2. Esquema Técnico de Salud y Capacidad Asistencial (D2)

### 2.1 Dataset: `SALUD/capacidad_camas_asistencial_localidad.csv` / `SALUD/osb_ofertasrv-ips-urgencias.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | Clave foránea |
| `total_camas_hospitalarias` | `int64` | Camas totales de internación hospitalaria | Entero $\ge 0$ | Registro REPS / SaluData |
| `camas_uci_adultos` | `int64` | Camas hospitalarias de alta complejidad / UCI | Entero $\ge 0$ | Capacidad crítica hospitalaria |
| `camas_por_10000_habitantes`| `float64` | Tasa asistencial hospitalaria por 10k hab | Real $\ge 0.0$ | `(total_camas / poblacion) * 10000` |
| `tasa_ips_urgencias_10k` | `float64` | IPS con urgencias activas por 10k hab | Real $\ge 0.0$ | Asignación espacial WGS84 |

---

## 3. Esquema Técnico de Educación y Cobertura (D3)

### 3.1 Dataset: `EDUCACION/calidad_educativa_saber11_retencion_localidad.csv` / `EDUCACION/ofertacupos_032025.geojson`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | Clave foránea |
| `puntaje_promedio_saber_11` | `float64` | Puntaje global promedio en pruebas Saber 11 | Real [0.0, 500.0] | Fuente SED / ICFES |
| `tasa_desercion_escolar_pct`| `float64` | Porcentaje de deserción escolar anual | Real [0.0, 100.0] % | Indicador de vulnerabilidad juvenil |
| `colegios_jornada_unica_pct`| `float64` | Proporción de sedes en Jornada Única | Real [0.0, 100.0] % | Política de jornada completa |
| `sedes_educativas_1k_ninos` | `float64` | Sedes oficiales por cada 1.000 menores de edad | Real $\ge 0.0$ | `(sedes_oficiales / pob_0_17) * 1000` |

---

## 4. Esquema Técnico de Movilidad y Transporte Masivo (D4)

### 4.1 Dataset: `MOVILIDAD/flota_vinculada_sitp_2024-12.csv` / `MOVILIDAD/paraderos_zonales_sitp.gpkg`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | Clave foránea |
| `total_paraderos_sitp` | `int64` | Conteo de paraderos zonales SITP | Entero $\ge 0$ | Malla de paraderos TransMilenio |
| `total_estaciones_troncales_tm` | `int64` | Conteo de estaciones troncales activas | Entero $\ge 0$ | Infraestructura de alta capacidad |
| `paraderos_por_10k_hab` | `float64` | Densidad de paraderos zonales por 10k hab | Real $\ge 0.0$ | `(total_paraderos / poblacion) * 10000` |

---

## 5. Esquema Técnico de Infraestructura y Espacio Público (D5)

### 5.1 Dataset: `INFRAESTRUCTURA_ESPACIO_PUBLICO/5.-parques-idrd.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | Clave foránea |
| `total_parques_idrd` | `int64` | Total parques distritales (bolsillo, vecinal, zonal, metro) | Entero $\ge 0$ | Inventario IDRD |
| `parques_por_10k_hab` | `float64` | Dotación de parques por cada 10.000 hab | Real $\ge 0.0$ | `(total_parques / poblacion) * 10000` |

---

## 6. Esquema Técnico de Ambiente y Sostenibilidad (D6)

### 6.1 Dataset: `AMBIENTE/situacion_ambiental_conflictiva.csv` / `AMBIENTE/estacion_calidad_aire.geojson`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | Clave foránea |
| `densidad_conflictos_sac_10k` | `float64` | Conflictos ambientales activos (SAC) por 10k hab | Real $\ge 0.0$ | Monitoreo SDA / IDECA |
| `estaciones_rmcab_activas` | `int64` | Estaciones fijas de la red de calidad del aire | Entero $\ge 0$ | Red RMCAB activa (PM2.5 / PM10) |

---

## 7. Esquema Técnico de Finanzas, Inversión Pública y Economía Social (D7)

### 7.1 Dataset: `FINANZAS_INVERSION_PUBLICA/inversion_fondos_desarrollo_local_fdl.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código de localidad (1 a 20) | Entero [1, 20] | No nulo |
| `presupuesto_aprobado_millones` | `float64` | Presupuesto total aprobado para el FDL | Millones COP ($> 0$) | No nulo |
| `presupuesto_ejecutado_millones` | `float64` | Presupuesto efectivamente comprometido y ejecutado | Millones COP ($\ge 0$) | $\le$ presupuesto aprobado |
| `porcentaje_ejecucion_fdl` | `float64` | Tasa de ejecución presupuestal del FDL | Real [0.0, 100.0] % | Métrica de eficiencia de gasto |
| `inversion_fdl_per_capita_millones`| `float64` | Inversión local ejecutada por habitante | Real $\ge 0.0$ | `presupuesto_ejecutado / poblacion` |

### 7.2 Dataset: `FINANZAS_INVERSION_PUBLICA/metas_inversion_social_sdis_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `presupuesto_social_sdis_millones`| `float64` | Gasto social territorializado de integración | Millones COP ($> 0$) | No nulo |
| `beneficiarios_transferencias_monetarias` | `int64` | Familias receptoras de transferencias (IMG/IMV) | Entero $\ge 0$ | Población vulnerable focalizada |
| `comedores_comunitarios_activos` | `int64` | Equipamientos de seguridad alimentaria | Entero $\ge 0$ | Conteo de comedores comunitarios |

### 7.3 Dataset: `FINANZAS_INVERSION_PUBLICA/vendedores_informales_consolidado.csv` (RIVI IPES)
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código de localidad | Entero [1, 20] | Clave foránea |
| `numero_vendedores` | `int64` | Vendedores informales censados en espacio público | Entero $\ge 0$ | Censo oficial RIVI |
| `presion_vendedores_rivi_10k`| `float64` | Densidad de comercio informal por 10k hab | Real $\ge 0.0$ | `(numero_vendedores / poblacion) * 10000` |

---

## 8. Esquema Técnico de Seguridad y Convivencia (D8)

### 8.1 Dataset: `SEGURIDAD/delitos_alto_impacto_localidad_2024_2026.csv` / `SEGURIDAD/Cuadrante de Policía. Bogotá D.C.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | Clave foránea |
| `homicidios_anual` | `int64` | Total de homicidios registrados en el año | Entero $\ge 0$ | SIEDCO / MEBOG |
| `hurto_a_personas_anual` | `int64` | Denuncias anuales de hurto a personas | Entero $\ge 0$ | SIEDCO / MEBOG |
| `tasa_delitos_alto_impacto_por_100k_hab`| `float64`| Tasa consolidada de criminalidad por 100k hab | Real $\ge 0.0$ | SIEDCO |
| `tasa_homicidios_por_100k_hab_calc`| `float64` | Tasa de homicidios calculada por 100k hab | Real $\ge 0.0$ | `(homicidios / poblacion) * 100000` |
| `cuadrantes_policia_100k` | `float64` | Cobertura de cuadrantes policiales por 100k hab | Real $\ge 0.0$ | MNVCC (599 cuadrantes distritales) |

---

## 9. Esquema Técnico de Participación Ciudadana y PQR (D9)

### 9.1 Dataset: `PARTICIPACION_CIUDADANA/pqr_bogota_te_escucha_por_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | Clave foránea |
| `total_pqr_recibidas` | `int64` | Peticiones, quejas y reclamos ciudadanos | Entero $\ge 0$ | Sistema Bogotá Te Escucha (SDQS) |
| `pqr_resueltas_a_tiempo_pct` | `float64` | Eficacia en el tiempo de respuesta institucional | Real [0.0, 100.0] % | Métrica de gestión pública |
| `pqr_por_10k_hab` | `float64` | Tasa de requerimientos ciudadanos por 10k hab | Real $\ge 0.0$ | `(total_pqr / poblacion) * 10000` |
| `tema_frecuente_1` | `object` | Causa principal de peticiones ciudadanas | Texto controlado | Malla vial, aseo, alumbrado, etc. |

---

## 10. Esquema Técnico de Modelo Territorial Espacial (D10)

### 10.1 Dataset: `MODELO_TERRITORIAL/poligonos_localidades.geojson`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `LOCCODIGO` | `object` / `int64` | Identificador de localidad IDECA | [1, 20] | Llave geoespacial |
| `LOCNOMBRE` | `object` | Nombre oficial distrital | 20 nombres | Mayúsculas sostenidas |
| `geometry` | `geometry` | Polígono vectorial de delimitación territorial | MultiPolygon WGS84 | EPSG:4326 |

---

## 11. Esquema Técnico de Servicios Públicos Domiciliarios y TIC (D11)

### 11.1 Dataset: `SERVICIOS_PUBLICOS/eaab_cobertura_acueducto_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad (1 a 20) | Entero [1, 20] | No nulo, clave foránea |
| `cobertura_acueducto_pct` | `float64` | Porcentaje de cobertura de acueducto | Real [0.0, 100.0] % | Cobertura distrital > 95% |
| `cobertura_alcantarillado_pct` | `float64` | Porcentaje de cobertura de alcantarillado | Real [0.0, 100.0] % | Cobertura distrital > 90% |
| `horas_interrupcion_promedio_mes` | `float64` | Horas de interrupción de servicio al mes | Real $\ge 0.0$ | Indicador de continuidad EAAB |

### 11.2 Dataset: `SERVICIOS_PUBLICOS/eaab_calidad_agua_irca_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | Clave foránea |
| `irca_promedio` | `float64` | Índice de Riesgo de la Calidad del Agua | Real [0.0, 100.0] | $< 5.0$ = Apta para consumo humano |
| `clasificacion_riesgo_irca` | `object` | Clasificación normativa del riesgo SIVICAP | `Sin Riesgo (Apta)`, `Riesgo Bajo` | Texto controlado |

### 11.3 Dataset: `SERVICIOS_PUBLICOS/uaesp_alumbrado_publico_localidad.csv` / `cobertura_conectividad_tic_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `total_luminarias` | `int64` | Conteo de luminarias públicas instaladas | Entero $> 0$ | Inventario UAESP |
| `tecnologia_led_pct` | `float64` | Proporción de alumbrado modernizado a LED | Real [0.0, 100.0] % | Eficiencia energética |
| `penetracion_internet_fijo_pct` | `float64` | Porcentaje de hogares con internet de banda ancha | Real [0.0, 100.0] % | MinTIC / Brecha digital |

---

## 12. Esquema Técnico de Mercado Laboral, Salarios y Conmutación (D12)

### 12.1 Dataset: `EMPLEO_ECONOMIA/conmutacion_laboral_residencia_trabajo_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código de localidad | Entero [1, 20] | Clave foránea |
| `ocupados_trabajan_en_su_localidad_pct` | `float64` | % Ocupados con empleo dentro de su localidad | Real [0.0, 100.0] % | Índice de autosuficiencia |
| `ocupados_conmutan_a_otras_localidades_pct`| `float64` | % Ocupados que viajan a trabajar a otra localidad | Real [0.0, 100.0] % | Suma con autosuficiencia = 100% |
| `tiempo_promedio_desplazamiento_laboral_min` | `float64` | Tiempo promedio de viaje de la casa al trabajo | Minutos ($> 0$) | Métrica de movilidad y calidad de vida |

### 12.2 Dataset: `EMPLEO_ECONOMIA/ingreso_promedio_salario_ocupados_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código de localidad | Entero [1, 20] | Clave foránea |
| `ingreso_laboral_promedio_ocupados_cop` | `float64` | Ingreso promedio mensual de los ocupados | Pesos COP ($> 0$) | GEIH / DANE |
| `tasa_informalidad_laboral_pct` | `float64` | Proporción de trabajadores sin seguridad social | Real [0.0, 100.0] % | Indicador de vulnerabilidad económica |
| `tasa_desempleo_pct` | `float64` | Tasa de desocupación laboral local | Real [0.0, 100.0] % | DANE GEIH |
