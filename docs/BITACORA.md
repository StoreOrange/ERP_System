# Bitacora del sistema de planificacion de recursos empresariales

Ultima actualizacion: 2026-06-21

## Objetivo

Construir un sistema de planificacion de recursos empresariales modular para
Orange Tec tomando como base funcional el sistema HollywoodPacas. Integra
autenticacion, inventario, produccion, configuracion empresarial y una interfaz
de ventas en evolucion, orientado a pymes, emprendimientos y negocios locales.

## Documento complementario por sprints

Se agrego la bitacora extendida por modulos y sprints en:

- [Bitacora_Sprint.md](./Bitacora_Sprint.md)

Este documento organiza el desarrollo bajo la estructura: problema a resolver,
objetivos, actividades, requerimientos funcionales, requerimientos no
funcionales, analisis, diseno, implementacion, evidencias, validacion,
retroalimentacion y resultados.

## Historial verificado

### 2026-06-06 - Catalogo de vendedores y accesos por sucursal/bodega

- Nuevas entidades persistentes: `sucursales`, `vendedores` y `user_access_profiles`.
- Relacion de `bodegas` con sucursal mediante `sucursal_id`.
- Router backend `/access` para usuarios, roles, sucursales, vendedores y perfiles de acceso.
- Usuario administrador inicial con perfil de acceso principal y vendedor vinculado.
- Respuesta de sesion extendida con accesos activos y vendedor asociado.
- Pantalla `Usuarios y accesos` reemplazada por gestion real con pestañas:
  usuarios, vendedores, sucursales y accesos.
- Ventas consume el catalogo real de vendedores y permite crear vendedores persistentes.
- Validacion Docker/API: `users=1`, `vendors=1`, `branches=1`, `userAccess=1`.

### 2025-12-02 - Version inicial desde VPS

Commit: `ffadcd3`

- Estructura inicial con FastAPI, SQLAlchemy, Alembic, Vue y Vite.
- Configuracion base de conexion y sesiones de base de datos.
- Modelos `users`, `roles` y relacion N:N `user_roles`.
- Registro, login JWT y consulta del usuario autenticado.
- Migracion inicial
  `5285f6b056a5_create_users_and_roles.py`.
- Primer prototipo frontend con login y pagina de inicio.

### 2026-05-03 - Port de HollywoodPacas y UI modular

Commit: `ebc7966`

- Limpieza de archivos generados `__pycache__` y reglas `.gitignore`.
- Port de catalogos: lineas, segmentos, unidades de medida, marcas, bodegas,
  proveedores y tipos de ingreso y egreso.
- Productos con codigo generado, codigo de barras, tres listas de precios,
  activacion, busqueda y saldos por bodega.
- Inventario con ingresos, egresos, transferencias, kardex y manejo de costos.
- Recetas y produccion con apertura, ejecucion, validacion de existencias y
  reporte.
- Configuracion empresarial con identidad visual, logos, politicas y entornos
  de empresa.
- Datos iniciales creados al iniciar la aplicacion: usuario administrador,
  catalogos principales y configuracion empresarial.
- Script `backend/scripts/import_hollpacas_inventory.py`.
- Nuevo shell Vue con proteccion de rutas, dashboard, usuarios, productos,
  inventario, produccion, ventas y configuraciones.
- Tema PrimeVue, Bootstrap Icons y servicios frontend.
- Script `run_dev.ps1` para desarrollo local.

### 2026-05-13 - Costos y acceso a ventas

Commit: `6973fc1`

- Correccion del manejo de moneda de costos.
- Conversiones USD/C$ condicionadas por configuracion.
- Redireccion `/sales` y `/sales/` hacia el frontend.
- Ajustes al formulario de movimientos.

### 2026-06-01 - Docker completo para desarrollo

Cambios locales verificados:

- `compose.yaml` con PostgreSQL 16, FastAPI y Vue/Vite.
- Dockerfiles, `.dockerignore` y `.env.example`.
- Migraciones Alembic antes de iniciar Uvicorn.
- Volumenes para recarga de codigo.
- Servicios validados:
  - Frontend: `http://127.0.0.1:5174`
  - Backend: `http://127.0.0.1:8001`
  - PostgreSQL: `127.0.0.1:5433`

