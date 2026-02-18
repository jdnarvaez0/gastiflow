#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Gastiflow Health Check Script
.DESCRIPTION
    Verifies that all services are running correctly
.EXAMPLE
    .\health-check.ps1
#>

param(
    [string]$ApiUrl = "http://localhost:8000",
    [string]$FrontendUrl = "http://localhost:3000",
    [switch]$Detailed
)

$ErrorActionPreference = "SilentlyContinue"

# Colors
$Green = "`e[32m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$Cyan = "`e[36m"
$Reset = "`e[0m"

function Write-Status($message) {
    Write-Host "${Cyan}[CHECK]${Reset} $message"
}

function Write-Success($message) {
    Write-Host "${Green}[OK]${Reset} $message"
}

function Write-Warning($message) {
    Write-Host "${Yellow}[WARN]${Reset} $message"
}

function Write-Error($message) {
    Write-Host "${Red}[FAIL]${Reset} $message"
}

function Test-Endpoint($url, $name) {
    try {
        $response = Invoke-RestMethod -Uri $url -Method GET -TimeoutSec 5
        return $true
    }
    catch {
        return $false
    }
}

# ==================== Header ====================
Write-Host ""
Write-Host "${Cyan}╔════════════════════════════════════════════════╗${Reset}"
Write-Host "${Cyan}║${Reset}     🏥 Gastiflow Health Check                 ${Cyan}║${Reset}"
Write-Host "${Cyan}╚════════════════════════════════════════════════╝${Reset}"
Write-Host ""

# ==================== System Checks ====================
Write-Status "Checking system components..."
Write-Host ""

$checks = @{}

# Check Backend API
Write-Host "Backend API ($ApiUrl)... " -NoNewline
if (Test-Endpoint "$ApiUrl/api/health" "API") {
    Write-Success "Running"
    $checks["Backend API"] = $true
    
    if ($Detailed) {
        try {
            $health = Invoke-RestMethod -Uri "$ApiUrl/api/health" -TimeoutSec 5
            Write-Host "    Version: $($health.version)"
            Write-Host "    Status: $($health.status)"
            Write-Host "    Environment: $($health.environment)"
        }
        catch {}
    }
}
else {
    Write-Error "Not responding"
    $checks["Backend API"] = $false
}

# Check Frontend
Write-Host "Frontend ($FrontendUrl)... " -NoNewline
if (Test-Endpoint $FrontendUrl "Frontend") {
    Write-Success "Running"
    $checks["Frontend"] = $true
}
else {
    Write-Error "Not responding"
    $checks["Frontend"] = $false
}

# Check Database (via API)
Write-Host "Database Connection... " -NoNewline
try {
    $dbHealth = Invoke-RestMethod -Uri "$ApiUrl/api/health" -TimeoutSec 5
    if ($dbHealth.status -eq "healthy") {
        Write-Success "Connected"
        $checks["Database"] = $true
    }
    else {
        Write-Error "Issues detected"
        $checks["Database"] = $false
    }
}
catch {
    Write-Error "Cannot check"
    $checks["Database"] = $false
}

# Check Environment Variables
Write-Host "Environment Configuration... " -NoNewline
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    $required = @("JWT_SECRET_KEY", "DATABASE_URL", "GEMINI_API_KEY")
    $missing = $required | Where-Object { $envContent -notmatch "^$_=.+$" }
    
    if ($missing.Count -eq 0) {
        Write-Success "Valid"
        $checks["Environment"] = $true
    }
    else {
        Write-Warning "Missing: $($missing -join ', ')"
        $checks["Environment"] = $false
    }
}
else {
    Write-Error ".env not found"
    $checks["Environment"] = $false
}

# Check Telegram Bot (if running)
Write-Host "Telegram Bot... " -NoNewline
$botProcess = Get-Process -Name "python" -ErrorAction SilentlyContinue | 
    Where-Object { $_.CommandLine -like "*run_bot.py*" }
if ($botProcess) {
    Write-Success "Running (PID: $($botProcess.Id))"
    $checks["Telegram Bot"] = $true
}
else {
    Write-Warning "Not running (optional)"
    $checks["Telegram Bot"] = $false
}

# Check Docker Services (if using Docker)
if (Get-Command "docker" -ErrorAction SilentlyContinue) {
    Write-Host "Docker Services... " -NoNewline
    $containers = docker ps --format "{{.Names}}" 2>$null
    if ($containers -match "gastiflow") {
        Write-Success "Running"
        $checks["Docker"] = $true
        
        if ($Detailed) {
            Write-Host ""
            docker ps --filter "name=gastiflow" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | 
                ForEach-Object { Write-Host "    $_" }
            Write-Host ""
        }
    }
    else {
        Write-Warning "Not running"
        $checks["Docker"] = $false
    }
}

# ==================== Summary ====================
Write-Host ""
Write-Host "${Cyan}══════════════════════════════════════════════════${Reset}"

$passed = ($checks.Values | Where-Object { $_ -eq $true }).Count
$total = $checks.Count

if ($passed -eq $total) {
    Write-Success "All systems operational ($passed/$total)"
    $exitCode = 0
}
elseif ($passed -ge ($total / 2)) {
    Write-Warning "Most systems operational ($passed/$total)"
    $exitCode = 0
}
else {
    Write-Error "Multiple systems down ($passed/$total)"
    $exitCode = 1
}

Write-Host "${Cyan}══════════════════════════════════════════════════${Reset}"
Write-Host ""

# ==================== Troubleshooting ====================
if ($checks["Backend API"] -eq $false) {
    Write-Host "${Yellow}Troubleshooting Backend:${Reset}"
    Write-Host "  1. Check if Python venv exists: Test-Path backend/.venv"
    Write-Host "  2. Start manually: cd backend; .venv\Scripts\uvicorn web.main:app --reload"
    Write-Host "  3. Check logs for errors"
    Write-Host ""
}

if ($checks["Frontend"] -eq $false) {
    Write-Host "${Yellow}Troubleshooting Frontend:${Reset}"
    Write-Host "  1. Check if node_modules exists: Test-Path frontend/node_modules"
    Write-Host "  2. Install dependencies: cd frontend; npm install"
    Write-Host "  3. Start manually: cd frontend; npm run dev"
    Write-Host ""
}

if ($checks["Database"] -eq $false) {
    Write-Host "${Yellow}Troubleshooting Database:${Reset}"
    Write-Host "  1. Verify DATABASE_URL in .env"
    Write-Host "  2. Check if PostgreSQL is running"
    Write-Host "  3. Using Docker? Run: docker-compose up -d db"
    Write-Host ""
}

# ==================== Quick Actions ====================
Write-Host "${Cyan}Quick Actions:${Reset}"
Write-Host "  Start all:     task dev"
Write-Host "  Start Docker:  docker-compose up -d"
Write-Host "  View logs:     task docker:logs"
Write-Host "  Run tests:     task test"
Write-Host ""

exit $exitCode
