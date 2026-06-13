from pathlib import Path
items=[
    ('playwright.config.ts', Path('playwright.config.ts').exists()),
    ('tests/e2e/production-smoke.spec.ts', Path('tests/e2e/production-smoke.spec.ts').exists()),
    ('frontend/src/app/api/health/route.ts', Path('frontend/src/app/api/health/route.ts').exists()),
]
print('# E2E Smoke Manifest')
failed=False
for name, ok in items:
    print(f'- {name}: {"OK" if ok else "MISSING"}')
    failed = failed or not ok
if failed: raise SystemExit(1)
print('Command: npx playwright test')
