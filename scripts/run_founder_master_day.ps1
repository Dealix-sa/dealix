param([switch]$VerifyProd)
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
if ($VerifyProd) { $env:DEALIX_VERIFY_PROD = "1" }
& "$PSScriptRoot\run_founder_commercial_day.ps1" @PSBoundParameters
& "$PSScriptRoot\founder_executive_stack_verify.sh"
Write-Host "FOUNDER_MASTER_DAY=PASS"
