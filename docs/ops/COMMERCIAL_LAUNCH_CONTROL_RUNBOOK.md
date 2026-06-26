# Dealix Commercial Launch Control Runbook

## Purpose

Commercial Launch Control is the top-level founder-led launch view for Dealix.

It connects:

- Startup OS Day
- Startup OS Release Gate
- Product catalog
- Sprint packages
- Founder daily brief
- Proof pack
- Frontend command pages
- Merge order
- Launch guardrails

## Command

```bash
make -f Makefile.startup-os commercial-launch-full
```

Or step by step:

```bash
make -f Makefile.startup-os startup-os-day
make -f Makefile.startup-os startup-release-gate
make -f Makefile.startup-os commercial-launch-control
make -f Makefile.startup-os startup-os-test
make -f Makefile.startup-os commercial-launch-test
make -f Makefile.startup-os startup-web-verify
```

## Generated outputs

- `reports/startup_command_center/latest.md`
- `reports/founder_daily_brief/latest.md`
- `reports/startup_proof_pack/latest.md`
- `reports/startup_release_gate/latest.md`
- `reports/commercial_launch_control/latest.md`
- `apps/web/lib/commercial-launch-control-snapshot.ts`

## Frontend pages

- `/app/command-room`
- `/app/startup-command`
- `/app/founder-brief`
- `/app/commercial-launch`

## Launch products

- Revenue Command Room OS
- Company Brain OS
- Follow-up Recovery OS
- Client Delivery OS
- AI Trust and Governance OS

## Sprint packages

- AI Revenue Diagnostic
- 7-Day Revenue Command Room Sprint
- 14-Day Company Brain Sprint
- Monthly Managed OS

## Merge order

1. Review database foundation first if it remains open.
2. Rebase commercial launch pack on updated `main`.
3. Run Startup OS Release Gate.
4. Run apps/web verifier.
5. Resolve conflicts.
6. Merge only after the launch pack is reviewable and safe.

## Launch guardrails

- Review-first external action.
- No fake ROI.
- No fake testimonials.
- No guaranteed revenue claim.
- `source_url` required.
- Pain remains a hypothesis until verified.
- Proof pack required after every paid sprint.

## Founder operating rhythm

Every commercial launch day:

1. Run `commercial-launch-full`.
2. Open `reports/commercial_launch_control/latest.md`.
3. Review the top P1 accounts.
4. Prepare three discovery notes.
5. Create one scoped diagnostic proposal only after qualification.
6. Record every founder action in HubSpot or local ledgers.
7. Attach proof notes after every paid sprint.

## What this proves

This proves that the commercial launch system is connected, generated, frontend-backed, and safe by default.

## What this does not prove

- Public SaaS readiness.
- Live billing readiness.
- Live external messaging readiness.
- Full repository CI green status.

Those remain separate gates.
