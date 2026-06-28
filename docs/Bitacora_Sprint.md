# Bitacora por sprints del sistema de planificacion de recursos empresariales

Ultima actualizacion: 2026-06-21

Este documento resume el proceso de construccion del sistema en formato de
sprints. Su objetivo es servir como base para elaborar informes academicos,
presentaciones, memoria tecnica, defensa del proyecto o documentacion paso a
paso del desarrollo.

## Vision general del proyecto

En la actualidad, la transformacion digital se ha convertido en un factor clave
para la competitividad y sostenibilidad de las empresas. Sin embargo, muchas
organizaciones aun enfrentan dificultades para gestionar de forma eficiente sus
procesos administrativos, operativos y financieros debido al uso de
herramientas aisladas, registros manuales y falta de integracion de la
informacion. Estas limitaciones generan retrasos, errores operativos y
dificultades para obtener informacion confiable que respalde la toma de
decisiones estrategicas.

Pacas Hollywood Managua, empresa dedicada a la comercializacion,
clasificacion y procesamiento de ropa usada, presenta necesidades especificas
relacionadas con el control de inventarios, seguimiento de procesos de
clasificacion por calidad, identificacion de perdidas por deterioro o descarte
de mercancia y determinacion precisa de la rentabilidad obtenida en la
produccion de pacas de 100 libras y bolsas de 25 libras destinadas a
emprendedores.

Ante esta necesidad, el proyecto consiste en el analisis, diseno, desarrollo e
implementacion de un sistema de planificacion de recursos empresariales para
Pacas Hollywood Managua. La solucion integra en una sola plataforma procesos de
inventario, ventas, finanzas, produccion, compras, reportes e indicadores de
gestion, centralizando la informacion y automatizando tareas criticas del
negocio.

El sistema se construye tomando como referencia funcional la metodologia
operativa de HollywoodPacas y adaptandola a una arquitectura web moderna con
FastAPI, Vue 3, PostgreSQL y Docker.

## Importancia y justificacion

La importancia del proyecto radica en que proporciona a la empresa una
herramienta tecnologica capaz de mejorar el control de sus operaciones,
optimizar la administracion de recursos y fortalecer la calidad de la
informacion utilizada para la toma de decisiones. Desde el punto de vista de la
innovacion, la propuesta integra procesos que actualmente se realizan de forma
dispersa o manual, incorporando trazabilidad, control de inventario, analisis
de rentabilidad, control de mermas e indicadores gerenciales.

La trascendencia del sistema se refleja en su impacto sobre la productividad,
la eficiencia administrativa y la capacidad de crecimiento de la empresa. El
proyecto tambien sirve como referencia de transformacion digital aplicable a
organizaciones comerciales con caracteristicas similares dentro del sector
nicaraguense.

El proyecto se alinea con objetivos nacionales de transformacion digital,
innovacion tecnologica y fortalecimiento de la productividad empresarial
promovidos por el Plan Nacional de Lucha contra la Pobreza y para el
Desarrollo Humano 2022-2026.

## Objetivo general

Desarrollar e implementar un sistema de planificacion de recursos
empresariales para Pacas Hollywood Managua que permita gestionar de forma
integral los procesos de clasificacion de prendas, control de inventarios,
registro de mermas, ventas, distribucion y generacion de reportes
estrategicos, contribuyendo a la optimizacion de las operaciones y a la mejora
de la toma de decisiones dentro de la empresa.

## Objetivos especificos

1. Analizar los procesos actuales de clasificacion de prendas, control de
   inventarios, produccion de pacas, ventas y distribucion de Pacas Hollywood
   Managua, identificando necesidades y oportunidades de mejora.
2. Disenar la arquitectura y estructura funcional del sistema, definiendo
   modulos, procesos y flujos de informacion requeridos para la gestion
   integral de la empresa.
3. Desarrollar un modulo de inventario que permita registrar pacas adquiridas,
   controlar clasificacion por calidad y tipo de prenda, gestionar mezclas de
   productos y registrar perdidas o mermas generadas durante la depuracion.
4. Implementar un modulo de produccion para controlar y dar seguimiento a la
   transformacion de mercancia clasificada en pacas y bolsas destinadas a la
   comercializacion.
5. Desarrollar un modulo de ventas y distribucion para administrar clientes,
   registrar transacciones comerciales, controlar pedidos y realizar
   seguimiento de entregas dentro y fuera de Managua.
6. Implementar herramientas de analisis y reportes para evaluar inventarios,
   rotacion de productos, mermas, costos, ventas y rentabilidad operativa.
7. Validar el funcionamiento del sistema mediante pruebas funcionales y
   retroalimentacion de usuarios de Pacas Hollywood Managua.
8. Elaborar documentacion tecnica y manuales de usuario que faciliten
   implementacion, operacion y mantenimiento del sistema.

## Metodologia SCRUM

Para la ejecucion del proyecto se utiliza la metodologia agil SCRUM, organizada
en ciclos iterativos e incrementales. Este enfoque permite entregar
funcionalidades de manera progresiva, incorporar retroalimentacion del usuario
final y reducir riesgos durante el desarrollo.

Cada modulo se documenta bajo una estructura de sprints:

- Sprint I: modelo de negocio y requerimientos.
- Sprint II: analisis y diseno.
- Sprint III: implementacion.
- Sprint IV: producto funcional, evidencias, validacion y retroalimentacion.

Esta organizacion facilita que el sistema evolucione de acuerdo con las
necesidades reales de Pacas Hollywood Managua, manteniendo trazabilidad entre
problema, requerimientos, diseno, codigo y validacion.

## Viabilidad del proyecto

**Viabilidad tecnica**

El proyecto es tecnicamente factible porque utiliza tecnologias modernas,
robustas y ampliamente utilizadas en la industria del software. La arquitectura
contempla un frontend desarrollado con Vue 3, PrimeVue, Bootstrap 5,
ApexCharts y Vite; un backend construido con Python y FastAPI; persistencia de
datos con PostgreSQL 16; gestion de modelos y validacion con SQLAlchemy,
Pydantic y Alembic; autenticacion mediante JWT; comunicacion por API REST; y
contenedorizacion con Docker y Docker Compose.

**Viabilidad economica**

