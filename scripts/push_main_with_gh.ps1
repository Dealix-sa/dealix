# Push main using GitHub CLI token (fixes 403 when credential manager PAT lacks repo scope)
$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$ahead = git rev-list --count origin/main..HEAD 2>$null
if (-not $ahead -or [int]$ahead -eq 0) {
    Write-Host "PUSH_MAIN=SKIP (nothing ahead of origin/main)"
    exit 0
}

Write-Host "Commits ahead: $ahead"
$token = (gh auth token 2>$null)
if (-not $token) {
    Write-Host "Run: gh auth login -h github.com -p https -s repo"
    exit 1
}
$token = $token.Trim()
$env:GIT_TERMINAL_PROMPT = "0"
gh auth setup-git 2>$null | Out-Null

$remoteUrl = "https://x-access-token:${token}@github.com/VoXc2/dealix.git"
git -c credential.helper= push $remoteUrl HEAD:main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "PUSH_MAIN=OK"
    exit 0
}

git push origin main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "PUSH_MAIN=OK (gh credential helper)"
    exit 0
}

Write-Host "PUSH_MAIN=FAIL - refresh token:"
Write-Host "  gh auth refresh -h github.com -s repo"
exit 1
