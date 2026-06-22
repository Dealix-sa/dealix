#!/usr/bin/env bash
# ============================================================
# Dealix — Local Environment Setup
# Run once after cloning to get from zero to production-check GO
# ============================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[OK]${NC}  $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail()  { echo -e "${RED}[FAIL]${NC} $1"; exit 1; }

echo "======================================================================"
echo "  DEALIX — Local Setup"
echo "======================================================================"
echo ""

# ---- Step 1: Check prerequisites ----
echo "--- Step 1/5: Checking prerequisites ---"

command -v node >/dev/null 2>&1 || fail "Node.js is required. Install Node 20+ from https://nodejs.org"
NODE_VER=$(node -v | sed 's/v//' | cut -d. -f1)
[ "$NODE_VER" -ge 20 ] || warn "Node 20+ recommended (found v$NODE_VER)"
info "Node.js $(node -v)"

command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1 || warn "Python 3.11+ recommended for operational scripts"
if command -v python3 >/dev/null 2>&1; then
  info "Python $(python3 --version 2>&1 | awk '{print $2}')"
elif command -v python >/dev/null 2>&1; then
  info "Python $(python --version 2>&1 | awk '{print $2}')"
fi

echo ""

# ---- Step 2: Install dependencies ----
echo "--- Step 2/5: Installing dependencies ---"
npm install
info "Dependencies installed"
echo ""

# ---- Step 3: Environment file ----
echo "--- Step 3/5: Checking environment ---"
if [ -f .env ] || [ -f .env.local ]; then
  info "Environment file found"
else
  warn "No .env or .env.local found"
  echo "  Create one based on docs/ops/ENVIRONMENT_VARIABLES.md"
  echo "  Minimum required:"
  echo "    DATABASE_URL=mysql://dealix:dealix_pass_2026@localhost:3306/dealix"
  echo ""
  echo "  For Docker Compose (no local MySQL needed):"
  echo "    docker compose up -d mysql"
  echo "    Then set DATABASE_URL=mysql://dealix:dealix_pass_2026@localhost:3306/dealix"
fi
echo ""

# ---- Step 4: TypeCheck + Build ----
echo "--- Step 4/5: TypeCheck + Build ---"
npm run check || fail "TypeScript check failed"
info "TypeCheck passed"

npm run build || fail "Build failed"
info "Build succeeded"
echo ""

# ---- Step 5: Production Check ----
echo "--- Step 5/5: Production Check ---"
npm run production-check || warn "Production check has warnings — review output above"
echo ""

echo "======================================================================"
echo "  SETUP COMPLETE"
echo ""
echo "  Next steps:"
echo "    1. Create .env with DATABASE_URL (see docs/ops/ENVIRONMENT_VARIABLES.md)"
echo "    2. Start MySQL:  docker compose up -d mysql"
echo "    3. Push schema:  npm run db:push"
echo "    4. Dev server:   npm run dev"
echo "    5. Daily ops:    npm run company-day"
echo "======================================================================"
