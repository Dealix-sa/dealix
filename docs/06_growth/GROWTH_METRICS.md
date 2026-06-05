# Growth Metrics — مقاييس النمو

> The dashboard. We measure the **funnel spine**, **loop velocity**, and **leading vs lagging**
> signals. No vanity metrics (no raw follower counts, no impressions-as-success, no "invites sent").
> Status: `DOCS_ONLY`. Targets are hypotheses, not guarantees.

## عمود المسار (The funnel spine)

```text
Visitors → Business OS Score → Diagnostic → Command Sprint (499) → Data Pack → Retainer
```

| Stage transition | Metric | Type |
|------------------|--------|------|
| Visitors → Score | Score start rate | Leading |
| Score → Diagnostic | Diagnostic booking rate | Leading |
| Diagnostic booked → held | Diagnostic show-rate | Leading |
| Diagnostic → Sprint | Sprint conversion rate | Lagging |
| Sprint → Proof Pack | Proof Pack production rate | Leading (of trust loop) |
| Sprint → Data Pack | Upsell rate | Lagging |
| Data Pack → Retainer | Retainer conversion | Lagging |

## سرعة الحلقة (Loop velocity)

How fast a loop completes one turn — compounding depends on velocity, not just conversion.

| Loop | Velocity metric |
|------|-----------------|
| Proof → Content | Days from Sprint delivered → published (approved) case study |
| Content → Inbound | Inbound Score starts attributed to content / week |
| Diagnostic → Sprint | Median days Diagnostic → Sprint start |
| Referral | Referred Diagnostics / delivered Proof Packs |

## رائد مقابل متأخر (Leading vs lagging)

- **Leading** (we can act on this week): Score starts, Diagnostic bookings, show-rate, draft queue
  throughput, Proof Packs approved.
- **Lagging** (confirm strategy worked): Sprint revenue, retainer count, MRR, referral→Sprint.

Act on leading; report on lagging.

## ما لا نقيس (Anti-vanity list)

- ❌ Raw page views / impressions as a success metric
- ❌ Follower / subscriber count in isolation
- ❌ "Emails queued" or "invites sent" (effort, not outcome)
- ❌ Any metric that can be inflated without creating revenue/proof/asset/next-offer

## لوحة بسيطة (Minimal dashboard layout)

```text
[ Spine ]   Visitors · Score · Diagnostic · Sprint · Pack · Retainer  (counts + conversion %)
[ Velocity] Proof→Content days · Diag→Sprint days · Inbound/wk · Referral rate
[ Health ]  Draft queue size · Proof Packs approved · Guardrail breaches (should be 0)
```

Guardrail-breach count (auto-sends attempted, unapproved publishes, fake-scarcity copy caught)
must read **0**. Any non-zero is a stop-the-line event.

## خطة 30 يوم (30-day plan)

1. Instrument the six spine transitions (Score → … → Retainer) with consistent event names.
2. Stand up the minimal dashboard (counts + conversion %) — Markdown/internal first.
3. Add the four loop-velocity metrics.
4. Add the guardrail-breach counter (target 0) and wire alerts to the founder.
5. Establish a weekly leading-metric review; report lagging monthly.
