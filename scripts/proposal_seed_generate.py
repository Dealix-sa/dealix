#!/usr/bin/env python3
"""Proposal Builder (review-only) — generates a proposal DRAFT, never sends.

Output:
    outputs/proposals/YYYY-MM-DD/<company_slug>/proposal_draft.md

The draft is for founder review and MANUAL sending only. No email/API/SMTP.
No guaranteed ROI, no unproven claims.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

from _v7_revenue_common import OUTPUTS, SAFETY_BANNER, slugify, today, write_text

SECTIONS = [
    "situation",
    "diagnosed pain",
    "recommended workflow",
    "scope",
    "what is included",
    "what is not included",
    "timeline",
    "price range SAR",
    "client inputs",
    "human approval boundaries",
    "data/security notes",
    "acceptance criteria",
    "next step",
]


def build(ctx: dict) -> str:
    ctx = dict(ctx)
    ctx["date"] = today(ctx.get("date"))
    company = ctx["company"]
    vertical = ctx.get("vertical", "")
    pain = ctx.get("pain_angle", "")
    offer = ctx.get("selected_offer", "Paid Diagnostic")
    price = ctx.get("price_range", "TBD per offer ladder")

    return f"""# Proposal Draft — {company}

> {SAFETY_BANNER}
> REVIEW ONLY. Founder sends this manually after approval.

- Vertical: {vertical}
- Prepared: {ctx['date']}
- Offer: {offer}

## Situation
{company} operates in {vertical}. This proposal addresses the friction we
discussed and is based on hypotheses to be confirmed in delivery.

## Diagnosed pain
{pain or "To be confirmed in discovery/diagnostic."}

## Recommended workflow
A founder-approved workflow that prepares drafts/handoffs while keeping a
human approval gate on every external action.

## Scope
One workflow, one measurable outcome, fixed boundaries.

## What is included
- Workflow mapping and setup
- Review-only draft generation
- Founder/operator approval gates
- Handover documentation

## What is not included
- Automated external sending
- Scraping or unauthorized data collection
- Guaranteed business outcomes

## Timeline
2–4 weeks for the initial scope (indicative).

## Price range SAR
{price}

## Client inputs
- Access to the relevant process/data under agreement
- A point of contact for review
- Timely feedback on drafts

## Human approval boundaries
Every external action (messages, sends, submissions) is executed by a human
after approval. The system only prepares.

## Data/security notes
- DPA/agreement required before any real data.
- PDPL-aware handling; data minimization by default.
- No secrets or credentials stored in artifacts.

## Acceptance criteria
- Agreed metric is measured before/after.
- Deliverables match the scope above.
- Client signs off on the outcome.

## Next step
Founder reviews this draft and sends it **manually**. No part of this document
is auto-sent.
"""


def generate(ctx: dict) -> dict:
    content = build(ctx)
    date = ctx.get("date") or today()
    slug = slugify(ctx["company"])
    out_path = OUTPUTS / "proposals" / date / slug / "proposal_draft.md"
    write_text(out_path, content)
    return {"out_path": str(out_path), "company": ctx["company"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--company", default="")
    parser.add_argument("--vertical", default="")
    parser.add_argument("--pain-angle", default="")
    parser.add_argument("--selected-offer", default="")
    parser.add_argument("--price-range", default="")
    parser.add_argument("--date", default=None)
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    if args.example or not args.company:
        ctx = {
            "company": args.company or "Example Retail Co",
            "vertical": args.vertical or "retail",
            "pain_angle": args.pain_angle or "manual restock approvals across branches",
            "selected_offer": args.selected_offer or "Paid Diagnostic",
            "price_range": args.price_range or "5,000–15,000 SAR (indicative)",
            "date": args.date,
        }
    else:
        ctx = {
            "company": args.company,
            "vertical": args.vertical,
            "pain_angle": args.pain_angle,
            "selected_offer": args.selected_offer,
            "price_range": args.price_range,
            "date": args.date,
        }
    result = generate(ctx)
    print(f"[proposal_seed] {result['company']} → {result['out_path']}")
    print(f"[proposal_seed] {SAFETY_BANNER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
