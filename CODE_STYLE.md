# Estilo de código de SUMAQ

## Propósito

Este documento define las convenciones básicas de código para el MVP de la API REST del Sistema de Gestión Hotelera SUMAQ.

## Lenguaje y formato

- El backend está desarrollado en Python.
- Usar cuatro espacios para la indentación.
- Mantener líneas legibles y evitar instrucciones demasiado extensas.
- Separar clases y funciones con líneas en blanco.
- Ordenar los imports en este orden:
  1. Librería estándar de Python.
  2. Librerías externas.
  3. Módulos internos de la aplicación.
- Eliminar imports que no se utilicen.

## Nombres

- Usar `PascalCase` para nombres de clases, por ejemplo `CrearReservaUseCase`.
- Usar `snake_case` para funciones, variables y archivos, por ejemplo `crear_reserva.py`.
- Usar nombres descriptivos que expresen la intención.
- Usar mayúsculas y guiones bajos para constantes, por ejemplo `MENSAJE_ERROR`.

## Funciones y clases

- Cada función debe tener una responsabilidad clara.
- Mantener las funciones enfocadas y fáciles de leer.
- Agregar anotaciones de tipos cuando ayuden a entender entradas y resultados.
- Usar docstrings para explicar el propósito de módulos, clases y funciones públicas.
- Evitar duplicar reglas de negocio.

## Organización por capas

Los módulos de la API se organizan en las siguientes capas:

- `domain/`: entidades y reglas de negocio.
- `application/`: casos de uso y coordinación de operaciones.
- `infrastructure/`: repositorios y adaptadores concretos.
- `presentation/`: rutas HTTP, esquemas y dependencias.
- `tests/`: pruebas del módulo.

Las reglas de negocio pertenecen al dominio. Las rutas HTTP deben recibir y devolver datos y delegar las operaciones a los casos de uso.

## Errores

- Validar las reglas de negocio en la capa correspondiente.
- Manejar errores esperados con excepciones claras.
- Evitar ocultar errores con bloques `except` demasiado amplios.
- No incluir contraseñas, tokens u otros datos sensibles en mensajes o registros.

## Cambios

- Mantener el estilo existente cuando se modifique un archivo.
- Revisar los cambios antes de crear un commit.
- Ejecutar las comprobaciones disponibles y documentar sus resultados reales.