El proyecto es economicamente viable porque se apoya en tecnologias de codigo
abierto, reduciendo costos de licenciamiento e implementacion. Esto permite
destinar los recursos principalmente al analisis, desarrollo, pruebas,
capacitacion y mantenimiento.

**Viabilidad operativa**

El proyecto es operativamente viable porque responde a necesidades reales de
Pacas Hollywood Managua: control de inventario, clasificacion de mercaderia,
registro de mermas, produccion de pacas y bolsas, ventas, distribucion,
reportes y analisis de rentabilidad. Al centralizar la informacion, el sistema
favorece su adopcion y aporta beneficios concretos para la mejora continua de
los procesos empresariales.

## Stack de desarrollo

| Capa | Tecnologias |
| --- | --- |
| Frontend | Vue 3, Vue Router, PrimeVue 4, Bootstrap 5, Bootstrap Icons, ApexCharts, Vite |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Base de datos | PostgreSQL 16 |
| Seguridad | JWT, roles, perfiles de acceso por usuario, sucursal y bodega |
| DevOps local | Docker, Docker Compose, variables `.env`, volumenes de desarrollo |
| Documentacion | Markdown en carpeta `docs` |

## Modulo 1 - Modelo de negocio y arquitectura base

### Sprint I - Modelo de negocio y requerimientos

**Problema a resolver**

Los negocios locales necesitan controlar ventas, inventario, usuarios,
existencias, costos y configuracion empresarial desde una sola plataforma. El
manejo manual o separado de estas operaciones genera diferencias de stock,
errores de facturacion, baja trazabilidad y dificultad para tomar decisiones.

**Objetivos**

- Definir una plataforma web modular para gestion empresarial.
- Centralizar autenticacion, inventario, productos, ventas y configuracion.
- Mantener una base reutilizable para distintos tipos de comercios.
- Tomar como referencia operativa el sistema HollywoodPacas.

**Actividades realizadas**

- Definicion del alcance funcional inicial.
- Seleccion del stack tecnico.
- Estructuracion del proyecto en `backend`, `frontend` y `docs`.
- Definicion de Docker como entorno de desarrollo.
- Identificacion de modulos principales: autenticacion, productos,
  inventario, ventas, configuracion, usuarios y produccion.

**Requerimientos funcionales**

- Inicio de sesion de usuarios.
- Administracion de productos y catalogos.
- Control de ingresos y egresos de inventario.
- Registro de ventas con afectacion de stock.
- Configuracion de datos de empresa.
- Reportes basicos de movimientos y ventas.

**Requerimientos no funcionales**

- Aplicacion web responsive.
- API REST desacoplada del frontend.
- Base de datos relacional.
- Entorno reproducible con Docker.
- Interfaz moderna, clara y utilizable en equipos de escritorio.

**Resultados**

- Arquitectura inicial definida.
- Primer repositorio funcional con backend, frontend y base de datos.
- Base preparada para evolucionar por modulos.

### Sprint II - Analisis y diseno

**Casos de uso**

- Usuario inicia sesion.
- Administrador configura datos de empresa.
- Operador crea productos.
- Operador registra movimientos de inventario.
- Vendedor factura productos disponibles.

**Diagramas sugeridos**

- Diagrama de arquitectura cliente-servidor.
- Diagrama entidad-relacion de usuarios, productos, inventario y ventas.
- Diagrama de casos de uso por modulo.
- Diagrama de flujo de venta POS.

**Mockups**

- Login empresarial.
- Dashboard.
- Terminal de ventas.
- Catalogo de productos.
- Modulo de ingresos y egresos.

**Arquitectura**

- Frontend Vue 3 consume servicios REST.
- Backend FastAPI expone routers por dominio.
- PostgreSQL almacena datos operativos.
- Docker Compose levanta base de datos, backend y frontend.

**Diseño UI**

- Tema claro empresarial.
- Tipografia moderna inspirada en Odoo.
- Sidebar colapsable.
- Header con breadcrumb.
- Componentes PrimeVue para formularios, dialogos, tablas y feedback.

**Resultados**

- Base visual y tecnica establecida.
- Rutas protegidas y shell autenticado.
- Navegacion modular inicial.

### Sprint III - Implementacion

**Codificacion**

- Backend FastAPI con routers de autenticacion, inventario, ventas,
  configuracion y accesos.
- Modelos SQLAlchemy para usuarios, roles, productos, movimientos, ventas,
  configuracion y perfiles de acceso.
- Frontend Vue 3 con vistas por modulo.
- Servicios frontend para consumir endpoints.

**Tecnologias utilizadas**

- FastAPI, SQLAlchemy, Pydantic, PostgreSQL.
- Vue 3, PrimeVue, Bootstrap 5, Vite.
- Docker Compose.

**Capturas sugeridas**

- Login.
- Dashboard.
- Sidebar y header.
- Vista de productos.
- Vista de ventas.

**Pruebas**

- Compilacion backend con `python -m compileall backend/app`.
- Build frontend con `npm run build`.
- Verificacion de servicios con `docker compose ps`.
- Pruebas manuales de navegacion y carga de vistas.

**Resultados**

- Sistema navegable y modular.
- API y frontend comunicados.
- Docker operativo para desarrollo local.

### Sprint IV - Producto funcional

**Evidencias**

- Sistema levanta en Docker.
- Login permite acceso al area autenticada.
- Modulos principales visibles en el sidebar.
- Dashboard y rutas principales disponibles.

**Validacion**

- Verificacion de servicios activos.
- Construccion frontend exitosa.
- Compilacion backend correcta.

**Retroalimentacion**

- Se requiere mayor nivel visual tipo sistema empresarial.
- Se solicita mejorar uniformidad, espacios, botones y formularios.

**Resultados**

- Base funcional del sistema lista para profundizar en modulos operativos.

## Modulo 2 - Autenticacion, usuarios y control de acceso

### Sprint I - Modelo de negocio y requerimientos

**Problema a resolver**

El sistema debe controlar quien accede, que puede hacer y desde que sucursal o
bodega opera. En un comercio real, el vendedor no debe seleccionar libremente
cualquier bodega si su acceso operativo esta ligado a una sucursal especifica.

**Objetivos**

