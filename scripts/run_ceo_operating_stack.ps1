# CEO operating stack — agent fleet + cadence + Railway verify (Windows)
param(
    [switch]$Quick,
    [switch]$SkipRailway
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not $env:DEALIX_API_BASE) { $env:DEALIX_API_BASE = "https://api.dealix.me" }

Write-Host "== CEO operating stack =="
py -3 scripts/founder_agent_queue_status.py --seed-today

if (Test-Path "scripts/run_founder_agent_fleet_rhythm.ps1") {
    & (Join-Path $PSScriptRoot "run_founder_agent_fleet_rhythm.ps1")
}

$cadence = Join-Path $PSScriptRoot "founder_daily_cadence.ps1"
if (Test-Path $cadence) {
    if ($Quick) { & $cadence -Quick } else { & $cadence }
}

if (-not $SkipRailway) {
    py -3 scripts/verify_railway_production_config.py --api-base $env:DEALIX_API_BASE
}

Write-Host "CEO_OPERATING_STACK=OK"
