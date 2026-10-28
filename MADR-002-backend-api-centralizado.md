# MADR-002 — Backend API REST Centralizado

**Sistema de Gestión Hotelera SUMAQ**  
**Registro de Decisión Arquitectónica (MADR)**

---

## 1. Propósito del documento

Este documento adapta la estructura genérica de un PMS (Property Management System) al diseño documentado de SUMAQ. **No representa código ya implementado**: el repositorio actual contiene documentación, diagramas y ejemplos pequeños de API; todavía no se verificaron las aplicaciones web, la app móvil, la API funcional ni la base de datos.

---

## 2. Criterios de adaptación

- Una **API REST centralizada** concentra reglas de negocio, acceso a datos e integraciones. Las interfaces y los procesos programados se comunican con ella; solo la API accede directamente a PostgreSQL (**MADR-001**).
- Se proponen dos interfaces web (huéspedes y personal) y una app móvil independiente para limpieza, pendiente de reconciliar con el alcance anterior de dos webs.
- El backend empieza como **monolito modular**. Reservas, Estadías, Operación de habitaciones, Cafetería e inventario, Cuentas y pagos, e Identidad y acceso son módulos internos, no microservicios separados.
- Los proveedores de pagos, reservas externas y notificaciones quedan como adaptadores por definir; su presencia en el árbol no implica integraciones contratadas o terminadas.

---

## 3. La API REST Centralizada

La **API REST Centralizada** del Sistema de Gestión Hotelera SUMAQ es la piedra angular y el núcleo del diseño del software.

Se definió mediante el registro de decisión **MADR-001** para concentrar toda la lógica de negocio, el control de acceso por roles, el registro de auditoría y las reglas de validación en un único contenedor ejecutable (desarrollado en **Python / FastAPI**).

Es el **único componente** que posee acceso directo a la base de datos PostgreSQL, exponiendo un contrato agnóstico e inmutable bajo la especificación **OpenAPI v3.1.0** para alimentar a los tres frontends del sistema:

- Web pública de huéspedes
- Web administrativa del personal
- App móvil de limpieza

---

## 4. Arquitecturas Combinadas (“Arquitectura Híbrida SaaS Multi-Tenant”)

Para lograr alta seguridad, escalabilidad y mantenibilidad sin sobrecargar al equipo de desarrollo con complejidad innecesaria, la API combina **cinco estilos y patrones arquitectónicos** complementarios:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                        ARQUITECTURA HÍBRIDA MULTI-TENANT (SUMAQ API)                                  │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. MONOLITO MODULAR     ──> 6 Bounded Contexts DDD internos en FastAPI (`apps/api/app/modules/`)      │
│ 2. CLEAN ARCHITECTURE   ──> Inversión de Dependencias (Domain, Application, Infrastructure, Pres.)   │
│ 3. SEGREGATED CORE      ──> Microservicios aislados para zonas de alto riesgo (Auth JWT RS256 & Pagos)│
│ 4. MULTI-TENANT (SaaS)  ──> Aislamiento lógico por `TenantId` (UUID) + Row Level Security en DB        │
│ 5. PRIMARY-REPLICA      ──> PostgreSQL Maestro (escritura con FOR UPDATE) + Réplicas (solo lectura)    │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Monolito Modular (Macroestructura del Backend)

En lugar de dividir todo el sistema en decenas de microservicios distribuidos de forma prematura, el núcleo hotelero se compila y despliega como una sola unidad en FastAPI.

Internamente, el código está estrictamente descompuesto en **6 módulos o Bounded Contexts** independientes (según Eric Evans y Vaughn Vernon):

