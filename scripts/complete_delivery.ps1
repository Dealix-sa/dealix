param(
    [string]$Client,
    [string]$Offer
)

Write-Host "[Dealix Delivery] Completing Delivery" -ForegroundColor Cyan
Write-Host "Client: $Client"
Write-Host "Offer: $Offer"

Write-Host "Generating Proof Pack..." -ForegroundColor Yellow
py -3 ../dealix.py proof-pack --client "$Client" --service "$Offer"

Write-Host "Delivery closed. Ready for Retainer pitch!" -ForegroundColor Green
