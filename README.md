# SIGH-Sumaq_Ing_software1
# Sistema de Gestión Hotelera "SUMAQ" (SGH)

[![PHP](https://img.shields.io/badge/PHP-8.2-777BB4?logo=php)](https://www.php.net/)
[![CodeIgniter](https://img.shields.io/badge/CodeIgniter-4.x-EF4223?logo=codeigniter)](https://codeigniter.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vuedotjs)](https://vuejs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)](https://www.mysql.com/)

El Sistema de Gestión Hotelera "SUMAQ" es un software diseñado para centralizar y automatizar las operaciones administrativas y operativas de un establecimiento hotelero, optimizando los flujos de trabajo de recepción, clientes y administración.
---

**Descripción del Proyecto**

El sistema reemplaza procesos manuales o fragmentados mediante una arquitectura en capas basada en **APIs REST** con desacoplamiento físico. Permite gestionar clientes, inventario de habitaciones, reservas, check-in/check-out, procesamiento de pagos y métricas en tiempo real.

---

**Equipo de Desarrollo & Roles**

| Integrante | Rol en el Proyecto | Módulo a Cargo |
| :--- | :--- | :--- |
| **Jhosep Rodrigo Arocutipa Mamani** | Líder Técnico / Backend Dev | Arquitectura Base, Autenticación y Módulo de Reservas |
| **Hugo Antonio Ordoño Quispe** | Scrum Master / Analista Funcional | Módulo de Huéspedes y Estadía (Check-in / Check-out) |
| **Ronald Alexander Huaman Huanca** | Product Owner / Frontend Dev | Módulo de Habitaciones, Tarifas e Interfaz Vue.js |
| **Marco Antonio Mamani Murillo** | QA / DBA / Developer | Módulo de Pagos, Reportes, Base de Datos y Pruebas |

---

**Arquitectura y Tecnologías**

El proyecto sigue una arquitectura desacoplada en tres capas principales:

* **Frontend (Presentación):** Vue.js 3 (Single Page Application - SPA responsive).
* **Backend (Servicios API REST):** PHP 8.2 con CodeIgniter 4 (respuestas en formato JSON, middleware de autenticación y filtros por roles).
* **Base de Datos:** MySQL 8.0 (`utf8mb4`).
* **Despliegue / Servidor:** VPS Linux (Nginx/Apache), GitHub Actions (CI/CD).
* 
**Funcionalidades Principales**

* **Módulo de Clientes:** Registro, modificación, consulta y gestión de historial de estancias y puntos de fidelidad.
* **Módulo de Habitaciones:** Control de inventario, consulta de disponibilidad por rango de fechas, asignación de tarifas de temporada y bloqueo por mantenimiento.
* **Módulo de Reservas:** Creación, consulta y cancelación de reservas evitando traslapes (*overbooking*), junto al registro de Check-in y Check-out.
* **Módulo de Pagos y Facturación:** Múltiples métodos de pago (Efectivo, Tarjeta, Transferencia), aplicación de cupones/descuentos y gestión de reembolsos.
* **Módulo de Administración:** Control de usuarios internos mediante RBAC, configuración de parámetros del hotel (impuestos, horarios) y dashboard con indicadores (porcentaje de ocupación e ingresos).

---

**Endpoints Principales de la API**

| Método | Ruta | Acción / Controlador | Descripción |
| :---: | :--- | :--- | :--- |
| `GET` | `/api/reservas/disponibilidad` | `ReservaController::disponibilidad` | Consulta habitaciones disponibles por fechas |
| `POST` | `/api/reservas` | `ReservaController::crear` | Crea una nueva reserva |
| `PUT` | `/api/reservas/{id}/cancelar` | `ReservaController::cancelar` | Cancela una reserva activa |
| `POST` | `/api/huespedes` | `HuespedController::registrar` | Registra a un nuevo huésped |
| `POST` | `/api/reservas/{id}/checkin` | `HuespedController::checkin` | Realiza el ingreso del cliente |
| `POST` | `/api/pagos` | `PagoController::registrar` | Registra el pago asociado a una reserva |
| `GET` | `/api/reportes/ocupacion` | `ReporteController::ocupacion` | Métricas de ocupación en el dashboard |

---

**Requisitos para Instalación Local**

* **PHP** >= 8.2
* **Composer** >= 2.0
* **Node.js** >= 18.x / **npm**
* **MySQL Server** >= 8.0

---

## 🔧 Pasos de Instalación

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/TU-USUARIO/sumaq-hotel.git](https://github.com/TU-USUARIO/sumaq-hotel.git)
cd sumaq-hotel
