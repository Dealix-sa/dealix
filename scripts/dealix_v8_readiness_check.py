from pathlib import Path
required=[
'investor/INVESTOR_MEMO_AR.md','investor/FUNDRAISING_READINESS_CHECKLIST_AR.md','trust-center/TRUST_CENTER_OVERVIEW_AR.md','proof/PROOF_VAULT_SYSTEM_AR.md','data/proof/proof_items.json','data/traction/traction_events.jsonl','scripts/dealix_traction_ledger.py','scripts/dealix_investor_memo_builder.py','frontend/src/app/[locale]/trust-center/page.tsx']
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('Missing V8 files:')
    print('\n'.join(missing))
    raise SystemExit(1)
print('OK: Dealix V8 proof, trust, and investor readiness files are present')
