# Dealix Commercial Controls Runbook

## Purpose

This runbook adds the delivery and claims-review controls around the commercial launch workflow.

It complements:

- Startup OS Day
- Startup OS Release Gate
- Commercial Launch Control

## Commands

```bash
python scripts/commercial/generate_client_delivery_control.py
python scripts/commercial/generate_trust_control.py
python -m pytest -q tests/saas/test_client_delivery_control_assets.py tests/saas/test_trust_control_assets.py
```

## Generated outputs

- `reports/client_delivery_control/latest.md`
- `reports/client_delivery_control/latest.json`
- `reports/trust_control/latest.md`
- `reports/trust_control/latest.json`
- `apps/web/lib/client-delivery-control-snapshot.ts`
- `apps/web/lib/trust-control-snapshot.ts`

## Frontend pages

- `/app/client-delivery`
- `/app/trust-control`

## Client delivery control

Client delivery control turns a sold sprint into:

- intake
- diagnosis
- blueprint
- sprint delivery
- proof pack
- renewal path

## Claims review control

Claims review control protects Dealix from unsupported sales language by requiring:

- no fake ROI
- no fake testimonials
- no guaranteed revenue claim
- proof-pack language
- owner review for sensitive actions

## Full commercial validation sequence

```bash
python scripts/commercial/run_startup_os_day.py
python scripts/commercial/verify_startup_os_release_gate.py
python scripts/commercial/generate_commercial_launch_control.py
python scripts/commercial/generate_client_delivery_control.py
python scripts/commercial/generate_trust_control.py

python -m pytest -q \
  tests/saas/test_startup_command_center_assets.py \
  tests/saas/test_startup_os_day_assets.py \
  tests/saas/test_startup_os_release_gate.py \
  tests/saas/test_commercial_launch_control_assets.py \
  tests/saas/test_client_delivery_control_assets.py \
  tests/saas/test_trust_control_assets.py

npm --prefix apps/web run verify || true
```

## Done criteria

- Commercial launch report generated.
- Client delivery report generated.
- Claims review report generated.
- Frontend snapshots generated.
- Frontend pages exist.
- Tests pass.
- Web verify is reviewed.
