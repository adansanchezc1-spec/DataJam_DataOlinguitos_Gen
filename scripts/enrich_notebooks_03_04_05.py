"""Enriquece y actualiza exhaustivamente los cuadernos de integración, modelado y visualización."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = ROOT / "notebooks"


def update_integration_master_nb():
    nb_path = NOTEBOOKS_DIR / "03_integration" / "01_integration_master.ipynb"
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Insertar celda de documentación de fuentes oficiales al inicio
    intro_cell = nb["cells"][0]
    intro_cell["source"] = [
        "# SIPTA: Integración Territorial Multidominio -- Tablón Maestro de Bogotá D.C.\n",
        "\n",
        "**Fase PDCO**: DEVELOPMENT -> CONTROL | **Sprint**: 5  \n",
        "**Estándares**: Clean Code, PEP 8, DAMA-BOK (Data Integration & Quality), SWEBOK Cap. 2 y 5, IEEE 830 (RF-003, RF-005, RF-007, RF-009, RF-018, RF-019)  \n",
        "**Sistema**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA)\n",
        "\n",
        "---\n",
        "\n",
        "## 🎯 Propósito y Alcance del Cuaderno\n",
        "Este cuaderno constituye el **nodo central de la fase de Integración de Datos (03_integration)**. Su objetivo exclusivo es:\n",
        "1. **Fuente Única de Población DANE/SDP (2018-2035)**: Integrar las proyecciones oficiales distritales (Total Bogotá 2025: **8.101.412 habitantes**) para todas las 20 localidades canónicas.\n",
        "2. **Microdatos PUA SDIS 2024 (1.048.575 registros)**: Incorporar atenciones y beneficiarios del Ingreso Mínimo Garantizado (IMG: 666.7k atenciones), comedores comunitarios (43.6k beneficiarios), comisarías y atención a habitante de calle.\n",
        "3. **Homologación Territorial Canónica**: Unificar los 12 dominios sectoriales bajo los códigos DIVIPOLA oficiales.\n",
        "4. **Feature Engineering Multidominio**: Derivar densidades espaciales (hab/km²) y tasas per cápita estandarizadas por 1.000, 10.000 y 100.000 habitantes.\n",
        "5. **Persistencia Contractual**: Exportar el Tablón Maestro Territorial consolidado a `data/processed/master_localidades.csv` (111 columnas x 20 localidades).\n",
    ]

    # Asegurar que la celda de ensamblaje ejecute build_master_table()
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            if "build_master_table" in source:
                cell["source"] = [
                    "# Construcción del Tablón Maestro Multidominio Integrado\n",
                    "df_master = build_master_table()\n",
                    "print(f'Tablon Maestro Territorial generado: {df_master.shape[0]} localidades x {df_master.shape[1]} variables')\n",
                    "display(df_master[['codigo_localidad', 'nombre_localidad', 'poblacion', 'area_km2', 'tasa_transferencias_img_por_10k_hab', 'atenciones_totales_sdis', 'total_sedes_ips']].head())\n",
                ]
                break

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("[OK] 01_integration_master.ipynb actualizado.")


def update_modeling_ipt_nb():
    nb_path = NOTEBOOKS_DIR / "04_modeling" / "01_modeling_ipt.ipynb"
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Actualizar la introducción con la fórmula de vulnerabilidad PUA y el Top 5 oficial
    intro_cell = nb["cells"][0]
    intro_cell["source"] = [
        "# SIPTA: Modelado Territorial y Cálculo Matemático Exhaustivo del IPT\n",
        "\n",
        "**Fase PDCO**: DEVELOPMENT -> CONTROL | **Sprint**: 5  \n",
        "**Estándares**: SWEBOK Cap. 2 & Cap. 4, DAMA-BOK, ISO/IEC 25010, OECD/JRC Composite Indicators Handbook, Clean Code, PEP 8  \n",
        "**Sistema**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA)\n",
        "\n",
        "---\n",
        "\n",
        "## 🎯 Propósito y Alcance del Cuaderno\n",
        "Este cuaderno expone **paso a paso y con rigor matemático cómo se calcula cada uno de los Índices de Priorización Territorial (IPT)**, desglosando:\n",
        "1. **Montaje de Tablas Maestras**: Generación de las 12 tablas temáticas curadas en `data/curated/`.\n",
        "2. **Sub-Índice de Vulnerabilidad Social PUA SDIS**: Integración de transferencias monetarias IMG y comercio informal:\n",
        "   $$s_{i, \\text{vuln}} = 0.70 \\cdot \\text{Norm}_{\\text{MinMax}}(\\text{Tasa IMG}_i) + 0.30 \\cdot \\text{Norm}_{\\text{MinMax}}(\\text{Tasa RIVI}_i)$$\n",
        "3. **Cálculo de los 5 Escenarios de IPT ($[0, 100]$)**:\n",
        "   - $\\text{IPT}_{\\text{Base}}$ (7 dimensiones balanceadas, $w_d = 1/7$).\n",
        "   - $\\text{IPT}_{\\text{Rangos}}$ (Normalización no paramétrica por percentiles).\n",
        "   - $\\text{IPT}_{\\text{SinParques}}$ (6 dimensiones, exclusión de infraestructura IDRD, $w_d = 1/6$).\n",
        "   - $\\text{IPT}_{\\text{SinRIVI}}$ (6 dimensiones, exclusión de vendedores informales, $w_d = 1/6$).\n",
        "   - $\\text{IPT}_{\\text{SinProxies}}$ (5 dimensiones duras: Educación, Salud, Movilidad, Ambiente y Seguridad, $w_d = 1/5$).\n",
        "4. **Agregación Geométrica No Compensatoria**: $\\text{IPT}_{\\text{Geom}} = \\left( \\prod (s_{i,d} + \\epsilon)^{w_d} \\right) \\times 100$.\n",
        "5. **Incertidumbre y Bootstrap Dirichlet**: Intervalos de confianza al 95% ($B=1.000$ réplicas).\n",
        "6. **Ranking de Consenso Oficial (Top 5 Prioritario)**: 1. Rafael Uribe Uribe, 2. Bosa, 3. Suba, 4. Usme, 5. Kennedy.\n",
    ]

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("[OK] 01_modeling_ipt.ipynb actualizado.")


def update_dict_indicadores_nb():
    nb_path = NOTEBOOKS_DIR / "04_modeling" / "02_diccionario_indicadores_ipt.ipynb"
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    intro_cell = nb["cells"][0]
    intro_cell["source"] = [
        "# SIPTA: Diccionario Metodológico y Catálogo Técnico de Indicadores Territoriales\n",
        "\n",
        "**Fase PDCO**: DEVELOPMENT -> CONTROL | **Sprint**: 5  \n",
        "**Estándares**: DAMA-BOK (Metadata Management), IEEE 830 / ISO 29148, ISO/IEC 25010, OECD/JRC  \n",
        "**Sistema**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas (SIPTA)\n",
        "\n",
        "---\n",
        "\n",
        "## 🎯 Propósito y Alcance del Cuaderno\n",
        "Este cuaderno documenta exhaustivamente las fichas técnicas, formulación en $\\LaTeX$, polaridades y fuentes de los **12 dominios sectoriales de SIPTA**:\n",
        "1. **Demografía DANE/SDP 2025**: Proyecciones oficiales de población por localidad y UPZ (`DEM-001`, `POB-002`, `POB-003`).\n",
        "2. **Vulnerabilidad Social PUA SDIS 2024**: Transferencias Monetarias IMG (`VUL-001`), Comedores Comunitarios (`VUL-002`), Comisarías de Familia (`VUL-003`) y Habitante de Calle (`VUL-004`).\n",
        "3. **Salud, Educación, Movilidad, Infraestructura, Finanzas, Ambiente, Seguridad, Servicios Públicos, Empleo y Participación**.\n",
    ]

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("[OK] 02_diccionario_indicadores_ipt.ipynb actualizado.")


def update_visualization_nb():
    nb_path = NOTEBOOKS_DIR / "05_visualization" / "01_visualization_dashboard.ipynb"
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    intro_cell = nb["cells"][0]
    intro_cell["source"] = [
        "# SIPTA -- Cuaderno 05: Visualización Espacial y Dashboard Geográfico Multicapa\n",
        "\n",
        "**Fase PDCO**: DEVELOPMENT / CONTROL | **Etapa Workflow**: 1.7 Visualización y Exportación  \n",
        "**Versión**: v1.0.0 (Demografía Oficial DANE 2025 & PUA SDIS 2024)  \n",
        "**Estándares**: Clean Code, PEP 8, ISO/IEC 25010, DAMA-BOK, OECD/JRC Composite Indicators Handbook.\n",
        "\n",
        "Este cuaderno integra la capa geoespacial vectorial oficial de las **20 localidades de Bogotá D.C.** con los **13 dominios analíticos** de SIPTA, construyendo mapas coropléticos temáticos, visualización del IPT de consenso con intervalos de confianza bootstrap 95%, y compilando el **Dashboard Web GIS Interactivo** autónomo (`reports/dashboard_geografico_sipta.html`).\n",
    ]

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("[OK] 01_visualization_dashboard.ipynb actualizado.")


if __name__ == "__main__":
    update_integration_master_nb()
    update_modeling_ipt_nb()
    update_dict_indicadores_nb()
    update_visualization_nb()
