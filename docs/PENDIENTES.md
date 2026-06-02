# Pendientes del proyecto ERP System

Ultima actualizacion: 2026-06-02

## Completado

- [x] Backend FastAPI y PostgreSQL.
- [x] Autenticacion JWT basica y administrador inicial.
- [x] Docker Compose para frontend, backend y PostgreSQL.
- [x] Catalogos, CRUD de productos y saldos.
- [x] Ingresos, egresos, traslado y kardex.
- [x] Recetas y flujo de produccion.
- [x] Configuracion empresarial, logos y entornos.
- [x] Login responsive, tema blanco/violeta y tipografia estilo Odoo.
- [x] Terminal de ventas responsive.
- [x] Documentacion tecnica consolidada.

## Prioridad critica

- [ ] Crear migracion Alembic consolidada para todas las tablas.
- [ ] Eliminar creacion y alteracion de esquema desde `app.main`.
- [ ] Mover `SECRET_KEY` JWT a variable de entorno.
- [ ] Retirar o proteger credenciales iniciales fijas del administrador.
- [ ] Restringir CORS; actualmente acepta todos los origenes.
- [ ] Proteger endpoints de inventario con autenticacion y permisos.

## Ventas y facturacion

- [ ] Crear tablas y endpoints de clientes y vendedores.
- [ ] Crear tablas y endpoints de facturas y detalle.
- [ ] Crear tablas de pagos, bancos y cuentas.
- [ ] Crear tablas para caja, apertura y cierre.
- [ ] Persistir clientes, vendedores y facturas desde ventas.
- [ ] Descontar inventario al confirmar venta.
- [ ] Implementar consecutivo fiscal, impresion o PDF.
- [ ] Implementar cobranza, depositos y cierre de caja.

## Usuarios y seguridad

- [ ] CRUD administrativo de usuarios y roles.
- [ ] Matriz de permisos por modulo y accion.
- [ ] Politica de contrasenas y recuperacion de acceso.
- [ ] Auditoria de operaciones sensibles.

## Base de datos

- [ ] Agregar migraciones incrementales.
- [ ] Definir borrado restringido o cascade en inventario.
- [ ] Agregar indices por producto, bodega y fecha.
- [ ] Evaluar `NOT NULL` para columnas con defaults funcionales.
- [ ] Eliminar duplicidad de indice unico de `productos.codigo_barra`.
- [ ] Definir respaldo, restauracion y proteccion de credenciales de BD.

## Inventario y produccion

- [ ] Pruebas automatizadas de ingreso, egreso, traslado, kardex y receta.
- [ ] Anulacion controlada de movimientos.
- [ ] Historial de cambios de costo.
- [ ] Trazabilidad completa por usuario autenticado.
- [ ] Validar unidades compatibles dentro de recetas.

## Frontend

- [ ] Conectar vista de usuarios a CRUD real.
- [ ] Actualizar textos del dashboard sobre el avance del POS.
- [ ] Estados de carga y error consistentes.
- [ ] Dividir bundle frontend; Vite reporta chunk mayor a 500 kB.
- [ ] Revisar `htmx.org`; build reporta uso de `eval`.
- [ ] Agregar pruebas E2E responsive.

## Importacion HollywoodPacas

- [ ] Parametrizar `SOURCE_DB_URL`.
- [ ] Probar importacion con respaldo real.
- [ ] Documentar reconciliacion de conteos.

## DevOps

- [ ] Configuracion separada para produccion.
- [ ] Deshabilitar `--reload` fuera de desarrollo.
- [ ] Healthchecks para backend y frontend.
- [ ] HTTPS, proxy inverso y CI.