| # | Módulo                    | Responsabilidad principal                                                                 |
|---|---------------------------|-------------------------------------------------------------------------------------------|
| 1 | `reservas`                | Disponibilidad, creación, modificación y anulación de reservas                            |
| 2 | `estadias`                | Huéspedes, asignación, check-in, cargos consultados y check-out                           |
| 3 | `operacion_habitaciones`  | Limpieza, objetos olvidados, bloqueos y mantenimiento                                     |
| 4 | `cafeteria_inventario`    | Consumos, productos, existencias y caducidad                                              |
| 5 | `cuentas_pagos`           | Cargos de estadía, descuentos, pagos, comprobantes y saldos                               |
| 6 | `identidad_acceso`        | Autenticación, usuarios, roles y permisos                                                 |

> Reportes son vistas/procesos de lectura y no un contexto central adicional por ahora. Auditoría, registro y seguridad son capacidades compartidas. Las integraciones externas se aíslan en adaptadores dentro de infraestructura.

### 4.2 Clean Architecture (Microestructura de cada Módulo)

Cada uno de los 6 módulos internos aplica la **Regla de Inversión de Dependencias (DIP)** de Robert C. Martin, organizada en 4 capas concéntricas:

1. **domain/** (Círculo Interno)  
   Lógica pura, entidades, objetos de valor e interfaces del patrón Repository (completamente aislados de SQL, ORMs o librerías externas).

2. **application/**  
   Casos de uso (Use Cases), DTOs y puertos de salida hacia servicios externos.

3. **infrastructure/**  
   Implementación física de la persistencia en PostgreSQL (`SqlRepository`), adaptadores de pasarelas de pago y servicios de correo/notificación.

4. **presentation/**  
   Endpoints HTTP en FastAPI (`routes.py`), esquemas de validación de entrada/salida (`schemas.py`) y dependencias.

### 4.3 Núcleo Segregado (Segregated Core)

Aplica el patrón de **Segregated Core** (Evans / Vernon). Para mantener la seguridad bajo el modelo Zero Trust (NIST SP 800-207), se extraen como microservicios autónomos e independientes del monolito central las zonas críticas de alto riesgo:

- **Microservicio Auth Server** (OAuth2 / JWT RS256): hashing de contraseñas (bcrypt), gestión de credenciales y firma asimétrica de tokens JWT.
- **Microservicio Adaptador de Pagos** (Zona PCI-DSS): aísla las integraciones con Yape, Plin y Stripe.
- **API Gateway / WAF**: terminación TLS, Rate Limiting y enrutamiento seguro.

### 4.4 Multi-Tenant / Multi-Inquilino (Modelo SaaS)

- **Aislamiento de Dominio (“Striped Entities”)**: Todas las entidades raíz de los agregados (Reserva, Habitación, Comprobante) incluyen el objeto de valor `TenantId` (UUID) dentro de su estado.
- **Persistencia Lógica Segura**: Base de Datos Compartida en PostgreSQL con políticas de **Row Level Security (RLS)**, inyectando de forma transparente el filtro `WHERE tenant_id = current_setting(...)` para impedir que un hotel acceda a datos de otro.

### 4.5 Persistencia Maestro-Esclavo (Primary-Replica)

- **PostgreSQL Primary (Maestro)**: Atiende exclusivamente operaciones de escritura transaccional (`INSERT`, `UPDATE`, `DELETE`) aplicando bloqueo pesimista `FOR UPDATE` para evitar condiciones de carrera (ej. dobles reservas del mismo cupo).
- **PostgreSQL Standby (Réplicas)**: Réplicas de solo lectura que procesan consultas masivas de reportes administrativos e indicadores sin reducir la velocidad de las transacciones en recepción.

---

## 5. Patrones de Diseño Tácticos (GoF)

Se incorporaron cuatro patrones fundamentales de la Gang of Four:

| Patrón              | Implementación              | Propósito                                                                 |
|---------------------|-----------------------------|---------------------------------------------------------------------------|
| **Facade**          | `ReservationFacade`         | Controlador de entrada de la API. Orquesta servicios internos de forma unificada. |
| **Repository**      | `IReservationRepository`    | Media entre dominio y almacenamiento relacional. Evita SQL en el modelo de negocio. |
| **Strategy**        | `ITarifaStrategy`           | Flexibiliza el cálculo de tarifas (temporada alta, promociones) sin condicionales frágiles. |
| **Adapter**         | `IPasarelaPagoAdapter`      | Normaliza la comunicación con servicios externos (Yape, Plin, Stripe).   |

---

## 6. Decisiones Arquitectónicas Principales

### 6.1 MADR-001 — Backend API REST Centralizado

**Decisión tomada:**  
Implementar un contenedor API de Aplicación (REST API en FastAPI) que centraliza toda la lógica de negocio, las reglas de validación, la autorización por roles y el registro de auditoría.

**Aislamiento de la Persistencia:**  
La API de Aplicación es el único contenedor con acceso directo (SQL/TCP) a PostgreSQL.

**Desacoplamiento de Frontends:**  
Las tres interfaces de usuario (Web pública de Reservas, Web Administrativa y App Móvil de Limpieza) junto con los trabajos programados de reportes consumen la API mediante peticiones HTTP/REST con datos en formato JSON.

**Consecuencias:**

| Positivas                                                                 | Negativas                                      |
|---------------------------------------------------------------------------|------------------------------------------------|
| Previene la duplicación de validaciones en los frontends                  | Introduce un punto único de fallo (requiere redundancia/balanceo) |
| Centraliza la seguridad                                                   | Añade un salto de red extra en las peticiones  |
| Garantiza que las trazas de auditoría no puedan ser omitidas              |                                                |

### 6.2 MADR-002 — Monolito Modular, Clean Architecture y Multi-Tenant

**Decisión tomada:**  
Estructurar el repositorio objetivo (`sumaq-hotel/`) bajo una Arquitectura Híbrida:

- **Monolito Modular Backend**: núcleo operativo en una sola unidad FastAPI, descompuesto en 6 Bounded Contexts DDD.
- **Clean Architecture**: cada módulo en 4 capas concéntricas (domain, application, infrastructure, presentation).
- **Núcleo Segregado**: zonas críticas (Auth JWT RS256 y Pasarela de Pagos) como adaptadores/microservicios aislados.
- **Aislamiento Multi-Tenant (SaaS)**: entidades con `TenantId` (UUID) + Row Level Security en PostgreSQL.

---

## 7. Estructura de Archivos

### 7.1 Árbol objetivo del repositorio (`sumaq-hotel/`)

```
sumaq-hotel/
├── apps/
│   ├── web-huespedes/                  # React SPA (Web pública para reservas de clientes)
│   ├── web-personal/                   # React SPA (Backoffice: recepción, cafetería y administración)
│   ├── movil-limpieza/                 # App Móvil (Flutter) para personal de campo
│   └── api/                            # API REST centralizada en FastAPI (Aplicación desplegable)
│       ├── app/
│       │   ├── main.py                 # Punto de entrada de la aplicación FastAPI
│       │   ├── api.py                  # Enrutador principal de endpoints
│       │   ├── config/                 # Variables de entorno y configuración general
│       │   ├── common/                 # Excepciones, middlewares de seguridad, ContextVar de Tenant
│       │   ├── infrastructure/         # Adaptadores globales (PostgreSQL, mailer, pasarelas)
│       │   └── modules/                # Los 6 Bounded Contexts del Monolito Modular
│       │       ├── reservas/
│       │       ├── estadias/
│       │       ├── operacion_habitaciones/
│       │       ├── cafeteria_inventario/
│       │       ├── cuentas_pagos/
│       │       └── identidad_acceso/
│       └── tests/                      # Pruebas de la API
├── jobs/
│   └── reportes_backups/               # Tareas programadas/batch que consumen la API (sin SQL directo)
├── database/
│   ├── migrations/                     # Scripts Alembic / SQL de migración
│   ├── seeders/                        # Datos iniciales de prueba
│   └── diagrams/                       # Modelos de datos entidad-relación
├── docs/
│   ├── arquitectura/                   # Diagramas C4 (L1-L4) y especificaciones
│   ├── requisitos/                     # Catálogo ERS, BDD y criterios MoSCoW
│   ├── decisiones/                     # Registros de decisión arquitectónica (MADR-001, MADR-002)
│   ├── api/                            # Especificación del contrato OpenAPI v3.1.0
│   ├── procesos/                       # Diagramas de secuencia UML
│   └── manuales/
├── infra/
│   ├── docker/                         # Dockerfiles y docker-compose.yml
│   └── nginx/                          # Configuración de API Gateway / Reverse Proxy
├── scripts/                            # Automatización de despliegue y mantenimiento
├── tests/
│   ├── integration/                    # Pruebas de integración entre capas
│   └── e2e/                            # Pruebas de extremo a extremo
├── .env.example
├── .gitignore
└── README.md
```

### 7.2 Estructura repetible de cada módulo de la API (Clean Architecture)

```
modulo/
├── domain/                             # CÍRCULO INTERNO: Reglas puras y conceptos del negocio
│   ├── entities/                       # Entidades de dominio (ej. Reserva, Habitacion)
│   ├── value_objects/                  # Objetos de valor (ej. TenantId, RangoFechas, Moneda)
│   ├── repositories/                   # Interfaces / Contratos de repositorios (sin SQL)
│   └── services/                       # Servicios puros de dominio
├── application/                        # CASOS DE USO: Orquestación de la lógica de aplicación
│   ├── use_cases/                      # Clases de casos de uso (ej. CrearReservaUseCase)
│   ├── dto/                            # Data Transfer Objects de entrada y salida
│   └── ports/                          # Puertos/Interfaces hacia adaptadores externos
├── infrastructure/                     # CÍRCULO EXTERNO: Implementación física e integraciones
│   ├── persistence/                    # Modelos ORM (SQLAlchemy) y tablas de PostgreSQL
│   ├── repositories/                   # Implementación concreta de repositorios SQL
│   └── adapters/                       # Conectores externos (Yape, Stripe, Auth Server)
├── presentation/                       # INTERFAZ HTTP / CONTROLADORES
│   ├── routes.py                       # Enrutadores HTTP de FastAPI (@router.post, etc.)
│   ├── schemas.py                      # Esquemas Pydantic / JSON Schema (OpenAPI v3.1)
│   └── dependencies.py                 # Inyección de dependencias de FastAPI
└── tests/                              # Pruebas unitarias del módulo
```

---

## 8. Flujo principal

```
Web o app móvil → endpoint FastAPI → caso de uso → dominio
                                      ↓
                              contrato repositorio
                                      ↓
                          adaptador PostgreSQL
```

El cliente y el job de reportes llaman a la API. El job **no consulta directamente** la base de datos, para mantener la decisión **MADR-001**.

---

## 9. Correspondencia de artefactos actuales

Los diagramas e informes actualmente ubicados en la raíz y en `output/` pueden organizarse gradualmente bajo:

- `docs/arquitectura/`
- `docs/procesos/`
- `docs/decisiones/`

Conviene conservar los originales mientras se actualicen sus enlaces.  
La carpeta `api-ejemplos/` debe seguir identificada como material ilustrativo y **no confundirse** con `apps/api/`.

---

## 10. Notas finales

- En SUMAQ, la separación debe servir al dominio hotelero y a la API central.
- No hace falta crear desde el inicio todos los módulos de un PMS genérico (spa, gimnasio, lealtad, multi-tenant avanzado, etc.): se incorporan cuando requisitos aprobados los necesiten.
- La decisión de multi-tenant tampoco aparece confirmada de forma exhaustiva en todos los requisitos recuperados; se mantiene como propuesta arquitectónica.

---

*Documento generado a partir de MADR-001 y MADR-002 — Sistema SUMAQ Hotel*