- Implementar autenticacion con JWT.
- Crear usuarios y roles.
- Asociar usuarios con vendedores.
- Vincular acceso operativo por sucursal y bodega.
- Preparar la base para permisos por modulo.

**Actividades realizadas**

- Creacion de modelos `users`, `roles` y `user_roles`.
- Implementacion de login y registro basico.
- Configuracion de token JWT.
- Extension de sesion a 8 horas en desarrollo.
- Creacion de sucursales, vendedores y perfiles de acceso.

**Requerimientos funcionales**

- Login con usuario valido.
- Token de sesion persistente.
- Catalogo de vendedores.
- Catalogo de sucursales.
- Perfil de acceso por usuario, bodega y sucursal.

**Requerimientos no funcionales**

- Seguridad basada en token.
- Expiracion configurable.
- Datos de acceso disponibles para el frontend.
- Escalabilidad futura para permisos detallados.

**Resultados**

- Autenticacion funcional.
- Usuario administrador inicial.
- Vendedor de piso como perfil base.
- Acceso ligado a bodega y sucursal.

### Sprint II - Analisis y diseno

**Casos de uso**

- Administrador crea usuario.
- Administrador crea vendedor.
- Administrador crea sucursal.
- Administrador asigna bodega y sucursal a usuario.
- Vendedor ingresa y factura desde su bodega asignada.

**Diagramas sugeridos**

- ERD de usuarios, roles, vendedores, sucursales, bodegas y perfiles.
- Flujo de autenticacion JWT.
- Flujo de asignacion de vendedor.

**Mockups**

- Pantalla de usuarios y accesos.
- Dialogo de vendedor.
- Dialogo de sucursal.
- Tabla de perfiles de acceso.

**Arquitectura**

- Router `/access`.
- Servicios frontend `access.js`.
- Vista `UsersView.vue` con pestañas de usuarios, vendedores, sucursales y
  accesos.

**Diseño UI**

- Tablas PrimeVue.
- Dialogos compactos.
- Tags para indicar permisos y estado.

**Resultados**

- Diseño del flujo de acceso operativo completo.

### Sprint III - Implementacion

**Codificacion**

- Modelos `Sucursal`, `Vendedor` y `UserAccessProfile`.
- Endpoints para usuarios, roles, sucursales, vendedores y perfiles.
- Respuesta de sesion enriquecida con `access_profiles` y `vendor_profile`.
- Vista administrativa de usuarios y accesos.
- Ventas consume el catalogo real de vendedores.

**Tecnologias utilizadas**

- FastAPI, SQLAlchemy, Pydantic.
- PrimeVue DataTable, Dialog, Select, Tag.

**Capturas sugeridas**

- Pantalla `Usuarios, vendedores y accesos`.
- Creacion de vendedor.
- Perfil con bodega y sucursal.
- Selector de vendedor en ventas.

**Pruebas**

- Validacion de creacion de vendedores.
- Validacion de carga de usuarios.
- Validacion de vendedor por defecto en ventas.
- Verificacion de bodega y sucursal asignada.

**Resultados**

- Catalogo real de vendedores implementado.
- Ventas deja de crear vendedores desde el POS y solo los selecciona.
- La bodega de venta queda amarrada al perfil del usuario.

### Sprint IV - Producto funcional

**Evidencias**

- Vista de usuarios conectada a datos reales.
- Vendedores visibles en ventas.
- Perfil de usuario entrega sucursal y bodega.

**Validacion**

- API `/access` responde datos.
- Ventas carga vendedores y usa bodega asignada.

**Retroalimentacion**

- Pendiente aplicar matriz completa de permisos por endpoint.
- Pendiente politica formal de contraseñas.

**Resultados**

- Control de acceso operativo suficiente para ventas e inventario inicial.

## Modulo 3 - Configuracion empresarial y datos maestros

### Sprint I - Modelo de negocio y requerimientos

**Problema a resolver**

Cada empresa necesita configurar su identidad, datos fiscales, logos, moneda,
tema visual, tasa de cambio y parametros operativos sin modificar codigo.

**Objetivos**

- Permitir gestion de datos generales de empresa.
- Cargar logo para sidebar, favicon y factura.
- Registrar tasas de cambio.
- Configurar tema visual y tipo de interfaz de ventas.
- Centralizar catalogos de clientes, vendedores y proveedores desde Datos.

**Actividades realizadas**

- Creacion de modelo `business_settings`.
- Creacion de modelo `company_environments`.
- Creacion de tabla `exchange_rates`.
- Implementacion de carga de logos.
- Sincronizacion de logo de comercio con favicon.
- Creacion de seccion de tasa de cambio.

**Requerimientos funcionales**

- Editar nombre comercial, razon social, RUC, telefono, correo y direccion.
- Subir logo empresarial.
- Registrar tasa diaria, mensual o trimestral.
- Consultar tasa vigente.
- Seleccionar tema visual.
- Seleccionar vista de ventas por tipo de negocio.

**Requerimientos no funcionales**

- Configuracion persistente.
- UI clara y compacta.
- Evitar valores fijos para tasa de cambio.
- Compatibilidad con recibo POS.

**Resultados**

- Datos empresariales disponibles para login, sidebar, favicon y factura POS.
- Tasa de cambio funcional para conversiones.

### Sprint II - Analisis y diseno

**Casos de uso**

- Administrador actualiza datos de empresa.
- Administrador carga logo.
- Administrador registra tasa de cambio.
- Sistema consulta tasa vigente para ventas e inventario.
- Administrador cambia vista de ventas.

**Diagramas sugeridos**

- Flujo de configuracion empresarial.
- Diagrama de uso de tasa de cambio en ventas e inventario.

**Mockups**

- Pantalla Datos de empresa.
- Seccion Tasa de cambio.
- Selector de tema visual.
- Selector de interfaz de ventas.

**Arquitectura**

- Router `/settings`.
- Servicio frontend `settings.js`.
- Vista `BusinessSettingsView.vue`.

**Diseño UI**

- Tarjetas compactas.
- Formularios por seccion.
- Listado de tasas registradas.
- Tema claro con colores corporativos.

**Resultados**

- Diseño modular para datos configurables.

### Sprint III - Implementacion

**Codificacion**

