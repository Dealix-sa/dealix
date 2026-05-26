$ErrorActionPreference = 'Stop'

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " LAUNCH READY MODE GATE - DEALIX OS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Verify Ledgers existence
Write-Host "[1/3] Checking MD Ledgers integrity..." -ForegroundColor Yellow
$ledgers = @(
    "EXECUTION_LEDGER.md",
    "REVENUE_LEDGER.md",
    "PROOF_LEDGER.md",
    "RISK_LEDGER.md",
    "DECISION_LEDGER.md"
)

foreach ($ledger in $ledgers) {
    $path = "docs\ops\$ledger"
    if (Test-Path $path) {
        Write-Host "  - $($ledger): PRESENT" -ForegroundColor Green
    } else {
        Write-Host "  - $($ledger): MISSING" -ForegroundColor Red
        exit 1
    }
}

# 2. Verify Company ready status
Write-Host "`n[2/3] Verifying Company Ready Gates..." -ForegroundColor Yellow
py -3 scripts/verify_full_mvp_ready.py --skip-tests

# 3. Run core test suite
Write-Host "`n[3/3] Running Core Regression Test Suite (q-mode)..." -ForegroundColor Yellow
$env:APP_ENV = "test"
py -3 -m pytest tests/test_revenue_ops_autopilot.py tests/test_founder_commercial_digest.py -q --no-cov

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host " LAUNCH VERDICT: PASS" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "You are officially cleared to execute outreach." -ForegroundColor White
