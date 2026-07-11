#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="${APP_DIR:-/home/ubuntu/Documents/universidad/ERP_System}"
SERVICE_NAME="${SERVICE_NAME:-erp-system}"
UPDATE_SERVICE_NAME="${UPDATE_SERVICE_NAME:-erp-system-update}"

if [ "$(id -u)" -ne 0 ]; then
  echo "Ejecuta este instalador con sudo."
  exit 1
fi

cd "$APP_DIR"

install -m 0755 deploy/update_erp.sh /usr/local/bin/update-erp-system
git config --global --add safe.directory "$APP_DIR" >/dev/null 2>&1 || true
git config --system --add safe.directory "$APP_DIR" >/dev/null 2>&1 || true

sed "s|__APP_DIR__|$APP_DIR|g; s|__SERVICE_NAME__|$SERVICE_NAME|g" \
  deploy/systemd/erp-system.service >/etc/systemd/system/"$SERVICE_NAME".service

sed "s|__APP_DIR__|$APP_DIR|g; s|__UPDATE_SCRIPT__|/usr/local/bin/update-erp-system|g" \
  deploy/systemd/erp-system-update.service >/etc/systemd/system/"$UPDATE_SERVICE_NAME".service

systemctl daemon-reload
systemctl enable "$SERVICE_NAME".service

if [ ! -f "$APP_DIR/.env" ]; then
  cp "$APP_DIR/.env.example" "$APP_DIR/.env"
  chown ubuntu:ubuntu "$APP_DIR/.env" 2>/dev/null || true
fi

echo "Servicios instalados:"
echo "  sudo systemctl start $SERVICE_NAME"
echo "  sudo systemctl start $UPDATE_SERVICE_NAME"
echo ""
echo "Antes de produccion, revisa $APP_DIR/.env y cambia JWT_SECRET_KEY y POSTGRES_PASSWORD."
