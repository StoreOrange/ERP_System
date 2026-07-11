param(
    [string]$OutputPath = ".dev/inventario_local.sql"
)

$ErrorActionPreference = "Stop"

$tables = @(
    "lineas",
    "segmentos",
    "unidades_medida",
    "marcas",
    "bodegas",
    "proveedores",
    "ingreso_tipos",
    "egreso_tipos",
    "productos",
    "saldos_productos",
    "producto_combos",
    "productos_recetas",
    "productos_receta_lineas",
    "ingresos_inventario",
    "ingreso_items",
    "egresos_inventario",
    "egreso_items"
)

$outputDirectory = Split-Path -Parent $OutputPath
if ($outputDirectory -and !(Test-Path $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null
}

$tableArgs = @()
foreach ($table in $tables) {
    $tableArgs += "-t"
    $tableArgs += $table
}

docker compose exec -T db pg_dump `
    -U user `
    -d ERPDB `
    --data-only `
    --column-inserts `
    @tableArgs `
    | Set-Content -Path $OutputPath -Encoding UTF8

Write-Host "Inventario exportado en $OutputPath"
