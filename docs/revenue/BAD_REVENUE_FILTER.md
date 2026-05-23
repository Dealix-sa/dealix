# مرشّح الإيراد الرديء — Bad Revenue Filter

> Revenue is not revenue unless it improves cash, proof, repeatability, trust, or learning.

## Purpose
Reject deals that are technically revenue but degrade Dealix. A bad deal taken is a moat lost.

## Owner
Founder/CEO.

## Inputs
- Proposal under consideration.
- Customer profile (ICP fit).
- Scope and exclusion list.
- Capacity at the proposed delivery window.

## Outputs
- A pass/fail filter result written into the proposal record.
- If fail: a polite decline letter (templated).

## Rules
1. Every proposal runs through this filter before the price is communicated externally.
2. A proposal must improve at least one of: cash, proof, repeatability, trust, learning. Two or more is preferred.
3. A proposal that fails on Trust is rejected regardless of cash benefit.
4. A proposal below margin floor without a declared bet (`docs/strategy/STRATEGIC_BETS.md`) is rejected.
5. The filter result is logged in the proposal record. Skipping the filter is a process exception requiring a written reason.

## Metrics
- Proposals filtered: 100%.
- Proposals rejected by this filter: tracked.
- Post-deal regret rate: target 0 (any "we should have rejected" learning).

## Cadence
Per proposal.

## Evidence
Filter result inside each proposal file.

## Verifier
`make bad-revenue-verify` — confirms each accepted proposal has a filter result recorded.

## Runtime Command
`make filter-proposal proposal=<id>`

---

## The Five Tests

### 1. Cash
Does this deal materially improve cash position in the next 60 days?

- Strong yes: large deposit on signing.
- Weak yes: net positive but not material.
- No: negative or breakeven cash within 60 days.

### 2. Proof
Will this deal produce a case-safe artifact (anonymized) Dealix can reference later?

- Strong yes: written consent to publish case-safe template.
- Weak yes: aggregate sector data only.
- No: zero artifact possible (NDA forbids any anonymized output).

### 3. Repeatability
Does this deal fit (or extend) an offer rung shape that Dealix wants to repeat?

- Strong yes: matches an existing rung; adds to 3/5/10 count.
- Weak yes: novel but adjacent.
- No: bespoke; cannot inform any future deal.

### 4. Trust
Does this deal preserve or strengthen Dealix's trust posture?

- Strong yes: respects disclosure, refund, governance norms.
- Weak yes: requires no compromise.
- No: requires a banned tactic, asks for guarantees, or compromises disclosure.

### 5. Learning
Does this deal teach Dealix something useful (new ICP angle, sector pattern, delivery insight)?

- Strong yes: novel ICP or sector entry meeting `MARKET_ENTRY_DECISION.md` stage rule.
- Weak yes: incremental learning.
- No: redundant with existing knowledge.

## Filter result template

```
# Bad Revenue Filter Result
Proposal: <id>
Date: YYYY-MM-DD

Cash: strong yes / weak yes / no — note
Proof: ... — note
Repeatability: ... — note
Trust: ... — note
Learning: ... — note

Pass conditions:
- At least one "strong yes" or two "weak yes".
- Trust = "no" → automatic reject regardless.
- Margin below floor without declared bet → automatic reject.

Decision: ACCEPT / REJECT / REWORK
Reason (if reject or rework):
Decline letter (if reject): sent YYYY-MM-DD
```

## Margin floor
- Default margin floor: 40% (after founder shadow rate of SAR 600/hour).
- Below floor: rejected unless a declared bet in `STRATEGIC_BETS.md` justifies a market-entry investment.

## Polite decline (template)
> Thank you for the conversation. After reviewing the scope, Dealix is not the right fit for this engagement because <reason in one sentence>. We are happy to refer you to <partner / alternative> if useful. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## Examples of automatic reject
- "We need a guarantee of 30% sales lift."
- "We need you to send 10,000 cold outreach messages."
- "We need full white-label — no Dealix branding anywhere."
- "The contract forbids any anonymized reference, even aggregated."
- "Payment after 120 days, no deposit."

## القواعد العربية
1. كل عرض يمر بالمرشّح قبل تواصل سعري.
2. العرض يجب أن يحسّن نقدًا أو دليلًا أو تكرارًا أو ثقة أو تعلمًا. اثنان أفضل.
3. الفشل في الثقة يعني رفضًا تلقائيًا.

## Cross-links
- `CASH_RULES.md`
- `OFFER_LADDER.md`
- `docs/strategy/ICP_STRATEGY.md`
- `docs/strategy/STRATEGIC_BETS.md`
- `docs/14_trust_os/TRUST_OS.md`
