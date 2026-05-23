# Win / Loss Review

> Every closed-won and closed-lost gets a 5-minute review and a logged learning.
> Patterns drive ICP, messaging, and pricing changes.

## Why

Win/Loss data is the highest-signal input for strategy. Loss patterns reveal the true objections. Win patterns reveal the true value.

## When To Run

- Per closed-won: within 7 days of payment
- Per closed-lost: within 7 days of close-lost stage move
- Aggregate review: monthly during Weekly CEO Review (last Sunday of month)

## Per-Deal Capture

In `pipeline/win_loss_log.md` (private repo):

```yaml
deal_id: D-NNNN
closed_at: YYYY-MM-DD
outcome: won | lost
rung: free | sprint | pack | managed_2999 | managed_4999 | custom
sector: ...
buyer_role: ...
source: warm_outreach | content | referral | partner | inbound
days_in_pipeline: ...
proposals_sent: ...
amount_sar: ...

if won:
  what_won_it: |
    Honest assessment, not marketing.
  expected_ltv_sar: ...
  case_study_consent: yes | partial | no | tbd

if lost:
  why_lost:
    - price
    - timing
    - fit
    - trust
    - competition (which?)
    - no_decision
    - process
    - other
  verbatim_reason: |
    What the buyer actually said
  could_we_have_won: yes | no | maybe
  what_we_could_have_done_differently: |
    Honest — not excuses
```

## Aggregate Monthly Review

```markdown
# Win/Loss Monthly Review — YYYY-MM

## Numbers
- Won: __ (SAR _____ closed)
- Lost: __
- Win rate: ___% (proposals → won within 60 days)

## Win Patterns
- Most common source for wins: _____
- Most common sector for wins: _____
- Most common rung for wins: _____
- Common phrase / signal that preceded a win: _____

## Loss Patterns
- Most common reason for loss: _____ (count)
- Most common sector lost: _____
- Most common competitor (if cited): _____
- Most common rung lost: _____

## What This Suggests
- ICP refinement: _____
- Messaging refinement: _____
- Pricing review: _____
- New experiment to run: _____

## Decisions
- ICP weight changes: _____
- Sector playbook updates: _____
- Pricing experiments: _____
- Sales motion changes: _____
```

## Loss Categorization Discipline

Be honest. A buyer says "too expensive" — but the real reason might be:
- They didn't see enough value (our framing)
- Wrong rung for their need (our qualification)
- Wrong buyer involved (our targeting)
- Competition was cited late (our awareness)

Capture verbatim + categorize. Don't bucket lazily.

## Anti-Patterns

- "Lost because of price" without verifying
- Wins captured but never reviewed
- Losses categorized only by the founder's gut, no buyer input
- "We couldn't have won this one" without honesty check
- Failing to feed back into ICP / messaging / pricing

## Win/Loss Calls (when feasible)

For losses:
- Request a 15-min "post-mortem" call within 7 days of close-lost
- Frame: "We respect your decision. Mind sharing what we could have done differently?"
- If they accept: capture verbatim + use for learning

For wins:
- Capture during Day-7 handoff call
- "What was the single thing that made you say yes?"

## Storage + Privacy

- Win/loss log in private repo only
- Verbatim quotes redacted before any public use (per `TESTIMONIAL_CAPTURE.md`)
- Aggregate patterns can appear in monthly board memo (anonymized)
- Specific competitor names stay private

## What This Refuses

- Cherry-picking wins for narrative
- Ignoring losses ("we wouldn't have wanted them anyway")
- Not contacting buyers post-loss
- Letting loss patterns persist without changing ICP / message / pricing
- Treating one loss as a trend (or one win as proven)
