# ERP System

## Desarrollo con Docker

El entorno incluye PostgreSQL, el backend FastAPI y el frontend Vue/Vite. Los
cambios del codigo fuente se reflejan automaticamente durante el desarrollo.
El backend aplica las migraciones pendientes de Alembic antes de iniciar.

### Requisitos

- Docker Desktop con Docker Compose

### Iniciar el proyecto

```powershell
docker compose up --build
```

Servicios disponibles:

- Frontend: http://127.0.0.1:5174
- Backend: http://127.0.0.1:8001
- Documentacion API: http://127.0.0.1:8001/docs
- PostgreSQL: `127.0.0.1:5433`

Para ejecutar los servicios en segundo plano:

```powershell
docker compose up --build -d
docker compose logs -f
```

### Comandos utiles

```powershell
# Detener los contenedores conservando los datos
docker compose down

# Aplicar manualmente las migraciones pendientes
docker compose exec backend alembic upgrade head

# Reiniciar completamente la base de datos local
docker compose down -v
docker compose up --build
```

Los datos de PostgreSQL se conservan en el volumen `postgres_data`. Para cambiar
credenciales o puertos, copia `.env.example` como `.env` y ajusta sus valores.

El script `run_dev.ps1` sigue disponible para desarrollo local sin Docker.
