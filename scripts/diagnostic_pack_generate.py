#!/usr/bin/env python3
"""Diagnostic Delivery Generator — builds a review-only diagnostic pack.

Inputs (CLI flags or --example for a worked sample):
    --company, --vertical, --pain-angle, --notes, --selected-offer

Outputs under outputs/diagnostics/YYYY-MM-DD/<company_slug>/:
    diagnostic_brief.md
    workflow_map.md
    risk_map.md
    pilot_recommendation.md
    proposal_seed.md
    handover_checklist.md

This produces internal preparation documents only. It does not contact the
client, send anything, or process real client data without agreement.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

from _v7_revenue_common import (
    OUTPUTS,
    SAFETY_BANNER,
    slugify,
    today,
    write_text,
)


def _brief(ctx: dict) -> str:
    return f"""# Diagnostic Brief — {ctx['company']}

> {SAFETY_BANNER}

- Vertical: {ctx['vertical']}
- Pain angle: {ctx['pain_angle']}
- Selected offer: {ctx['selected_offer']}
- Prepared: {ctx['date']}

## Situation (hypothesis)
We believe {ctx['company']} ({ctx['vertical']}) loses time/cost to:
{ctx['pain_angle']}.

## Diagnostic goals
1. Confirm the real friction with the client (interview + data review).
2. Map the current workflow end to end.
3. Identify the highest-leverage automation candidate.
4. Decide GO / NO-GO on a paid pilot.

## Notes
{ctx['notes']}

## Boundaries
- No real client data is processed without a signed agreement.
- All recommendations are hypotheses until validated with the client.
- No guaranteed ROI is claimed.
"""


def _workflow_map(ctx: dict) -> str:
    return f"""# Workflow Map — {ctx['company']}

> {SAFETY_BANNER}

## Current state (to confirm with client)
1. Trigger / intake
2. Manual handling step(s)
3. Decision / approval
4. Output / handoff
5. Follow-up

## Friction points (hypotheses)
- Where {ctx['pain_angle']} shows up most.
- Manual rework loops.
- Hand-off delays.

## Target state (proposed)
- Founder-approved automation prepares drafts/handoffs.
- Human stays in the approval loop for every external action.
"""


def _risk_map(ctx: dict) -> str:
    return f"""# Risk Map — {ctx['company']}

> {SAFETY_BANNER}

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Data access blocked | Medium | High | Start with anonymized/sample data |
| Wrong process targeted | Medium | High | Validate in discovery before pilot |
| Over-automation | Low | High | Keep human approval gates |
| Scope creep | Medium | Medium | Fixed pilot scope + acceptance criteria |
| Privacy/PDPL | Low | High | DPA before any real data |
"""


def _pilot_reco(ctx: dict) -> str:
    return f"""# Pilot Recommendation — {ctx['company']}

> {SAFETY_BANNER}

## Recommendation
Run a scoped pilot on the single highest-leverage workflow tied to:
{ctx['pain_angle']}.

## Pilot shape
- Duration: 2–4 weeks.
- One workflow, one clear metric.
- Human approval gate on every external action.
- Acceptance criteria agreed up front.

## GO / NO-GO
- GO if discovery confirms the friction is real, measurable, and the client
  can provide access/data under agreement.
- NO-GO if the pain is not confirmed or data cannot be shared safely.
"""


def _proposal_seed(ctx: dict) -> str:
    return f"""# Proposal Seed — {ctx['company']}

> {SAFETY_BANNER}

This seed feeds `scripts/proposal_seed_generate.py`. Review-only.

- Company: {ctx['company']}
- Vertical: {ctx['vertical']}
- Diagnosed pain: {ctx['pain_angle']}
- Recommended offer: {ctx['selected_offer']}
- Price range: to be set by founder per offer ladder (SAR).
- Next step: founder reviews → sends proposal manually.
"""


def _handover(ctx: dict) -> str:
    return f"""# Handover Checklist — {ctx['company']}

> {SAFETY_BANNER}

- [ ] Discovery completed and notes recorded
- [ ] Workflow map confirmed with client
- [ ] Risk map reviewed
- [ ] Pilot scope + acceptance criteria agreed
- [ ] DPA/agreement in place before real data
- [ ] Proposal drafted (review-only) and approved by founder
- [ ] Proposal sent MANUALLY by founder
- [ ] Outcome recorded in manual events ledger
"""


def generate(ctx: dict) -> dict:
    ctx = dict(ctx)
    ctx["date"] = today(ctx.get("date"))
    slug = slugify(ctx["company"])
    out_dir = OUTPUTS / "diagnostics" / ctx["date"] / slug
    files = {
        "diagnostic_brief.md": _brief(ctx),
        "workflow_map.md": _workflow_map(ctx),
        "risk_map.md": _risk_map(ctx),
        "pilot_recommendation.md": _pilot_reco(ctx),
        "proposal_seed.md": _proposal_seed(ctx),
        "handover_checklist.md": _handover(ctx),
    }
    for name, content in files.items():
        write_text(out_dir / name, content)
    return {"out_dir": str(out_dir), "files": list(files), "company": ctx["company"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--company", default="")
    parser.add_argument("--vertical", default="")
    parser.add_argument("--pain-angle", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--selected-offer", default="")
    parser.add_argument("--date", default=None)
    parser.add_argument("--example", action="store_true", help="Use a worked sample")
    args = parser.parse_args()

    if args.example or not args.company:
        ctx = {
            "company": args.company or "Example Logistics Co",
            "vertical": args.vertical or "logistics",
            "pain_angle": args.pain_angle or "manual order-status updates to customers",
            "notes": args.notes or "Discovery call pending; hypotheses only.",
            "selected_offer": args.selected_offer or "Paid Diagnostic",
            "date": args.date,
        }
    else:
        ctx = {
            "company": args.company,
            "vertical": args.vertical,
            "pain_angle": args.pain_angle,
            "notes": args.notes,
            "selected_offer": args.selected_offer,
            "date": args.date,
        }
    result = generate(ctx)
    print(f"[diagnostic_pack] {result['company']} → {result['out_dir']}")
    print(f"[diagnostic_pack] {SAFETY_BANNER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
