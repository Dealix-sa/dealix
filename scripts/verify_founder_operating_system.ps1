# Verify Founder Operating System (Windows)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Py = if ($env:PY) { $env:PY } else { "python" }
$Fail = 0

Write-Host "== 1/2 Founder commercial day dry-run =="
& powershell -File scripts/run_founder_commercial_day.ps1 -DryRun
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Host "`n== 2/2 pytest bundle =="
$tests = @(
  "tests/test_founder_revenue_day_script.py",
  "tests/test_targeting_rotation.py",
  "tests/test_generate_weekly_content_drafts.py",
  "tests/test_commercial_ops_digest.py"
)
& $Py -m pytest @tests -q --no-cov
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

if ($Fail -eq 0) {
  Write-Host "`nFOUNDER_OPERATING_SYSTEM_VERDICT=PASS"
  exit 0
}
Write-Host "`nFOUNDER_OPERATING_SYSTEM_VERDICT=FAIL"
exit 1
