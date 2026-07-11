#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="${APP_DIR:-/home/ubuntu/Documents/universidad/ERP_System}"
DUMP_FILE="${1:-/home/ubuntu/inventario_local.sql}"
BACKUP_FILE="${BACKUP_FILE:-/home/ubuntu/backup_erp_antes_inventario_$(date '+%Y%m%d_%H%M%S').sql}"

cd "$APP_DIR"

if [ ! -f "$DUMP_FILE" ]; then
  echo "No existe el archivo de importacion: $DUMP_FILE"
  exit 1
fi

echo "Creando backup completo en $BACKUP_FILE"
docker compose exec -T db pg_dump -U user -d ERPDB >"$BACKUP_FILE"

echo "Limpiando inventario actual en nube"
docker compose exec -T db psql -U user -d ERPDB <<'SQL'
TRUNCATE TABLE
  paca_apertura_lineas,
  paca_apertura_origenes,
  paca_aperturas,
  producciones_inventario_lineas,
  producciones_inventario,
  producto_combos,
  productos_receta_lineas,
  productos_recetas,
  egreso_items,
  egresos_inventario,
  ingreso_items,
  ingresos_inventario,
  saldos_productos,
  productos,
  proveedores,
  marcas,
  bodegas,
  ingreso_tipos,
  egreso_tipos,
  unidades_medida,
  segmentos,
  lineas
RESTART IDENTITY CASCADE;
SQL

echo "Importando inventario desde $DUMP_FILE"
docker compose exec -T db psql -U user -d ERPDB <"$DUMP_FILE"

echo "Reiniciando backend y frontend"
docker compose restart backend frontend

echo "Importacion completada"
