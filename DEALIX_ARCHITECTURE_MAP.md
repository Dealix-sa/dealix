# DEALIX ARCHITECTURE MAP

> The 12 Super Systems and how they connect.
> One picture. Update only when the architecture itself changes.

## Top-Level Mental Model

```
              ┌─────────────────────────────────────┐
              │   1. Founder Command OS (CEO Brain) │
              │   Daily Brief · Weekly Review · Log │
              └────────────────┬────────────────────┘
                               │ decides
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
   ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
   │ 2. Strategy OS │ │ 7. Trust &     │ │ 12. Learning & │
   │    North Star  │ │    Governance  │ │    Intelligence│
   │    Focus rules │ │    (cross-cut) │ │    Feedback    │
   └────────┬───────┘ └────────┬───────┘ └────────┬───────┘
            │ guards            │ guards           │ improves
            ▼                   ▼                  ▼
   ┌──────────────────────────────────────────────────────┐
   │              Operating Layer (Day-to-Day)             │
   │                                                       │
   │  3. Revenue OS ◄── 4. Acquisition OS                  │
   │       │              (leads → outreach → replies)     │
   │       ▼                                               │
   │  5. Delivery OS ──► 9. Client Success OS ──► Retainer │
   │       │                                               │
   │       ▼                                               │
   │  6. Product OS (builds what Revenue + Delivery need)  │
   │       │                                               │
   │       ▼                                               │
   │  8. Finance & Billing OS (cash + invoices + MRR)      │
   │                                                       │
   │  10. Content & Authority OS (proof outbound)          │
   │  11. People & Delegation OS (when to hire)            │
   └──────────────────────────────────────────────────────┘
```

## Cross-Cutting Concerns

Three systems wrap **every** other system:

- **Founder Command OS (1)** decides direction and priorities
- **Trust & Governance OS (7)** approves risky actions and blocks unsafe ones
- **Learning OS (12)** measures, evaluates, and feeds improvements back

This matches NIST AI RMF (Govern/Map/Measure/Manage) and OpenAI's agent-platform guidance: governance and feedback are not separate buckets — they wrap everything.

## Repo Layout (mapping to systems)

| System | Public docs | Public code | Private repo path |
|---|---|---|---|
| 1. Founder Command OS | `docs/founder/` | — | `founder/` |
| 2. Strategy OS | `docs/strategy/` | — | `strategy/` |
| 3. Revenue OS | `docs/revenue/` | `dealix/revenue_ops_autopilot/` | `pipeline/`, `sales/` |
| 4. Acquisition OS | `docs/acquisition/` | `dealix/agents/` | `prompts/` |
| 5. Delivery OS | `docs/delivery/` | `dealix/execution/` | `delivery/`, `clients/` |
| 6. Product OS | `docs/product/` | `dealix/`, `api/` | — |
| 7. Trust & Governance OS | `docs/trust/` | `dealix/trust/` | `trust/` |
| 8. Finance & Billing OS | `docs/finance/` | `dealix/payments/` | `revenue/` |
| 9. Client Success OS | `docs/client_success/` | — | `clients/` |
| 10. Content & Authority OS | `docs/content/` | `dealix/marketing_factory/` | `content/` |
| 11. People & Delegation OS | `docs/people/` | — | `people/` |
| 12. Learning & Intelligence OS | `docs/learning/` | `dealix/analytics/` | `learning/`, `weekly_reviews/` |

## Data Flow: One Customer, End to End

1. **Acquisition OS** finds a lead → enriches → scores → drafts a message
2. **Trust OS** validates: ICP fit, suppression list clean, no overclaim → founder approves
3. **Revenue OS** logs the outreach in pipeline → tracks reply → books call
4. **Delivery OS** runs the sprint → produces a report → QA passes
5. **Trust OS** approves any external claims → founder signs off
6. **Client Success OS** delivers report → captures feedback → triggers retainer talk
7. **Finance OS** issues invoice → records payment → updates MRR
8. **Content OS** drafts case study → trust approves → founder publishes
9. **Learning OS** captures: which channel, which message, which sector won
10. **Founder OS** sees it all in tomorrow's Daily Brief

## What This Architecture Refuses To Do

- No agent acts externally without trust approval (Trust gate)
- No feature ships without revenue/delivery justification (Product gate)
- No public claim without evidence (Trust gate)
- No client data in the public repo (Public Safety gate, enforced in CI)
- No decision without a log entry (Decision Engine)

See `DEALIX_DECISION_RULES.md` for the rules that govern transitions.
