# Trust Preflight Rules

> **Status:** Operating policy. The preflight runs on every draft.
> **Tool:** `scripts/trust_preflight_dry_run.py`.
> **Schema:** `schemas/launch/trust_preflight.schema.json`.

## The 3 phases of the preflight

### Phase 1 — Pattern check (regex)

The preflight scans the draft for banned patterns:

- "guaranteed ROI" patterns.
- "cold WhatsApp" patterns.
- "payment link" patterns.
- "final price" patterns.
- "fake proof" patterns.
- "scraping" patterns.
- "API key" patterns.
- "real phone number" patterns.
- "real email" patterns (in examples, not in founder signature).

### Phase 2 — Schema check

The preflight validates the draft against its schema (`outreach_draft.schema.json`, `proposal_pack.schema.json`, etc.):

- `evidence_level` field is present and in L0–L5.
- `risk_level` field is present and in low/medium/high.
- `approval_required` field is `true` for any external channel.
- `pricing_status` field is present for any draft with a price reference.
- `consent_record` is referenced for any WhatsApp draft.

### Phase 3 — Code check (for scripts)

For Python scripts, the preflight scans the source for:

- `requests.post` or `requests.put` (external send).
- `smtplib` (email send).
- `sendgrid` or `sendgrid.send`.
- `twilio` or `twilio.messages.create`.
- `subprocess.run` with a network command.
- `urllib.request` to a non-allowlisted host.
- `socket.connect` to a non-allowlisted port.

If any of these are present, the script fails the preflight.

## The 5 hard preflight rules

1. **No draft is sent without a PASS.** The preflight is the first gate.
2. **No override is silent.** The founder's override is logged.
3. **No pattern is allowed because "it was meant differently."** The regex matches the string, not the intent.
4. **No script runs in production without preflight.** Local dry-runs are fine.
5. **No draft bypasses the queue.** The approval queue is the only path.

## The preflight output

```json
{
  "preflight_id": "pf_001",
  "draft_id": "outreach_2024_agency_001",
  "run_at_iso": "2024-12-01T10:00:00Z",
  "phase_1_pattern": {
    "status": "PASS",
    "banned_matches": []
  },
  "phase_2_schema": {
    "status": "PASS",
    "errors": []
  },
  "phase_3_code": {
    "status": "N/A",
    "errors": []
  },
  "overall_status": "PASS",
  "reviewer": "trust_preflight_dry_run.py v1.0"
}
```

If `overall_status: FAIL`, the draft is rejected.

## The re-run rule

A draft that fails can be rewritten and re-run. The preflight is idempotent.

## The allowlist (for code)

The preflight's code scanner maintains an allowlist of safe imports and calls:

- `import os`, `import sys`, `import json`, `import yaml` → safe.
- `import pathlib` → safe.
- `import argparse` → safe.
- `open()`, `read()`, `write()` on local files → safe.
- `requests.get` to allowlisted hosts (e.g. the founder's API) → safe if explicitly allowed.
- All other network calls → blocked.

The allowlist is in `scripts/trust_preflight_dry_run.py`.

## The escalation

- A founder override of a preflight FAIL must be logged in the approval queue with `override_reason`.
- A re-run after a FAIL must be logged in the approval queue.
- A preflight PASS that is later found to have missed something must trigger a preflight rule update.

## When to update the preflight

- When a new banned pattern emerges.
- When a new safe pattern is identified.
- When a violation is discovered in the wild.
- When the schema is updated.
