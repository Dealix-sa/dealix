param(
    [string]$Client,
    [string]$Offer,
    [string]$Amount
)

Write-Host "[Dealix Delivery] Starting Delivery Phase" -ForegroundColor Cyan
Write-Host "Client: $Client"
Write-Host "Offer: $Offer"
Write-Host "Contract Amount: $Amount"

# Log to execution ledger
py -3 ../dealix.py add-task --initiative "Delivery-$Client" --task "Kickoff $Offer" --due "today"

Write-Host "Delivery successfully initiated!" -ForegroundColor Green
