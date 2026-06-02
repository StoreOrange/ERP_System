# API ERP System

Ultima verificacion OpenAPI: 2026-06-02

Base local Docker: `http://127.0.0.1:8001`

Swagger UI: `http://127.0.0.1:8001/docs`

## Resumen

- Operaciones OpenAPI publicadas: 43.
- Framework: FastAPI.
- Autenticacion: JWT Bearer.
- Expiracion de token: 60 minutos.

## Metodos generales

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/` | Estado basico de la API |
| `GET` | `/sales` | Redireccion 307 al frontend de ventas |
| `GET` | `/sales/` | Redireccion 307 al frontend de ventas |

Las rutas `/sales` no aparecen en OpenAPI porque usan
`include_in_schema=False`.

## Autenticacion

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `POST` | `/auth/register` | Crea un usuario |
| `POST` | `/auth/login` | Inicia sesion por correo o nombre y retorna JWT |
| `GET` | `/auth/me` | Retorna el usuario autenticado |

Ejemplo de login:

```json
{
  "email": "administrador",
  "password": "020416"
}
```

Respuesta:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "administrador",
    "full_name": "Administrador",
    "is_active": true,
    "roles": [
      {
        "id": 1,
        "name": "administrador"
      }
    ]
  }
}
```

## Catalogos de inventario

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/inventory/catalogs` | Retorna todos los catalogos |
| `POST` | `/inventory/lineas` | Crea linea |
| `PUT` | `/inventory/lineas/{linea_id}` | Actualiza linea |
| `POST` | `/inventory/segmentos` | Crea segmento |
| `PUT` | `/inventory/segmentos/{segmento_id}` | Actualiza segmento |
| `POST` | `/inventory/unidades-medida` | Crea unidad |
| `PUT` | `/inventory/unidades-medida/{unidad_id}` | Actualiza unidad |
| `POST` | `/inventory/marcas` | Crea marca |
| `PUT` | `/inventory/marcas/{marca_id}` | Actualiza marca |
| `POST` | `/inventory/bodegas` | Crea bodega |
| `POST` | `/inventory/proveedores` | Crea proveedor |
| `POST` | `/inventory/ingreso-tipos` | Crea tipo de ingreso |
| `POST` | `/inventory/egreso-tipos` | Crea tipo de egreso |

## Productos

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/inventory/products` | Lista productos; admite `q` e `include_inactive` |
| `POST` | `/inventory/products` | Crea producto y saldo |
| `GET` | `/inventory/products/next-code` | Genera siguiente codigo numerico |
| `GET` | `/inventory/products/search` | Busqueda POS por texto o codigo de barras |
| `GET` | `/inventory/products/{product_id}` | Consulta detalle |
| `PUT` | `/inventory/products/{product_id}` | Actualiza producto |
| `PATCH` | `/inventory/products/{product_id}/toggle-active` | Activa o desactiva |
| `GET` | `/inventory/products/{product_id}/balances` | Existencia por bodega |

Parametros de busqueda POS:

| Parametro | Tipo | Descripcion |
| --- | --- | --- |
| `q` | texto | Codigo, barra o descripcion |
| `bodega_id` | entero opcional | Restringe saldo a bodega |
| `price_list` | entero opcional | Lista 1, 2 o 3 |

## Recetas

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/inventory/products/{product_id}/recipe` | Consulta receta |
| `PUT` | `/inventory/products/{product_id}/recipe` | Guarda receta e insumos |

Ejemplo:

```json
{
  "nombre": "Producto empacado",
  "activo": true,
  "lineas": [
    {
      "insumo_producto_id": 10,
      "unidad_medida_id": 1,
      "cantidad": 2.5
    }
  ]
}
```

## Ingresos y egresos

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/inventory/ingresos` | Lista ingresos |
| `POST` | `/inventory/ingresos` | Registra ingreso e items |
| `GET` | `/inventory/egresos` | Lista egresos |
| `POST` | `/inventory/egresos` | Registra egreso, valida stock y procesa traslado |
| `GET` | `/inventory/kardex/{product_id}` | Kardex del producto |

Reglas:

- Moneda permitida: `USD` o `CS`.
- USD requiere tasa mayor que cero.
- Un ingreso exige al menos un item.
- Un egreso exige stock suficiente en la bodega origen.
- Si el egreso incluye `bodega_destino_id`, se crea el ingreso espejo del
  traslado.

## Produccion

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/inventory/producciones` | Lista producciones |
| `POST` | `/inventory/producciones/open` | Abre orden de produccion |
| `POST` | `/inventory/producciones/{production_id}/execute` | Ejecuta produccion |
| `GET` | `/inventory/producciones/{production_id}/report` | Reporte detallado |

Flujo:

1. Abrir orden para un producto `RECETA`.
2. Calcular insumos segun cantidad producida.
3. Validar stock de materia prima.
4. Ejecutar orden.
5. Crear egreso de insumos.
6. Crear ingreso del producto final.
7. Recalcular saldos.

## Configuracion empresarial

| Metodo | Ruta | Autenticacion | Descripcion |
| --- | --- | --- | --- |
| `GET` | `/settings/business/public` | No | Branding publico |
| `GET` | `/settings/business` | Si | Configuracion completa |
| `PUT` | `/settings/business` | Si | Actualiza configuracion y logos |

`PUT /settings/business` recibe `multipart/form-data`.

## Entornos de empresa

| Metodo | Ruta | Autenticacion | Descripcion |
| --- | --- | --- | --- |
| `GET` | `/settings/environments` | Si | Lista entornos |
| `POST` | `/settings/environments` | Si | Crea entorno |
| `PUT` | `/settings/environments/{environment_id}` | Si | Actualiza entorno |
| `PATCH` | `/settings/environments/{environment_id}/activate` | Si | Activa uno y desactiva los demas |

## Funciones internas relevantes

### Autenticacion

| Funcion | Responsabilidad |
| --- | --- |
| `create_access_token()` | Firma JWT HS256 |
| `verify_password()` | Valida bcrypt |
| `hash_password()` | Genera hash bcrypt |
| `_get_user_from_token()` | Decodifica token y valida estado |

### Inventario

| Funcion | Responsabilidad |
| --- | --- |
| `_normalize_product_code()` | Limpia codigo |
| `_next_product_code()` | Genera secuencia visual |
| `_normalize_currency()` | Acepta solo USD o CS |
| `_require_exchange_rate()` | Exige tasa para USD |
| `_balances_by_bodega()` | Calcula existencia por bodega |
| `_rebuild_global_saldo()` | Reconstruye saldo global |
| `_inventory_cost_currency()` | Resuelve moneda de costo |
| `_cost_pair_from_amount()` | Convierte costo a USD y CS |
| `_build_recipe_requirements()` | Explota receta |
| `_ensure_recipe_stock()` | Valida insumos disponibles |

### Configuracion

| Funcion | Responsabilidad |
| --- | --- |
| `_get_or_create_business_settings()` | Inicializa configuracion |
| `_save_upload()` | Guarda logo y reemplaza archivo previo |
| `_serialize()` | Construye respuesta empresarial |
| `_validate_company_key()` | Valida clave `[a-z0-9_]+` |

## Endpoints no implementados

No existen endpoints persistentes para:

- Clientes.
- Vendedores.
- Facturas.
- Detalles de venta.
- Pagos.
- Bancos o cuentas.
- Caja.
- Cobranza.

La vista `/app/sales` simula estas entidades en memoria del navegador y usa la
API real solo para catalogos, configuracion y busqueda de productos.
