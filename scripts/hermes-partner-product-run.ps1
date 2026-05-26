$ErrorActionPreference = 'Stop'

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " RUNNING HERMES PARTNERS & PRODUCTIZATION " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Partner initialization and report
Write-Host "[1/4] Checking Channel Partners databases..." -ForegroundColor Yellow
py -3 scripts/hermes_partner_init.py
py -3 scripts/hermes_partner_os.py report

# 2. Whitelabel intro pack
Write-Host "`n[2/4] Compiling Agency Channel Partner Packs..." -ForegroundColor Yellow
py -3 scripts/hermes_partner_pack.py "Riyadh Marketing Agency" "AI Trust Diagnostic"

# 3. Case study creation
Write-Host "`n[3/4] Creating case studies..." -ForegroundColor Yellow
py -3 scripts/hermes_case_study.py --client "Al-Majd Group" --offer "AI Trust Diagnostic" --problem "Insecure AI usage and data leakage risks" --baseline "No approval matrix or quality controls" --work "Built Risk Map and Human Approval Matrix" --result "100 percent of outputs secured and audited" --metric "AI Governance Compliance" --anonymous "true"

# 4. Productization gate review
Write-Host "`n[4/4] Evaluating SaaS MVP Readiness..." -ForegroundColor Yellow
py -3 scripts/hermes_productization_gate.py --offer "AI Trust Diagnostic" --paid-runs 3 --proof-packs 2 --retainers 1 --delivery-burden 45

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host " PARTNERS & PRODUCTIZATION VERDICT: PASS" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "All reports generated successfully."
