#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Gastiflow Development Environment Setup Script
.DESCRIPTION
    Automates the setup of development environment for Gastiflow
.EXAMPLE
    .\setup.ps1
#>

param(
    [switch]$SkipBackend,
    [switch]$SkipFrontend,
    [switch]$SkipDocker,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# Colors
$Green = "`e[32m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$Reset = "`e[0m"

function Write-Status($message) {
    Write-Host "${Green}[SETUP]${Reset} $message"
}

function Write-Warning($message) {
    Write-Host "${Yellow}[WARNING]${Reset} $message"
}

function Write-Error($message) {
    Write-Host "${Red}[ERROR]${Reset} $message"
}

function Test-Command($command) {
    return [bool](Get-Command -Name $command -ErrorAction SilentlyContinue)
}

function Test-PythonVersion {
    try {
        $version = python --version 2>&1
        if ($version -match "Python 3\.(\d+)") {
            $minorVersion = [int]$matches[1]
            return $minorVersion -ge 10
        }
        return $false
    }
    catch {
        return $false
    }
}

# ==================== Prerequisites Check ====================
Write-Status "Checking prerequisites..."

$checks = @{
    "Python 3.10+" = { Test-PythonVersion }
    "Node.js" = { Test-Command "node" }
    "npm" = { Test-Command "npm" }
    "Git" = { Test-Command "git" }
}

$missing = @()
foreach ($check in $checks.GetEnumerator()) {
    Write-Host "Checking $($check.Key)... " -NoNewline
    if (& $check.Value) {
        Write-Host "${Green}✓${Reset}"
    }
    else {
        Write-Host "${Red}✗${Reset}"
        $missing += $check.Key
    }
}

if ($missing.Count -gt 0) {
    Write-Error "Missing prerequisites: $($missing -join ', ')"
    Write-Host ""
    Write-Host "Please install:"
    Write-Host "  - Python 3.10+: https://www.python.org/downloads/"
    Write-Host "  - Node.js 18+: https://nodejs.org/"
    Write-Host "  - Git: https://git-scm.com/downloads"
    exit 1
}

# ==================== Environment File ====================
Write-Status "Setting up environment file..."

if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Warning "Created .env from .env.example - Please edit it with your actual values!"
    }
    else {
        Write-Error ".env.example not found"
        exit 1
    }
}
else {
    Write-Warning ".env already exists, skipping..."
}

# ==================== Backend Setup ====================
if (-not $SkipBackend) {
    Write-Status "Setting up backend..."
    
    Set-Location backend
    
    # Create virtual environment
    if ((-not (Test-Path ".venv")) -or $Force) {
        Write-Status "Creating Python virtual environment..."
        python -m venv .venv
    }
    else {
        Write-Warning "Virtual environment already exists (use -Force to recreate)"
    }
    
    # Install dependencies
    Write-Status "Installing Python dependencies..."
    & .venv\Scripts\pip.exe install --upgrade pip
    & .venv\Scripts\pip.exe install -r requirements.txt
    
    # Install dev dependencies
    Write-Status "Installing development dependencies..."
    & .venv\Scripts\pip.exe install pytest pytest-asyncio flake8 black
    
    Set-Location ..
    Write-Status "Backend setup complete!"
}
else {
    Write-Warning "Skipping backend setup"
}

# ==================== Frontend Setup ====================
if (-not $SkipFrontend) {
    Write-Status "Setting up frontend..."
    
    Set-Location frontend
    
    # Check Node version
    $nodeVersion = node --version
    Write-Status "Node.js version: $nodeVersion"
    
    # Install dependencies
    Write-Status "Installing npm packages..."
    npm install
    
    Set-Location ..
    Write-Status "Frontend setup complete!"
}
else {
    Write-Warning "Skipping frontend setup"
}

# ==================== Docker Setup (Optional) ====================
if (-not $SkipDocker) {
    if (Test-Command "docker") {
        Write-Status "Docker detected. Pulling images..."
        docker pull postgres:15-alpine
        docker pull redis:7-alpine
    }
    else {
        Write-Warning "Docker not found. Skipping Docker setup."
    }
}

# ==================== Git Hooks (Optional) ====================
Write-Status "Setting up Git hooks..."

$preCommitHook = @'
#!/bin/sh
# Pre-commit hook for Gastiflow

echo "Running pre-commit checks..."

# Check Python syntax
cd backend
.venv\Scripts\python -m py_compile web/main.py
if [ $? -ne 0 ]; then
    echo "❌ Python syntax error"
    exit 1
fi

echo "✅ Pre-commit checks passed"
'@

if (Test-Path ".git") {
    $preCommitHook | Out-File -FilePath ".git\hooks\pre-commit" -Encoding utf8 -NoNewline
    # Git bash requires unix line endings
    $content = Get-Content ".git\hooks\pre-commit" -Raw
    $content = $content -replace "`r`n", "`n"
    Set-Content ".git\hooks\pre-commit" $content -NoNewline
}

# ==================== Summary ====================
Write-Host ""
Write-Host "${Green}========================================${Reset}"
Write-Host "${Green}  🎉 Gastiflow Setup Complete!${Reset}"
Write-Host "${Green}========================================${Reset}"
Write-Host ""
Write-Host "Next steps:"
Write-Host ""
Write-Host "1. ${Yellow}Configure environment:${Reset}"
Write-Host "   Edit .env with your API keys and settings"
Write-Host ""
Write-Host "2. ${Yellow}Start development:${Reset}"
Write-Host "   # Option A: Using Task (recommended)"
Write-Host "   task dev"
Write-Host ""
Write-Host "   # Option B: Manual start"
Write-Host "   cd backend; .venv\Scripts\uvicorn web.main:app --reload"
Write-Host "   cd backend; .venv\Scripts\python run_bot.py"
Write-Host "   cd frontend; npm run dev"
Write-Host ""
Write-Host "   # Option C: Using Docker"
Write-Host "   docker-compose -f docker-compose.yml -f docker-compose.override.yml up"
Write-Host ""
Write-Host "3. ${Yellow}Run tests:${Reset}"
Write-Host "   task test"
Write-Host ""
Write-Host "4. ${Yellow}Documentation:${Reset}"
Write-Host "   - API docs: http://localhost:8000/docs"
Write-Host "   - Frontend: http://localhost:3000"
Write-Host ""

# Check if Task is installed
if (-not (Test-Command "task")) {
    Write-Warning "Task is not installed. Install it for easier development:"
    Write-Host "   winget install Task.Task" -ForegroundColor Cyan
    Write-Host "   # or visit: https://taskfile.dev/installation/"
    Write-Host ""
}
