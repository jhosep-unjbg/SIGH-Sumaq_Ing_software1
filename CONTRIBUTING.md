# Guía para contribuir a SUMAQ

## Propósito

Esta guía describe el flujo de trabajo para proponer cambios al Sistema de Gestión Hotelera SUMAQ.

## Antes de empezar

1. Confirma con el equipo qué historia de usuario o tarea vas a implementar.
2. Revisa los casos de uso y criterios de aceptación relacionados.
3. Comprueba que tienes acceso al repositorio remoto.

## Ramas

- `main` contiene la versión principal del proyecto.
- `develop` se utiliza para integrar cambios del equipo, si esa es la política acordada.
- Crea una rama de trabajo desde la rama base acordada para cada tarea.
- Usa nombres descriptivos, por ejemplo:
  - `feature/HU-HOT-01-crear-reserva`
  - `fix/validacion-fechas-reserva`
  - `docs/actualizar-readme`

Ejemplo:

```bash
git switch main
git pull
git switch -c feature/HU-HOT-01-crear-reserva