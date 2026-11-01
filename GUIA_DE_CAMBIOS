# Guía para entregar cambios en SUMAQ

## 1. Objetivo

Esta guía explica cómo documentar, implementar, verificar y entregar cambios al MVP de la API REST del Sistema de Gestión Hotelera SUMAQ mediante Git y un Pull Request (PR).

## 2. Archivos de documentación

En la raíz del repositorio deben estar estos archivos:

- `README.md`: descripción, instalación, ejecución y pruebas del proyecto.
- `CODE_STYLE.md`: convenciones para escribir y organizar código.
- `CONTRIBUTING.md`: flujo para crear ramas, commits y PR.
- `LICENSE`: condiciones de uso acordadas por el equipo y el docente.

Antes de reemplazar el `README.md` existente, revisa su contenido y conserva la información que todavía corresponda al proyecto.

## 3. Confirmar la ubicación y el estado del repositorio

Abre Git Bash y entra en la carpeta raíz:

```bash
cd "/c/Rodrigo/software1_proyecto/SIGH-Sumaq_Ing_software1"
```

Confirma que Git reconoce el repositorio y revisa la rama actual:

```bash
git status
git branch --show-current
```

Antes de cambiar de rama, confirma que tus cambios estén guardados en un commit. No uses `git restore` ni `git reset` para descartar cambios sin revisar qué contienen.

## 4. Definir la historia o tarea

Antes de programar, confirma con el equipo qué funcionalidad vas a implementar.

Si el repositorio usa Issues:

1. Crea un Issue en GitHub.
2. Incluye el código y el nombre de la historia.
3. Describe el actor, la necesidad y el beneficio.
4. Agrega criterios de aceptación que se puedan comprobar.
5. Enlaza el caso de uso y el módulo correspondiente.

No agregues reglas que no estén en los requisitos o en el comportamiento acordado.

## 5. Crear una rama de trabajo

Confirma con el equipo si la rama base es `main` o `develop`.

Para crear una rama desde `main`:

```bash
git switch main
git pull origin main
git switch -c feature/HU-HOT-01-crear-reserva
```

Para crearla desde `develop`:

```bash
git switch develop
git pull origin develop
git switch -c feature/HU-HOT-01-crear-reserva
```

Verifica la rama actual:

```bash
git branch --show-current
```

Usa nombres claros, por ejemplo:

- `feature/HU-HOT-01-crear-reserva`
- `fix/validar-fechas-reserva`
- `docs/actualizar-readme`

### Si Git no permite cambiar de rama

Revisa primero el estado:

```bash
git status
```

Si tienes cambios sin guardar, consérvalos en un commit antes de cambiar de rama. Pide orientación al equipo si no sabes cómo hacerlo.

## 6. Implementar el cambio

El código de la API está en:

```text
mvp_SGH/apps/api/app/modules/
```

Módulos disponibles:

```text
reservas/
estadias/
operacion_habitaciones/
cafeteria_inventario/
cuentas_pagos/
identidad_acceso/
```

Conserva la separación por capas:

- `domain/`: entidades y reglas de negocio.
- `application/`: casos de uso.
- `infrastructure/`: repositorios y adaptadores.
- `presentation/`: rutas HTTP, esquemas y dependencias.
- `tests/`: pruebas del módulo.

Implementa el alcance de la historia asignada y actualiza la documentación si cambia el comportamiento.

## 7. Ejecutar comprobaciones

En Git Bash, entra en la carpeta de la API:

```bash
cd "/c/Rodrigo/software1_proyecto/SIGH-Sumaq_Ing_software1/mvp_SGH/apps/api"
```

Comprueba la sintaxis con el Python del entorno virtual:

```bash
./.venv/Scripts/python.exe -m compileall app
```

Si termina sin errores, inicia la API:

```bash
./.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

Mantén abierta la terminal. En el navegador visita:

- Estado de la API: `http://127.0.0.1:8000/health`
- Documentación interactiva: `http://127.0.0.1:8000/docs`

### Probar un endpoint

