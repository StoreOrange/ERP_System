# Base de datos ERP System

Ultima verificacion directa: 2026-06-02

Motor local verificado: PostgreSQL 16, base `ERPDB`.

## Resumen

- Tablas fisicas: 24, incluyendo `alembic_version`.
- Tablas funcionales: 23.
- Claves foraneas: 29.
- Indices registrados: 63.
- Migracion Alembic versionada: `5285f6b056a5`.

## Advertencia de migraciones

Alembic solo contiene la migracion inicial de usuarios y roles. Las tablas de
inventario, recetas, produccion y configuracion se crean actualmente mediante
`Base.metadata.create_all()` y varios `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`
ejecutados al iniciar el backend.

Antes de produccion se debe crear una migracion Alembic consolidada y eliminar
la dependencia de cambios de esquema durante el arranque.

## Tablas de control y seguridad

### `alembic_version`

Control interno de Alembic.

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `version_num` | `varchar` | PK |

### `roles`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `name` | `varchar(50)` | unico, requerido |

### `users`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `full_name` | `varchar(100)` | opcional |
| `email` | `varchar(120)` | unico, requerido |
| `hashed_password` | `varchar` | requerido |
| `is_active` | `boolean` | estado de acceso |

### `user_roles`

Relacion N:N entre usuarios y roles.

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `user_id` | `integer` | FK `users.id`, cascade al eliminar |
| `role_id` | `integer` | FK `roles.id`, cascade al eliminar |

## Catalogos de inventario

### `lineas`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `cod_linea` | `varchar(50)` | unico, requerido |
| `linea` | `varchar(120)` | requerido |
| `activo` | `boolean` | activo/inactivo |
| `registro` | `timestamp` | default `now()` |

### `segmentos`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `segmento` | `varchar(120)` | unico, requerido |
| `activo` | `boolean` | activo/inactivo |
| `registro` | `timestamp` | default `now()` |

### `unidades_medida`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `codigo` | `varchar(20)` | unico, requerido |
| `nombre` | `varchar(80)` | unico, requerido |
| `abreviatura` | `varchar(20)` | requerido |
| `activo` | `boolean` | activo/inactivo |
| `created_at` | `timestamp` | default `now()` |

### `marcas`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `nombre` | `varchar(120)` | unico, requerido |
| `activo` | `boolean` | activo/inactivo |
| `created_at` | `timestamp` | default `now()` |

### `bodegas`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `code` | `varchar(40)` | unico, requerido |
| `name` | `varchar(120)` | requerido |
| `activo` | `boolean` | activo/inactivo |
| `created_at` | `timestamp` | default `now()` |

### `proveedores`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `nombre` | `varchar(160)` | unico, requerido |
| `tipo` | `varchar(40)` | opcional |
| `activo` | `boolean` | activo/inactivo |
| `created_at` | `timestamp` | default `now()` |

### `ingreso_tipos`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `nombre` | `varchar(120)` | unico, requerido |
| `requiere_proveedor` | `boolean` | controla validacion |
| `created_at` | `timestamp` | default `now()` |

### `egreso_tipos`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `nombre` | `varchar(120)` | unico, requerido |
| `created_at` | `timestamp` | default `now()` |

## Productos, existencias y recetas

### `productos`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `cod_producto` | `varchar(60)` | unico, requerido |
| `usa_codigo_barra` | `boolean` | default `false` |
| `codigo_barra` | `varchar(120)` | unico si existe |
| `descripcion` | `varchar(200)` | requerido |
| `segmento_id` | `integer` | FK `segmentos.id` |
| `linea_id` | `integer` | FK `lineas.id` |
| `unidad_medida_id` | `integer` | FK `unidades_medida.id` |
| `marca_id` | `integer` | FK `marcas.id` |
| `marca` | `varchar(80)` | campo legado opcional |
| `presentacion` | `varchar(100)` | opcional |
| `precio_venta1` | `numeric(12,2)` | lista de precio 1 |
| `precio_venta2` | `numeric(12,2)` | lista de precio 2 |
| `precio_venta3` | `numeric(12,2)` | lista de precio 3 |
| `activo` | `boolean` | activo/inactivo |
| `servicio_producto` | `boolean` | servicio o producto |
| `es_por_peso` | `boolean` | venta o inventario pesado |
| `costo_producto` | `numeric(12,2)` | costo segun configuracion |
| `referencia_producto` | `varchar(120)` | opcional |
| `tipo_producto` | `varchar(30)` | `DIRECTO` o `RECETA` |
| `usuario_registro` | `varchar(80)` | auditoria |
| `maquina_registro` | `varchar(80)` | auditoria |
| `registro` | `timestamp` | default `now()` |
| `ultima_modificacion` | `timestamp` | actualizacion automatica ORM |

### `saldos_productos`

