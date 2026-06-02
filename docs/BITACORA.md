# Bitacora del proyecto ERP System

Ultima actualizacion: 2026-06-02

## Objetivo

Construir un ERP empresarial modular para Orange Tec tomando como base funcional
el sistema HollywoodPacas. Integra autenticacion, inventario, produccion,
configuracion empresarial y una interfaz de ventas en evolucion.

## Historial verificado

### 2025-12-02 - Version inicial desde VPS

Commit: `ffadcd3`

- Estructura inicial con FastAPI, SQLAlchemy, Alembic, Vue y Vite.
- Modelos `users`, `roles` y relacion N:N `user_roles`.
- Registro, login y migracion inicial
  `5285f6b056a5_create_users_and_roles.py`.

### 2026-05-03 - Port de HollywoodPacas y UI modular

Commit: `ebc7966`

- Port de catalogos, productos, saldos, movimientos, kardex, recetas y
  produccion.
- Configuracion empresarial, logos y entornos de empresa.
- Script `backend/scripts/import_hollpacas_inventory.py`.
- Nuevo shell Vue con dashboard, usuarios, productos, inventario, produccion,
  ventas y configuraciones.
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
- Orden CSS corregido: Bootstrap antes del tema ERP.
- Login, ventas, inputs, botones y PrimeVue auditados desde navegador.

### 2026-06-02 - Documentacion consolidada

- Esquema verificado directamente contra PostgreSQL.
- Confirmadas 24 tablas fisicas y 29 claves foraneas.
- Confirmadas 43 operaciones OpenAPI.
- Documentacion actualizada:
  - `docs/BITACORA.md`
  - `docs/SISTEMA.md`
  - `docs/PENDIENTES.md`
  - `docs/BASEDEDATOS.md`
  - `docs/API.md`

## Validacion actual

- `docker compose ps`: base saludable, backend y frontend activos.
- `docker compose exec -T frontend npm run build`: correcto.
- `git diff --check`: correcto.
- PostgreSQL consultado directamente.
- OpenAPI consultado desde `http://127.0.0.1:8001/openapi.json`.
