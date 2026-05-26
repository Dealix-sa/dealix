param(
    [Parameter(Mandatory=$true)][string]$Client,
    [Parameter(Mandatory=$true)][string]$Offer
)

$ErrorActionPreference = 'Stop'

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " COMPLETING SPRINT DELIVERY - DEALIX OS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Client: $Client"
Write-Host "Offer: $Offer"

# 1. Update lead status to proof_pack_created
py -3 scripts/mark_lead.py "$Client" "proof_pack_created" "Delivery complete. Generating Proof Pack."

# 2. Generate Proof Pack (which also calls dealix CLI internally to log to PROOF_LEDGER.md)
Write-Host "`n[1/2] Triggering Proof Pack & Retainer generation..." -ForegroundColor Yellow
py -3 scripts/generate_proof_pack.py "$Client"

# 3. Transition lead to complete
Write-Host "`n[2/2] Finalizing pipeline state..." -ForegroundColor Yellow
py -3 scripts/mark_lead.py "$Client" "complete" "Sami signed off. Retainer offered."

Write-Host "`nDelivery successfully marked complete. Lead state is set to 'complete'." -ForegroundColor Green
Write-Host "Check reports/board/ for the generated Proof Pack."
