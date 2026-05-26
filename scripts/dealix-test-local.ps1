$ErrorActionPreference = "Stop"
$root = Resolve-Path "$PSScriptRoot\.."
Set-Location $root

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " DEALIX LOCAL TEST" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

py -3 ".\dealix-v2\dealix_os\cli.py" doctor
py -3 ".\dealix-v2\dealix_os\cli.py" services
py -3 ".\dealix-v2\dealix_os\cli.py" governance-check "we guarantee sales and send WhatsApp automatically"
py -3 ".\dealix-v2\dealix_os\cli.py" score "paid B2B agency partner with monthly retainer and CRM data"
py -3 ".\dealix-v2\dealix_os\cli.py" client-pack --client "Demo Client" --sector "B2B Services" --problem "messy leads" --service "lead-intelligence"
py -3 ".\dealix-v2\dealix_os\cli.py" value --client "Demo Client" --service "lead-intelligence" --metric "qualified accounts ranked" --result "top 50 accounts ranked" --evidence "manual test" --next-value "Pilot Conversion Sprint"
py -3 ".\dealix-v2\dealix_os\cli.py" proof-pack --client "Demo Client" --service "lead-intelligence" --metric "qualified accounts ranked" --result "top 50 accounts ranked" --evidence "manual test" --next-value "Pilot Conversion Sprint"
py -3 ".\dealix-v2\dealix_os\cli.py" proposal --client "Demo Client" --service "lead-intelligence" --problem "messy leads and weak pipeline"
py -3 ".\dealix-v2\dealix_os\cli.py" dashboard
py -3 ".\dealix-v2\dealix_os\cli.py" monthly-review

Write-Host "DONE" -ForegroundColor Green
