# Modulo de usuarios, roles y accesos

Este documento explica como esta desarrollado el modulo de usuarios del ERP, que modelos lo componen, que funciones expone y como se relaciona con las demas entidades del sistema.

## 1. Objetivo del modulo

El modulo de usuarios controla la identidad de las personas que pueden entrar al sistema y prepara la base para definir su alcance operativo.

Actualmente cubre:

- Registro e inicio de sesion.
- Generacion y validacion de token JWT.
- Usuarios activos o inactivos.
- Roles generales del sistema.
- Perfiles de acceso por sucursal y bodega.
- Vinculacion entre usuario y vendedor.
- Administracion visual desde la pantalla `Usuarios, vendedores y accesos`.

El modulo esta dividido en dos areas principales:

- **Autenticacion**: login, registro, usuario autenticado y token.
- **Administracion de accesos**: usuarios, roles, sucursales, vendedores y perfiles operativos.

## 2. Archivos principales

| Archivo | Responsabilidad |
| --- | --- |
| `backend/app/models/user.py` | Define los modelos SQLAlchemy de usuarios, roles, sucursales, perfiles y vendedores. |
| `backend/app/schemas/user.py` | Define los esquemas Pydantic usados para entrada y salida de datos. |
| `backend/app/routers/auth.py` | Expone endpoints de autenticacion: registro, login y usuario actual. |
| `backend/app/routers/access.py` | Expone endpoints administrativos para usuarios, roles, sucursales, vendedores y perfiles. |
| `backend/app/core/security.py` | Maneja hash de claves, verificacion de claves y creacion de JWT. |
| `backend/app/main.py` | Registra routers, crea tablas y siembra datos iniciales del modulo. |
| `frontend/src/services/auth.js` | Consume endpoints de autenticacion y guarda la sesion en `localStorage`. |
| `frontend/src/services/access.js` | Consume endpoints del modulo administrativo de accesos. |
| `frontend/src/views/users/UsersView.vue` | Pantalla principal para administrar usuarios, vendedores, sucursales y accesos. |

## 3. Modelos de base de datos

Los modelos estan definidos en `backend/app/models/user.py`.

### 3.1. `Role`

Tabla: `roles`

Representa los roles generales de seguridad del sistema.

Campos principales:

| Campo | Tipo | Descripcion |
| --- | --- | --- |
| `id` | Integer | Identificador primario. |
| `name` | String(50) | Nombre unico del rol. |

Relacion:

- Un rol puede pertenecer a muchos usuarios.
- Se relaciona con `User` mediante la tabla intermedia `user_roles`.

Roles sembrados inicialmente:

- `administrador`
- `vendedor`
- `caja`
- `inventario`
- `supervisor`

### 3.2. `User`

Tabla: `users`

Representa una cuenta autenticable dentro del sistema.

Campos principales:

| Campo | Tipo | Descripcion |
| --- | --- | --- |
| `id` | Integer | Identificador primario. |
| `full_name` | String(100) | Nombre visible del usuario. |
| `email` | String(120) | Identificador unico de login. Aunque el campo se llama `email`, el sistema tambien lo usa como nombre de usuario. |
| `hashed_password` | String | Clave encriptada con bcrypt. |
| `is_active` | Boolean | Define si el usuario puede iniciar sesion. |

Relaciones:

- `roles`: relacion muchos a muchos con `Role`.
- `access_profiles`: perfiles de acceso por sucursal y bodega.
- `vendor_profile`: vendedor asociado al usuario, relacion uno a uno.

### 3.3. `user_roles`

Tabla: `user_roles`

Es una tabla intermedia para resolver la relacion muchos a muchos entre usuarios y roles.

Campos:

| Campo | Descripcion |
| --- | --- |
| `user_id` | Llave foranea hacia `users.id`. |
| `role_id` | Llave foranea hacia `roles.id`. |

