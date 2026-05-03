$ErrorActionPreference = "Stop"
$requiredPythonVersion = "3.11"

function Test-PortInUse {
    param([int]$Port)

    return $null -ne (Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue)
}

function Get-FreePort {
    param([int]$StartPort)

    $port = $StartPort
    while (Test-PortInUse -Port $port) {
        $port++
    }

    return $port
}

function Test-PythonModule {
    param(
        [string]$PythonExe,
        [string]$ModuleName
    )

    try {
        & $PythonExe -c "import $ModuleName" 1>$null 2>$null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

function Get-PythonVersion {
    param([string]$PythonExe)

    try {
        return (& $PythonExe -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null).Trim()
    }
    catch {
        return $null
    }
}

function New-BackendVenv {
    param(
        [string]$BackendPath,
        [string]$PythonVersion
    )

    $venvPath = Join-Path $BackendPath "venv"
    $resolvedBackendPath = (Resolve-Path $BackendPath).Path

    if (Test-Path $venvPath) {
        $resolvedVenvPath = (Resolve-Path $venvPath).Path
        if ($resolvedVenvPath -ne (Join-Path $resolvedBackendPath "venv")) {
            throw "Ruta inesperada para el entorno virtual: $resolvedVenvPath"
        }

        Remove-Item -LiteralPath $resolvedVenvPath -Recurse -Force
    }

    & py "-$PythonVersion" -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo crear el entorno virtual con Python $PythonVersion"
    }
}

function Stop-TrackedProcess {
    param([string]$PidFile)

    if (-not (Test-Path $PidFile)) {
        return
    }

    $oldPid = Get-Content $PidFile -ErrorAction SilentlyContinue
    if ($oldPid) {
        $proc = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
        if ($proc) {
            Stop-Process -Id $oldPid -Force
        }
    }

    Remove-Item $PidFile -ErrorAction SilentlyContinue
}

function Get-PortProcessInfo {
    param([int]$Port)

    $connection = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue |
        Select-Object -First 1

    if (-not $connection) {
        return $null
    }

    $owningPid = $connection.OwningProcess
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $owningPid" -ErrorAction SilentlyContinue
    if (-not $process) {
        return [pscustomobject]@{
            ProcessId = $owningPid
            Name = "desconocido"
            CommandLine = ""
        }
    }

    return [pscustomobject]@{
        ProcessId = $process.ProcessId
        Name = $process.Name
        CommandLine = $process.CommandLine
    }
}

Write-Host "==============================================="
Write-Host "   ERP SYSTEM - ENTORNO DE DESARROLLO"
Write-Host "   Backend (FastAPI) + Frontend (Vue)"
Write-Host "==============================================="
Write-Host ""

$root = $PSScriptRoot
$backendPath = Join-Path $root "backend"
$frontendPath = Join-Path $root "frontend"
$pythonExe = Join-Path $backendPath "venv\Scripts\python.exe"
$npmCmd = (Get-Command npm.cmd -ErrorAction Stop).Source
$backendPreferredPort = 8000
$backendPort = Get-FreePort -StartPort $backendPreferredPort
$frontendPort = Get-FreePort -StartPort 5173
$devPath = Join-Path $root ".dev"
$logPath = Join-Path $devPath "logs"
$backendPidFile = Join-Path $devPath "backend.pid"
$frontendPidFile = Join-Path $devPath "frontend.pid"
$backendOutLog = Join-Path $logPath "backend.out.log"
$backendErrLog = Join-Path $logPath "backend.err.log"
$frontendOutLog = Join-Path $logPath "frontend.out.log"
$frontendErrLog = Join-Path $logPath "frontend.err.log"
$frontendEnvFile = Join-Path $frontendPath ".env.development.local"

New-Item -ItemType Directory -Force -Path $logPath | Out-Null
Stop-TrackedProcess -PidFile $frontendPidFile
Remove-Item $backendPidFile -ErrorAction SilentlyContinue

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: No se encontro el launcher 'py' de Python." -ForegroundColor Red
    exit 1
}

