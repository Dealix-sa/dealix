# Growth Experiments — تجارب النمو

> The experiment backlog. Every experiment is a **hypothesis** with a single success metric and a
> **guardrail** that protects the hard rules. Forward-looking numbers are hypotheses, not
> guarantees. Status: `DOCS_ONLY`. Metrics defined in `GROWTH_METRICS.md`.

## كيف نجري التجارب (How we run them)

1. State a hypothesis (one variable). 2. Pick one metric. 3. Set a guardrail (what must NOT break).
4. Run for a fixed window. 5. Decide: ship / kill / iterate. No experiment may violate the hard
rules (no fake scarcity, no auto-send, no guaranteed revenue, no scraping).

## السجل (Backlog)

| # | Hypothesis | Metric | Guardrail | Status |
|---|------------|--------|-----------|--------|
| E1 | Showing the Score result *before* email capture lifts Score completion | Score completions / visitors | No forced wall; PDPL consent intact | `Proposed` |
| E2 | Routing free-tool results to Diagnostic (not Sprint) raises qualified bookings | Diagnostics / tool completions | Only one CTA per page | `Proposed` |
| E3 | An Arabic category-definition Learn page improves GEO citation + Score CTR | Score CTR from Learn | No ranking promises; claims dated | `Proposed` |
| E4 | A B2B-services sector page out-converts the generic diagnostic page | Diagnostic conversion (sector vs generic) | Claims evidence/hypothesis-framed | `Proposed` |
| E5 | Proof Pack preview on the Diagnostic page reduces no-shows | Diagnostic show-rate | No fake testimonials | `Proposed` |
| E6 | Manual, founder-approved Sequence 1 lifts tool-lead → Diagnostic | Tool-lead → Diagnostic rate | No auto-send; opt-in only | `Proposed` |
| E7 | Post-proof referral ask yields warm Diagnostics | Referral rate | Honest incentives only | `Proposed` |
| E8 | Simplifying the Diagnostic form (fewer fields) raises completion | Form completion rate | Keep PDPL consent field | `Proposed` |
| E9 | One founder case study/week increases inbound Score starts | Inbound Score starts | Approved Proof Pack only | `Proposed` |
| E10 | A partner-shared Diagnostic link converts comparably to direct | Partner-link Diagnostic rate | No scraping; warm only | `Proposed` |
| E11 | Trust/governance page as a Diagnostic waypoint lifts hot-tier conversion | Diagnostic → Sprint rate | No overstated claims | `Proposed` |
| E12 | Pricing transparency (ladder visible) shortens time-to-Sprint | Days from Diagnostic → Sprint | No anchoring tricks/fake discounts | `Proposed` |

## قواعد الإيقاف (Kill rules)

- Kill any experiment that requires a dark pattern, fake scarcity, or an unapproved external send.
- Kill if the guardrail metric degrades, even when the success metric improves.

## خطة 30 يوم (30-day plan)

1. Prioritize 3 experiments (suggest E1, E2, E5) — highest leverage on the Score→Diagnostic→Sprint spine.
2. Define exact metric + guardrail thresholds for each before launch.
3. Run each for a fixed 2-week window with a clear ship/kill decision.
4. Record outcomes here (move status to `Running` → `Shipped`/`Killed`) and in the dashboard.
5. Feed every shipped winner back into `CONVERSION_PLAYBOOK.md`.
