---
name: maintenance-refactoring
description: Mantenimiento, optimización y refactorización segura — detección de code smells, eliminación de deuda técnica y antipatrones, perfilado de rendimiento y gestión de changelogs.
---

# Skill 05 — Mantenimiento, Optimización y Refactorización
**Fase PDCO**: OPERATIONS | **SDLC Stage**: Maintenance

---

## Propósito

Mantener y elevar continuamente la calidad del software existente mediante la identificación sistemática de deuda técnica, antipatrones y refactorizaciones seguras (tests primero), siguiendo el catálogo de **Martin Fowler**, **SWEBOK** (Capítulo 5) e **ISO/IEC 14764**.

---

## Workflow de Ejecución

```
ENTRADA: Código fuente existente + suite de tests en verde
    │
    ▼
[1] DIAGNÓSTICO DE SALUD DEL CÓDIGO
    │   Code Smells (Long Method, Large Class, Primitive Obsession, etc.)
    │   Violaciones SOLID y antipatrones
    │   Complejidad ciclomática y duplicación
    │
    ▼
[2] PRIORIZACIÓN DE DEUDA TÉCNICA
    │   Clasificación: Crítica / Alta / Media / Baja
    │   Evaluación Impacto vs Esfuerzo
    │
    ▼
[3] REFACTORIZACIÓN SEGURA (Tests Primero)
    │   Verificar tests en verde ANTES de tocar el código
    │   Aplicar un cambio atómico a la vez (Extract Method, Replace Conditional, etc.)
    │   Verificar tests en verde DESPUÉS de cada cambio
    │
    ▼
[4] OPTIMIZACIÓN BASADA EN PERFILADO
    │   Medir con herramientas de profiling (cProfile)
    │   Optimizar complejidad algorítmica (O(n²) → O(n log n) / O(1))
    │
    ▼
[5] DOCUMENTACIÓN DE MEJORAS
    │   Registro en refactoring-log.md
    │   Actualización de changelog.md (Keep a Changelog)
    │
    ▼
SALIDA: Código refactorizado + changelog.md + refactoring-log.md
```

---

## Catálogo de Refactorizaciones Clave

```
CODE SMELL                   REFACTORIZACIÓN RECOMENDADA
─────────────────────────────────────────────────────────────
Long Method (>20 líneas)     → Extract Method (crear métodos con nombres descriptivos)
Large Class (>300 líneas)    → Extract Class / Move Method (aplicar SRP)
Long Parameter List (>3)     → Introduce Parameter Object (Dataclass / DTO)
Switch / if-elif por tipo    → Replace Conditional with Polymorphism (Strategy)
Duplicate Code               → Extract Method / Pull Up Method (DRY)
Dead Code                    → Eliminar directamente (el VCS conserva el historial)
Speculative Generality       → Eliminar abstracciones innecesarias (YAGNI)
Magic Numbers / Literales    → Replace Magic Number with Named Constant / Enum
```

---

## Regla de Oro de Refactorización Segura

```
1. 🟢 Verificar que el 100% de los tests pasan antes de modificar.
2. 🔄 Realizar una sola transformación a la vez.
3. 🟢 Ejecutar la suite de tests inmediatamente tras cada cambio.
4. 🚫 Si un test falla, revertir el cambio de inmediato, no parchear.
5. 📝 Registrar la refactorización (REF-XXX) en refactoring-log.md.
```

---

## Checklist de Completitud

- [ ] Diagnóstico de code smells y antipatrones documentado
- [ ] Suite de pruebas validada en verde antes de empezar
- [ ] Refactorizaciones atómicas aplicadas paso a paso
- [ ] Tests en verde tras cada refactorización sin degradar cobertura
- [ ] Optimizaciones justificadas con mediciones objetivas
- [ ] `docs/05-maintenance/refactoring-log.md` actualizado
- [ ] `docs/05-maintenance/changelog.md` actualizado
- [ ] `metadata.json` actualizado con `"active_skill": "05-maintenance"`
