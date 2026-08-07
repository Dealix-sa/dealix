# Service OS Frontend Launch Runbook

## Purpose

This launch pack gives Dealix a real frontend surface for the commercial Service OS.

It connects the current Service OS runner to a frontend page that can be shown to prospects, clients, and the founder during launch review.

## Frontend route

```text
/service-os
```

## What the page shows

- RCMax readiness
- Auto14 readiness
- Client Ops readiness
- Conversation Intelligence readiness
- Deal Strategy readiness
- Service OS readiness
- commercial offers
- client deliverables
- approval gates
- operating flow
- live sends = 0
- final commitments = 0

## Run locally

```bash
python run_os16.py
python generate_service_os_snapshot.py
python -m pytest -q test_service_os_frontend.py test_client_ops_max.py
npm --prefix apps/web run verify
npm --prefix apps/web run dev
```

Then open:

```text
/service-os
```

## Safety posture

The frontend is commercial-ready, but it does not enable outbound actions.

Sensitive actions remain approval-gated:

- external sharing
- final quote
- contracts
- terms
- result claims
- live outbound

## Launch checklist

1. Pull latest main.
2. Run Service OS runner.
3. Generate frontend snapshot.
4. Run Python tests.
5. Run web verify.
6. Open `/service-os`.
7. Use the page in sales review and client discovery.
8. Do not enable live outbound unless a separate controlled-live PR passes.
