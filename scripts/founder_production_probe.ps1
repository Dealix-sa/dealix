# Founder production probe — Railway verify + curl healthz/version/meta
param(
    [string]$ApiBase = "https://api.dealix.me",
    [switch]$SkipLive
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$py = if (Get-Command py -ErrorAction SilentlyContinue) { "py -3" } else { "python3" }

Write-Host "== verify_railway_production_config =="
$railArgs = @("scripts/verify_railway_production_config.py", "--api-base", $ApiBase)
if ($SkipLive) { $railArgs += "--skip-live" }
Invoke-Expression "$py $($railArgs -join ' ')"
$railRc = $LASTEXITCODE

if (-not $SkipLive) {
    Write-Host "`n== curl.exe probes =="
    foreach ($path in @("/healthz", "/version", "/api/v1/meta")) {
        $url = "$ApiBase$path"
        Write-Host "  GET $url"
        try {
            $body = curl.exe -fsS $url 2>&1
            Write-Host "    $body"
        } catch {
            Write-Host "    FAIL: $_"
        }
    }
}

Write-Host "`nFOUNDER_PRODUCTION_PROBE_RC=$railRc"
exit $railRc