### 2026-06-01 - Tema visual claro y responsive

- Sustitucion del tema oscuro por blanco y violeta.
- Login rediseñado con portada animada.
- Superficies, tarjetas, bordes, espacios y botones uniformes.
- Tema PrimeVue adaptado.
- Login compacto en pantallas pequeñas.

### 2026-06-01 - Reorganizacion de ventas

- Catalogo a la izquierda; ticket y datos comerciales a la derecha.
- Botones PrimeVue corregidos con propiedad `label`.
- Formulario plegable de cliente y observacion integrada.
- Anchos, margenes y truncamiento normalizados.
- Navegacion movil horizontal compacta.
- Seleccion de cliente y accion `Consumidor final` agrupadas.
- Responsive verificado a `390px`: `scrollWidth=390`, `offenders=0`.

### 2026-06-02 - Tipografia estilo Odoo

- Pila tipografica de Odoo 18 aplicada globalmente:
  `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`,
  `Helvetica Neue`, `Ubuntu`, `Noto Sans`, `Arial`.
- Titulos con prioridad `SF Pro Display`.
- Orden CSS corregido: Bootstrap antes del tema del sistema.
- Login, ventas, inputs, botones y PrimeVue auditados desde navegador.

### 2026-06-02 - Documentacion consolidada

- Esquema verificado directamente contra PostgreSQL.
- Confirmadas 25 tablas fisicas y 29 claves foraneas.
- Confirmadas 46 operaciones OpenAPI.
- Documentacion actualizada:
  - `docs/BITACORA.md`
  - `docs/SISTEMA.md`
  - `docs/PENDIENTES.md`
  - `docs/BASEDEDATOS.md`
  - `docs/API.md`

### 2026-06-02 - Publicacion sincronizada en GitHub

Commit: `5e38589`

- Consolidacion de Docker, documentacion y experiencia visual.
- Publicacion del mismo commit en `erpfinal/main`,
  `erpfinal/desarrollador-1` y `erpfinal/desarrollador-2`.

### 2026-06-02 - Sesion extendida y header de ventas compacto

Cambios locales verificados:

