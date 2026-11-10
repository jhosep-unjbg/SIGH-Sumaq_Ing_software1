# Estructura de pruebas unitarias

Las futuras pruebas unitarias se organizarán por los cinco módulos acordados. Crea los archivos de prueba con el patrón `test_*.py` en la carpeta correspondiente y enfócalos en reglas de dominio y casos de uso, aislando sus dependencias externas.

| Módulo de pruebas | Casos actuales relacionados | Módulos de API existentes |
|-------------------|-----------------------------|---------------------------|
| `clientes` | No hay casos independientes; `huesped_id` se recibe en reservas. | Pendiente de implementar un módulo de clientes/huéspedes. |
| `habitacion` | 10–12: tareas de limpieza. | `operacion_habitaciones` |
| `reservas` | 2–9: reservas y ciclo de estadía. | `reservas`, `estadias` |
| `pagos` | 17–20: cargos, pagos y saldo. | `cuentas_pagos` |
| `administracion` | 1, 13–16, 21–24: salud, cafetería/inventario e identidad. | `cafeteria_inventario`, `identidad_acceso` |

La estructura inicial es:

```text
tests/
└── unit/
    ├── clientes/
    ├── habitacion/
    ├── reservas/
    ├── pagos/
    └── administracion/
```

Los casos de uso del inventario de la [guía manual](../../../../GUIA_PRUEBAS_CASOS_DE_USO.md) sirven como referencia funcional, pero no son pruebas unitarias. Para ejecutar las futuras pruebas con la biblioteca estándar de Python, desde `apps/api`:

```powershell
python -m unittest discover -s tests/unit -p "test_*.py"
```
