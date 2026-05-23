# Ultimate Revenue Factory

Revenue is the test that everything else works. The factory:

```
market → lead intelligence → scoring → outreach draft → approval →
send queue → follow-up → reply classification → sample draft →
proposal draft → approval → cash capture → delivery → retention →
proof (after founder approval) → referral → inbound demand →
productization candidate
```

## Where each step lives

| Step | Artifact |
|---|---|
| market | external (not in repo) |
| lead intelligence | `intelligence/lead_intelligence_base.csv` |
| scoring | column in same CSV |
| outreach draft | `outreach/outreach_queue.csv` |
| approval | `approvals/approval_queue.csv` + `trust/approval_decisions.csv` |
| send queue | `outreach/outreach_queue.csv` (status=queued) |
| follow-up | same CSV (status=followup) |
| reply classification | `outreach/conversation_log.csv` |
| sample / proposal draft | `sales/proposal_queue.csv` |
| cash capture | `finance/payment_capture_queue.csv` |
| cash received | `finance/cash_collected.csv` |
| delivery | `sales/proposal_queue.csv` (status=delivering) |
| retention | `trust/trust_flags.csv` (category=retention) |
| proof | gated by founder approval; not in repo until approved |
| productization | `product/productization_candidates.csv` |

## Honest rule

No step is "automatic" if it crosses the trust boundary. The factory is
fast on internal work and deliberately slow on external impact.
