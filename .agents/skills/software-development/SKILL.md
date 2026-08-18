---
name: software-development
description: Desarrollo de software y pipelines de datos de alta calidad — implementa código limpio en Python (PEP 8) y Java (Google Style), POO avanzada, SOLID, inyección de dependencias y genera dev-logs.
---

# Skill 03 — Desarrollo de Software
**Fase PDCO**: DEVELOPMENT | **SDLC Stage**: Implementation

---

## Propósito

Implementar software y pipelines de datos de forma limpia, mantenible y robusta siguiendo **Clean Code**, **PEP 8** (Python), **Google Java Style Guide**, **POO avanzada**, **SOLID** y los patrones definidos en la Skill 02, manteniendo trazabilidad hacia los requerimientos de la Skill 01.

---

## Workflow de Ejecución

```
ENTRADA: architecture.md + patterns.md + requirements.md
    │
    ▼
[1] SETUP DEL PROYECTO
    │   Estructura modular de carpetas
    │   Gestión de dependencias y entornos
    │   Configuración de linters, formateadores y tipado estático
    │
    ▼
[2] IMPLEMENTACIÓN POR CAPAS (Inside-Out)
    │   Dominio (Entidades, Value Objects, Puertos/Interfaces)
    │   Aplicación (Casos de uso, Servicios de aplicación, DTOs)
    │   Infraestructura (Adaptadores DB, APIs externas, I/O)
    │   Presentación (APIs REST, CLI, Dashboards)
    │
    ▼
[3] CLEAN CODE & ESTÁNDARES
    │   Funciones pequeñas (< 20 líneas), cohesivas
    │   Nombres descriptivos y sin abreviaturas oscuras
    │   Type hints estrictos en Python (typing / dataclasses / pydantic)
    │
    ▼
[4] REVISIÓN PEP 8 / JAVA STYLE
    │   Black, flake8, isort, mypy / Checkstyle
    │
    ▼
[5] DOCUMENTACIÓN DE APIS Y REGISTRO DE DESARROLLO
    │   Docstrings explicativos del PORQUÉ
    │   Registro en dev-log.md y api-docs.md
    │
    ▼
SALIDA: Código fuente limpio + dev-log.md + api-docs.md
```

---

## Estándares de Código Obligatorios

### Python (PEP 8 + Type Hints + Dataclasses)
```python
from dataclasses import dataclass
from typing import Protocol, Optional, List


MAX_REINTENTOS_CONEXION: int = 3


@dataclass(frozen=True)
class IndicadorTerritorialDTO:
    """Objeto de transferencia inmutable para métricas territoriales."""
    codigo_divipola: str
    nombre_municipio: str
    indice_priorizacion: float


class RepositorioIndicadores(Protocol):
    """Puerto de repositorio abstracto para el cálculo de índices."""

    def obtener_por_municipio(self, divipola: str) -> Optional[IndicadorTerritorialDTO]:
        """Obtiene las métricas calculadas para un municipio específico."""
        ...

    def guardar_batch(self, indicadores: List[IndicadorTerritorialDTO]) -> None:
        """Persiste una lista de indicadores calculados."""
        ...
```

### Reglas de Clean Code
```
NOMBRES
├── Variables: descripción clara del contenido (ej: municipios_priorizados, latencia_ms)
├── Funciones: verbos en infinitivo (ej: calcular_indice_priorizacion, validar_esquema_datos)
├── Clases: sustantivos en PascalCase (ej: CalculadorIndiceSIPTAService)
└── Prohibido: x, data, temp, aux, do_it, manager

FUNCIONES
├── Máximo 20 líneas (idealmente < 10 líneas)
├── Un solo nivel de abstracción y una única responsabilidad
├── Máximo 3 parámetros (agrupar en DTO/dataclass si requiere más)
└── Cero efectos secundarios ocultos

ESTRUCTURA Y FORMATO
├── Inyección de dependencias en constructores
├── Manejo de excepciones de dominio específicas
└── Tipado estático validado
```

---

## Checklist de Completitud

- [ ] Estructura de proyecto modular organizada según arquitectura
- [ ] Dominio implementado primero (entidades, value objects, interfaces)
- [ ] Principios SOLID cumplidos en cada clase/módulo
- [ ] PEP 8 estricto verificado con Type Hints en todo Python
- [ ] Nombres descriptivos y funciones pequeñas (< 20 líneas)
- [ ] Sin variables mágicas ni rutas hardcodeadas
- [ ] Docstrings en todas las funciones y clases públicas
- [ ] Inyección de dependencias implementada
- [ ] `docs/03-development/dev-log.md` actualizado
- [ ] `docs/03-development/api-docs.md` generado
- [ ] `metadata.json` actualizado con `"active_skill": "03-development"`
