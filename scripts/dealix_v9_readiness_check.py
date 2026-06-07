from pathlib import Path
required = [
 'product/SAAS_PRODUCTIZATION_MASTER_PLAN_AR.md',
 'product/TENANT_WORKSPACE_MODEL_AR.md',
 'db/migrations/0002_create_multi_tenant_saas.sql',
 'frontend/src/app/api/tenants/route.ts',
 'frontend/src/app/api/usage/route.ts',
 'frontend/src/app/[locale]/app/workspace/page.tsx',
 'billing/BILLING_AND_USAGE_MODEL_AR.md',
 'data/billing/plans.json',
 'security/MULTI_TENANT_SECURITY_CHECKLIST_AR.md',
 '.github/workflows/dealix-v9-saas-readiness.yml'
]
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('MISSING:')
    [print('-',m) for m in missing]
    raise SystemExit(1)
print('OK: Dealix V9 SaaS productization files are present')
