from pathlib import Path
checks={
 'tenant schema': Path('db/migrations/0002_create_multi_tenant_saas.sql').exists(),
 'usage meter': Path('scripts/dealix_usage_meter.py').exists(),
 'audit log': Path('scripts/dealix_audit_log.py').exists(),
 'billing plans': Path('data/billing/plans.json').exists(),
 'admin console': Path('frontend/src/app/[locale]/app/admin/page.tsx').exists(),
 'security checklist': Path('security/MULTI_TENANT_SECURITY_CHECKLIST_AR.md').exists(),
}
score=sum(checks.values())
for k,v in checks.items(): print(f'{k}: {"OK" if v else "MISSING"}')
print(f'SaaS maturity score: {score}/{len(checks)}')
