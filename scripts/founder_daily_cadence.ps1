param(
    [switch]$Evening,
    [switch]$Quick
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if ($Evening) {
    if (Test-Path "scripts/founder_evening_evidence.py") {
        py -3 scripts/founder_evening_evidence.py
    }
    exit $LASTEXITCODE
}

Write-Host "== Founder daily cadence (morning) =="
py -3 scripts/founder_agent_queue_status.py --seed-today
if ($Quick -and (Test-Path "scripts/run_ceo_operating_stack.ps1")) {
    & (Join-Path $PSScriptRoot "run_ceo_operating_stack.ps1") -Quick -SkipRailway
} elseif (Test-Path "scripts/run_ceo_operating_stack.ps1") {
    & (Join-Path $PSScriptRoot "run_ceo_operating_stack.ps1") -SkipRailway
}
Write-Host "Review: /ar/ops/approvals"
