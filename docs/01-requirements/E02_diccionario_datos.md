# E02 — Diccionario Maestro de Datos Analizados
**Proyecto**: SIPTA (Sistema de Indicadores y Priorización Territorial y Alertas Tempranas) — DataJam Bogotá  
**Fase PDCO**: PLAN → DEVELOPMENT | **SDLC Stage**: Requirements / Data Design  
**Estándar**: IEEE 830 / ISO 29148 / DAMA-BOK  
**Responsables**: 
- Persona A (Adan Sánchez — Scrum Master & Lead Data Engineer)
- Persona B (Yesid Bello — Data Scientist & Territorial Analyst)  
- Persona C (Sofía Hidalgo — Tech Lead & BI Developer / Ingesta & QA)
**Última Actualización**: 2026-08-18  

---

## 1. Esquema Técnico de Servicios Públicos (D11)

### 1.1 Dataset: `SERVICIOS_PUBLICOS/eaab_cobertura_acueducto_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad (1 a 20) | Entero [1, 20] | No nulo, clave foránea |
| `nombre_localidad` | `object` | Nombre canónico de la localidad | 20 nombres oficiales | No nulo |
| `codigo_divipola` | `int64` | Código DANE DIVIPOLA | [1100101, 1100120] | No nulo |
| `cobertura_acueducto_pct` | `float64` | Porcentaje de cobertura de acueducto | Real [0.0, 100.0] | Cobertura distrital > 95% |
| `cobertura_alcantarillado_pct` | `float64` | Porcentaje de cobertura de alcantarillado | Real [0.0, 100.0] | Cobertura distrital > 90% |
| `horas_interrupcion_promedio_mes` | `float64` | Horas de interrupción de servicio al mes | Real $\ge 0.0$ | Indicador de continuidad |

### 1.2 Dataset: `SERVICIOS_PUBLICOS/eaab_calidad_agua_irca_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código oficial de localidad | Entero [1, 20] | No nulo |
| `irca_promedio` | `float64` | Índice de Riesgo de la Calidad del Agua | Real [0.0, 100.0] | $< 5.0$ = Apta para consumo |
| `clasificacion_riesgo_irca` | `object` | Clasificación normativa del riesgo SIVICAP | `Sin Riesgo (Apta)`, `Riesgo Bajo` | Texto controlado |

---

## 2. Esquema Técnico de Inversión FDL y Gasto Social (D7)

### 2.1 Dataset: `FINANZAS_INVERSION_PUBLICA/inversion_fondos_desarrollo_local_fdl.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `codigo_localidad` | `int64` | Código de localidad (1 a 20) | Entero [1, 20] | No nulo |
| `presupuesto_aprobado_millones` | `float64` | Presupuesto total aprobado para el FDL | Millones COP ($> 0$) | No nulo |
| `presupuesto_ejecutado_millones` | `float64` | Presupuesto efectivamente comprometido y ejecutado | Millones COP ($\ge 0$) | $\le$ presupuesto aprobado |
| `porcentaje_ejecucion_fdl` | `float64` | Tasa de ejecución presupuestal del FDL | Real [0.0, 100.0] % | Métrica de eficiencia |

### 2.2 Dataset: `FINANZAS_INVERSION_PUBLICA/metas_inversion_social_sdis_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `presupuesto_social_sdis_millones`| `float64` | Gasto social territorializado de integración | Millones COP ($> 0$) | No nulo |
| `beneficiarios_transferencias_monetarias` | `int64` | Familias receptoras de transferencias (IMV) | Entero $\ge 0$ | Población vulnerable |
| `comedores_comunitarios_activos` | `int64` | Equipamientos de seguridad alimentaria | Entero $\ge 0$ | Conteo de comedores |

---

## 3. Esquema Técnico de Mercado Laboral, Salarios y Conmutación (D12)

### 3.1 Dataset: `EMPLEO_ECONOMIA/conmutacion_laboral_residencia_trabajo_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `ocupados_trabajan_en_su_localidad_pct` | `float64` | % Ocupados con empleo dentro de su localidad | Real [0.0, 100.0] | Índice de autosuficiencia |
| `ocupados_conmutan_a_otras_localidades_pct`| `float64` | % Ocupados que viajan a trabajar a otra localidad | Real [0.0, 100.0] | Suma con autosuficiencia = 100% |
| `tiempo_promedio_desplazamiento_laboral_min` | `float64` | Tiempo promedio de viaje de la casa al trabajo | Minutos ($> 0$) | Métrica de calidad de vida |

### 3.2 Dataset: `EMPLEO_ECONOMIA/ingreso_promedio_salario_ocupados_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `ingreso_laboral_promedio_ocupados_cop` | `float64` | Ingreso promedio mensual de los ocupados | Pesos COP ($> 0$) | GEIH / DANE |
| `tasa_informalidad_laboral_pct` | `float64` | Proporción de trabajadores informales | Real [0.0, 100.0] % | DANE |
| `tasa_desempleo_pct` | `float64` | Tasa de desocupación laboral local | Real [0.0, 100.0] % | DANE |

---

## 4. Esquema Técnico de Participación Ciudadana y PQR (D9)

### 4.1 Dataset: `PARTICIPACION_CIUDADANA/pqr_bogota_te_escucha_por_localidad.csv`
| Atributo | Tipo Técnico | Descripción Semántica | Valores Admisibles | Reglas de Calidad |
| :--- | :--- | :--- | :--- | :--- |
| `total_pqr_recibidas` | `int64` | Peticiones, quejas y reclamos ciudadanos | Entero $\ge 0$ | Sistema Bogotá Te Escucha |
| `pqr_resueltas_a_tiempo_pct` | `float64` | Eficacia en el tiempo de respuesta institucional | Real [0.0, 100.0] % | Métrica de gestión pública |
| `tema_frecuente_1` | `object` | Causa principal de peticiones ciudadanas | Texto (Malla vial, aseo, etc.) | No nulo |
