# Pendientes del sistema de planificacion de recursos empresariales

Ultima actualizacion: 2026-06-06

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
- [x] Primera fase UI de ingresos y egresos: formulario priorizado, historial documental y controles compactos.
- [x] Retirar `htmx.org` del arranque y dependencias del frontend.
- [x] Arquitectura visual Enterprise fase 1: shell, header, breadcrumb, PanelMenu, MegaMenu, Toast, ConfirmDialog y dashboard con ApexCharts.
- [x] Formularios Enterprise fase 2 inicial: FloatLabel en productos, validacion visual y DatePicker PrimeVue en historico de inventario.
- [x] Tablas Enterprise fase 3 inicial: productos, historico de inventario y produccion con DataTable avanzado y exportacion CSV.
- [x] Catalogo real de vendedores vinculado a usuarios, sucursales y bodegas.
- [x] CRUD visual inicial de usuarios, sucursales, vendedores y perfiles de acceso.
- [x] Documentacion tecnica consolidada.

## Prioridad critica

- [ ] Crear migracion Alembic consolidada para todas las tablas.
- [ ] Eliminar creacion y alteracion de esquema desde `app.main`.
- [x] Mover `SECRET_KEY` JWT a variable de entorno.
- [ ] Configurar un valor secreto unico de `JWT_SECRET_KEY` fuera del repositorio
  antes de produccion.
- [ ] Retirar o proteger credenciales iniciales fijas del administrador.
- [ ] Restringir CORS; actualmente acepta todos los origenes.
- [ ] Proteger endpoints de inventario con autenticacion y permisos.

## Ventas y facturacion

- [ ] Crear tablas y endpoints de clientes.
- [x] Crear tablas y endpoints de vendedores.
- [x] Crear tablas y endpoints de facturas POS y detalle.
- [x] Registrar pagos aplicados a factura POS.
- [ ] Crear catalogos reales de bancos, cuentas y formas de pago.
- [ ] Crear tablas para caja, apertura y cierre.
- [ ] Persistir clientes desde ventas.
- [x] Persistir vendedores desde ventas.
- [x] Persistir facturas POS desde ventas.
- [x] Descontar inventario al confirmar venta mediante egreso tipo `Venta`.
- [x] Implementar consecutivo POS e impresion basica del recibo en pantalla.
- [ ] Implementar consecutivo fiscal legal y PDF.
- [ ] Implementar cobranza, depositos y cierre de caja.

## Usuarios y seguridad

- [x] CRUD administrativo inicial de usuarios.
- [x] Perfiles de acceso por sucursal y bodega.
- [ ] Matriz de permisos por modulo y accion aplicada a endpoints protegidos.
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
- [ ] Segunda fase UI de ingresos y egresos: flujo guiado por pasos, atajos de teclado y vista de documento previa.
- [ ] Anulacion controlada de movimientos.
- [ ] Historial de cambios de costo.
- [ ] Trazabilidad completa por usuario autenticado.
- [ ] Validar unidades compatibles dentro de recetas.

## Frontend

- [ ] Migrar vistas restantes a patrones PrimeVue Enterprise: DataTable avanzado, Tabs, Accordion, Splitter y Card.
- [ ] Agregar Toast/ConfirmDialog en acciones reales de guardado, eliminacion y confirmacion.
- [ ] Extender filtros, ordenamiento, columnas redimensionables y exportacion a tablas restantes de ventas, configuracion y usuarios.
- [ ] Convertir formularios restantes a Floating Labels, DatePicker y AutoComplete donde aplique.
- [ ] Extender validacion visual a ventas, configuracion, marcas, subcatalogos y produccion.
- [x] Conectar vista de usuarios a CRUD real.
- [ ] Estados de carga y error consistentes.
- [x] Dividir bundle frontend por chunks base.
- [ ] Reducir carga inicial con imports dinamicos de graficos y vistas pesadas.
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
