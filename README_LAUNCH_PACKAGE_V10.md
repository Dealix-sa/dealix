# Dealix Launch Package V10 — Production Implementation Bridge

V10 turns Dealix from launch/growth/SaaS planning into an implementation bridge that can be wired to real auth, database, migrations, CI, deployment smoke tests, seed data, and E2E checks.

Core rule: do not jump to full automation before proving tenant isolation, auth enforcement, migration safety, audit logs, and smoke tests.

## Run

```bash
python scripts/dealix_v10_readiness_check.py
python scripts/dealix_env_contract_check.py --env-file .env.example
python scripts/dealix_migration_plan.py
python scripts/dealix_seed_tenant_data.py --tenant "شركة تدريب الرياض"
python scripts/dealix_e2e_smoke_manifest.py
python scripts/dealix_production_go_no_go.py
```
