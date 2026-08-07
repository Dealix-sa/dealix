from pathlib import Path

CHECKS = {
    'master_readiness_script': 'scripts/dealix_v13_master_readiness.py',
    'env_example': '.env.example',
    'health_route': 'frontend/src/app/api/health/route.ts',
    'migration_0003': 'db/migrations/0003_production_bridge.sql',
    'first_revenue_sprint': 'revenue-sprint/FIRST_5_CLIENTS_SPRINT_AR.md',
    'outbound_policy': 'compliance/OUTBOUND_AND_DATA_POLICY_AR.md',
    'proof_vault': 'proof/PROOF_VAULT_SYSTEM_AR.md',
    'scale_plan': 'scale/SCALE_MASTER_PLAN_AR.md',
    'makefile': 'Makefile',
}

def main():
    passed=[]; failed=[]
    for name, path in CHECKS.items():
        (passed if Path(path).exists() else failed).append(name)
    print('# Dealix Launch Decision Report')
    for n in passed: print(f'- {n}: GO')
    for n in failed: print(f'- {n}: NO-GO')
    score=len(passed)
    print(f'Score: {score}/{len(CHECKS)}')
    if failed:
        print('Decision: NO-GO until missing controls are added')
        raise SystemExit(1)
    print('Decision: CONTROLLED PREVIEW GO')
    print('Scope: first 5 managed clients, no self-serve SaaS launch yet')

if __name__ == '__main__':
    main()
