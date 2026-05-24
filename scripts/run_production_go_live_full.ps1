# Production go-live - full layer orchestration (local + live probes)
param(
    [switch]$Strict,
    [switch]$SkipFrontendBuild,
    [switch]$SkipPush,
    [string]$ApiBase = "https://api.dealix.me",
    [string]$FrontendBase = "https://dealix.me"
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Fail = 0

function Write-Step([string]$Title) {
    Write-Host ""
    Write-Host "=== $Title ===" -ForegroundColor Cyan
}

function Import-RailwayEnvFile([string]$Path) {
    if (-not (Test-Path $Path)) { return }
    Get-Content $Path | ForEach-Object {
        if ($_ -match '^\s*([A-Z][A-Z0-9_]+)=(.*)$') {
            $k = $Matches[1]
            $v = $Matches[2].Trim().Trim('"').Trim("'")
            if ($k -and -not (Test-Path "env:$k")) { Set-Item -Path "env:$k" -Value $v }
        }
    }
}

Write-Step "0 Git push"
if ($SkipPush) {
    Write-Host "  skipped (-SkipPush)"
} else {
    $pushScript = Join-Path $PSScriptRoot "push_main_with_gh.ps1"
    if (Test-Path $pushScript) {
        powershell -File $pushScript
        if ($LASTEXITCODE -ne 0) { $Fail = 1 }
    } else {
        git push origin main 2>&1
        if ($LASTEXITCODE -ne 0) { $Fail = 1 }
    }
}

Write-Step "1 P0 env files"
$apiEnv = Join-Path $Root ".env.railway.generated"
if (-not (Test-Path $apiEnv)) {
    if (Test-Path (Join-Path $Root "scripts/generate_railway_p0_secrets.py")) {
        py -3 scripts/generate_railway_p0_secrets.py
    }
    Write-Host "  ensure .env.railway.generated exists and paste Railway vars"
}

Write-Step "2 Repo gates"
if (Test-Path $apiEnv) {
    Import-RailwayEnvFile $apiEnv
    Import-RailwayEnvFile (Join-Path $Root ".env.railway.frontend.generated")
}
py -3 scripts/verify_railway_production_config.py
if ($LASTEXITCODE -ne 0) { $Fail = 1 }
$envCheckArgs = @("scripts/railway_launch_env_check.py")
if (Test-Path $apiEnv) { $envCheckArgs += "--from-railway-env" }
py -3 @envCheckArgs
if ($Strict -and $LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Step "3 Unit tests"
py -3 -m pytest tests/test_production_layers.py tests/test_founder_production_layers.py tests/test_gtm_public_surfaces.py tests/test_official_launch_verify.py -q --no-cov
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Step "4 Frontend build"
if ($SkipFrontendBuild) {
    Write-Host "  skipped"
} elseif (Test-Path "$Root/frontend/package.json") {
    Push-Location "$Root/frontend"
    $env:NEXT_PUBLIC_API_URL = "https://api.dealix.me"
    $env:NEXT_PUBLIC_SITE_URL = "https://dealix.me"
    $env:NEXT_PUBLIC_USE_DEALIX_OPS_PROXY = "1"
    npm run build 2>&1
    if ($LASTEXITCODE -ne 0) { $Fail = 1 }
    Pop-Location
}

Write-Step "5 Layer map"
$layerArgs = @("scripts/production_layers_verify.py", "--write-cache")
if (Test-Path $apiEnv) { $layerArgs += "--from-railway-env" }
if ($Strict) { $layerArgs += "--strict" }
py -3 @layerArgs
if ($LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Step "6 Railway redeploy"
py -3 scripts/railway_redeploy_checklist.py

Write-Step "7 Webhooks"
$whArgs = @("scripts/webhook_setup_checklist.py")
if (Test-Path $apiEnv) { $whArgs += "--from-railway-env" }
py -3 @whArgs

Write-Step "8 Founder gates"
$env:DEALIX_API_BASE = $ApiBase
if (Test-Path (Join-Path $Root "scripts/run_founder_production_gates.py")) {
    py -3 scripts/run_founder_production_gates.py --api-base $ApiBase
}

Write-Step "9 Paid launch"
Import-RailwayEnvFile $apiEnv
Import-RailwayEnvFile (Join-Path $Root ".env.railway.frontend.generated")
if (-not $env:DEALIX_ADMIN_API_KEY -and $env:ADMIN_API_KEYS) {
    $env:DEALIX_ADMIN_API_KEY = ($env:ADMIN_API_KEYS -split ',')[0].Trim()
}
$paidArgs = @("scripts/verify_paid_launch_readiness.py")
if ($Strict) { $paidArgs += "--strict" }
py -3 @paidArgs
if ($Strict -and $LASTEXITCODE -ne 0) { $Fail = 1 }

Write-Step "10 Post-redeploy verify"
$postArgs = @("scripts/post_redeploy_verify_dealix.py", "--api-base", $ApiBase, "--frontend-base", $FrontendBase)
if ($env:DEALIX_ADMIN_API_KEY) { $postArgs += "--admin-key", $env:DEALIX_ADMIN_API_KEY }
py -3 @postArgs
if ($LASTEXITCODE -ne 0) {
    if ($Strict) { $Fail = 1 }
    else { Write-Host "  (expected until Railway deploy + DNS)" -ForegroundColor Yellow }
}

Write-Step "11 Validate railway env files"
if ((Test-Path $apiEnv) -and (Test-Path (Join-Path $Root ".env.railway.frontend.generated"))) {
    py -3 scripts/validate_railway_generated_env.py --from-railway-env
    if ($Strict -and $LASTEXITCODE -ne 0) { $Fail = 1 }
}

Write-Step "12 Live HTTP"
$urls = @(
    "$ApiBase/healthz",
    "$ApiBase/version",
    "$ApiBase/api/v1/meta",
    "$FrontendBase/ar"
)
foreach ($u in $urls) {
    try {
        $r = Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 25
        Write-Host "  $u -> $($r.StatusCode)"
    } catch {
        $code = $_.Exception.Response.StatusCode.value__
        if ($code) { Write-Host "  $u -> $code" }
        else { Write-Host "  $u -> ERR" }
    }
}

Write-Host ""
if ($Fail -eq 0) {
    Write-Host "PRODUCTION_GO_LIVE_FULL=OK" -ForegroundColor Green
} else {
    Write-Host "PRODUCTION_GO_LIVE_FULL=PARTIAL" -ForegroundColor Yellow
    Write-Host "  docs/ops/PRODUCTION_LAYERS_GO_LIVE_AR.md"
    Write-Host "  docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md"
}
exit $Fail
