# Dealix production API smoke — founder daily check
$ErrorActionPreference = "Stop"
$base = if ($env:DEALIX_API_BASE) { $env:DEALIX_API_BASE } else { "https://api.dealix.me" }

Write-Host "== Dealix production smoke ==" -ForegroundColor Cyan
Write-Host "API: $base"

function Invoke-DealixGet($path) {
    $url = "$base$path"
    try {
        $r = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 15
        Write-Host "  OK $path" -ForegroundColor Green
        return $r
    } catch {
        Write-Host "  FAIL $path : $_" -ForegroundColor Red
        throw
    }
}

Invoke-DealixGet "/healthz" | Out-Null
try {
    Invoke-DealixGet "/version" | Out-Null
} catch {
    Write-Host "  WARN: /version failed — trying /health (older deploy)" -ForegroundColor Yellow
    $h = Invoke-DealixGet "/health"
    Write-Host "  version via /health: $($h.version) env=$($h.env) sha=$($h.git_sha)"
}

Write-Host "DEALIX_PRODUCTION_SMOKE=PASS" -ForegroundColor Green
