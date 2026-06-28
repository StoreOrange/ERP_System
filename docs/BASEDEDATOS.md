# Base de datos del sistema de planificacion de recursos empresariales

Ultima verificacion directa: 2026-06-22

## Resumen ejecutivo

Este documento fue generado a partir del esquema `public` de PostgreSQL en
Docker. Refleja las tablas, columnas, relaciones, restricciones e indices que
existen realmente en la base operativa, no solo los modelos ORM.

| Dato | Valor |
| --- | --- |
| Motor | PostgreSQL 16 |
| Base de datos | `ERPDB` |
| Esquema | `public` |
| Host desde Windows | `localhost` |
| Puerto | `5433` |
| Usuario de desarrollo | `user` |
| Tablas fisicas | 37 |
| Columnas | 335 |
| Claves foraneas | 52 |
| Restricciones | 110 |
| Indices | 101 |
| Revision Alembic | `5285f6b056a5` |
| Volumen Docker | `erp_system_postgres_data` |

> La instancia utilizada por la aplicacion esta en Docker y se publica en el
> puerto `5433`. Una base `ERPDB` abierta en PostgreSQL local por el puerto
> `5432` corresponde a otra instancia y puede aparecer vacia.

## Convenciones

- **PK**: clave primaria.
- **FK**: clave foranea.
- **UNIQUE**: valor o combinacion no repetible.
- **CHECK**: validacion declarativa.
- **Nulo = No**: columna obligatoria.
- Los importes `USD` y `CS` se conservan por separado para mantener el
  valor historico de cada operacion.
- La existencia por bodega se calcula con entradas menos salidas.

## Estado de migraciones

Alembic registra la revision `5285f6b056a5`, pero esta revision no representa
por si sola las 37 tablas actuales. Parte del esquema se crea con
`Base.metadata.create_all()` y sentencias de compatibilidad ejecutadas durante
el arranque del backend. Antes de produccion se debe crear una migracion
consolidada y retirar los cambios de esquema desde `app.main`.

## Mapa completo de relaciones

- `user_access_profiles`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`
- `user_access_profiles`: `FOREIGN KEY (sucursal_id) REFERENCES sucursales(id)`
- `user_access_profiles`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `user_roles`: `FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE`
- `user_roles`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- `vendedores`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`
- `vendedores`: `FOREIGN KEY (sucursal_id) REFERENCES sucursales(id)`
- `vendedores`: `FOREIGN KEY (user_id) REFERENCES users(id)`
- `bodegas`: `FOREIGN KEY (sucursal_id) REFERENCES sucursales(id)`
- `productos`: `FOREIGN KEY (linea_id) REFERENCES lineas(id)`
- `productos`: `FOREIGN KEY (marca_id) REFERENCES marcas(id)`
- `productos`: `FOREIGN KEY (segmento_id) REFERENCES segmentos(id)`
- `productos`: `FOREIGN KEY (unidad_medida_id) REFERENCES unidades_medida(id)`
- `saldos_productos`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`
- `producto_combos`: `FOREIGN KEY (child_producto_id) REFERENCES productos(id)`
- `producto_combos`: `FOREIGN KEY (parent_producto_id) REFERENCES productos(id)`
- `productos_receta_lineas`: `FOREIGN KEY (insumo_producto_id) REFERENCES productos(id)`
- `productos_receta_lineas`: `FOREIGN KEY (receta_id) REFERENCES productos_recetas(id)`
- `productos_receta_lineas`: `FOREIGN KEY (unidad_medida_id) REFERENCES unidades_medida(id)`
- `productos_recetas`: `FOREIGN KEY (producto_final_id) REFERENCES productos(id)`
- `ingreso_items`: `FOREIGN KEY (ingreso_id) REFERENCES ingresos_inventario(id)`
- `ingreso_items`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`
- `ingresos_inventario`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`
- `ingresos_inventario`: `FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)`
- `ingresos_inventario`: `FOREIGN KEY (tipo_id) REFERENCES ingreso_tipos(id)`
- `ingresos_inventario`: `FOREIGN KEY (usuario_id) REFERENCES users(id)`
- `egreso_items`: `FOREIGN KEY (egreso_id) REFERENCES egresos_inventario(id)`
- `egreso_items`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`
- `egresos_inventario`: `FOREIGN KEY (bodega_destino_id) REFERENCES bodegas(id)`
- `egresos_inventario`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`
- `egresos_inventario`: `FOREIGN KEY (tipo_id) REFERENCES egreso_tipos(id)`
- `egresos_inventario`: `FOREIGN KEY (usuario_id) REFERENCES users(id)`
- `producciones_inventario`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`
- `producciones_inventario`: `FOREIGN KEY (egreso_id) REFERENCES egresos_inventario(id)`
- `producciones_inventario`: `FOREIGN KEY (ingreso_id) REFERENCES ingresos_inventario(id)`
- `producciones_inventario`: `FOREIGN KEY (producto_final_id) REFERENCES productos(id)`
- `producciones_inventario_lineas`: `FOREIGN KEY (produccion_id) REFERENCES producciones_inventario(id)`
- `producciones_inventario_lineas`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`
- `paca_apertura_origenes`: `FOREIGN KEY (apertura_id) REFERENCES paca_aperturas(id)`
- `paca_apertura_origenes`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`
- `paca_aperturas`: `FOREIGN KEY (bodega_destino_id) REFERENCES bodegas(id)`
- `paca_aperturas`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`
- `paca_aperturas`: `FOREIGN KEY (egreso_id) REFERENCES egresos_inventario(id)`
- `paca_aperturas`: `FOREIGN KEY (ingreso_id) REFERENCES ingresos_inventario(id)`
- `paca_aperturas`: `FOREIGN KEY (paca_producto_id) REFERENCES productos(id)`
- `paca_apertura_lineas`: `FOREIGN KEY (apertura_id) REFERENCES paca_aperturas(id)`
- `paca_apertura_lineas`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`
- `sales_invoice_items`: `FOREIGN KEY (invoice_id) REFERENCES sales_invoices(id)`
- `sales_invoice_items`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`
- `sales_invoices`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`
- `sales_invoices`: `FOREIGN KEY (egreso_id) REFERENCES egresos_inventario(id)`
- `sales_payments`: `FOREIGN KEY (invoice_id) REFERENCES sales_invoices(id)`

## Inventario de tablas

### Control, seguridad y acceso

| Tabla | Proposito |
| --- | --- |
| `alembic_version` | Control de la revision de esquema aplicada por Alembic. |
| `roles` | Catalogo de roles de seguridad. |
| `users` | Usuarios autenticables del sistema. |
| `user_roles` | Relacion muchos a muchos entre usuarios y roles. |
| `sucursales` | Sucursales o puntos operativos de la empresa. |
| `user_access_profiles` | Alcance operativo del usuario por sucursal, bodega y permisos. |
| `vendedores` | Vendedores vinculables con usuario, sucursal y bodega. |

### Configuracion y terceros

| Tabla | Proposito |
| --- | --- |
| `business_settings` | Identidad empresarial, tema y politicas operativas. |
| `company_environments` | Entornos o conexiones empresariales configurables. |
| `exchange_rates` | Historial de tasas de cambio por fecha y periodo. |
| `clientes` | Catalogo de clientes utilizados en ventas. |
| `proveedores` | Catalogo de proveedores de mercaderia. |

### Catalogos de inventario

