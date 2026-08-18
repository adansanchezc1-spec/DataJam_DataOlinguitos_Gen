---
name: unit-testing
description: Pruebas unitarias, cobertura (≥80%), TDD/BDD y control de calidad — diseño de suites con pytest/JUnit, fixtures, mocks, tests parametrizados y documentación de planes/resultados de prueba.
---

# Skill 04 — Pruebas Unitarias y Calidad
**Fase PDCO**: CONTROL | **SDLC Stage**: Testing

---

## Propósito

Garantizar la calidad, confiabilidad y ausencia de regresiones del software mediante pruebas automatizadas con patrón **AAA**, cobertura mínima del **80%**, y documentación completa del plan y resultados de prueba conforme a **SWEBOK** (Capítulo 4) e **ISO/IEC 25010**.

---

## Workflow de Ejecución

```
ENTRADA: Código implementado (Skill 03) + requirements.md (Skill 01)
    │
    ▼
[1] PLAN DE PRUEBAS
    │   Identificar casos de prueba por cada Requerimiento Funcional (RF)
    │   Definir criterios de aceptación y tipos de prueba
    │
    ▼
[2] DISEÑO DE CASOS DE PRUEBA
    │   Happy path (flujo exitoso principal)
    │   Edge cases (límites, 0, vacíos, nulos)
    │   Error cases (excepciones de dominio esperadas)
    │   Boundary value analysis (valores frontera)
    │
    ▼
[3] IMPLEMENTACIÓN DE TESTS
    │   Patrón AAA: Arrange → Act → Assert
    │   Mocks / Stubs para aislar dependencias externas (DB, red, I/O)
    │   Fixtures reusables y tests parametrizados (`@pytest.mark.parametrize`)
    │
    ▼
[4] EJECUCIÓN Y COBERTURA
    │   Coverage ≥ 80% (líneas y ramas)
    │   Identificar y cubrir líneas no ejecutadas
    │
    ▼
[5] DOCUMENTACIÓN DE RESULTADOS
    │
    ▼
SALIDA: tests/ + test-plan.md + test-results.md
```

---

## Taxonomía y Métricas de Calidad

```
COBERTURA MÍNIMA
├── Líneas de código: ≥ 80%
├── Ramas condicionales: ≥ 75%
├── Métodos/Funciones: ≥ 85%
└── Cero tests en rojo (100% passing)

REGLAS DE CALIDAD DE PRUEBAS
├── Un solo concepto o aserción lógica por test
├── Nombres autoexplicativos: test_[metodo]_[escenario]_[resultado_esperado]
├── Sin lógica de control (sin `if` o bucles `for` complejos dentro del test)
├── Tests deterministas, aislados e independientes entre sí
└── Ejecución ultra rápida (< 100ms por test unitario)
```

---

## Implementación Estándar (pytest)

```python
import pytest
from unittest.mock import Mock
from src.dominio.servicios.servicio_usuario import ServicioUsuario
from src.dominio.excepciones import UsuarioYaExisteException


class TestServicioUsuario:
    """Suite de pruebas unitarias para ServicioUsuario bajo patrón AAA."""

    @pytest.fixture
    def repositorio_mock(self) -> Mock:
        return Mock()

    @pytest.fixture
    def servicio(self, repositorio_mock: Mock) -> ServicioUsuario:
        return ServicioUsuario(repositorio=repositorio_mock)

    def test_registrar_usuario_con_datos_validos_crea_usuario_exitosamente(
        self, servicio: ServicioUsuario, repositorio_mock: Mock
    ) -> None:
        """RF-001: Registro exitoso con email único."""
        # Arrange
        repositorio_mock.existe_por_email.return_value = False
        repositorio_mock.guardar.return_value = Mock(id=1, nombre="Juan")
        comando = {"nombre": "Juan Pérez", "email": "juan@test.com"}

        # Act
        resultado = servicio.registrar_usuario(comando)

        # Assert
        assert resultado.id == 1
        repositorio_mock.guardar.assert_called_once()

    def test_registrar_usuario_email_duplicado_lanza_excepcion(
        self, servicio: ServicioUsuario, repositorio_mock: Mock
    ) -> None:
        """RF-001: Rechazo de registro duplicado."""
        # Arrange
        repositorio_mock.existe_por_email.return_value = True
        comando = {"nombre": "Juan", "email": "duplicado@test.com"}

        # Act & Assert
        with pytest.raises(UsuarioYaExisteException):
            servicio.registrar_usuario(comando)

    @pytest.mark.parametrize("nombre_invalido", ["", "   ", None])
    def test_registrar_usuario_nombre_invalido_lanza_value_error(
        self, servicio: ServicioUsuario, nombre_invalido: str | None
    ) -> None:
        """Validación de entradas inválidas."""
        with pytest.raises(ValueError):
            servicio.registrar_usuario({"nombre": nombre_invalido, "email": "a@b.com"})
```

---

## Checklist de Completitud

- [ ] Plan de pruebas documentado con cobertura por RF
- [ ] Happy path, error cases y edge cases implementados
- [ ] Tests parametrizados para particiones de equivalencia
- [ ] Mocks y fixtures aíslan 100% dependencias de I/O
- [ ] Cobertura ≥ 80% alcanzada
- [ ] Cero tests dependientes del orden de ejecución
- [ ] `docs/04-testing/test-plan.md` creado
- [ ] `docs/04-testing/test-results.md` generado
- [ ] `metadata.json` actualizado con `"active_skill": "04-testing"`
