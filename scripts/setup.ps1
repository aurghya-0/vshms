<#
.SYNOPSIS
    One-command development setup for VSHMS on Windows.

.DESCRIPTION
    Installs uv if it is missing, then Python 3.12+ and every project package at the locked
    versions, creates the local development database and runs the full check.
    Safe to run again at any time: it only installs what is missing.
    Full guide: docs\SETUP.md

.PARAMETER Run
    After setup, start the app at http://127.0.0.1:8710.

.PARAMETER Yes
    Install uv without asking if it is missing.

.PARAMETER SkipChecks
    Skip lint, type check and tests (faster).

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
    powershell -ExecutionPolicy Bypass -File scripts\setup.ps1 -Run
#>
[CmdletBinding()]
param(
    [switch]$Run,
    [switch]$Yes,
    [switch]$SkipChecks
)

$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

function Write-Step([string]$Message) {
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Stop-Setup([string]$Message) {
    Write-Host ""
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

# Runs a native command. Windows PowerShell 5.1 can turn a program's normal stderr output
# (uv and uvicorn log there) into an error when errors are set to stop, so errors are relaxed
# for the call and the exit code is checked instead.
function Invoke-Native([string]$Command, [string[]]$Arguments) {
    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try { & $Command @Arguments } finally { $ErrorActionPreference = $previous }
}

# Same, but throws if the command fails (PowerShell does not do this by itself).
function Invoke-Checked([string]$Command, [string[]]$Arguments) {
    Invoke-Native $Command $Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed (exit code $LASTEXITCODE): $Command $($Arguments -join ' ')"
    }
}

Write-Step 'Checking git'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Stop-Setup 'git is not installed. Install Git for Windows (https://git-scm.com/download/win), open a new terminal, then run this script again.'
}
git --version

Write-Step 'Checking uv (installs Python and all packages for us)'
# uv's installer puts it in %USERPROFILE%\.local\bin, which may not be on PATH yet in this window.
$uvDir = Join-Path $env:USERPROFILE '.local\bin'
if (Test-Path $uvDir) { $env:Path = "$uvDir;$env:Path" }
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host 'uv is not installed.'
    $install = $Yes.IsPresent
    if (-not $install) {
        try {
            $answer = Read-Host 'Install uv now from https://astral.sh/uv/install.ps1? [Y/n]'
            $install = ($answer -eq '' -or $answer -match '^[Yy]')
        } catch {
            $install = $false
        }
    }
    if (-not $install) {
        Stop-Setup 'uv is required. Install it from https://docs.astral.sh/uv/getting-started/installation/ or run: scripts\setup.ps1 -Yes'
    }
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    if (Test-Path $uvDir) { $env:Path = "$uvDir;$env:Path" }
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Stop-Setup 'uv was installed but is not on PATH. Open a new terminal and run this script again.'
    }
}
uv --version

try {
    Write-Step 'Installing Python 3.12+ and all project packages (locked versions)'
    Invoke-Checked 'uv' @('sync', '--locked')

    Write-Step 'Creating the local development database'
    Invoke-Checked 'uv' @('run', 'alembic', 'upgrade', 'head')
} catch {
    Stop-Setup "$($_.Exception.Message)`nSee docs\SETUP.md, Troubleshooting, or ask your mentor."
}

if (-not $SkipChecks) {
    Write-Step 'Running the full check: lint, format, types, tests'
    try {
        Invoke-Checked 'uv' @('run', 'ruff', 'check', '.')
        Invoke-Checked 'uv' @('run', 'ruff', 'format', '--check', '.')
        Invoke-Checked 'uv' @('run', 'mypy')
        Invoke-Checked 'uv' @('run', 'pytest', '--cov')
    } catch {
        Stop-Setup "Setup finished, but the checks failed: $($_.Exception.Message)`nFix that before you start (see docs\SETUP.md, Troubleshooting) or ask your mentor."
    }
} else {
    Write-Step 'Skipping checks (-SkipChecks)'
}

Write-Host ''
Write-Host 'All set. Useful commands (always prefix with "uv run"):'
Write-Host '  uv run uvicorn vshms.main:create_app --factory --reload --port 8710   start the app'
Write-Host '  uv run pytest -m "not integration and not slow"                       quick tests'
Write-Host '  uv run ruff check . ; uv run ruff format --check . ; uv run mypy ; uv run pytest --cov   full check'
Write-Host 'Next: read docs\SETUP.md and CONTRIBUTING.md, then pick up your starter task.'

if ($Run) {
    Write-Step 'Starting the app at http://127.0.0.1:8710 (Ctrl+C to stop)'
    Invoke-Native 'uv' @('run', 'uvicorn', 'vshms.main:create_app', '--factory', '--reload', '--port', '8710')
}
