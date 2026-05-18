# Paid launch gate — after soft motion
param([string]$ApiBase = $env:DEALIX_API_BASE)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
if (-not $ApiBase) { $ApiBase = "https://api.dealix.me" }
$env:DEALIX_API_BASE = $ApiBase

py -3 scripts/verify_soft_launch_motion.py
if ($LASTEXITCODE -ne 0) { exit 1 }

py -3 scripts/verify_production_soft_launch.py
if ($LASTEXITCODE -ne 0) { exit 1 }

if (Test-Path "scripts/verify_paid_launch_readiness.py") {
    py -3 scripts/verify_paid_launch_readiness.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "PAID_LAUNCH_GATE=INCOMPLETE (Moyasar env)"
        exit 2
    }
}

Write-Host "PAID_LAUNCH_GATE=READY"
exit 0