Ambas llaves usan `ON DELETE CASCADE`, por lo que al eliminar un usuario o rol se eliminan sus asociaciones.

### 3.4. `Branch`

Tabla: `sucursales`

Representa una sucursal o ubicacion operativa del negocio.

Campos principales:

| Campo | Tipo | Descripcion |
| --- | --- | --- |
| `id` | Integer | Identificador primario. |
| `code` | String(40) | Codigo unico de la sucursal. |
| `name` | String(140) | Nombre de la sucursal. |
| `address` | String(220) | Direccion. |
| `phone` | String(80) | Telefono. |
| `activo` | Boolean | Estado operativo. |
| `created_at` | DateTime | Fecha de creacion. |

Relaciones:

- Una sucursal tiene muchas bodegas.
- Una sucursal puede aparecer en muchos perfiles de acceso.
- Una sucursal puede tener muchos vendedores.

### 3.5. `UserAccessProfile`

Tabla: `user_access_profiles`

Define el alcance operativo de un usuario. Este modelo responde preguntas como:

- En que sucursal trabaja el usuario.
- En que bodega opera.
- Que tipo de perfil operativo tiene.
- Que acciones puede realizar.
- Cual es su acceso principal.

Campos principales:

| Campo | Tipo | Descripcion |
| --- | --- | --- |
| `id` | Integer | Identificador primario. |
| `user_id` | Integer | Usuario propietario del perfil. |
| `sucursal_id` | Integer nullable | Sucursal asignada. Si es nulo, puede interpretarse como alcance general. |
| `bodega_id` | Integer nullable | Bodega asignada. Si es nulo, puede interpretarse como alcance general. |
| `role_scope` | String(50) | Perfil operativo: por ejemplo `VENDEDOR`, `CAJA`, `INVENTARIO`, `ADMINISTRADOR`. |
| `can_sell` | Boolean | Permite vender. |
| `can_move_inventory` | Boolean | Permite movimientos de inventario. |
| `can_manage_catalogs` | Boolean | Permite administrar catalogos. |
| `is_default` | Boolean | Marca el perfil principal del usuario. |
| `activo` | Boolean | Estado del perfil. |
| `created_at` | DateTime | Fecha de creacion. |

Restriccion:

- Existe una restriccion unica sobre `user_id`, `sucursal_id` y `bodega_id` para evitar duplicar el mismo alcance para un usuario.

Relaciones:

- Pertenece a un `User`.
- Puede pertenecer a una `Branch`.
- Puede pertenecer a una `Bodega`.

### 3.6. `Vendor`

Tabla: `vendedores`

Representa un vendedor comercial. Puede estar ligado a un usuario del sistema, pero tambien puede existir sin usuario vinculado.

Campos principales:

| Campo | Tipo | Descripcion |
| --- | --- | --- |
| `id` | Integer | Identificador primario. |
| `code` | String(40) | Codigo unico del vendedor. |
| `nombre` | String(160) | Nombre del vendedor. |
| `user_id` | Integer nullable unique | Usuario asociado. Es unico para mantener una relacion uno a uno. |
| `sucursal_id` | Integer nullable | Sucursal asignada. |
| `bodega_id` | Integer nullable | Bodega asignada. |
| `telefono` | String(80) | Telefono. |
| `email` | String(140) | Correo o usuario de referencia. |
| `meta_ventas` | Integer | Meta comercial. |
| `activo` | Boolean | Estado del vendedor. |
| `created_at` | DateTime | Fecha de creacion. |

Relaciones:

- Puede pertenecer a un `User`.
- Puede pertenecer a una `Branch`.
- Puede pertenecer a una `Bodega`.

## 4. Esquemas Pydantic

Los esquemas estan en `backend/app/schemas/user.py`. Separan los datos de entrada y salida del API.

### Roles

- `RoleBase`: contiene `name`.
- `RoleResponse`: agrega `id`.

### Usuarios

