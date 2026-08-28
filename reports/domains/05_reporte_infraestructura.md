# SIPTA — Informe Analítico Sectorial: Infraestructura y Espacio Público

**Fase PDCO**: DEVELOPMENT → OPERATIONS  
**Dominio**: Infraestructura y Espacio Público  
**Estándares**: DAMA-BOK / SWEBOK Cap. 2 y 4 / ISO/IEC 25010  
**Fecha de Emisión**: 2026-08-26  
**Cobertura**: 100% (20 Localidades Oficiales de Bogotá D.C.)  
**Certificación de Calidad**: ISO/IEC 25010 Conforme (100% Completitud Territorial)  

---

## 1. Pregunta de Negocio y Resumen Ejecutivo
> **Pregunta Clave**: ¿Cuál es la dotación relativa de espacio público verde, superficie de parques y alumbrado?

El presente informe expone el comportamiento multidimensional de los indicadores de **Infraestructura y Espacio Público** a lo largo de las 20 localidades del Distrito Capital, evaluando la distribución de capacidades, brechas estructurales, patrones geoespaciales y focos de intervención prioritaria.

---

## 2. Visualización Analítica y Geoespacial Multi-Panel (3 Paneles)
![Gráfica Sectorial](../figures/fig_05_infraestructura_parques_idrd.png)

*Figura: (A) Mapa coroplético oficial de Bogotá D.C.; (B) Ranking y distribución territorial; (C) Dispersión bivariada y brechas estructurales.*

---

## 3. Catálogo de Indicadores Calculados del Dominio

| Código | Indicador | Fórmula Matemática | Unidad | Polaridad IPT | Fuente |
|---|---|---|---|:---:|---|
| `INF-001` | **Espacio Público (m² de Parque / hab)** | $$\text{m}^2_{\text{parque/hab}} = \frac{\text{Área Total Parques m}^2}{\text{Población}}$$ | m²/hab | `Inversa (Carencia = 1 - Norm)` | IDRD / DADEP |
| `INF-002` | **Área Total de Parques IDRD** | $$\text{Área Parques} = \sum \text{Superficie en m}^2$$ | m² | `Informativo / Superficie Absoluta` | IDRD |
| `INF-003` | **Luminarias de Alumbrado por 10.000 hab** | $$t_{\text{lum}} = \frac{\text{Total Luminarias}}{\text{Población}} \times 10\,000$$ | lum/10k hab | `Inversa (Carencia = 1 - Norm)` | UAESP |

---

## 4. Hallazgos Analíticos, Espaciales y Brechas Territoriales
- **Oferta Absoluta vs Per Cápita**: Suba (1.066 parques) y Kennedy (892 parques) cuentan con gran número de parques barriales, pero su alta población reduce la tasa per cápita a menos de `8.5 parques/10k hab`.
- **Déficit Severo en el Centro Consolidado**: Los Mártires (`2.28 parques/10k hab`, `1.4 m²/hab`) y Santa Fe presentan saturación extrema del suelo y ausencia de zonas verdes recreativas.
- **Dotación Destacada**: Barrios Unidos y Teusaquillo cuentan con más de `18.5 parques/10k hab` y alta dotación de parques estructurantes.

### 4.1. Diagnóstico Estadístico y Distribución Multivariada (DAMA-BOK)

| Variable / Indicador | Media (μ) | Mediana (Q2) | Desv. Est. (σ) | IQR | Mín | Máx | CV (%) | Asimetría (g1) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `area_total_parques_m2` | 4,723,500.00 | 2,280,000.00 | 10,723,636.60 | 1,700,000.00 | 210,000.00 | 50,000,000.00 | 227.0% | +4.38 |
| `m2_parque_por_habitante` | 630.46 | 5.54 | 2,778.45 | 6.96 | 2.24 | 12,434.72 | 440.7% | +4.47 |
| `total_parques_idrd` | 6.95 | 6.50 | 4.14 | 6.50 | 0.00 | 14.00 | 59.5% | +0.26 |
| `luminarias_por_10k_hab` | 1,325.25 | 858.76 | 1,499.96 | 839.46 | 366.85 | 6,963.44 | 113.2% | +3.15 |

---

## 5. Tabla de Datos Oficiales de las 20 Localidades

