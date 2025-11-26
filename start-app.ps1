# Script para levantar toda la aplicación Gastiflow
# Ejecuta la API, el bot de Telegram y el frontend

Write-Host "🚀 Iniciando Gastiflow..." -ForegroundColor Cyan

# Verificar si .venv existe
if (-not (Test-Path ".\backend\.venv")) {
    Write-Host "❌ Error: No se encontró el ambiente virtual en .\backend\.venv" -ForegroundColor Red
    Write-Host "Por favor, crea el ambiente virtual primero con: python -m venv backend\.venv" -ForegroundColor Yellow
    exit 1
}

# Verificar si node_modules existe
if (-not (Test-Path ".\frontend\node_modules")) {
    Write-Host "⚠️ node_modules no encontrado. Instalando dependencias del frontend..." -ForegroundColor Yellow
    Push-Location frontend
    npm install
    Pop-Location
}

# Array para almacenar los procesos
$jobs = @()

# Función para limpiar procesos al salir
function Cleanup {
    Write-Host "`n🛑 Deteniendo todos los servicios..." -ForegroundColor Yellow
    
    # Detener todos los jobs
    $jobs | ForEach-Object {
        if ($_ -and $_.State -eq 'Running') {
            Stop-Job -Job $_
            Remove-Job -Job $_
        }
    }
    
    Write-Host "✅ Servicios detenidos. ¡Hasta luego!" -ForegroundColor Green
    exit 0
}

# Registrar el evento de Ctrl+C
Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup }

try {
    # 1. Iniciar la API
    Write-Host "`n📡 Iniciando API (puerto 8000)..." -ForegroundColor Green
    $apiJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        Set-Location backend
        & .\.venv\Scripts\Activate.ps1
        uvicorn web.main:app --reload --port 8000
    }
    $jobs += $apiJob
    Start-Sleep -Seconds 2
    
    # 2. Iniciar el bot de Telegram
    Write-Host "🤖 Iniciando Bot de Telegram..." -ForegroundColor Green
    $botJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        Set-Location backend
        & .\.venv\Scripts\Activate.ps1
        python run_bot.py
    }
    $jobs += $botJob
    Start-Sleep -Seconds 2
    
    # 3. Iniciar el frontend
    Write-Host "🎨 Iniciando Frontend (puerto 3000)..." -ForegroundColor Green
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        Set-Location frontend
        npm run dev
    }
    $jobs += $frontendJob
    
    Write-Host "`n✅ Todos los servicios iniciados!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "📡 API:      http://localhost:8000" -ForegroundColor White
    Write-Host "📚 Docs:     http://localhost:8000/docs" -ForegroundColor White
    Write-Host "🎨 Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "`n💡 Presiona Ctrl+C para detener todos los servicios`n" -ForegroundColor Yellow
    
    # Mostrar logs en tiempo real
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Verificar si algún job falló
        foreach ($job in $jobs) {
            if ($job.State -eq 'Failed') {
                Write-Host "`n❌ Un servicio falló. Detalles:" -ForegroundColor Red
                Receive-Job -Job $job
                Cleanup
            }
        }
        
        # Mostrar output de los jobs
        $jobs | ForEach-Object {
            if ($_.HasMoreData) {
                Receive-Job -Job $_ | ForEach-Object {
                    Write-Host $_ -ForegroundColor Gray
                }
            }
        }
    }
}
catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
    Cleanup
}
finally {
    Cleanup
}
