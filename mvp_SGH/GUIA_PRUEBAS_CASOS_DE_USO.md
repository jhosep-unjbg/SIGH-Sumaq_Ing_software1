# Guía de Pruebas — Casos de Uso MVP SUMAQ

**Sistema de Gestión Hotelera SUMAQ**  
API REST Centralizada · Python / FastAPI · Monolito Modular

---

## 1. Lista de casos de uso

Los casos se agrupan en los cinco módulos de trabajo acordados. Esta organización es para pruebas y no cambia los módulos internos ni las rutas actuales de la API. La numeración se conserva para mantener las referencias de la secuencia de prueba.

| # | Módulo | Caso de uso | Método | Ruta |
|---|--------|-------------|--------|------|
| — | Clientes | Sin casos independientes implementados; las reservas reciben `huesped_id`. | — | — |
| 10 | Habitación | Crear tarea de limpieza | `POST` | `/api/v1/operacion-habitaciones/` |
| 11 | Habitación | Completar tarea | `POST` | `/api/v1/operacion-habitaciones/{id}/completar` |
| 12 | Habitación | Listar tareas | `GET` | `/api/v1/operacion-habitaciones/` |
| 2 | Reservas | Crear reserva | `POST` | `/api/v1/reservas/` |
| 3 | Reservas | Listar reservas | `GET` | `/api/v1/reservas/` |
| 4 | Reservas | Obtener reserva por ID | `GET` | `/api/v1/reservas/{id}` |
| 5 | Reservas | Conflicto de fechas (doble reserva) | `POST` | `/api/v1/reservas/` |
| 6 | Reservas | Crear estadía | `POST` | `/api/v1/estadias/` |
| 7 | Reservas | Check-in | `POST` | `/api/v1/estadias/{id}/check-in` |
| 8 | Reservas | Check-out | `POST` | `/api/v1/estadias/{id}/check-out` |
| 9 | Reservas | Listar estadías | `GET` | `/api/v1/estadias/` |
| 17 | Pagos | Crear cargo | `POST` | `/api/v1/cuentas-pagos/cargos` |
| 18 | Pagos | Registrar pago | `POST` | `/api/v1/cuentas-pagos/pagos` |
| 19 | Pagos | Consultar saldo | `GET` | `/api/v1/cuentas-pagos/saldo/{estadia_id}` |
| 20 | Pagos | Listar cargos | `GET` | `/api/v1/cuentas-pagos/cargos` |
| 1 | Administración | Health check | `GET` | `/health` |
| 13 | Administración | Crear producto | `POST` | `/api/v1/cafeteria/productos` |
| 14 | Administración | Listar productos | `GET` | `/api/v1/cafeteria/productos` |
| 15 | Administración | Registrar consumo | `POST` | `/api/v1/cafeteria/consumos` |
| 16 | Administración | Listar consumos | `GET` | `/api/v1/cafeteria/consumos` |
| 21 | Administración | Crear usuario | `POST` | `/api/v1/identidad/usuarios` |
| 22 | Administración | Login | `POST` | `/api/v1/identidad/login` |
| 23 | Administración | Login inválido | `POST` | `/api/v1/identidad/login` |
| 24 | Administración | Listar usuarios | `GET` | `/api/v1/identidad/usuarios` |

---

## 2. Compilación y arranque del programa

### 2.1 ¿Desde qué carpeta se ejecuta?

**Carpeta obligatoria:**

```text
mvp_SGH\apps\api
```

Desde PowerShell, cambia a esa carpeta dentro de tu clon:

```powershell
cd "<ruta-del-repositorio>\mvp_SGH\apps\api"
```

> No ejecutes los comandos desde `app\`, ni desde `modules\`, ni desde la raíz del repo.  
> Siempre desde **`apps\api`**.

---

### 2.2 Requisitos previos

- Python 3.10 o superior instalado
- En Windows, comprobar con:

```powershell
python --version
```

Si no funciona:

```powershell
py --version
```

---

### 2.3 Pasos de instalación y arranque (Windows PowerShell)

```powershell
# 1. Ir a la carpeta correcta
cd "<ruta-del-repositorio>\mvp_SGH\apps\api"

# 2. Crear entorno virtual (solo la primera vez)
python -m venv .venv

# 3. Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Si da error de política de ejecución:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 4. Instalar dependencias (solo la primera vez o si cambió requirements.txt)
pip install -r requirements.txt

# 5. Arrancar la API
uvicorn app.main:app --reload --port 8000
```

Mensaje esperado en consola:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### 2.4 URLs de acceso

| URL | Uso |
|-----|-----|
| http://127.0.0.1:8000/docs | Swagger (probar casos de uso) |
| http://127.0.0.1:8000/health | Comprobar que el servidor responde |
| http://127.0.0.1:8000/redoc | Documentación alternativa |

> `http://127.0.0.1:8000/` (raíz) **no tiene ruta** → devuelve 404. Es normal.

