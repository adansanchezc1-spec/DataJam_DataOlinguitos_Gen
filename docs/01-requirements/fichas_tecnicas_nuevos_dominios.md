# Fichas Técnicas de Datos — Dominios de Expansión SIPTA

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA — DataJam Bogotá)  
**Fase PDCO**: PLAN → DEVELOPMENT | **SDLC Stage**: Requirements & Data Architecture  
**Estándares**: IEEE 830 / ISO 29148 / DAMA-BOK / ISO/IEC 25010  
**Autores**: Persona A (Adan Sánchez), Persona B (Yesid Bello), Persona C (Sofía Hidalgo)  
**Fecha de Publicación**: 2026-08-18  

---

## 1. Dominio: Servicios Públicos Domiciliarios y Calidad (D11)

### 1.1 Ficha Técnica: Cobertura y Continuidad de Acueducto y Alcantarillado
- **Identificador**: `FT-PUB-001`
- **Dataset Crudo**: `data/raw/SERVICIOS_PUBLICOS/eaab_cobertura_acueducto_localidad.csv`
- **Entidad Rectora**: Empresa de Acueducto y Alcantarillado de Bogotá (EAAB - ESP) / Superintendencia de Servicios Públicos Domiciliarios (SSPD).
- **Periodicidad / Vigencia**: Anual (Corte 2024–2025).
- **Granularidad Territorial**: 20 Localidades canónicas de Bogotá D.C.
- **Variables Críticas**:
  - `cobertura_acueducto_pct` (Float, %): Porcentaje de predios conectados a la red matriz de acueducto.
  - `cobertura_alcantarillado_pct` (Float, %): Porcentaje de predios con evacuación de aguas residuales y pluviales.
  - `consumo_promedio_m3_suscriptor` (Float, $m^3$/mes): Volumen medio facturado por usuario residencial.
  - `horas_interrupcion_promedio_mes` (Float, Horas): Tiempo medio mensual de suspensión del servicio por racionamiento, contingencias o mantenimiento.
- **Reglas de Calidad DAMA-BOK**:
  - Cobertura $\in [0.0, 100.0]\%$.
  - Llave territorial foránea `codigo_localidad` única e íntegra en $[1, 20]$.
- **Indicador Respaldado**: `PUB-001` (Déficit de Continuidad y Acceso al Agua Potable).

---

### 1.2 Ficha Técnica: Calidad del Agua Potable (IRCA)
- **Identificador**: `FT-PUB-002`
- **Dataset Crudo**: `data/raw/SERVICIOS_PUBLICOS/eaab_calidad_agua_irca_localidad.csv`
- **Entidad Rectora**: Secretaría Distrital de Salud (SDS) — Laboratorio de Salud Pública / SIVICAP (MinSalud).
- **Periodicidad / Vigencia**: Mensual consolidado anual (2025).
- **Variables Críticas**:
  - `irca_promedio` (Float, Puntos 0 a 100): Índice de Riesgo de la Calidad del Agua según Resolución 2115 de 2007.
    - $0.0 - 5.0$: **Sin Riesgo** (Agua apta para consumo humano).
    - $5.1 - 14.0$: **Riesgo Bajo**.
    - $14.1 - 35.0$: **Riesgo Medio**.
  - `clasificacion_riesgo_irca` (String): Categoría cualitativa oficial.
- **Indicador Respaldado**: `PUB-002` (Riesgo Sanitario en Calidad del Agua).

---

### 1.3 Ficha Técnica: Alumbrado Público y Eficiencia Energética
- **Identificador**: `FT-PUB-003`
- **Dataset Crudo**: `data/raw/SERVICIOS_PUBLICOS/uaesp_alumbrado_publico_localidad.csv`
- **Entidad Rectora**: Unidad Administrativa Especial de Servicios Públicos (UAESP) — Subdirección de Alumbrado.
- **Variables Críticas**:
  - `total_luminarias` (Int): Inventario total de puntos luminosos en espacio público.
  - `tecnologia_led_pct` (Float, %): Porcentaje de luminarias modernizadas con tecnología LED de bajo consumo.
  - `fallas_reportadas_mes` (Int): Reportes de luminarias apagadas o intermitentes.
  - `tiempo_medio_reparacion_horas` (Float): Tiempo de respuesta de la cuadrilla técnica.
