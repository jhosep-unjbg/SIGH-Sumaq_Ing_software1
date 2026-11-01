# Guía de Contribución (CONTRIBUTING) — Sistema Hotelero SUMAQ

¡Bienvenido al repositorio del proyecto **SUMAQ**![cite: 11] Este documento establece el flujo de trabajo, las reglas de Git, los estándares de contribución y las ceremonias que todo integrante del equipo debe seguir para colaborar de forma ordenada y profesional[cite: 1, 5, 81].

---

## Principios de Gobierno del Equipo

* **Comunicación Oficial:** La gestión de tareas, historias de usuario e incidentes se realiza exclusivamente a través de **GitHub Issues** y **GitHub Projects**[cite: 5, 81].
* **Revisión Obligatoria:** Queda estrictamente **prohibido realizar push directo** a las ramas `main` y `develop`. Todo cambio ingresa mediante Pull Request (PR).
* **Definición de Hecho (DoD):** Ningún trabajo se considera terminado si no cumple con la *Definition of Done* (pruebas pasando, código limpio, revisión aprobada y documentación actualizada)[cite: 1, 65, 85].

---

## Estrategia de Ramas (GitFlow Adaptado)

El repositorio se organiza bajo las siguientes ramas de trabajo[cite: 87]:

* **`main`**: Contiene únicamente código estable, auditado y listo para despliegue en producción o entrega académica.
* **`develop`**: Rama de integración continua donde se consolidan las funcionalidades desarrolladas durante el Sprint[cite: 87].
* **`feature/RF-XXX-nombre`**: Ramas de desarrollo creadas a partir de `develop` para implementar una Historia de Usuario o Requisito Funcional específico (Ejemplo: `feature/RF-012-registrar-reserva`)[cite: 87].
* **`fix/DEF-XXX-nombre`**: Ramas cortas para la corrección de errores reportados en pruebas de QA (Ejemplo: `fix/DEF-003-error-calculo-noches`)[cite: 87].

---

## Flujo Paso a Paso para Contribuir

### 1. Asignación de la Tare/Issue
1. Revisa el tablero en **GitHub Projects** y selecciona una Issue priorizada que cumpla con la **Definition of Ready (DoR)**[cite: 5, 81, 85].
2. Asígnate la Issue y cambia su estado a `In Progress`.

### 2. Crear la Rama de Trabajo
Actualiza tu repositorio local y crea tu rama desde `develop`[cite: 87]:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/RF-XXX-descripcion-corta
