param(
  [string]$Model = "qwen3:4b"
)

$ErrorActionPreference = "Stop"

Write-Host "===================================================================="
Write-Host " Dealix Revenue Execution Lock"
Write-Host "===================================================================="

if (Test-Path ".\scripts\dealix-local-ai-env.ps1") {
  . .\scripts\dealix-local-ai-env.ps1 -Model $Model
}

Write-Host ""
Write-Host "1) Backup / guard"
if (Test-Path ".\scripts\ledger_guard.py") {
  py -3 .\scripts\ledger_guard.py
}
if (Test-Path ".\scripts\backup_ledgers.py") {
  py -3 .\scripts\backup_ledgers.py
}

Write-Host ""
Write-Host "2) Revenue dashboard"
py -3 .\scripts\revenue_lock_dashboard.py
if ($LASTEXITCODE -ne 0) { throw "revenue dashboard failed" }

Write-Host ""
Write-Host "3) Proposal to payment plan"
py -3 .\scripts\proposal_to_payment_plan.py
if ($LASTEXITCODE -ne 0) { throw "proposal to payment failed" }

Write-Host ""
Write-Host "4) Collection queue"
py -3 .\scripts\build_collection_queue.py
if ($LASTEXITCODE -ne 0) { throw "collection queue failed" }

Write-Host ""
Write-Host "5) Existing operator / Hermes if available"
if (Test-Path ".\scripts\dealix-operator-day.ps1") {
  powershell -ExecutionPolicy Bypass -File .\scripts\dealix-operator-day.ps1 -Model $Model
}

if (Test-Path ".\scripts\hermes-core-run.ps1") {
  powershell -ExecutionPolicy Bypass -File .\scripts\hermes-core-run.ps1 -Model $Model
}

Write-Host ""
Write-Host "DEALIX_REVENUE_EXECUTION_LOCK=PASS"
Write-Host "Open:"
Write-Host "  reports\revenue_lock"
Write-Host "  reports\collections"
Write-Host "  local_ai\collections"
