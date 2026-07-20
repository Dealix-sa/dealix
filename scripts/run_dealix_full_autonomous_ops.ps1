# Maximum governed autonomous ops (expand + founder day + gates + report)
# Usage: powershell -File scripts/run_dealix_full_autonomous_ops.ps1
#        powershell -File scripts/run_dealix_full_autonomous_ops.ps1 -StatusOnly
param(
    [switch]$SkipExpand,
    [switch]$SkipFounderDay,
    [switch]$SkipGates,
    [switch]$StatusOnly,
    [switch]$Quick,
    [switch]$Evening,
    [switch]$Weekly,
    [switch]$DryRun,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:APP_ENV = "test"

$argsList = @("scripts/run_dealix_full_autonomous_ops.py")
if ($StatusOnly) {
    $argsList += "--status-only"
} elseif ($Quick -or $SkipFounderDay) {
    $argsList += "--quick"
} else {
    if ($Evening) { $argsList += "--evening" }
    if ($Weekly) { $argsList += "--weekly" }
    if ($DryRun) { $argsList += "--dry-run" }
    if ($Json) { $argsList += "--json" }
}

if ($SkipExpand) {
    Write-Warning "-SkipExpand is deprecated; the canonical runner owns expansion policy."
}
if ($SkipGates) {
    Write-Warning "-SkipGates is deprecated; safety gates cannot be bypassed by this wrapper."
}

if ($env:PY) { & $env:PY @argsList } else { & py -3 @argsList }
exit $LASTEXITCODE
