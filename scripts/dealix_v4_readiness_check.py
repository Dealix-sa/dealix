from pathlib import Path

required = [
 'deployment/PRODUCTION_DEPLOYMENT_RUNBOOK_AR.md','deployment/ENVIRONMENT_CONTRACT.md','db/schema.sql',
 'api/openapi/dealix-leads.openapi.json','partners/PARTNER_PROGRAM_AR.md','finance/UNIT_ECONOMICS_MODEL_AR.md',
 'data-room/FOUNDER_MEMO_AR.md','qa/LAUNCH_QA_CHECKLIST_AR.md','observability/OBSERVABILITY_PLAN_AR.md',
 '.github/workflows/dealix-v4-production-readiness.yml'
]
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('Missing V4 files:')
    for m in missing: print('-',m)
    raise SystemExit(1)
print('OK: Dealix V4 production growth files are present')