Saldo global reconstruido desde movimientos.

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `producto_id` | `integer` | FK `productos.id`, unico |
| `existencia` | `numeric(14,2)` | saldo global |

### `productos_recetas`

Cabecera unica de receta por producto final.

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `producto_final_id` | `integer` | FK `productos.id`, unico |
| `nombre` | `varchar(160)` | opcional |
| `activo` | `boolean` | activo/inactivo |
| `created_at` | `timestamp` | default `now()` |
| `updated_at` | `timestamp` | actualizacion ORM |

### `productos_receta_lineas`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `receta_id` | `integer` | FK `productos_recetas.id` |
| `insumo_producto_id` | `integer` | FK `productos.id` |
| `unidad_medida_id` | `integer` | FK `unidades_medida.id` |
| `cantidad` | `numeric(14,4)` | requerido |
| `created_at` | `timestamp` | default `now()` |
| `updated_at` | `timestamp` | actualizacion ORM |

Restriccion unica: `(receta_id, insumo_producto_id)`.

## Movimientos de inventario

### `ingresos_inventario`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `tipo_id` | `integer` | FK `ingreso_tipos.id` |
| `bodega_id` | `integer` | FK `bodegas.id` |
| `proveedor_id` | `integer` | FK `proveedores.id`, opcional |
| `usuario_id` | `integer` | FK `users.id`, opcional |
| `fecha` | `date` | requerido |
| `moneda` | `varchar(10)` | `USD` o `CS` |
| `tasa_cambio` | `numeric(12,4)` | requerida para USD |
| `total_usd` | `numeric(14,2)` | total calculado |
| `total_cs` | `numeric(14,2)` | total calculado |
| `observacion` | `varchar(300)` | opcional |
| `usuario_registro` | `varchar(120)` | auditoria |
| `created_at` | `timestamp` | default `now()` |

### `ingreso_items`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `ingreso_id` | `integer` | FK `ingresos_inventario.id` |
| `producto_id` | `integer` | FK `productos.id` |
| `cantidad` | `numeric(14,2)` | cantidad ingresada |
| `costo_unitario_usd` | `numeric(14,2)` | costo normalizado |
| `costo_unitario_cs` | `numeric(14,2)` | costo normalizado |
| `subtotal_usd` | `numeric(14,2)` | calculado |
| `subtotal_cs` | `numeric(14,2)` | calculado |

### `egresos_inventario`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `tipo_id` | `integer` | FK `egreso_tipos.id` |
| `bodega_id` | `integer` | FK `bodegas.id` origen |
| `bodega_destino_id` | `integer` | FK `bodegas.id`, opcional |
| `usuario_id` | `integer` | FK `users.id`, opcional |
| `fecha` | `date` | requerido |
| `moneda` | `varchar(10)` | `USD` o `CS` |
| `tasa_cambio` | `numeric(12,4)` | requerida para USD |
| `total_usd` | `numeric(14,2)` | total calculado |
| `total_cs` | `numeric(14,2)` | total calculado |
| `observacion` | `varchar(300)` | opcional |
| `usuario_registro` | `varchar(120)` | auditoria |
| `created_at` | `timestamp` | default `now()` |

### `egreso_items`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `egreso_id` | `integer` | FK `egresos_inventario.id` |
| `producto_id` | `integer` | FK `productos.id` |
| `cantidad` | `numeric(14,2)` | cantidad egresada |
| `costo_unitario_usd` | `numeric(14,2)` | costo normalizado |
| `costo_unitario_cs` | `numeric(14,2)` | costo normalizado |
| `subtotal_usd` | `numeric(14,2)` | calculado |
| `subtotal_cs` | `numeric(14,2)` | calculado |

## Produccion

### `producciones_inventario`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `producto_final_id` | `integer` | FK `productos.id` |
| `bodega_id` | `integer` | FK `bodegas.id` |
| `fecha` | `date` | requerido |
| `estado` | `varchar(20)` | inicia en `ABIERTA` |
| `moneda` | `varchar(10)` | default `CS` |
| `tasa_cambio` | `numeric(12,4)` | opcional |
| `cantidad_producida` | `numeric(14,4)` | requerido |
| `total_insumos_usd` | `numeric(14,2)` | calculado |
| `total_insumos_cs` | `numeric(14,2)` | calculado |
| `total_produccion_usd` | `numeric(14,2)` | calculado |
| `total_produccion_cs` | `numeric(14,2)` | calculado |
| `observacion` | `varchar(300)` | opcional |
| `usuario_registro` | `varchar(120)` | auditoria |
| `ingreso_id` | `integer` | FK `ingresos_inventario.id` |
| `egreso_id` | `integer` | FK `egresos_inventario.id` |
| `created_at` | `timestamp` | default `now()` |
| `updated_at` | `timestamp` | actualizacion ORM |