| Tabla | Proposito |
| --- | --- |
| `lineas` | Lineas comerciales de productos. |
| `segmentos` | Segmentos o subclasificaciones de productos. |
| `unidades_medida` | Unidades utilizadas por productos y recetas. |
| `marcas` | Catalogo de marcas. |
| `bodegas` | Bodegas de inventario asociables a sucursales. |
| `ingreso_tipos` | Conceptos de entrada de inventario. |
| `egreso_tipos` | Conceptos de salida de inventario. |

### Productos, saldos, recetas y combos

| Tabla | Proposito |
| --- | --- |
| `productos` | Maestro de productos, precios, costo y clasificacion. |
| `saldos_productos` | Saldo global materializado por producto. |
| `productos_recetas` | Cabecera de receta de un producto final. |
| `productos_receta_lineas` | Insumos y cantidades requeridas por receta. |
| `producto_combos` | Composicion de combos: principal e incluidos/regalias. |

### Movimientos de inventario

| Tabla | Proposito |
| --- | --- |
| `ingresos_inventario` | Cabecera documental de entradas de inventario. |
| `ingreso_items` | Productos y costos de cada ingreso. |
| `egresos_inventario` | Cabecera documental de salidas y traslados. |
| `egreso_items` | Productos y costos de cada egreso. |

### Produccion y apertura de pacas

| Tabla | Proposito |
| --- | --- |
| `producciones_inventario` | Ordenes generales de produccion. |
| `producciones_inventario_lineas` | Insumos y resultados de una produccion. |
| `paca_aperturas` | Cabecera de apertura y clasificacion de pacas. |
| `paca_apertura_origenes` | Pacas o productos origen consumidos. |
| `paca_apertura_lineas` | Productos clasificados, valor y costo asignado. |

### Ventas y facturacion POS

| Tabla | Proposito |
| --- | --- |
| `sales_invoices` | Cabecera de factura POS y totales financieros. |
| `sales_invoice_items` | Detalle historico facturado, incluidos combos. |
| `sales_payments` | Pagos aplicados a facturas POS. |
| `sales_sequences` | Consecutivos de numeracion de facturas. |

## Diccionario de datos completo

### Control, seguridad y acceso

#### `alembic_version`

Control de la revision de esquema aplicada por Alembic.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `version_num` | `character varying(32)` | No | - |

**Restricciones**

- **PRIMARY KEY** `alembic_version_pkc`: `PRIMARY KEY (version_num)`.

**Indices**

- `alembic_version_pkc`: `CREATE UNIQUE INDEX alembic_version_pkc ON public.alembic_version USING btree (version_num)`.

#### `roles`

Catalogo de roles de seguridad.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('roles_id_seq'::regclass)` |
| 2 | `name` | `character varying(50)` | No | - |

**Restricciones**

- **PRIMARY KEY** `roles_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `roles_name_key`: `UNIQUE (name)`.

**Indices**

- `ix_roles_id`: `CREATE INDEX ix_roles_id ON public.roles USING btree (id)`.
- `roles_name_key`: `CREATE UNIQUE INDEX roles_name_key ON public.roles USING btree (name)`.
- `roles_pkey`: `CREATE UNIQUE INDEX roles_pkey ON public.roles USING btree (id)`.

#### `users`

Usuarios autenticables del sistema.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('users_id_seq'::regclass)` |
| 2 | `full_name` | `character varying(100)` | Si | - |
| 3 | `email` | `character varying(120)` | No | - |
| 4 | `hashed_password` | `character varying` | No | - |
| 5 | `is_active` | `boolean` | Si | - |

**Restricciones**

- **PRIMARY KEY** `users_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ix_users_email`: `CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email)`.
- `ix_users_id`: `CREATE INDEX ix_users_id ON public.users USING btree (id)`.
- `users_pkey`: `CREATE UNIQUE INDEX users_pkey ON public.users USING btree (id)`.

#### `user_roles`

Relacion muchos a muchos entre usuarios y roles.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `user_id` | `integer` | Si | - |
| 2 | `role_id` | `integer` | Si | - |

**Restricciones**

- **FOREIGN KEY** `user_roles_role_id_fkey`: `FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE`.
- **FOREIGN KEY** `user_roles_user_id_fkey`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`.

**Indices**

- No registra indices.

#### `sucursales`

Sucursales o puntos operativos de la empresa.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('sucursales_id_seq'::regclass)` |
| 2 | `code` | `character varying(40)` | No | - |
| 3 | `name` | `character varying(140)` | No | - |
| 4 | `address` | `character varying(220)` | Si | - |
| 5 | `phone` | `character varying(80)` | Si | - |
| 6 | `activo` | `boolean` | Si | - |
| 7 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `sucursales_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `sucursales_code_key`: `UNIQUE (code)`.

**Indices**

- `ix_sucursales_id`: `CREATE INDEX ix_sucursales_id ON public.sucursales USING btree (id)`.
- `sucursales_code_key`: `CREATE UNIQUE INDEX sucursales_code_key ON public.sucursales USING btree (code)`.
- `sucursales_pkey`: `CREATE UNIQUE INDEX sucursales_pkey ON public.sucursales USING btree (id)`.

#### `user_access_profiles`

Alcance operativo del usuario por sucursal, bodega y permisos.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('user_access_profiles_id_seq'::regclass)` |
| 2 | `user_id` | `integer` | No | - |
| 3 | `sucursal_id` | `integer` | Si | - |
| 4 | `bodega_id` | `integer` | Si | - |
| 5 | `role_scope` | `character varying(50)` | No | - |
| 6 | `can_sell` | `boolean` | Si | - |
| 7 | `can_move_inventory` | `boolean` | Si | - |
| 8 | `can_manage_catalogs` | `boolean` | Si | - |
| 9 | `is_default` | `boolean` | Si | - |
| 10 | `activo` | `boolean` | Si | - |
| 11 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `user_access_profiles_bodega_id_fkey`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`.
- **FOREIGN KEY** `user_access_profiles_sucursal_id_fkey`: `FOREIGN KEY (sucursal_id) REFERENCES sucursales(id)`.
- **FOREIGN KEY** `user_access_profiles_user_id_fkey`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`.
- **PRIMARY KEY** `user_access_profiles_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `uq_user_access_scope`: `UNIQUE (user_id, sucursal_id, bodega_id)`.

**Indices**

- `ix_user_access_profiles_id`: `CREATE INDEX ix_user_access_profiles_id ON public.user_access_profiles USING btree (id)`.
- `uq_user_access_scope`: `CREATE UNIQUE INDEX uq_user_access_scope ON public.user_access_profiles USING btree (user_id, sucursal_id, bodega_id)`.
- `uq_user_access_scope_idx`: `CREATE UNIQUE INDEX uq_user_access_scope_idx ON public.user_access_profiles USING btree (user_id, COALESCE(sucursal_id, 0), COALESCE(bodega_id, 0))`.
- `user_access_profiles_pkey`: `CREATE UNIQUE INDEX user_access_profiles_pkey ON public.user_access_profiles USING btree (id)`.

#### `vendedores`

