# SIPTA — Capa Silver / Datos Procesados e Integrados (`data/processed/`)

**Propósito**: Almacenamiento de datasets limpios, homologados territorialmente y estandarizados para integración.

---

## Artefactos Principales

1. **`master_localidades.csv`**:
   - **Dimensiones**: 20 localidades $\times$ 111 variables territoriales integradas.
   - **Claves Primarias**: `codigo_localidad` (1 a 20) y `nombre_localidad`.
   - **Denominador Poblacional**: 8.101.412 habitantes (DANE / SDP 2025).
   - **Indicadores PUA SDIS**: Atenciones IMG, beneficiarios de comedores, comisarías y habitante de calle.

2. **Subdirectorios Sectoriales**:
   - `DEMOGRAFIA/`: `poblacion_localidad_2025.csv`, `poblacion_localidad_dane_sdp.csv`, `poblacion_upz_dane_sdp.csv`.
   - `VULNERABILIDAD/`: `pua_sdis_indicadores_localidad.csv`.
   - `SALUD/`, `EDUCACION/`, `MOVILIDAD/`, `INFRAESTRUCTURA_ESPACIO_PUBLICO/`, `FINANZAS_INVERSION_PUBLICA/`, `AMBIENTE/`, `SEGURIDAD/`, `SERVICIOS_PUBLICOS/`, `EMPLEO_ECONOMIA/`, `PARTICIPACION_CIUDADANA/`.
