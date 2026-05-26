param(
    [string]$Client
)

Write-Host "[Dealix Finance] Confirming Payment Received" -ForegroundColor Green
Write-Host "Client: $Client"

py -3 ../scripts/mark_lead.py "$Client" "Payment_Received" "Start Delivery"
Write-Host "Revenue Ledger updated successfully!" -ForegroundColor Green
