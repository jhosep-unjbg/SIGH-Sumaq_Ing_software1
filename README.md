# Sistema de Gestión Hotelera "SUMAQ" (SGH)

[![PHP](https://img.shields.io/badge/PHP-8.2-777BB4?logo=php)](https://www.php.net/)
[![CodeIgniter](https://img.shields.io/badge/CodeIgniter-4.x-EF4223?logo=codeigniter)](https://codeigniter.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vuedotjs)](https://vuejs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)](https://www.mysql.com/)

## Descripción del proyecto

El sistema de gestión hotelera **Hotel Sumaq** es una aplicación web desarrollada como prototipo funcional para administrar las operaciones principales de un hotel. El sistema permite gestionar clientes, habitaciones, reservas, pagos, empleados, reportes y parámetros generales del hotel.

El proyecto fue desarrollado con **PHP, MySQL/MariaDB, HTML, CSS y JavaScript**, utilizando **XAMPP** como entorno local de ejecución.

El sistema está orientado principalmente al uso interno del hotel, permitiendo el acceso de usuarios con diferentes roles, como administrador y recepcionista.

---

**Equipo de Desarrollo & Roles**

| Integrante | Rol en el Proyecto | Módulo a Cargo |
| :--- | :--- | :--- |
| **Jhosep Rodrigo Arocutipa Mamani** | Líder Técnico / Backend Dev | Arquitectura Base, Autenticación y Módulo de Reservas |
| **Hugo Antonio Ordoño Quispe** | Scrum Master / Analista Funcional | Módulo de Huéspedes y Estadía (Check-in / Check-out) |
| **Ronald Alexander Huaman Huanca** | Product Owner / Frontend Dev | Módulo de Habitaciones, Tarifas e Interfaz Vue.js |
| **Marco Antonio Mamani Murillo** | QA / DBA / Developer | Módulo de Pagos, Reportes, Base de Datos y Pruebas |



## Objetivo general

Desarrollar un software de gestión hotelera que permita centralizar las operaciones principales del hotel, facilitando el trabajo administrativo y operativo del personal.

---

## Objetivos específicos

* Gestionar el registro, actualización y consulta de clientes.
* Administrar habitaciones, tipos, precios, capacidad y estados.
* Registrar reservas asociadas a clientes, habitaciones y fechas.
* Controlar el proceso de check-in y finalización de reservas.
* Registrar pagos, descuentos, boletas y reembolsos.
* Generar reportes generales del sistema.
* Gestionar empleados del hotel.
* Configurar parámetros generales como moneda, impuesto, horarios y política de cancelación.
* Aplicar control de acceso mediante roles de usuario.

---

## Módulos implementados

* Login con sesiones.
* Control de acceso por roles.
* Dashboard general.
* Gestión de clientes.
* Gestión de habitaciones.
* Gestión de reservas.
* Check-in y finalización de reservas.
* Gestión de pagos.
* Confirmación de pagos pendientes.
* Generación de boletas.
* Registro de reembolsos.
* Reportes generales.
* Gestión de empleados.
* Configuración del hotel.

---

## Roles del sistema

### Administrador

El administrador tiene acceso completo al sistema. Puede gestionar clientes, habitaciones, reservas, pagos, reportes, empleados y configuración general del hotel.

### Recepcionista

El recepcionista puede acceder a los módulos operativos del hotel, como clientes, habitaciones, reservas, pagos y reportes. No tiene acceso a la gestión de empleados ni a la configuración general del sistema.

---

## Tecnologías utilizadas

* PHP
* MySQL / MariaDB
* HTML5
* CSS3
* JavaScript
* XAMPP
* Git
* Visual Studio Code

---

## Estructura del proyecto

```text
hotel_sumaq/
│
├── app/
│   ├── config/
│   │   └── database.php
│   │
│   ├── controllers/
│   │   ├── AuthController.php
│   │   ├── ClienteController.php
│   │   ├── HabitacionController.php
│   │   ├── ReservaController.php
│   │   ├── PagoController.php
│   │   ├── EmpleadoController.php
│   │   └── ConfiguracionController.php
│   │
│   ├── models/
│   │
│   └── views/
│       └── includes/
│           ├── header.php
│           ├── sidebar.php
│           └── footer.php
│
├── public/
│   ├── css/
│   │   └── estilos.css
│   │
│   ├── js/
│   │   └── app.js
│   │
│   └── img/
│
├── database/
│   └── hotel_sumaq.sql
│
├── docs/
│   ├── auditoria.md
│   └── pruebas.md
│
├── index.php
├── dashboard.php
├── clientes.php
├── habitaciones.php
├── reservas.php
├── pagos.php
├── reportes.php
├── empleados.php
├── configuracion.php
├── logout.php
├── README.md
└── .gitignore
```

---

## Descripción de carpetas principales

### `app/config`

Contiene la configuración de conexión a la base de datos.

### `app/controllers`

Contiene los archivos encargados de procesar las acciones del sistema, como registrar, actualizar, cambiar estados o validar formularios.

### `app/views/includes`

Contiene archivos reutilizables de la interfaz, como el encabezado, el menú lateral y el pie de página.

### `public/css`

Contiene los estilos visuales del sistema.

### `public/js`

Contiene funciones JavaScript generales del sistema.

### `public/img`

Carpeta destinada para imágenes, logos o recursos visuales del sistema.

### `database`

Contiene el script SQL de la base de datos.

### `docs`

Contiene documentación relacionada con auditoría y pruebas funcionales.

---

## Instalación local

### 1. Copiar el proyecto en XAMPP

Copiar la carpeta del proyecto dentro de:

```text
C:\xampp\htdocs\
```

La ruta final debería quedar de la siguiente manera:

```text
C:\xampp\htdocs\hotel_sumaq\
```

---

### 2. Iniciar XAMPP

Abrir el panel de control de XAMPP e iniciar los servicios:

```text
Apache
MySQL
```

Ambos servicios deben aparecer en estado activo.

---

### 3. Entrar a phpMyAdmin

Abrir el navegador e ingresar a:

```text
http://localhost/phpmyadmin
```

---

### 4. Crear la base de datos

Desde phpMyAdmin, importar o ejecutar el archivo SQL ubicado en:

```text
database/hotel_sumaq.sql
```

Este archivo contiene la estructura principal de la base de datos del sistema.

---

### 5. Configurar la conexión con la base de datos

La conexión se configura en el archivo:

```text
app/config/database.php
```

Dentro de este archivo se deben revisar los siguientes datos:

```php
$host = "127.0.0.1";
$port = "3307";
$dbname = "hotel_sumaq";
$user = "root";
$password = "";
```

El valor de `$port` debe modificarse según el puerto que esté usando MySQL/MariaDB en XAMPP.

Si MySQL usa el puerto normal de XAMPP:

```php
$port = "3306";
```

Si MySQL fue configurado para usar otro puerto, como en este proyecto:

```php
$port = "3307";
```

Para saber qué puerto está usando MySQL, se debe revisar el panel de control de XAMPP, en la fila de MySQL, donde aparece la información de puertos.

---

### 6. Verificar la conexión

Opcionalmente, durante la instalación se puede crear temporalmente un archivo llamado:

```text
test_conexion.php
```

con el siguiente contenido:

```php
<?php

require_once "app/config/database.php";

echo "Conexión correcta con la base de datos hotel_sumaq";

?>
```

Luego se debe ingresar desde el navegador a:

```text
http://localhost/hotel_sumaq/test_conexion.php
```

Si aparece el mensaje de conexión correcta, la configuración está funcionando.

Después de realizar la prueba, se recomienda eliminar el archivo `test_conexion.php`, ya que solo se usa para verificar la conexión durante la instalación.

---

### 7. Creación de usuarios iniciales

Por seguridad, el sistema no incluye contraseñas fijas en el código fuente ni en el archivo SQL principal. Después de importar la base de datos, se debe crear al menos un usuario inicial para poder acceder al sistema.

Las cuentas de acceso se almacenan en la tabla `usuarios`, mientras que los roles disponibles se almacenan en la tabla `roles`.

La contraseña no se guarda en texto plano. Antes de almacenarse, se cifra mediante la función `password_hash()` de PHP. Luego, durante el inicio de sesión, el sistema valida la contraseña mediante `password_verify()`.

Para crear usuarios iniciales durante la instalación local, se puede crear temporalmente un archivo llamado:

```text
crear_usuarios.php
```

Este archivo debe ubicarse en la raíz del proyecto:

```text
hotel_sumaq/crear_usuarios.php
```

Contenido sugerido del archivo temporal:

```php
<?php

require_once "app/config/database.php";

$mensaje = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $nombre = trim($_POST["nombre"] ?? "");
    $usuario = trim($_POST["usuario"] ?? "");
    $clave = $_POST["clave"] ?? "";
    $rolNombre = $_POST["rol"] ?? "";

    if ($nombre === "" || $usuario === "" || $clave === "" || $rolNombre === "") {
        $mensaje = "Todos los campos son obligatorios.";
    } else {
        try {
            $stmtRol = $pdo->prepare("SELECT id_rol FROM roles WHERE nombre = :rol");
            $stmtRol->execute([":rol" => $rolNombre]);
            $rol = $stmtRol->fetch(PDO::FETCH_ASSOC);

            if (!$rol) {
                $mensaje = "El rol seleccionado no existe.";
            } else {
                $stmtExiste = $pdo->prepare("SELECT COUNT(*) FROM usuarios WHERE usuario = :usuario");
                $stmtExiste->execute([":usuario" => $usuario]);
                $existe = $stmtExiste->fetchColumn();

                if ($existe > 0) {
                    $mensaje = "El nombre de usuario ya existe.";
                } else {
                    $claveCifrada = password_hash($clave, PASSWORD_DEFAULT);

                    $stmt = $pdo->prepare("
                        INSERT INTO usuarios(nombre, usuario, clave, id_rol, estado)
                        VALUES (:nombre, :usuario, :clave, :id_rol, 'Activo')
                    ");

                    $stmt->execute([
                        ":nombre" => $nombre,
                        ":usuario" => $usuario,
                        ":clave" => $claveCifrada,
                        ":id_rol" => $rol["id_rol"]
                    ]);

                    $mensaje = "Usuario creado correctamente.";
                }
            }
        } catch (PDOException $e) {
            $mensaje = "Error al crear el usuario.";
        }
    }
}

?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Crear usuario inicial</title>
</head>
<body>

    <h2>Crear usuario inicial</h2>

    <?php if ($mensaje !== ""): ?>
        <p><?php echo htmlspecialchars($mensaje); ?></p>
    <?php endif; ?>

    <form method="POST">
        <label>Nombre completo:</label><br>
        <input type="text" name="nombre" required><br><br>

        <label>Usuario:</label><br>
        <input type="text" name="usuario" required><br><br>

        <label>Contraseña:</label><br>
        <input type="password" name="clave" required><br><br>

        <label>Rol:</label><br>
        <select name="rol" required>
            <option value="Administrador">Administrador</option>
            <option value="Recepcionista">Recepcionista</option>
        </select><br><br>

        <button type="submit">Crear usuario</button>
    </form>

</body>
</html>
```

Luego se debe ejecutar desde el navegador:

```text
http://localhost/hotel_sumaq/crear_usuarios.php
```

Desde ese formulario se puede crear un usuario administrador o recepcionista, definiendo el nombre, usuario y contraseña que correspondan.

Después de crear los usuarios necesarios, el archivo `crear_usuarios.php` debe eliminarse del proyecto por seguridad.

También se recomienda agregar este archivo al `.gitignore` para evitar subirlo al repositorio:

```gitignore
crear_usuarios.php
test_conexion.php
```

---

### 8. Abrir el sistema

Ingresar desde el navegador a:

```text
http://localhost/hotel_sumaq/
```

Luego iniciar sesión con el usuario y contraseña creados previamente.

---

## Flujo principal del sistema

El flujo principal del sistema es el siguiente:

```text
Login
↓
Dashboard
↓
Gestión de clientes
↓
Gestión de habitaciones
↓
Registro de reserva
↓
Check-in
↓
Registro de pago
↓
Generación de boleta
↓
Finalización de reserva
↓
Reportes
```

---

## Funcionalidades principales

### Login

Permite iniciar sesión mediante usuario y contraseña. El sistema valida las credenciales y crea una sesión para el usuario autenticado.

### Dashboard

Muestra un resumen general de clientes, habitaciones, reservas e ingresos.

### Clientes

Permite registrar, editar, buscar, desactivar y reactivar clientes.

### Habitaciones

Permite registrar habitaciones, modificar datos, cambiar estados y enviar habitaciones a mantenimiento.

### Reservas

Permite crear reservas asociando cliente, habitación, fecha de ingreso, fecha de salida y cantidad de personas. También permite realizar check-in, cancelar reservas y finalizar estadías.

### Pagos

Permite registrar pagos asociados a reservas, aplicar descuentos, seleccionar método de pago, marcar pagos pendientes como pagados, generar boletas y registrar reembolsos.

### Reportes

Muestra indicadores generales del sistema, como clientes registrados, habitaciones disponibles, reservas activas, pagos, ingresos y mantenimientos recientes.

### Empleados

Permite al administrador registrar, editar, buscar, desactivar y reactivar empleados.

### Configuración

Permite modificar parámetros generales del hotel, como nombre, moneda, impuesto, horario de check-in, horario de check-out y política de cancelación.

---

## Seguridad básica aplicada

El sistema implementa medidas básicas de seguridad:

* Validación de sesión en los módulos internos.
* Control de acceso según rol de usuario.
* Restricción de módulos administrativos para usuarios no autorizados.
* Uso de contraseñas cifradas con `password_hash()`.
* Validación de credenciales con `password_verify()`.
* Uso de PDO para la conexión con MySQL.
* Uso de consultas preparadas para reducir riesgos de inyección SQL.
* Uso de `htmlspecialchars()` para mostrar datos en la interfaz de forma segura.

---

## Base de datos

La base de datos principal se llama:

```text
hotel_sumaq
```

Tablas principales:

```text
roles
usuarios
clientes
habitaciones
reservas
pagos
boletas
mantenimientos
reembolsos
empleados
parametros_hotel
```

El archivo SQL se encuentra en:

```text
database/hotel_sumaq.sql
```

---

## Control de versiones

El proyecto utiliza Git para registrar los avances del desarrollo.

Ejemplos de commits realizados:

```text
Estructura inicial del sistema hotelero
Crear base de datos y conexión inicial
Implementar login con sesiones y roles
Implementar módulo de clientes
Implementar módulo de habitaciones
Implementar módulo de reservas
Implementar módulo de pagos
Implementar módulo de reportes
Implementar módulo de empleados
Implementar módulo de configuración del hotel
Unificar estructura de interfaz con includes
Agregar documentación del sistema
```

---

## Pruebas funcionales

Las pruebas funcionales del sistema se encuentran documentadas en:

```text
docs/pruebas.md
```

En este archivo se describen pruebas como:

* Inicio de sesión.
* Control de roles.
* Registro de clientes.
* Validación de DNI duplicado.
* Gestión de habitaciones.
* Registro de reservas.
* Check-in.
* Finalización de reservas.
* Registro de pagos.
* Confirmación de pagos pendientes.
* Reembolsos.
* Reportes.
* Gestión de empleados.
* Configuración del hotel.

---

## Estado actual del proyecto

El sistema se encuentra en estado de **prototipo funcional**. Permite realizar las operaciones principales del flujo hotelero mediante una aplicación web local conectada a una base de datos MySQL/MariaDB.

Aunque no corresponde todavía a un sistema comercial completo, el proyecto permite demostrar:

* Funcionamiento con base de datos.
* Control de usuarios y roles.
* Operaciones CRUD.
* Gestión de reservas.
* Registro de pagos.
* Reportes.
* Documentación.
* Uso de Git.
* Buenas prácticas básicas de desarrollo.

---

## Mejoras futuras

Entre las mejoras que podrían implementarse más adelante se encuentran:

* Mejorar el diseño visual según el mockup final.
* Agregar diseño responsive avanzado.
* Exportar reportes en PDF o Excel.
* Implementar búsqueda avanzada por fechas.
* Agregar historial detallado por cliente.
* Agregar módulo de servicios adicionales.
* Integrar gráficos estadísticos.
* Preparar empaquetado con Electron.
* Mejorar validaciones del lado cliente con JavaScript.
* Separar completamente la lógica en modelos.
* Implementar variables de entorno para credenciales de base de datos.

---

## Autor

Proyecto desarrollado como prototipo académico para el sistema de gestión hotelera **Hotel Sumaq**.

## Pasos de Instalación

### 1. Clonar el Repositorio
```bash
git clone [https://github.com/TU-USUARIO/sumaq-hotel.git](https://github.com/TU-USUARIO/sumaq-hotel.git)
cd sumaq-hotel
