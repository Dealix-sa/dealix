# Revenue Sprint Kit — Private Setup Steps

The public Dealix repo carries the offer definition, pricing, scope, QA checklist, and no-overclaim policy. The actual operating templates — Founder DM Pack, Sample Pack Template, Proposal Fast Template, Client Intake, Delivery Report Template, Handoff, Feedback Request, Retainer Ask — live in the private `dealix-ops-private` repo so that no client-identifiable text ends up in a public repository.

This document is the checklist for setting up the private side. Run these steps in the `dealix-ops-private` repo, not here.

## Directory Layout

Create under `dealix-ops-private/`:

```
offers/
  revenue_sprint/
    founder_dm_pack.md
    sample_pack_template.md
    proposal_fast_template.md
    payment_followup_templates.md
    client_intake.md
    delivery_report_template.md
    qa_checklist.md
    handoff_template.md
    feedback_request.md
    retainer_ask.md
verify_revenue_sprint_kit.py
```

## File Contents

The content for each template is in the conversation log that established the Revenue Sprint Kit v1. Each template:

- `founder_dm_pack.md` — three Arabic founder DM variants plus two follow-ups and trust rules.
- `sample_pack_template.md` — five-row sample table with prospect, sector, why-relevant, priority, evidence, suggested message; closes with a non-guarantee trust note.
- `proposal_fast_template.md` — client, objective, scope, deliverables, timeline, investment, start condition, out-of-scope, trust note.
- `payment_followup_templates.md` — short payment / PO / written-approval reminder sequences.
- `client_intake.md` — ICP, sectors, geography, deal size, exclusions, success definition, approval contact, data constraints.
- `delivery_report_template.md` — executive summary, ICP, method, lead table, top opportunities, outreach pack, 14-day plan, risks, next step, trust note.
- `qa_checklist.md` — mirrors `docs/delivery/revenue_sprint/QA_CHECKLIST.md` from the public repo.
- `handoff_template.md` — delivered items, recommended first action, operating cadence, what to track, next Dealix support option.
- `feedback_request.md` — four-question Arabic feedback message.
- `retainer_ask.md` — Revenue Desk monthly proposal text.

## Private Verifier

Save as `dealix-ops-private/verify_revenue_sprint_kit.py`:

```python
from pathlib import Path

required = [
    "offers/revenue_sprint/founder_dm_pack.md",
    "offers/revenue_sprint/sample_pack_template.md",
    "offers/revenue_sprint/proposal_fast_template.md",
    "offers/revenue_sprint/payment_followup_templates.md",
    "offers/revenue_sprint/client_intake.md",
    "offers/revenue_sprint/delivery_report_template.md",
    "offers/revenue_sprint/qa_checklist.md",
    "offers/revenue_sprint/handoff_template.md",
    "offers/revenue_sprint/feedback_request.md",
    "offers/revenue_sprint/retainer_ask.md",
]

failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 120:
        failures.append(f"Too short: {file}")

if failures:
    print("Revenue Sprint Kit verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: private Revenue Sprint Kit is ready.")
```

Run with: `python verify_revenue_sprint_kit.py`

## Trust Rules

- No client identity in the public repo.
- No A-priority lead without evidence.
- No delivery without QA pass.
- No case study without written approval.
- No public claim without evidence.

## Completion Criteria

Private kit is ready when:

- All ten template files exist and are filled.
- Private verifier passes.
- At least one full dry-run (intake → sample → proposal → delivery report → QA → handoff → feedback → retainer ask) has been walked end-to-end on a real lead.

## Last Reviewed
2026-05-23
