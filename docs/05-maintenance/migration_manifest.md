# Migración de exploración del usuario A a `DataJam_DataOlinguitos_Gen`

## Objetivo
Registrar el estado de la migración de datos y scripts desde el proyecto original `Exploracion_Adan` hacia este repositorio.

## Archivos añadidos
- `.gitignore`
- `requirements.txt`
- `scripts/inventory_data.py`
- `scripts/inspect_discovered.py`
- `scripts/build_eda_notebook.py`
- `docs/01-requirements/README.md`

## Datos migrados a `data/raw`
- `DEMOGRAFIA_POBLACION/osb_demografia-poblacion-localidad.csv`
- `DEMOGRAFIA_POBLACION/osb_demografia-poblacion-upl.csv`
- `EDUCACION/colegios122025.gpkg`
- `EDUCACION/matricula_total_colegios_oficiales.gpkg`
- `FINANZAS_INVERSION_PUBLICA/inversion_educacion_por_localidad_12_2025.gpkg`
- `INFRAESTRUCTURA_ESPACIO_PUBLICO/5.-parques-idrd.csv`
- `INFRAESTRUCTURA_ESPACIO_PUBLICO/ips.gpkg`
- `INFRAESTRUCTURA_ESPACIO_PUBLICO/gpkg_mr_v03.26/gpkg_mr_v03.26.gpkg`
- `MOVILIDAD/conexion_operacional.geojson`
- `MOVILIDAD/estaciones_linea1.geojson`
- `MOVILIDAD/estaciones_linea2.gpkg`
- `MOVILIDAD/estaciones_troncales.geojson`
- `MOVILIDAD/flota_vinculada_sitp_2024-12.csv`
- `MOVILIDAD/paraderos_zonales_sitp.gpkg`
- `MOVILIDAD/retorno_operacional.geojson`
- `MOVILIDAD/servicios_rutas_troncales_zonales.csv`
- `MOVILIDAD/trazado_linea2.gpkg`
- `MOVILIDAD/trazados_troncales.geojson`
- `MOVILIDAD/zonas_zat.geojson`
- `MOVILIDAD/Validaciones/*.xlsx` (validaciones troncal y zonal 2024-2026)
- `SALUD/ips_sds.gpkg`
- `SALUD/osb_tiporazoncamas.csv`

## Estado actual
- Branch activo: `feature`
- `data/status/approved_sources.csv` y `data/status/source_catalog.csv` ya presentes
- `docs/01-requirements` creado con instrucciones para generar inventario
- `src/` ya contiene plantillas de ingesta, validación, limpieza e integración

## Siguientes pasos sugeridos
1. Ejecutar `python scripts/inventory_data.py` para crear el reporte de inventario.
2. Completar `docs/01-requirements/01-data-inventory.md` y validar que los archivos migrados sean correctos.
3. Actualizar `README.md` o `README_WORKFLOW.md` con la ruta de los datos adicionados.
4. Comenzar a escribir tests para los módulos de `src/`.
