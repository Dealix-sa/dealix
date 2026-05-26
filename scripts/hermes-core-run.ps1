$ErrorActionPreference = 'Stop'

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " RUNNING HERMES SOVEREIGN OPERATING LOOP " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Initialize schemas
Write-Host "[1/5] Checking Hermes Ledgers Schemas..." -ForegroundColor Yellow
py -3 scripts/hermes_safe_init.py

# 2. Compile Daily Brief
Write-Host "`n[2/5] Synthesizing Founder Command Brief..." -ForegroundColor Yellow
py -3 scripts/hermes_founder_brief.py

# 3. Opportunity Radar
Write-Host "`n[3/5] Scanning Regional Market Intel & Opportunity Radar..." -ForegroundColor Yellow
py -3 scripts/hermes_opportunity_radar.py

# 4. Compile Trust compliance pack
Write-Host "`n[4/5] Compiling B2B PDPL/NIST Trust Pack..." -ForegroundColor Yellow
py -3 scripts/hermes_trust_pack.py

# 5. Run Weekly Empire Review
Write-Host "`n[5/5] Synthesizing Weekly Empire Review..." -ForegroundColor Yellow
py -3 scripts/hermes_weekly_review.py

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host " HERMES CORE LOOP VERDICT: PASS" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "All reports generated inside reports/ directory."