---

### 2.5 Header obligatorio

En **todas** las rutas de negocio debes enviar:

```http
X-Tenant-ID: 11111111-1111-1111-1111-111111111111
```

En Swagger (`/docs`): botón **Authorize** no aplica aquí; el header se agrega en cada request en la sección *Parameters* → `X-Tenant-ID`.

---

## 3. Cómo probar cada caso de uso

Usa **http://127.0.0.1:8000/docs** → **Try it out** → **Execute**.

Los pasos siguientes conservan el orden necesario para reutilizar los IDs entre casos. La clasificación de cada caso por módulo está en la tabla anterior.

---

### Caso 1 — Health check

- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/health`
- **Header:** no requiere
- **Resultado esperado:** `200`

```json
{"status": "ok", "service": "sumaq-api", "version": "1.0.0"}
```

---

### Caso 2 — Crear reserva

- **Método:** `POST`
- **URL:** `/api/v1/reservas/`
- **Header:** `X-Tenant-ID: 11111111-1111-1111-1111-111111111111`
- **Body:**

```json
{
  "habitacion_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "huesped_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "fecha_entrada": "2026-12-01",
  "fecha_salida": "2026-12-05",
  "precio_total": 800,
  "moneda": "PEN",
  "notas": "Primera prueba"
}
```

- **Resultado esperado:** `201 Created`
- **Guarda** el `id` de la respuesta para otros casos.

---

### Caso 3 — Listar reservas

- **Método:** `GET`
- **URL:** `/api/v1/reservas/`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200` y un arreglo con al menos la reserva creada.

---

### Caso 4 — Obtener reserva por ID

- **Método:** `GET`
- **URL:** `/api/v1/reservas/{reserva_id}`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200` con los datos de esa reserva.

---

### Caso 5 — Conflicto de fechas (doble reserva)

- Repite el **Caso 2** con la **misma** `habitacion_id` y las **mismas fechas**.
- **Resultado esperado:** `409 Conflict`

```json
{"detail": "La habitación no está disponible en el rango de fechas solicitado"}
```

---

### Caso 6 — Crear estadía

- **Método:** `POST`
- **URL:** `/api/v1/estadias/`
- **Header:** `X-Tenant-ID: ...`
- **Body:**

```json
{
  "reserva_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "habitacion_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "huesped_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "fecha_entrada": "2026-12-01",
  "fecha_salida": "2026-12-05"
}
```

- **Resultado esperado:** `201`
- **Guarda** el `id` → lo usarás en check-in, check-out, consumos y saldo.

---

### Caso 7 — Check-in

- **Método:** `POST`
- **URL:** `/api/v1/estadias/{estadia_id}/check-in`
- **Header:** `X-Tenant-ID: ...`
- **Body:** vacío
- **Resultado esperado:** `200` y `"estado": "checked_in"`

---

### Caso 8 — Check-out

- **Método:** `POST`
- **URL:** `/api/v1/estadias/{estadia_id}/check-out`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200` y `"estado": "checked_out"`

---

### Caso 9 — Listar estadías

- **Método:** `GET`
- **URL:** `/api/v1/estadias/`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200` con la lista de estadías.

---

### Caso 10 — Crear tarea de limpieza

- **Método:** `POST`
- **URL:** `/api/v1/operacion-habitaciones/`
- **Header:** `X-Tenant-ID: ...`
- **Body:**

```json
{
  "habitacion_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "notas": "Limpieza post check-out"
}
```

- **Resultado esperado:** `201` y `"estado": "pendiente"`
- **Guarda** el `id` de la tarea.

---

### Caso 11 — Completar tarea

- **Método:** `POST`
- **URL:** `/api/v1/operacion-habitaciones/{tarea_id}/completar`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200` y `"estado": "completada"`

---

### Caso 12 — Listar tareas

- **Método:** `GET`
- **URL:** `/api/v1/operacion-habitaciones/`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200`

---

### Caso 13 — Crear producto

- **Método:** `POST`
- **URL:** `/api/v1/cafeteria/productos`
- **Header:** `X-Tenant-ID: ...`
- **Body:**

```json
{
  "nombre": "Agua mineral",
  "precio": 5.0,
  "stock": 100,
  "categoria": "bebidas"
}
```

- **Resultado esperado:** `201`
- **Guarda** el `id` del producto.

---

### Caso 14 — Listar productos

- **Método:** `GET`
- **URL:** `/api/v1/cafeteria/productos`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200`

---

### Caso 15 — Registrar consumo

