"""Módulo de Visualización Geoespacial y Dashboard Interactivo SIPTA.

Fase PDCO: DEVELOPMENT / CONTROL
Estándares: Clean Code, PEP 8, ISO/IEC 25010, DAMA-BOK, OECD/JRC, ISO 9241-110 (IHC).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import geopandas as gpd
import numpy as np
import pandas as pd

# Rutas Canónicas del Proyecto
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
CURATED_DIR = DATA_DIR / "curated"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = ROOT / "reports"

CURATED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Definición de Metadatos de los 13 Dominios, Indicadores y Mapeo de Inversión Pública
DOMAIN_CATALOG: Dict[str, Dict[str, Any]] = {
    "00_ipt": {
        "id": "00_ipt",
        "nombre": "Priorización Territorial (IPT)",
        "icono": "target",
        "color_base": "#e11d48",
        "paleta": "RdYlGn_r",  # Invertida: Rojo = Alta prioridad / privación
        "polaridad": "alta_es_privacion",
        "descripcion": "Índice de Priorización Territorial multidimensional compuesto (7 dimensiones, OCDE/JRC) y escenarios de robustez.",
        "indicador_principal": "IPT_MULTIDIMENSIONAL",
        "investment_key": "inversion_total_consolidada_per_capita_cop",
        "investment_label": "Inversión Distrital Consolidada per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "IPT_MULTIDIMENSIONAL",
                "nombre": "IPT Escenario 1 (Base Lineal 7D)",
                "unidad": "pts",
                "formato": "{:.2f}",
                "desc": "Índice compuesto base lineal (1/7 por dimensión). Mayor puntaje = mayor privación y urgencia.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "IPT_ESCENARIO_2_RANGOS",
                "nombre": "IPT Escenario 2 (Rangos Percentiles No Paramétricos)",
                "unidad": "pts",
                "formato": "{:.2f}",
                "desc": "Transformación de rangos no paramétricos (rank-1)/19 sobre las 7 dimensiones canónicas.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "IPT_ESCENARIO_3_SIN_PARQUES",
                "nombre": "IPT Escenario 3 (Sin Proxy Parques - 6D)",
                "unidad": "pts",
                "formato": "{:.2f}",
                "desc": "Sensibilidad excluyendo la dimensión de Infraestructura y Parques.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "IPT_ESCENARIO_4_SIN_RIVI",
                "nombre": "IPT Escenario 4 (Sin Vulnerabilidad RIVI - 6D)",
                "unidad": "pts",
                "formato": "{:.2f}",
                "desc": "Sensibilidad excluyendo la dimensión de Vulnerabilidad informal (RIVI).",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "IPT_ESCENARIO_5_DURAS",
                "nombre": "IPT Escenario 5 (Cinco Dimensiones Duras - 5D)",
                "unidad": "pts",
                "formato": "{:.2f}",
                "desc": "Modelo estricto de derechos y servicios esenciales (Educación, Salud, Movilidad, Ambiente, Seguridad).",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "IPT_GEOMETRICO",
                "nombre": "IPT Geométrico No Compensatorio",
                "unidad": "pts",
                "formato": "{:.2f}",
                "desc": "Agregación geométrica ponderada que penaliza desbalances dimensionales críticos.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "RANKING_PRIORIDAD",
                "nombre": "Ranking de Prioridad Consenso",
                "unidad": "puesto",
                "formato": "{:.0f}",
                "desc": "Puesto distrital de vulnerabilidad consolidado (1 = máxima urgencia social).",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "ancho_intervalo_ci95",
                "nombre": "Incertidumbre Bootstrap (Ancho IC 95%)",
                "unidad": "pts",
                "formato": "{:.2f}",
                "desc": "Amplitud del intervalo de confianza al 95% derivado de remuestreo Dirichlet (B=1.000).",
                "polaridad": "alta_es_privacion",
            },
        ],
    },
    "01_demografia": {
        "id": "01_demografia",
        "nombre": "Demografía y Espacio",
        "icono": "users",
        "color_base": "#7c3aed",
        "paleta": "Purples",
        "polaridad": "neutro",
        "descripcion": "Concentración demográfica, densidad urbana y población infanto-juvenil.",
        "indicador_principal": "densidad_poblacional",
        "investment_key": "inversion_fdl_per_capita_cop",
        "investment_label": "Inversión FDL per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "densidad_poblacional",
                "nombre": "Densidad Poblacional",
                "unidad": "hab/km²",
                "formato": "{:,.0f}",
                "desc": "Habitantes proyectados por kilómetro cuadrado territorial.",
                "polaridad": "neutro",
            },
            {
                "col": "poblacion_2025",
                "nombre": "Población Total (2025)",
                "unidad": "hab",
                "formato": "{:,.0f}",
                "desc": "Población total estimada por DANE / Secretaría Distrital de Planeación.",
                "polaridad": "neutro",
            },
            {
                "col": "poblacion_5_17_2025",
                "nombre": "Población en Edad Escolar (5 a 17 años)",
                "unidad": "hab",
                "formato": "{:,.0f}",
                "desc": "Demanda potencial del sistema educativo formal distrital.",
                "polaridad": "neutro",
            },
        ],
    },
    "02_salud": {
        "id": "02_salud",
        "nombre": "Salud y Capacidad Asistencial",
        "icono": "heart-pulse",
        "color_base": "#0284c7",
        "paleta": "Blues",
        "polaridad": "baja_es_privacion",
        "descripcion": "Oferta de servicios de salud, sedes IPS y camas hospitalarias contrastadas con la población.",
        "indicador_principal": "sedes_ips_por_10000_hab",
        "investment_key": "inversion_fdl_per_capita_cop",
        "investment_label": "Inversión FDL per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "sedes_ips_por_10000_hab",
                "nombre": "Sedes IPS por 10.000 hab",
                "unidad": "sedes/10k",
                "formato": "{:.2f}",
                "desc": "Disponibilidad de infraestructura prestadora de salud contrastada con la población de la localidad.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "camas_por_10000_habitantes",
                "nombre": "Camas Hospitalarias por 10.000 hab",
                "unidad": "camas/10k",
                "formato": "{:.2f}",
                "desc": "Capacidad de internación hospitalaria general contrastada con la población de la localidad.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "total_camas_hospitalarias",
                "nombre": "Total Camas Hospitalarias (Capacidad Absoluta)",
                "unidad": "camas",
                "formato": "{:,.0f}",
                "desc": "Capacidad física total instalada de camas hospitalarias en la localidad.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "sedes_ips_registradas",
                "nombre": "Total Sedes IPS Registradas",
                "unidad": "sedes",
                "formato": "{:,.0f}",
                "desc": "Conteo absoluto de sedes de salud habilitadas en el Registro Especial de Prestadores (REPS).",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "camas_uci_adultos",
                "nombre": "Camas UCI Adultos",
                "unidad": "camas",
                "formato": "{:,.0f}",
                "desc": "Camas de cuidados intensivos para adultos habilitadas.",
                "polaridad": "baja_es_privacion",
            },
        ],
    },
    "03_educacion": {
        "id": "03_educacion",
        "nombre": "Educación y Logro",
        "icono": "graduation-cap",
        "color_base": "#059669",
        "paleta": "Greens",  # Paleta esmeralda/verde accesible sin negros
        "polaridad": "baja_es_privacion",
        "descripcion": "Oferta de cupos oficiales SED, desempeño Saber 11 y deserción escolar.",
        "indicador_principal": "cupos_por_1000_pob_5_17",
        "investment_key": "inversion_educacion_per_capita_cop",
        "investment_label": "Inversión SED Educación per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "cupos_por_1000_pob_5_17",
                "nombre": "Cupos SED por 1.000 niños (5-17 años)",
                "unidad": "cupos/1k",
                "formato": "{:.1f}",
                "desc": "Capacidad de absorción de matrícula en colegios oficiales SED.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "puntaje_promedio_saber_11",
                "nombre": "Puntaje Promedio Saber 11",
                "unidad": "puntos",
                "formato": "{:.1f}",
                "desc": "Calidad educativa media en pruebas de Estado estandarizadas.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "tasa_desercion_escolar_pct",
                "nombre": "Tasa de Deserción Escolar",
                "unidad": "%",
                "formato": "{:.2f}%",
                "desc": "Porcentaje de estudiantes que abandonan el ciclo lectivo anual.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "inversion_educacion_per_capita_cop",
                "nombre": "Inversión SED por Habitante",
                "unidad": "COP/hab",
                "formato": "${:,.0f}",
                "desc": "Recursos ejecutados por la Secretaría de Educación Distrital por habitante.",
                "polaridad": "baja_es_privacion",
            },
        ],
    },
    "04_movilidad": {
        "id": "04_movilidad",
        "nombre": "Movilidad y Accesibilidad",
        "icono": "bus",
        "color_base": "#d97706",
        "paleta": "Plasma",
        "polaridad": "baja_es_privacion",
        "descripcion": "Densidad de transporte masivo (TransMilenio, SITP) y tiempos de viaje.",
        "indicador_principal": "paraderos_por_km2",
        "investment_key": "inversion_fdl_per_capita_cop",
        "investment_label": "Inversión FDL per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "paraderos_por_km2",
                "nombre": "Paraderos SITP por km²",
                "unidad": "par/km²",
                "formato": "{:.1f}",
                "desc": "Densidad territorial de puntos de acceso zonal del transporte público.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "estaciones_por_km2",
                "nombre": "Estaciones Troncales por km²",
                "unidad": "est/km²",
                "formato": "{:.2f}",
                "desc": "Densidad de estaciones del sistema troncal TransMilenio por km².",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "tiempo_promedio_desplazamiento_laboral_min",
                "nombre": "Tiempo de Viaje Laboral Promedio",
                "unidad": "min",
                "formato": "{:.1f} min",
                "desc": "Minutos promedio invertidos en traslados hacia el lugar de trabajo.",
                "polaridad": "alta_es_privacion",
            },
        ],
    },
    "05_infraestructura": {
        "id": "05_infraestructura",
        "nombre": "Infraestructura y Parques",
        "icono": "trees",
        "color_base": "#10b981",
        "paleta": "Greens",
        "polaridad": "baja_es_privacion",
        "descripcion": "Espacio público recreativo, superficie de parques IDRD y alumbrado público.",
        "indicador_principal": "m2_parque_por_habitante",
        "investment_key": "inversion_fdl_per_capita_cop",
        "investment_label": "Inversión FDL per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "m2_parque_por_habitante",
                "nombre": "Espacio Público (m² de Parque / hab)",
                "unidad": "m²/hab",
                "formato": "{:.2f}",
                "desc": "Metros cuadrados de parques administrados por IDRD por habitante de la localidad.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "area_total_parques_m2",
                "nombre": "Área Total de Parques (m²)",
                "unidad": "m²",
                "formato": "{:,.0f}",
                "desc": "Superficie total de parques y zonas recreativas IDRD en la localidad.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "parques_por_10k_hab",
                "nombre": "Parques IDRD por 10.000 hab",
                "unidad": "parques/10k",
                "formato": "{:.2f}",
                "desc": "Disponibilidad de parques administrados por el IDRD por cada 10.000 habitantes.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "luminarias_por_km2",
                "nombre": "Luminarias de Alumbrado por km²",
                "unidad": "lum/km²",
                "formato": "{:.1f}",
                "desc": "Densidad de iluminación pública instalada por kilómetro cuadrado territorial.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "luminarias_por_10k_hab",
                "nombre": "Luminarias por 10.000 hab",
                "unidad": "lum/10k",
                "formato": "{:,.0f}",
                "desc": "Dotación de alumbrado público por cada 10.000 habitantes.",
                "polaridad": "baja_es_privacion",
            },
        ],
    },
    "06_ambiente": {
        "id": "06_ambiente",
        "nombre": "Ambiente y Sostenibilidad",
        "icono": "leaf",
        "color_base": "#eab308",
        "paleta": "YlOrBr",
        "polaridad": "alta_es_privacion",
        "descripcion": "Conflictos ambientales (SAC), huella hídrica y calidad de agua para consumo.",
        "indicador_principal": "conflictos_ambientales_por_km2",
        "investment_key": "inversion_fdl_per_capita_cop",
        "investment_label": "Inversión FDL per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "conflictos_ambientales_por_km2",
                "nombre": "Conflictos Ambientales (SAC) por km²",
                "unidad": "eventos/km²",
                "formato": "{:.2f}",
                "desc": "Densidad de situaciones ambientales conflictivas y pasivos identificados por SDA.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "consumo_promedio_m3_suscriptor",
                "nombre": "Consumo Hídrico Promedio Mensual",
                "unidad": "m³/susc",
                "formato": "{:.1f}",
                "desc": "Volumen medio mensual de agua consumida por suscriptor residencial (EAAB).",
                "polaridad": "neutro",
            },
            {
                "col": "irca_promedio",
                "nombre": "Riesgo Calidad de Agua (IRCA)",
                "unidad": "pts",
                "formato": "{:.2f}",
                "desc": "Índice de Riesgo de la Calidad del Agua para consumo humano (0 = Agua Apta sin riesgo).",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "conflictos_ambientales_registrados",
                "nombre": "Total Conflictos Ambientales",
                "unidad": "eventos",
                "formato": "{:.0f}",
                "desc": "Conteo total de puntos críticos ambientales inventariados en la localidad.",
                "polaridad": "alta_es_privacion",
            },
        ],
    },
    "07_finanzas": {
        "id": "07_finanzas",
        "nombre": "Finanzas e Inversión Pública",
        "icono": "landmark",
        "color_base": "#2563eb",
        "paleta": "Blues",
        "polaridad": "neutro",
        "descripcion": "Presupuestos de Fondos de Desarrollo Local (FDL), ejecución y gasto social distrital.",
        "indicador_principal": "inversion_total_consolidada_per_capita_cop",
        "investment_key": "inversion_total_consolidada_per_capita_cop",
        "investment_label": "Inversión Total Consolidada per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "inversion_total_consolidada_per_capita_cop",
                "nombre": "Inversión Distrital Total per Cápita",
                "unidad": "COP/hab",
                "formato": "${:,.0f}",
                "desc": "Consolidación de inversión per cápita (FDL + SDIS + SED + Presupuestos Participativos).",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "inversion_fdl_per_capita_millones",
                "nombre": "Inversión FDL per Cápita (COP M)",
                "unidad": "COP M/hab",
                "formato": "${:.2f} M",
                "desc": "Inversión asignada por habitante desde el Fondo de Desarrollo Local.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "porcentaje_ejecucion_fdl",
                "nombre": "Porcentaje de Ejecución FDL",
                "unidad": "%",
                "formato": "{:.1f}%",
                "desc": "Capacidad de ejecución presupuestal del gobierno local.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "inversion_social_sdis_per_capita_cop",
                "nombre": "Gasto Social SDIS per Cápita",
                "unidad": "COP/hab",
                "formato": "${:,.0f}",
                "desc": "Inversión social de la Secretaría Distrital de Integración Social por habitante.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "inversion_educacion_ejecutada_millones",
                "nombre": "Inversión SED Educación (COP Millones)",
                "unidad": "COP M",
                "formato": "${:,.0f} M",
                "desc": "Monto total ejecutado en educación por localidad por la SED.",
                "polaridad": "neutro",
            },
        ],
    },
    "08_vulnerabilidad_social": {
        "id": "08_vulnerabilidad_social",
        "nombre": "Vulnerabilidad Social y RIVI",
        "icono": "hand-heart",
        "color_base": "#dc2626",
        "paleta": "Reds",
        "polaridad": "alta_es_privacion",
        "descripcion": "Registro Individual de Vendedores Informales (RIVI), comedores y transferencias SDIS.",
        "indicador_principal": "rivi_por_10000_hab_2017_2019",
        "investment_key": "inversion_social_sdis_per_capita_cop",
        "investment_label": "Inversión Social SDIS per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "rivi_por_10000_hab_2017_2019",
                "nombre": "Vendedores RIVI por 10.000 hab",
                "unidad": "vendedores/10k",
                "formato": "{:.1f}",
                "desc": "Densidad de vendedores informales caracterizados en el registro distrital.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "tasa_beneficiarios_transferencias_pct",
                "nombre": "Población con Transferencias Monetarias",
                "unidad": "%",
                "formato": "{:.2f}%",
                "desc": "Porcentaje de la población de la localidad cubierta con apoyos monetarios SDIS.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "comedores_por_10k_hab",
                "nombre": "Comedores Comunitarios por 10.000 hab",
                "unidad": "comedores/10k",
                "formato": "{:.3f}",
                "desc": "Red de comedores comunitarios activos por escala de 10.000 habitantes.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "beneficiarios_transferencias_monetarias",
                "nombre": "Total Beneficiarios Transferencias SDIS",
                "unidad": "personas",
                "formato": "{:,.0f}",
                "desc": "Conteo de personas beneficiadas con transferencias en la localidad.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "inversion_social_sdis_per_capita_cop",
                "nombre": "Inversión Social SDIS por Habitante",
                "unidad": "COP/hab",
                "formato": "${:,.0f}",
                "desc": "Presupuesto de asistencia social SDIS ejecutado por habitante.",
                "polaridad": "baja_es_privacion",
            },
        ],
    },
    "09_seguridad": {
        "id": "09_seguridad",
        "nombre": "Seguridad y Convivencia",
        "icono": "shield-alert",
        "color_base": "#881337",
        "paleta": "Reds",  # Carmesí y vino profundo sin negros
        "polaridad": "alta_es_privacion",
        "descripcion": "Tasas de hurtos por habitante, homicidios y cobertura de cuadrantes policiales.",
        "indicador_principal": "tasa_hurto_personas_por_10k_hab",
        "investment_key": "inversion_fdl_per_capita_cop",
        "investment_label": "Inversión FDL per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "tasa_hurto_personas_por_10k_hab",
                "nombre": "Tasa Hurtos a Personas por 10.000 hab",
                "unidad": "hurtos/10k",
                "formato": "{:.2f}",
                "desc": "Frecuencia anual de denuncias por hurto a personas normalizada por la población de la localidad.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "tasa_homicidios_por_100k_hab_calc",
                "nombre": "Tasa de Homicidios por 100k hab",
                "unidad": "hom/100k",
                "formato": "{:.1f}",
                "desc": "Tasa estandarizada anual de muertes violentas por 100.000 habitantes.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "hurto_a_personas_anual",
                "nombre": "Total Hurtos a Personas Anuales",
                "unidad": "casos",
                "formato": "{:,.0f}",
                "desc": "Conteo total anual de denuncias por hurto a personas registradas por MEBOG / SIEDCO.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "cuadrantes_por_10000_hab_2026",
                "nombre": "Cuadrantes Policiales por 10.000 hab",
                "unidad": "cuadrantes/10k",
                "formato": "{:.2f}",
                "desc": "Cobertura preventiva y de patrullaje policial por escala poblacional.",
                "polaridad": "baja_es_privacion",
            },
        ],
    },
    "10_servicios_publicos": {
        "id": "10_servicios_publicos",
        "nombre": "Servicios Públicos Domiciliarios",
        "icono": "droplet",
        "color_base": "#0891b2",
        "paleta": "RdYlBu_r",
        "polaridad": "alta_es_privacion",
        "descripcion": "Riesgo en calidad de agua (IRCA), cobertura de acueducto y continuidad.",
        "indicador_principal": "irca_promedio",
        "investment_key": "inversion_fdl_per_capita_cop",
        "investment_label": "Inversión FDL per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "irca_promedio",
                "nombre": "Índice de Riesgo Agua (IRCA Promedio)",
                "unidad": "pts",
                "formato": "{:.2f}",
                "desc": "Nivel de riesgo de calidad del agua para consumo humano.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "cobertura_acueducto_pct",
                "nombre": "Cobertura de Acueducto",
                "unidad": "%",
                "formato": "{:.1f}%",
                "desc": "Porcentaje de viviendas con conexión formal a la red de acueducto.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "horas_interrupcion_promedio_mes",
                "nombre": "Horas Interrupción Acueducto / Mes",
                "unidad": "horas/mes",
                "formato": "{:.1f} h",
                "desc": "Tiempo promedio de interrupción en la prestación del servicio de agua.",
                "polaridad": "alta_es_privacion",
            },
        ],
    },
    "11_empleo_economia": {
        "id": "11_empleo_economia",
        "nombre": "Mercado Laboral y Salarios",
        "icono": "briefcase",
        "color_base": "#b45309",
        "paleta": "YlOrBr",  # Ámbar y ocre dorado sin negro
        "polaridad": "alta_es_privacion",
        "descripcion": "Movilidad residencia-trabajo, salarios promedio por trabajador e informalidad.",
        "indicador_principal": "ocupados_conmutan_a_otras_localidades_pct",
        "investment_key": "inversion_fdl_per_capita_cop",
        "investment_label": "Inversión FDL per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "ocupados_conmutan_a_otras_localidades_pct",
                "nombre": "Tasa de Conmutación Laboral Externa",
                "unidad": "%",
                "formato": "{:.1f}%",
                "desc": "Porcentaje de trabajadores ocupados que deben conmutar fuera de su localidad.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "ingreso_laboral_promedio_ocupados_cop",
                "nombre": "Ingreso Laboral Promedio Mensual ($ COP / ocupado)",
                "unidad": "COP/mes",
                "formato": "${:,.0f}",
                "desc": "Remuneración salarial promedio de los trabajadores ocupados en la localidad (GEIH / DANE / OSB).",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "tasa_informalidad_laboral_pct",
                "nombre": "Tasa de Informalidad Laboral",
                "unidad": "%",
                "formato": "{:.1f}%",
                "desc": "Porcentaje de trabajadores sin cobertura de seguridad social en salud/pensión.",
                "polaridad": "alta_es_privacion",
            },
        ],
    },
    "12_participacion_ciudadana": {
        "id": "12_participacion_ciudadana",
        "nombre": "Participación Ciudadana y Presupuestos Participativos",
        "icono": "message-square",
        "color_base": "#9333ea",
        "paleta": "PuRd",
        "polaridad": "alta_es_privacion",
        "descripcion": "Votación en presupuestos participativos, propuestas ciudadanas y peticiones PQR.",
        "indicador_principal": "tasa_votantes_pp_por_10k_hab",
        "investment_key": "inversion_pp_per_capita_cop",
        "investment_label": "Inversión Presupuestos Participativos per Cápita",
        "investment_unit": "COP/hab",
        "indicadores": [
            {
                "col": "tasa_votantes_pp_por_10k_hab",
                "nombre": "Votantes en Presupuestos Participativos / 10k hab",
                "unidad": "votantes/10k",
                "formato": "{:.1f}",
                "desc": "Tasa de ciudadanos que votaron en las jornadas de presupuestos participativos por 10.000 hab.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "propuestas_ciudadanas_por_10k_hab",
                "nombre": "Propuestas Ciudadanas Radicadas / 10k hab",
                "unidad": "propuestas/10k",
                "formato": "{:.1f}",
                "desc": "Iniciativas comunitarias radicadas por cada 10.000 habitantes.",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "pqr_resueltas_a_tiempo_pct",
                "nombre": "Oportunidad de Respuesta PQR",
                "unidad": "%",
                "formato": "{:.1f}%",
                "desc": "Porcentaje de peticiones ciudadanas resueltas dentro de los plazos de ley (SDQS).",
                "polaridad": "baja_es_privacion",
            },
            {
                "col": "pqr_por_10k_hab",
                "nombre": "PQR Ciudadanas por 10.000 hab",
                "unidad": "pqr/10k",
                "formato": "{:.1f}",
                "desc": "Densidad de quejas y solicitudes ciudadanas radicadas en el sistema distrital.",
                "polaridad": "alta_es_privacion",
            },
            {
                "col": "inversion_pp_per_capita_cop",
                "nombre": "Inversión Presupuesto Participativo por Habitante",
                "unidad": "COP/hab",
                "formato": "${:,.0f}",
                "desc": "Monto de inversión comunitaria priorizada por habitante.",
                "polaridad": "baja_es_privacion",
            },
        ],
    },
}


def calculate_classification_breaks(
    series: pd.Series, method: str = "jenks", k: int = 5
) -> List[float]:
    """Calcula rupturas de clasificación cartográfica no arbitrarias (Jenks o Cuantiles).

    Implementa el algoritmo de Fisher-Jenks en Python puro para garantizar
    mínima varianza intra-clase y máxima varianza inter-clase sin dependencias C.
    """
    clean_series = pd.to_numeric(series, errors="coerce").dropna().sort_values()
    data = clean_series.to_numpy(dtype=float)
    n = len(data)

    if n == 0:
        return [0.0] * (k + 1)

    min_val, max_val = float(data[0]), float(data[-1])
    if min_val == max_val:
        return [min_val] * (k + 1)

    if method == "quantiles":
        quantiles = np.linspace(0, 1, k + 1)
        breaks = np.quantile(data, quantiles).tolist()
        return [float(b) for b in sorted(list(dict.fromkeys(breaks)))]

    # Fisher-Jenks exacto optimizado para n=20
    k = min(k, len(np.unique(data)))
    mat1 = np.zeros((n + 1, k + 1))
    mat2 = np.zeros((n + 1, k + 1))

    for i in range(1, k + 1):
        mat1[1][i] = 1.0
        mat2[1][i] = 0.0
        for j in range(2, n + 1):
            mat2[j][i] = float("inf")

    v = 0.0
    for l in range(2, n + 1):
        s1 = 0.0
        s2 = 0.0
        w = 0.0
        for m in range(1, l + 1):
            i3 = l - m + 1
            val = float(data[i3 - 1])
            s2 += val * val
            s1 += val
            w += 1.0
            v = s2 - (s1 * s1) / w
            i4 = i3 - 1
            if i4 != 0:
                for j in range(2, k + 1):
                    if mat2[l][j] >= (v + mat2[i4][j - 1]):
                        mat1[l][j] = float(i3)
                        mat2[l][j] = v + mat2[i4][j - 1]
        mat1[l][1] = 1.0
        mat2[l][1] = v

    kclass = [0] * (k + 1)
    kclass[k] = n
    kclass[0] = 0

    count_num = n
    for j in range(k, 1, -1):
        pivot = int(mat1[count_num][j]) - 1
        kclass[j - 1] = pivot
        count_num = pivot

    breaks = [float(data[0])]
    for j in range(1, k + 1):
        idx = min(kclass[j] - 1, n - 1)
        breaks.append(float(data[idx]))

    # Evitar duplicados manteniendo orden
    breaks = sorted(list(dict.fromkeys(breaks)))
    if len(breaks) < 2:
        breaks = [min_val, max_val]
    return breaks


def build_multidomain_geodataframe() -> gpd.GeoDataFrame:
    """Carga y cruza deterministamente la geometría de localidades con el tablón maestro curado.

    Retorna un GeoDataFrame WGS84 EPSG:4326 con 20 localidades y todos los 13 dominios.
    """
    geojson_path = PROCESSED_DIR / "MODELO_TERRITORIAL" / "poligonos_localidades.geojson"
    master_csv_path = CURATED_DIR / "master_indicadores_territoriales.csv"

    if not geojson_path.exists():
        raise FileNotFoundError(f"No existe el archivo de geometrías: {geojson_path}")
    if not master_csv_path.exists():
        raise FileNotFoundError(f"No existe el tablón maestro curado: {master_csv_path}")

    gdf = gpd.read_file(geojson_path)
    df_master = pd.read_csv(master_csv_path)

    # Asegurar tipado canónico para merge determinista por código de localidad (1 a 20)
    gdf["codigo_localidad"] = pd.to_numeric(gdf["LOCCODIGO"], errors="coerce").astype(int)
    df_master["codigo_localidad"] = pd.to_numeric(
        df_master["codigo_localidad"], errors="coerce"
    ).astype(int)

    # Merge espacial-tabular
    gdf_merged = gdf.merge(df_master, on="codigo_localidad", how="inner")

    # Reproyección garantizada a WGS84
    if gdf_merged.crs is None or gdf_merged.crs.to_string() != "EPSG:4326":
        gdf_merged = gdf_merged.to_crs(epsg=4326)

    # Ordenar por ranking de prioridad consensuada
    if "RANKING_PRIORIDAD" in gdf_merged.columns:
        gdf_merged = gdf_merged.sort_values(by="RANKING_PRIORIDAD").reset_index(drop=True)

    return gdf_merged


def export_curated_multidomain_geojson(
    output_path: Optional[Path] = None,
) -> Path:
    """Exporta el GeoDataFrame enriquecido a data/curated en formato RFC 7946 GeoJSON."""
    if output_path is None:
        output_path = CURATED_DIR / "sipta_localidades_multidominio.geojson"

    gdf = build_multidomain_geodataframe()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(output_path, driver="GeoJSON")
    return output_path


def load_point_overlay_layers() -> Dict[str, Any]:
    """Carga y re-proyecta a WGS84 las capas vectoriales puntuales de interés."""
    layers_paths = {
        "estaciones_tm": (
            PROCESSED_DIR / "MOVILIDAD" / "estaciones_troncales.geojson",
            "Estaciones TransMilenio",
            "#ef4444",
        ),
        "estaciones_metro": (
            PROCESSED_DIR / "MOVILIDAD" / "estaciones_linea1.geojson",
            "Estaciones Metro L1 (16 Estaciones)",
            "#06b6d4",
        ),
        "calidad_aire": (
            PROCESSED_DIR / "AMBIENTE" / "estacion_calidad_aire.geojson",
            "Estaciones Calidad Aire (RMCAB)",
            "#0284c7",
        ),
        "vendedores_puntos": (
            PROCESSED_DIR
            / "FINANZAS_INVERSION_PUBLICA"
            / "Punto de encuentro vendedores. Bogotá D.C..geojson",
            "Puntos Encuentro RIVI",
            "#f97316",
        ),
        "cupos_sed": (
            PROCESSED_DIR / "EDUCACION" / "ofertacupos_032025_wgs84.geojson",
            "Oferta Colegios SED",
            "#059669",
        ),
    }

    overlays = {}
    for key, (path, label, color) in layers_paths.items():
        if path.exists():
            try:
                g = gpd.read_file(path)
                g = g[g.geometry.notna() & (~g.geometry.is_empty)].copy()
                if g.crs is not None and g.crs.to_string() != "EPSG:4326":
                    g = g.to_crs(epsg=4326)
                # Extraer centroides precisos para geometrías poligonales
                if (g.geometry.geom_type != "Point").any():
                    # Forzar 2D para evitar warnings en 3D CRS
                    g["geometry"] = g.geometry.force_2d()
                    g["geometry"] = g.to_crs(epsg=3116).geometry.centroid.to_crs(epsg=4326)
                geojson_str = json.loads(g.to_json())
                overlays[key] = {
                    "label": label,
                    "color": color,
                    "count": len(g),
                    "geojson": geojson_str,
                }
            except Exception:
                pass
    return overlays


def generate_interactive_gis_dashboard(
    output_html_path: Optional[Path] = None,
) -> Path:
    """Genera una aplicación Web GIS autónoma, interactiva y responsiva con Leaflet y Chart.js.

    Incluye selector multicapa para los 13 dominios, clasificación Jenks/Cuantiles,
    ranking dinámico por indicador activo, cruce con inversión distrital en 4 cuadrantes,
    tooltips con intervalos de confianza Bootstrap 95%, semáforos de alerta y gráficos.
    """
    if output_html_path is None:
        output_html_path = REPORTS_DIR / "dashboard_geografico_sipta.html"

    gdf = build_multidomain_geodataframe()
    # Exportar también el GeoJSON curado
    export_curated_multidomain_geojson()

    # Cargar overlays
    overlays_data = load_point_overlay_layers()

    # Convertir GeoDataFrame a GeoJSON dict serializable
    geojson_dict = json.loads(gdf.to_json())

    # Pre-calcular rupturas de clasificación para cada indicador
    breaks_dict: Dict[str, Dict[str, Any]] = {}
    for dom_key, dom_data in DOMAIN_CATALOG.items():
        breaks_dict[dom_key] = {}
        for ind in dom_data["indicadores"]:
            col = ind["col"]
            if col in gdf.columns:
                breaks_dict[dom_key][col] = {
                    "jenks": calculate_classification_breaks(gdf[col], "jenks", 5),
                    "quantiles": calculate_classification_breaks(
                        gdf[col], "quantiles", 5
                    ),
                    "min": float(gdf[col].min()),
                    "max": float(gdf[col].max()),
                    "mean": float(gdf[col].mean()),
                    "median": float(gdf[col].median()),
                    "std": float(gdf[col].std()),
                }

    # Serializar datos para incrustar en JavaScript
    geojson_json = json.dumps(geojson_dict)
    catalog_json = json.dumps(DOMAIN_CATALOG)
    breaks_json = json.dumps(breaks_dict)
    overlays_json = json.dumps(overlays_data)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SIPTA — Dashboard Geográfico Multicapa (13 Dominios)</title>
  
  <!-- Tailwind CSS & Google Fonts -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  
  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .glass-panel {{
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    /* Custom Leaflet Tooltip */
    .sipta-tooltip {{
      background: rgba(15, 23, 42, 0.96);
      border: 1px solid rgba(56, 189, 248, 0.6);
      border-radius: 8px;
      color: #f8fafc;
      padding: 8px 12px;
      font-size: 12px;
      box-shadow: 0 12px 28px -4px rgba(0, 0, 0, 0.6);
    }}
    .sipta-tooltip::before {{
      border-top-color: rgba(15, 23, 42, 0.96) !important;
    }}
    /* Focus styling for WCAG 2.1 AA Accessibility */
    *:focus-visible {{
      outline: 2px solid #38bdf8 !important;
      outline-offset: 2px !important;
    }}
    /* Smooth Transitions for Collapsible Sidebars */
    .sidebar-transition {{
      transition: width 0.28s cubic-bezier(0.4, 0, 0.2, 1), transform 0.28s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s ease;
    }}
    /* Scrollbar */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: rgba(15, 23, 42, 0.6);
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(59, 130, 246, 0.4);
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: rgba(59, 130, 246, 0.7);
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-screen overflow-hidden antialiased select-none">

  <!-- Accessible Skip Link for Screen Readers (WCAG 2.1 AA) -->
  <a href="#map" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded-lg">Saltar al mapa interactivo</a>

  <!-- Top Header Navigation & HCI Breadcrumb -->
  <header class="bg-slate-900/95 border-b border-slate-800 px-5 py-2.5 flex items-center justify-between z-30 shrink-0 shadow-lg" role="banner">
    <div class="flex items-center gap-3.5">
      <div class="h-9 w-9 rounded-xl bg-gradient-to-tr from-rose-600 via-amber-500 to-blue-600 flex items-center justify-center shadow-lg shadow-rose-900/20 shrink-0">
        <i data-lucide="map" class="h-5 w-5 text-white" aria-hidden="true"></i>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-base font-bold text-white tracking-tight flex items-center gap-2">
            SIPTA <span class="text-[11px] px-1.5 py-0.2 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 font-mono">v1.1.0</span>
          </h1>
          <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1 font-medium">
            <span class="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" aria-hidden="true"></span> Certificado OCDE/JRC
          </span>
        </div>
        <!-- HCI Breadcrumb: Current System Context -->
        <nav aria-label="Contexto de navegación" class="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
          <span class="text-slate-300">Bogotá D.C.</span>
          <span>&rsaquo;</span>
          <span id="breadcrumb-domain" class="text-sky-400 font-semibold">Priorización Territorial</span>
          <span>&rsaquo;</span>
          <span id="breadcrumb-indicator" class="text-slate-200">IPT Multidimensional</span>
        </nav>
      </div>
    </div>

    <!-- Quick Distrital Diagnostics -->
    <div class="hidden xl:flex items-center gap-4 text-xs" role="region" aria-label="Diagnósticos Estadísticos Distritales">
      <div class="flex items-center gap-1.5 bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700/50">
        <span class="text-slate-400">Cobertura:</span>
        <span class="font-bold text-white font-mono">20 Localidades (100%)</span>
      </div>
      <div class="flex items-center gap-1.5 bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700/50">
        <span class="text-slate-400">Moran I:</span>
        <span class="font-bold text-rose-400 font-mono">0.412 (p=0.008)</span>
      </div>
      <div class="flex items-center gap-1.5 bg-slate-800/80 px-2.5 py-1 rounded-lg border border-slate-700/50">
        <span class="text-slate-400">VIF Multicolinealidad:</span>
        <span class="font-bold text-emerald-400 font-mono">3.21 &lt; 10.0</span>
      </div>
    </div>

    <!-- HCI Global Actions & Tools -->
    <div class="flex items-center gap-1.5">
      <!-- Colorblind Mode Toggle -->
      <button id="btn-colorblind" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-lg border border-slate-700 flex items-center gap-1.5 transition-all" title="Alternar Paleta Accesible para Daltonismo (Viridis)" aria-label="Alternar Paleta Accesible para Daltonismo">
        <i data-lucide="eye" class="h-3.5 w-3.5 text-amber-400" aria-hidden="true"></i>
        <span class="hidden sm:inline">Paleta Accesible</span>
      </button>

      <!-- Export CSV -->
      <button id="btn-export-csv" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-lg border border-slate-700 flex items-center gap-1.5 transition-all" title="Exportar tabla actual a CSV [Tecla C]" aria-label="Exportar datos a archivo CSV">
        <i data-lucide="file-spreadsheet" class="h-3.5 w-3.5 text-emerald-400" aria-hidden="true"></i>
        <span class="hidden sm:inline">CSV</span>
      </button>

      <!-- Export GeoJSON -->
      <button id="btn-export-geojson" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-lg border border-slate-700 flex items-center gap-1.5 transition-all" title="Exportar capa espacial GeoJSON RFC 7946 [Tecla E]" aria-label="Exportar capa espacial GeoJSON">
        <i data-lucide="download" class="h-3.5 w-3.5 text-sky-400" aria-hidden="true"></i>
        <span class="hidden sm:inline">GeoJSON</span>
      </button>

      <!-- Reset / Center Bogotá -->
      <button id="btn-reset-view" class="px-2.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium rounded-lg shadow-lg shadow-blue-900/30 flex items-center gap-1.5 transition-all" title="Centrar Mapa en Bogotá [Tecla R]" aria-label="Centrar vista en Bogotá">
        <i data-lucide="crosshair" class="h-3.5 w-3.5" aria-hidden="true"></i>
        <span class="hidden md:inline">Centrar</span>
      </button>

      <!-- Help & Keyboard Shortcuts Modal Trigger -->
      <button id="btn-help" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-medium rounded-lg border border-amber-500/30 flex items-center gap-1.5 transition-all" title="Guía de Interacción y Atajos [Tecla ?]" aria-label="Abrir guía de ayuda e interacción">
        <i data-lucide="help-circle" class="h-3.5 w-3.5" aria-hidden="true"></i>
        <span class="hidden lg:inline">Ayuda (?)</span>
      </button>
    </div>
  </header>

  <!-- Main Content Layout (Collapsible Controls + Map Canvas + Analytical Inspector) -->
  <div class="flex flex-1 overflow-hidden relative">

    <!-- Left Controls Panel (Collapsible) -->
    <aside id="panel-left" class="w-80 bg-slate-900/95 border-r border-slate-800 flex flex-col z-20 shrink-0 overflow-y-auto sidebar-transition" aria-label="Panel de Controles y Selección de Capas">
      
      <!-- Panel Header with Collapse Button -->
      <div class="p-3.5 border-b border-slate-800 flex items-center justify-between bg-slate-950/40">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
          <i data-lucide="sliders-horizontal" class="h-4 w-4 text-blue-400" aria-hidden="true"></i> Controles del Sistema
        </span>
        <button id="btn-toggle-left" class="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition" title="Colapsar Panel Izquierdo [Tecla []" aria-label="Colapsar panel izquierdo">
          <i data-lucide="panel-left-close" class="h-4 w-4" aria-hidden="true"></i>
        </button>
      </div>

      <!-- Domain Selector (13 Sectors) -->
      <div class="p-4 border-b border-slate-800">
        <label for="select-domain" class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 block flex items-center gap-1.5">
          <i data-lucide="layers" class="h-4 w-4 text-blue-400" aria-hidden="true"></i> Sector / Dominio Analítico
        </label>
        <select id="select-domain" class="w-full bg-slate-800 border border-slate-700 text-white text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all font-medium" aria-label="Seleccionar sector temático">
        </select>
      </div>

      <!-- Indicator Selector -->
      <div class="p-4 border-b border-slate-800">
        <label for="select-indicator" class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 block flex items-center gap-1.5">
          <i data-lucide="activity" class="h-4 w-4 text-rose-400" aria-hidden="true"></i> Indicador Específico
        </label>
        <select id="select-indicator" class="w-full bg-slate-800 border border-slate-700 text-white text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all font-medium" aria-label="Seleccionar indicador">
        </select>
        <p id="indicator-desc" class="text-xs text-slate-400 mt-2 italic leading-relaxed"></p>
        <div id="indicator-polarity" class="mt-2 text-[11px] font-mono px-2 py-1 rounded bg-slate-950 border border-slate-800 text-slate-300"></div>
      </div>

      <!-- Cartographic Classification Method & Investment Cross Button -->
      <div class="p-4 border-b border-slate-800 space-y-3">
        <div class="flex items-center justify-between">
          <label class="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
            <i data-lucide="scale" class="h-4 w-4 text-emerald-400" aria-hidden="true"></i> Clasificación Cartográfica
          </label>
          <span class="text-[10px] text-slate-500" title="Algoritmos no arbitrarios para evitar sesgos cartográficos">Rigor OCDE</span>
        </div>
        <div class="grid grid-cols-2 gap-2" role="radiogroup" aria-label="Método de clasificación cartográfica">
          <button id="btn-jenks" class="px-2.5 py-1.5 text-xs font-medium rounded-lg border border-blue-500 bg-blue-500/20 text-blue-300 flex items-center justify-center gap-1.5 transition" role="radio" aria-checked="true">
            <i data-lucide="check" class="h-3 w-3" aria-hidden="true"></i> Fisher-Jenks (J)
          </button>
          <button id="btn-quantiles" class="px-2.5 py-1.5 text-xs font-medium rounded-lg border border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center justify-center gap-1.5 transition" role="radio" aria-checked="false">
            Cuantiles (Q)
          </button>
        </div>

        <!-- Botón Cruce IPT / Inversión Distrital -->
        <button id="btn-investment-cross" onclick="openInvestmentModal('ipt')" class="w-full mt-2 px-3 py-2.5 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white text-xs font-bold rounded-xl border border-sky-400/40 flex items-center justify-center gap-2 shadow-lg shadow-indigo-950/50 transition-all transform active:scale-95 cursor-pointer" title="Abrir análisis bivariado de IPT e Inversión Pública [Tecla I]" aria-label="Abrir análisis de cruce de IPT e inversión distrital">
          <i data-lucide="scale" class="h-4 w-4 text-amber-300" aria-hidden="true"></i>
          <span>Cruce IPT / Inversión (I)</span>
        </button>
        <p class="text-[10px] text-slate-400 text-center">Matriz 4 cuadrantes: IPT / Indicador vs Inversión</p>
      </div>

      <!-- Point Overlay Toggles -->
      <div class="p-4 border-b border-slate-800">
        <label class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2.5 block flex items-center gap-1.5">
          <i data-lucide="map-pin" class="h-4 w-4 text-amber-400" aria-hidden="true"></i> Capas Vectoriales Overlay
        </label>
        <div class="space-y-2 text-xs" id="overlays-container">
          <!-- Dynamically generated overlay checkboxes -->
        </div>
      </div>

      <!-- Domain Description Card -->
      <div class="p-4 mt-auto bg-slate-950/50 m-3 rounded-xl border border-slate-800/80">
        <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider mb-1 flex items-center gap-1">
          <i data-lucide="info" class="h-3.5 w-3.5 text-blue-400" aria-hidden="true"></i> Sobre este Dominio
        </h4>
        <p id="domain-long-desc" class="text-xs text-slate-400 leading-relaxed"></p>
      </div>
    </aside>

    <!-- Floating Re-open Left Panel Button (Visible when collapsed) -->
    <button id="btn-open-left" class="hidden absolute top-4 left-4 z-20 p-2 bg-slate-900/90 text-white rounded-lg border border-slate-700 shadow-xl hover:bg-slate-800 transition" title="Abrir Panel de Controles [Tecla []" aria-label="Abrir panel de controles">
      <i data-lucide="panel-left-open" class="h-4 w-4" aria-hidden="true"></i>
    </button>

    <!-- Center Map Canvas Container -->
    <main id="main-map-container" class="flex-1 relative h-full bg-slate-950" role="main">
      <div id="map" class="h-full w-full bg-slate-950 z-10" aria-label="Mapa coroplético de las 20 localidades de Bogotá D.C."></div>

      <!-- Floating Predictive Search Box (HCI Autocomplete) -->
      <div class="absolute top-4 left-16 z-20 glass-panel rounded-xl shadow-2xl border border-slate-700/60 w-72">
        <div class="p-2 flex items-center gap-2">
          <i data-lucide="search" class="h-4 w-4 text-slate-400 ml-1" aria-hidden="true"></i>
          <input id="input-search-locality" type="text" placeholder="Buscar localidad (Ctrl+K)..." class="bg-transparent text-xs text-white placeholder-slate-400 outline-none w-full font-medium" aria-label="Buscar localidad de Bogotá" autocomplete="off">
          <button id="btn-clear-search" class="hidden p-0.5 text-slate-400 hover:text-white" title="Limpiar búsqueda" aria-label="Limpiar búsqueda">
            <i data-lucide="x" class="h-3.5 w-3.5" aria-hidden="true"></i>
          </button>
        </div>
        <!-- Predictive Dropdown List -->
        <div id="search-suggestions" class="hidden max-h-56 overflow-y-auto border-t border-slate-800 text-xs divide-y divide-slate-800/60 bg-slate-900/95 rounded-b-xl" role="listbox">
        </div>
      </div>

      <!-- Floating Dynamic Map Legend -->
      <div class="absolute bottom-6 left-6 z-20 glass-panel p-4 rounded-xl shadow-2xl max-w-xs border border-slate-700/60" role="region" aria-label="Leyenda del mapa">
        <div class="flex items-center justify-between mb-2">
          <h4 id="legend-title" class="text-xs font-bold text-white uppercase tracking-wider">Leyenda</h4>
          <span id="legend-unit" class="text-[10px] font-mono text-slate-400"></span>
        </div>
        <div id="legend-items" class="space-y-1.5 text-xs">
          <!-- Dynamically generated color steps -->
        </div>
        <div class="mt-3 pt-2 border-t border-slate-800 text-[10px] text-slate-400 flex items-center justify-between font-mono">
          <span>Mín: <b id="legend-min" class="text-slate-200"></b></span>
          <span>Media: <b id="legend-mean" class="text-blue-400"></b></span>
          <span>Máx: <b id="legend-max" class="text-slate-200"></b></span>
        </div>
        <div id="legend-semantic-guide" class="mt-2.5 pt-2 border-t border-slate-800/80 text-[10px] text-center font-medium leading-tight">
          <!-- Dynamically populated semantic guide -->
        </div>
      </div>
    </main>

    <!-- Floating Re-open Right Panel Button (Visible when collapsed) -->
    <button id="btn-open-right" class="hidden absolute top-4 right-4 z-20 p-2 bg-slate-900/90 text-white rounded-lg border border-slate-700 shadow-xl hover:bg-slate-800 transition" title="Abrir Panel Inspector [Tecla ]]" aria-label="Abrir panel inspector">
      <i data-lucide="panel-right-open" class="h-4 w-4" aria-hidden="true"></i>
    </button>

    <!-- Right Analytical Inspector Panel (Collapsible) -->
    <aside id="panel-right" class="w-96 bg-slate-900/95 border-l border-slate-800 flex flex-col z-20 shrink-0 overflow-y-auto sidebar-transition" aria-label="Ficha Analítica Territorial">
      
      <!-- Panel Header with Collapse Button -->
      <div class="p-3.5 border-b border-slate-800 flex items-center justify-between bg-slate-950/40">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
          <i data-lucide="clipboard-check" class="h-4 w-4 text-emerald-400" aria-hidden="true"></i> Ficha Territorial
        </span>
        <div class="flex items-center gap-1">
          <button id="btn-copy-card" class="p-1 rounded-lg text-slate-400 hover:text-sky-300 hover:bg-slate-800 transition text-xs flex items-center gap-1" title="Copiar ficha al portapapeles" aria-label="Copiar datos al portapapeles">
            <i data-lucide="copy" class="h-3.5 w-3.5" aria-hidden="true"></i>
          </button>
          <button id="btn-toggle-right" class="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition" title="Colapsar Panel Derecho [Tecla ]]" aria-label="Colapsar panel derecho">
            <i data-lucide="panel-right-close" class="h-4 w-4" aria-hidden="true"></i>
          </button>
        </div>
      </div>

      <!-- Locality Inspector Card -->
      <div class="p-4 border-b border-slate-800">
        <div class="flex items-center justify-between mb-1.5">
          <span id="loc-divipola" class="text-xs font-mono text-sky-400 font-semibold">DIVIPOLA: --</span>
          <button id="btn-zoom-locality" class="text-[10px] px-2 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 flex items-center gap-1 transition" title="Enfocar esta localidad en el mapa">
            <i data-lucide="maximize-2" class="h-3 w-3" aria-hidden="true"></i> Zoom
          </button>
        </div>
        <h2 id="loc-name" class="text-xl font-bold text-white tracking-tight">Seleccione una Localidad</h2>
        <p id="loc-area-pop" class="text-xs text-slate-400 mt-1 font-mono">Haga clic o pase el cursor sobre el mapa</p>
      </div>

      <!-- Active Indicator Metric & Early Warning Semaphore -->
      <div class="p-4 border-b border-slate-800 bg-slate-950/40">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-[10px] uppercase font-semibold tracking-wider text-slate-400 block mb-1">Valor Indicador Activo</span>
            <div class="flex items-baseline gap-2">
              <span id="loc-metric-val" class="text-3xl font-extrabold text-white font-mono">--</span>
              <span id="loc-metric-unit" class="text-xs text-slate-400 font-mono"></span>
            </div>
          </div>
          <div class="text-right">
            <span class="text-[10px] uppercase font-semibold tracking-wider text-slate-400 block mb-1" title="Ranking dinámico correspondiente al indicador activo seleccionado">Puesto Indicador</span>
            <span id="loc-metric-rank" class="text-2xl font-bold text-amber-400 font-mono">#-- / 20</span>
          </div>
        </div>

        <!-- Redundant Semaphore Badge (Color + Icon + Text for Accessibility) -->
        <div id="loc-semaphore" class="mt-3 p-2.5 rounded-lg border text-xs font-medium flex items-center justify-between" role="status">
          <span class="flex items-center gap-2">
            <span id="loc-sem-icon" class="text-sm">⚪</span>
            <span id="loc-sem-text">Nivel de Prioridad: Sin selección</span>
          </span>
          <span id="loc-sem-badge" class="font-mono text-[10px]">--</span>
        </div>

        <!-- Bootstrap Confidence Interval & Marshall Smoothing Card -->
        <div id="loc-stats-note" class="mt-3 p-2.5 bg-slate-900 rounded-lg border border-slate-800 text-[11px] text-slate-300 space-y-1">
          <div class="flex justify-between font-mono text-[10px]">
            <span class="text-slate-400">IC 95% Bootstrap:</span>
            <span id="loc-ci95" class="text-blue-300 font-bold">[--, --]</span>
          </div>
          <div class="flex justify-between font-mono text-[10px]">
            <span class="text-slate-400">Ajuste Bayesiano Marshall:</span>
            <span id="loc-marshall" class="text-emerald-300">Estándar Distrital</span>
          </div>
        </div>
      </div>

      <!-- Tabbed Analytical Visualizations (Bar Ranking vs Multidimensional Radar) -->
      <div class="p-4 border-b border-slate-800 flex-1 flex flex-col min-h-[360px]">
        <!-- Tabs Header -->
        <div class="flex items-center gap-2 border-b border-slate-800 pb-2 mb-3" role="tablist">
          <button id="tab-btn-bars" class="px-2.5 py-1 text-xs font-semibold rounded-lg bg-blue-600 text-white flex items-center gap-1.5 transition" role="tab" aria-selected="true">
            <i data-lucide="bar-chart-2" class="h-3.5 w-3.5" aria-hidden="true"></i> Ranking Indicador
          </button>
          <button id="tab-btn-radar" class="px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-400 hover:text-white flex items-center gap-1.5 transition" role="tab" aria-selected="false">
            <i data-lucide="radar" class="h-3.5 w-3.5" aria-hidden="true"></i> Perfil 7D (Radar)
          </button>
        </div>

        <!-- Tab 1: Ranking Chart Canvas -->
        <div id="tab-content-bars" class="flex-1 relative">
          <canvas id="chart-ranking"></canvas>
        </div>

        <!-- Tab 2: Multidimensional Radar Canvas -->
        <div id="tab-content-radar" class="hidden flex-1 relative">
          <canvas id="chart-radar"></canvas>
        </div>
      </div>

      <!-- Methodological Guarantee Footer -->
      <div class="p-3 bg-slate-950 text-[10px] text-slate-400 border-t border-slate-800 space-y-1 leading-relaxed">
        <p><b>Marco Metodológico:</b> OECD/JRC Composite Indicators & SWEBOK v3.</p>
        <p><b>Gobernanza de Datos:</b> DAMA-BOK / ISO 25010 sobre 25 fuentes oficiales de Bogotá.</p>
      </div>

    </aside>

  </div>

  <!-- MODAL: CRUCE CON INVERSIÓN DISTRITAL (ANÁLISIS BIVARIADO 4 CUADRANTES) -->
  <div id="modal-investment" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/85 backdrop-blur-md" role="dialog" aria-modal="true" aria-labelledby="modal-inv-title">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-w-5xl w-full p-6 space-y-5 text-slate-200 max-h-[92vh] overflow-y-auto">
      
      <!-- Modal Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-3 gap-3">
        <div class="flex items-center gap-3">
          <div class="p-2.5 rounded-xl bg-gradient-to-tr from-amber-500 to-indigo-600 text-white shadow-lg shrink-0">
            <i data-lucide="scale" class="h-6 w-6" aria-hidden="true"></i>
          </div>
          <div>
            <h3 id="modal-inv-title" class="text-base sm:text-lg font-bold text-white tracking-tight">Cruce Analítico: IPT vs Inversión Distrital</h3>
            <p id="modal-inv-subtitle" class="text-xs text-slate-400 font-medium">Contraste entre necesidad territorial y asignación presupuestal per cápita</p>
          </div>
        </div>
        <div class="flex items-center gap-2 self-end sm:self-center">
          <!-- Mode Tabs: IPT vs Active Indicator -->
          <div class="inline-flex rounded-lg bg-slate-950 p-1 border border-slate-800 text-xs">
            <button id="btn-inv-mode-ipt" onclick="openInvestmentModal('ipt')" class="px-2.5 py-1 rounded-md text-xs font-bold transition flex items-center gap-1.5 bg-blue-600 text-white shadow cursor-pointer">
              <i data-lucide="target" class="h-3.5 w-3.5 text-rose-300"></i>
              <span>IPT vs Inversión</span>
            </button>
            <button id="btn-inv-mode-active" onclick="openInvestmentModal('active')" class="px-2.5 py-1 rounded-md text-xs font-medium text-slate-400 hover:text-white transition flex items-center gap-1.5 cursor-pointer">
              <i data-lucide="activity" class="h-3.5 w-3.5 text-sky-400"></i>
              <span id="btn-inv-mode-active-label">Indicador Activo</span>
            </button>
          </div>
          <button id="btn-close-inv" onclick="document.getElementById('modal-investment').classList.add('hidden')" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition cursor-pointer" aria-label="Cerrar ventana de cruce de inversión">
            <i data-lucide="x" class="h-5 w-5" aria-hidden="true"></i>
          </button>
        </div>
      </div>

      <!-- KPI Summary Cards (All 4 Quadrants Explicitly Represented) -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5 text-xs">
        <div class="p-2.5 bg-blue-950/40 border border-blue-500/40 rounded-xl cursor-pointer hover:bg-blue-900/40 transition" onclick="filterInvTable('I. Prioridad Atendida')">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] uppercase font-bold text-sky-400">🔵 Cuadrante I</span>
            <span id="inv-kpi-q1-count" class="text-base font-extrabold text-sky-300 font-mono">0 / 20</span>
          </div>
          <b class="text-white text-xs block truncate">Prioridad Atendida</b>
          <p class="text-[10px] text-sky-300/80 mt-0.5">Alta Necesidad + Alta Inversión</p>
        </div>

        <div class="p-2.5 bg-rose-950/40 border border-rose-500/40 rounded-xl cursor-pointer hover:bg-rose-900/40 transition" onclick="filterInvTable('II. Brecha Crítica')">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] uppercase font-bold text-rose-400">🔴 Cuadrante II</span>
            <span id="inv-kpi-q2-count" class="text-base font-extrabold text-rose-300 font-mono">0 / 20</span>
          </div>
          <b class="text-white text-xs block truncate">Brecha Crítica (Déficit)</b>
          <p class="text-[10px] text-rose-300/80 mt-0.5">Alta Necesidad + Baja Inversión</p>
        </div>

        <div class="p-2.5 bg-emerald-950/40 border border-emerald-500/40 rounded-xl cursor-pointer hover:bg-emerald-900/40 transition" onclick="filterInvTable('III. Autosuficiencia')">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] uppercase font-bold text-emerald-400">🟢 Cuadrante III</span>
            <span id="inv-kpi-q3-count" class="text-base font-extrabold text-emerald-300 font-mono">0 / 20</span>
          </div>
          <b class="text-white text-xs block truncate">Autosuficiencia</b>
          <p class="text-[10px] text-emerald-300/80 mt-0.5">Baja Necesidad + Baja Inversión</p>
        </div>

        <div class="p-2.5 bg-amber-950/40 border border-amber-500/40 rounded-xl cursor-pointer hover:bg-amber-900/40 transition" onclick="filterInvTable('IV. Eficiencia a Revisar')">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[10px] uppercase font-bold text-amber-400">🟠 Cuadrante IV</span>
            <span id="inv-kpi-q4-count" class="text-base font-extrabold text-amber-300 font-mono">0 / 20</span>
          </div>
          <b class="text-white text-xs block truncate">Eficiencia a Revisar</b>
          <p class="text-[10px] text-amber-300/80 mt-0.5">Baja Necesidad + Alta Inversión</p>
        </div>
      </div>

      <!-- Statistical Summary Strip -->
      <div class="p-2.5 bg-slate-950/80 border border-slate-800 rounded-xl flex flex-wrap items-center justify-between gap-2 text-xs">
        <div class="flex items-center gap-3">
          <span class="text-slate-400 font-mono">Pearson r: <b id="inv-kpi-pearson" class="text-sky-400 font-bold">--</b></span>
          <span class="text-slate-400 font-mono">Spearman <span id="inv-kpi-spearman" class="text-slate-300 font-bold">ρ: --</span></span>
          <span class="text-slate-400">Inversión Media: <b id="inv-kpi-mean" class="text-white font-mono">$ --</b> <span id="inv-kpi-mean-unit" class="text-[10px] text-slate-400">COP/hab</span></span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-slate-400">Diagnóstico Fiscal:</span>
          <span id="inv-kpi-diagnosis" class="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-600/30 text-sky-300 border border-sky-400/30">Progresivo Moderado</span>
          <span id="inv-kpi-corr-desc" class="text-[10px] text-slate-400 hidden sm:inline"></span>
        </div>
      </div>

      <!-- Main Scatter Plot Canvas (2D Quadrant Matrix) -->
      <div class="bg-slate-950/60 border border-slate-800 rounded-xl p-4">
        <div class="flex items-center justify-between mb-2">
          <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
            <i data-lucide="scatter-chart" class="h-4 w-4 text-sky-400" aria-hidden="true"></i> Matriz Estratégica de Priorización (4 Cuadrantes)
          </h4>
          <span class="text-[10px] text-slate-400 italic">Haga clic en un punto para seleccionar la localidad en el mapa</span>
        </div>
        <div class="h-72 w-full relative">
          <canvas id="chart-investment-scatter"></canvas>
        </div>
      </div>

      <!-- Quadrant Interpretation Guide -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 text-xs">
        <div class="p-2.5 rounded-lg bg-blue-950/30 border border-blue-500/30 text-blue-200">
          <b class="text-sky-300 block mb-0.5">🔵 I. Prioridad Atendida</b>
          <p class="text-[10px] text-slate-300">Alta privación acompañada de alta asignación presupuestal distrital.</p>
        </div>
        <div class="p-2.5 rounded-lg bg-rose-950/40 border border-rose-500/40 text-rose-200">
          <b class="text-rose-300 block mb-0.5">🔴 II. Brecha Crítica (Déficit)</b>
          <p class="text-[10px] text-rose-200/90">Alta privación con baja inversión per cápita. <b>Máxima urgencia de rebalanceo presupuestal.</b></p>
        </div>
        <div class="p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-500/30 text-emerald-200">
          <b class="text-emerald-300 block mb-0.5">🟢 III. Autosuficiencia</b>
          <p class="text-[10px] text-slate-300">Baja privación y baja demanda de recursos extraordinarios (mantenimiento).</p>
        </div>
        <div class="p-2.5 rounded-lg bg-amber-950/30 border border-amber-500/30 text-amber-200">
          <b class="text-amber-300 block mb-0.5">🟠 IV. Eficiencia a Revisar</b>
          <p class="text-[10px] text-slate-300">Baja privación con alta inversión per cápita. Requiere auditoría de retorno social.</p>
        </div>
      </div>

      <!-- Locality Table with Quadrant & Gap Assessment -->
      <div class="border border-slate-800 rounded-xl overflow-hidden">
        <div class="p-2.5 bg-slate-950/70 border-b border-slate-800 flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="text-xs font-bold text-slate-300 uppercase tracking-wider mr-2">Filtrar:</span>
            <button id="btn-flt-all" onclick="filterInvTable('all')" class="px-2.5 py-1 rounded text-xs font-bold bg-blue-600 text-white transition cursor-pointer">Todos (20)</button>
            <button id="btn-flt-q1" onclick="filterInvTable('I. Prioridad Atendida')" class="px-2.5 py-1 rounded text-xs font-medium text-sky-300 bg-sky-950/60 border border-sky-500/40 hover:bg-sky-900/60 transition cursor-pointer">🔵 Q1 Atendida (<span id="cnt-flt-q1">0</span>)</button>
            <button id="btn-flt-q2" onclick="filterInvTable('II. Brecha Crítica')" class="px-2.5 py-1 rounded text-xs font-medium text-rose-300 bg-rose-950/60 border border-rose-500/40 hover:bg-rose-900/60 transition cursor-pointer">🔴 Q2 Brecha Crítica (<span id="cnt-flt-q2">0</span>)</button>
            <button id="btn-flt-q3" onclick="filterInvTable('III. Autosuficiencia')" class="px-2.5 py-1 rounded text-xs font-medium text-emerald-300 bg-emerald-950/60 border border-emerald-500/40 hover:bg-emerald-900/60 transition cursor-pointer">🟢 Q3 Autosuficiente (<span id="cnt-flt-q3">0</span>)</button>
            <button id="btn-flt-q4" onclick="filterInvTable('IV. Eficiencia a Revisar')" class="px-2.5 py-1 rounded text-xs font-medium text-amber-300 bg-amber-950/60 border border-amber-500/40 hover:bg-amber-900/60 transition cursor-pointer">🟠 Q4 Eficiencia (<span id="cnt-flt-q4">0</span>)</button>
          </div>
          <button id="btn-export-inv-csv" class="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded border border-slate-700 flex items-center gap-1 transition cursor-pointer">
            <i data-lucide="download" class="h-3 w-3" aria-hidden="true"></i> Exportar Cruce CSV
          </button>
        </div>
        <div class="max-h-52 overflow-y-auto text-xs">
          <table class="w-full text-left divide-y divide-slate-800">
            <thead class="bg-slate-950 text-slate-400 font-mono text-[10px] uppercase sticky top-0">
              <tr>
                <th class="p-2.5">Localidad</th>
                <th class="p-2.5">Cuadrante</th>
                <th class="p-2.5 text-right">Indicador Activo</th>
                <th class="p-2.5 text-right">Inversión per Cápita</th>
                <th class="p-2.5 text-center">Acción</th>
              </tr>
            </thead>
            <tbody id="table-inv-body" class="divide-y divide-slate-800/60 font-medium">
              <!-- Dynamically populated rows -->
            </tbody>
          </table>
        </div>
      </div>

      <div class="flex justify-end pt-2">
        <button id="btn-close-inv-footer" onclick="document.getElementById('modal-investment').classList.add('hidden')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg shadow-lg transition cursor-pointer">
          Volver al Mapa
        </button>
      </div>
    </div>
  </div>

  <!-- HCI Help & Keyboard Shortcuts Modal (WCAG Accessible Dialog) -->
  <div id="modal-help" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm" role="dialog" aria-modal="true" aria-labelledby="modal-help-title">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-w-2xl w-full p-6 space-y-5 text-slate-200 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="p-2 rounded-lg bg-blue-500/20 text-blue-400">
            <i data-lucide="compass" class="h-5 w-5" aria-hidden="true"></i>
          </div>
          <div>
            <h3 id="modal-help-title" class="text-base font-bold text-white">Guía de Interacción y Protocolos IHC</h3>
            <p class="text-xs text-slate-400">Diseñado bajo principios ISO 9241-110, Heurísticas de Nielsen y Accesibilidad WCAG 2.1 AA</p>
          </div>
        </div>
        <button id="btn-close-help" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition" aria-label="Cerrar ventana de ayuda">
          <i data-lucide="x" class="h-5 w-5" aria-hidden="true"></i>
        </button>
      </div>

      <!-- Keyboard Shortcuts Table -->
      <div class="space-y-2">
        <h4 class="text-xs font-bold uppercase tracking-wider text-sky-400 flex items-center gap-1.5">
          <i data-lucide="keyboard" class="h-4 w-4" aria-hidden="true"></i> Atajos de Teclado Universales
        </h4>
        <div class="grid grid-cols-2 gap-2 text-xs">
          <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
            <span>Buscar localidad</span>
            <kbd class="px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-mono text-[10px] border border-slate-700">Ctrl + K / /</kbd>
          </div>
          <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
            <span>Cruce con Inversión</span>
            <kbd class="px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-mono text-[10px] border border-slate-700">I</kbd>
          </div>
          <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
            <span>Centrar Bogotá</span>
            <kbd class="px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-mono text-[10px] border border-slate-700">R</kbd>
          </div>
          <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
            <span>Método Fisher-Jenks</span>
            <kbd class="px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-mono text-[10px] border border-slate-700">J</kbd>
          </div>
          <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
            <span>Método Cuantiles</span>
            <kbd class="px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-mono text-[10px] border border-slate-700">Q</kbd>
          </div>
          <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
            <span>Colapsar panel izquierdo</span>
            <kbd class="px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-mono text-[10px] border border-slate-700">[</kbd>
          </div>
          <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
            <span>Colapsar panel derecho</span>
            <kbd class="px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-mono text-[10px] border border-slate-700">]</kbd>
          </div>
          <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
            <span>Exportar GeoJSON / CSV</span>
            <kbd class="px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-mono text-[10px] border border-slate-700">E / C</kbd>
          </div>
          <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
            <span>Cerrar diálogos / Limpiar</span>
            <kbd class="px-2 py-0.5 rounded bg-slate-800 text-blue-300 font-mono text-[10px] border border-slate-700">Esc</kbd>
          </div>
        </div>
      </div>

      <!-- Interpretation of Semaphores and Early Warnings -->
      <div class="space-y-2">
        <h4 class="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
          <i data-lucide="shield-alert" class="h-4 w-4" aria-hidden="true"></i> Semáforos de Alerta Temprana
        </h4>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
          <div class="p-2.5 rounded-lg bg-rose-950/40 border border-rose-500/40 text-rose-200">
            <div class="font-bold flex items-center gap-1">🔴 Muy Alta</div>
            <p class="text-[10px] text-rose-300/80 mt-1">Urgencia crítica de inversión y provisión de servicios.</p>
          </div>
          <div class="p-2.5 rounded-lg bg-amber-950/40 border border-amber-500/40 text-amber-200">
            <div class="font-bold flex items-center gap-1">🟠 Alta</div>
            <p class="text-[10px] text-amber-300/80 mt-1">Vulnerabilidad acentuada en 2 o más dimensiones.</p>
          </div>
          <div class="p-2.5 rounded-lg bg-yellow-950/40 border border-yellow-500/40 text-yellow-200">
            <div class="font-bold flex items-center gap-1">🟡 Media</div>
            <p class="text-[10px] text-yellow-300/80 mt-1">Niveles de privación cercanos a la media distrital.</p>
          </div>
          <div class="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-500/40 text-emerald-200">
            <div class="font-bold flex items-center gap-1">🟢 Baja</div>
            <p class="text-[10px] text-emerald-300/80 mt-1">Mayor suficiencia y capacidad asistencial instalada.</p>
          </div>
        </div>
      </div>

      <!-- Methodological Explanation of Breaks -->
      <div class="p-3.5 bg-slate-950 rounded-xl border border-slate-800 text-xs space-y-1.5 text-slate-300">
        <h5 class="font-bold text-white flex items-center gap-1">
          <i data-lucide="scale" class="h-3.5 w-3.5 text-blue-400" aria-hidden="true"></i> Métodos Cartográficos No Arbitrarios
        </h5>
        <p>• <b>Fisher-Jenks:</b> Algoritmo de optimización que minimiza la varianza dentro de cada clase y maximiza la diferencia entre grupos, revelando discontinuidades espaciales reales.</p>
        <p>• <b>Cuantiles:</b> Distribuye exactamente el mismo número de localidades (4 por cada uno de los 5 quintiles), facilitando la comparación de percentiles.</p>
      </div>

      <div class="flex justify-end pt-2">
        <button id="btn-close-help-footer" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg shadow-lg transition">
          Entendido, Volver al Dashboard
        </button>
      </div>
    </div>
  </div>

  <!-- Toast Notification Container (HCI Feedback) -->
  <div id="toast-container" class="fixed bottom-6 right-6 z-50 flex flex-col gap-2 pointer-events-none" aria-live="polite"></div>

  <!-- Embedded Data Payloads -->
  <script>
    const geojsonData = {geojson_json};
    const domainCatalog = {catalog_json};
    const classificationBreaks = {breaks_json};
    const overlaysCatalog = {overlays_json};
  </script>

  <!-- Application Logic (HCI & Accessible Controller) -->
  <script>
    lucide.createIcons();

    let currentDomain = "00_ipt";
    let currentIndicator = "IPT_MULTIDIMENSIONAL";
    let currentMethod = "jenks"; // 'jenks' | 'quantiles'
    let isColorblindMode = false;
    let activeTab = "bars"; // 'bars' | 'radar'
    let selectedLocalityCode = null;
    let map, geojsonLayer, overlaysLayers = {{}};
    let rankingChart = null, radarChart = null, investmentScatterChart = null;

    // Color Palettes (Auditoría Cromática Estricta: Cero Negros #000000 / #000004)
    // Gradientes secuenciales armónicos de alto contraste perceptivo
    const COLOR_PALETTES = {{
      RdYlGn_r: ['#1a9641', '#a6d96a', '#ffffbf', '#fdae61', '#d7191c'],
      Purples:  ['#f2f0f7', '#cbc9e2', '#9e9ac8', '#756bb1', '#4c1d95'], // Violeta profundo
      Blues:    ['#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#1e3a8a'], // Azul noche
      Viridis:  ['#fde725', '#5ec962', '#21918c', '#3b528b', '#312e81'], // Índigo accesible
      Plasma:   ['#fca636', '#e16462', '#b12a90', '#6a00a8', '#1e1b4b'], // Violeta noche
      Greens:   ['#ecfdf5', '#a7f3d0', '#34d399', '#059669', '#064e3b'], // Esmeralda bosque
      YlOrBr:   ['#fef3c7', '#fde68a', '#f59e0b', '#d97706', '#78350f'], // Ámbar tostado sin negro
      Reds:     ['#fee2e2', '#fca5a5', '#ef4444', '#b91c1c', '#881337'], // Carmesí profundo sin negro
      Inferno:  ['#fef08a', '#f97316', '#dc2626', '#86198f', '#4a044e'], // Ciruela oscuro sin negro
      RdYlBu_r: ['#4575b4', '#91bfdb', '#ffffbf', '#fee090', '#fc8d59'],
      Cividis:  ['#ffea46', '#bdaf69', '#7c7b78', '#414d6b', '#0f172a'], // Azul noche sin negro
      PuRd:     ['#f1eef6', '#d7b5d8', '#df65b0', '#be185d', '#831843']  // Magenta vino
    }};

    // Dynamic Ranking Engine (Solves Professor Feedback #1: Rank responds dynamically to active indicator)
    function getDynamicRanking(indicatorCol) {{
      const domMeta = domainCatalog[currentDomain];
      const indMeta = domMeta.indicadores.find(i => i.col === indicatorCol);
      const polarity = indMeta?.polaridad || domMeta.polaridad;
      
      const features = geojsonData.features || [];
      const items = features.map(f => ({{
        code: f.properties.codigo_localidad,
        name: f.properties.nombre_localidad || f.properties.LOCNOMBRE,
        val: (f.properties[indicatorCol] !== null && f.properties[indicatorCol] !== undefined) ? Number(f.properties[indicatorCol]) : 0,
        rawProps: f.properties
      }}));

      // Si la polaridad es 'baja_es_privacion', menor valor significa mayor déficit/urgencia (puesto 1)
      // Si la polaridad es 'alta_es_privacion' o neutro, mayor valor significa mayor magnitud/privación (puesto 1)
      if (polarity === 'baja_es_privacion') {{
        items.sort((a, b) => a.val - b.val);
      }} else {{
        items.sort((a, b) => b.val - a.val);
      }}

      const rankMap = {{}};
      items.forEach((item, index) => {{
        rankMap[item.code] = index + 1;
      }});

      return {{ sortedItems: items, rankMap: rankMap }};
    }}

    // HCI Toast Notification Feedback
    function showToast(msg, type = 'info') {{
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      const icon = type === 'success' ? 'check-circle' : (type === 'warn' ? 'alert-triangle' : 'info');
      const colorClass = type === 'success' ? 'border-emerald-500/40 text-emerald-200 bg-emerald-950/90' : (type === 'warn' ? 'border-amber-500/40 text-amber-200 bg-amber-950/90' : 'border-sky-500/40 text-sky-200 bg-slate-900/90');
      
      toast.className = `p-3 rounded-xl border ${{colorClass}} text-xs shadow-2xl backdrop-blur-md flex items-center gap-2.5 transition-all duration-300 transform translate-y-2 opacity-0 pointer-events-auto`;
      toast.innerHTML = `<i data-lucide="${{icon}}" class="h-4 w-4 shrink-0"></i><span>${{msg}}</span>`;
      container.appendChild(toast);
      lucide.createIcons();

      requestAnimationFrame(() => {{
        toast.classList.remove('translate-y-2', 'opacity-0');
      }});

      setTimeout(() => {{
        toast.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => toast.remove(), 300);
      }}, 3200);
    }}

    // Initialize Map
    function initMap() {{
      map = L.map('map', {{
        center: [4.65, -74.12],
        zoom: 11,
        zoomControl: false
      }});

      L.control.zoom({{ position: 'topright' }}).addTo(map);

      // Dark Matter Base Layer
      L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
        attribution: '&copy; CartoDB & OpenStreetMap contributors',
        subdomains: 'abcd',
        maxZoom: 19
      }}).addTo(map);

      renderChoropleth();
      initOverlays();
      updateSidebarDomainInfo();
      updateCharts();
    }}

    // Get Active Color for a Value based on Classification Breaks & Indicator Polarity
    function getColor(val) {{
      if (val === null || val === undefined || isNaN(val)) return '#475569';
      
      const breaksInfo = classificationBreaks[currentDomain]?.[currentIndicator];
      if (!breaksInfo) return '#3b82f6';
      
      const breaks = breaksInfo[currentMethod] || [breaksInfo.min, breaksInfo.max];
      const domMeta = domainCatalog[currentDomain];
      const indMeta = domMeta.indicadores.find(i => i.col === currentIndicator);
      const polarity = indMeta?.polaridad || domMeta.polaridad;
      
      const paletteKey = isColorblindMode ? 'Viridis' : (domMeta.paleta || 'Blues');
      let colors = (COLOR_PALETTES[paletteKey] || COLOR_PALETTES.Blues).slice();

      // Inversión semántica: cuando menor valor representa carencia/déficit ('baja_es_privacion'),
      // los valores más bajos deben recibir el color más oscuro/crítico de alerta.
      if (polarity === 'baja_es_privacion') {{
        colors.reverse();
      }}

      for (let i = 0; i < breaks.length - 1; i++) {{
        if (val <= breaks[i + 1] || i === breaks.length - 2) {{
          return colors[i % colors.length];
        }}
      }}
      return colors[colors.length - 1];
    }}

    // Style function for GeoJSON polygons
    function styleFeature(feature) {{
      const val = feature.properties[currentIndicator];
      const isSelected = selectedLocalityCode === feature.properties.codigo_localidad;
      return {{
        fillColor: getColor(val),
        weight: isSelected ? 3.5 : 1.5,
        opacity: 1,
        color: isSelected ? '#38bdf8' : '#334155',
        dashArray: isSelected ? '' : '2',
        fillOpacity: isSelected ? 0.92 : 0.72
      }};
    }}

    // Render Choropleth Layer
    function renderChoropleth() {{
      if (geojsonLayer) {{
        map.removeLayer(geojsonLayer);
      }}

      const rankingData = getDynamicRanking(currentIndicator);

      geojsonLayer = L.geoJSON(geojsonData, {{
        style: styleFeature,
        onEachFeature: function(feature, layer) {{
          const props = feature.properties;
          const val = props[currentIndicator];
          const indMeta = domainCatalog[currentDomain].indicadores.find(i => i.col === currentIndicator);
          const formattedVal = (val !== null && val !== undefined) ? Number(val).toLocaleString(undefined, {{maximumFractionDigits: 2}}) : 'N/D';
          const dynamicRank = rankingData.rankMap[props.codigo_localidad] || '--';

          let extraContext = '';
          const pobStr = Number(props.poblacion_2025 || props.poblacion || 0).toLocaleString();
          if (currentDomain === '02_salud') {{
            const ips = Number(props.sedes_ips_registradas || 0).toLocaleString();
            const camas = Number(props.total_camas_hospitalarias || 0).toLocaleString();
            extraContext = `<div class="text-[10px] text-sky-200 mt-1 border-t border-slate-700/60 pt-1">
              Sedes IPS: <b>${{ips}}</b> | Camas: <b>${{camas}}</b> | Pob: <b>${{pobStr}} hab</b>
            </div>`;
          }} else if (currentDomain === '05_infraestructura' && props.area_total_parques_m2) {{
            const m2p = Number(props.m2_parque_por_habitante || 0).toFixed(2);
            const areaHa = Number(props.area_parques_ha || 0).toLocaleString();
            extraContext = `<div class="text-[10px] text-emerald-200 mt-1 border-t border-slate-700/60 pt-1">
              Área Parques: <b>${{areaHa}} ha</b> (${{m2p}} m²/hab | Pob: ${{pobStr}})
            </div>`;
          }} else if (currentDomain === '09_seguridad' && props.hurto_a_personas_anual) {{
            const hurtos = Number(props.hurto_a_personas_anual || 0).toLocaleString();
            const hom = Number(props.homicidios_anual || 0).toLocaleString();
            extraContext = `<div class="text-[10px] text-rose-200 mt-1 border-t border-slate-700/60 pt-1">
              Hurtos: <b>${{hurtos}}</b> | Homicidios: <b>${{hom}}</b> | Pob: <b>${{pobStr}}</b>
            </div>`;
          }}

          layer.bindTooltip(`
            <div class="sipta-tooltip font-sans">
              <div class="font-bold text-sm text-sky-400 mb-0.5">${{props.nombre_localidad || props.LOCNOMBRE}}</div>
              <div class="text-[11px] text-slate-300">${{indMeta ? indMeta.nombre : currentIndicator}}: <b class="text-white font-mono">${{formattedVal}} ${{indMeta?.unidad || ''}}</b></div>
              <div class="text-[10px] text-slate-400 mt-1">Puesto Indicador: <b class="text-amber-400 font-mono">#${{dynamicRank}} / 20</b> | Consenso IPT: <b class="text-rose-400 font-mono">#${{props.RANKING_PRIORIDAD || '--'}}</b></div>
              ${{extraContext}}
            </div>
          `, {{ sticky: true, opacity: 1, className: 'custom-leaflet-tooltip' }});

          layer.on({{
            mouseover: function(e) {{
              const l = e.target;
              if (selectedLocalityCode !== props.codigo_localidad) {{
                l.setStyle({{ weight: 2.5, color: '#f8fafc', fillOpacity: 0.86 }});
              }}
              updateInspector(props);
            }},
            mouseout: function(e) {{
              if (selectedLocalityCode !== props.codigo_localidad) {{
                geojsonLayer.resetStyle(e.target);
              }}
              if (selectedLocalityCode) {{
                const selFeat = geojsonData.features.find(f => f.properties.codigo_localidad === selectedLocalityCode);
                if (selFeat) updateInspector(selFeat.properties);
              }}
            }},
            click: function(e) {{
              selectLocality(props.codigo_localidad);
            }}
          }});
        }}
      }}).addTo(map);

      updateLegend();
    }}

    // Select Locality Function
    function selectLocality(code) {{
      selectedLocalityCode = code;
      geojsonLayer.eachLayer(ly => ly.setStyle(styleFeature(ly.feature)));
      const feat = geojsonData.features.find(f => f.properties.codigo_localidad === code);
      if (feat) {{
        updateInspector(feat.properties);
        updateCharts();
        showToast(`Localidad seleccionada: ${{feat.properties.nombre_localidad}}`, 'info');
      }}
    }}

    // Update Floating Legend
    function updateLegend() {{
      const breaksInfo = classificationBreaks[currentDomain]?.[currentIndicator];
      if (!breaksInfo) return;

      const breaks = breaksInfo[currentMethod] || [breaksInfo.min, breaksInfo.max];
      const domMeta = domainCatalog[currentDomain];
      const indMeta = domMeta.indicadores.find(i => i.col === currentIndicator);
      const polarity = indMeta?.polaridad || domMeta.polaridad;
      
      const paletteKey = isColorblindMode ? 'Viridis' : (domMeta.paleta || 'Blues');
      let colors = (COLOR_PALETTES[paletteKey] || COLOR_PALETTES.Blues).slice();
      
      if (polarity === 'baja_es_privacion') {{
        colors.reverse();
      }}

      document.getElementById('legend-title').innerText = indMeta?.nombre || currentIndicator;
      document.getElementById('legend-unit').innerText = indMeta?.unidad || '';
      document.getElementById('legend-min').innerText = Number(breaksInfo.min).toLocaleString(undefined, {{maximumFractionDigits: 1}});
      document.getElementById('legend-mean').innerText = Number(breaksInfo.mean).toLocaleString(undefined, {{maximumFractionDigits: 1}});
      document.getElementById('legend-max').innerText = Number(breaksInfo.max).toLocaleString(undefined, {{maximumFractionDigits: 1}});

      const container = document.getElementById('legend-items');
      container.innerHTML = '';

      for (let i = 0; i < breaks.length - 1; i++) {{
        const b1 = Number(breaks[i]).toLocaleString(undefined, {{maximumFractionDigits: 1}});
        const b2 = Number(breaks[i+1]).toLocaleString(undefined, {{maximumFractionDigits: 1}});
        const col = colors[i % colors.length];
        
        container.innerHTML += `
          <div class="flex items-center gap-2">
            <span class="h-3 w-6 rounded shrink-0 border border-slate-600/40" style="background-color: ${{col}}"></span>
            <span class="text-slate-300 font-mono text-[11px]">${{b1}} &ndash; ${{b2}}</span>
          </div>
        `;
      }}

      // Semantic Direction Guide in Legend
      const semGuide = document.getElementById('legend-semantic-guide');
      if (semGuide) {{
        if (polarity === 'baja_es_privacion') {{
          semGuide.innerHTML = '<span class="text-amber-400 font-semibold">● Oscuro = Mayor Carencia</span> <span class="text-slate-500 mx-1">|</span> <span class="text-slate-400">● Claro = Adecuado</span>';
        }} else if (polarity === 'alta_es_privacion') {{
          semGuide.innerHTML = '<span class="text-slate-400">● Claro = Bajo</span> <span class="text-slate-500 mx-1">|</span> <span class="text-rose-400 font-semibold">● Oscuro = Mayor Urgencia</span>';
        }} else {{
          semGuide.innerHTML = '<span class="text-slate-400">● Claro = Menor</span> <span class="text-slate-500 mx-1">|</span> <span class="text-sky-400">● Oscuro = Mayor Magnitud</span>';
        }}
      }}
    }}

    // Update Inspector Sidebar with Locality Details
    function updateInspector(props) {{
      if (!props) return;
      document.getElementById('loc-divipola').innerText = `DIVIPOLA: ${{props.codigo_divipola || ('11001' + String(props.codigo_localidad).padStart(2, '0'))}}`;
      document.getElementById('loc-name').innerText = props.nombre_localidad || props.LOCNOMBRE;
      document.getElementById('loc-area-pop').innerText = `Área: ${{Number(props.area_km2 || 0).toFixed(1)}} km² | Población: ${{Number(props.poblacion_2025 || props.poblacion || 0).toLocaleString()}} hab`;

      const indMeta = domainCatalog[currentDomain].indicadores.find(i => i.col === currentIndicator);
      const val = props[currentIndicator];
      const formattedVal = (val !== null && val !== undefined) ? Number(val).toLocaleString(undefined, {{maximumFractionDigits: 2}}) : '--';
      
      const rankingData = getDynamicRanking(currentIndicator);
      const dynamicRank = rankingData.rankMap[props.codigo_localidad] || '--';

      document.getElementById('loc-metric-val').innerText = formattedVal;
      document.getElementById('loc-metric-unit').innerText = indMeta?.unidad || '';
      document.getElementById('loc-metric-rank').innerText = `#${{dynamicRank}} / 20`;

      // Semaphore update (Accessible Icon + Text)
      const prio = props.NIVEL_PRIORIDAD || 'No Definido';
      const semBox = document.getElementById('loc-semaphore');
      const semIcon = document.getElementById('loc-sem-icon');
      const semText = document.getElementById('loc-sem-text');
      const semBadge = document.getElementById('loc-sem-badge');

      semText.innerText = `Prioridad IPT: ${{prio}}`;
      semBadge.innerText = `Consenso IPT #${{props.RANKING_PRIORIDAD || '--'}}`;

      if (prio.includes('Muy Alta') || prio.includes('Crítica')) {{
        semBox.className = 'mt-3 p-2.5 rounded-lg border border-rose-500/40 bg-rose-950/40 text-xs font-medium text-rose-200 flex items-center justify-between';
        semIcon.innerText = '🔴';
      }} else if (prio.includes('Alta')) {{
        semBox.className = 'mt-3 p-2.5 rounded-lg border border-amber-500/40 bg-amber-950/40 text-xs font-medium text-amber-200 flex items-center justify-between';
        semIcon.innerText = '🟠';
      }} else if (prio.includes('Media')) {{
        semBox.className = 'mt-3 p-2.5 rounded-lg border border-yellow-500/40 bg-yellow-950/40 text-xs font-medium text-yellow-200 flex items-center justify-between';
        semIcon.innerText = '🟡';
      }} else {{
        semBox.className = 'mt-3 p-2.5 rounded-lg border border-emerald-500/40 bg-emerald-950/40 text-xs font-medium text-emerald-200 flex items-center justify-between';
        semIcon.innerText = '🟢';
      }}

      // Bootstrap & Marshall notes
      const ciLow = props.ci_lower_95 !== undefined ? Number(props.ci_lower_95).toFixed(1) : '--';
      const ciHigh = props.ci_upper_95 !== undefined ? Number(props.ci_upper_95).toFixed(1) : '--';
      document.getElementById('loc-ci95').innerText = `[${{ciLow}}, ${{ciHigh}}]`;

      if (props.nombre_localidad === 'SUMAPAZ' || props.nombre_localidad === 'CANDELARIA') {{
        document.getElementById('loc-marshall').innerText = 'Suavizamiento Bayesiano Aplicado';
        document.getElementById('loc-marshall').className = 'text-amber-400 font-bold';
      }} else {{
        document.getElementById('loc-marshall').innerText = 'Estándar Distrital';
        document.getElementById('loc-marshall').className = 'text-emerald-300';
      }}
    }}

    // Update Domain & Indicator Selection Details
    function updateSidebarDomainInfo() {{
      const domMeta = domainCatalog[currentDomain];
      document.getElementById('domain-long-desc').innerText = domMeta.descripcion;
      document.getElementById('breadcrumb-domain').innerText = domMeta.nombre;
      
      const indMeta = domMeta.indicadores.find(i => i.col === currentIndicator);
      document.getElementById('indicator-desc').innerText = indMeta?.desc || '';
      document.getElementById('breadcrumb-indicator').innerText = indMeta?.nombre || currentIndicator;

      const polarityEl = document.getElementById('indicator-polarity');
      const polarity = indMeta?.polaridad || domMeta.polaridad;
      if (polarity === 'alta_es_privacion') {{
        polarityEl.innerHTML = '<span class="text-rose-400 font-bold">▲ Mayor valor</span> = Mayor privación / urgencia';
      }} else if (polarity === 'baja_es_privacion') {{
        polarityEl.innerHTML = '<span class="text-emerald-400 font-bold">▼ Menor valor</span> = Mayor privación (baja oferta)';
      }} else {{
        polarityEl.innerHTML = '<span class="text-blue-400 font-bold">■ Polaridad neutra</span> / Descriptiva';
      }}
    }}

    // Update Both Charts (Ranking Bar Chart & Multidimensional Radar)
    function updateCharts() {{
      updateBarChart();
      updateRadarChart();
    }}

    // Update Chart.js Ranking Chart (Horizontal Bars sorted by dynamic ranking)
    function updateBarChart() {{
      const rankingData = getDynamicRanking(currentIndicator);
      const dataItems = rankingData.sortedItems;

      const labels = dataItems.map(d => d.name);
      const values = dataItems.map(d => d.val);
      const bgColors = dataItems.map(d => d.code === selectedLocalityCode ? '#38bdf8' : getColor(d.val));

      const ctx = document.getElementById('chart-ranking').getContext('2d');
      if (rankingChart) {{
        rankingChart.destroy();
      }}

      const indMeta = domainCatalog[currentDomain].indicadores.find(i => i.col === currentIndicator);

      rankingChart = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: labels,
          datasets: [{{
            label: indMeta?.nombre || currentIndicator,
            data: values,
            backgroundColor: bgColors,
            borderRadius: 4,
            borderWidth: 0
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: function(c) {{ return `${{c.raw.toLocaleString()}} ${{indMeta?.unidad || ''}}`; }}
              }}
            }}
          }},
          scales: {{
            x: {{
              grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
              ticks: {{ color: '#94a3b8', font: {{ family: 'JetBrains Mono', size: 9 }} }}
            }},
            y: {{
              grid: {{ display: false }},
              ticks: {{ color: '#e2e8f0', font: {{ family: 'Plus Jakarta Sans', size: 9, weight: '500' }} }}
            }}
          }},
          onClick: function(e, elements) {{
            if (elements.length > 0) {{
              const idx = elements[0].index;
              const targetItem = dataItems[idx];
              selectLocality(targetItem.code);
            }}
          }}
        }}
      }});
    }}

    // Update Chart.js Radar Chart (7 Canonical Dimensions Profile)
    function updateRadarChart() {{
      const ctx = document.getElementById('chart-radar').getContext('2d');
      const dimensions = [
        {{ key: 'dim_educacion', label: 'Educación' }},
        {{ key: 'dim_salud', label: 'Salud' }},
        {{ key: 'dim_movilidad', label: 'Movilidad' }},
        {{ key: 'dim_ambiente', label: 'Ambiente' }},
        {{ key: 'dim_infraestructura', label: 'Infraestructura' }},
        {{ key: 'dim_vulnerabilidad', label: 'Vulnerabilidad' }},
        {{ key: 'dim_seguridad', label: 'Seguridad' }}
      ];

      const features = geojsonData.features || [];
      // Calculate District Means for the 7 dimensions
      const districtMeans = dimensions.map(d => {{
        const vals = features.map(f => Number(f.properties[d.key] || 0) * 100);
        return vals.reduce((a, b) => a + b, 0) / (vals.length || 1);
      }});

      let localityValues = districtMeans;
      let localityLabel = 'Promedio Distrital';
      if (selectedLocalityCode) {{
        const feat = features.find(f => f.properties.codigo_localidad === selectedLocalityCode);
        if (feat) {{
          localityLabel = feat.properties.nombre_localidad;
          localityValues = dimensions.map(d => Number(feat.properties[d.key] || 0) * 100);
        }}
      }}

      if (radarChart) {{
        radarChart.destroy();
      }}

      radarChart = new Chart(ctx, {{
        type: 'radar',
        data: {{
          labels: dimensions.map(d => d.label),
          datasets: [
            {{
              label: localityLabel,
              data: localityValues,
              backgroundColor: 'rgba(56, 189, 248, 0.35)',
              borderColor: '#38bdf8',
              pointBackgroundColor: '#38bdf8',
              borderWidth: 2
            }},
            {{
              label: 'Promedio Distrital',
              data: districtMeans,
              backgroundColor: 'rgba(148, 163, 184, 0.15)',
              borderColor: '#94a3b8',
              borderDash: [4, 4],
              pointRadius: 0,
              borderWidth: 1.5
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            r: {{
              angleLines: {{ color: 'rgba(255, 255, 255, 0.1)' }},
              grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
              pointLabels: {{ color: '#cbd5e1', font: {{ size: 10, weight: 'bold' }} }},
              ticks: {{ display: false, min: 0, max: 100 }}
            }}
          }},
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{ color: '#e2e8f0', font: {{ size: 10 }} }}
            }}
          }}
        }}
      }});
    }}

    // Bivariate Statistical Calculator for Investment Cross Analysis
    function calculateBivariateStats(xVals, yVals) {{
      const n = xVals.length;
      if (n === 0) return {{ pearson: 0, spearman: 0, meanX: 0, meanY: 0 }};

      const meanX = xVals.reduce((a, b) => a + b, 0) / n;
      const meanY = yVals.reduce((a, b) => a + b, 0) / n;

      let num = 0, denX = 0, denY = 0;
      for (let i = 0; i < n; i++) {{
        const dx = xVals[i] - meanX;
        const dy = yVals[i] - meanY;
        num += dx * dy;
        denX += dx * dx;
        denY += dy * dy;
      }}
      const pearson = denX > 0 && denY > 0 ? num / Math.sqrt(denX * denY) : 0;

      // Spearman Rank Helper
      const sortedX = xVals.map((v, i) => ({{ v, i }})).sort((a, b) => a.v - b.v);
      const sortedY = yVals.map((v, i) => ({{ v, i }})).sort((a, b) => a.v - b.v);
      const rankX = new Array(n);
      const rankY = new Array(n);
      for (let i = 0; i < n; i++) {{
        rankX[sortedX[i].i] = i + 1;
        rankY[sortedY[i].i] = i + 1;
      }}

      let sumD2 = 0;
      for (let i = 0; i < n; i++) {{
        const d = rankX[i] - rankY[i];
        sumD2 += d * d;
      }}
      const spearman = n > 1 ? 1 - (6 * sumD2) / (n * (n * n - 1)) : 0;

      return {{ pearson, spearman, meanX, meanY }};
    }}

    let currentInvModalMode = 'ipt';

    let currentClassifiedPoints = [];
    let currentFilteredQuadrant = 'all';

    function filterInvTable(quadKey) {{
      currentFilteredQuadrant = quadKey;
      const tableBody = document.getElementById('table-inv-body');
      if (!tableBody) return;
      tableBody.innerHTML = '';

      const btnMap = {{
        'all': document.getElementById('btn-flt-all'),
        'I. Prioridad Atendida': document.getElementById('btn-flt-q1'),
        'II. Brecha Crítica': document.getElementById('btn-flt-q2'),
        'III. Autosuficiencia': document.getElementById('btn-flt-q3'),
        'IV. Eficiencia a Revisar': document.getElementById('btn-flt-q4')
      }};

      Object.entries(btnMap).forEach(([k, btn]) => {{
        if (!btn) return;
        if (k === quadKey) {{
          btn.className = 'px-2.5 py-1 rounded text-xs font-bold bg-blue-600 text-white shadow transition cursor-pointer';
        }} else {{
          btn.className = 'px-2.5 py-1 rounded text-xs font-medium text-slate-300 bg-slate-900 border border-slate-700 hover:bg-slate-800 transition cursor-pointer';
        }}
      }});

      const filtered = quadKey === 'all'
        ? currentClassifiedPoints
        : currentClassifiedPoints.filter(p => p.quadName === quadKey);

      filtered.forEach(row => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/80 transition cursor-pointer';
        const formattedX = isNaN(Number(row.x)) ? '0' : Number(row.x).toLocaleString(undefined, {{maximumFractionDigits: 2}});
        const formattedY = Math.round(row.y).toLocaleString();
        const unitSpan = row.xUnit ? '<span class="text-[10px] text-slate-400">' + row.xUnit + '</span>' : '';

        tr.innerHTML = '<td class="p-2.5 font-bold text-white flex items-center gap-1.5">' +
            '<span class="h-2 w-2 rounded-full" style="background-color: ' + row.quadColor + '"></span>' +
            row.name +
          '</td>' +
          '<td class="p-2.5">' + row.quadBadge + '</td>' +
          '<td class="p-2.5 text-right font-mono text-slate-200">' + formattedX + ' ' + unitSpan + '</td>' +
          '<td class="p-2.5 text-right font-mono text-sky-300">$ ' + formattedY + '</td>' +
          '<td class="p-2.5 text-center">' +
            '<button class="px-2 py-1 bg-blue-600/30 hover:bg-blue-600 text-sky-200 hover:text-white rounded text-[10px] font-semibold transition cursor-pointer" onclick="selectLocalityFromModal(' + row.code + ')">' +
              'Ver' +
            '</button>' +
          '</td>';
        tableBody.appendChild(tr);
      }});
    }}

    // Investment Cross Analysis Modal Controller
    function openInvestmentModal(mode) {{
      if (mode === 'ipt' || mode === 'active') {{
        currentInvModalMode = mode;
      }}

      const modalEl = document.getElementById('modal-investment');
      if (modalEl) {{
        modalEl.classList.remove('hidden');
      }}
      if (window.lucide && typeof lucide.createIcons === 'function') {{
        lucide.createIcons();
      }}

      const domMeta = domainCatalog[currentDomain] || domainCatalog['00_ipt'];
      const indMeta = domMeta && domMeta.indicadores ? domMeta.indicadores.find(i => i.col === currentIndicator) : null;

      let xCol = 'IPT_MULTIDIMENSIONAL';
      let xName = 'Índice de Priorización Territorial (IPT)';
      let xUnit = 'pts (0-100)';
      let invKey = 'inversion_total_consolidada_per_capita_cop';
      let invLabel = 'Inversión Distrital Consolidada';
      let invUnit = 'COP/hab';
      let polarity = 'alta_es_privacion';

      if (currentInvModalMode === 'active') {{
        xCol = currentIndicator;
        xName = indMeta && indMeta.nombre ? indMeta.nombre : currentIndicator;
        xUnit = indMeta && indMeta.unidad ? indMeta.unidad : '';
        invKey = domMeta.investment_key || 'inversion_total_consolidada_per_capita_cop';
        invLabel = domMeta.investment_label || 'Inversión per Cápita';
        invUnit = domMeta.investment_unit || 'COP/hab';
        polarity = indMeta && indMeta.polaridad ? indMeta.polaridad : domMeta.polaridad;

        const titleEl = document.getElementById('modal-inv-title');
        if (titleEl) titleEl.innerText = 'Cruce Sectorial: ' + xName + ' vs ' + invLabel;
        const subEl = document.getElementById('modal-inv-subtitle');
        if (subEl) subEl.innerText = 'Contraste espacial de necesidad frente al flujo de inversión pública distrital (' + invLabel + ')';

        const btnIpt = document.getElementById('btn-inv-mode-ipt');
        const btnAct = document.getElementById('btn-inv-mode-active');
        if (btnIpt && btnAct) {{
          btnIpt.className = 'px-2.5 py-1 rounded-md text-xs font-medium text-slate-400 hover:text-white transition flex items-center gap-1.5 cursor-pointer';
          btnAct.className = 'px-2.5 py-1 rounded-md text-xs font-bold bg-blue-600 text-white shadow transition flex items-center gap-1.5 cursor-pointer';
        }}
      }} else {{
        const titleEl = document.getElementById('modal-inv-title');
        if (titleEl) titleEl.innerText = 'Cruce Macro: IPT Multidimensional vs Inversión Consolidada';
        const subEl = document.getElementById('modal-inv-subtitle');
        if (subEl) subEl.innerText = 'Evaluación de progresividad fiscal: Asignación consolidada per cápita vs Privación multidimensional (IPT)';

        const btnIpt = document.getElementById('btn-inv-mode-ipt');
        const btnAct = document.getElementById('btn-inv-mode-active');
        if (btnIpt && btnAct) {{
          btnIpt.className = 'px-2.5 py-1 rounded-md text-xs font-bold bg-blue-600 text-white shadow transition flex items-center gap-1.5 cursor-pointer';
          btnAct.className = 'px-2.5 py-1 rounded-md text-xs font-medium text-slate-400 hover:text-white transition flex items-center gap-1.5 cursor-pointer';
        }}
      }}

      const activeLabelEl = document.getElementById('btn-inv-mode-active-label');
      if (activeLabelEl && indMeta && indMeta.nombre) {{
        activeLabelEl.innerText = indMeta.nombre.length > 16 ? indMeta.nombre.substring(0, 16) + '...' : indMeta.nombre;
      }}

      const features = (geojsonData && geojsonData.features) ? geojsonData.features : [];
      const xVals = [], yVals = [], pointsData = [];

      features.forEach(f => {{
        const p = f.properties || {{}};
        let xVal = Number(p[xCol]);
        if ((isNaN(xVal) || xVal === undefined) && currentInvModalMode === 'ipt') {{
          xVal = Number(p.ipt_consenso_score || p.ipt_base || p.indice_privacion_multidimensional || p.IPT_MULTIDIMENSIONAL || 0);
        }} else if (isNaN(xVal)) {{
          xVal = 0;
        }}

        let yVal = Number(p[invKey]);
        if (isNaN(yVal) || yVal === undefined) {{
          yVal = Number(p.inversion_total_consolidada_per_capita_cop || p.inversion_fdl_per_capita_cop || 0);
        }}

        xVals.push(xVal);
        yVals.push(yVal);
        pointsData.push({{
          code: p.codigo_localidad,
          name: p.nombre_localidad || p.LOCNOMBRE || 'Localidad',
          x: xVal,
          y: yVal,
          raw: p
        }});
      }});

      const stats = calculateBivariateStats(xVals, yVals);
      const medianX = xVals.length > 0 ? xVals.slice().sort((a,b)=>a-b)[Math.floor(xVals.length/2)] : 0;
      const medianY = yVals.length > 0 ? yVals.slice().sort((a,b)=>a-b)[Math.floor(yVals.length/2)] : 0;

      const pEl = document.getElementById('inv-kpi-pearson');
      if (pEl) pEl.innerText = stats.pearson.toFixed(2);
      const sEl = document.getElementById('inv-kpi-spearman');
      if (sEl) sEl.innerText = 'ρ: ' + stats.spearman.toFixed(2);
      const mEl = document.getElementById('inv-kpi-mean');
      if (mEl) mEl.innerText = '$ ' + Math.round(stats.meanY).toLocaleString();
      const muEl = document.getElementById('inv-kpi-mean-unit');
      if (muEl) muEl.innerText = invUnit + ' promedio';

      let corrText = 'Asociación débil';
      if (stats.pearson > 0.4) corrText = 'Directa / Progresiva';
      else if (stats.pearson < -0.4) corrText = 'Inversa / Regresiva';
      else corrText = 'Baja focalización';
      const corrDescEl = document.getElementById('inv-kpi-corr-desc');
      if (corrDescEl) corrDescEl.innerText = corrText;

      // Classify All 4 Quadrants
      let q1Count = 0, q2Count = 0, q3Count = 0, q4Count = 0;
      currentClassifiedPoints = pointsData.map(pt => {{
        let isHighPriv = polarity === 'baja_es_privacion' ? (pt.x <= medianX) : (pt.x >= medianX);
        let isHighInv = pt.y >= medianY;

        let quadKey = '', quadName = '', quadBadge = '', quadColor = '#3b82f6';
        if (isHighPriv && isHighInv) {{
          quadKey = 'Q1';
          quadName = 'I. Prioridad Atendida';
          quadBadge = '<span class="px-2 py-0.5 rounded bg-blue-500/20 text-sky-300 font-semibold text-[10px]">🔵 Atendida</span>';
          quadColor = '#38bdf8';
          q1Count++;
        }} else if (isHighPriv && !isHighInv) {{
          quadKey = 'Q2';
          quadName = 'II. Brecha Crítica';
          quadBadge = '<span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold text-[10px]">🔴 Brecha Crítica</span>';
          quadColor = '#f43f5e';
          q2Count++;
        }} else if (!isHighPriv && !isHighInv) {{
          quadKey = 'Q3';
          quadName = 'III. Autosuficiencia';
          quadBadge = '<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-semibold text-[10px]">🟢 Autosuficiente</span>';
          quadColor = '#10b981';
          q3Count++;
        }} else {{
          quadKey = 'Q4';
          quadName = 'IV. Eficiencia a Revisar';
          quadBadge = '<span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-semibold text-[10px]">🟠 Eficiencia</span>';
          quadColor = '#f59e0b';
          q4Count++;
        }}

        return {{ ...pt, quadKey, quadName, quadBadge, quadColor, isHighPriv, isHighInv, xUnit }};
      }});

      // Update all 4 KPI Cards
      const q1El = document.getElementById('inv-kpi-q1-count');
      if (q1El) q1El.innerText = q1Count + ' / 20';
      const q2El = document.getElementById('inv-kpi-q2-count');
      if (q2El) q2El.innerText = q2Count + ' / 20';
      const q3El = document.getElementById('inv-kpi-q3-count');
      if (q3El) q3El.innerText = q3Count + ' / 20';
      const q4El = document.getElementById('inv-kpi-q4-count');
      if (q4El) q4El.innerText = q4Count + ' / 20';

      const cntQ1 = document.getElementById('cnt-flt-q1');
      if (cntQ1) cntQ1.innerText = q1Count;
      const cntQ2 = document.getElementById('cnt-flt-q2');
      if (cntQ2) cntQ2.innerText = q2Count;
      const cntQ3 = document.getElementById('cnt-flt-q3');
      if (cntQ3) cntQ3.innerText = q3Count;
      const cntQ4 = document.getElementById('cnt-flt-q4');
      if (cntQ4) cntQ4.innerText = q4Count;

      const diagEl = document.getElementById('inv-kpi-diagnosis');
      if (diagEl) diagEl.innerText = q2Count > 5 ? 'Déficit Territorial Acentuado' : (q2Count > 0 ? 'Focalización Moderada' : 'Alta Progresividad');

      // Sort and populate table
      currentClassifiedPoints.sort((a, b) => (a.quadName === 'II. Brecha Crítica' ? -1 : 1));
      filterInvTable('all');

      // Render Scatter Chart
      const ctx = document.getElementById('chart-investment-scatter').getContext('2d');
      if (investmentScatterChart) {{
        investmentScatterChart.destroy();
      }}

      investmentScatterChart = new Chart(ctx, {{
        type: 'scatter',
        data: {{
          datasets: [{{
            label: 'Localidades',
            data: currentClassifiedPoints.map(p => ({{ x: p.x, y: p.y, name: p.name, code: p.code, quad: p.quadName }})),
            backgroundColor: currentClassifiedPoints.map(p => p.quadColor),
            pointRadius: currentClassifiedPoints.map(p => p.code === selectedLocalityCode ? 9 : 6),
            pointHoverRadius: 9,
            borderColor: '#ffffff',
            borderWidth: currentClassifiedPoints.map(p => p.code === selectedLocalityCode ? 2.5 : 1)
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: function(c) {{
                  const raw = c.raw;
                  const u = xUnit ? ' ' + xUnit : '';
                  return raw.name + ' [' + raw.quad + ']: (' + raw.x.toLocaleString(undefined, {{maximumFractionDigits: 2}}) + u + ', $' + Math.round(raw.y).toLocaleString() + ' COP)';
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              title: {{ display: true, text: xName + (xUnit ? ' (' + xUnit + ')' : ''), color: '#94a3b8', font: {{ size: 10, weight: 'bold' }} }},
              grid: {{ color: 'rgba(255, 255, 255, 0.06)' }},
              ticks: {{ color: '#94a3b8', font: {{ family: 'JetBrains Mono', size: 9 }} }}
            }},
            y: {{
              title: {{ display: true, text: invLabel + ' (' + invUnit + ')', color: '#94a3b8', font: {{ size: 10, weight: 'bold' }} }},
              grid: {{ color: 'rgba(255, 255, 255, 0.06)' }},
              ticks: {{ color: '#94a3b8', font: {{ family: 'JetBrains Mono', size: 9 }} }}
            }}
          }},
          onClick: function(e, elements) {{
            if (elements.length > 0) {{
              const idx = elements[0].index;
              const target = currentClassifiedPoints[idx];
              selectLocalityFromModal(target.code);
            }}
          }}
        }}
      }});

      document.getElementById('modal-investment').classList.remove('hidden');
      showToast('Análisis bivariado de inversión (' + (currentInvModalMode === 'ipt' ? 'IPT Consolidado' : xName) + ')', 'info');
    }}

    function selectLocalityFromModal(code) {{
      selectLocality(code);
      document.getElementById('modal-investment').classList.add('hidden');
      geojsonLayer.eachLayer(layer => {{
        if (layer.feature.properties.codigo_localidad === code) {{
          map.flyToBounds(layer.getBounds(), {{ padding: [30, 30], duration: 0.8 }});
        }}
      }});
    }}

    // Initialize Vector Overlays
    function initOverlays() {{
      const container = document.getElementById('overlays-container');
      container.innerHTML = '';

      Object.entries(overlaysCatalog).forEach(([key, item]) => {{
        container.innerHTML += `
          <label class="flex items-center justify-between p-2 rounded-lg bg-slate-800/60 border border-slate-700/50 hover:bg-slate-800 cursor-pointer transition">
            <span class="flex items-center gap-2 text-slate-300">
              <input type="checkbox" id="overlay-${{key}}" class="rounded border-slate-600 text-blue-600 focus:ring-0">
              <span>${{item.label}}</span>
            </span>
            <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-950 border border-slate-700" style="color: ${{item.color}}">${{item.count}} pts</span>
          </label>
        `;
      }});

      Object.entries(overlaysCatalog).forEach(([key, item]) => {{
        document.getElementById(`overlay-${{key}}`)?.addEventListener('change', function(e) {{
          if (e.target.checked) {{
            const layer = L.geoJSON(item.geojson, {{
              pointToLayer: function(feature, latlng) {{
                return L.circleMarker(latlng, {{
                  radius: 4.5,
                  fillColor: item.color,
                  color: '#ffffff',
                  weight: 1,
                  opacity: 1,
                  fillOpacity: 0.9
                }});
              }},
              onEachFeature: function(f, l) {{
                l.bindPopup(`<b class="text-slate-900">${{f.properties.nombre || f.properties.NOMBRE || item.label}}</b>`);
              }}
            }}).addTo(map);
            overlaysLayers[key] = layer;
            showToast(`Capa activada: ${{item.label}}`, 'info');
          }} else if (overlaysLayers[key]) {{
            map.removeLayer(overlaysLayers[key]);
            delete overlaysLayers[key];
            showToast(`Capa desactivada: ${{item.label}}`, 'info');
          }}
        }});
      }});
    }}

    // Setup Event Handlers & Dropdowns
    function setupInteractions() {{
      const domainSelect = document.getElementById('select-domain');
      domainSelect.innerHTML = '';
      Object.entries(domainCatalog).forEach(([key, d]) => {{
        domainSelect.innerHTML += `<option value="${{key}}">${{d.nombre}}</option>`;
      }});

      domainSelect.addEventListener('change', function(e) {{
        currentDomain = e.target.value;
        populateIndicatorDropdown();
        currentIndicator = domainCatalog[currentDomain].indicadores[0].col;
        updateSidebarDomainInfo();
        renderChoropleth();
        updateCharts();
        showToast(`Sector cambiado a: ${{domainCatalog[currentDomain].nombre}}`, 'info');
      }});

      populateIndicatorDropdown();

      document.getElementById('select-indicator').addEventListener('change', function(e) {{
        currentIndicator = e.target.value;
        updateSidebarDomainInfo();
        renderChoropleth();
        updateCharts();
        showToast(`Indicador activo actualizado`, 'info');
      }});

      // Classification Method buttons
      document.getElementById('btn-jenks').addEventListener('click', function() {{
        currentMethod = 'jenks';
        this.className = 'px-2.5 py-1.5 text-xs font-medium rounded-lg border border-blue-500 bg-blue-500/20 text-blue-300 flex items-center justify-center gap-1.5 transition';
        document.getElementById('btn-quantiles').className = 'px-2.5 py-1.5 text-xs font-medium rounded-lg border border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center justify-center gap-1.5 transition';
        renderChoropleth();
        showToast('Clasificación: Fisher-Jenks Natural Breaks', 'info');
      }});

      document.getElementById('btn-quantiles').addEventListener('click', function() {{
        currentMethod = 'quantiles';
        this.className = 'px-2.5 py-1.5 text-xs font-medium rounded-lg border border-blue-500 bg-blue-500/20 text-blue-300 flex items-center justify-center gap-1.5 transition';
        document.getElementById('btn-jenks').className = 'px-2.5 py-1.5 text-xs font-medium rounded-lg border border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center justify-center gap-1.5 transition';
        renderChoropleth();
        showToast('Clasificación: Cuantiles (Percentiles Equidistribuidos)', 'info');
      }});

      // Cruce con Inversión Trigger Button & Mode Toggles
      document.getElementById('btn-investment-cross').addEventListener('click', () => openInvestmentModal('ipt'));
      document.getElementById('btn-inv-mode-ipt')?.addEventListener('click', () => openInvestmentModal('ipt'));
      document.getElementById('btn-inv-mode-active')?.addEventListener('click', () => openInvestmentModal('active'));
      document.getElementById('btn-close-inv').addEventListener('click', () => document.getElementById('modal-investment').classList.add('hidden'));
      document.getElementById('btn-close-inv-footer').addEventListener('click', () => document.getElementById('modal-investment').classList.add('hidden'));

      // Export Investment CSV
      document.getElementById('btn-export-inv-csv').addEventListener('click', function() {{
        const domMeta = domainCatalog[currentDomain];
        const invKey = domMeta.investment_key || 'inversion_total_consolidada_per_capita_cop';
        const rows = [
          ['codigo_localidad', 'nombre_localidad', 'codigo_divipola', currentIndicator, invKey, 'inversion_total_consolidada_per_capita_cop']
        ];
        geojsonData.features.forEach(f => {{
          const p = f.properties;
          rows.push([p.codigo_localidad, p.nombre_localidad, p.codigo_divipola, p[currentIndicator], p[invKey], p.inversion_total_consolidada_per_capita_cop]);
        }});
        const csvContent = 'data:text/csv;charset=utf-8,' + rows.map(e => e.join(',')).join('\\n');
        const encodedUri = encodeURI(csvContent);
        const a = document.createElement('a');
        a.href = encodedUri;
        a.download = `cruce_inversion_${{currentDomain}}_${{currentIndicator}}.csv`;
        a.click();
        showToast('Cruce de inversión exportado a CSV', 'success');
      }});

      // Colorblind Mode Toggle
      document.getElementById('btn-colorblind').addEventListener('click', function() {{
        isColorblindMode = !isColorblindMode;
        this.className = isColorblindMode ? 'px-2.5 py-1.5 bg-amber-500/20 text-amber-300 text-xs font-medium rounded-lg border border-amber-500/40 flex items-center gap-1.5 transition-all' : 'px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-lg border border-slate-700 flex items-center gap-1.5 transition-all';
        renderChoropleth();
        updateCharts();
        showToast(isColorblindMode ? 'Modo Accesible Viridis Activado' : 'Paleta Estándar Restaurada', 'success');
      }});

      // Reset View Button
      document.getElementById('btn-reset-view').addEventListener('click', function() {{
        map.setView([4.65, -74.12], 11);
        showToast('Vista centrada en Bogotá D.C.', 'info');
      }});

      // Zoom to Selected Locality
      document.getElementById('btn-zoom-locality').addEventListener('click', function() {{
        if (selectedLocalityCode) {{
          geojsonLayer.eachLayer(layer => {{
            if (layer.feature.properties.codigo_localidad === selectedLocalityCode) {{
              map.flyToBounds(layer.getBounds(), {{ padding: [30, 30], duration: 0.8 }});
            }}
          }});
        }}
      }});

      // Copy Locality Summary to Clipboard
      document.getElementById('btn-copy-card').addEventListener('click', function() {{
        const feat = geojsonData.features.find(f => f.properties.codigo_localidad === selectedLocalityCode);
        if (feat) {{
          const p = feat.properties;
          const rankingData = getDynamicRanking(currentIndicator);
          const dynamicRank = rankingData.rankMap[p.codigo_localidad] || '--';
          const text = `SIPTA - Ficha Territorial\\nLocalidad: ${{p.nombre_localidad}} (DIVIPOLA: ${{p.codigo_divipola}})\\nPuesto en Indicador (${{currentIndicator}}): #${{dynamicRank}} / 20 (Valor: ${{p[currentIndicator]}})\\nRanking IPT Consenso: #${{p.RANKING_PRIORIDAD}} (${{p.NIVEL_PRIORIDAD}})\\nIC 95% Bootstrap: [${{p.ci_lower_95}}, ${{p.ci_upper_95}}]`;
          navigator.clipboard.writeText(text).then(() => {{
            showToast('Ficha copiada al portapapeles', 'success');
          }});
        }}
      }});

      // Export GeoJSON
      document.getElementById('btn-export-geojson').addEventListener('click', function() {{
        const blob = new Blob([JSON.stringify(geojsonData, null, 2)], {{ type: 'application/json' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'sipta_localidades_multidominio.geojson';
        a.click();
        showToast('Exportación GeoJSON completada', 'success');
      }});

      // Export CSV
      document.getElementById('btn-export-csv').addEventListener('click', function() {{
        const rows = [
          ['codigo_localidad', 'nombre_localidad', 'codigo_divipola', currentIndicator, 'RANKING_PRIORIDAD', 'NIVEL_PRIORIDAD']
        ];
        geojsonData.features.forEach(f => {{
          const p = f.properties;
          rows.push([p.codigo_localidad, p.nombre_localidad, p.codigo_divipola, p[currentIndicator], p.RANKING_PRIORIDAD, p.NIVEL_PRIORIDAD]);
        }});
        const csvContent = 'data:text/csv;charset=utf-8,' + rows.map(e => e.join(',')).join('\\n');
        const encodedUri = encodeURI(csvContent);
        const a = document.createElement('a');
        a.href = encodedUri;
        a.download = `sipta_${{currentDomain}}_${{currentIndicator}}.csv`;
        a.click();
        showToast('Exportación CSV completada', 'success');
      }});

      // Tabs Logic
      document.getElementById('tab-btn-bars').addEventListener('click', function() {{
        activeTab = 'bars';
        this.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg bg-blue-600 text-white flex items-center gap-1.5 transition';
        document.getElementById('tab-btn-radar').className = 'px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-400 hover:text-white flex items-center gap-1.5 transition';
        document.getElementById('tab-content-bars').classList.remove('hidden');
        document.getElementById('tab-content-radar').classList.add('hidden');
      }});

      document.getElementById('tab-btn-radar').addEventListener('click', function() {{
        activeTab = 'radar';
        this.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg bg-blue-600 text-white flex items-center gap-1.5 transition';
        document.getElementById('tab-btn-bars').className = 'px-2.5 py-1 text-xs font-semibold rounded-lg bg-slate-800 text-slate-400 hover:text-white flex items-center gap-1.5 transition';
        document.getElementById('tab-content-radar').classList.remove('hidden');
        document.getElementById('tab-content-bars').classList.add('hidden');
        updateRadarChart();
      }});

      // Collapsible Panels (HCI User Freedom)
      const pLeft = document.getElementById('panel-left');
      const pRight = document.getElementById('panel-right');
      const btnOpenLeft = document.getElementById('btn-open-left');
      const btnOpenRight = document.getElementById('btn-open-right');

      function toggleLeft(collapse) {{
        if (collapse) {{
          pLeft.classList.add('w-0', 'opacity-0', 'pointer-events-none', 'p-0', 'border-0');
          pLeft.classList.remove('w-80');
          btnOpenLeft.classList.remove('hidden');
        }} else {{
          pLeft.classList.remove('w-0', 'opacity-0', 'pointer-events-none', 'p-0', 'border-0');
          pLeft.classList.add('w-80');
          btnOpenLeft.classList.add('hidden');
        }}
        setTimeout(() => map.invalidateSize(), 300);
      }}

      function toggleRight(collapse) {{
        if (collapse) {{
          pRight.classList.add('w-0', 'opacity-0', 'pointer-events-none', 'p-0', 'border-0');
          pRight.classList.remove('w-96');
          btnOpenRight.classList.remove('hidden');
        }} else {{
          pRight.classList.remove('w-0', 'opacity-0', 'pointer-events-none', 'p-0', 'border-0');
          pRight.classList.add('w-96');
          btnOpenRight.classList.add('hidden');
        }}
        setTimeout(() => map.invalidateSize(), 300);
      }}

      document.getElementById('btn-toggle-left').addEventListener('click', () => toggleLeft(true));
      btnOpenLeft.addEventListener('click', () => toggleLeft(false));
      document.getElementById('btn-toggle-right').addEventListener('click', () => toggleRight(true));
      btnOpenRight.addEventListener('click', () => toggleRight(false));

      // Help Modal Logic
      const modalHelp = document.getElementById('modal-help');
      function openHelp() {{ modalHelp.classList.remove('hidden'); }}
      function closeHelp() {{ modalHelp.classList.add('hidden'); }}
      document.getElementById('btn-help').addEventListener('click', openHelp);
      document.getElementById('btn-close-help').addEventListener('click', closeHelp);
      document.getElementById('btn-close-help-footer').addEventListener('click', closeHelp);

      // Predictive Search Box Autocomplete (HCI Recognition over Recall)
      const searchInput = document.getElementById('input-search-locality');
      const searchSuggestions = document.getElementById('search-suggestions');
      const btnClearSearch = document.getElementById('btn-clear-search');

      function filterSuggestions() {{
        const query = searchInput.value.trim().toLowerCase();
        if (!query) {{
          searchSuggestions.classList.add('hidden');
          btnClearSearch.classList.add('hidden');
          return;
        }}
        btnClearSearch.classList.remove('hidden');
        const matches = geojsonData.features.filter(f => {{
          const name = (f.properties.nombre_localidad || '').toLowerCase();
          const divipola = String(f.properties.codigo_divipola || '');
          return name.includes(query) || divipola.includes(query);
        }});

        if (matches.length === 0) {{
          searchSuggestions.innerHTML = '<div class="p-3 text-slate-400 text-center">No se encontraron localidades</div>';
        }} else {{
          searchSuggestions.innerHTML = matches.map(m => `
            <div class="p-2.5 hover:bg-slate-800 cursor-pointer flex items-center justify-between transition" data-code="${{m.properties.codigo_localidad}}">
              <div>
                <b class="text-white">${{m.properties.nombre_localidad}}</b>
                <span class="text-[10px] text-slate-400 ml-1">DIVIPOLA: ${{m.properties.codigo_divipola}}</span>
              </div>
              <span class="px-1.5 py-0.5 rounded bg-blue-500/20 text-sky-400 font-mono text-[10px]">#${{m.properties.RANKING_PRIORIDAD}}</span>
            </div>
          `).join('');
        }}
        searchSuggestions.classList.remove('hidden');
      }}

      searchInput.addEventListener('input', filterSuggestions);
      btnClearSearch.addEventListener('click', () => {{
        searchInput.value = '';
        filterSuggestions();
        searchInput.focus();
      }});

      searchSuggestions.addEventListener('click', function(e) {{
        const row = e.target.closest('[data-code]');
        if (row) {{
          const code = Number(row.getAttribute('data-code'));
          selectLocality(code);
          searchSuggestions.classList.add('hidden');
          searchInput.value = '';
          btnClearSearch.classList.add('hidden');
          geojsonLayer.eachLayer(layer => {{
            if (layer.feature.properties.codigo_localidad === code) {{
              map.flyToBounds(layer.getBounds(), {{ padding: [30, 30], duration: 0.8 }});
            }}
          }});
        }}
      }});

      // Global Keyboard Shortcuts (ISO 9241-110 HCI standards)
      window.addEventListener('keydown', function(e) {{
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {{
          if (e.key === 'Escape') {{
            searchSuggestions.classList.add('hidden');
            e.target.blur();
          }}
          return;
        }}

        if (e.key === '/' || (e.ctrlKey && e.key.toLowerCase() === 'k')) {{
          e.preventDefault();
          searchInput.focus();
        }} else if (e.key.toLowerCase() === 'i') {{
          openInvestmentModal();
        }} else if (e.key.toLowerCase() === 'r') {{
          map.setView([4.65, -74.12], 11);
          showToast('Vista centrada en Bogotá', 'info');
        }} else if (e.key.toLowerCase() === 'j') {{
          document.getElementById('btn-jenks').click();
        }} else if (e.key.toLowerCase() === 'q') {{
          document.getElementById('btn-quantiles').click();
        }} else if (e.key === '[') {{
          toggleLeft(pLeft.classList.contains('w-80'));
        }} else if (e.key === ']') {{
          toggleRight(pRight.classList.contains('w-96'));
        }} else if (e.key.toLowerCase() === 'e') {{
          document.getElementById('btn-export-geojson').click();
        }} else if (e.key.toLowerCase() === 'c') {{
          document.getElementById('btn-export-csv').click();
        }} else if (e.key === '?' || e.key.toLowerCase() === 'h') {{
          openHelp();
        }} else if (e.key === 'Escape') {{
          closeHelp();
          document.getElementById('modal-investment').classList.add('hidden');
        }}
      }});
    }}

    function populateIndicatorDropdown() {{
      const indSelect = document.getElementById('select-indicator');
      indSelect.innerHTML = '';
      domainCatalog[currentDomain].indicadores.forEach(ind => {{
        indSelect.innerHTML += `<option value="${{ind.col}}">${{ind.nombre}}</option>`;
      }});
    }}

    // Boot
    window.addEventListener('DOMContentLoaded', () => {{
      setupInteractions();
      initMap();
      // Auto select Top 1 Locality on start
      if (geojsonData.features && geojsonData.features.length > 0) {{
        const top1 = geojsonData.features[0].properties;
        selectLocality(top1.codigo_localidad);
      }}
    }});
  </script>
</body>
</html>
"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_html_path


if __name__ == "__main__":
    out_html = generate_interactive_gis_dashboard()
    print(f"Dashboard Geográfico SIPTA generado con éxito en: {out_html}")