- Duracion JWT movida a `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.
- Valor predeterminado de desarrollo: `480` minutos (8 horas).
- Clave JWT movida a `JWT_SECRET_KEY` con fallback local de desarrollo.
- Variables agregadas a `.env.example` y `compose.yaml`.
- Header de ventas compactado:
  - Menor padding exterior.
  - Cajetines KPI de menor altura.
  - Tipografia y separaciones reducidas.
  - Pestañas comerciales mas compactas.
- Token nuevo validado con `28800` segundos de vigencia.
- Header refinado a una sola fila de seis KPIs.
- Header validado con altura de `132px`, cajetines de `42px` y cero
  desbordamientos.
- Segunda limpieza visual de ventas:
  - Header reducido a factura, bodega y total.
  - Pestanas de modulos aun no operativos retiradas de la pantalla.
  - Textos descriptivos repetidos y boton `Combos` sin accion retirados.
  - Resumen del ticket reducido a total de factura, unidades y tasa.
  - Vista verificada en escritorio y movil desde navegador.
- Barra superior `Workspace` retirada del shell autenticado.
- Accion `Salir` trasladada al menu lateral y conservada en responsive movil.
- Identidad visual simplificada con una sola carga `Logo del comercio`.
- Logo comercial aplicado al sidebar en reemplazo del bloque textual y
  sincronizado automaticamente como favicon.
- Reemplazo de logo validado: la nueva carga elimina el archivo anterior para
  evitar residuos en `uploads/business`.
- Encabezado del sidebar refinado:
  - Logo centrado dentro de un cajetin blanco con borde sutil.
  - Nombre comercial y subtitulo centrados bajo la imagen.
  - Boton de colapsar separado del area util del logo.
  - Version movil compacta con logo y nombre en una sola fila.
- Encabezado lateral compactado nuevamente:
  - Cajetin e imagen de menor altura.
  - Margenes verticales reducidos.
  - Flecha de ocultar movida a una fila independiente bajo el encabezado.
- Selector de lista de precios retirado de la interfaz de ventas.
- Ventas usa internamente la lista base de precio `1`.
- Sidebar reducido de `278px` a `232px`.
- Estado colapsado reducido de `92px` a `76px`.
- Navegacion, logo y tarjeta de sesion compactados para el nuevo ancho.
- Interfaz de ventas refinada con estilo POS/Odoo:
  - Paneles mas planos, bordes uniformes y sombra ligera.
  - Total de factura jerarquizado en violeta corporativo.
  - Catalogo de productos con resaltado lateral al seleccionar o pasar cursor.
  - Ticket actual mas compacto, con filas limpias y controles alineados.
  - Datos de factura contenidos en tarjeta comercial mas sobria.
  - Barra inferior de acciones reducida y consistente.
- Interfaz de ventas parametrizada por tipo de negocio:
  - `ecommerce`: lista elegante para catalogo y venta asistida.
  - `supermarket`: grilla de tarjetas para buscar y cargar productos rapido.
  - `hardware`: busqueda general densa por codigo, barra, stock y precio.
  - Configuracion empresarial permite seleccionar la vista activa.
  - Backend normaliza valores legacy hacia las nuevas vistas.
- Tasa de cambio agregada como dato operativo:
  - Tabla `exchange_rates` creada para tasas diarias, mensuales o trimestrales.
  - Endpoints para consultar tasa vigente, listar historial y registrar tasas.
  - Nueva seccion `Tasa de cambio` en Datos y Configuraciones.
  - Ventas deja de usar tasa fija y consume la tasa vigente registrada.
  - Movimientos de inventario y produccion precargan la tasa vigente cuando
    requieren conversiones USD/C$.
- Escala visual global compactada:
  - Tarjetas, paneles, headers internos y modulos reducidos a una escala unica.
  - Menus internos de configuracion y tarjetas de opciones compactados.
  - Inputs, botones, labels y textos normalizados para evitar recuadros enormes.
  - Previews de logo y tarjetas KPI ajustadas a tamanos mas consistentes.
  - Segunda pasada aplicada con selectores especificos y guard final en
    `.app-main` para evitar textos y recuadros sobredimensionados en pantallas
    autenticadas.
- Checkboxes de formularios convertidos a chips compactos sin quiebre de
  linea, incluyendo `Activar al guardar` en Entornos.
- Control de inventario activado en ventas:
  - Busqueda de productos muestra existencia por bodega y bloquea productos
    sin stock suficiente.
  - Cantidades del ticket no pueden superar la existencia disponible.
  - Cambio de bodega limpia el ticket para evitar mezclar saldos.
  - Confirmar venta registra egreso de inventario tipo `Venta` y descuenta
    saldo real.
  - Tipo de egreso `Venta` agregado a catalogos iniciales.
- Facturacion POS y pagos aplicados:
  - Nuevas tablas `sales_invoices`, `sales_invoice_items`, `sales_payments` y
    `sales_sequences`.
  - Nuevo modulo backend `/sales-api` con consecutivo POS, listado y registro
    de facturas.
  - La confirmacion de venta ahora registra factura, detalle, pagos y egreso de
    inventario en una sola transaccion.
  - Venta de contado exige pago completo; credito permite saldo pendiente.
  - Recibo POS en pantalla con resumen de items, pagos, saldo y vuelto.
- Selectores de fecha uniformados:
  - `input[type=date]`, `datetime-local`, `time` y `month` reciben estilo tipo
    Bootstrap 5.
  - Foco, hover, bordes, icono del calendario y escala compacta quedan
    consistentes en ventas, inventario, produccion y configuracion.
- Modal de pagos mejorado:
  - Campo de monto recibe foco automatico al abrir el modal.
  - Monto se muestra con texto grueso y estilo destacado.
  - `Enter` registra el pago aplicado y devuelve el foco al monto.
  - Tarjetas de forma de pago y lista de pagos quedan con acabado visual mas
    profesional.
- Modal de pagos compactado:
  - Objetos, tarjetas, botones, inputs, totales y pagos aplicados reducidos de
    escala.
  - Al abrir el modal se precarga el saldo total de la factura en el monto y
    queda autoseleccionado.
  - `Enter` en monto o referencia aplica el pago; si cubre el total, registra
    la factura POS y abre la impresion del recibo.
  - Reorganizacion de grillas del modal para evitar campos alargados,
    montados o desbordados en escritorio y responsive.
  - Flujo de teclado corregido: primer `Enter` en monto agrega la forma de
    pago; segundo `Enter`, con el monto vacio y el total cubierto, genera la
    factura POS.
- Selector de fecha de ventas redisenado:
  - Control tipo Bootstrap 5 con icono de calendario, foco lila y boton rapido
    `Hoy`.
  - Datepicker propio en Vue con calendario desplegable, navegacion de mes,
    dias de semana, dia actual y fecha seleccionada.
  - Se elimina la dependencia visual del selector nativo basico del navegador.
  - Correccion del campo de fecha en ventas: el calendario ya no queda
    recortado por el contenedor y se retiro la fecha tecnica duplicada del
    boton principal.
  - La fecha visible en ventas, resumen de pago y recibo POS se muestra en
    formato `dd-mm-yyyy`; el valor interno se mantiene como `yyyy-mm-dd` para
    guardar correctamente en backend.
  - Ajuste visual posterior del campo fecha en la informacion de factura:
    ocupa dos columnas, se elimina el boton `Hoy` que comprimía el valor y se
    deja el calendario como selector principal.

### 2026-06-04 - Refuerzo de ingresos y egresos de inventario

- Modulo de ingresos/egresos revisado y reforzado:
  - Solo ingresos por `Compras Locales` permiten editar costo/precio de entrada
    para actualizar costo del producto segun moneda configurada.
  - Los demas tipos de ingreso usan costo vigente del producto y bloquean
    edicion manual de costo.
  - Egresos bloquean la edicion manual de costo en la interfaz; muestran costo
    de referencia del producto.
  - Backend de egresos ignora cualquier costo enviado por API y calcula siempre
    el costo con el producto vigente.
  - Validacion de egreso reforzada para no exceder existencia acumulada del
    producto en la bodega.
  - Al registrar ingreso o egreso se abre reporte del movimiento en pantalla.
  - Historico de movimientos permite abrir reporte de cualquier ingreso/egreso.
  - Reporte imprimible/PDF con documento, fecha, tipo, bodega, proveedor,
    usuario, detalle de productos, costos, totales y afectacion de inventario.
- Revision de guardado de productos:
  - Se confirmo que la base actual no tenia productos guardados y no existia
    POST registrado para el producto indicado por el usuario.
  - El formulario de productos ahora aplica defaults de linea, segmento, unidad
    y bodega inicial cuando corresponde.
  - El boton `Crear producto` ejecuta guardado directo y muestra validaciones
    visibles antes de enviar.
- Selector de fecha de ingresos/egresos reemplazado:
  - Se elimina el `input type=date` nativo del modulo de movimientos.
  - Nuevo calendario visual con icono, fecha `dd-mm-yyyy`, navegacion mensual,
    cierre por clic externo y ajuste responsive.
- Importacion de productos desde base `hollpacas`:
  - Se conecto al PostgreSQL del host mediante `host.docker.internal`.
  - Se importaron 280 productos, 280 saldos, catalogos de lineas, segmentos,
    unidades y bodegas.
  - Se normalizaron productos sin unidad asignandoles `Unidad`.
  - Resultado validado: 280 productos activos, 0 productos sin unidad, 20 saldos
    positivos y existencia total 321.
- Compatibilidad Firefox:
  - Se retiraron selectores CSS `:has()` usados en impresion y modal de pagos.
  - Las reglas de impresion ahora se activan con clases `printing-*` desde Vue.
  - Frontend validado con build y assets principales respondiendo `200`.

### 2026-06-05 - Enfoque empresarial y mejora inicial de inventario

- Se adopta la denominacion visible "sistema de planificacion de recursos
  empresariales" en lugar de presentar el producto con siglas.
- Textos visibles del login, dashboard, recibo POS, shell principal y usuarios
  ajustados a "Sistema empresarial" o equivalentes.
- Inicio de refinamiento UI del modulo de ingresos y egresos:
  - Formulario operativo toma prioridad sobre el historico.
  - Historial documental queda como panel secundario.
  - Buscador de productos con icono, menor altura y estilo mas limpio.
  - Producto seleccionado se muestra en tarjeta compacta con disponibilidad.
  - Totales, campos, botones y espaciados reducidos para una vista mas
    profesional.
  - Correccion de separadores visuales con codificacion danada.

### 2026-06-06 - Arquitectura visual Enterprise fase 1

- Se inicia modernizacion visual global inspirada en Odoo Enterprise, Zoho One,
  SAP Business One Web y Monday.com sin tocar endpoints, rutas ni modelos.
- Frontend:
  - Registro global de `ToastService` y `ConfirmationService`.
  - `Toast` y `ConfirmDialog` disponibles a nivel de aplicacion.
  - Dependencias agregadas: `apexcharts` y `vue3-apexcharts`.
  - Separacion de chunks en Vite para Vue, PrimeVue y graficos.
- Shell principal:
  - Sidebar colapsable conserva rutas actuales.
  - Navegacion agrupada con `PanelMenu`.
  - Header superior fijo con breadcrumb dinamico.
  - `MegaMenu` de acciones rapidas y drawer movil.
- Dashboard:
  - KPIs empresariales por productos, inventario y gestion financiera.
  - Graficos ApexCharts para movimientos y distribucion operativa.
  - Timeline de actividad, tags, skeleton de carga y widgets responsivos.

### 2026-06-06 - Formularios Enterprise fase 2

- Productos:
  - Formulario principal modernizado con `FloatLabel` de PrimeVue.
  - Campos principales de descripcion, codigo de barra, linea, segmento,
    unidad, marca, costos, precios, existencia y bodega inicial alineados al
    patron Enterprise.
  - Validacion visual con `p-invalid` para descripcion, unidad y bodega inicial
    requerida cuando hay existencia.
- Inventario:
  - Filtros de fecha del historico de ingresos/egresos migrados a `DatePicker`
    PrimeVue con icono y formato visual `dd-mm-yyyy`.
  - Se conserva el filtrado interno en formato ISO para no afectar datos ni API.
- Estilos:
  - Reglas globales para `FloatLabel`, `DatePicker` e invalidacion visual en
    formularios del area principal.

### 2026-06-06 - Tablas Enterprise fase 3

- Productos:
  - `DataTable` avanzado con filtro global conectado al buscador existente.
  - Ordenamiento, columnas redimensionables, scroll, paginacion extendida,
    filas alternas y exportacion CSV compatible con Excel.
  - Columnas con `field` para mejorar ordenamiento y exportacion.
- Ingresos y egresos:
  - Historico documental actualizado con exportacion CSV, ordenamiento,
    resize de columnas, scroll, paginacion avanzada y columna de acciones fija.
- Produccion:
  - Historico de producciones y detalle del informe con exportacion CSV,
    ordenamiento, columnas redimensionables, scroll y filas alternas.
- Estilos:
  - Acciones de tabla unificadas con clase `enterprise-table-actions`.
  - Cabeceras de tabla alineadas al estilo Enterprise.

## Estado funcional consolidado

| Frente | Estado actual |
| --- | --- |
| Autenticacion | Registro, login JWT, usuario autenticado y sesion local de 8 horas |
| Configuracion | Datos empresariales, logos, politicas, entornos y tasas de cambio |
| Productos | Catalogos, precios, codigos, busqueda y saldos |
| Inventario | Ingresos, egresos, transferencias y kardex |
| Produccion | Recetas, apertura, ejecucion y reporte |
| Ventas | Interfaz POS responsive con factura, pagos, tasa vigente, control de stock y egreso de inventario |
| Usuarios | Base de roles y usuarios disponible; administracion completa aun pendiente |
| Desarrollo | Entorno Docker completo con PostgreSQL, backend y frontend |

## Hallazgos tecnicos vigentes

- Alembic contiene la migracion inicial de usuarios y roles. Las tablas de
  inventario y configuracion se materializan actualmente mediante
  `Base.metadata.create_all()` y ajustes de arranque.
- La interfaz de ventas administra temporalmente cliente, vendedor, pagos y
  ticket en frontend; el backend de ventas y su persistencia siguen pendientes.
- Antes de produccion se debe configurar un valor privado y unico para
  `JWT_SECRET_KEY`.

## Validacion actual

- `docker compose ps`: base saludable, backend y frontend activos.
- `docker compose exec -T frontend npm run build`: correcto.
- `git diff --check`: correcto.
- PostgreSQL consultado directamente.
- OpenAPI consultado desde `http://127.0.0.1:8001/openapi.json`.
