# SIPTA — Alcance, supuestos y restricciones

## 1. Propósito

Este documento define el alcance operativo del proyecto SIPTA, los supuestos
necesarios para su desarrollo y las restricciones que condicionan la solución.

Su objetivo es establecer límites claros antes de continuar con el modelo
territorial, la integración de fuentes, los indicadores y la priorización.

---

## 2. Alcance

El proyecto incluye:

- Integración de datos abiertos relacionados con Bogotá D.C.
- Limpieza y transformación de las fuentes seleccionadas.
- Análisis exploratorio de datos.
- Construcción de indicadores territoriales.
- Construcción de índices territoriales.
- Desarrollo de un radar de brechas.
- Desarrollo de un motor de priorización territorial.
- Definición de alertas tempranas cuando la disponibilidad de los datos lo permita.
- Construcción de un dashboard ejecutivo.
- Elaboración de documentación técnica y metodológica.
- Preparación de la presentación final del proyecto.

### Unidad territorial principal

Para el MVP del proyecto se adopta la **localidad** como unidad territorial
primaria de análisis.

Bogotá D.C. cuenta con **20 localidades**, que constituyen la referencia
territorial común para la integración de los diferentes dominios.

Las fuentes que utilicen otras granularidades territoriales deberán ser
homologadas o agregadas al nivel de localidad cuando sea técnicamente posible.

---

## 3. Fuera de alcance

El proyecto no incluye:

- Integración directa con sistemas internos de la Alcaldía de Bogotá.
- Automatización productiva en infraestructura cloud.
- Desarrollo de una aplicación móvil.
- Uso de inteligencia artificial generativa como componente funcional del producto.
- Construcción de modelos predictivos complejos cuando no existan series
  históricas suficientes.
- Implementación de una plataforma productiva de actualización automática de datos.
- Análisis territorial completo a nivel de barrio o UPZ como unidad principal
  del MVP.

---

## 4. Supuestos

El proyecto parte de los siguientes supuestos:

1. Los datasets requeridos para el DataJam pueden descargarse o consultarse
   desde fuentes públicas.

2. Las fuentes utilizadas disponen de algún mecanismo que permita su
   territorialización, por ejemplo:

   - código de localidad;
   - nombre de localidad;
   - UPZ o barrio homologable;
   - coordenadas geográficas.

3. El equipo puede utilizar Python para procesamiento y análisis de datos.

4. Git y GitHub pueden utilizarse para control de versiones y colaboración.

5. El equipo dispone de una herramienta de visualización para la construcción
   del dashboard.

6. Los datasets utilizados cuentan con condiciones de reutilización pública.

7. Los datos oficiales constituyen la referencia primaria del proyecto, pero
   deben someterse a controles de calidad antes de ser utilizados
   analíticamente.

8. Cuando un indicador requiera comparabilidad territorial podrá normalizarse
   por población, área, capacidad o demanda, siempre que la fórmula y el
   denominador utilizado queden documentados.

9. Toda transformación deberá mantener trazabilidad respecto a la fuente
   original.

---

## 5. Restricciones

El proyecto está condicionado por las siguientes restricciones:

### Equipo

El trabajo es desarrollado por un equipo de **3 personas**, por lo que deben
evitarse actividades duplicadas y mantenerse claramente delimitadas las
responsabilidades.

### Tiempo

El tiempo disponible para el DataJam es limitado.

Por esta razón, el MVP prioriza el análisis al nivel de **localidad** y evita
aumentar innecesariamente la granularidad territorial.

### Recursos computacionales

Los recursos de cómputo disponibles son limitados, por lo que se priorizan
métodos reproducibles, interpretables y adecuados al volumen real de los datos.

### Calidad de los datos

La solución depende directamente de:

- disponibilidad de las fuentes;
- completitud;
- consistencia;
- actualidad;
- precisión;
- capacidad de territorialización.

Los problemas de calidad detectados deberán documentarse y no corregirse
arbitrariamente en los archivos originales.

### Series históricas

Los modelos predictivos dependerán de la existencia de series temporales
suficientes.

Cuando estas no existan, deberán priorizarse indicadores, índices, reglas de
priorización y alertas interpretables.

---

## 6. Principio de preservación de datos

Los archivos almacenados en `data/raw` representan las fuentes originales del
proyecto y no deben modificarse manualmente.

Las operaciones de:

- limpieza;
- normalización;
- homologación;
- agregación;
- territorialización;
- integración;

deberán realizarse en etapas posteriores y conservar trazabilidad respecto al
archivo original.

---

## 7. Relación con el modelo territorial

El modelo territorial permitirá que los distintos dominios del proyecto
utilicen una referencia común.

El flujo conceptual será:

`Fuentes → Validación → Limpieza → Estandarización → Modelo territorial → Indicadores → Índices → Priorización`

La unidad territorial común será representada mediante `DIM_TERRITORIO`.

---

## 8. Estado

- Alcance definido.
- Supuestos documentados.
- Restricciones documentadas.
- Unidad territorial primaria definida: **Localidad**.
- Modelo territorial detallado: pendiente.
- `DIM_TERRITORIO`: pendiente de definición e implementación.