- `UserBase`: contiene `email` y `full_name`.
- `UserCreate`: agrega `password`.
- `UserUpdate`: permite actualizar `email`, `full_name`, `password`, `is_active` y `role_names`.
- `UserResponse`: retorna `id`, estado, roles, perfiles de acceso y vendedor vinculado.

### Sucursales

- `BranchCreate`: datos para crear sucursal.
- `BranchUpdate`: datos opcionales para modificar sucursal.
- `BranchResponse`: datos devueltos al frontend.

### Perfiles de acceso

- `UserAccessProfileCreate`: datos para crear perfil.
- `UserAccessProfileUpdate`: datos opcionales para modificar perfil.
- `UserAccessProfileResponse`: incluye nombres calculados como `sucursal_name`, `bodega_name`, `user_name` y `user_email`.

### Vendedores

- `VendorCreate`: datos para crear vendedor.
- `VendorUpdate`: datos opcionales para modificar vendedor.
- `VendorResponse`: incluye datos del usuario, sucursal y bodega relacionados.

## 5. Seguridad y autenticacion

La seguridad base esta en `backend/app/core/security.py`.

Funciones principales:

| Funcion | Descripcion |
| --- | --- |
| `hash_password(password)` | Encripta una clave usando bcrypt. |
| `verify_password(plain, hashed)` | Compara una clave plana contra el hash guardado. |
| `create_access_token(data)` | Genera un JWT con expiracion configurada. |

Configuracion importante:

- Algoritmo JWT: `HS256`.
- Clave secreta: `JWT_SECRET_KEY`.
- Expiracion: `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.
- En desarrollo la documentacion del proyecto indica 480 minutos, equivalente a 8 horas.

## 6. Router de autenticacion

Archivo: `backend/app/routers/auth.py`

Prefijo: `/auth`

### `POST /auth/register`

Crea un usuario basico.

Flujo:

1. Normaliza el email a minusculas.
2. Verifica que no exista otro usuario con el mismo email.
3. Encripta la clave con `hash_password`.
4. Crea el usuario activo.
5. Retorna el usuario creado.

Este endpoint no asigna roles por defecto. La asignacion automatica de rol `vendedor` se hace en el endpoint administrativo `/access/users`.

### `POST /auth/login`

Inicia sesion.

Entrada:

- `email`
- `password`

Detalle importante:

- El campo `email` funciona como identificador.
- El sistema busca por `email` o por `full_name`, ambos normalizados a minusculas.

Validaciones:

1. Usuario existente.
2. Clave correcta.
3. Usuario activo.

Salida:

- `access_token`
- `token_type`
- `user`

El objeto `user` incluye:

- Datos del usuario.
- Roles.
- Perfiles de acceso.
- Vendedor vinculado, si existe.

### `GET /auth/me`

Devuelve el usuario autenticado segun el token Bearer.

Usa la funcion interna `_get_user_from_token`.

### `_get_user_from_token(credentials, db)`

Funcion reutilizable para validar sesion.

Flujo:

1. Verifica que exista encabezado Authorization tipo Bearer.
2. Decodifica el JWT.
3. Lee el `sub` del token.
4. Busca el usuario por email.
5. Rechaza usuarios inexistentes o inactivos.
6. Retorna el modelo `User`.

Esta funcion tambien se reutiliza en el router de configuracion para proteger endpoints.

## 7. Router administrativo de accesos

Archivo: `backend/app/routers/access.py`

Prefijo: `/access`

Este router administra usuarios, roles, sucursales, vendedores y perfiles.

### Funciones auxiliares

| Funcion | Proposito |
| --- | --- |
| `_normalize(value, field)` | Limpia texto y valida que sea requerido. |
| `_role_names_for_scope(scope)` | Convierte un perfil operativo en roles base. |
| `_get_or_create_roles(db, names)` | Busca roles por nombre o los crea si no existen. |
| `_ensure_branch(db, branch_id)` | Valida que exista una sucursal. |
| `_ensure_bodega(db, bodega_id)` | Valida que exista una bodega. |
| `_user_response(user)` | Construye respuesta completa de usuario. |
| `_vendor_response(vendor)` | Construye respuesta completa de vendedor. |
| `_access_response(profile)` | Construye respuesta completa de perfil de acceso. |
| `_apply_default_scope(db, profile)` | Si un perfil es principal, desmarca los otros perfiles principales del mismo usuario. |

### Roles

#### `GET /access/roles`

Lista los roles ordenados por nombre.

### Usuarios

#### `GET /access/users`

Lista usuarios con:

- Roles.
- Perfiles de acceso.
- Sucursal y bodega asociadas a cada perfil.
- Vendedor vinculado.

Usa `joinedload` para cargar relaciones y evitar consultas repetidas.

#### `POST /access/users`

Crea un usuario administrativo.

Flujo:

1. Normaliza email.
2. Valida duplicados.
3. Encripta la clave.
4. Crea el usuario activo.
5. Asigna el rol `vendedor` por defecto.
6. Retorna el usuario completo.

#### `PUT /access/users/{user_id}`

Actualiza usuario.

Permite modificar:

- Email.
- Nombre.
- Clave.
- Estado activo/inactivo.
- Lista de roles.

Si se envia una nueva clave, se vuelve a guardar como hash.

### Sucursales

#### `GET /access/branches`

Lista sucursales ordenadas por nombre.

#### `POST /access/branches`

Crea una sucursal.

Validaciones:

- Codigo requerido.
- Nombre requerido.
- Codigo unico.

El codigo se guarda en mayusculas.

#### `PUT /access/branches/{branch_id}`

Actualiza sucursal.

Permite cambiar:

- Codigo.
- Nombre.
- Direccion.
- Telefono.
- Estado activo.

### Vendedores

#### `GET /access/vendors`

Lista vendedores.

Parametro:

- `include_inactive`: si es `true`, incluye vendedores inactivos.

#### `POST /access/vendors`

Crea vendedor.

Validaciones:

- Codigo unico.
- Usuario existente si se envia `user_id`.
- Sucursal existente si se envia `sucursal_id`.
- Bodega existente si se envia `bodega_id`.

Comportamiento adicional:

- Si el vendedor se vincula a un usuario y ese usuario no tiene rol `vendedor`, el rol se agrega automaticamente.

#### `PUT /access/vendors/{vendor_id}`

Actualiza vendedor.

Permite cambiar:

- Codigo.
- Nombre.
- Usuario vinculado.
- Sucursal.
- Bodega.
- Telefono.
- Email.
- Meta de ventas.
- Estado activo.

### Perfiles de acceso

#### `POST /access/profiles`

Crea perfil de acceso para un usuario.

Validaciones:

- Usuario existente.
- Sucursal existente si se envia.
- Bodega existente si se envia.

Comportamiento adicional:

- Asigna roles automaticamente segun `role_scope`.
- Si el perfil se marca como `is_default`, se desmarcan los otros perfiles principales del mismo usuario.

Mapeo de `role_scope` a rol:

| `role_scope` contiene | Rol asignado |
| --- | --- |
| `admin` | `administrador` |
| `inventario` | `inventario` |
| `caja` | `caja` |
| otro valor | `vendedor` |

#### `PUT /access/profiles/{profile_id}`

Actualiza perfil de acceso.

Permite cambiar:

- Sucursal.
- Bodega.
- Perfil operativo.
- Permiso de ventas.
- Permiso de inventario.
- Permiso de catalogos.
- Indicador de acceso principal.
- Estado activo.

## 8. Datos iniciales del modulo

El archivo `backend/app/main.py` ejecuta varias funciones al iniciar la aplicacion.

### `create_initial_admin()`

Crea o actualiza el usuario administrador inicial.

Valores actuales:

| Dato | Valor |
| --- | --- |
| Usuario/email | `administrador` |
| Clave | `020416` |
| Nombre | `Administrador` |
| Rol | `administrador` |

Si ya existe un usuario con email `administrador`, email `admin@erp.com` o nombre `Administrador`, lo normaliza a los valores actuales.

### `seed_inventory_catalogs()`

Ademas de catalogos de inventario, asegura la existencia de:

- Tabla `sucursales`.
- Columna `sucursal_id` en `bodegas`.
- Tabla `user_access_profiles`.
- Indice unico para evitar perfiles duplicados por usuario/sucursal/bodega.
- Tabla `vendedores`.
- Sucursal principal `SUC-001`.
- Bodega principal `BOD-001`, si no existe ninguna.

### `seed_access_catalogs()`

Siembra los catalogos de acceso:

- Roles base.
- Perfil de acceso administrador para la sucursal y bodega principal.
- Vendedor `VEN-001` vinculado al administrador.
- Vendedor `VEN-PISO` sin usuario vinculado.

## 9. Frontend del modulo

La administracion visual esta en `frontend/src/views/users/UsersView.vue`.

La pantalla tiene cuatro pestanas:

- `Usuarios`
- `Vendedores`
- `Sucursales`
- `Accesos`

Servicios usados:

- `frontend/src/services/auth.js`
- `frontend/src/services/access.js`
- `frontend/src/config/api.js`

### Manejo de sesion en frontend

Cuando el login es correcto:

1. `loginUser()` llama a `/auth/login`.
2. `storeSession()` guarda:
   - `token`
   - `currentUser`
3. `apiRequest()` adjunta automaticamente `Authorization: Bearer <token>` si existe token.
4. `readStoredUser()` permite a las vistas obtener el usuario actual desde `localStorage`.

### Pantalla de usuarios

Permite:

- Listar usuarios.
- Crear usuarios.
- Editar usuarios.
- Cambiar clave.
- Activar o desactivar usuarios.
- Asignar roles.
- Ver acceso principal.

### Pantalla de vendedores

Permite:

- Listar vendedores.
- Crear vendedores.
- Editar vendedores.
- Vincular vendedor con usuario.
- Asignar sucursal y bodega.

### Pantalla de sucursales

Permite:

- Listar sucursales.
- Crear sucursales.
- Editar datos generales.
- Activar o desactivar sucursales.

### Pantalla de accesos

Permite:

- Listar perfiles de acceso.
- Crear perfil por usuario.
- Editar perfil.
- Definir sucursal y bodega.
- Definir permisos operativos:
  - Ventas.
  - Inventario.
  - Catalogos.
- Marcar acceso principal.

## 10. Relaciones con otras entidades

### Relacion con bodegas

El modelo `Bodega`, definido en `backend/app/models/inventory.py`, se relaciona con:

- `Branch` mediante `sucursal_id`.
- `UserAccessProfile` mediante `bodega_id`.
- `Vendor` mediante `bodega_id`.

Esto permite que un usuario o vendedor quede ligado a una bodega especifica.

### Relacion con inventario

Los movimientos de inventario tienen trazabilidad de usuario:

- `IngresoInventario.usuario_id` apunta a `users.id`.
- `EgresoInventario.usuario_id` apunta a `users.id`.
- Tambien existe `usuario_registro`, usado para guardar texto como email o nombre del usuario.

En el estado actual, varias operaciones envian `usuario_registro` desde el frontend usando el usuario guardado en sesion. En algunas rutas `usuario_id` todavia puede enviarse como `None`.

### Relacion con ventas

El modelo `SalesInvoice` guarda:

- `vendor_name`: nombre del vendedor usado en la factura.
- `bodega_id`: bodega desde donde sale la venta.
- `usuario_registro`: usuario que registro la venta.
- `egreso_id`: movimiento de egreso de inventario generado por la venta.

En la vista de ventas, el sistema usa el usuario actual para seleccionar una bodega por defecto:

1. Busca un perfil de acceso activo y principal con `bodega_id`.
2. Si no lo encuentra, busca otro perfil activo con `bodega_id`.
3. Si no lo encuentra, usa el `vendor_profile`.
4. Si no hay datos, usa la primera bodega disponible.

Esto hace que el modulo de usuarios influya directamente en el flujo comercial.

### Relacion con configuracion

El router de configuracion reutiliza `_get_user_from_token` para proteger endpoints. Esto significa que la configuracion depende del modulo de autenticacion para validar que exista un usuario activo.

### Relacion con navegacion del frontend

El router frontend protege rutas con `meta.requiresAuth`. Si no existe token en `localStorage`, redirige a `/login`.

La seguridad de navegacion frontend evita accesos visuales casuales, pero la proteccion real debe aplicarse tambien en backend por endpoint.

## 11. Flujo completo de uso

### Login

1. El usuario entra a `/login`.
2. El frontend envia credenciales a `POST /auth/login`.
3. El backend busca usuario por `email` o `full_name`.
4. Valida clave con bcrypt.
5. Verifica `is_active`.
6. Genera JWT.
7. Retorna token y datos completos del usuario.
8. El frontend guarda la sesion y entra al sistema.

### Creacion de usuario administrativo

1. El administrador abre la pestana `Usuarios`.
2. Completa nombre, usuario/email, clave y roles.
3. El frontend llama a `POST /access/users`.
4. El backend crea el usuario con clave encriptada.
5. Si no se especifica otro rol, queda como `vendedor`.

### Asignacion de acceso operativo

1. El administrador abre la pestana `Accesos`.
2. Selecciona usuario, perfil, sucursal y bodega.
3. Define permisos operativos.
4. El frontend llama a `POST /access/profiles`.
5. El backend crea el perfil y asigna rol segun `role_scope`.
6. Si es acceso principal, desmarca otros accesos principales del usuario.

### Vinculacion de vendedor

1. El administrador abre la pestana `Vendedores`.
2. Crea o edita un vendedor.
3. Selecciona usuario vinculado.
4. Define sucursal y bodega.
5. El backend guarda la relacion uno a uno entre vendedor y usuario.

## 12. Estado actual y consideraciones tecnicas

El modulo ya tiene una base funcional para usuarios y accesos:

- Existe login JWT.
- Existen roles.
- Existe CRUD administrativo inicial.
- Existe perfil de acceso por sucursal y bodega.
- Existe vinculacion usuario-vendedor.
- Ventas e inventario usan datos del usuario para trazabilidad y bodega por defecto.

Pendientes o puntos a reforzar:

- El router `/access` actualmente no usa dependencia de autenticacion en sus endpoints. El frontend envia token, pero el backend no lo exige ahi.
- Falta aplicar una matriz completa de permisos por modulo y accion.
- En inventario y ventas, parte de la trazabilidad usa `usuario_registro` como texto y no siempre `usuario_id`.
- Los permisos `can_sell`, `can_move_inventory` y `can_manage_catalogs` estan modelados, pero no estan aplicados de forma completa como autorizacion en todos los endpoints.
- Conviene centralizar una dependencia tipo `get_current_user` y helpers como `require_role` o `require_permission`.

## 13. Resumen de relaciones

```text
users N:N roles
users 1:N user_access_profiles
users 1:1 vendedores
sucursales 1:N bodegas
sucursales 1:N user_access_profiles
sucursales 1:N vendedores
bodegas 1:N user_access_profiles
bodegas 1:N vendedores
bodegas 1:N sales_invoices
bodegas 1:N ingresos_inventario
bodegas 1:N egresos_inventario
users 1:N ingresos_inventario
users 1:N egresos_inventario
```

En conjunto, el modulo de usuarios no solo permite iniciar sesion. Tambien define desde donde opera cada usuario, que rol tiene, que vendedor representa y como se registra su participacion en ventas e inventario.