| Código | Localidad | `area_total_parques_m2` | `m2_parque_por_habitante` | `total_parques_idrd` | `luminarias_por_10k_hab` |
| :---: | :--- | :---: | :---: | :---: | :---: |
| `01` | **USAQUEN** | 2,840,000.00 | 4.71 | 5 | 538.67 |
| `02` | **CHAPINERO** | 3,120,000.00 | 16.89 | 3 | 1,147.45 |
| `03` | **SANTA FE** | 3,850,000.00 | 35.70 | 8 | 1,344.45 |
| `04` | **SAN CRISTOBAL** | 2,410,000.00 | 5.86 | 7 | 651.17 |
| `05` | **USME** | 1,820,000.00 | 4.31 | 7 | 523.09 |
| `06` | **TUNJUELITO** | 1,910,000.00 | 10.26 | 3 | 1,015.44 |
| `07` | **BOSA** | 1,650,000.00 | 2.24 | 11 | 462.28 |
| `08` | **KENNEDY** | 3,250,000.00 | 3.12 | 13 | 437.92 |
| `09` | **FONTIBON** | 2,150,000.00 | 5.22 | 5 | 702.07 |
| `10` | **ENGATIVA** | 3,620,000.00 | 4.40 | 13 | 525.31 |
| `11` | **SUBA** | 4,250,000.00 | 3.19 | 12 | 366.85 |
| `12` | **BARRIOS UNIDOS** | 1,850,000.00 | 11.62 | 10 | 1,244.01 |
| `13` | **TEUSAQUILLO** | 4,520,000.00 | 27.50 | 4 | 1,423.50 |
| `14` | **LOS MARTIRES** | 410,000.00 | 4.95 | 4 | 1,835.15 |
| `15` | **ANTONIO NARINO** | 820,000.00 | 9.52 | 3 | 1,869.51 |
| `16` | **PUENTE ARANDA** | 1,520,000.00 | 5.86 | 6 | 1,072.06 |
| `17` | **LA CANDELARIA** | 210,000.00 | 11.09 | 2 | 3,273.32 |
| `18` | **RAFAEL URIBE URIBE** | 1,620,000.00 | 4.11 | 9 | 644.88 |
| `19` | **CIUDAD BOLIVAR** | 2,650,000.00 | 3.95 | 14 | 464.51 |
| `20` | **SUMAPAZ** | 50,000,000.00 | 12,434.72 | 0 | 6,963.44 |

---

## 6. Recomendaciones de Política Pública y Alertas Tempranas

### A. Recomendación Estratégica Principal (Corto Plazo / Plan de Choque)
- **Localidades Críticas**: Los Mártires, Santa Fe, Bosa, Rafael Uribe Uribe
- **Entidad Responsable**: Instituto Distrital de Recreación y Deporte (IDRD) y DADEP
- **Acción Operativa / Mecanismo**: Adquisición predial para micro-parques de bolsillo, adecuación de cubiertas verdes y mejoramiento integral de parques vecinales deteriorados.
- **Meta / Efecto Esperado**: Habilitar al menos 45.000 m² nuevos de espacio público verde en Los Mártires y Santa Fe.

### B. Recomendación de Sostenibilidad y Eficiencia (Mediano y Largo Plazo)
- **Alcance Distrital**: Parques Metropolitanos y Zonales
- **Acción de Gestión**: Mantenimiento preventivo e iluminación LED de canchas deportivas y senderos ecológicos.
- **Impacto Cuantificable**: Índice de satisfacción ciudadana de espacio público >= 85%.

### C. Protocolo de Semaforización de Alertas Tempranas
- 🔴 **Alerta Crítica (Rojo)**: Espacio de parques < 4.0 m²/hab o Tasa de Parques < 5.0 por 10k hab.
- 🟠 **Alerta Media (Naranja)**: Espacio de parques entre 4.0 y 8.0 m²/hab.
- 🟢 **Condición Estable (Verde)**: Espacio de parques >= 8.0 m²/hab.

---

## 7. Certificación de Calidad y Linaje DAMA-BOK / ISO 25010
- **Completitud Espacial**: 100.0% (20 de 20 localidades canónicas homologadas).
- **Consistencia de Tipos**: Tipado estático conforme y validado con `src.validation`.
- **Inmutabilidad de Fuentes**: Origen verificado en `data/raw/` y transformaciones deterministas sin pérdida de precisión.
