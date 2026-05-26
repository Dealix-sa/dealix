param(
    [Parameter(Mandatory=$true)][string]$Client,
    [Parameter(Mandatory=$true)][string]$Offer,
    [Parameter(Mandatory=$true)][string]$Amount
)

$ErrorActionPreference = 'Stop'

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " STARTING PAID DELIVERY PROCESS - DEALIX" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Client: $Client"
Write-Host "Offer: $Offer"
Write-Host "Amount: $Amount SAR"

# Create a payment request file for the client
$date = Get-Date -Format "yyyyMMdd"
$filename = "payment_request_$($Client.Replace(' ','_').ToLower())_$date.md"
$filepath = Join-Path "reports" $filename

$content = @"
# 💳 Payment Request — $Client

**Client:** $Client
**Offer:** $Offer
**Amount:** $Amount SAR
**Date:** $(Get-Date -Format 'yyyy-MM-dd')

Please complete the payment of **$Amount SAR** to initiate the onboarding and delivery process for your **$Offer**.
Once payment is confirmed, we will launch the execution sprint.
"@

Set-Content -Path $filepath -Value $content -Encoding UTF8
Write-Host "Payment request generated at $filepath" -ForegroundColor Green

# Update lead status using Python script
py -3 scripts/mark_lead.py "$Client" "invoice_sent" "Invoice sent for $Amount SAR ($Offer)"

# Add delivery task to EXECUTION_LEDGER.md using dealix CLI
py -3 dealix.py add-task --initiative $Offer --task "Deliver $Offer sprint to $Client" --due "+7 days"

Write-Host "`nNext Action: Wait for payment confirmation. Once received, run:"
Write-Host "powershell -File scripts/confirm_payment.ps1 -Client ""$Client""" -ForegroundColor Yellow