$installedPythons = ((& py -0p 2>$null) | Out-String)
if ($installedPythons -notmatch [regex]::Escape("-V:$requiredPythonVersion")) {
    Write-Host "ERROR: Python $requiredPythonVersion no esta instalado." -ForegroundColor Red
    Write-Host "Instala Python $requiredPythonVersion y vuelve a ejecutar el script." -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $pythonExe)) {
    Write-Host "Creando entorno virtual del backend con Python $requiredPythonVersion..." -ForegroundColor Yellow
    New-BackendVenv -BackendPath $backendPath -PythonVersion $requiredPythonVersion
}
else {
    $currentVenvVersion = Get-PythonVersion -PythonExe $pythonExe
    if ($currentVenvVersion -ne $requiredPythonVersion) {
        Write-Host "El entorno virtual actual usa Python $currentVenvVersion. Recreando con Python $requiredPythonVersion..." -ForegroundColor Yellow
        New-BackendVenv -BackendPath $backendPath -PythonVersion $requiredPythonVersion
    }
}

if ($backendPort -ne $backendPreferredPort) {
    Write-Host "AVISO: El puerto $backendPreferredPort esta ocupado." -ForegroundColor Yellow
    $portProcess = Get-PortProcessInfo -Port $backendPreferredPort
    if ($portProcess) {
        Write-Host "Proceso actual: PID $($portProcess.ProcessId) | $($portProcess.Name)" -ForegroundColor Yellow
        if ($portProcess.CommandLine) {
            Write-Host "Comando: $($portProcess.CommandLine)" -ForegroundColor DarkYellow
        }
    }
    Write-Host "Se usara el puerto alterno $backendPort para el backend." -ForegroundColor Yellow
}

Write-Host "Verificando dependencias del BACKEND..."
$pythonExe = Join-Path $backendPath "venv\Scripts\python.exe"
if (-not (Test-PythonModule -PythonExe $pythonExe -ModuleName "uvicorn")) {
    Write-Host "Instalando dependencias de backend..." -ForegroundColor Yellow
    & $pythonExe -m pip install -r (Join-Path $backendPath "requirements.txt")
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: No se pudieron instalar las dependencias del backend." -ForegroundColor Red
        exit 1
    }
}

if (-not (Test-Path (Join-Path $frontendPath "node_modules"))) {
    Write-Host "Instalando dependencias del FRONTEND..." -ForegroundColor Yellow
    Push-Location $frontendPath
    try {
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: No se pudieron instalar las dependencias del frontend." -ForegroundColor Red
            exit 1
        }
    }
    finally {
        Pop-Location
    }
}

Set-Content -Path $frontendEnvFile -Value "VITE_API_BASE_URL=http://127.0.0.1:$backendPort"

Write-Host "Iniciando FRONTEND (Vue + Vite) en segundo plano..."
$frontendProc = Start-Process `
    -FilePath $npmCmd `
    -ArgumentList "run", "dev", "--", "--host", "127.0.0.1", "--port", $frontendPort `
    -WorkingDirectory $frontendPath `
    -RedirectStandardOutput $frontendOutLog `
    -RedirectStandardError $frontendErrLog `
    -WindowStyle Hidden `
    -PassThru
Set-Content -Path $frontendPidFile -Value $frontendProc.Id

Write-Host ""
Write-Host "==============================================="
Write-Host " Frontend iniciado en segundo plano"
Write-Host " Frontend VUE: http://127.0.0.1:$frontendPort"
Write-Host " Logs frontend: $frontendOutLog"
Write-Host " API Backend configurada para frontend: http://127.0.0.1:$backendPort"
if ($frontendPort -ne 5173) {
    Write-Host " Nota: 5173 estaba ocupado, Vite se movio a $frontendPort" -ForegroundColor Yellow
}
Write-Host " Backend: se iniciara en esta misma terminal"
Write-Host " Para detener todo usa Ctrl+C aqui"
Write-Host "==============================================="

try {
    Push-Location $backendPath
    Write-Host ""
    Write-Host "Iniciando BACKEND (FastAPI) en primer plano..." -ForegroundColor Cyan
    Write-Host "Backend: http://127.0.0.1:$backendPort" -ForegroundColor Cyan
    & $pythonExe -m uvicorn app.main:app --reload --host 127.0.0.1 --port $backendPort
}
finally {
    Pop-Location
    Stop-TrackedProcess -PidFile $frontendPidFile
    Remove-Item $backendPidFile -ErrorAction SilentlyContinue
    Remove-Item $frontendEnvFile -ErrorAction SilentlyContinue
    Write-Host ""
    Write-Host "Servicios detenidos." -ForegroundColor Yellow
}
