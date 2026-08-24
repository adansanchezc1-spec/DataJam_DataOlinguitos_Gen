# Directorio de Modelos y Artefactos — SIPTA

**Fase PDCO**: DEVELOPMENT → OPERATIONS  
**Estándares**: DAMA-BOK (Model Governance), SWEBOK Cap. 2, ISO/IEC 25010  

---

## 1. Propósito del Directorio
El directorio `models/` aloja los artefactos de configuración, fichas técnicas de gobernanza, esquemas de ponderación y parámetros de calibración del **Índice de Priorización Territorial (IPT)** multidimensional para las 20 localidades de Bogotá D.C.

---

## 2. Contenido del Directorio

```
models/
├── model_card.json                       ← Ficha técnica formal del modelo IPT v2.0
├── ipt_config_weights.json               ← Ponderaciones dimensionales y 5 escenarios de sensibilidad
├── README.md                             ← Documentación de gobernanza del modelo
└── transformers/
    └── minmax_scalers_config.json        ← Parámetros de normalización Min-Max y polaridades por indicador
```

---

## 3. Especificación Técnica de los Artefactos

### A. `model_card.json`
Define los metadatos de gobernanza del modelo:
- **Nombre**: Índice de Priorización Territorial (IPT) Multidimensional.
- **Versión**: 2.0.0.
- **Escala**: $[0, 100]$ (Mayor puntaje $\implies$ Mayor necesidad / prioridad de intervención).
- **Cobertura Territorial**: 20 Localidades oficiales de Bogotá D.C. (DIVIPOLA SDP).
- **Dimensiones Canónicas**: 7 (Educación, Salud, Movilidad, Ambiente, Infraestructura, Vulnerabilidad, Seguridad).

### B. `ipt_config_weights.json`
Configuración determinística de las ponderaciones:
- **Escenario 1 (Base)**: 7 dimensiones con peso balanceado ($w_d = 1/7 \approx 0.142857$).
- **Escenario 2 (Rangos)**: Normalización no paramétrica basada en percentiles.
- **Escenario 3 (Sin Parques)**: 6 dimensiones ($w_d = 1/6 \approx 0.166667$, Infraestructura = 0).
- **Escenario 4 (Sin RIVI)**: 6 dimensiones ($w_d = 1/6 \approx 0.166667$, Vulnerabilidad = 0).
- **Escenario 5 (Sin Proxies)**: 5 dimensiones duras ($w_d = 1/5 = 0.20$).

### C. `transformers/minmax_scalers_config.json`
Parámetros de normalización por indicador con especificación de polaridad:
- **Polaridad Inversa** ($s_i = 1 - \hat{x}_i$): Indicadores de oferta y capacidad asistencial/educativa/movilidad.
- **Polaridad Directa** ($s_i = \hat{x}_i$): Indicadores de riesgo, conflicto ambiental y vulnerabilidad.
