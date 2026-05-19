$ErrorActionPreference = "Stop"

Write-Host "========================================"
Write-Host "AI-assisted Customer Segmentation Pipeline"
Write-Host "========================================"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$PythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$RawDataPath = Join-Path $ProjectRoot "data\raw\ecommerce_user_behavior_dataset.csv"

if (!(Test-Path $RawDataPath)) {
    Write-Host "ERROR: Raw data file not found."
    Write-Host "Expected path: $RawDataPath"
    exit 1
}

if (!(Test-Path $PythonPath)) {
    Write-Host "Virtual environment not found. Creating .venv..."
    python -m venv .venv
}

Write-Host ""
Write-Host "[1/4] Installing or checking Python dependencies..."
& $PythonPath -m pip install -r requirements.txt

Write-Host ""
Write-Host "[2/4] Generating processed business data from raw dataset..."
& $PythonPath llm_agent\src\prepare_processed_data.py

Write-Host ""
Write-Host "[3/4] Generating AI insights and Power BI insight CSV..."
& $PythonPath llm_agent\src\insight_generator.py

Write-Host ""
Write-Host "[4/4] Pipeline completed successfully."

Write-Host ""
Write-Host "Generated files:"
Write-Host "- data\processed\customer_segments.csv"
Write-Host "- data\processed\cross_dimensional_insights.csv"
Write-Host "- llm_agent\outputs\segment_insights.md"
Write-Host "- llm_agent\outputs\powerbi_llm_insights.csv"

Write-Host ""
Write-Host "Next step: Open Power BI and click Home -> Refresh."