- **Indicador Respaldado**: `PUB-003` (Déficit de Iluminación Pública Segura).

---

### 1.4 Ficha Técnica: Conectividad Digital y TIC
- **Identificador**: `FT-PUB-004`
- **Dataset Crudo**: `data/raw/SERVICIOS_PUBLICOS/cobertura_conectividad_tic_localidad.csv`
- **Entidad Rectora**: Ministerio de Tecnologías de la Información y las Comunicaciones (MinTIC) / Alta Consejería Distrital de TIC.
- **Variables Críticas**:
  - `penetracion_internet_fijo_pct` (Float, %): Hogares con suscripción a internet fijo de banda ancha.
  - `velocidad_promedio_bajada_mbps` (Float, Mbps): Velocidad efectiva de descarga.
  - `zonas_wifi_publicas` (Int): Puntos de acceso público gratuito activos.
- **Indicador Respaldado**: `PUB-004` (Brecha de Inclusión Digital Territorial).

---

## 2. Dominio: Mercado Laboral, Salarios y Conmutación (D12)

### 2.1 Ficha Técnica: Matriz de Conmutación Residencia - Trabajo
- **Identificador**: `FT-EMP-001`
- **Dataset Crudo**: `data/raw/EMPLEO_ECONOMIA/conmutacion_laboral_residencia_trabajo_localidad.csv`
- **Entidad Rectora**: Secretaría Distrital de Movilidad (SDM) — Encuesta de Movilidad / DANE.
- **Variables Críticas**:
  - `ocupados_trabajan_en_su_localidad_pct` (Float, %): Tasa de autosuficiencia laboral local.
  - `ocupados_conmutan_a_otras_localidades_pct` (Float, %): Tasa de expulsión y dependencia de empleo externo.
  - `conmutacion_hacia_centro_ampliado_pct` (Float, %): Proporción de viajes laborales con destino a Chapinero, Santa Fe, Teusaquillo, Barrios Unidos y Usaquén.
  - `tiempo_promedio_desplazamiento_laboral_min` (Float, Minutos): Duración media del trayecto origen-destino.
- **Consistencia Lógica**: `% Trabajo Local + % Conmutación Externa = 100.0%`.
- **Indicador Respaldado**: `EMP-001` (Tasa de Dependencia y Conmutación Laboral Externa).

---

### 2.2 Ficha Técnica: Ingresos, Salarios e Informalidad Laboral
- **Identificador**: `FT-EMP-002`
- **Dataset Crudo**: `data/raw/EMPLEO_ECONOMIA/ingreso_promedio_salario_ocupados_localidad.csv`
- **Entidad Rectora**: DANE (Gran Encuesta Integrada de Hogares - GEIH) / Secretaría Distrital de Desarrollo Económico (SDDE).
- **Variables Críticas**:
  - `ingreso_laboral_promedio_ocupados_cop` (Int, Pesos COP): Ingreso medio mensual de la población ocupada.
  - `tasa_informalidad_laboral_pct` (Float, %): Ocupados que no cotizan a seguridad social en salud y pensión.
  - `tasa_desempleo_pct` (Float, %): Tasa de desocupación abierta local.
- **Indicador Respaldado**: `EMP-002` (Vulnerabilidad por Ingresos e Informalidad Laboral).

---

## 3. Dominio: Participación Ciudadana y Alertas Tempranas (D9)

### 3.1 Ficha Técnica: Requerimientos Ciudadanos (PQR Bogotá Te Escucha)
- **Identificador**: `FT-PAR-001`
- **Dataset Crudo**: `data/raw/PARTICIPACION_CIUDADANA/pqr_bogota_te_escucha_por_localidad.csv`
- **Entidad Rectora**: Secretaría General de la Alcaldía Mayor de Bogotá — Sistema Distrital de Quejas y Reclamos (SDQS).
- **Variables Críticas**:
  - `total_pqr_recibidas` (Int): Volumen bruto de peticiones, quejas, reclamos y solicitudes.
  - `pqr_resueltas_a_tiempo_pct` (Float, %): Eficacia de la respuesta institucional dentro del término legal (15 días hábiles).
  - `tema_frecuente_1`, `tema_frecuente_2`, `tema_frecuente_3` (String): Categorías de falla urbana más reportadas.