- Endpoints para configuracion publica y privada.
- Endpoints `/settings/exchange-rates/current`, `/settings/exchange-rates`.
- Carga y reemplazo de imagenes.
- Aplicacion de tema visual.
- Uso de tasa en ventas, movimientos y apertura de pacas.

**Tecnologias utilizadas**

- FastAPI multipart/form-data.
- SQLAlchemy.
- Vue 3 y formularios con Bootstrap/PrimeVue.

**Capturas sugeridas**

- Datos de empresa con RUC visible.
- Logo en sidebar.
- Favicon actualizado.
- Registro de tasa de cambio.

**Pruebas**

- Guardado de datos de empresa.
- Consulta de tasa vigente.
- Verificacion de logo en sidebar y recibo POS.
- Verificacion de datos empresariales en ticket.

**Resultados**

- Configuracion empresarial operativa y visible en ventas.

### Sprint IV - Producto funcional

**Evidencias**

- Logo empresarial aplicado.
- Datos de empresa impresos en recibo POS.
- Tasa vigente usada por ventas e inventario.

**Validacion**

- Guardado correcto de configuracion.
- Endpoint de tasa vigente disponible.

**Retroalimentacion**

- Se ajustaron colores de tema por preferencia del usuario.
- Se redujeron tamaños de tarjetas y textos para mejorar lectura.

**Resultados**

- Modulo de datos empresariales funcional y configurable.

## Modulo 4 - Productos, catalogos e importacion de HollywoodPacas

### Sprint I - Modelo de negocio y requerimientos

**Problema a resolver**

El comercio requiere administrar productos con codigos, precios, costos,
categorias, unidades y existencias iniciales. Tambien se necesitaba recuperar
productos desde la base existente de HollywoodPacas.

**Objetivos**

- Crear catalogo de productos.
- Manejar lineas, segmentos, marcas, unidades y bodegas.
- Registrar existencia inicial.
- Importar productos de HollywoodPacas.
- Buscar productos por descripcion, codigo o barra.

**Actividades realizadas**

- Modelado de productos y catalogos.
- Creacion de saldos globales y por bodega.
- Formulario de productos con defaults.
- Importacion de 280 productos desde base externa.
- Correccion de productos sin unidad.

**Requerimientos funcionales**

- Crear y editar productos.
- Activar o desactivar productos.
- Buscar productos.
- Registrar precios y costos.
- Asociar unidad, linea, segmento, marca y bodega inicial.

**Requerimientos no funcionales**

- Busqueda rapida.
- Validaciones visuales.
- Tabla con paginacion y exportacion.
- Datos consistentes para inventario y ventas.

**Resultados**

- Catalogo de productos operativo.
- Productos importados desde HollywoodPacas.

### Sprint II - Analisis y diseno

**Casos de uso**

- Usuario crea producto.
- Usuario registra existencia inicial.
- Usuario busca producto para venta o inventario.
- Usuario exporta listado.

**Diagramas sugeridos**

- ERD de productos, catalogos y saldos.
- Flujo de creacion de producto con existencia inicial.

**Mockups**

- Formulario de producto.
- Tabla de productos.
- Buscador de productos.

**Arquitectura**

- Router `/inventory/products`.
- Servicio `inventory.js`.
- Vista `ProductsView.vue`.

**Diseño UI**

- Formularios con floating labels.
- DataTable con filtros, ordenamiento y exportacion CSV.
- Validaciones visuales `p-invalid`.

**Resultados**

- Diseño de producto alineado a uso operativo.

### Sprint III - Implementacion

**Codificacion**

- Modelos `Producto`, `SaldoProducto`, `Linea`, `Segmento`,
  `UnidadMedida`, `Marca`, `Bodega`.
- Endpoints CRUD.
- Busqueda de productos para ventas con existencia por bodega.
- Script `import_hollpacas_inventory.py`.
- DataTable avanzada en productos.

**Tecnologias utilizadas**

- SQLAlchemy, PostgreSQL.
- PrimeVue DataTable, FloatLabel, Select.

**Capturas sugeridas**

- Listado de productos.
- Formulario de producto.
- Busqueda de producto en ventas.
- Resultado de importacion.

**Pruebas**

- Creacion de producto.
- Importacion validada.
- Busqueda por codigo y descripcion.
- Existencia visible en ventas.

**Resultados**

- 280 productos importados en entorno local.
- Catalogo listo para operaciones de inventario y ventas.

### Sprint IV - Producto funcional

**Evidencias**

- Productos activos visibles.
- Saldos positivos importados.
- Busqueda operacional funcionando.

**Validacion**

- Productos con unidad asignada.
- Saldos por bodega calculados.

**Retroalimentacion**

- Se corrigio caso donde productos creados no aparecian por defaults faltantes.

**Resultados**

- Modulo de productos funcional.

## Modulo 5 - Inventario, ingresos, egresos y traslados

### Sprint I - Modelo de negocio y requerimientos

**Problema a resolver**

El inventario debe reflejar entradas y salidas reales por bodega. Las ventas no
deben facturar productos sin existencia y los egresos no deben permitir saldos
negativos.

**Objetivos**

- Registrar ingresos de inventario.
- Registrar egresos de inventario.
- Validar existencia por bodega.
- Permitir traslados entre bodegas.
- Generar reporte imprimible de movimientos.

**Actividades realizadas**

- Implementacion de cabeceras e items de ingresos y egresos.
- Calculo de costos USD/C$.
- Recalculo de saldos globales.
- Validacion de egresos por existencia.
- Reporte visual de ingreso/egreso.
- Historico documental con filtros.

**Requerimientos funcionales**

- Registrar ingreso.
- Registrar egreso.
- Registrar traslado.
- Consultar historico.
- Imprimir reporte de movimiento.
- Filtrar por tipo, movimiento y rango de fecha.

**Requerimientos no funcionales**

- Integridad de stock.
- Costos no editables salvo compra local.
- UI compacta y ordenada.
- Trazabilidad documental.

**Resultados**

- Inventario conectado a ventas y produccion.
- Reportes visibles en pantalla.

### Sprint II - Analisis y diseno

**Casos de uso**

- Operador ingresa productos por compra local.
- Operador registra egreso por merma o venta.
- Operador traslada productos entre bodegas.
- Usuario consulta historico.

**Diagramas sugeridos**

