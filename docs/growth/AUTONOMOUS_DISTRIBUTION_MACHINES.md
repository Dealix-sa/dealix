# Autonomous Distribution Machines

This document is the overview of every autonomous draft machine in Dealix
distribution and the trust gate diagram that binds them. "Autonomous" here
means autonomous in drafting only — every machine terminates at an approval
queue. No machine sends.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Machine catalogue

| Machine | Doc | Owner Agent | Approval Class | Worker (script) | Output |
|---|---|---|---|---|---|
| Outbound Draft | `OUTBOUND_DRAFT_MACHINE.md` | distribution_operator | A2 | `scripts/dealix_outbound_draft.py` | `outreach/outreach_queue.csv` |
| LinkedIn Queue | `LINKEDIN_QUEUE_MACHINE.md` | distribution_operator | A2 | `scripts/dealix_linkedin_queue.py` | `outreach/linkedin_queue.csv` |
| Email Draft | `EMAIL_DRAFT_MACHINE.md` | distribution_operator | A2 | `scripts/dealix_email_draft.py` | `outreach/email_queue.csv` |
| Contact Form | `CONTACT_FORM_QUEUE_MACHINE.md` | distribution_operator | A2 | `scripts/dealix_contact_form_queue.py` | `outreach/contact_form_queue.csv` |
| Follow-up | `FOLLOW_UP_MACHINE.md` | distribution_operator | A2 | `scripts/dealix_followup_queue.py` | `outreach/followup_queue.csv` |
| Reply Router | `REPLY_ROUTER_MACHINE.md` | distribution_operator | A1 | `scripts/dealix_reply_router.py` | `outreach/reply_routing.csv` |
| Nurture | `NURTURE_MACHINE.md` | content_strategist | A2 | `scripts/dealix_nurture_queue.py` | `marketing/nurture_queue.csv` |
| Partner Referral | `PARTNER_REFERRAL_MACHINE.md` | partner_revenue_agent | A2 | `scripts/dealix_partner_referral.py` | `customer_success/referral_queue.csv` |
| ABM Strategic | `ABM_STRATEGIC_ACCOUNT_MACHINE.md` | growth_strategist | A2 | `scripts/dealix_abm_queue.py` | `growth/abm_queue.csv` |
| Proof-to-Demand | `PROOF_TO_DEMAND_MACHINE.md` | proof_safety_agent | A2 | `scripts/dealix_proof_to_demand.py` | `outreach/proof_demand_queue.csv` |
| Content-to-Demand | `CONTENT_TO_DEMAND_ENGINE.md` | content_strategist | A2 | `scripts/dealix_content_to_demand.py` | `marketing/content_demand_queue.csv` |
| Channel Portfolio | `CHANNEL_PORTFOLIO_SYSTEM.md` | performance_analyst | A1 | `scripts/dealix_channel_portfolio.py` | `distribution/channel_scorecard.csv` |
| Community | `COMMUNITY_ECOSYSTEM_ENGINE.md` | content_strategist | A2 | `scripts/dealix_community_engine.py` | `marketing/community_queue.csv` |
| Events | `EVENTS_AND_PARTNERSHIP_ENGINE.md` | partner_revenue_agent | A2 | `scripts/dealix_events_engine.py` | `marketing/events_queue.csv` |

All worker scripts terminate at a queue file in the private ops runtime;
none invoke a third-party send API.

## 2. Trust gate diagram (text)

```
+-------------------+
|  Intelligence     |
|  Layer (scores)   |
+---------+---------+
          |
          v
+-------------------+     +------------------------+
|  Machine Drafter  | --> | Brand Voice Check      |
| (A1 produces      |     | (Brand Guardian)       |
|  candidate copy)  |     +-----------+------------+
+-------------------+                 |
                                      v
                          +-----------+------------+
                          | Suppression + Consent  |
                          | Check (Trust Guardian) |
                          +-----------+------------+
                                      |
                                      v
                          +-----------+------------+
                          | Guaranteed-Claim Scan  |
                          | (Brand Guardian)       |
                          +-----------+------------+
                                      |
                                      v
                          +-----------+------------+
                          | Channel Fit Check      |
                          | (Offer-Channel Fit)    |
                          +-----------+------------+
                                      |
                                      v
                          +-----------+------------+
                          | Approval Queue (A2)    |
                          | (Founder Console)      |
                          +-----------+------------+
                                      |
                            Approve   |   Reject
                              |       |     |
                              v       |     v
                       Operator Send  |  Rewrite Loop
                       (manual)       |  back to Drafter
                                      |
                                      v
                          +-----------+------------+
                          | Audit Ledger Entry     |
                          | (Trust Guardian)       |
                          +------------------------+
```

Every machine adds and removes nothing from this diagram. Variants are
captured per machine in their respective documents.

## 3. Cross-cutting controls

- A3 banned (policy rule `no_a3_auto`).
- Suppression list enforced (policy rule `no_suppressed_outreach`).
- Guaranteed-claim scan (policy rule `no_guaranteed_revenue_claims`).
- A2 needs approval to execute (policy rule
  `approved_a2_can_request_execution`).
- All decisions auditable.

## 4. Source documents

- `policies/dealix_control_policy.yaml` for the policy rules.
- `registries/agent_registry.yaml` for agent ownership.
- `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md` for channel intensity
  caps.
- `docs/growth/CHANNEL_PORTFOLIO_SYSTEM.md` for portfolio rebalancing.

## 5. Cadence

| Cadence | Activity |
|---|---|
| Daily | Drafts produced; queues reviewed |
| Weekly | Brand voice + reply quality audit |
| Monthly | Cross-machine performance review |
| Quarterly | Portfolio retune (channel weights) |

## 6. Approval class summary

- A1 machines: Reply Router, Channel Portfolio (observation/routing).
- A2 machines: all others (drafting + assist with approval before any
  external action).
- A3 machines: none. Banned at policy level.

## 7. KPIs

- System-wide draft approval rate.
- Time from intelligence to draft.
- Time from draft to approval.
- Reply quality (per-machine and aggregated).
- Brand voice first-pass rate.
- Suppression bleed (target: 0).
- A3 attempts (target: 0).

## 8. Failure modes and recovery

| Failure | Recovery |
|---|---|
| Drafts bypass trust gate | Worker halted; pipeline re-run |
| Brand voice regressions | Brand Guardian retrains; drafts paused |
| Queue backlog | Cap lowered; backlog drained with founder triage |
| A3-shaped behaviour | Trust Guardian halts; incident opened |
| Data residency breach | Security Guardian halts; PDPL review |

## 9. Non-negotiables

- No machine sends anything.
- No machine bypasses the trust gate.
- No machine carries A3 behaviour.
- Every machine has a documented owner, worker, KPI, and recovery path.

## 10. Where each machine lives

Drafts live in `outreach/` and `marketing/`. Scorecards live in
`distribution/`. Partner queues live in `customer_success/`. Strategic
queues live in `growth/`. None of these paths can be written by agents
outside their declared `allowed_write_targets` in
`registries/agent_registry.yaml`.

The point of the autonomous distribution layer is not to replace
operators. It is to make sure operators spend their time approving
high-quality drafts of high-quality outreach to high-quality accounts.
