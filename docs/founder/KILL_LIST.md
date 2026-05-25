# Kill List

> What we are explicitly **not** doing.
> The Kill List is more valuable than the roadmap.

## Why this file exists

The cost of saying yes to the wrong thing is invisible.
The cost of saying no is fully visible (the thing not done).
This file makes the invisible cost legible: we wrote it down.

## Rules

1. Once on the Kill List, an item cannot return without
   **named evidence** that the original reason for killing it is gone.
2. Every kill has a reason. "It does not fit" is not a reason.
3. Every kill names the alternative we chose instead.
4. Kill items expire after 6 months — at that point they must be
   re-affirmed (still killed) or formally revisited.

## Format

```
- id: K-yyyy-mm-dd-NN
  item: "..."
  reason: "..."
  evidence_against: "..."
  alternative_chosen: "..."
  killed_on: yyyy-mm-dd
  revisit_trigger: "..."
  re-affirm_date: yyyy-mm-dd
```

## Current Kill List

- id: K-template
  item: "Build a marketplace product"
  reason: "No repeatable customer pull; would require capital we do not have."
  evidence_against: "Zero inbound demand for marketplace; all customer asks are for done-for-you intelligence."
  alternative_chosen: "Revenue Sprint as the wedge product."
  killed_on: 2026-01-01
  revisit_trigger: "≥ 10 paying Sprint customers asking unprompted for a marketplace."
  re-affirm_date: 2026-07-01

- id: K-template-2
  item: "Build a full SaaS product before validation"
  reason: "SaaS without repeated manual delivery has no template, pricing, or retention model."
  evidence_against: "Zero customers have asked for self-serve."
  alternative_chosen: "Manual sprints → templates → automation → SaaS, in that order."
  killed_on: 2026-01-01
  revisit_trigger: "≥ 5 retainers asking for self-serve access."
  re-affirm_date: 2026-07-01

- id: K-template-3
  item: "Expand to all sectors simultaneously"
  reason: "Founder-led sales requires focused ICP; broad targeting kills reply rates."
  evidence_against: "Industry data on cold outreach reply rates by specificity."
  alternative_chosen: "2–3 sectors maximum during pre-PMF."
  killed_on: 2026-01-01
  revisit_trigger: "Two sectors at ≥ 3 retainers each."
  re-affirm_date: 2026-07-01

- id: K-template-4
  item: "Enterprise sales motion before founder-led proof"
  reason: "Enterprise cycles will starve cash and learning loop."
  evidence_against: "No completed case studies yet."
  alternative_chosen: "SMB → mid-market via Sprint → Retainer."
  killed_on: 2026-01-01
  revisit_trigger: "≥ 2 completed enterprise-grade case studies + ≥ 3 enterprise inbound asks."
  re-affirm_date: 2026-07-01

- id: K-template-5
  item: "Hiring before workflow repeatability"
  reason: "Hiring before templates means hiring is the bottleneck, not the leverage."
  evidence_against: "No workflow has hit 10 successes yet."
  alternative_chosen: "Founder + AI assist until hiring triggers fire (see `HIRING_TRIGGERS.md`)."
  killed_on: 2026-01-01
  revisit_trigger: "See `HIRING_TRIGGERS.md`."
  re-affirm_date: 2026-07-01