- Flujo de ingreso.
- Flujo de egreso.
- Flujo de traslado.
- Kardex por producto.

**Mockups**

- Pantalla de ingresos y egresos.
- Pestaña de historico.
- Reporte imprimible.

**Arquitectura**

- Router `/inventory/ingresos` y `/inventory/egresos`.
- Calculo de saldos con `_balances_by_bodega`.
- Recalculo global con `_rebuild_global_saldo`.

**Diseño UI**

- Panel principal de movimiento.
- Historico en tab independiente.
- DatePicker visual.
- DataTable empresarial.

**Resultados**

- Diseño enfocado en operacion y trazabilidad.

### Sprint III - Implementacion

**Codificacion**

- `create_ingreso()`.
- `create_egreso()`.
- Validacion de costos segun tipo de ingreso.
- Bloqueo de costo editable en egresos.
- Reporte de movimiento.
- DataTable con exportacion CSV.

**Tecnologias utilizadas**

- FastAPI, SQLAlchemy.
- PrimeVue DataTable, DatePicker, Dialog.

**Capturas sugeridas**

- Ingreso de inventario.
- Egreso de inventario.
- Historico documental.
- Reporte en pantalla.

**Pruebas**

- Ingreso aumenta existencia.
- Egreso disminuye existencia.
- Egreso bloquea stock insuficiente.
- Traslado crea salida e ingreso destino.

**Resultados**

- Control de inventario funcional.

### Sprint IV - Producto funcional

**Evidencias**

- Movimientos registrados.
- Reportes imprimibles.
- Saldos afectados.

**Validacion**

- Ventas consulta existencia real.
- Ingresos alimentan stock disponible.

**Retroalimentacion**

- Se redujeron cajetines grandes.
- Se ordenaron campos de cantidad, costo y total.
- Se acomodo texto de equivalencia USD para no deformar cajas.

**Resultados**

- Modulo operativo para entradas, salidas y traslados.

## Modulo 6 - Ventas POS, pagos, facturacion y combos

### Sprint I - Modelo de negocio y requerimientos

**Problema a resolver**

El punto de venta debe facturar productos disponibles, aplicar pagos, imprimir
ticket y descontar inventario. Tambien debe soportar combos como en
HollywoodPacas: producto principal mas productos incluidos o regalias.

**Objetivos**

- Crear interfaz POS.
- Buscar productos por codigo, barra o descripcion.
- Validar stock antes de facturar.
- Aplicar pagos.
- Generar factura POS.
- Descontar inventario.
- Agregar venta de combos.

**Actividades realizadas**

- Rediseño completo de ventas.
- Control de stock por bodega.
- Modal de pagos compacto.
- Recibo POS en pantalla.
- Fecha fija no editable.
- Bodega/sucursal tomada del usuario.
- Eliminacion de boton Gestion.
- Integracion de vendedores reales.
- Implementacion de combos.

**Requerimientos funcionales**

- Agregar productos al ticket.
- Aumentar cantidad sin exceder existencia.
- Seleccionar cliente y vendedor.
- Registrar pago de contado.
- Permitir credito con saldo pendiente.
- Generar factura POS.
- Aplicar combo con producto principal y productos incluidos.

**Requerimientos no funcionales**

- Interfaz tipo Odoo/POS.
- Flujo rapido por teclado.
- No permitir edicion peligrosa de precio y cantidad en ticket.
- Fecha no editable.
- Bodega no editable desde POS.
- UI responsive.

**Resultados**

- Ventas POS funcional con facturacion e inventario.
- Combos agregados al ticket con agrupacion logica.

### Sprint II - Analisis y diseno

**Casos de uso**

- Vendedor busca producto.
- Vendedor agrega cantidad.
- Sistema valida existencia.
- Vendedor aplica pago.
- Sistema registra factura y descuenta inventario.
- Vendedor aplica combo.

**Diagramas sugeridos**

- Flujo de facturacion POS.
- Flujo de pago.
- Flujo de combo.
- Flujo de descuento de inventario.

**Mockups**

- Terminal de ventas.
- Modal de pago.
- Ticket POS.
- Modal de combo.

**Arquitectura**

- Router `/sales-api`.
- Modelos `sales_invoices`, `sales_invoice_items`, `sales_payments`,
  `sales_sequences`.
- Campos `combo_role` y `combo_group` para identificar lineas de combo.
- Tabla `producto_combos` para configuracion de regalias.

**Diseño UI**

- Ticket compacto.
- Buscador de productos.
- KPIs superiores: factura, fecha, bodega/sucursal y total.
- Modal de pago con foco automatico.
- Boton pequeño `Aplicar combo`.

**Resultados**

- Diseño de flujo POS alineado a operacion real.

### Sprint III - Implementacion

**Codificacion**

- Registro de factura POS en backend.
- Consecutivo `POS`.
- Registro de pagos.
- Egreso de inventario tipo `Venta`.
- Validacion de stock con `_balances_by_bodega`.
- Recibo POS con datos de empresa.
- Modal de combos en ventas.
- Endpoints de combos en inventario.
- Servicios `fetchProductCombo`, `saveProductComboItem`,
  `deleteProductComboItem`.

**Tecnologias utilizadas**

- FastAPI, SQLAlchemy.
- Vue 3, PrimeVue Dialog, Button, Tag, Select.

**Capturas sugeridas**

- Pantalla de ventas.
- Boton `Aplicar combo`.
- Modal de combo.
- Modal de pagos.
- Recibo POS.

**Pruebas**

- Facturar producto con existencia.
- Intentar facturar sin existencia.
- Registrar pago con Enter.
- Generar recibo POS.
- Agregar combo al ticket.
- Verificar lineas `Combo` e `Incluido`.

**Resultados**

- Facturacion POS funcional.
- Combos se facturan como grupo: la linea principal lleva el precio y las
  lineas incluidas descuentan inventario con precio cero.

### Sprint IV - Producto funcional

**Evidencias**

- Ticket actual muestra productos agregados.
- Factura POS se genera y muestra recibo.
- Venta descuenta inventario.
- Combo se agrega al ticket.

**Validacion**

- Build frontend correcto.
- Compilacion backend correcta.
- Verificacion manual en `/app/sales`.

**Retroalimentacion**

