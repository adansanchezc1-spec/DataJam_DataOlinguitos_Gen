# SIPTA — Arquitectura y Gobierno de Datos (`data/`)

**Marco Metodológico**: DAMA-BOK (Data Management Body of Knowledge) / SWEBOK  
**Fase PDCO**: DEVELOPMENT -> CONTROL  
**Estándares**: ISO/IEC 25010, RFC 7946 (GeoJSON), CSV UTF-8  

---

## 🏛️ Estructura del Data Lakehouse Territorial

El repositorio de datos de SIPTA está organizado bajo una arquitectura de capas (*Medallion Architecture*):

```
data/
├── raw/               ← [BRONZE] Datos crudos originales inmutables (DANE, SDIS, IDECA, MEBOG, etc.)
│   ├── DEMOGRAFIA/    ← Proyecciones DANE/SDP (2018-2035) corte 2025 (8.10M hab)
│   ├── VULNERABILIDAD/← Microdatos PUA SDIS 2024 (1.048M registros) y RIVI IPES
│   ├── SALUD/         ← Capacidad hospitalaria REPS y eventos epidemiológicos
│   ├── EDUCACION/     ← Sedes educativas, matrículas y pruebas Saber 11
│   ├── MOVILIDAD/     ← Troncales TransMilenio, paraderos SITP y ciclorrutas
│   ├── INFRAESTRUCTURA_ESPACIO_PUBLICO/ ← Parques IDRD y equipamientos
│   ├── FINANZAS_INVERSION_PUBLICA/ ← Fondos de Desarrollo Local (FDL)
│   ├── AMBIENTE/      ← Monitoreo RMCAB y arbolado urbano
│   ├── SEGURIDAD/     ← Delitos de alto impacto MEBOG y cuadrantes
│   ├── SERVICIOS_PUBLICOS/ ← Cobertura EAAB, UAESP y conectividad TIC
│   ├── EMPLEO_ECONOMIA/    ← Mercado laboral GEIH y micronegocios DANE
│   └── PARTICIPACION_CIUDADANA/ ← Sistema Distrital de Quejas y Soluciones
│
├── processed/         ← [SILVER] Datos limpios, homologados a DIVIPOLA y estandarizados
│   ├── master_localidades.csv ← Tablón Maestro Consolidado (111 columnas x 20 localidades)
│   ├── DEMOGRAFIA/    ← poblacion_localidad_2025.csv, series temporales
│   ├── VULNERABILIDAD/← pua_sdis_indicadores_localidad.csv
│   └── ...            ← Tablas intermedias sectoriales
│
└── curated/           ← [GOLD] Datos contractuales listos para modelado y visualización
    ├── master_indicadores_territoriales.csv ← Indicadores normalizados y sub-índices
    ├── dashboard_ranking.csv                ← Ranking oficial de consenso IPT y escenarios
    ├── sipta_localidades_multidominio.geojson ← Capa vectorial enriquecida (RFC 7946)
    └── domain_*.csv                         ← 12 Tablas temáticas por dominio
```

---

## 🔒 Reglas de Oro de Gobernanza (DAMA-BOK)
1. **Inmutabilidad en Bronze (`raw/`)**: Los archivos crudos jamás se modifican directamente; todo cambio se realiza mediante pipelines en `src/ingestion/`.
2. **Homologación Canónica en Silver (`processed/`)**: Toda tabla contiene `codigo_localidad` (1 a 20) y `nombre_localidad` estandarizado.
3. **Contrato de Salida en Gold (`curated/`)**: 100% de completitud, sin valores nulos residuales y auditado contra ISO 25010.