Vendedores vinculables con usuario, sucursal y bodega.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('vendedores_id_seq'::regclass)` |
| 2 | `code` | `character varying(40)` | No | - |
| 3 | `nombre` | `character varying(160)` | No | - |
| 4 | `user_id` | `integer` | Si | - |
| 5 | `sucursal_id` | `integer` | Si | - |
| 6 | `bodega_id` | `integer` | Si | - |
| 7 | `telefono` | `character varying(80)` | Si | - |
| 8 | `email` | `character varying(140)` | Si | - |
| 9 | `meta_ventas` | `integer` | Si | - |
| 10 | `activo` | `boolean` | Si | - |
| 11 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `vendedores_bodega_id_fkey`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`.
- **FOREIGN KEY** `vendedores_sucursal_id_fkey`: `FOREIGN KEY (sucursal_id) REFERENCES sucursales(id)`.
- **FOREIGN KEY** `vendedores_user_id_fkey`: `FOREIGN KEY (user_id) REFERENCES users(id)`.
- **PRIMARY KEY** `vendedores_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `vendedores_code_key`: `UNIQUE (code)`.
- **UNIQUE** `vendedores_user_id_key`: `UNIQUE (user_id)`.

**Indices**

- `ix_vendedores_id`: `CREATE INDEX ix_vendedores_id ON public.vendedores USING btree (id)`.
- `vendedores_code_key`: `CREATE UNIQUE INDEX vendedores_code_key ON public.vendedores USING btree (code)`.
- `vendedores_pkey`: `CREATE UNIQUE INDEX vendedores_pkey ON public.vendedores USING btree (id)`.
- `vendedores_user_id_key`: `CREATE UNIQUE INDEX vendedores_user_id_key ON public.vendedores USING btree (user_id)`.

### Configuracion y terceros

#### `business_settings`

Identidad empresarial, tema y politicas operativas.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('business_settings_id_seq'::regclass)` |
| 2 | `business_name` | `character varying(160)` | No | - |
| 3 | `legal_name` | `character varying(180)` | Si | - |
| 4 | `trade_name` | `character varying(180)` | Si | - |
| 5 | `app_title` | `character varying(180)` | Si | - |
| 6 | `sidebar_subtitle` | `character varying(200)` | Si | - |
| 7 | `address` | `text` | Si | - |
| 8 | `ruc` | `character varying(80)` | Si | - |
| 9 | `phone` | `character varying(80)` | Si | - |
| 10 | `phones` | `character varying(200)` | Si | - |
| 11 | `email` | `character varying(180)` | Si | - |
| 12 | `website` | `character varying(200)` | Si | - |
| 13 | `theme_code` | `character varying(60)` | Si | - |
| 14 | `sales_interface_code` | `character varying(60)` | Si | - |
| 15 | `pricing_currency` | `character varying(10)` | No | - |
| 16 | `logo_login` | `character varying(255)` | Si | - |
| 17 | `logo_sidebar` | `character varying(255)` | Si | - |
| 18 | `logo_invoice` | `character varying(255)` | Si | - |
| 19 | `logo_favicon` | `character varying(255)` | Si | - |
| 20 | `inventory_cs_only` | `boolean` | No | - |
| 21 | `weighted_inventory_enabled` | `boolean` | No | - |
| 22 | `weighted_sales_enabled` | `boolean` | No | - |
| 23 | `recipe_explosion_on_ingreso` | `boolean` | No | - |
| 24 | `multi_branch_enabled` | `boolean` | No | - |
| 25 | `price_auto_from_cost_enabled` | `boolean` | No | - |
| 26 | `price_margin_percent` | `integer` | No | - |

**Restricciones**

- **PRIMARY KEY** `business_settings_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `business_settings_pkey`: `CREATE UNIQUE INDEX business_settings_pkey ON public.business_settings USING btree (id)`.
- `ix_business_settings_id`: `CREATE INDEX ix_business_settings_id ON public.business_settings USING btree (id)`.

#### `company_environments`

Entornos o conexiones empresariales configurables.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('company_environments_id_seq'::regclass)` |
| 2 | `company_key` | `character varying(80)` | No | - |
| 3 | `company_name` | `character varying(180)` | No | - |
| 4 | `database_url` | `text` | No | - |
| 5 | `is_active` | `boolean` | No | - |

**Restricciones**

- **PRIMARY KEY** `company_environments_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `company_environments_company_key_key`: `UNIQUE (company_key)`.

**Indices**

- `company_environments_company_key_key`: `CREATE UNIQUE INDEX company_environments_company_key_key ON public.company_environments USING btree (company_key)`.
- `company_environments_pkey`: `CREATE UNIQUE INDEX company_environments_pkey ON public.company_environments USING btree (id)`.
- `ix_company_environments_id`: `CREATE INDEX ix_company_environments_id ON public.company_environments USING btree (id)`.

#### `exchange_rates`

Historial de tasas de cambio por fecha y periodo.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('exchange_rates_id_seq'::regclass)` |
| 2 | `effective_date` | `date` | No | - |
| 3 | `period_type` | `character varying(20)` | No | - |
| 4 | `rate` | `numeric(12,4)` | No | - |
| 5 | `notes` | `text` | Si | - |
| 6 | `is_active` | `boolean` | No | - |
| 7 | `created_at` | `timestamp without time zone` | No | - |

**Restricciones**

