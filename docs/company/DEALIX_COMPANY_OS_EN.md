# Dealix — The Company as an Operating System

> **English mirror of `DEALIX_COMPANY_OS_AR.md`.**
> Arabic is the primary positioning language of Dealix; this English file exists for investors, international partners, and bilingual readers and is kept in sync with the Arabic original.
> Branch: `phase/startup-architecture-brand-os`. All outbound is draft-only by default (`OUTBOUND_MODE=draft_only`).

---

## 1. Vision

To make every Saudi company run on an intelligent operating system — not on scattered tools, not on an external agency, not on a dashboard that cannot execute.

Dealix does not sell a chatbot, a CRM, a dashboard, or an agency service. Dealix designs, ships, and operates compact, governed AI operating systems — one per commercial function — that plug into Saudi SMEs and mid-market companies and run that function end-to-end: discovery, decision, delivery, and proof.

The positioning is Saudi-native: a Saudi limited liability company (LLC), pricing in SAR, Asia/Riyadh timezone, PDPL compliance, ZATCA e-invoicing awareness. The primary language is Arabic, with English mirrors for investors and international partners.

Operating doctrine:

> AI explores, analyzes, and recommends. Deterministic workflows execute. Humans approve critical external commitments.
> No autonomous external sending. No fake clients, testimonials, or guaranteed ROI. Every forecast is a scenario with an explicit confidence level and assumptions.

---

## 2. Mission

Turn every commercial function inside a Saudi company from manual chaos into a measurable, provable intelligent operating system — in weeks, not years.

The mission is operational, not aspirational: take an existing function (revenue, delivery, follow-up, decisions), build a small system for it, run it, then prove the delta with documented before/after data.

---

## 3. Products (14 products)

Each product is a self-contained operating system: defined inputs, defined outputs, approval gates, and proof artifacts.

| # | Product | Function |
|---|---|---|
| 1 | Revenue Command Room OS | Daily revenue command: pipeline, outreach drafts, CEO brief, KPIs. |
| 2 | Company Brain OS | Central knowledge + memory layer: decisions, playbooks, client context. |
| 3 | WhatsApp / Inbox Follow-up OS | Drafted, approval-gated follow-ups. No live send by default. |
| 4 | Email Outreach Review OS | Drafted outbound email, review queue, approval before any send. |
| 5 | SMS Notification / Follow-up OS | Drafted SMS notifications and follow-ups; `SMS_SEND_ENABLED=false` by default. |
| 6 | AI Trust & Compliance OS | PDPL controls, approval classes, audit trails, no-overclaim register, evidence packs. |
| 7 | Client Delivery OS | Discovery → build → test → success report per client. |
| 8 | Controlled Live Outbound OS | Strictly gated live outbound; requires `EXTERNAL_SEND_ENABLED=true` + per-channel flags. Default off. |
| 9 | Founder Decision Desk | Daily decision queue, escalation matrix, delegation matrix. |
| 10 | Company Diagnosis Sprint | Paid 1-week diagnostic: pain mapping, data audit, baseline, recommendation. |
| 11 | Offer Intelligence OS | Offer ladder, pricing engine, sector-specific offer generation. |
| 12 | Market & Competitor Watch OS | Sector radar, competitor signals, market shifts, Saudi regulatory updates. |
| 13 | Proposal + Contract OS | Proposal and contract generation, ZATCA-aware invoicing, Moyasar payment links. |
| 14 | Executive Proof Pack OS | Baseline → after → documented delta proof packs for executives. |

All 14 products share the same trust engine, the same approval gates, and the same draft-only-by-default outbound posture.

---

## 4. Daily Operations

### Morning (30 min) — Command Room
1. `make company-day`
2. Review `reports/command_room/index.html`
3. Review drafts in `outbox/YYYY-MM-DD/`
4. Review the founder approval queue in Founder Decision Desk

### During the day
5. For each draft: approve / reject / rewrite / shorten / make formal / change offer / move to nurture / do not contact.
6. Manually send approved drafts only (requires `EXTERNAL_SEND_ENABLED` + channel flags on).
7. Update `ledgers/outreach_log.csv` after each send.
8. Log replies in `ledgers/reply_log.csv`.

### Evening (15 min)
9. Update `ledgers/deals_pipeline.csv`.
10. Review `reports/revenue/YYYY-MM-DD/daily_ceo_report.md`.
11. Record decisions into Company Brain OS.

### Golden rule
Nothing is sent externally without explicit human approval and the correct send flags enabled. The default state of the entire system is: generate drafts + human review.

---

## 5. Roles

### Today (founder stage)
- **Founder / CEO / Operator** — runs the daily commercial loop, approvals, delivery, founder decisions.
- **AI / Platform (founder-led engineering)** — LLM gateway, agents, product OSes, delivery builds.

