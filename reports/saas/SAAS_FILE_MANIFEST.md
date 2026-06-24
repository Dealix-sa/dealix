# SaaS Foundation Manifest

## Branch

`feat/turnkey-saas-foundation`

## Backend

- `api/tenant_context.py`
- `app/saas/access_policy.py`
- `app/saas/tenant_guard.py`
- `app/saas/audit.py`
- `app/billing/plans.py`
- `app/billing/moyasar_stub.py`

## Scripts

- `scripts/saas/verify_saas_env.py`
- `scripts/saas/check_saas_foundation.py`
- `scripts/saas/run_commercial_launch_day.py`

## Tests

- `tests/saas/test_saas_foundation_contract.py`
- `tests/saas/test_saas_env_defaults.py`
- `tests/saas/test_billing_stub_only.py`
- `tests/saas/test_commercial_launch_safety.py`

## Frontend

- `apps/web/lib/saas-api.ts`
- `apps/web/components/saas/*`
- `apps/web/app/(saas)/*`

## Safety

Outbound and live billing remain disabled by default.
