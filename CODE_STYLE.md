# Guía de Estilo de Código (CODE_STYLE) — Sistema Hotelero SUMAQ

Este documento establece las convenciones de estilo, estándares de programación y buenas prácticas de **Clean Code** obligatorias para el proyecto **SUMAQ**[cite: 1, 11]. Todo código subido mediante Pull Request al repositorio debe cumplir con estas pautas para garantizar su mantenibilidad, legibilidad y calidad[cite: 1, 5, 87].

---

## Stack Tecnológico del Proyecto

* **Backend:** PHP 8.2 | Framework CodeIgniter 4
* **Frontend:** JavaScript / TypeScript | Framework Vue.js 3 (SPA)
* **Base de Datos:** MySQL 8.0 (`utf8mb4`)[cite: 90]
* **Estándar de Formato:** PSR-12 (PHP) / ESLint + Prettier (Vue/JS)

---

## Principios Generales de Clean Code

1. **Responsabilidad Única (SRP):** Cada clase, función o componente debe tener una única razón para cambiar[cite: 1, 3]. Separa estrictamente la lógica de negocio, controladores y acceso a datos[cite: 3].
2. **Nombres Significativos:** Usa nombres expresivos y en inglés o español técnico coherente (preferencia en español para el dominio de negocio hotelero: `reserva`, `huesped`, `habitacion`)[cite: 1, 3, 91].
3. **Funciones Pequeñas:** Las funciones no deben superar las 20-30 líneas de código[cite: 1, 3]. Una función debe realizar una sola acción y hacerla bien[cite: 1, 3].
4. **No Te Repitas (DRY):** Centraliza reglas complejas (como el cálculo de tarifas por temporada o validaciones de *overbooking*) en servicios o modelos reutilizables[cite: 1, 3, 13].
5. **Manejo Explicito de Errores:** Devuelve respuestas estructuradas HTTP/JSON claras para errores de validación o del negocio; no uses retornos ambiguos como `false` o `0`[cite: 1, 3, 4].
6. **Cero Credenciales:** Prohibido incluir tokens, contraseñas, URLs de BD o archivos `.env` en el código fuente[cite: 5, 7].

---

## 🐘 Backend: PHP 8.2 & CodeIgniter 4

### 1. Convenciones de Nombres
* **Clases y Controladores:** `PascalCase` (Ejemplo: `ReservaController`, `HuespedModel`)[cite: 91].
* **Métodos y Funciones:** `camelCase` (Ejemplo: `obtenerDisponibilidad()`, `cancelarReserva()`)[cite: 91].
* **Variables:** `camelCase` (Ejemplo: `$habitacionId`, `$montoTotal`).
* **Constantes:** `UPPER_SNAKE_CASE` (Ejemplo: `ESTADO_RESERVADO`, `TARIFA_BASE`).
* **Archivos PHP:** Mismo nombre de la clase expuesta, respetando `PascalCase.php`.

### 2. Estándar de Código (PSR-12)
* Activa siempre el tipado estricto en la primera línea de cada archivo PHP:
  ```php
  <?php

  declare(strict_types=1);

  namespace App\Controllers;