- **Indicador Respaldado**: `PAR-001` (Índice de Insatisfacción y Falla Urbana Ciudadana).

---

### 3.2 Ficha Técnica: Presupuestos Participativos
- **Identificador**: `FT-PAR-002`
- **Dataset Crudo**: `data/raw/FINANZAS_INVERSION_PUBLICA/presupuestos_participativos_propuestas_priorizadas.csv`
- **Entidad Rectora**: Secretaría Distrital de Gobierno — Plataforma de Participación Ciudadana.
- **Variables Críticas**:
  - `total_votantes_pp` (Int): Ciudadanos que ejercieron el voto en la priorización de proyectos locales.
  - `propuestas_priorizadas_aprobadas` (Int): Iniciativas ciudadanas con asignación presupuestal directa.
  - `inversion_presupuesto_participativo_millones` (Float, Millones COP): Recursos descentralizados asignados por decisión ciudadana.
- **Indicador Respaldado**: `PAR-002` (Alineación entre Demanda Social y Asignación de Presupuesto Participativo).

---

## 4. Dominio: Finanzas e Inversión Local (D7 Expandido)

### 4.1 Ficha Técnica: Fondos de Desarrollo Local (FDL)
- **Identificador**: `FT-FIN-002`
- **Dataset Crudo**: `data/raw/FINANZAS_INVERSION_PUBLICA/inversion_fondos_desarrollo_local_fdl.csv`
- **Entidad Rectora**: Secretaría Distrital de Gobierno / CONFIS Distrital / Mapa de Inversiones de Bogotá.
- **Variables Críticas**:
  - `presupuesto_aprobado_millones` (Float): Presupuesto total asignado a la Alcaldía Local.
  - `presupuesto_ejecutado_millones` (Float): Recursos comprometidos y girados en la vigencia fiscal.
  - `porcentaje_ejecucion_fdl` (Float, %): Eficiencia de ejecución presupuestal.
- **Indicador Respaldado**: `FIN-002` (Eficiencia y Desbalance en la Ejecución Presupuestal Local).

---

### 4.2 Ficha Técnica: Inversión Social y Asistencia (SDIS)
- **Identificador**: `FT-FIN-003`
- **Dataset Crudo**: `data/raw/FINANZAS_INVERSION_PUBLICA/metas_inversion_social_sdis_localidad.csv`
- **Entidad Rectora**: Secretaría Distrital de Integración Social (SDIS).
- **Variables Críticas**:
  - `presupuesto_social_sdis_millones` (Float, Millones COP): Gasto social focalizado.
  - `beneficiarios_transferencias_monetarias` (Int): Hogares receptores del Ingreso Mínimo Garantizado (IMG).
  - `comedores_comunitarios_activos` (Int): Puntos de asistencia y seguridad alimentaria.
- **Indicador Respaldado**: `FIN-003` (Cobertura de Red de Seguridad Social y Asistencia).

---

## 5. Dominios Sectoriales Expandidos (D2, D3, D8, D10)

| Dominio | Dataset | Entidad Rectora | Variables Clave | Indicador SIPTA |
| :--- | :--- | :--- | :--- | :---: |
| **Salud (D2)** | `SALUD/capacidad_camas_asistencial_localidad.csv` | SDS / REPS | `total_camas_hospitalarias`, `camas_por_10000_habitantes`, `camas_uci_adultos` | `SAL-002` |
| **Educación (D3)** | `EDUCACION/calidad_educativa_saber11_retencion_localidad.csv` | SED / ICFES | `puntaje_promedio_saber_11`, `tasa_desercion_escolar_pct`, `relacion_estudiantes_por_docente` | `EDU-003` |
| **Seguridad (D8)** | `SEGURIDAD/delitos_alto_impacto_localidad_2024_2026.csv` | MEBOG / SDSCJ | `homicidios_anual`, `hurto_a_personas_anual`, `tasa_delitos_alto_impacto_por_100k_hab` | `SEG-002` |
| **Cartografía (D10)**| `MODELO_TERRITORIAL/poligonos_localidades.geojson` | IDECA / Catastro | Geometría `MultiPolygon` WGS84, `LOCCODIGO` (1-20), `LOCNOMBRE` | `GEO-001` |
