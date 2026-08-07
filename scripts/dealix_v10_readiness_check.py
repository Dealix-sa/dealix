from pathlib import Path

REQUIRED = [
    'implementation/PRODUCTION_IMPLEMENTATION_BRIDGE_AR.md',
    'implementation/AUTH_AND_SESSION_ARCHITECTURE_AR.md',
    'implementation/DATABASE_AND_MIGRATION_RUNBOOK_AR.md',
    'implementation/CI_CD_PRODUCTION_PIPELINE_AR.md',
    'implementation/E2E_AND_SMOKE_TEST_PLAN_AR.md',
    'implementation/PRODUCTION_GO_NO_GO_AR.md',
    '.env.example',
    'db/migrations/0003_production_bridge.sql',
    'db/seed/seed_demo_tenant.json',
    'frontend/src/app/api/health/route.ts',
    'frontend/src/lib/authGuard.ts',
    'playwright.config.ts',
    'tests/e2e/production-smoke.spec.ts',
    '.github/workflows/dealix-v10-production-bridge.yml',
]

missing = [p for p in REQUIRED if not Path(p).exists()]
if missing:
    print('Missing V10 files:')
    for p in missing: print('-', p)
    raise SystemExit(1)
print('OK: Dealix V10 production implementation bridge files are present')