### Planned roles (trigger-based hiring, not forecast-based)
| Role | Trigger | Confidence |
|---|---|---|
| Delivery lead | 2 concurrent paid pilots | High |
| Sales / founder associate | 1 recurring subscription after pilot | Medium |
| Engineer #2 | 3 concurrent client builds | Medium |
| Compliance / ops lead | First enterprise pilot or regulator engagement | Medium |
| Customer success | 5 active subscriptions | Medium |

Hiring is conservative and trigger-based. No hires on forecast alone; the trigger must actually fire.

---

## 6. Decision Making

### Decision rule
Every external decision (send, offer, contract, payment, client commitment) requires human approval. AI only recommends.

### Approval matrix
| Decision type | Approver | Condition |
|---|---|---|
| Send outreach draft | Founder | Explicit approval + channel flags on |
| Price offer to client | Founder | Via Offer Intelligence OS + Proposal + Contract OS |
| Client contract | Founder | Legal review + signature |
| Enable live payment (Moyasar) | Founder | `MOYASAR_LIVE_MODE=true` + review |
| Enable live outbound | Founder | `EXTERNAL_SEND_ENABLED=true` + channel flags + opt-in + legal review |
| External results claim | Founder | Real proof pack: baseline → after → documented delta |
| Hire | Founder | Trigger actually fired |

### No-overclaim register
Strictly forbidden:
- Guaranteed ROI
- Specific percentages as guarantees
- Fake clients or testimonials
- Autonomous external sends without approval

Every external forecast must carry: confidence level + explicit assumptions + description as a scenario, not a guarantee.

---

## 7. Metrics

### North Star
- Monthly recurring revenue (SAR) from active subscriptions.

### Daily KPIs
- Prospects researched
- Outreach drafts generated (not sent)
- Drafts approved
- Drafts manually sent (only if flags on)
- Replies received
- Pipeline updates

### Weekly KPIs
- Diagnostics booked
- Pilots started
- Pilots completed
- Subscriptions signed
- Proof packs delivered

### Monthly KPIs
- MRR (SAR)
- Active subscriptions count
- Net new diagnostics
- Pilot → subscription conversion rate
- Churn
- Gross margin
- Runway (months)

### Trust KPIs (always tracked)
- Approval gates bypassed (target: 0)
- Send flags in correct state per environment
- PDPL controls active
- No-overclaim register violations (target: 0)
- Audit trail completeness (target: 100%)

---

## 8. Revenue Model (summary)

| Stage | Price | Output |
|---|---|---|
| Diagnosis | SAR 4,999 | Diagnostic report + recommended OS bundle |
| Pilot (1 month) | SAR 14,999 | Built OS + proof pack |
| Monthly subscription | Scenario (see table) | Ongoing OS operation |

Monthly subscription scenarios (planning scenarios, not price commitments):

| Scenario | Monthly subscription (SAR) | Confidence | Assumptions |
|---|---|---|---|
| Conservative | 7,500 – 12,000 | Medium-high | Single OS, one function, light ops. |
| Base | 12,000 – 25,000 | Medium | 2–3 OSes bundled, moderate delivery load. |
| Stretch | 25,000 – 60,000 | Low-medium | Multi-OS bundle + controlled live outbound + proof packs. |

Actual pricing is set per client via Offer Intelligence OS and confirmed in Proposal + Contract OS.

---

## 9. Client Lifecycle

```
Prospecting → Diagnosis → Pilot → Subscription → Expansion → Renewal
```

- **Prospecting:** Saudi B2B opportunities, ICP scoring, PDPL-aware enrichment.
- **Diagnosis:** 1-week paid diagnostic, pain mapping, data audit, baseline.
- **Pilot:** 4 weeks — discovery → build → test → success report.
- **Subscription:** Monthly operation of the OS after pilot success.
- **Expansion:** Add 2–3 bundled OSes using the same trust engine.
- **Renewal:** Executive Proof Pack is the renewal artifact.

---

## 10. Deployment & Compliance

- **PDPL-native:** data subject requests, breach response, retention policy, cross-border transfer addendum.
- **ZATCA-aware:** e-invoicing readiness, Moyasar sandbox by default.
- **Approval-first:** no autonomous external commitments. Humans approve.
- **Send flags:** all off by default. No external send without explicit per-environment enablement.

Outbound send flags (default state for every environment):
- `EXTERNAL_SEND_ENABLED=false`
- `EMAIL_SEND_ENABLED=false`
- `WHATSAPP_SEND_ENABLED=false`
- `WHATSAPP_ALLOW_LIVE_SEND=false`
- `SMS_SEND_ENABLED=false`
- `OUTBOUND_MODE=draft_only`

---

## 11. Related Documents

- `DEALIX_STARTUP_ARCHITECTURE.md` — full system architecture
- `DEALIX_COMPANY_OS_AR.md` — Arabic original of this file
- `FOUNDER_OPERATING_SYSTEM_AR.md` — founder operating system (Arabic)
- `STARTUP_OPERATING_MODEL.md` — operating model detail
- `SAUDI_B2B_MARKET_STRATEGY.md` — Saudi B2B market strategy
- `DAILY_OPERATING_RHYTHM.md` — daily / weekly / monthly rhythm