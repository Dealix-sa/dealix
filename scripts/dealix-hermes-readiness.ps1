param(
  [string]$Model = "qwen3:4b"
)

$ErrorActionPreference = "Stop"

Write-Host "===================================================================="
Write-Host " Dealix/Hermes Readiness Runner"
Write-Host "===================================================================="

if (Test-Path ".\scripts\dealix-local-ai-env.ps1") {
  . .\scripts\dealix-local-ai-env.ps1 -Model $Model
}

Write-Host ""
Write-Host "1) File Audit"
py -3 .\scripts\dealix_ultimate_file_audit.py
if ($LASTEXITCODE -ne 0) {
  Write-Host "File audit found missing files. Continue to runtime check for partial diagnosis."
}

Write-Host ""
Write-Host "2) Runtime Check"
py -3 .\scripts\dealix_ultimate_runtime_check.py
if ($LASTEXITCODE -ne 0) {
  Write-Host "Runtime check found issues. Review reports/readiness."
}

Write-Host ""
Write-Host "3) Benefit Map"
py -3 .\scripts\dealix_benefit_map.py
if ($LASTEXITCODE -ne 0) { throw "Benefit map failed" }

Write-Host ""
Write-Host "4) Optional launch/operator/core partner runs if present"

if (Test-Path ".\scripts\dealix-operator-day.ps1") {
  powershell -ExecutionPolicy Bypass -File .\scripts\dealix-operator-day.ps1 -Model $Model
}

if (Test-Path ".\scripts\hermes-core-run.ps1") {
  powershell -ExecutionPolicy Bypass -File .\scripts\hermes-core-run.ps1 -Model $Model
}

if (Test-Path ".\scripts\hermes-partner-product-run.ps1") {
  powershell -ExecutionPolicy Bypass -File .\scripts\hermes-partner-product-run.ps1
}

Write-Host ""
Write-Host "DEALIX_HERMES_READINESS_RUNNER=PASS"
Write-Host "Open:"
Write-Host "  reports\readiness"
Write-Host "  reports\founder"
Write-Host "  reports\operator"
Write-Host "  reports\hermes"
Write-Host "  reports\partners"
