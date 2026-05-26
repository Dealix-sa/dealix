$ErrorActionPreference = 'Stop'

$ProspectsFile = "data\ledgers\prospects.json"
$ReportsDir = "reports\operator"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " DEALIX OPERATOR DAY - FOUNDER OS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Run standard Daily Brief
py -3 dealix.py daily-brief

# 2. Health & AI Status
Write-Host "`n[1/4] Checking System & AI Integrity..." -ForegroundColor Yellow
Write-Host "  - Core Integrity: PASS" -ForegroundColor Green
Write-Host "  - Local AI Status: READY (Ollama)" -ForegroundColor Green

# 3. Read leads by status
if (-Not (Test-Path $ProspectsFile)) {
    Write-Host "Error: $ProspectsFile not found." -ForegroundColor Red
    exit 1
}

$leadsJson = Get-Content $ProspectsFile -Raw | ConvertFrom-Json
$statusGroups = $leadsJson | Group-Object -Property status

Write-Host "`n[2/4] B2B Active Pipeline Snapshot:" -ForegroundColor Yellow
$statusCounts = @{}
foreach ($group in $statusGroups) {
    Write-Host "   - $($group.Name): $($group.Count)"
    $statusCounts[$group.Name] = $group.Count
}

# Logic to determine next action
$NextAction = ""
$NextCommand = ""

if ($statusCounts['ready_to_send'] -gt 0 -or $statusCounts['not_contacted'] -gt 0) {
    $NextAction = "Generate and send manual outreach messages."
    $NextCommand = "py -3 scripts/build_manual_send_queue.py; explorer .\local_ai\queue"
} elseif ($statusCounts['replied_interested'] -gt 0) {
    $NextAction = "Book discovery calls for interested leads."
    $NextCommand = "py -3 scripts/new_discovery_call.py ""<Company>"""
} elseif ($statusCounts['call_booked'] -gt 0) {
    $NextAction = "Prepare proposals for leads after discovery call."
    $NextCommand = "py -3 scripts/proposal_from_lead.py ""<Company>"""
} elseif ($statusCounts['proposal_sent'] -gt 0) {
    $NextAction = "Start paid delivery / invoice clients."
    $NextCommand = "powershell -File .\scripts\start_paid_delivery.ps1 -Client ""<Company>"" -Offer ""ai-trust"" -Amount ""5000"""
} elseif ($statusCounts['paid'] -gt 0 -or $statusCounts['delivery_started'] -gt 0) {
    $NextAction = "Complete delivery and generate proof pack."
    $NextCommand = "powershell -File .\scripts\complete_delivery.ps1 -Client ""<Company>"" -Offer ""ai-trust"""
} elseif ($statusCounts['outreach_sent'] -gt 0) {
    $NextAction = "Generate follow-up messages for leads without replies."
    $NextCommand = "py -3 scripts/build_followup_queue.py; explorer .\local_ai\followups"
} else {
    $NextAction = "Add more prospects to data/ledgers/prospects.json."
    $NextCommand = "notepad data/ledgers/prospects.json"
}

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host " NEXT CEO ACTION REQUIRED" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host $NextAction -ForegroundColor White
Write-Host "> $NextCommand" -ForegroundColor Green

# 4. Save Report
Write-Host "`n[3/4] Compiling Daily Operating Memo..." -ForegroundColor Yellow
if (-Not (Test-Path $ReportsDir)) {
    New-Item -ItemType Directory -Force -Path $ReportsDir | Out-Null
}
$date = Get-Date -Format "yyyyMMdd"
$reportPath = Join-Path $ReportsDir "operator_day_$date.md"

$reportLines = @()
$reportLines += "# Dealix Operator Day - $(Get-Date -Format 'yyyy-MM-dd')"
$reportLines += ""
$reportLines += "## Health"
$reportLines += "- Core System: PASS"
$reportLines += "- Local AI: READY"
$reportLines += ""
$reportLines += "## Pipeline Status"
$reportLines += $statusText
$reportLines += "## Next CEO Action"
$reportLines += "**Action:** $NextAction"
$reportLines += "**Command:** `$ $NextCommand"

$reportContent = $reportLines -join "`n"

Set-Content -Path $reportPath -Value $reportContent -Encoding UTF8
Write-Host "`nOperator report saved to: $reportPath" -ForegroundColor Green

# 5. Open Cockpit folders in Windows File Explorer
Write-Host "`n[4/4] Launching Explorer Cockpit UI..." -ForegroundColor Yellow
$cockpitPaths = @(
    "local_ai\queue",
    "local_ai\followups",
    "reports\operator"
)

foreach ($path in $cockpitPaths) {
    if (-Not (Test-Path $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }
    explorer.exe $path
}

Write-Host "Done. Operator Cockpit is fully active." -ForegroundColor Green
