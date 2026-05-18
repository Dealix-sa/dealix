param([switch]$Weekly, [switch]$SkipRailway)
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$py = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "py -3" }
Write-Host "== Founder agent fleet rhythm =="
& $py scripts/founder_soaen_daily.py --out "data/founder_briefs/soaen_$((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd')).md"
& $py scripts/founder_agent_queue_status.py --seed-today --unified
& $py scripts/verify_soaen_loop.py
& $py scripts/founder_gtm_proof_loop.py
if (-not $SkipRailway) {
  & $py scripts/verify_railway_production_config.py --skip-live --ui-start-command "./start.sh" --ui-predeploy 'echo "no migration needed"'
}
if ($Weekly) {
  & $py scripts/founder_weekly_board_init.py --write
  & $py scripts/founder_agent_weekly_learning.py --seed-quarterly
  & $py scripts/founder_agent_weekly_learning.py --apply-hints
}
Write-Host "FOUNDER_AGENT_FLEET_RHYTHM=OK"
