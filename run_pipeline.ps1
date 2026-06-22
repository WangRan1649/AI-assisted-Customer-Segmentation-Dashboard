$ErrorActionPreference = "Stop"

Write-Host "=============================================="
Write-Host "V3 AI-assisted BI Decision Workflow Pipeline"
Write-Host "=============================================="

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$PythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$RawDataDir = Join-Path $ProjectRoot "data\raw"
$RawCsvFiles = Get-ChildItem -Path $RawDataDir -Filter "*.csv" -File -ErrorAction SilentlyContinue

if (!$RawCsvFiles -or $RawCsvFiles.Count -eq 0) {
    Write-Host "ERROR: No raw CSV files found under data\raw."
    Write-Host "Put your e-commerce CSV file(s) under: $RawDataDir"
    exit 1
}

if (!(Test-Path $PythonPath)) {
    Write-Host "Virtual environment not found. Creating .venv..."
    python -m venv .venv
}

Write-Host ""
Write-Host "[1/2] Installing or checking Python dependencies..."
& $PythonPath -m pip install -r requirements.txt

Write-Host ""
Write-Host "[2/2] Running V3 pipeline..."
& $PythonPath run_pipeline.py

Write-Host ""
Write-Host "Next step: Open Power BI and click Home -> Refresh."