- **PRIMARY KEY** `exchange_rates_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `exchange_rates_pkey`: `CREATE UNIQUE INDEX exchange_rates_pkey ON public.exchange_rates USING btree (id)`.
- `ix_exchange_rates_effective_date`: `CREATE INDEX ix_exchange_rates_effective_date ON public.exchange_rates USING btree (effective_date)`.
- `ix_exchange_rates_id`: `CREATE INDEX ix_exchange_rates_id ON public.exchange_rates USING btree (id)`.

#### `clientes`

Catalogo de clientes utilizados en ventas.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('clientes_id_seq'::regclass)` |
| 2 | `nombre` | `character varying(180)` | No | - |
| 3 | `telefono` | `character varying(80)` | Si | - |
| 4 | `identificacion` | `character varying(80)` | Si | - |
| 5 | `direccion` | `character varying(250)` | Si | - |
| 6 | `email` | `character varying(140)` | Si | - |
| 7 | `tipo` | `character varying(40)` | Si | - |
| 8 | `activo` | `boolean` | Si | - |
| 9 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `clientes_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `clientes_pkey`: `CREATE UNIQUE INDEX clientes_pkey ON public.clientes USING btree (id)`.
- `ix_clientes_id`: `CREATE INDEX ix_clientes_id ON public.clientes USING btree (id)`.
- `ix_clientes_identificacion`: `CREATE INDEX ix_clientes_identificacion ON public.clientes USING btree (identificacion)`.
- `ix_clientes_nombre`: `CREATE INDEX ix_clientes_nombre ON public.clientes USING btree (nombre)`.

#### `proveedores`

Catalogo de proveedores de mercaderia.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('proveedores_id_seq'::regclass)` |
| 2 | `nombre` | `character varying(160)` | No | - |
| 3 | `tipo` | `character varying(40)` | Si | - |
| 4 | `activo` | `boolean` | Si | - |
| 5 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `proveedores_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `proveedores_nombre_key`: `UNIQUE (nombre)`.

**Indices**

- `ix_proveedores_id`: `CREATE INDEX ix_proveedores_id ON public.proveedores USING btree (id)`.
- `proveedores_nombre_key`: `CREATE UNIQUE INDEX proveedores_nombre_key ON public.proveedores USING btree (nombre)`.
- `proveedores_pkey`: `CREATE UNIQUE INDEX proveedores_pkey ON public.proveedores USING btree (id)`.

### Catalogos de inventario

#### `lineas`

Lineas comerciales de productos.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('lineas_id_seq'::regclass)` |
| 2 | `cod_linea` | `character varying(50)` | No | - |
| 3 | `linea` | `character varying(120)` | No | - |
| 4 | `activo` | `boolean` | Si | - |
| 5 | `registro` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `lineas_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `lineas_cod_linea_key`: `UNIQUE (cod_linea)`.

**Indices**

- `ix_lineas_id`: `CREATE INDEX ix_lineas_id ON public.lineas USING btree (id)`.
- `lineas_cod_linea_key`: `CREATE UNIQUE INDEX lineas_cod_linea_key ON public.lineas USING btree (cod_linea)`.
- `lineas_pkey`: `CREATE UNIQUE INDEX lineas_pkey ON public.lineas USING btree (id)`.

#### `segmentos`

Segmentos o subclasificaciones de productos.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('segmentos_id_seq'::regclass)` |
| 2 | `segmento` | `character varying(120)` | No | - |
| 3 | `activo` | `boolean` | Si | - |
| 4 | `registro` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `segmentos_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `segmentos_segmento_key`: `UNIQUE (segmento)`.

**Indices**

- `ix_segmentos_id`: `CREATE INDEX ix_segmentos_id ON public.segmentos USING btree (id)`.
- `segmentos_pkey`: `CREATE UNIQUE INDEX segmentos_pkey ON public.segmentos USING btree (id)`.
- `segmentos_segmento_key`: `CREATE UNIQUE INDEX segmentos_segmento_key ON public.segmentos USING btree (segmento)`.

#### `unidades_medida`

Unidades utilizadas por productos y recetas.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('unidades_medida_id_seq'::regclass)` |
| 2 | `codigo` | `character varying(20)` | No | - |
| 3 | `nombre` | `character varying(80)` | No | - |
| 4 | `abreviatura` | `character varying(20)` | No | - |
| 5 | `activo` | `boolean` | Si | - |
| 6 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `unidades_medida_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `unidades_medida_codigo_key`: `UNIQUE (codigo)`.
- **UNIQUE** `unidades_medida_nombre_key`: `UNIQUE (nombre)`.

**Indices**

- `ix_unidades_medida_id`: `CREATE INDEX ix_unidades_medida_id ON public.unidades_medida USING btree (id)`.
- `unidades_medida_codigo_key`: `CREATE UNIQUE INDEX unidades_medida_codigo_key ON public.unidades_medida USING btree (codigo)`.
- `unidades_medida_nombre_key`: `CREATE UNIQUE INDEX unidades_medida_nombre_key ON public.unidades_medida USING btree (nombre)`.
- `unidades_medida_pkey`: `CREATE UNIQUE INDEX unidades_medida_pkey ON public.unidades_medida USING btree (id)`.

#### `marcas`

Catalogo de marcas.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('marcas_id_seq'::regclass)` |
| 2 | `nombre` | `character varying(120)` | No | - |
| 3 | `activo` | `boolean` | Si | - |
| 4 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `marcas_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `marcas_nombre_key`: `UNIQUE (nombre)`.

**Indices**

- `ix_marcas_id`: `CREATE INDEX ix_marcas_id ON public.marcas USING btree (id)`.
- `marcas_nombre_key`: `CREATE UNIQUE INDEX marcas_nombre_key ON public.marcas USING btree (nombre)`.
- `marcas_pkey`: `CREATE UNIQUE INDEX marcas_pkey ON public.marcas USING btree (id)`.

#### `bodegas`

Bodegas de inventario asociables a sucursales.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('bodegas_id_seq'::regclass)` |
| 2 | `code` | `character varying(40)` | No | - |
| 3 | `name` | `character varying(120)` | No | - |
| 4 | `sucursal_id` | `integer` | Si | - |
| 5 | `activo` | `boolean` | Si | - |
| 6 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `bodegas_sucursal_id_fkey`: `FOREIGN KEY (sucursal_id) REFERENCES sucursales(id)`.
- **PRIMARY KEY** `bodegas_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `bodegas_code_key`: `UNIQUE (code)`.

**Indices**

- `bodegas_code_key`: `CREATE UNIQUE INDEX bodegas_code_key ON public.bodegas USING btree (code)`.
- `bodegas_pkey`: `CREATE UNIQUE INDEX bodegas_pkey ON public.bodegas USING btree (id)`.
- `ix_bodegas_id`: `CREATE INDEX ix_bodegas_id ON public.bodegas USING btree (id)`.

#### `ingreso_tipos`

Conceptos de entrada de inventario.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('ingreso_tipos_id_seq'::regclass)` |
| 2 | `nombre` | `character varying(120)` | No | - |
| 3 | `requiere_proveedor` | `boolean` | Si | - |
| 4 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `ingreso_tipos_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `ingreso_tipos_nombre_key`: `UNIQUE (nombre)`.

**Indices**

- `ingreso_tipos_nombre_key`: `CREATE UNIQUE INDEX ingreso_tipos_nombre_key ON public.ingreso_tipos USING btree (nombre)`.
- `ingreso_tipos_pkey`: `CREATE UNIQUE INDEX ingreso_tipos_pkey ON public.ingreso_tipos USING btree (id)`.
- `ix_ingreso_tipos_id`: `CREATE INDEX ix_ingreso_tipos_id ON public.ingreso_tipos USING btree (id)`.

#### `egreso_tipos`

Conceptos de salida de inventario.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('egreso_tipos_id_seq'::regclass)` |
| 2 | `nombre` | `character varying(120)` | No | - |
| 3 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `egreso_tipos_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `egreso_tipos_nombre_key`: `UNIQUE (nombre)`.

**Indices**

- `egreso_tipos_nombre_key`: `CREATE UNIQUE INDEX egreso_tipos_nombre_key ON public.egreso_tipos USING btree (nombre)`.
- `egreso_tipos_pkey`: `CREATE UNIQUE INDEX egreso_tipos_pkey ON public.egreso_tipos USING btree (id)`.
- `ix_egreso_tipos_id`: `CREATE INDEX ix_egreso_tipos_id ON public.egreso_tipos USING btree (id)`.

### Productos, saldos, recetas y combos

#### `productos`

Maestro de productos, precios, costo y clasificacion.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('productos_id_seq'::regclass)` |
| 2 | `cod_producto` | `character varying(60)` | No | - |
| 3 | `usa_codigo_barra` | `boolean` | Si | - |
| 4 | `codigo_barra` | `character varying(120)` | Si | - |
| 5 | `descripcion` | `character varying(200)` | No | - |
| 6 | `segmento_id` | `integer` | Si | - |
| 7 | `linea_id` | `integer` | Si | - |
| 8 | `unidad_medida_id` | `integer` | Si | - |
| 9 | `marca_id` | `integer` | Si | - |
| 10 | `marca` | `character varying(80)` | Si | - |
| 11 | `presentacion` | `character varying(100)` | Si | - |
| 12 | `precio_venta1` | `numeric(12,2)` | Si | - |
| 13 | `precio_venta2` | `numeric(12,2)` | Si | - |
| 14 | `precio_venta3` | `numeric(12,2)` | Si | - |
| 15 | `activo` | `boolean` | Si | - |
| 16 | `servicio_producto` | `boolean` | Si | - |
| 17 | `es_por_peso` | `boolean` | Si | - |
| 18 | `costo_producto` | `numeric(12,2)` | Si | - |
| 19 | `referencia_producto` | `character varying(120)` | Si | - |
| 20 | `tipo_producto` | `character varying(30)` | No | - |
| 21 | `usuario_registro` | `character varying(80)` | Si | - |
| 22 | `maquina_registro` | `character varying(80)` | Si | - |
| 23 | `registro` | `timestamp without time zone` | Si | `now()` |
| 24 | `ultima_modificacion` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `productos_linea_id_fkey`: `FOREIGN KEY (linea_id) REFERENCES lineas(id)`.
- **FOREIGN KEY** `productos_marca_id_fkey`: `FOREIGN KEY (marca_id) REFERENCES marcas(id)`.
- **FOREIGN KEY** `productos_segmento_id_fkey`: `FOREIGN KEY (segmento_id) REFERENCES segmentos(id)`.
- **FOREIGN KEY** `productos_unidad_medida_id_fkey`: `FOREIGN KEY (unidad_medida_id) REFERENCES unidades_medida(id)`.
- **PRIMARY KEY** `productos_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `productos_cod_producto_key`: `UNIQUE (cod_producto)`.
- **UNIQUE** `productos_codigo_barra_key`: `UNIQUE (codigo_barra)`.

**Indices**

- `ix_productos_codigo_barra`: `CREATE UNIQUE INDEX ix_productos_codigo_barra ON public.productos USING btree (codigo_barra) WHERE (codigo_barra IS NOT NULL)`.
- `ix_productos_id`: `CREATE INDEX ix_productos_id ON public.productos USING btree (id)`.
- `productos_cod_producto_key`: `CREATE UNIQUE INDEX productos_cod_producto_key ON public.productos USING btree (cod_producto)`.
- `productos_codigo_barra_key`: `CREATE UNIQUE INDEX productos_codigo_barra_key ON public.productos USING btree (codigo_barra)`.
- `productos_pkey`: `CREATE UNIQUE INDEX productos_pkey ON public.productos USING btree (id)`.

#### `saldos_productos`

Saldo global materializado por producto.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('saldos_productos_id_seq'::regclass)` |
| 2 | `producto_id` | `integer` | No | - |
| 3 | `existencia` | `numeric(14,2)` | Si | - |