- **Método:** `POST`
- **URL:** `/api/v1/cafeteria/consumos`
- **Header:** `X-Tenant-ID: ...`
- **Body:** (usa el `estadia_id` y `producto_id` guardados)

```json
{
  "estadia_id": "PEGA-AQUI-EL-ID-DE-ESTADIA",
  "producto_id": "PEGA-AQUI-EL-ID-DE-PRODUCTO",
  "cantidad": 2
}
```

- **Resultado esperado:** `201` y `"total": 10.0`
- El stock del producto debe bajar de 100 a 98.

---

### Caso 16 — Listar consumos

- **Método:** `GET`
- **URL:** `/api/v1/cafeteria/consumos`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200`

---

### Caso 17 — Crear cargo

- **Método:** `POST`
- **URL:** `/api/v1/cuentas-pagos/cargos`
- **Header:** `X-Tenant-ID: ...`
- **Body:**

```json
{
  "estadia_id": "PEGA-AQUI-EL-ID-DE-ESTADIA",
  "descripcion": "Habitación 4 noches",
  "monto": 800,
  "tipo": "habitacion"
}
```

- **Resultado esperado:** `201`

---

### Caso 18 — Registrar pago

- **Método:** `POST`
- **URL:** `/api/v1/cuentas-pagos/pagos`
- **Header:** `X-Tenant-ID: ...`
- **Body:**

```json
{
  "estadia_id": "PEGA-AQUI-EL-ID-DE-ESTADIA",
  "monto": 500,
  "metodo": "yape",
  "referencia": "YAP-001"
}
```

- **Resultado esperado:** `201`

---

### Caso 19 — Consultar saldo

- **Método:** `GET`
- **URL:** `/api/v1/cuentas-pagos/saldo/{estadia_id}`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200`

```json
{
  "estadia_id": "...",
  "total_cargos": 800.0,
  "total_pagos": 500.0,
  "saldo": 300.0
}
```

---

### Caso 20 — Listar cargos

- **Método:** `GET`
- **URL:** `/api/v1/cuentas-pagos/cargos`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200`

---

### Caso 21 — Crear usuario

- **Método:** `POST`
- **URL:** `/api/v1/identidad/usuarios`
- **Header:** `X-Tenant-ID: ...`
- **Body:**

```json
{
  "email": "recepcion@sumaq.com",
  "nombre": "Ana Recepción",
  "rol": "recepcion",
  "password": "secreto123"
}
```

- **Resultado esperado:** `201`

---

### Caso 22 — Login correcto

- **Método:** `POST`
- **URL:** `/api/v1/identidad/login`
- **Header:** `X-Tenant-ID: ...`
- **Body:**

```json
{
  "email": "recepcion@sumaq.com",
  "password": "secreto123"
}
```

- **Resultado esperado:** `200` con `access_token`

---

### Caso 23 — Login inválido

- Mismo endpoint que el Caso 22, pero con password incorrecta:

```json
{
  "email": "recepcion@sumaq.com",
  "password": "mala"
}
```

- **Resultado esperado:** `401 Unauthorized`

---

### Caso 24 — Listar usuarios

- **Método:** `GET`
- **URL:** `/api/v1/identidad/usuarios`
- **Header:** `X-Tenant-ID: ...`
- **Resultado esperado:** `200`

---

## 4. Orden recomendado de prueba

Para no perder IDs, sigue este flujo:

1. Health  
2. Crear reserva → Conflicto de fechas → Listar reservas  
3. Crear estadía → Check-in → Check-out  
4. Crear tarea → Completar tarea  
5. Crear producto → Registrar consumo → Listar productos  
6. Crear cargo → Registrar pago → Consultar saldo  
7. Crear usuario → Login OK → Login inválido → Listar usuarios  

---

## 5. Notas importantes

| Tema | Detalle |
|------|---------|
| Persistencia | Datos en **memoria**. Al reiniciar la API se borran. |
| Multi-tenant | Siempre envía el mismo `X-Tenant-ID` en una sesión de prueba. |
| IDs | Copia los `id` de las respuestas (estadía, producto, tarea) para los siguientes casos. |
| Carpeta de ejecución | Siempre `apps\api` |
| Raíz `/` | No está definida → 404 es correcto |

---

## 6. Comandos rápidos (copiar y pegar)

```powershell
cd "<ruta-del-repositorio>\mvp_SGH\apps\api"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Luego abrir: **http://127.0.0.1:8000/docs**

## 7. Estructura para futuras pruebas unitarias

Las carpetas y criterios de organización están en [`apps/api/tests/unit/README.md`](apps/api/tests/unit/README.md). La guía actual contiene pruebas manuales de API; todavía no hay pruebas unitarias implementadas.

---

*Documento de pruebas del MVP SUMAQ — Monolito Modular + Clean Architecture*
