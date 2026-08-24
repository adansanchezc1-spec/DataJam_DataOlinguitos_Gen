# SIPTA — Inventario Maestro de Indicadores Territoriales (v2.6.0)

**Fase PDCO**: PLAN → DEVELOPMENT | **SDLC Stage**: Requirements & Data Modeling  
**Estándar**: DAMA-BOK (Metadata Management), IEEE 830 / ISO 29148, OECD/JRC  
**Autores**: Persona A (Adan Sánchez), Persona B (Yesid Bello), Persona C (Sofía Hidalgo), Senior Software Engineer Agent, Chief Statistical Reviewer Agent  

---

## 1. Propósito y Gobernanza

Este documento consolida el **catálogo maestro y oficial de indicadores calculados, validados y auditados** para el proyecto **SIPTA**, garantizando trazabilidad técnica, definición matemática en $\LaTeX$, unidades de medida, fuentes rectoras y polaridad analítica.

---

## 2. Clasificación Sectorial de Códigos

| Prefijo | Dominio Sectorial | Entidad Fuente Principal | Total Indicadores |
|---|---|---|:---:|
| `DEM` | Demografía y Población | SDP / DANE | 2 |
| `SAL` | Salud y Capacidad Asistencial | SDS / REPS | 2 |
| `EDU` | Educación y Logro Académico | SED / ICFES | 2 |
| `MOV` | Movilidad y Transporte | TransMilenio S.A. / SDM | 3 |
| `INF` | Infraestructura y Espacio Público | IDRD | 2 |
| `AMB` | Ambiente y Sostenibilidad | SDA / SAC | 2 |
| `FIN` | Finanzas e Inversión Local | Secretaría de Gobierno / FDL | 2 |
| `VUL` | Vulnerabilidad Social y RIVI | IPES / SDIS | 2 |
| `SEG` | Seguridad y Convivencia | MEBOG / SCJ | 2 |
| `PUB` | Servicios Públicos Domiciliarios | EAAB / Superservicios | 2 |
| `EMP` | Mercado Laboral y Salarios | DANE (GEIH) | 2 |
| `PAR` | Participación Ciudadana y PQR | Secretaría General / SDQS | 2 |
| `EST` | Estimadores y Métricas de Rigor | Auditoría Estadística SIPTA | 5 |

---

## 3. Catálogo Maestro de Indicadores Operativos

