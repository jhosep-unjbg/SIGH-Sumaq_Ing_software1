# Política de Seguridad - Proyecto SUMAQ (Sistema de Gestión Hotelera)

## 1. Versiones Soportadas

Actualmente, solo el incremento activo en el entorno del VPS Linux institucional y la rama `develop`/`main` reciben actualizaciones y parches de seguridad.

| Versión | Soportada | Stack Tecnológico Base |
| :--- | :--- | :--- |
| MVP Heredado | No | SQLite local sin llaves foráneas / Monolítico estático |

## 2. Reporte de Vulnerabilidades

El equipo del proyecto SUMAQ prioriza la integridad de la información hotelera y financiera. Si identificas un fallo o vulnerabilidad de seguridad:

1. **Contactos Principales:** Notifica directamente a:
   * **Líder Técnico / Backend:** Jhose Arocutipa
   * **Analista de Calidad (QA) / DBA:** Marco Mamani
2. **Procedimiento de Reporte:**
   * Registrar un informe privado indicando el componente afectado (Frontend Vue.js, API REST CodeIgniter o Base de Datos MySQL).
   * Adjuntar pasos para reproducir el fallo y el nivel de riesgo estimado (ej. inyección SQL, bypass de roles, exposición de credenciales).
3. **Plazo de Respuesta:** El equipo responderá en un plazo máximo de 24 horas y coordinará la corrección prioritaria en una rama de tipo `fix/`.

## 3. Medidas y Estándares de Seguridad Implementados

### A. Control de Acceso Basado en Roles (RBAC) - RNF-03
* **Filtros de Autenticación:** Las peticiones a la API REST requieren validación mediante tokens en formato JSON.
* **Segregación de Funciones:** Las interfaces y endpoints están restringidos según los roles del sistema (Administrador, Recepcionista, Personal de Limpieza/Mantenimiento).
* **Bloqueo Directo:** Cualquier intento de acceso no autorizado mediante URL directa o manipulación de parámetros se bloquea tanto en la capa de presentación como en la de servicios.

### B. Protección de Información Sensible y Cifrado - RNF-04
* **Almacenamiento de Credenciales:** Las contraseñas de los usuarios no se almacenan en texto plano; se procesan con algoritmos de hash seguros (`passwordHash`).
* **Tráfico Cifrado:** Las comunicaciones entre la aplicación web SPA y los servidores backend se ejecutan bajo HTTPS/TLS. La transmisión de notificaciones/correos utiliza el protocolo SMTP/TLS.
* **Prevención de Inyección SQL:** Todas las consultas a la base de datos MySQL 8 utilizan sentencias preparadas mediante el ORM/Modelos de CodeIgniter 4, prohibiendo consultas SQL concatenadas.

### C. Integridad Referencial y Transacciones ACID - RNF-08 / RNF-09
* **Claves Foráneas Habilitadas:** Restricciones de integridad referencial activas a nivel de esquema en MySQL 8 para evitar registros huérfanos en tablas de reservas, pagos y huéspedes.
* **Transacciones Atómicas:** Las operaciones sensibles (registro de pagos, aplicación de descuentos y procesamiento de reembolsos) se ejecutan dentro de bloques transaccionales ("todo o nada").

### D. Respaldos y Disponibilidad - RNF-13
* **Respaldos Automáticos:** Copias de seguridad de la base de datos programadas cada 24 horas.
* **Almacenamiento Aislado:** Los archivos de respaldo se almacenan fuera del servidor principal del VPS para permitir una restauración limpia ante contingencias.

### E. Seguridad en el Repositorio y Despliegue (SCM)
* **Secretos e Integridad:** Prohibida la inclusión de cadenas de conexión hardcodeadas o claves privadas dentro del código fuente.
* **Revisiones Obligatorias:** Todo código integrado debe pasar por revisión por pares (Code Review) y Pull Requests a la rama `develop`.
