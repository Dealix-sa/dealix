# Ultimate Revenue Factory

The revenue factory is the funnel that moves a lead from intelligence to
collected cash, with a founder approval at every external move.

## Stages

1. **Lead intelligence** — research builds `lead_intelligence_base.csv`.
2. **Scoring** — lead scoring agent attaches A/B/C grades.
3. **Outreach draft (A2)** — outreach draft agent queues drafts.
4. **Founder approval** — Approvals page records the decision.
5. **External send (manual until Stage 5)** — humans send.
6. **Reply intake** — `conversation_log.csv` accumulates inbound.
7. **Reply classification** — positive/neutral/negative/OOO.
8. **Sample draft (A2)** — sample draft agent prepares deliverables.
9. **Proposal draft (A2)** — bilingual proposal without price commit.
10. **Payment capture (A2)** — polite follow-ups.
11. **Cash collected** — finance updates `cash_collected.csv`.
12. **Retention + proof** — manual, gated.

## Bottleneck signals

- Pending approval > 5 ⇒ founder review backlog.
- Sent > 0 and positive replies == 0 ⇒ messaging or targeting.
- Payment capture queue non-empty ⇒ payment capture is the blocker.
