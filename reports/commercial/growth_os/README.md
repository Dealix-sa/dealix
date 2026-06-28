# Commercial Growth OS — Command Room reports

This directory holds the latest run output of the Dealix Commercial Growth OS v2.

| File | What it is |
|------|------------|
| `latest.json` | Full machine-readable command-room snapshot + proof pack + pipeline events. |
| `latest.md` | Human-readable command room: safety posture, summary, decisions required, risks, next 10 actions. |
| `README.md` | This file. |

## Regenerate

```bash
python scripts/commercial/run_commercial_growth_os.py
# or
make commercial-growth-os
```

## Safety note

These reports are **draft-only artefacts**. Nothing here has been sent, no
calendar event has been written, and no proposal price has been finalised.
Every actionable item is queued for explicit human approval in the decision
queue. See `docs/commercial/CONTROLLED_LIVE_OUTBOUND_POLICY_AR.md` and
`docs/commercial/COMMERCIAL_AUTONOMY_LEVELS_AR.md`.

The sample committed here is generated from `data/commercial/*.sample.json`
and contains **no real client data**.
