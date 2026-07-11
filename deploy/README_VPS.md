# Despliegue en VPS

Ruta esperada:

```bash
/home/ubuntu/Documents/universidad/ERP_System
```

## Primera instalacion

```bash
cd /home/ubuntu/Documents/universidad/ERP_System
git fetch --all
git checkout main
git pull --ff-only origin main
sudo bash deploy/install_vps.sh
sudo nano .env
sudo systemctl start erp-system
```

En `.env`, cambia al menos `JWT_SECRET_KEY` y `POSTGRES_PASSWORD`.

## Actualizar despues de enviar cambios a Git

```bash
sudo systemctl start erp-system-update
```

Tambien se puede ejecutar directo:

```bash
sudo APP_DIR=/home/ubuntu/Documents/universidad/ERP_System REMOTE=origin BRANCH=main update-erp-system
```

## Ver estado y logs

```bash
sudo systemctl status erp-system
docker compose ps
docker compose logs -f backend frontend
```

## Puertos por defecto

Los puertos salen de `.env`:

- Frontend: `FRONTEND_PORT`, por defecto `5310`
- Backend: `BACKEND_PORT`, por defecto `8010`
- PostgreSQL: `POSTGRES_PORT`, por defecto `5433`
