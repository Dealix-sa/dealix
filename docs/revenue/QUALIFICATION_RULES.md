# Qualification Rules

> What it takes for a lead to become "qualified".
> Stricter than the average startup playbook — by design.

## The 5-Question Qualification (BANT-adjusted for Saudi mid-market)

A lead is qualified only when 4 of 5 are TRUE:

1. **Fit (F):** Tier 1 ICP per `ICP_STRATEGY.md`? Score ≥ 60?
2. **Budget (B):** Realistic spend capacity for at least Rung 2 (499 SAR) — visible from company size / sector?
3. **Authority (A):** Direct line to founder / CEO / Head of Sales? Or warm intro?
4. **Need (N):** Visible signal of revenue-ops pain (recent SDR hire/loss, CRM purchase, public hiring page mentioning sales ops, etc.)?
5. **Timing (T):** No active competing engagement / no recent failed RFP cycle that would block

If only 3 of 5 are true → stays in "lead" stage, not qualified.
If only 2 of 5 → suppression candidate.

## Source Of Truth For Each Question

| Question | Source / agent |
|---|---|
| Fit | `dealix/agents/scoring_agent.py` (when present) + ICP scoring weights |
| Budget | Enrichment agent (revenue band, employee count, sector benchmark) |
| Authority | Manual research + LinkedIn role check |
| Need | Pain hypothesis agent (signals: hiring page, recent news, CRM purchase) |
| Timing | Manual + competitor scan |

## Auto-Disqualifiers

A lead is **immediately** suppressed (not just disqualified) if any of these:
- Pre-revenue company
- Outside Saudi (unless Tier 3 unlock active)
- On suppression list (any reason)
- Direct competitor
- Compliance-only buyer (we don't sell to procurement-only relationships)
- Has explicitly said "not interested" in any past interaction

## Soft Signals (raise score but don't qualify alone)

- Active LinkedIn presence by buyer
- Has English + Arabic ops
- Recently raised funding
- Recently launched new product line
- Recently expanded to new city
- Active in trade associations we map

## Qualification Output

For each qualified lead, the qualification agent produces:

```yaml
lead_id: L-2026-0142
fit_score: 78
sector: logistics
buyer: Head of Sales
buyer_authority: confirmed (LinkedIn + intro)
pain_hypothesis: |
  Recently posted 2 SDR roles after losing senior AE; current CRM is HubSpot,
  no visible lead scoring in their stack
budget_estimate: SAR 500-5000 monthly
timing_window: 30 days (post-Ramadan rebuild)
recommended_offer: Free Diagnostic → Sprint
recommended_channel: warm intro via {advisor_name} → LinkedIn DM
risk_flags: []
evidence:
  - https://example.com/news/x  # public sources only
  - https://linkedin.com/...     # public profile
```

## Forbidden Sources

- Scraped contact databases
- Leaked datasets
- "Founder list" purchases
- Unverified third-party intent data
- Anything that can't be cited publicly

## Confidence + Honesty Rule

If the agent isn't sure on a field, it writes `unknown` — **not a guess**. Hallucinated qualification data is a Trust incident (logged + scored).

## When To Re-Qualify

A previously disqualified lead re-enters Lead stage only if:
- A trigger signal fires (new role, new funding, new sector launch)
- > 90 days have passed since prior disqualification
- They were NOT on the suppression list

Suppression-list contacts are **never** re-qualified without founder + advisor signoff.

## Review Cadence

- Weekly: % qualified vs total leads (target 50%)
- Monthly: qualification quality audit — of the 10 "qualified" leads, how many actually replied? Adjust weights if < 15% reply.
- Quarterly: rewrite ICP scoring weights based on closed-won patterns

## What This Refuses

- "Qualify everyone, sort later"
- Buying intent data without source verification
- Letting volume metrics override quality
- Skipping the Authority check ("we'll figure out who to contact later")
