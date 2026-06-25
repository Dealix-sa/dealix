# Dealix Startup OS Release Gate

## Purpose

The Startup OS Release Gate verifies that the Dealix daily startup operating system is not only documented, but runnable and connected.

It checks:

- required operating files
- generated reports
- frontend snapshots
- frontend pages
- safety phrases
- startup command center payload

## Command

```bash
python scripts/commercial/verify_startup_os_release_gate.py
```

Or with the standalone Makefile:

```bash
make -f Makefile.startup-os startup-release-gate
```

## Full local validation

```bash
make -f Makefile.startup-os startup-os-day
make -f Makefile.startup-os startup-release-gate
make -f Makefile.startup-os startup-os-test
make -f Makefile.startup-os startup-web-verify
```

## Generated report

- `reports/startup_release_gate/latest.md`
- `reports/startup_release_gate/latest.json`

## Pass criteria

- Startup OS Day runs.
- Commercial command report exists.
- Review actions report exists.
- Startup command center exists.
- Founder daily brief exists.
- Startup proof pack exists.
- Frontend snapshots exist.
- Frontend pages exist.
- Safe defaults and guardrails remain present.

## Safety baseline

This release gate does not enable live outbound.

Required safety posture:

- no live outbound by default
- no fake ROI
- source_url required
- `draft_only` present
- `WHATSAPP_ALLOW_LIVE_SEND` present and documented as false by default

## Founder usage

Every morning:

```bash
make -f Makefile.startup-os startup-os-day
make -f Makefile.startup-os startup-release-gate
```

Then review:

- `reports/startup_command_center/latest.md`
- `reports/founder_daily_brief/latest.md`
- `reports/startup_proof_pack/latest.md`
- `/app/startup-command`
- `/app/founder-brief`

## What this gate does not prove

It does not prove public SaaS readiness.
It does not prove live outbound readiness.
It does not prove billing readiness.
It does not prove all repository CI is green.

It proves the founder-led Startup OS workflow is connected, generated, and safe by default.