- Se retiro texto excesivo del boton de combos.
- El boton queda limitado a `Aplicar combo`.
- Se solicito modal mas compacto y letra mas pequeña.

**Resultados**

- POS listo para pruebas operativas con ventas normales y combos.

## Modulo 7 - Apertura de pacas y produccion especializada

### Sprint I - Modelo de negocio y requerimientos

**Problema a resolver**

El negocio de pacas necesita registrar la apertura de una o varias pacas,
descargar la existencia origen, ingresar la clasificacion resultante en una
bodega destino y generar informe de costo, valor producido, ganancia o perdida.

Una de las problematicas mas grandes del modelo HollywoodPacas es el registro
de mercaderia procesada despues de abrir pacas. Al abrir, filtrar y clasificar
ropa directa se obtienen productos de diferentes calidades, cantidades y valor
comercial. Esa clasificacion determina si la produccion recupera el costo de
la paca o si genera perdida.

La regla de negocio principal es comparar el costo total de las pacas abiertas
contra el valor total de los productos resultantes. Si el costo de origen es
mayor que el valor clasificado, el resultado es perdida. Si el valor
clasificado es mayor que el costo de origen, el resultado es ganancia. Si ambos
valores son equivalentes, el resultado queda en equilibrio.

Tambien se requiere porcentualizar la ropa obtenida por cada producto
clasificado. Por ejemplo: cuanto porcentaje de la paca termino en primera
calidad, segunda calidad, seleccion especial, desperdicio u otra categoria.
Este control permite medir rendimiento, calidad real de la mercaderia,
recuperacion de costo, margen, merma, ganancia y perdida por cada apertura.

**Objetivos**

- Replicar metodologia de HollywoodPacas para apertura de pacas.
- Permitir varias pacas origen.
- Validar existencia de pacas antes de producir.
- Definir bodega origen y bodega destino.
- Usar tasa de cambio vigente no editable.
- Generar reporte visible/imprimible.
- Registrar la clasificacion de productos resultantes por calidad o categoria.
- Calcular el porcentaje que representa cada producto clasificado dentro del
  total procesado.
- Determinar ganancia o perdida comparando costo de origen contra valor
  resultante.
- Reducir calculos manuales que historicamente complican el proceso de
  apertura y clasificacion.

**Actividades realizadas**

- Revision de logica de HollywoodPacas.
- Creacion de modelos de apertura de pacas.
- Creacion de endpoints de apertura y reporte.
- UI especifica para apertura.
- Documentacion del problema de clasificacion de ropa procesada.
- Definicion del calculo de rendimiento porcentual por producto resultante.
- Definicion del calculo de resultado economico: ganancia, perdida o
  equilibrio.
- Historico de aperturas separado en pestaña.
- Validacion de existencia por bodega.

**Requerimientos funcionales**

- Seleccionar bodega origen.
- Seleccionar bodega destino.
- Agregar una o varias pacas origen.
- Registrar productos resultantes.
- Calcular costos y totales.
- Registrar cantidad clasificada por cada producto resultante.
- Calcular porcentaje de participacion de cada producto clasificado.
- Calcular valor total producido a partir de cantidades resultantes y valores
  comerciales.
- Calcular diferencia entre costo de pacas origen y valor producido.
- Clasificar el resultado como ganancia, perdida o equilibrio.
- Generar reporte.
- Reimprimir historico.

**Requerimientos no funcionales**

- Tasa no editable.
- Costos no editables salvo cantidad.
- Mensajes claros de validacion.
- UI compacta.
- Control de inventario obligatorio.
- Calculos financieros transparentes y auditables.
- La clasificacion debe ser comprensible para usuarios operativos sin depender
  de hojas externas.
- El reporte debe mostrar rendimiento porcentual y resultado economico.

**Resultados**

- Apertura de pacas implementada con afectacion de inventario.
- Problematica de clasificacion, rendimiento, ganancia y perdida documentada
  como eje critico del modulo.

### Sprint II - Analisis y diseno

**Casos de uso**

- Usuario selecciona paca origen.
- Sistema muestra existencia y costo.
- Usuario define cantidad a abrir.
- Usuario registra productos resultantes.
- Usuario clasifica la mercaderia procesada por producto/calidad.
- Sistema calcula porcentaje de cada clasificacion sobre el total obtenido.
- Sistema compara costo de origen contra valor resultante.
- Sistema determina si la apertura produjo ganancia, perdida o equilibrio.
- Sistema genera egreso origen e ingreso destino.
- Sistema muestra reporte.

**Diagramas sugeridos**

- Flujo de apertura de paca.
- Diagrama de movimiento origen/destino.
- Diagrama de costos de produccion.
- Diagrama de clasificacion de mercaderia procesada.
- Diagrama de calculo de rendimiento porcentual.
- Diagrama de resultado financiero: costo origen vs valor clasificado.

**Mockups**

- Formulario de apertura.
- Grid de pacas origen.
- Grid de resultados.
- Resumen de porcentajes por producto clasificado.
- Panel de ganancia/perdida de apertura.
- Pestaña de historico.
- Reporte de apertura.

**Arquitectura**

- Endpoints `/inventory/paca-aperturas`.
- Reporte `/inventory/paca-aperturas/{id}/report`.
- Modelos `PacaApertura`, `PacaAperturaOrigen`, `PacaAperturaLinea`.
- Las lineas resultantes deben servir como base para calcular cantidad,
  porcentaje, costo distribuido, valor producido y resultado economico.

**Diseño UI**

- Resumen superior reducido.
- Tabs para apertura e historico.
- DatePicker visual tipo Bootstrap.
- Grids compactos.
- Columnas sugeridas para clasificacion: producto resultante, cantidad,
  costo distribuido, valor estimado, porcentaje sobre total, subtotal y
  observacion.
- Indicadores visuales para resultado: ganancia, perdida o equilibrio.

**Resultados**

- Diseño especializado para proceso de pacas.

### Sprint III - Implementacion

**Codificacion**

- Validacion de existencia antes de abrir.
- Bodega destino configurable; por defecto misma bodega.
- Multiples pacas origen.
- Tasa tomada de tabla de tasas de cambio.
- Costos y precios bloqueados.
- Reporte con costo, valor producido y resultado.
- Calculo de costo total de origen con base en pacas abiertas.
- Calculo de valor producido con base en productos resultantes.
- Preparacion del reporte para mostrar perdida o ganancia segun diferencia.
- Base documental para incorporar porcentualizacion por clasificacion.

