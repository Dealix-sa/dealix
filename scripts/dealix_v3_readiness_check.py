#!/usr/bin/env python3
from pathlib import Path
required=[
 'frontend/src/app/api/leads/route.ts',
 'frontend/src/app/[locale]/diagnostic/page.tsx',
 'frontend/src/components/LeadCaptureForm.tsx',
 'data/crm/pipeline_schema.md',
 'scripts/dealix_crm_append_lead.py',
 'scripts/dealix_offer_builder.py',
 'scripts/dealix_kpi_dashboard.py',
 'delivery/PILOT_DELIVERY_PLAYBOOK_AR.md',
 'security/AI_USAGE_GUARDRAILS_AR.md',
 '.github/workflows/dealix-security-smoke.yml'
]
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('MISSING:')
    for m in missing: print('-',m)
    raise SystemExit(1)
print('OK: Dealix V3 revenue machine files are present')
