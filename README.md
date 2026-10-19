# API REST de gestión de menús y usuarios

## 1. Descripción del proyecto

Este proyecto consiste en una API REST desarrollada con Django y Django REST Framework para gestionar usuarios, menús y los permisos de acceso a dichos menús.

La API permite iniciar sesión, consultar la información del usuario autenticado, administrar usuarios y menús, asignar menús a usuarios y comprobar si un usuario tiene acceso a un menú determinado.

El objetivo es centralizar la gestión de usuarios y sus permisos mediante endpoints que pueden consumirse desde herramientas como Thunder Client, Postman o cualquier aplicación frontend.

## 2. Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **Django:** framework utilizado para desarrollar el backend.
- **Django REST Framework:** extensión de Django para construir APIs REST.
- **Django REST Framework Token Authentication:** mecanismo de autenticación mediante tokens.
- **Base de datos:** la configurada en el proyecto.
- **Thunder Client:** herramienta para realizar peticiones HTTP y probar los endpoints.

## 3. Requisitos previos

Antes de instalar el proyecto, asegúrate de tener los siguientes programas en tu computador:

1. **Python:** necesario para ejecutar el backend.
2. **Git:** necesario para descargar el repositorio, si está disponible en GitHub.
3. **Visual Studio Code:** recomendado para abrir y revisar el proyecto.
4. **Thunder Client:** extensión de Visual Studio Code para probar los endpoints.

Para comprobar que Python está instalado, abre una terminal y ejecuta:

```powershell
py --version
```

Para comprobar que Git está instalado:

```powershell
git --version
```

Si alguno de los comandos no funciona, instala el programa correspondiente antes de continuar.

## 4. Descargar el proyecto

### Opción A. Descargar desde GitHub

Abre una terminal en la carpeta donde quieras guardar el proyecto y ejecuta:

```powershell
git clone <URL_DEL_REPOSITORIO>
```

Reemplaza `<URL_DEL_REPOSITORIO>` por la dirección real del repositorio.

Después, entra en la carpeta descargada:

```powershell
cd <NOMBRE_DE_LA_CARPETA>
```

**Importante:** los siguientes comandos deben ejecutarse desde la carpeta raíz del proyecto, donde se encuentra `manage.py`.

## 5. Crear el entorno virtual

Un entorno virtual permite instalar las dependencias del proyecto de forma aislada, evitando conflictos con otros proyectos de Python.

En Windows, ejecuta:

```powershell
py -m venv .venv
```

Este comando crea una carpeta llamada `.venv` que contendrá el entorno virtual.

### Activar el entorno virtual

Si utilizas PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si utilizas el símbolo del sistema (CMD):

```bat
.venv\Scripts\activate.bat
```

Cuando esté activado, normalmente aparecerá `(.venv)` al comienzo de la línea de la terminal.

Si PowerShell bloquea la activación, puedes abrir una terminal CMD desde Visual Studio Code y utilizar el comando de activación indicado para CMD.

## 6. Instalar las dependencias

Primero, actualiza la herramienta utilizada para instalar paquetes de Python:

```powershell
python -m pip install --upgrade pip
```

Después, comprueba si el proyecto contiene un archivo llamado `requirements.txt`.

Si existe, instala las dependencias con:

```powershell
pip install -r requirements.txt
```

Este archivo contiene las librerías necesarias para ejecutar el proyecto.

Si no existe, instala como mínimo las dependencias principales:

```powershell
pip install django djangorestframework
```

La autenticación por tokens utilizada por Django REST Framework se proporciona mediante su módulo `rest_framework.authtoken`; no es necesario instalar un paquete independiente con ese nombre.

**Recomendación:** si el proyecto utiliza otras dependencias, estas también deben instalarse antes de continuar. Es preferible contar con un `requirements.txt` actualizado para que la instalación sea reproducible en otros computadores.

## 7. Configurar la base de datos

Antes de ejecutar el proyecto, revisa la configuración de la base de datos en los ajustes de Django.

La configuración se encuentra normalmente en el archivo `settings.py`.

La base de datos debe corresponder a la utilizada por el proyecto:

- **SQLite:** normalmente no requiere instalar ni iniciar un servidor de base de datos.
- **PostgreSQL u otro motor:** requiere que el servicio esté disponible, que las credenciales sean correctas y que esté instalada la dependencia correspondiente.

Si el proyecto utiliza variables de entorno, configura los valores necesarios siguiendo la estructura proporcionada por el proyecto.

No compartas contraseñas ni credenciales reales en el repositorio.

## 8. Verificar la configuración

Con el entorno virtual activado y las dependencias instaladas, ejecuta:

```powershell
python manage.py check
```

Este comando revisa la configuración del proyecto y muestra posibles errores.

Si aparece un mensaje indicando que no se encontraron problemas, puedes continuar.

Si aparecen errores, corrige los problemas señalados antes de avanzar.

## 9. Crear las tablas de la base de datos

Django utiliza migraciones para crear y actualizar las tablas de la base de datos según los modelos definidos en el proyecto.

Ejecuta:

```powershell
python manage.py migrate
```

Este comando aplica las migraciones existentes y crea las tablas necesarias.

En una instalación normal desde un repositorio, las migraciones deben estar incluidas en el proyecto. Si faltan migraciones propias de la aplicación, será necesario revisar el estado del repositorio antes de generarlas.

El comando para generar migraciones cuando corresponda es:

```powershell
python manage.py makemigrations
```

Después de generarlas, aplícalas:

```powershell
python manage.py migrate
```

## 10. Crear un usuario administrador

Para acceder al panel administrativo de Django, crea un superusuario ejecutando:

```powershell
python manage.py createsuperuser
```

