# ============================================================
# Dealix - Local Environment Setup (Windows PowerShell)
# Run once after cloning to get from zero to production-check GO
# ============================================================
$ErrorActionPreference = "Stop"

function Write-OK($msg)   { Write-Host "[OK]  " -ForegroundColor Green -NoNewline; Write-Host " $msg" }
function Write-Warn($msg) { Write-Host "[WARN]" -ForegroundColor Yellow -NoNewline; Write-Host " $msg" }
function Write-Fail($msg) { Write-Host "[FAIL]" -ForegroundColor Red -NoNewline; Write-Host " $msg"; exit 1 }

Write-Host "======================================================================"
Write-Host "  DEALIX - Local Setup"
Write-Host "======================================================================"
Write-Host ""

# ---- Step 1: Check prerequisites ----
Write-Host "--- Step 1/5: Checking prerequisites ---"

$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) { Write-Fail "Node.js is required. Install Node 20+ from https://nodejs.org" }
$nodeVer = (node -v) -replace 'v','' -split '\.' | Select-Object -First 1
if ([int]$nodeVer -lt 20) { Write-Warn "Node 20+ recommended (found v$nodeVer)" }
Write-OK "Node.js $(node -v)"

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Warn "Python 3.11+ recommended for operational scripts"
} else {
    Write-OK "Python $(python --version 2>&1)"
}

Write-Host ""

# ---- Step 2: Install dependencies ----
Write-Host "--- Step 2/5: Installing dependencies ---"
npm install
if ($LASTEXITCODE -ne 0) { Write-Fail "npm install failed" }
Write-OK "Dependencies installed"
Write-Host ""

# ---- Step 3: Environment file ----
Write-Host "--- Step 3/5: Checking environment ---"
if ((Test-Path .env) -or (Test-Path .env.local)) {
    Write-OK "Environment file found"
} else {
    Write-Warn "No .env or .env.local found"
    Write-Host "  Create one based on docs/ops/ENVIRONMENT_VARIABLES.md"
    Write-Host "  Minimum required:"
    Write-Host "    DATABASE_URL=mysql://dealix:dealix_pass_2026@localhost:3306/dealix"
    Write-Host ""
    Write-Host "  For Docker Compose (no local MySQL needed):"
    Write-Host "    docker compose up -d mysql"
    Write-Host "    Then set DATABASE_URL=mysql://dealix:dealix_pass_2026@localhost:3306/dealix"
}
Write-Host ""

# ---- Step 4: TypeCheck + Build ----
Write-Host "--- Step 4/5: TypeCheck + Build ---"
npm run check
if ($LASTEXITCODE -ne 0) { Write-Fail "TypeScript check failed" }
Write-OK "TypeCheck passed"

npm run build
if ($LASTEXITCODE -ne 0) { Write-Fail "Build failed" }
Write-OK "Build succeeded"
Write-Host ""

# ---- Step 5: Production Check ----
Write-Host "--- Step 5/5: Production Check ---"
npm run production-check
if ($LASTEXITCODE -ne 0) { Write-Warn "Production check has warnings - review output above" }
Write-Host ""

Write-Host "======================================================================"
Write-Host "  SETUP COMPLETE"
Write-Host ""
Write-Host "  Next steps:"
Write-Host "    1. Create .env with DATABASE_URL (see docs/ops/ENVIRONMENT_VARIABLES.md)"
Write-Host "    2. Start MySQL:  docker compose up -d mysql"
Write-Host "    3. Push schema:  npm run db:push"
Write-Host "    4. Dev server:   npm run dev"
Write-Host "    5. Daily ops:    npm run company-day"
Write-Host "======================================================================"
