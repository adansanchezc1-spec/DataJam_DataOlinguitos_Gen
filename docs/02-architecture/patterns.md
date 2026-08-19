# Catálogo de Patrones de Diseño y Buenas Prácticas — SIPTA

**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas  
**Fase PDCO**: DEVELOPMENT | **Estándares**: Clean Code, GoF, GRASP, SOLID  

---

## 1. Patrones GoF Aplicados

| Patrón | Tipo | Componente | Problema que Resuelve |
| :--- | :--- | :--- | :--- |
| **Factory Method** | Creacional | `src/validation/validate_data.py` | Instanciación y despacho dinámico de validadores de calidad según el dominio sectorial. |
| **Strategy** | Comportamiento | `src/modeling/calculate_indicators.py` | Algoritmos intercambiables de normalización (Min-Max, Z-Score, Ratios) según la polaridad de la variable. |
| **Builder** | Creacional | `src/visualization/prepare_visualization.py` | Construcción por pasos de la matriz analítica consolidada y rankings para exportación. |
| **Facade** | Estructural | `src/eda/__init__.py` | Interfaz simplificada y unificada para perfilado, lectura geoespacial y cálculo de indicadores. |

---

## 2. Patrones GRASP y Principios SOLID

- **Single Responsibility (SRP)**: Cada módulo de `src/` tiene una única razón para cambiar (ej. `validate_data.py` solo audita calidad, `clean_data.py` solo transforma).
- **Open/Closed (OCP)**: Nuevos dominios sectoriales se incorporan añadiendo funciones validadoras a la tupla `validators` sin modificar la lógica interna del runner.
- **Dependency Inversion (DIP)**: Los módulos de alto nivel dependen de abstracciones de DataFrames y esquemas de metadatos tipados.
- **Low Coupling & High Cohesion**: Módulos desacoplados que interactúan únicamente a través de tablas intermedias versionadas en `data/processed/`.
