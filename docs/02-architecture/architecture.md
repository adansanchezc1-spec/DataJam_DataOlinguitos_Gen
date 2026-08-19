# Documento de Arquitectura de Software — SIPTA
**Proyecto**: Sistema de Indicadores y Priorización Territorial y Alertas Tempranas  
**Versión**: 2.0.0  
**Fecha**: 2026-08-18  
**Fase PDCO**: PLAN → DEVELOPMENT | **SDLC Stage**: System Design  
**Estilo Arquitectónico**: Arquitectura Hexagonal / Pipeline Modular por Capas  
**Autores**: Persona A (Adan Sánchez) & Persona B (Yesid Bello)  

---

## 1. Visión General del Sistema
SIPTA implementa un diseño modular orientado a datos con desacoplamiento entre las capas de **Adquisición**, **Validación de Calidad**, **Limpieza/Homologación**, **Integración Territorial**, **Modelado Analítico** y **Visualización**. Cada módulo opera como un componente autónomo con interfaces claras y funciones de transformación reproducibles.

---

## 2. Decisiones de Arquitectura (ADR Summary)
| ID | Decisión Arquitectónica | Alternativas | Justificación Metodológica |
| :--- | :--- | :--- | :--- |
| **ADR-001** | Arquitectura Hexagonal con Pipeline Modular | Monolito de Notebooks | Permite testabilidad unitaria completa en `tests/`, reutilización en CLI y ejecución independiente. |
| **ADR-002** | Escalado Min-Max [0, 1] e Inversión Polar | Z-Score / Rangos Puros | Mantiene interpretabilidad para tomadores de decisión no técnicos en una escala intuitiva de 0 a 100. |
| **ADR-003** | Homologación Canónica a 20 Localidades D.C. | UPZ / UPL / ZAT | Las 20 localidades constituyen la unidad político-administrativa con capacidad presupuestal y de gobierno local. |

---

## 3. Componentes del Sistema y Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│   Jupyter Notebooks (01 a 05) / Dashboards de Visualización │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    CAPA DE APLICACIÓN                       │
│    src/ingestion  │  src/validation  │  src/cleaning        │
│    src/integration│  src/modeling    │  src/visualization   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                  CAPA DE DOMINIO Y DATOS                    │
│    data/raw/ (Inmutable) │ data/processed/ (Estandarizado)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Patrones de Diseño Aplicados
- **Builder Pattern**: En la construcción de DataFrames enriquecidos y tableros en `src.modeling.calculate_indicators`.
- **Strategy Pattern**: En la selección dinámica de métodos de normalización y ponderación de indicadores.
- **Factory / Dispatcher Pattern**: En la suite de validación `run_full_validation_suite()` para despachar validadores por dominio.
- **Information Expert (GRASP)**: Módulos específicos encapsulan las reglas de negocio de su propio dominio sectorial.
