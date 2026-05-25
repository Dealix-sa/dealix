# Win-Loss Review — مراجعة الفوز والخسارة

## Purpose
After every closed deal — won or lost — capture why. The pattern across many win-loss reviews is the most direct signal for sector strategy, pricing, and positioning.

## Owner
Founder.

## Inputs
- Closed deal data: client name (private), sector, deal size band, outcome.
- Conversations with the client (won) or the decision-maker (lost).
- Internal proposal and negotiation history.

## Outputs
- Win-loss entry per closed deal.
- Quarterly aggregate analysis.

## Rules (numbered)
1. Every closed deal gets a review entry within 14 days of close.
2. Won deals: capture why we won, in the client's words where possible.
3. Lost deals: capture why we lost, with a conversation with the decision-maker when accessible.
4. Reviews are private (under `dealix-ops-private/`) by default; anonymized aggregates may surface in public learning notes.
5. No spin. If we lost on price, we write "lost on price", not "lost on perceived value".
6. Aggregate patterns reviewed quarterly.

## Metrics
- Win-loss reviews completed per closed deal (target 100 percent).
- Conversations with lost decision-makers (target greater than or equal to 50 percent).
- Days from close to review entry.

## Cadence
Per close. Quarterly aggregate.

## Evidence (paths)
- `dealix-ops-private/win_loss/<deal_id>.md` (private).
- Anonymized aggregates referenced in `docs/learning/COMPANY_MEMORY.md`.

## Verifier
Founder.

## Runtime Command
`make learning.winloss.new DEAL=<id>` opens a review entry skeleton.

## Entry template

```
Deal ID: <id>
Date closed: YYYY-MM-DD
Outcome: won | lost | no-decision
Sector: <code>
Deal size band: <SAR band>
Geo: <country/region>

Why we won (or lost):
- <reason 1, with evidence or quote where available>
- <reason 2>
- <reason 3>

Decision criteria as stated by the buyer:
- <criterion 1>
- <criterion 2>

What we did well:
- <observation>

What we did poorly or could have done better:
- <observation>

What we would change in our process:
- <action item, with owner>

Quote (with permission):
> <buyer or operator quote>
```

## Quarterly aggregate

Each quarter, the founder reads all win-loss entries from the quarter and produces an anonymized aggregate:

- Win rate by sector.
- Win rate by deal size band.
- Top three reasons for wins (frequency).
- Top three reasons for losses (frequency).
- Decision criteria patterns: what buyers consistently care about.
- Operational changes proposed and adopted.

The aggregate is summarized in `docs/learning/MONTHLY_STRATEGY_UPDATE.md` and informs the next quarter's sector focus.

## Operating substance
Most teams hold post-mortems for losses and silently celebrate wins. Dealix reviews both because wins are as informative as losses. A pattern in why-we-won is a pattern we can replicate; a pattern in why-we-lost is a pattern we can defend against.

The discipline of writing within 14 days is what preserves the signal. After 30 days, the operator's memory has rewritten the deal. Within 14 days, the details are still recoverable.

The "no spin" rule is the hardest. Losing on price is uncomfortable to write; rewriting it as "lost on perceived value" feels softer but produces no learning. We write what happened.

Conversations with lost decision-makers are the highest-value input and the lowest-frequency. Buyers will often share why they chose a competitor if asked respectfully and with a short, focused ask. The 50 percent target is aspirational; even 30 percent yields the patterns we need.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
