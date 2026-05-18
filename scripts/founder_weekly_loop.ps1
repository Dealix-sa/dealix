# Founder weekly loop — Windows (see founder_weekly_loop.sh)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "== Founder operating system =="
& "$PSScriptRoot\verify_founder_operating_system.ps1"

Write-Host "== Commercial launch readiness =="
py -3 scripts/verify_commercial_launch_ready.py

Write-Host "== Strongest plan checklist =="
py -3 scripts/founder_strongest_plan_status.py

Write-Host "== Comprehensive plan =="
py -3 scripts/founder_comprehensive_plan_status.py

Write-Host "== Dogfooding war room =="
py -3 scripts/founder_dogfooding_war_room_sync.py

Write-Host "FOUNDER_WEEKLY_LOOP=PASS"
