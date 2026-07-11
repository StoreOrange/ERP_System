#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="${APP_DIR:-/home/ubuntu/Documents/universidad/ERP_System}"
REMOTE="${REMOTE:-origin}"
BRANCH="${BRANCH:-main}"
LOCK_FILE="${LOCK_FILE:-/tmp/erp-system-update.lock}"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

cd "$APP_DIR"

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  log "Otra actualizacion esta en ejecucion."
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  log "git no esta instalado."
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  log "docker no esta instalado."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  log "docker compose no esta disponible."
  exit 1
fi

if [ ! -f .env ]; then
  log "No existe .env; creando desde .env.example."
  cp .env.example .env
fi

if [ -n "$(git status --porcelain)" ]; then
  log "Hay cambios locales sin commit en $APP_DIR. No se actualiza para no sobrescribirlos."
  git status --short
  exit 1
fi

log "Descargando cambios desde $REMOTE/$BRANCH."
git fetch "$REMOTE" "$BRANCH"
git checkout "$BRANCH"
git pull --ff-only "$REMOTE" "$BRANCH"

log "Construyendo y levantando servicios."
docker compose up --build -d --remove-orphans

log "Estado de contenedores."
docker compose ps

log "Actualizacion completada."
