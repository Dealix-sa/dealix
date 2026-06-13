from pathlib import Path
required = [
 'enterprise/ENTERPRISE_SALES_PLAYBOOK_AR.md',
 'enterprise/BUSINESS_CASE_TEMPLATE_AR.md',
 'demos/DEMO_ROOM_BLUEPRINT_AR.md',
 'integrations/INTEGRATIONS_ROADMAP_AR.md',
 'customer-success/CUSTOMER_SUCCESS_SYSTEM_AR.md',
 'legal/MSA_LIGHT_TEMPLATE_AR.md',
 'enablement/FOUNDER_SALES_TRAINING_AR.md',
 'hiring/FIRST_5_ROLES_AR.md',
 'finance/ENTERPRISE_PRICING_LADDER_AR.md',
 'ops/CEO_CONTROL_TOWER_AR.md',
 'frontend/src/app/[locale]/enterprise/page.tsx',
]
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('MISSING V6 FILES:')
    print('\n'.join(missing))
    raise SystemExit(1)
print('OK: Dealix V6 enterprise revenue factory files are present')
