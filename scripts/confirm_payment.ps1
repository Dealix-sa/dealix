param(
    [Parameter(Mandatory=$true)][string]$Client
)

$ErrorActionPreference = 'Stop'

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " CONFIRMING PAYMENT - DEALIX REVENUE OS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Client: $Client"

# Update lead status using Python script
py -3 scripts/mark_lead.py "$Client" "paid" "Payment confirmed. Invoice cleared."
py -3 scripts/mark_lead.py "$Client" "delivery_started" "Delivery sprint officially started."

Write-Host "Payment confirmed. Delivery active." -ForegroundColor Green

Write-Host "`nNext Action: Begin delivery work. Once complete, run:"
Write-Host "powershell -File scripts/complete_delivery.ps1 -Client ""$Client"" -Offer ""ai-trust""" -ForegroundColor Yellow