### `producciones_inventario_lineas`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `produccion_id` | `integer` | FK `producciones_inventario.id` |
| `tipo_linea` | `varchar(20)` | requerido |
| `producto_id` | `integer` | FK `productos.id` |
| `cantidad` | `numeric(14,4)` | requerido |
| `costo_unitario_usd` | `numeric(14,2)` | calculado |
| `costo_unitario_cs` | `numeric(14,2)` | calculado |
| `subtotal_usd` | `numeric(14,2)` | calculado |
| `subtotal_cs` | `numeric(14,2)` | calculado |

## Configuracion empresarial

### `business_settings`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `business_name` | `varchar(160)` | requerido |
| `legal_name` | `varchar(180)` | opcional |
| `trade_name` | `varchar(180)` | opcional |
| `app_title` | `varchar(180)` | opcional |
| `sidebar_subtitle` | `varchar(200)` | opcional |
| `address` | `text` | opcional |
| `ruc` | `varchar(80)` | opcional |
| `phone` | `varchar(80)` | opcional |
| `phones` | `varchar(200)` | opcional |
| `email` | `varchar(180)` | opcional |
| `website` | `varchar(200)` | opcional |
| `theme_code` | `varchar(60)` | tema |
| `sales_interface_code` | `varchar(60)` | interfaz comercial |
| `pricing_currency` | `varchar(10)` | `CS` o `USD` |
| `logo_login` | `varchar(255)` | ruta multimedia |
| `logo_sidebar` | `varchar(255)` | ruta multimedia |
| `logo_invoice` | `varchar(255)` | ruta multimedia |
| `logo_favicon` | `varchar(255)` | ruta multimedia |
| `inventory_cs_only` | `boolean` | politica |
| `weighted_inventory_enabled` | `boolean` | politica |
| `weighted_sales_enabled` | `boolean` | politica |
| `recipe_explosion_on_ingreso` | `boolean` | politica |
| `multi_branch_enabled` | `boolean` | politica |
| `price_auto_from_cost_enabled` | `boolean` | politica |
| `price_margin_percent` | `integer` | margen, minimo `0` |

### `company_environments`

| Columna | Tipo | Restricciones |
| --- | --- | --- |
| `id` | `integer` | PK |
| `company_key` | `varchar(80)` | unico, requerido |
| `company_name` | `varchar(180)` | requerido |
| `database_url` | `text` | requerido |
| `is_active` | `boolean` | solo uno debe quedar activo |

## Relaciones principales

- `users` N:N `roles` mediante `user_roles`.
- `productos` pertenece opcionalmente a linea, segmento, unidad y marca.
- `saldos_productos` mantiene una relacion 1:1 con `productos`.
- `productos_recetas` mantiene una relacion 1:1 con producto final.
- `productos_receta_lineas` relaciona receta con productos insumo.
- Ingresos y egresos tienen cabecera e items.
- Una produccion referencia producto final, bodega, ingreso generado y egreso de
  insumos.

## Metodos que afectan datos

| Metodo backend | Efecto |
| --- | --- |
| `_get_or_create_saldo()` | Crea saldo global faltante |
| `_balances_by_bodega()` | Calcula entradas menos salidas por bodega |
| `_rebuild_global_saldo()` | Reconstruye saldo global desde items |
| `_cost_pair_from_amount()` | Convierte costos USD/C$ |
| `_assign_product_cost()` | Guarda costo segun politica empresarial |
| `_build_recipe_requirements()` | Calcula insumos requeridos por receta |
| `_ensure_recipe_stock()` | Valida disponibilidad de materia prima |
| `create_ingreso()` | Registra cabecera, items, costos y recalcula saldo |
| `create_egreso()` | Valida stock, registra salida y opcionalmente traslado |
| `open_production()` | Abre orden y calcula lineas de insumo |
| `execute_production()` | Genera egreso de insumos e ingreso de producto final |
| `seed_inventory_catalogs()` | Crea catalogos base y compatibilidad de esquema |
| `seed_business_settings()` | Inicializa branding, politicas y entorno principal |

## Datos verificados en entorno local

| Tabla | Filas |
| --- | ---: |
| `users` | 1 |
| `roles` | 1 |
| `bodegas` | 1 |
| `lineas` | 1 |
| `segmentos` | 1 |
| `unidades_medida` | 3 |
| `proveedores` | 2 |
| `ingreso_tipos` | 8 |
| `egreso_tipos` | 10 |
| `business_settings` | 1 |
| `company_environments` | 1 |
| Productos, movimientos, recetas y producciones | 0 |

## Tablas todavia no implementadas

No existen tablas para:

- Clientes.
- Vendedores.
- Facturas de venta.
- Detalle de factura.
- Pagos.
- Bancos y cuentas.
- Caja, apertura o cierre.
- Cobranza.

Estas entidades forman parte del pendiente del modulo comercial.