**Tecnologias utilizadas**

- FastAPI, SQLAlchemy.
- Vue 3, PrimeVue Tabs/Dialog/DataTable.

**Capturas sugeridas**

- Apertura de pacas.
- Seleccion de bodega destino.
- Grid de pacas origen.
- Historico de aperturas.
- Reporte final.
- Seccion de rendimiento porcentual.
- Seccion de ganancia o perdida.

**Pruebas**

- Intentar abrir paca sin existencia.
- Abrir varias pacas.
- Verificar egreso de origen.
- Verificar ingreso en bodega destino.
- Verificar que el valor resultante se compare contra el costo de origen.
- Verificar que el reporte permita identificar perdida o ganancia.
- Verificar porcentajes de participacion por producto resultante cuando se
  registre clasificacion detallada.
- Consultar reporte.

**Resultados**

- Modulo de apertura de pacas operativo.
- Queda documentada la necesidad de perfeccionar la clasificacion porcentual de
  mercaderia procesada como mejora critica de negocio.

### Sprint IV - Producto funcional

**Evidencias**

- Registro de apertura creado.
- Inventario afectado.
- Reporte visible.
- Reporte con lectura de costo, valor producido y resultado economico.

**Validacion**

- Mensaje de error ajustado: "producto no posee existencia, valide antes de
  registrar la produccion de abiertas de pacas".
- Tasa de cambio bloqueada.
- Cantidad como campo editable principal.
- El resultado debe evidenciar si la produccion recupero el costo de las pacas
  abiertas o si genero perdida.

**Retroalimentacion**

- Se redujeron tarjetas superiores.
- Historico se movio a pestaña independiente.
- Se agrego bodega destino.
- Se identifico que la clasificacion de ropa procesada es el punto mas sensible
  del modulo, porque de ella depende medir calidad, rendimiento, recuperacion de
  costo, perdida y ganancia real.

**Resultados**

- La bitacora deja documentada la clasificacion de productos como componente
  central pendiente de perfeccionamiento y evidencia del reto de diseno del
  modulo.
- Proceso de produccion de pacas alineado a la metodologia solicitada.

## Modulo 8 - Experiencia visual Enterprise

### Sprint I - Modelo de negocio y requerimientos

**Problema a resolver**

La aplicacion necesitaba dejar de verse como prototipo y acercarse a una
experiencia profesional similar a Odoo Enterprise, Zoho One, SAP Business One
Web y Monday.com.

**Objetivos**

- Modernizar layout general.
- Unificar tamaños de textos, botones e inputs.
- Evitar cajas enormes y textos desalineados.
- Crear dashboard con KPIs y graficos.
- Migrar tablas a PrimeVue DataTable donde fuera posible.

**Actividades realizadas**

- Rediseño de sidebar.
- Header superior fijo con breadcrumb.
- PanelMenu y MegaMenu.
- Toast y ConfirmDialog globales.
- Dashboard con ApexCharts.
- Tablas avanzadas en productos, inventario y produccion.

**Requerimientos funcionales**

- Navegacion clara por modulos.
- Dashboard informativo.
- Tablas con paginacion, filtros, ordenamiento y exportacion.
- Formularios con validacion visual.

**Requerimientos no funcionales**

- Diseño responsive.
- Estilo corporativo claro.
- Bordes redondeados y sombras sutiles.
- Espaciado consistente.
- Compatibilidad con Firefox.

**Resultados**

- Sistema con apariencia empresarial mas moderna.

### Sprint II - Analisis y diseno

**Casos de uso**

- Usuario navega por dashboard.
- Usuario consulta productos en DataTable.
- Usuario filtra historico de inventario.
- Usuario recibe confirmaciones y notificaciones.

**Diagramas sugeridos**

- Mapa de navegacion.
- Wireframe del shell principal.
- Diseño del dashboard.

**Mockups**

- Sidebar colapsado/expandido.
- Dashboard.
- DataTable empresarial.
- Formularios compactos.

**Arquitectura**

- Componentes PrimeVue globales.
- CSS centralizado en `frontend/src/style.css`.
- Layout `AppShell.vue`.

**Diseño UI**

- Tema claro violeta/azul oscuro.
- Superficies con contraste suave.
- Inputs compactos.
- Sidebar con logo del comercio.

**Resultados**

- Lineamientos visuales aplicados al sistema.

### Sprint III - Implementacion

**Codificacion**

- Registro global de servicios PrimeVue.
- Dashboard con KPIs y graficos.
- DataTable avanzada.
- CSS global de compactacion.
- Correcciones de DatePicker.
- Correcciones responsive.

**Tecnologias utilizadas**

- PrimeVue DataTable, Dialog, Toast, ConfirmDialog, Tag, Badge, Tabs.
- ApexCharts.
- Bootstrap Icons.

**Capturas sugeridas**

- Dashboard.
- Sidebar.
- Tabla de productos.
- Historico de inventario.
- Ventas POS.

**Pruebas**

- `npm run build`.
- Validacion visual manual.
- Pruebas en Firefox.
- Revision de responsive.

**Resultados**

- UI mas consistente y profesional.

### Sprint IV - Producto funcional

**Evidencias**

- Sidebar con logo.
- Dashboard con graficos.
- Formularios compactos.
- Tablas empresariales.

**Validacion**

- Build frontend correcto.
- Navegacion funcional.

**Retroalimentacion**

- Se realizaron varias rondas de ajuste por textos enormes, recuadros grandes,
  checkbox desalineado, campos de fecha dañados y espacios excesivos.

**Resultados**

- Experiencia visual alineada al objetivo empresarial.

## Modulo 9 - Docker, despliegue local y control de versiones

### Sprint I - Modelo de negocio y requerimientos

**Problema a resolver**

El proyecto debia poder levantarse completo de forma local para desarrollo,
pruebas y futura publicacion, evitando configuraciones manuales repetitivas.

**Objetivos**

- Levantar frontend, backend y base de datos con Docker.
- Usar variables de entorno.
- Facilitar reconstruccion del entorno.
- Publicar cambios en ramas de trabajo.

