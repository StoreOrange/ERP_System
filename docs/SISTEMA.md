# Estado actual del sistema ERP

Ultima actualizacion: 2026-06-02

## Resumen ejecutivo

ERP System es una aplicacion web modular en desarrollo para Orange Tec. El
nucleo operativo de autenticacion, catalogos, inventario, recetas, produccion y
configuracion empresarial ya existe. El terminal de ventas tiene una interfaz
avanzada y responsive, pero todavia no persiste facturas, clientes, vendedores
ni pagos en PostgreSQL.

## Arquitectura

| Capa | Tecnologia | Estado |
| --- | --- | --- |
| Frontend | Vue 3, Vite, PrimeVue 4, Bootstrap 5, Bootstrap Icons | Activo |
| Backend | FastAPI, SQLAlchemy 2, Pydantic, JWT | Activo |
| Base de datos | PostgreSQL 16 | Activa |
| Migraciones | Alembic | Parcial |
| Desarrollo | Docker Compose con recarga automatica | Activo |

## Servicios Docker

| Servicio | Puerto host | Puerto contenedor | Funcion |
| --- | --- | --- | --- |
| `frontend` | `5174` | `5173` | Aplicacion Vue/Vite |
| `backend` | `8001` | `8000` | API FastAPI |
| `db` | `5433` | `5432` | PostgreSQL `ERPDB` |

Inicio recomendado:

```powershell
docker compose up --build -d
```

## Modulos frontend

| Ruta | Modulo | Estado actual |
| --- | --- | --- |
| `/login` | Inicio de sesion | Funcional, responsive y con branding |
| `/app/dashboard` | Dashboard | Funcional; resume productos, ingresos y egresos |
| `/app/users` | Usuarios | Vista informativa; CRUD de usuarios y permisos pendiente |
| `/app/products` | Productos | Funcional; CRUD, catalogos, activacion y recetas |
| `/app/inventory/movements` | Inventario | Funcional; ingresos, egresos y consulta operativa |
| `/app/inventory/production` | Produccion | Funcional; apertura, ejecucion y reporte |
| `/app/sales` | Ventas | UI funcional; persistencia comercial pendiente |
| `/app/settings/business` | Configuracion | Funcional; empresa, logos, politicas y entornos |

## Funcionalidades implementadas

### Autenticacion

- Registro de usuario mediante API.
- Inicio de sesion con correo o nombre visible.
- Token JWT tipo Bearer con expiracion de 60 minutos.
- Consulta del usuario autenticado.
- Usuario administrador sembrado al iniciar el backend.

### Productos y catalogos

- Productos con codigo automatico opcional.
- Codigo de barras opcional y busqueda comercial.
- Tres listas de precios.
- Costo, existencia global y existencia por bodega.
- Linea, segmento, unidad de medida, marca y presentacion.
- Activacion o desactivacion de productos.
- Productos directos o productos por receta.
- Catalogos de bodegas, proveedores y tipos de movimiento.

### Inventario

- Registro de ingresos con items y conversion USD/C$.
- Registro de egresos con validacion de stock.
- Traslado entre bodegas mediante egreso origen e ingreso destino.
- Recalculo de saldo global desde movimientos.
- Consulta de kardex por producto.
- Configuracion de moneda de costo.

### Recetas y produccion

- Receta unica por producto final.
- Lineas de receta con insumo, unidad y cantidad.
- Apertura de orden de produccion.
- Validacion de materia prima disponible.
- Ejecucion de produccion con egreso de insumos e ingreso de producto final.
- Reporte de produccion.

### Configuracion empresarial

- Nombre legal y comercial.
- Titulo de aplicacion y subtitulo lateral.
- Direccion, RUC, telefonos, correo y sitio web.
- Logos para login, sidebar, factura y favicon.
- Moneda de precios.
- Politicas de inventario, peso, recetas, multibodega y margen automatico.
- Registro y activacion de entornos de empresa.

### Ventas

Implementado en frontend:

- Busqueda de productos conectada a inventario.
- Lector de codigo de barras.
- Ticket, cantidades, precios, descuentos y resumen.
- Cliente, vendedor, observacion, condicion, fecha y bodega.
- Modal de cobro con metodos de pago, moneda, bancos y cuentas.
- Diseno responsive validado a `390px`.

Pendiente en backend:

- Tablas comerciales.
- Endpoints para clientes y vendedores.
- Persistencia de facturas, detalle, pagos y caja.
- Consecutivo fiscal real.
- Afectacion de inventario al confirmar venta.

## Inicializacion automatica del backend

Al importar `app.main` se ejecutan:

1. `Base.metadata.create_all(bind=engine)`.
2. `create_initial_admin()`.
3. `seed_inventory_catalogs()`.
4. `seed_business_settings()`.

Esto mantiene el entorno local utilizable, pero debe reemplazarse gradualmente
por migraciones Alembic completas antes de desplegar en produccion.

## Datos iniciales sembrados

- Rol: `administrador`.
- Usuario local de desarrollo: `administrador`.
- Bodega: `BOD-001 - Bodega Principal`.
- Linea y segmento: `General`.
- Unidades: `UND`, `CJ`, `LB`.
- Ocho tipos de ingreso.
- Diez tipos de egreso.
- Dos proveedores base.
- Entorno empresarial activo: `principal`.

## Tema visual

- Interfaz clara con superficies blancas y acentos violeta.
- Tipografia basada en la pila oficial de Odoo 18.
- Titulos con prioridad `SF Pro Display`.
- PrimeVue y Bootstrap integrados bajo el mismo tema.
- Navegacion movil horizontal compacta.

## Documentos relacionados

- [Bitacora](./BITACORA.md)
- [Base de datos](./BASEDEDATOS.md)
- [API](./API.md)
- [Pendientes](./PENDIENTES.md)
