from pathlib import Path

required=['integrations/CRM_INTEGRATION_CONTRACT.md','integrations/INTEGRATIONS_ROADMAP_AR.md','integrations/CALENDLY_AND_BOOKING_FLOW_AR.md']
missing=[x for x in required if not Path(x).exists()]
if missing:
 print('Missing integration docs:', missing); raise SystemExit(1)
print('OK: integration manifest present')