**Actividades realizadas**

- Creacion de `compose.yaml`.
- Dockerfile para backend.
- Dockerfile para frontend.
- Configuracion de PostgreSQL 16.
- Puertos locales ajustados segun necesidades.
- Publicacion a ramas `main`, `desarrollador-1` y `desarrollador-2`.

**Requerimientos funcionales**

- `docker compose up --build -d`.
- Backend ejecuta migraciones y Uvicorn.
- Frontend ejecuta Vite.
- Base de datos persiste en volumen.

**Requerimientos no funcionales**

- Recarga de codigo en desarrollo.
- Variables configurables.
- Separacion entre servicios.

**Resultados**

- Entorno Docker funcional.

### Sprint II - Analisis y diseno

**Casos de uso**

- Desarrollador levanta sistema.
- Desarrollador reinicia frontend.
- Desarrollador verifica contenedores.
- Desarrollador publica cambios.

**Diagramas sugeridos**

- Diagrama Docker Compose.
- Flujo de desarrollo local.

**Mockups**

- No aplica directamente; evidencias por terminal.

**Arquitectura**

- Servicio `db`.
- Servicio `backend`.
- Servicio `frontend`.
- Volumen para PostgreSQL.
- Volumen de `node_modules`.

**Diseño UI**

- No aplica.

**Resultados**

- Entorno reproducible para desarrollo.

### Sprint III - Implementacion

**Codificacion**

- Variables `.env` y `.env.example`.
- Configuracion de puertos.
- Reinicios y validaciones con Docker.
- Instalacion de dependencias faltantes.

**Tecnologias utilizadas**

- Docker, Docker Compose, npm, Python.

**Capturas sugeridas**

- `docker compose ps`.
- Frontend levantado.
- Backend OpenAPI.

**Pruebas**

- `docker compose ps`.
- `npm run build`.
- `python -m compileall backend/app`.

**Resultados**

- Entorno probado.

### Sprint IV - Producto funcional

**Evidencias**

- Servicios activos.
- Frontend accesible.
- Backend accesible.
- PostgreSQL saludable.

**Validacion**

- Builds correctos.
- Reinicio de frontend cuando no se reflejaban cambios.

**Retroalimentacion**

- Se ajustaron puertos por conflictos locales.
- Se verifico que el navegador estuviera cargando el bundle actual.

**Resultados**

- Flujo local estable para continuar el desarrollo.

## Evidencias tecnicas actuales

### Archivos clave

| Archivo | Uso |
| --- | --- |
| `compose.yaml` | Orquestacion local de servicios |
| `backend/app/main.py` | Inicializacion FastAPI, routers y compatibilidad de esquema |
| `backend/app/models/` | Modelos SQLAlchemy |
| `backend/app/routers/` | Endpoints por modulo |
| `backend/app/schemas/` | Esquemas Pydantic |
| `frontend/src/router/routes.js` | Rutas del frontend |
| `frontend/src/layouts/AppShell.vue` | Layout autenticado |
| `frontend/src/views/sales/SalesView.vue` | Terminal POS |
| `frontend/src/views/inventory/MovementsView.vue` | Ingresos y egresos |
| `frontend/src/views/inventory/PacaOpeningView.vue` | Apertura de pacas |
| `frontend/src/views/settings/BusinessSettingsView.vue` | Datos empresariales |
| `frontend/src/views/users/UsersView.vue` | Usuarios, vendedores y accesos |
| `frontend/src/style.css` | Tema visual global |

### Tablas principales del sistema

- `users`
- `roles`
- `user_roles`
- `sucursales`
- `user_access_profiles`
- `vendedores`
- `business_settings`
- `company_environments`
- `exchange_rates`
- `lineas`
- `segmentos`
- `unidades_medida`
- `marcas`
- `bodegas`
- `proveedores`
- `productos`
- `saldos_productos`
- `productos_recetas`
- `productos_receta_lineas`
- `producto_combos`
- `ingresos_inventario`
- `ingreso_items`
- `egresos_inventario`
- `egreso_items`
- `producciones_inventario`
- `producciones_inventario_lineas`
- `paca_aperturas`
- `paca_apertura_origenes`
- `paca_apertura_lineas`
- `sales_invoices`
- `sales_invoice_items`
- `sales_payments`
- `sales_sequences`

### Metodos y procesos importantes

- `_balances_by_bodega()`: calcula existencias por bodega.
- `_rebuild_global_saldo()`: reconstruye saldo global.
- `_current_exchange_rate_query()`: obtiene tasa vigente.
- `_require_exchange_rate()`: valida tasa para moneda USD.
- `create_ingreso()`: registra entradas de inventario.
- `create_egreso()`: registra salidas y traslados.
- `create_invoice()`: registra factura POS, pagos y egreso por venta.
- `create_paca_apertura()`: registra apertura de pacas con egreso e ingreso.
- `get_product_combo()`: consulta productos incluidos en un combo.
- `save_product_combo_item()`: registra o actualiza item incluido de combo.

## Pendientes recomendados para siguientes sprints

### Seguridad y arquitectura

- Crear migraciones Alembic completas.
- Retirar cambios de esquema desde `main.py`.
- Proteger endpoints con autenticacion y permisos.
- Configurar CORS restringido.
- Definir politica de contraseñas.

### Ventas y caja

- Crear catalogos reales de formas de pago, bancos y cuentas.
- Implementar apertura y cierre de caja.
- Agregar consecutivo fiscal y PDF formal.
- Crear modulo de cobranza y depositos.

### Inventario

- Implementar anulacion controlada de movimientos.
- Crear historial de cambios de costo.
- Agregar pruebas automatizadas de ingresos, egresos, ventas y pacas.

### UI/UX

- Continuar migracion de formularios a PrimeVue Enterprise.
- Agregar skeleton/loading en todas las vistas.
- Reducir bundle con imports dinamicos.
- Agregar pruebas responsive E2E.

### Documentacion

- Actualizar `BASEDEDATOS.md` con tablas recientes de combos y apertura de
  pacas si no estan completamente descritas.
- Actualizar `API.md` con endpoints recientes.
- Agregar capturas reales por sprint.
- Crear diagramas ERD, casos de uso y arquitectura.