| Código | Indicador | Entidad Fuente | Unidad | Fórmula $\LaTeX$ | Polaridad IPT | Estado |
|:---:|---|---|---|---|:---:|:---:|
| `DEM-001` | Densidad Poblacional | SDP / DANE | hab/km² | $\text{Densidad} = \frac{\text{Población}}{\text{Área km}^2}$ | Contexto | ✅ Implementado |
| `DEM-002` | Población Total Proyectada | SDP / DANE | habitantes | Conteo censal proyectado | Contexto | ✅ Implementado |
| `SAL-001` | Sedes IPS por 10.000 Hab. | SDS / REPS | sedes / 10k hab | $\text{IPS/10k} = \frac{\text{Sedes IPS}}{\text{Población}} \times 10\,000$ | Inversa | ✅ Implementado |
| `SAL-002` | Camas Hospitalarias / 10k | SDS / REPS | camas / 10k hab | $\text{Camas/10k} = \frac{\text{Camas Total}}{\text{Población}} \times 10\,000$ | Inversa | ✅ Implementado |
| `EDU-001` | Oferta Cupos / 1.000 Pob 5-17 | SED | cupos / 1k niños | $\text{Cupos/1k} = \frac{\text{Cupos Regulares}}{\text{Pob 5-17}} \times 1\,000$ | Inversa | ✅ Implementado |
| `EDU-002` | Puntaje Global Saber 11 | ICFES | puntos [0, 500] | Promedio ponderado de pruebas | Inversa | ✅ Implementado |
| `MOV-001` | Densidad Estaciones TransMilenio| TransMilenio S.A.| est / km² | $\text{Dens Est} = \frac{\text{Estaciones Troncales}}{\text{Área km}^2}$ | Inversa | ✅ Implementado |
| `MOV-002` | Densidad Paraderos SITP | TransMilenio S.A.| par / km² | $\text{Dens Par} = \frac{\text{Paraderos Zonales}}{\text{Área km}^2}$ | Inversa | ✅ Implementado |
| `MOV-003` | Tiempo Promedio de Viaje | SDM | minutos | Tiempo medio residencia-trabajo | Directa | ✅ Implementado |
| `INF-001` | Parques IDRD / 10.000 Hab. | IDRD | parques / 10k hab | $\text{Parques/10k} = \frac{\text{Parques IDRD}}{\text{Población}} \times 10\,000$ | Inversa | ✅ Implementado |
| `INF-002` | Inventario Total de Parques | IDRD | parques | Conteo georreferenciado | Inversa | ✅ Implementado |
| `AMB-001` | Conflictos Ambientales / km² | SDA / SAC | eventos / km² | $\text{SAC/km}^2 = \frac{\text{Conflictos SAC}}{\text{Área km}^2}$ | Directa | ✅ Implementado |
| `AMB-002` | Total Situaciones SAC | SDA / SAC | eventos | Conteo de incidentes | Directa | ✅ Implementado |
| `FIN-001` | Inversión FDL per cápita | Sec. Gobierno | COP / hab | $\text{FDL/hab} = \frac{\text{Presupuesto FDL}}{\text{Población}}$ | Inversa | ✅ Implementado |
| `FIN-002` | Tasa de Ejecución FDL | Sec. Gobierno | porcentaje % | $\text{Ejecución} = \frac{\text{Compromisos}}{\text{Apropiación}} \times 100$ | Inversa | ✅ Implementado |
| `VUL-001` | Vendedores RIVI / 10.000 Hab. | IPES / RIVI | reg / 10k hab | $\text{RIVI/10k} = \frac{\text{Registros RIVI}}{\text{Población}} \times 10\,000$ | Directa | ✅ Implementado |
| `VUL-002` | Beneficiarios Subsidios SDIS | SDIS | personas | Conteo programas sociales | Directa | ✅ Implementado |
| `SEG-001` | Cuadrantes MEBOG / 10.000 Hab. | MEBOG / SCJ | cuad / 10k hab | $\text{Cuad/10k} = \frac{\text{Cuadrantes MEBOG}}{\text{Población}} \times 10\,000$ | Inversa | ✅ Implementado |
| `SEG-002` | Tasa Homicidios / 100.000 Hab. | SCJ - SIEDCO | hom / 100k hab | $\text{Hom/100k} = \frac{\text{Homicidios}}{\text{Población}} \times 100\,000$ | Directa | ✅ Implementado |
| `PUB-001` | Índice Riesgo Agua (IRCA) | EAAB / SIVICAP | índice [0, 100] | $\text{IRCA} = \sum \text{Puntaje Parámetros}$ | Directa | ✅ Implementado |
| `PUB-002` | Cobertura Acueducto | EAAB | porcentaje % | $\text{Cob} = \frac{\text{Suscriptores}}{\text{Viviendas}} \times 100$ | Inversa | ✅ Implementado |
| `EMP-001` | Tasa Conmutación Laboral | DANE | porcentaje % | $\text{Tasa Conm} = \frac{\text{Viajes Trabajo Salientes}}{\text{Población Ocupada}} \times 100$ | Directa | ✅ Implementado |
| `EMP-002` | Salario Promedio Mensual | DANE | COP | Ingreso laboral mediano | Inversa | ✅ Implementado |
| `PAR-001` | Peticiones PQR / 10.000 Hab. | Sec. General | PQR / 10k hab | $\text{PQR/10k} = \frac{\text{Peticiones SDQS}}{\text{Población}} \times 10\,000$ | Directa | ✅ Implementado |
| `PAR-002` | Tasa de Oportunidad PQR | Sec. General | porcentaje % | $\text{Oportunidad} = \frac{\text{PQR a Tiempo}}{\text{PQR Totales}} \times 100$ | Inversa | ✅ Implementado |

---

## 4. Métricas de Rigor Estadístico y Auditoría Cuantitativa (OCDE/JRC)

| Código | Métrica / Estimador | Dominio | Fórmula $\LaTeX$ | Umbral de Aceptación | Estado |
|:---:|---|---|---|---|:---:|
| `EST-001` | Factor Inflación Varianza (VIF) | Colinealidad | $\text{VIF}_j = \frac{1}{1 - R_j^2}$ | $\text{VIF} < 10.0$ ($\overline{\text{VIF}} = 3.21$) | ✅ Certificado |
| `EST-002` | IPT Agregación Geométrica | Compensabilidad | $\text{IPT}_{\text{Geom}} = 100 \left(\prod (s_d + \epsilon)^{w_d}\right) - 100\epsilon$ | Correlación $\rho = 0.962$ con lineal | ✅ Certificado |
| `EST-003` | Intervalos Bootstrap al 95% | Incertidumbre | $\text{IC}_{95\%} = [Q_{0.025}(\text{IPT}^*), Q_{0.975}(\text{IPT}^*)]$ | $\Delta \text{IC} < 15.0$ pts | ✅ Certificado |
| `EST-004` | Marshall Bayes Smoother | Tasas en $N < 10\text{k}$ | $\tilde{r}_i = w_i r_i + (1 - w_i) \mu$ | Varianza estabilizada | ✅ Certificado |
| `EST-005` | Moran's I Espacial Global | Dependencia Espacial | $I = \frac{N}{S_0} \frac{\sum \sum w_{ij}(x_i - \bar{x})(x_j - \bar{x})}{\sum (x_i - \bar{x})^2}$ | $I = +0.4124$ ($p = 0.0080$) | ✅ Certificado |