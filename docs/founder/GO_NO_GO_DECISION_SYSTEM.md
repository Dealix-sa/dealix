# نظام قرار "ابدأ / لا تبدأ" — Go / No-Go Decision System

> Formal gate for any non-reversible decision. Especially A3 actions: irreversible, public, customer-facing.

## Purpose
Stop the founder from making irreversible decisions in the same mental mode as reversible ones. Force a written gate.

## Owner
Founder/CEO. A reviewer (advisor or co-founder) signs off on A3 gates when available.

## Inputs
- The decision brief (≤ 1 page, written).
- Evidence cited (artifacts in repo or `dealix-ops-private/`).
- Reversibility classification (A1 / A2 / A3).
- Risk to: cash, trust, customers, brand.

## Outputs
- Signed gate file at `docs/founder/decisions/YYYY-MM-DD_<slug>.md`.
- One-line summary appended to `dealix-ops-private/decisions/log.md`.
- If A3: explicit human approval recorded.

## Rules
1. Any A3 action (irreversible + public + customer-facing) requires this gate. No exceptions.
2. A2 (irreversible but private) requires this gate without a reviewer.
3. A1 (reversible) does not need the gate but must be logged.
4. The gate is run before the action, never as documentation after the fact.
5. A "No-Go" outcome is logged the same way as "Go" — both are decisions.
6. The gate file is immutable once signed; corrections go in a follow-up file.

## Metrics
- A3 actions taken without gate: 0 (target).
- Median time to run gate: ≤ 30 minutes.
- Reversal rate of Go decisions within 90 days: ≤ 10% (signals poor gating).

## Cadence
Per-decision. Reviewed in Monthly Strategy Review for pattern.

## Evidence
`docs/founder/decisions/`.

## Verifier
`make decisions-verify` — checks every A3-tagged action in logs has a matching gate file.

## Runtime Command
`make ceo-gate slug=<decision-slug>`

---

## Reversibility classes

| Class | Definition | Examples |
|---|---|---|
| A1 | Reversible within a week, low blast radius | edit internal doc, change pricing on draft proposal |
| A2 | Irreversible but private | sign a vendor contract, change accounting policy |
| A3 | Irreversible + public + customer-facing | publish a case study, send mass email, public price change, enter new market |

## Gate file template

```
# Decision: <slug>
Date: YYYY-MM-DD
Class: A3
Owner: Founder/CEO
Reviewer: <name or "none — solo founder")

## What is being decided
<single paragraph>

## Why now
<evidence link>

## Reversibility
<A1 / A2 / A3, justification>

## Risks
- Cash:
- Trust:
- Customer:
- Brand:
- Legal:

## Evidence supporting Go
1. <link>
2. <link>

## Evidence supporting No-Go
1. <link>
2. <link>

## Pre-mortem
"In 90 days, if this fails, the most likely reason will be: ___"

## Decision
[ ] Go
[ ] No-Go
[ ] Defer until <condition>

## If Go: success criteria (measurable, dated)
1.
2.

## If Go: kill criteria (measurable, dated)
1.

## Approval
Founder/CEO: signed YYYY-MM-DD
Reviewer (if A3): signed YYYY-MM-DD
```

## Hard "No-Go" signals
- Cash runway < 90 days and decision consumes cash without near-term return.
- Decision implies any external automated send without recipient consent.
- Decision implies a guarantee, ROI claim, or "AI-powered" framing.
- Decision implies using real customer data without anonymization in any public surface.

## القواعد العربية
1. كل قرار A3 يحتاج هذه البوابة. لا استثناء.
2. تُجرى قبل التنفيذ، لا بعده.
3. "لا تبدأ" قرار يُسجَّل مثل "ابدأ" تمامًا.

## Cross-links
- `DECISION_QUALITY_SYSTEM.md`
- `CEO_OPERATING_MODEL.md`
- `KILL_LIST.md`
- `docs/14_trust_os/TRUST_OS.md`