Django solicitará los datos necesarios para crear la cuenta, como nombre de usuario, correo electrónico y contraseña, según la configuración del proyecto.

Esta cuenta permitirá administrar los datos desde el panel de Django.

Ten presente que el acceso administrativo de la API puede depender de que el usuario tenga habilitada la condición de personal (`is_staff`).

## 11. Iniciar el servidor

Una vez completados los pasos anteriores, inicia el servidor de desarrollo:

```powershell
python manage.py runserver
```

Si todo está configurado correctamente, Django mostrará un mensaje indicando que el servidor está ejecutándose.

La dirección local será:

- **Servidor:** http://127.0.0.1:8000/
- **Panel administrativo:** http://127.0.0.1:8000/admin/
- **API:** http://127.0.0.1:8000/api/

Para detener el servidor, utiliza `Ctrl + C` en la terminal.

## 12. Preparar los datos iniciales

Accede al panel administrativo desde el navegador:

http://127.0.0.1:8000/admin/

Inicia sesión con el superusuario creado anteriormente.

Si los modelos están registrados en el panel administrativo, desde allí podrás crear o revisar los usuarios y menús disponibles.

Para probar la asignación de permisos, asegúrate de tener usuarios y menús creados. La estructura y los campos disponibles dependerán de los modelos implementados en el proyecto.

## 13. Probar la API con Thunder Client

Thunder Client permite enviar peticiones HTTP al servidor y revisar las respuestas sin necesidad de desarrollar un frontend.

Si no lo tienes instalado, búscalo en la sección de extensiones de Visual Studio Code e instálalo.

### 13.1. Iniciar sesión

Crea una nueva petición en Thunder Client con la siguiente configuración:

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/api/auth/login/`
- **Body:** selecciona `JSON`.

Envía las credenciales del usuario en el cuerpo de la petición:

```json
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

Sustituye los valores de ejemplo por las credenciales de un usuario existente.

Si las credenciales son correctas, la respuesta debe incluir el token de autenticación y la información que devuelve el endpoint de inicio de sesión.

Guarda el token recibido. Lo necesitarás para probar los endpoints protegidos.

### 13.2. Configurar la autenticación

Para consultar endpoints protegidos, abre la sección **Headers** de Thunder Client y agrega:

| Key | Value |
|---|---|
| Authorization | Token TU_TOKEN |

Reemplaza `TU_TOKEN` por el token obtenido al iniciar sesión.

No incluyas las palabras `Bearer` ni `Token` dentro del valor del token. El encabezado completo debe utilizar el formato `Authorization: Token <token>`.

### 13.3. Consultar la información del usuario autenticado

- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/api/auth/me/`

Envía la petición con el encabezado de autenticación configurado.

Si el token es válido, el endpoint debe devolver la información del usuario autenticado.

### 13.4. Consultar los menús

- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/api/menus/`

Envía la petición.

Si la configuración de permisos permite la consulta al usuario autenticado, recibirás la lista de menús disponibles.

### 13.5. Consultar los usuarios

- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/api/users/`

Este endpoint está destinado a la administración de usuarios y requiere los permisos establecidos en el proyecto.

Utiliza un token de un usuario con privilegios administrativos para probarlo.

### 13.6. Crear un usuario

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/api/users/`
- **Body:** `JSON`

Envía los campos que espera el serializador de usuarios. La estructura exacta debe verificarse en la implementación del proyecto.

La petición debe incluir el encabezado de autenticación correspondiente y cumplir con los permisos definidos para crear usuarios.

### 13.7. Crear un menú

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/api/menus/`
- **Body:** `JSON`

Envía los campos definidos por el modelo y el serializador de menús.

Esta operación debe realizarse con un usuario que tenga permisos administrativos.

### 13.8. Consultar los menús asignados a un usuario

- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/api/users/ID/menus/`

Reemplaza `ID` por el identificador del usuario que deseas consultar.

Esta operación permite comprobar qué menús tiene asignados ese usuario. Su acceso está sujeto a los permisos configurados en el proyecto.

### 13.9. Asignar menús a un usuario

- **Método:** `PUT`
- **URL:** `http://127.0.0.1:8000/api/users/ID/menus/`
- **Body:** `JSON`

Reemplaza `ID` por el identificador del usuario.

El cuerpo de la petición utiliza la lista de identificadores de menús que espera el serializador de asignación. En la implementación actual, el campo se denomina `menu_ids`.

Ejemplo de estructura:

```json
{
  "menu_ids": [1, 2]
}
```

Los identificadores deben corresponder a menús existentes y activos. Esta operación requiere los permisos administrativos establecidos en la API.

### 13.10. Comprobar el acceso a un menú

- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/api/menus/ID/access/`

Reemplaza `ID` por el identificador del menú que deseas consultar.

La respuesta permitirá comprobar el acceso del usuario autenticado de acuerdo con la lógica de permisos implementada.

## 14. Resumen de endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/auth/login/` | Iniciar sesión y obtener un token. |
| `GET` | `/api/auth/me/` | Consultar el usuario autenticado. |
| `GET` | `/api/users/` | Consultar usuarios. |
| `POST` | `/api/users/` | Crear un usuario. |
| `GET` | `/api/menus/` | Consultar menús. |
| `POST` | `/api/menus/` | Crear un menú. |
| `GET` | `/api/users/{id}/menus/` | Consultar los menús asignados a un usuario. |
| `PUT` | `/api/users/{id}/menus/` | Actualizar los menús asignados a un usuario. |
| `GET` | `/api/menus/{id}/access/` | Comprobar el acceso a un menú. |

Los endpoints de administración están sujetos a los permisos definidos en el backend. Para conocer todas las operaciones disponibles, consulta las rutas registradas en el proyecto.

