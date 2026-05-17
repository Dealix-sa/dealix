# Founder commercial morning — canonical (Windows)
param(
    [switch]$DryRun,
    [switch]$WithBusinessNow,
    [switch]$Full
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
function Invoke-DealixPy {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    if ($env:PY) { & $env:PY @Args } else { & py -3 @Args }
}
$Date = Get-Date -Format "yyyy-MM-dd"

if ($Full) {
    $WithBusinessNow = $true
    $env:DEALIX_SYNC_EVIDENCE = "1"
}

if ($DryRun) {
    Invoke-DealixPy scripts/founder_revenue_day_runner.py --dry-run
    exit $LASTEXITCODE
}

Write-Host "== Dealix Founder Commercial Day (canonical) =="

$dailyArgs = @()
if (-not $env:DEALIX_ADMIN_API_KEY) { $dailyArgs += "--skip-api" } else { $dailyArgs += "--api-only" }
Write-Host "`n== 0/7 Dealix daily ops (bridge + health) =="
Invoke-DealixPy scripts/run_dealix_daily_ops.py @dailyArgs

Write-Host "`n== 1/7 Founder daily brief =="
Invoke-DealixPy scripts/dealix_founder_daily_brief.py --out "data/founder_briefs/brief_$Date.md"

Write-Host "`n== 2/7 KPI commercial status =="
Invoke-DealixPy scripts/apply_kpi_founder_commercial.py --status

if ($WithBusinessNow -and (Test-Path "scripts/run_business_now.ps1")) {
    Write-Host "`n== optional: Business NOW =="
    & powershell -File scripts/run_business_now.ps1
}

Write-Host "`n== 3/8 War Room sync =="
Invoke-DealixPy scripts/commercial_war_room_sync.py

Write-Host "`n== 4/8 War Room CSV import =="
if ($env:DEALIX_ADMIN_API_KEY) {
    if (-not $env:DEALIX_API_BASE) { $env:DEALIX_API_BASE = $env:DEALIX_API_URL }
    if (-not $env:DEALIX_API_BASE) { $env:DEALIX_API_BASE = "http://localhost:8000" }
    Invoke-DealixPy scripts/import_war_room_targets.py --apply --via-api
    if ($LASTEXITCODE -ne 0) { Invoke-DealixPy scripts/import_war_room_targets.py --apply }
} else {
    Invoke-DealixPy scripts/import_war_room_targets.py --apply
}

Write-Host "`n== 5/8 Commercial digest =="
$sync = @()
if ($env:DEALIX_SYNC_EVIDENCE -eq "1") { $sync += "--sync-evidence"; $sync += "--pull-evidence" }
Invoke-DealixPy scripts/founder_commercial_digest.py --out "data/founder_briefs/commercial_$Date.md" @sync

Write-Host "`n== 5b/9 War Room touch drafts =="
Invoke-DealixPy scripts/generate_war_room_touch_drafts.py --top-n 10

Write-Host "`n== 6/9 Social queue =="
Invoke-DealixPy scripts/social_queue_today.py

Write-Host "`n== 7/9 AEO + verdict =="
Invoke-DealixPy scripts/founder_revenue_day_runner.py --skip-substeps

Write-Host "`n== 8/9 Social queue expand 12w =="
Invoke-DealixPy scripts/expand_social_queue_12w.py

Write-Host "`nFOUNDER_COMMERCIAL_DAY: OK"
Write-Host "Soft launch: py -3 scripts/verify_commercial_launch_ready.py"
Write-Host "Docs: docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md"
