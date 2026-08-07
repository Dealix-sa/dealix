from pathlib import Path

REQUIRED = [
    'docs/launch/DEALIX_FULL_LAUNCH_MASTER_PLAN_AR.md',
    'frontend/src/app/api/health/route.ts',
    'frontend/src/app/[locale]/diagnostic/page.tsx',
    'data/crm/leads.jsonl',
    'data/revenue/first_5_clients.json',
    'data/agents/agent_registry.json',
    'data/proof/proof_items.json',
    'db/migrations/0001_create_revenue_machine.sql',
    'db/migrations/0002_create_multi_tenant_saas.sql',
    'db/migrations/0003_production_bridge.sql',
    'implementation/PRODUCTION_IMPLEMENTATION_BRIDGE_AR.md',
    'revenue-sprint/FIRST_5_CLIENTS_SPRINT_AR.md',
    'scale/SCALE_MASTER_PLAN_AR.md',
    'consolidation/MASTER_MERGE_PLAN_AR.md',
    'Makefile',
]

def main():
    missing = [p for p in REQUIRED if not Path(p).exists()]
    if missing:
        print('NO-GO: missing required Dealix master files')
        for p in missing:
            print(f'- {p}')
        raise SystemExit(1)
    print('OK: Dealix V13 master consolidation files are present')
    print(f'Checked: {len(REQUIRED)} critical files')
    print('Decision: ready for controlled preview merge review')

if __name__ == '__main__':
    main()
