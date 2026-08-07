from pathlib import Path

required = [
 'revenue-sprint/FIRST_5_CLIENTS_SPRINT_AR.md',
 'client-onboarding/CLIENT_INTAKE_FORM_AR.md',
 'sales-room/DISCOVERY_CALL_SCORECARD_AR.md',
 'billing-ops/INVOICE_AND_COLLECTION_PLAYBOOK_AR.md',
 'proof-reports/WEEKLY_CLIENT_PROOF_REPORT_AR.md',
 'scripts/dealix_first_revenue_sprint.py',
 'scripts/dealix_revenue_dashboard.py',
 'frontend/src/app/[locale]/first-revenue-sprint/page.tsx',
 '.github/workflows/dealix-v11-first-revenue.yml'
]
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('Missing V11 files:')
    print('\n'.join(missing))
    raise SystemExit(1)
print('OK: Dealix V11 first revenue sprint files are present')
