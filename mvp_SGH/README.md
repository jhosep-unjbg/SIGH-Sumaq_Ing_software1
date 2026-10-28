# SUMAQ Hotel — Sistema de Gestión Hotelera

**API REST Centralizada · Arquitectura Híbrida SaaS Multi-Tenant**

---

## Descripción

**SUMAQ** es un Sistema de Gestión Hotelera (PMS) diseñado bajo una arquitectura moderna, segura y escalable. El núcleo del sistema es una **API REST Centralizada** desarrollada en **Python / FastAPI**, que concentra toda la lógica de negocio, validaciones, autorización y acceso a datos.

El sistema atiende tres interfaces de usuario independientes:

| Interfaz                        | Tecnología          | Usuarios                              |
|---------------------------------|---------------------|---------------------------------------|
| Web Pública de Reservas         | React (TypeScript)  | Huéspedes / Clientes finales          |
| Web Administrativa (Backoffice) | React (TypeScript)  | Recepcionistas, administradores, cafetería |
| App Móvil de Campo              | Flutter (Dart)      | Personal de limpieza y mantenimiento  |

---

## Decisiones Arquitectónicas Principales

### MADR-001 — API REST Centralizada
Se implementa una única API REST (FastAPI) como **único componente con acceso directo a PostgreSQL**.  
Todos los frontends y trabajos programados consumen la API mediante HTTPS + JSON.

**Ventajas:**
- Centralización de reglas de negocio y seguridad (RBAC)
- Trazabilidad e inmutabilidad de auditoría
- Desacoplamiento total de los frontends

**Trade-off:**
- Punto único de fallo → se mitiga con réplicas y balanceo de carga

### MADR-002 — Monolito Modular + Clean Architecture + Multi-Tenant
El backend se organiza como un **Monolito Modular** con 6 Bounded Contexts (DDD), aplicando Clean Architecture en cada módulo y soporte Multi-Tenant (SaaS).

---

## Arquitectura Híbrida

La API combina cinco estilos arquitectónicos complementarios:

```text
1. Monolito Modular     → 6 Bounded Contexts DDD en un solo despliegue FastAPI
2. Clean Architecture   → 4 capas concéntricas (Domain → Application → Infrastructure → Presentation)
3. Segregated Core      → Microservicios aislados para Auth (JWT RS256) y Pagos (PCI-DSS)
4. Multi-Tenant (SaaS)  → TenantId (UUID) + Row Level Security en PostgreSQL
5. Primary-Replica      → Escritura en Maestro (FOR UPDATE) + Réplicas de solo lectura
```

### Bounded Contexts (Módulos)

| Módulo                    | Responsabilidad principal                                      |
|---------------------------|----------------------------------------------------------------|
| `reservas`                | Disponibilidad, creación, modificación y anulación de reservas |
| `estadias`                | Huéspedes, check-in, cargos al folio y check-out               |
| `operacion_habitaciones`  | Limpieza, objetos olvidados, bloqueos y mantenimiento          |
| `cafeteria_inventario`    | Consumos, productos, existencias y caducidad                   |
| `cuentas_pagos`           | Liquidación, descuentos, pagos, comprobantes y saldos          |
| `identidad_acceso`        | Autenticación, usuarios, roles (RBAC) y contexto de tenant     |

---

## Estructura del Repositorio

```text
sumaq-hotel/
├── apps/
│   ├── web-huespedes/                  # React SPA – Clientes
│   ├── web-personal/                   # React SPA – Backoffice
│   ├── movil-limpieza/                 # Flutter – Personal de campo
│   └── api/                            # API REST Centralizada (FastAPI)
│       ├── app/
│       │   ├── main.py
│       │   ├── api.py
│       │   ├── config/
│       │   ├── common/
│       │   ├── infrastructure/
│       │   └── modules/                # 6 Bounded Contexts
│       │       ├── reservas/
│       │       ├── estadias/
│       │       ├── operacion_habitaciones/
│       │       ├── cafeteria_inventario/
│       │       ├── cuentas_pagos/
│       │       └── identidad_acceso/
│       └── tests/
├── jobs/                               # Tareas programadas (consumen la API)
├── database/                           # Migraciones, seeders y diagramas
├── docs/                               # Arquitectura, decisiones (MADR), OpenAPI
├── infra/                              # Docker + Nginx
└── README.md
```

### Estructura interna de cada módulo (Clean Architecture)

```text
modulo/
├── domain/                 # Reglas puras de negocio (entidades, value objects, repositorios abstractos)
├── application/            # Casos de uso, DTOs y puertos
├── infrastructure/         # Implementaciones concretas (SQL, adaptadores externos)
├── presentation/           # Rutas FastAPI, schemas Pydantic, dependencias
└── tests/
```

---

## Patrones de Diseño Aplicados (GoF)

| Patrón          | Uso en SUMAQ                                      | Beneficio principal                     |
|-----------------|---------------------------------------------------|-----------------------------------------|
| **Facade**      | `ReservationFacade`                               | Reduce acoplamiento en controladores    |
| **Repository**  | `IReservationRepository`                          | Aísla el dominio del SQL                |
| **Strategy**    | `ITarifaStrategy`                                 | Cálculo flexible de tarifas             |
| **Adapter**     | `IPasarelaPagoAdapter` (Yape, Plin, Stripe)       | Normaliza pasarelas de pago externas    |

---

## Stack Tecnológico Recomendado

| Capa              | Tecnología                     |
|-------------------|--------------------------------|
| Backend API       | **Python 3.11+ / FastAPI**     |
| Frontend Web      | **TypeScript + React**         |
| App Móvil         | **Dart + Flutter**             |
| Base de Datos     | **PostgreSQL** (Primary + Replica) |
| Autenticación     | OAuth2 + JWT RS256             |
| Contenedores      | Docker + Docker Compose        |
| Proxy / Gateway   | Nginx                          |

---

## Flujo Principal

```text
Frontend / App Móvil / Job
          │
          ▼
   API Gateway / WAF
          │
          ▼
   FastAPI (Monolito Modular)
          │
          ├─→ Caso de Uso
          │         │
          │         ▼
          │    Dominio (Reglas de negocio)
          │         │
          │         ▼
          │    Repositorio (interfaz)
          │         │
          ▼         ▼
   Adaptador PostgreSQL (Primary / Replica)
```

---

## Calidad Interna (Métricas CK)

La arquitectura y los patrones aplicados mejoran significativamente las métricas de calidad:

- **CBO** (Coupling Between Objects): reducido de 7 → 2
- **WMC** (Weighted Methods per Class): reducido de 18 → 4
- **LCOM** (Lack of Cohesion): 0 % (máxima cohesión)

---

## Documentación Relacionada

- `docs/decisiones/MADR-001` — API REST Centralizada
- `docs/decisiones/MADR-002` — Estructura de repositorio y Clean Architecture
- `docs/arquitectura/` — Diagramas C4 y especificación formal
- `docs/api/` — Contrato OpenAPI v3.1.0

---

## Estado Actual

> Este repositorio contiene la **especificación arquitectónica**, diagramas y un esqueleto de código de la API.  
> Las aplicaciones web, la app móvil, la API productiva y la base de datos aún se encuentran en fase de implementación.

---

## Licencia

Proyecto privado — Sistema SUMAQ Hotel  
Todos los derechos reservados.