**Restricciones**

- **FOREIGN KEY** `saldos_productos_producto_id_fkey`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `saldos_productos_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `saldos_productos_producto_id_key`: `UNIQUE (producto_id)`.

**Indices**

- `ix_saldos_productos_id`: `CREATE INDEX ix_saldos_productos_id ON public.saldos_productos USING btree (id)`.
- `saldos_productos_pkey`: `CREATE UNIQUE INDEX saldos_productos_pkey ON public.saldos_productos USING btree (id)`.
- `saldos_productos_producto_id_key`: `CREATE UNIQUE INDEX saldos_productos_producto_id_key ON public.saldos_productos USING btree (producto_id)`.

#### `productos_recetas`

Cabecera de receta de un producto final.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('productos_recetas_id_seq'::regclass)` |
| 2 | `producto_final_id` | `integer` | No | - |
| 3 | `nombre` | `character varying(160)` | Si | - |
| 4 | `activo` | `boolean` | Si | - |
| 5 | `created_at` | `timestamp without time zone` | Si | `now()` |
| 6 | `updated_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `productos_recetas_producto_final_id_fkey`: `FOREIGN KEY (producto_final_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `productos_recetas_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `productos_recetas_producto_final_id_key`: `UNIQUE (producto_final_id)`.

**Indices**

- `ix_productos_recetas_id`: `CREATE INDEX ix_productos_recetas_id ON public.productos_recetas USING btree (id)`.
- `productos_recetas_pkey`: `CREATE UNIQUE INDEX productos_recetas_pkey ON public.productos_recetas USING btree (id)`.
- `productos_recetas_producto_final_id_key`: `CREATE UNIQUE INDEX productos_recetas_producto_final_id_key ON public.productos_recetas USING btree (producto_final_id)`.

#### `productos_receta_lineas`

Insumos y cantidades requeridas por receta.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('productos_receta_lineas_id_seq'::regclass)` |
| 2 | `receta_id` | `integer` | No | - |
| 3 | `insumo_producto_id` | `integer` | No | - |
| 4 | `unidad_medida_id` | `integer` | Si | - |
| 5 | `cantidad` | `numeric(14,4)` | No | - |
| 6 | `created_at` | `timestamp without time zone` | Si | `now()` |
| 7 | `updated_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `productos_receta_lineas_insumo_producto_id_fkey`: `FOREIGN KEY (insumo_producto_id) REFERENCES productos(id)`.
- **FOREIGN KEY** `productos_receta_lineas_receta_id_fkey`: `FOREIGN KEY (receta_id) REFERENCES productos_recetas(id)`.
- **FOREIGN KEY** `productos_receta_lineas_unidad_medida_id_fkey`: `FOREIGN KEY (unidad_medida_id) REFERENCES unidades_medida(id)`.
- **PRIMARY KEY** `productos_receta_lineas_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `uq_producto_receta_insumo`: `UNIQUE (receta_id, insumo_producto_id)`.

**Indices**

- `ix_productos_receta_lineas_id`: `CREATE INDEX ix_productos_receta_lineas_id ON public.productos_receta_lineas USING btree (id)`.
- `productos_receta_lineas_pkey`: `CREATE UNIQUE INDEX productos_receta_lineas_pkey ON public.productos_receta_lineas USING btree (id)`.
- `uq_producto_receta_insumo`: `CREATE UNIQUE INDEX uq_producto_receta_insumo ON public.productos_receta_lineas USING btree (receta_id, insumo_producto_id)`.

#### `producto_combos`

Composicion de combos: principal e incluidos/regalias.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('producto_combos_id_seq'::regclass)` |
| 2 | `parent_producto_id` | `integer` | No | - |
| 3 | `child_producto_id` | `integer` | No | - |
| 4 | `cantidad` | `numeric(12,2)` | Si | - |
| 5 | `activo` | `boolean` | Si | - |
| 6 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `producto_combos_child_producto_id_fkey`: `FOREIGN KEY (child_producto_id) REFERENCES productos(id)`.
- **FOREIGN KEY** `producto_combos_parent_producto_id_fkey`: `FOREIGN KEY (parent_producto_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `producto_combos_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `uq_producto_combo_child`: `UNIQUE (parent_producto_id, child_producto_id)`.

**Indices**

- `ix_producto_combos_id`: `CREATE INDEX ix_producto_combos_id ON public.producto_combos USING btree (id)`.
- `producto_combos_pkey`: `CREATE UNIQUE INDEX producto_combos_pkey ON public.producto_combos USING btree (id)`.
- `uq_producto_combo_child`: `CREATE UNIQUE INDEX uq_producto_combo_child ON public.producto_combos USING btree (parent_producto_id, child_producto_id)`.
- `uq_producto_combo_child_idx`: `CREATE UNIQUE INDEX uq_producto_combo_child_idx ON public.producto_combos USING btree (parent_producto_id, child_producto_id)`.

### Movimientos de inventario

#### `ingresos_inventario`

Cabecera documental de entradas de inventario.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('ingresos_inventario_id_seq'::regclass)` |
| 2 | `tipo_id` | `integer` | No | - |
| 3 | `bodega_id` | `integer` | No | - |
| 4 | `proveedor_id` | `integer` | Si | - |
| 5 | `usuario_id` | `integer` | Si | - |
| 6 | `fecha` | `date` | No | - |
| 7 | `moneda` | `character varying(10)` | No | - |
| 8 | `tasa_cambio` | `numeric(12,4)` | Si | - |
| 9 | `total_usd` | `numeric(14,2)` | Si | - |
| 10 | `total_cs` | `numeric(14,2)` | Si | - |
| 11 | `observacion` | `character varying(300)` | Si | - |
| 12 | `usuario_registro` | `character varying(120)` | Si | - |
| 13 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `ingresos_inventario_bodega_id_fkey`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`.
- **FOREIGN KEY** `ingresos_inventario_proveedor_id_fkey`: `FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)`.
- **FOREIGN KEY** `ingresos_inventario_tipo_id_fkey`: `FOREIGN KEY (tipo_id) REFERENCES ingreso_tipos(id)`.
- **FOREIGN KEY** `ingresos_inventario_usuario_id_fkey`: `FOREIGN KEY (usuario_id) REFERENCES users(id)`.
- **PRIMARY KEY** `ingresos_inventario_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ingresos_inventario_pkey`: `CREATE UNIQUE INDEX ingresos_inventario_pkey ON public.ingresos_inventario USING btree (id)`.
- `ix_ingresos_inventario_id`: `CREATE INDEX ix_ingresos_inventario_id ON public.ingresos_inventario USING btree (id)`.

#### `ingreso_items`

Productos y costos de cada ingreso.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('ingreso_items_id_seq'::regclass)` |
| 2 | `ingreso_id` | `integer` | No | - |
| 3 | `producto_id` | `integer` | No | - |
| 4 | `cantidad` | `numeric(14,2)` | Si | - |
| 5 | `costo_unitario_usd` | `numeric(14,2)` | Si | - |
| 6 | `costo_unitario_cs` | `numeric(14,2)` | Si | - |
| 7 | `subtotal_usd` | `numeric(14,2)` | Si | - |
| 8 | `subtotal_cs` | `numeric(14,2)` | Si | - |

**Restricciones**

- **FOREIGN KEY** `ingreso_items_ingreso_id_fkey`: `FOREIGN KEY (ingreso_id) REFERENCES ingresos_inventario(id)`.
- **FOREIGN KEY** `ingreso_items_producto_id_fkey`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `ingreso_items_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ingreso_items_pkey`: `CREATE UNIQUE INDEX ingreso_items_pkey ON public.ingreso_items USING btree (id)`.
- `ix_ingreso_items_id`: `CREATE INDEX ix_ingreso_items_id ON public.ingreso_items USING btree (id)`.

#### `egresos_inventario`

Cabecera documental de salidas y traslados.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('egresos_inventario_id_seq'::regclass)` |
| 2 | `tipo_id` | `integer` | No | - |
| 3 | `bodega_id` | `integer` | No | - |
| 4 | `bodega_destino_id` | `integer` | Si | - |
| 5 | `usuario_id` | `integer` | Si | - |
| 6 | `fecha` | `date` | No | - |
| 7 | `moneda` | `character varying(10)` | No | - |
| 8 | `tasa_cambio` | `numeric(12,4)` | Si | - |
| 9 | `total_usd` | `numeric(14,2)` | Si | - |
| 10 | `total_cs` | `numeric(14,2)` | Si | - |
| 11 | `observacion` | `character varying(300)` | Si | - |
| 12 | `usuario_registro` | `character varying(120)` | Si | - |
| 13 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `egresos_inventario_bodega_destino_id_fkey`: `FOREIGN KEY (bodega_destino_id) REFERENCES bodegas(id)`.
- **FOREIGN KEY** `egresos_inventario_bodega_id_fkey`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`.
- **FOREIGN KEY** `egresos_inventario_tipo_id_fkey`: `FOREIGN KEY (tipo_id) REFERENCES egreso_tipos(id)`.
- **FOREIGN KEY** `egresos_inventario_usuario_id_fkey`: `FOREIGN KEY (usuario_id) REFERENCES users(id)`.
- **PRIMARY KEY** `egresos_inventario_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `egresos_inventario_pkey`: `CREATE UNIQUE INDEX egresos_inventario_pkey ON public.egresos_inventario USING btree (id)`.
- `ix_egresos_inventario_id`: `CREATE INDEX ix_egresos_inventario_id ON public.egresos_inventario USING btree (id)`.

#### `egreso_items`

Productos y costos de cada egreso.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('egreso_items_id_seq'::regclass)` |
| 2 | `egreso_id` | `integer` | No | - |
| 3 | `producto_id` | `integer` | No | - |
| 4 | `cantidad` | `numeric(14,2)` | Si | - |
| 5 | `costo_unitario_usd` | `numeric(14,2)` | Si | - |
| 6 | `costo_unitario_cs` | `numeric(14,2)` | Si | - |
| 7 | `subtotal_usd` | `numeric(14,2)` | Si | - |
| 8 | `subtotal_cs` | `numeric(14,2)` | Si | - |

**Restricciones**

- **FOREIGN KEY** `egreso_items_egreso_id_fkey`: `FOREIGN KEY (egreso_id) REFERENCES egresos_inventario(id)`.
- **FOREIGN KEY** `egreso_items_producto_id_fkey`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `egreso_items_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `egreso_items_pkey`: `CREATE UNIQUE INDEX egreso_items_pkey ON public.egreso_items USING btree (id)`.
- `ix_egreso_items_id`: `CREATE INDEX ix_egreso_items_id ON public.egreso_items USING btree (id)`.

### Produccion y apertura de pacas

#### `producciones_inventario`

Ordenes generales de produccion.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('producciones_inventario_id_seq'::regclass)` |
| 2 | `producto_final_id` | `integer` | No | - |
| 3 | `bodega_id` | `integer` | No | - |
| 4 | `fecha` | `date` | No | - |
| 5 | `estado` | `character varying(20)` | No | - |
| 6 | `moneda` | `character varying(10)` | No | - |
| 7 | `tasa_cambio` | `numeric(12,4)` | Si | - |
| 8 | `cantidad_producida` | `numeric(14,4)` | No | - |
| 9 | `total_insumos_usd` | `numeric(14,2)` | Si | - |
| 10 | `total_insumos_cs` | `numeric(14,2)` | Si | - |
| 11 | `total_produccion_usd` | `numeric(14,2)` | Si | - |
| 12 | `total_produccion_cs` | `numeric(14,2)` | Si | - |
| 13 | `observacion` | `character varying(300)` | Si | - |
| 14 | `usuario_registro` | `character varying(120)` | Si | - |
| 15 | `ingreso_id` | `integer` | Si | - |
| 16 | `egreso_id` | `integer` | Si | - |
| 17 | `created_at` | `timestamp without time zone` | Si | `now()` |
| 18 | `updated_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `producciones_inventario_bodega_id_fkey`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`.
- **FOREIGN KEY** `producciones_inventario_egreso_id_fkey`: `FOREIGN KEY (egreso_id) REFERENCES egresos_inventario(id)`.
- **FOREIGN KEY** `producciones_inventario_ingreso_id_fkey`: `FOREIGN KEY (ingreso_id) REFERENCES ingresos_inventario(id)`.
- **FOREIGN KEY** `producciones_inventario_producto_final_id_fkey`: `FOREIGN KEY (producto_final_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `producciones_inventario_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ix_producciones_inventario_id`: `CREATE INDEX ix_producciones_inventario_id ON public.producciones_inventario USING btree (id)`.
- `producciones_inventario_pkey`: `CREATE UNIQUE INDEX producciones_inventario_pkey ON public.producciones_inventario USING btree (id)`.

#### `producciones_inventario_lineas`

Insumos y resultados de una produccion.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('producciones_inventario_lineas_id_seq'::regclass)` |
| 2 | `produccion_id` | `integer` | No | - |
| 3 | `tipo_linea` | `character varying(20)` | No | - |
| 4 | `producto_id` | `integer` | No | - |
| 5 | `cantidad` | `numeric(14,4)` | No | - |
| 6 | `costo_unitario_usd` | `numeric(14,2)` | Si | - |
| 7 | `costo_unitario_cs` | `numeric(14,2)` | Si | - |
| 8 | `subtotal_usd` | `numeric(14,2)` | Si | - |
| 9 | `subtotal_cs` | `numeric(14,2)` | Si | - |

**Restricciones**

- **FOREIGN KEY** `producciones_inventario_lineas_produccion_id_fkey`: `FOREIGN KEY (produccion_id) REFERENCES producciones_inventario(id)`.
- **FOREIGN KEY** `producciones_inventario_lineas_producto_id_fkey`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `producciones_inventario_lineas_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ix_producciones_inventario_lineas_id`: `CREATE INDEX ix_producciones_inventario_lineas_id ON public.producciones_inventario_lineas USING btree (id)`.
- `producciones_inventario_lineas_pkey`: `CREATE UNIQUE INDEX producciones_inventario_lineas_pkey ON public.producciones_inventario_lineas USING btree (id)`.

#### `paca_aperturas`

Cabecera de apertura y clasificacion de pacas.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('paca_aperturas_id_seq'::regclass)` |
| 2 | `paca_producto_id` | `integer` | No | - |
| 3 | `bodega_id` | `integer` | No | - |
| 4 | `bodega_destino_id` | `integer` | Si | - |
| 5 | `fecha` | `date` | No | - |
| 6 | `cantidad_pacas` | `numeric(14,4)` | No | - |
| 7 | `moneda` | `character varying(10)` | No | - |
| 8 | `tasa_cambio` | `numeric(12,4)` | Si | - |
| 9 | `costo_origen_usd` | `numeric(14,2)` | Si | - |
| 10 | `costo_origen_cs` | `numeric(14,2)` | Si | - |
| 11 | `valor_estimado_usd` | `numeric(14,2)` | Si | - |
| 12 | `valor_estimado_cs` | `numeric(14,2)` | Si | - |
| 13 | `diferencia_usd` | `numeric(14,2)` | Si | - |
| 14 | `diferencia_cs` | `numeric(14,2)` | Si | - |
| 15 | `estado` | `character varying(20)` | No | - |
| 16 | `observacion` | `character varying(300)` | Si | - |
| 17 | `usuario_registro` | `character varying(120)` | Si | - |
| 18 | `ingreso_id` | `integer` | Si | - |
| 19 | `egreso_id` | `integer` | Si | - |
| 20 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `paca_aperturas_bodega_destino_id_fkey`: `FOREIGN KEY (bodega_destino_id) REFERENCES bodegas(id)`.
- **FOREIGN KEY** `paca_aperturas_bodega_id_fkey`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`.
- **FOREIGN KEY** `paca_aperturas_egreso_id_fkey`: `FOREIGN KEY (egreso_id) REFERENCES egresos_inventario(id)`.
- **FOREIGN KEY** `paca_aperturas_ingreso_id_fkey`: `FOREIGN KEY (ingreso_id) REFERENCES ingresos_inventario(id)`.
- **FOREIGN KEY** `paca_aperturas_paca_producto_id_fkey`: `FOREIGN KEY (paca_producto_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `paca_aperturas_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ix_paca_aperturas_id`: `CREATE INDEX ix_paca_aperturas_id ON public.paca_aperturas USING btree (id)`.
- `paca_aperturas_pkey`: `CREATE UNIQUE INDEX paca_aperturas_pkey ON public.paca_aperturas USING btree (id)`.

#### `paca_apertura_origenes`

Pacas o productos origen consumidos.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('paca_apertura_origenes_id_seq'::regclass)` |
| 2 | `apertura_id` | `integer` | No | - |
| 3 | `producto_id` | `integer` | No | - |
| 4 | `cantidad` | `numeric(14,4)` | No | - |
| 5 | `costo_unitario_usd` | `numeric(14,2)` | Si | - |
| 6 | `costo_unitario_cs` | `numeric(14,2)` | Si | - |
| 7 | `subtotal_usd` | `numeric(14,2)` | Si | - |
| 8 | `subtotal_cs` | `numeric(14,2)` | Si | - |

**Restricciones**

- **FOREIGN KEY** `paca_apertura_origenes_apertura_id_fkey`: `FOREIGN KEY (apertura_id) REFERENCES paca_aperturas(id)`.
- **FOREIGN KEY** `paca_apertura_origenes_producto_id_fkey`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `paca_apertura_origenes_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ix_paca_apertura_origenes_id`: `CREATE INDEX ix_paca_apertura_origenes_id ON public.paca_apertura_origenes USING btree (id)`.
- `paca_apertura_origenes_pkey`: `CREATE UNIQUE INDEX paca_apertura_origenes_pkey ON public.paca_apertura_origenes USING btree (id)`.

#### `paca_apertura_lineas`

Productos clasificados, valor y costo asignado.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('paca_apertura_lineas_id_seq'::regclass)` |
| 2 | `apertura_id` | `integer` | No | - |
| 3 | `producto_id` | `integer` | No | - |
| 4 | `cantidad` | `numeric(14,4)` | No | - |
| 5 | `precio_estimado_unitario_usd` | `numeric(14,2)` | Si | - |
| 6 | `precio_estimado_unitario_cs` | `numeric(14,2)` | Si | - |
| 7 | `valor_estimado_usd` | `numeric(14,2)` | Si | - |
| 8 | `valor_estimado_cs` | `numeric(14,2)` | Si | - |
| 9 | `costo_asignado_unitario_usd` | `numeric(14,2)` | Si | - |
| 10 | `costo_asignado_unitario_cs` | `numeric(14,2)` | Si | - |
| 11 | `costo_asignado_usd` | `numeric(14,2)` | Si | - |
| 12 | `costo_asignado_cs` | `numeric(14,2)` | Si | - |

**Restricciones**

- **FOREIGN KEY** `paca_apertura_lineas_apertura_id_fkey`: `FOREIGN KEY (apertura_id) REFERENCES paca_aperturas(id)`.
- **FOREIGN KEY** `paca_apertura_lineas_producto_id_fkey`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `paca_apertura_lineas_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ix_paca_apertura_lineas_id`: `CREATE INDEX ix_paca_apertura_lineas_id ON public.paca_apertura_lineas USING btree (id)`.
- `paca_apertura_lineas_pkey`: `CREATE UNIQUE INDEX paca_apertura_lineas_pkey ON public.paca_apertura_lineas USING btree (id)`.

### Ventas y facturacion POS

#### `sales_invoices`

Cabecera de factura POS y totales financieros.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('sales_invoices_id_seq'::regclass)` |
| 2 | `invoice_number` | `character varying(40)` | No | - |
| 3 | `customer_name` | `character varying(180)` | No | - |
| 4 | `customer_phone` | `character varying(80)` | Si | - |
| 5 | `customer_document` | `character varying(80)` | Si | - |
| 6 | `customer_address` | `character varying(250)` | Si | - |
| 7 | `vendor_name` | `character varying(160)` | Si | - |
| 8 | `bodega_id` | `integer` | No | - |
| 9 | `egreso_id` | `integer` | Si | - |
| 10 | `fecha` | `date` | No | - |
| 11 | `condicion` | `character varying(20)` | No | - |
| 12 | `moneda` | `character varying(10)` | No | - |
| 13 | `tasa_cambio` | `numeric(12,4)` | Si | - |
| 14 | `subtotal_usd` | `numeric(14,2)` | Si | - |
| 15 | `subtotal_cs` | `numeric(14,2)` | Si | - |
| 16 | `total_usd` | `numeric(14,2)` | Si | - |
| 17 | `total_cs` | `numeric(14,2)` | Si | - |
| 18 | `paid_usd` | `numeric(14,2)` | Si | - |
| 19 | `paid_cs` | `numeric(14,2)` | Si | - |
| 20 | `balance_usd` | `numeric(14,2)` | Si | - |
| 21 | `balance_cs` | `numeric(14,2)` | Si | - |
| 22 | `change_usd` | `numeric(14,2)` | Si | - |
| 23 | `change_cs` | `numeric(14,2)` | Si | - |
| 24 | `status` | `character varying(20)` | No | - |
| 25 | `observacion` | `text` | Si | - |
| 26 | `usuario_registro` | `character varying(120)` | Si | - |
| 27 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `sales_invoices_bodega_id_fkey`: `FOREIGN KEY (bodega_id) REFERENCES bodegas(id)`.
- **FOREIGN KEY** `sales_invoices_egreso_id_fkey`: `FOREIGN KEY (egreso_id) REFERENCES egresos_inventario(id)`.
- **PRIMARY KEY** `sales_invoices_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ix_sales_invoices_id`: `CREATE INDEX ix_sales_invoices_id ON public.sales_invoices USING btree (id)`.
- `ix_sales_invoices_invoice_number`: `CREATE UNIQUE INDEX ix_sales_invoices_invoice_number ON public.sales_invoices USING btree (invoice_number)`.
- `sales_invoices_pkey`: `CREATE UNIQUE INDEX sales_invoices_pkey ON public.sales_invoices USING btree (id)`.

#### `sales_invoice_items`

Detalle historico facturado, incluidos combos.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('sales_invoice_items_id_seq'::regclass)` |
| 2 | `invoice_id` | `integer` | No | - |
| 3 | `producto_id` | `integer` | No | - |
| 4 | `cod_producto` | `character varying(60)` | No | - |
| 5 | `descripcion` | `character varying(220)` | No | - |
| 6 | `unidad` | `character varying(30)` | Si | - |
| 7 | `cantidad` | `numeric(14,4)` | No | - |
| 8 | `precio_unitario_usd` | `numeric(14,2)` | Si | - |
| 9 | `precio_unitario_cs` | `numeric(14,2)` | Si | - |
| 10 | `subtotal_usd` | `numeric(14,2)` | Si | - |
| 11 | `subtotal_cs` | `numeric(14,2)` | Si | - |
| 12 | `combo_role` | `character varying(20)` | Si | - |
| 13 | `combo_group` | `character varying(60)` | Si | - |

**Restricciones**

- **FOREIGN KEY** `sales_invoice_items_invoice_id_fkey`: `FOREIGN KEY (invoice_id) REFERENCES sales_invoices(id)`.
- **FOREIGN KEY** `sales_invoice_items_producto_id_fkey`: `FOREIGN KEY (producto_id) REFERENCES productos(id)`.
- **PRIMARY KEY** `sales_invoice_items_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ix_sales_invoice_items_id`: `CREATE INDEX ix_sales_invoice_items_id ON public.sales_invoice_items USING btree (id)`.
- `sales_invoice_items_pkey`: `CREATE UNIQUE INDEX sales_invoice_items_pkey ON public.sales_invoice_items USING btree (id)`.

#### `sales_payments`

Pagos aplicados a facturas POS.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('sales_payments_id_seq'::regclass)` |
| 2 | `invoice_id` | `integer` | No | - |
| 3 | `forma_codigo` | `character varying(40)` | No | - |
| 4 | `forma_nombre` | `character varying(100)` | No | - |
| 5 | `moneda` | `character varying(10)` | No | - |
| 6 | `monto` | `numeric(14,2)` | No | - |
| 7 | `monto_usd` | `numeric(14,2)` | Si | - |
| 8 | `monto_cs` | `numeric(14,2)` | Si | - |
| 9 | `banco` | `character varying(120)` | Si | - |
| 10 | `cuenta` | `character varying(120)` | Si | - |
| 11 | `referencia` | `character varying(120)` | Si | - |
| 12 | `created_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **FOREIGN KEY** `sales_payments_invoice_id_fkey`: `FOREIGN KEY (invoice_id) REFERENCES sales_invoices(id)`.
- **PRIMARY KEY** `sales_payments_pkey`: `PRIMARY KEY (id)`.

**Indices**

- `ix_sales_payments_id`: `CREATE INDEX ix_sales_payments_id ON public.sales_payments USING btree (id)`.
- `sales_payments_pkey`: `CREATE UNIQUE INDEX sales_payments_pkey ON public.sales_payments USING btree (id)`.

#### `sales_sequences`

Consecutivos de numeracion de facturas.

| # | Columna | Tipo PostgreSQL | Nulo | Predeterminado |
| ---: | --- | --- | :---: | --- |
| 1 | `id` | `integer` | No | `nextval('sales_sequences_id_seq'::regclass)` |
| 2 | `prefix` | `character varying(20)` | No | - |
| 3 | `current_value` | `integer` | No | - |
| 4 | `is_active` | `boolean` | Si | - |
| 5 | `updated_at` | `timestamp without time zone` | Si | `now()` |

**Restricciones**

- **PRIMARY KEY** `sales_sequences_pkey`: `PRIMARY KEY (id)`.
- **UNIQUE** `uq_sales_sequences_prefix`: `UNIQUE (prefix)`.

**Indices**

- `ix_sales_sequences_id`: `CREATE INDEX ix_sales_sequences_id ON public.sales_sequences USING btree (id)`.
- `sales_sequences_pkey`: `CREATE UNIQUE INDEX sales_sequences_pkey ON public.sales_sequences USING btree (id)`.
- `uq_sales_sequences_prefix`: `CREATE UNIQUE INDEX uq_sales_sequences_prefix ON public.sales_sequences USING btree (prefix)`.

## Relaciones funcionales principales

- `users` se relaciona N:N con `roles` mediante `user_roles`.
- `user_access_profiles` limita la operacion de un usuario por sucursal,
  bodega y capacidades.
- `vendedores` puede vincular usuario, sucursal y bodega.
- Una sucursal puede agrupar varias bodegas.
- Un producto puede pertenecer a linea, segmento, unidad y marca.
- `saldos_productos` mantiene el saldo global 1:1 del producto.
- Una receta pertenece a un producto final y contiene varios insumos.
- Un combo relaciona un producto principal con productos incluidos.
- Ingresos y egresos usan estructura cabecera-detalle.
- Un traslado genera salida en origen y entrada en destino.
- Una produccion consume insumos y genera producto final.
- Una apertura consume una o varias pacas y genera productos clasificados.
- Una factura POS referencia bodega, egreso de inventario, items y pagos.
- `combo_role` y `combo_group` preservan la agrupacion historica del combo.

## Observaciones de integridad

1. Las reglas `ON DELETE` y `ON UPDATE` aparecen en las definiciones FK.
2. La existencia por bodega no se almacena en una tabla independiente; se
   calcula desde movimientos.
3. `saldos_productos` debe sincronizarse mediante la reconstruccion de saldo
   del backend.
4. Precios, costos, cantidades, subtotales y tasas usan `numeric`.
5. `sales_invoice_items` conserva codigo, descripcion y unidad historicos.
6. `paca_apertura_lineas` conserva valor estimado y costo asignado para
   evaluar rendimiento, ganancia o perdida.
7. Aun no existen tablas formales para caja, aperturas/cierres de caja, bancos,
   cuentas bancarias, pedidos, entregas o cobranza.
8. Se recomiendan indices compuestos por producto, bodega y fecha para kardex y
   reportes de alto volumen.

## Verificacion y conexion

```powershell
docker compose exec -T db psql -U user -d ERPDB -c "\dt public.*"
```

```text
Host: localhost
Puerto: 5433
Base: ERPDB
Usuario: user
Contrasena: 1234
Esquema: public
```