1. Busca el módulo y el endpoint que modificaste.
2. Pulsa **Try it out**.
3. Completa los datos requeridos.
4. Si solicita `X-Tenant-ID`, utiliza el UUID de prueba indicado en la guía.
5. Pulsa **Execute**.
6. Registra el código HTTP y la respuesta que recibiste.
7. Prueba también los criterios de error de la historia.

Consulta los ejemplos de:

```text
mvp_SGH/GUIA_PRUEBAS_CASOS_DE_USO.md
```

## 8. Registrar los resultados de prueba

Usa esta tabla para documentar cada prueba:

| Campo | Resultado |
|---|---|
| Caso probado | [Nombre del caso] |
| Endpoint | [Método y ruta] |
| Datos enviados | [Resumen o referencia] |
| Código HTTP | [Código recibido] |
| Resultado observado | [Respuesta real] |
| Estado | Aprobado / Fallido |
| Evidencia | [Ruta de captura, si corresponde] |

Marca como aprobadas únicamente las pruebas que ejecutaste. La compilación sintáctica no sustituye las pruebas funcionales.

## 9. Revisar y guardar los cambios

Vuelve a la raíz del repositorio:

```bash
cd "/c/Rodrigo/software1_proyecto/SIGH-Sumaq_Ing_software1"
```

Revisa los archivos modificados:

```bash
git status
git diff
```

Agrega únicamente los archivos relacionados con la tarea. Por ejemplo:

```bash
git add CODE_STYLE.md CONTRIBUTING.md LICENSE README.md
git add mvp_SGH/apps/api/app/modules/
git add mvp_SGH/docs/
```

Crea un commit descriptivo:

```bash
git commit -m "Refactoriza caso de uso de reservas"
```

Publica la rama:

```bash
git push -u origin feature/HU-HOT-01-crear-reserva
```

Si la rama ya está publicada, actualízala con:

```bash
git push
```

## 10. Abrir el Pull Request

En GitHub:

1. Abre el repositorio.
2. Selecciona **Compare & pull request**.
3. Comprueba la rama de origen y la rama de destino.
4. Enlaza el Issue de la historia de usuario.
5. Resume el cambio y los módulos modificados.
6. Indica las comprobaciones ejecutadas y sus resultados.
7. Adjunta o enlaza las evidencias.
8. Solicita revisión al equipo o al docente.

Confirma que la rama de trabajo parte de la rama base acordada. En el repositorio SUMAQ, `develop` se creó inicialmente desde `jhosep`; si el equipo exige que se origine desde `main`, consulta cómo corregir su base antes de integrar cambios.

## 11. Resolver comentarios e integrar

1. Lee los comentarios del Pull Request.
2. Realiza las correcciones solicitadas en la misma rama.
3. Vuelve a ejecutar las comprobaciones afectadas.
4. Publica los commits actualizados.
5. Espera la aprobación requerida.
6. Integra el PR según la política del equipo.
7. Enlaza el PR integrado y las evidencias en la documentación final.

## 12. Limitaciones conocidas del MVP

- Algunos repositorios usan almacenamiento en memoria; los datos pueden perderse al reiniciar la API.
- `compileall` comprueba sintaxis, pero no confirma que las funciones respondan correctamente.
- Las contraseñas y los tokens del módulo de identidad son simulados en este MVP; no son mecanismos seguros para producción.
- No afirmes que PostgreSQL, RLS, réplicas o interfaces web y móviles están implementadas sin verificarlo en el código.

## 13. Lista final de entrega

- [ ] `README.md` explica instalación, ejecución y pruebas comprobadas.
- [ ] `CODE_STYLE.md` está en la raíz.
- [ ] `CONTRIBUTING.md` está en la raíz.
- [ ] `LICENSE` está en la raíz y su contenido fue acordado.
- [ ] La historia de usuario y sus criterios están documentados.
- [ ] La rama se creó desde la base acordada.
- [ ] Los commits tienen mensajes descriptivos.
- [ ] Se ejecutó `compileall`.
- [ ] Se probaron los endpoints relacionados con el cambio.
- [ ] Los resultados reales y las evidencias están registrados.
- [ ] El Pull Request enlaza la historia y describe las pruebas.
- [ ] Se resolvieron los comentarios de revisión.
- [ ] El cambio se integró según la política del equipo.