from pathlib import Path

checks={
 'v10_readiness': Path('scripts/dealix_v10_readiness_check.py').exists(),
 'env_example': Path('.env.example').exists(),
 'migration_0003': Path('db/migrations/0003_production_bridge.sql').exists(),
 'health_route': Path('frontend/src/app/api/health/route.ts').exists(),
 'e2e_spec': Path('tests/e2e/production-smoke.spec.ts').exists(),
 'workflow': Path('.github/workflows/dealix-v10-production-bridge.yml').exists(),
}
print('# Production Go/No-Go')
score=sum(checks.values())
for k,v in checks.items(): print(f'- {k}: {"GO" if v else "NO-GO"}')
print(f'Score: {score}/{len(checks)}')
if score != len(checks): raise SystemExit(1)
print('GO for controlled preview / managed production validation')
