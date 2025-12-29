# Script para levantar toda la aplicación Gastiflow
# Ejecuta la API, el bot de Telegram y el frontend

Write-Host "🚀 Iniciando Gastiflow..." -ForegroundColor Cyan

# Obtener el directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Paths importantes
$backendDir = Join-Path $scriptDir "backend"
$frontendDir = Join-Path $scriptDir "frontend"
$venvPython = Join-Path $backendDir ".venv\Scripts\python.exe"
$venvUvicorn = Join-Path $backendDir ".venv\Scripts\uvicorn.exe"

# Verificar si .venv existe
if (-not (Test-Path $venvPython)) {
    Write-Host "❌ Error: No se encontró el ambiente virtual en $backendDir\.venv" -ForegroundColor Red
    Write-Host "Por favor, crea el ambiente virtual primero con: python -m venv backend\.venv" -ForegroundColor Yellow
    exit 1
}

# Verificar si node_modules existe
if (-not (Test-Path "$frontendDir\node_modules")) {
    Write-Host "⚠️ node_modules no encontrado. Instalando dependencias del frontend..." -ForegroundColor Yellow
    Push-Location $frontendDir
    npm install
    Pop-Location
}

# Función para matar procesos existentes de Gastiflow
function Stop-ExistingProcesses {
    Write-Host "🔍 Verificando procesos existentes..." -ForegroundColor Yellow
    
    # Buscar y matar procesos de python que estén ejecutando run_bot.py o uvicorn con gastiflow
    $pythonProcesses = Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" | 
        Where-Object { $_.CommandLine -like "*gastiflow*" }
    
    if ($pythonProcesses) {
        Write-Host "   ⚠️ Encontrados procesos Python de Gastiflow. Deteniendo..." -ForegroundColor Yellow
        foreach ($proc in $pythonProcesses) {
            try {
                Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
                Write-Host "   ✓ Detenido proceso $($proc.ProcessId)" -ForegroundColor Gray
            } catch {
                # Ignorar errores si el proceso ya terminó
            }
        }
        Start-Sleep -Seconds 2
    }
    
    # También buscar node processes relacionados con gastiflow
    $nodeProcesses = Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" | 
        Where-Object { $_.CommandLine -like "*gastiflow*" }
    
    if ($nodeProcesses) {
        Write-Host "   ⚠️ Encontrados procesos Node de Gastiflow. Deteniendo..." -ForegroundColor Yellow
        foreach ($proc in $nodeProcesses) {
            try {
                Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
                Write-Host "   ✓ Detenido proceso $($proc.ProcessId)" -ForegroundColor Gray
            } catch {
                # Ignorar errores
            }
        }
        Start-Sleep -Seconds 1
    }
    
    Write-Host "   ✅ Verificación completada" -ForegroundColor Green
}

# Array para almacenar los procesos
$global:processes = @()

# Función para limpiar procesos al salir
function Cleanup {
    Write-Host "`n🛑 Deteniendo todos los servicios..." -ForegroundColor Yellow
    
    foreach ($proc in $global:processes) {
        if ($proc -and -not $proc.HasExited) {
            try {
                # Matar el proceso y sus hijos
                $procId = $proc.Id
                Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
                
                # También matar procesos hijos
                Get-CimInstance Win32_Process -Filter "ParentProcessId = $procId" | ForEach-Object {
                    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
                }
            } catch {
                # Ignorar errores
            }
        }
    }
    
    Write-Host "✅ Servicios detenidos. ¡Hasta luego!" -ForegroundColor Green
}

# Registrar el handler de Ctrl+C
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup } -ErrorAction SilentlyContinue

# Matar procesos existentes antes de iniciar
Stop-ExistingProcesses

try {
    # 1. Iniciar la API
    Write-Host "`n📡 Iniciando API (puerto 8000)..." -ForegroundColor Green
    $apiProcess = Start-Process -FilePath $venvPython -ArgumentList "-m", "uvicorn", "web.main:app", "--reload", "--port", "8000" -WorkingDirectory $backendDir -PassThru -NoNewWindow
    $global:processes += $apiProcess
    Start-Sleep -Seconds 3
    
    # 2. Iniciar el bot de Telegram
    Write-Host "🤖 Iniciando Bot de Telegram..." -ForegroundColor Green
    $botProcess = Start-Process -FilePath $venvPython -ArgumentList "run_bot.py" -WorkingDirectory $backendDir -PassThru -NoNewWindow
    $global:processes += $botProcess
    Start-Sleep -Seconds 3
    
    # 3. Iniciar el frontend
    Write-Host "🎨 Iniciando Frontend (puerto 3000)..." -ForegroundColor Green
    $frontendProcess = Start-Process -FilePath "npm.cmd" -ArgumentList "run", "dev" -WorkingDirectory $frontendDir -PassThru -NoNewWindow
    $global:processes += $frontendProcess
    
    Write-Host "`n✅ Todos los servicios iniciados!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "📡 API:      http://localhost:8000" -ForegroundColor White
    Write-Host "📚 Docs:     http://localhost:8000/docs" -ForegroundColor White
    Write-Host "🎨 Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "`n💡 Presiona Ctrl+C para detener todos los servicios`n" -ForegroundColor Yellow
    
    # Monitorear los procesos
    while ($true) {
        Start-Sleep -Seconds 2
        
        # Verificar si algún proceso crítico terminó
        $apiRunning = -not $apiProcess.HasExited
        $botRunning = -not $botProcess.HasExited
        $frontendRunning = -not $frontendProcess.HasExited
        
        if (-not $apiRunning) {
            Write-Host "❌ La API se ha detenido inesperadamente" -ForegroundColor Red
            break
        }
        
        if (-not $botRunning) {
            Write-Host "❌ El Bot se ha detenido inesperadamente" -ForegroundColor Red
            break
        }
        
        if (-not $frontendRunning) {
            Write-Host "❌ El Frontend se ha detenido inesperadamente" -ForegroundColor Red
            break
        }
    }
}
catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
}
finally {
    Cleanup
}
