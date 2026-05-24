# Market Domination Intelligence

> The intelligence layer that answers, daily and weekly, the questions a founder needs answered to dominate the Saudi B2B market.

## 1. Questions the system must answer

| Cadence | Question |
|---|---|
| Daily | Which accounts to engage today? |
| Daily | Which replies need a human now? |
| Daily | Which approvals are blocking cash? |
| Weekly | Which sector is winning? |
| Weekly | Which sector should we exit or de-prioritise? |
| Weekly | Which message / offer is converting? |
| Weekly | Which objection is most expensive? |
| Monthly | Which buyer title is the real economic buyer? |
| Monthly | Which competitor is appearing in the conversation? |
| Quarterly | Where is the next ICP edge? |

## 2. Component machines

| Machine | Output | File |
|---|---|---|
| Sector Ranking | Ranked sector table | `SECTOR_RANKING_SYSTEM.md` |
| ICP Segmentation | Segments + fit signals | `ICP_SEGMENTATION_SYSTEM.md` |
| Buyer Personas | Personas per segment | `BUYER_PERSONA_SYSTEM.md` |
| Competitive Intelligence | Competitor radar | `COMPETITIVE_INTELLIGENCE_SYSTEM.md` |
| Trigger Events | Daily trigger feed | `TRIGGER_EVENT_SYSTEM.md` |
| Account Scoring | Per-account composite | `ACCOUNT_SCORING_MODEL.md` |

## 3. Data sources

1. Public signal (registries, news, hiring boards, regulators).
2. First-party signal (Dealix delivery + finance + Trust events).
3. Customer-provided signal (CRM exports, intake forms).
4. Partner signal (co-sell and referral channels).

When public signal is unavailable, fallback datasets carry `source=fallback` and the verifier flags them.

## 4. Outputs into the runtime

| Output | Consumer |
|---|---|
| `growth/sector_targets.csv` | Distribution machines |
| `growth/account_scores.csv` | Distribution & Sales Cockpit |
| `growth/target_segments.csv` | Marketing OS |
| `growth/distribution_machines.csv` | Worker Orchestrator |

## 5. Operating cadence

- **Daily 05:00 KSA** — refresh trigger events and account scores.
- **Weekly Sunday 08:00 KSA** — sector ranking and segment rotation.
- **Monthly first Sunday** — buyer persona review.
- **Quarterly** — full ICP recompute.

## 6. Trust posture

The intelligence layer is **decision support** only. No engagement decision is made automatically; every action goes through `/approvals`.

## 7. Verifier

`scripts/verify_growth_system.py` enforces:

- Required documents exist.
- Required CSVs exist and have valid headers.
- No file carries unverified `guaranteed_*` claims.
