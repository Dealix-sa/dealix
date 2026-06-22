# Dealix — Startup Operating Model

> **How the startup actually operates: legal, pricing, delivery, lifecycle, revenue, cost, runway, hiring.**
> Branch: `phase/startup-architecture-brand-os`
> All outbound is draft-only by default. No fake clients, testimonials, or guaranteed ROI. All forecasts are scenarios with confidence + assumptions.

---

## 1. Legal Entity

- **Entity type:** Saudi limited liability company (LLC).
- **Jurisdiction:** Kingdom of Saudi Arabia.
- **Currency:** Saudi Riyal (SAR).
- **Timezone:** Asia/Riyadh.
- **Compliance posture:**
  - PDPL-native (data subject requests, breach response, retention, cross-border transfer addendum)
  - ZATCA-aware e-invoicing
  - Moyasar payment gateway (sandbox by default; `MOYASAR_LIVE_MODE=false` until cutover approved)
- **Brand language:** Arabic-first; English mirrors for investors and international partners.

---

## 2. Pricing Model

Dealix sells in three stages. Pricing is in SAR and set per client via Offer Intelligence OS + Proposal + Contract OS.

| Stage | Price (SAR) | Duration | What the client gets |
|---|---|---|---|
| Company Diagnosis Sprint | 4,999 | 1 week | Pain mapping, data audit, baseline, recommended OS bundle. |
| Pilot | 14,999 | 1 month (4 weeks) | One product OS built + deployed + Executive Proof Pack. |
| Monthly subscription | Scenario (see below) | Ongoing | Operation of 1–N product OSes post-pilot. |

### Monthly subscription scenarios (planning scenarios, not price commitments)

| Scenario | Monthly (SAR) | Confidence | Assumptions |
|---|---|---|---|
| Conservative | 7,500 – 12,000 | Medium-high | Single OS, one function, light ongoing ops. One client team contact. |
| Base | 12,000 – 25,000 | Medium | 2–3 OSes bundled, moderate delivery load, bi-weekly proof updates. |
| Stretch | 25,000 – 60,000 | Low-medium | Multi-OS bundle + controlled live outbound + executive proof packs + SLA. |

These scenarios assume a Saudi SME or mid-market client with 10–200 employees. Enterprise pricing (larger scope, SLA, regulator engagement) is a separate track via Proposal + Contract OS.

### Pricing rules
- No guaranteed ROI in any proposal.
- No fixed-percentage claims.
- Every proposal includes a baseline → after → documented delta plan.
- Diagnosis and Pilot are fixed-price. Subscription is scenario-based and confirmed per client.

---

## 3. Delivery Model

### Diagnosis Sprint (1 week)
| Day | Activity | Output |
|---|---|---|
| 1 | Discovery interview + pain mapping | Pain map |
| 2 | Data audit (what exists, what's missing, PDPL scope) | Data audit report |
| 3 | Baseline measurement | Baseline metrics |
| 4 | OS bundle recommendation | Recommended OS scope |
| 5 | Diagnostic report + pilot proposal | Report + Proposal |

### Pilot (4 weeks)
| Week | Phase | Output |
|---|---|---|
| 1 | Discovery + data wiring | Scoped build plan |
| 2 | Build the small system | Deployed OS (draft mode) |
| 3 | Test + adjust | Validated OS |
| 4 | Success report + Executive Proof Pack | Baseline → after → delta |

### Subscription (ongoing)
- Monthly operation of the OS(es).
- Bi-weekly or monthly proof pack updates.
- Expansion: add 2–3 OSes using the same trust engine.
- Renewal: Executive Proof Pack is the renewal artifact.

### Delivery capacity
- Current capacity: founder-led, 1–2 concurrent pilots.
- Trigger to add delivery lead: 2 concurrent paid pilots (confidence: high).

---

## 4. Client Lifecycle

```
Prospecting → Diagnosis → Pilot → Subscription → Expansion → Renewal
   ↑                                                              │
   └──────────── (re-engage on churn / pause) ←────────────────────┘
```

| Stage | Entry | Exit criteria | Tool |
|---|---|---|---|
| Prospecting | ICP match + PDPL-aware enrichment | Qualified lead in `ledgers/prospects.csv` | Revenue Command Room OS |
| Diagnosis | Lead accepts SAR 4,999 sprint | Diagnostic report + pilot proposal | Company Diagnosis Sprint |
| Pilot | Client signs pilot proposal | Executive Proof Pack delivered | Client Delivery OS |
| Subscription | Pilot success + client signs subscription | Active subscription | Proposal + Contract OS |
| Expansion | Client wants 2nd/3rd OS | Additional OS deployed | Offer Intelligence OS |
| Renewal | Monthly renewal review | Renewed or churned | Executive Proof Pack OS |

---

## 5. Revenue Streams

| Stream | Type | When it starts | Scenario confidence |
|---|---|---|---|
| Diagnosis sprint | One-time | First client engagement | High (productized, fixed price) |
| Pilot | One-time | After diagnosis | Medium-high (productized, fixed price) |
| Monthly subscription | Recurring | After pilot success | Medium (scenario-based) |
| Expansion (additional OSes) | Recurring uplift | After first subscription stabilizes | Low-medium |
| Controlled live outbound (add-on) | Recurring add-on | Only after opt-in + legal + flags | Low (gated, not default) |

### Revenue scenario forecast (first 12 months, planning only)

| Scenario | Diagnostics in 12mo | Pilots | Subscriptions by month 12 | 12mo revenue (SAR) | Confidence | Assumptions |
|---|---|---|---|---|---|---|
| Conservative | 8 | 4 | 2 | 110,000 – 160,000 | Medium | Manual outreach, draft-only, 50% pilot→sub conversion, conservative subscription. |
| Base | 16 | 8 | 5 | 280,000 – 420,000 | Low-medium | Manual + controlled outreach after month 4, 60% pilot→sub, base subscription. |
| Stretch | 30 | 15 | 9 | 600,000 – 900,000 | Low | Controlled live outbound enabled by month 5, 60% pilot→sub, stretch subscription. |

Assumptions common to all scenarios:
- No paid acquisition in months 1–3.
- All outbound is draft-only until controlled live outbound is explicitly enabled.
- No fake clients. Conversion rates are planning assumptions, not commitments.
- One founder-led operator. Hiring only when triggers fire.

---

## 6. Cost Structure

| Cost category | Description | Notes |
|---|---|---|
| LLM API spend | Anthropic, Gemini, Groq, DeepSeek, GLM | Tracked per provider; cost governance in place. |
| Infrastructure | Railway / Docker hosting, Postgres, Redis | Scales with clients. |
| WhatsApp Business API | Meta WhatsApp Cloud API | Only when live send enabled. |
| Moyasar fees | Payment processing (sandbox free; live fees apply) | Only after `MOYASAR_LIVE_MODE=true`. |
| Google Places API | Lead research | Per-call cost. |
| Founder time | Opportunity cost | Not a cash cost but the binding constraint. |
| Compliance / legal | PDPL review, contract templates, opt-in review | Triggered by first live send / enterprise pilot. |
| Hiring | Trigger-based | Only when triggers fire. |

### Cost control principles
- Sandbox first: Moyasar sandbox, WhatsApp draft-only, no live sends until approved.
- Per-provider LLM cost tracking.
- No paid acquisition until organic motion is validated.
- Hiring is the largest discretionary cost and is trigger-gated.

---

## 7. Unit Economics

### Per-pilot unit economics (planning estimate, not a guarantee)

| Item | Value (SAR) | Confidence | Notes |
|---|---|---|---|
| Pilot price | 14,999 | High | Fixed price. |
| LLM + infra cost per pilot | 500 – 1,500 | Medium | Depends on OS scope and LLM usage. |
| Founder time per pilot | ~40 hours | Medium | Opportunity cost, not cash. |
| Gross margin per pilot | ~85% – 90% | Medium | High margin because delivery is AI-augmented. |

### Per-subscription unit economics (planning estimate)

| Item | Value (SAR/month) | Confidence | Notes |
|---|---|---|---|
| Subscription (base scenario) | 12,000 – 25,000 | Medium | Scenario-based. |
| LLM + infra cost per account | 300 – 1,200 | Medium | Scales with OS count and usage. |
| Gross margin | ~80% – 90% | Medium | |
| CAC | Near-zero cash + high founder time | Medium | Organic + draft-only outreach. |
| Payback period | 1 – 3 months | Medium | Because pilot revenue covers initial build. |

These are planning estimates with assumptions, not commitments. Actual unit economics are measured per client and recorded in the operating ledger.

---

## 8. Runway

Runway depends on founder capital and monthly burn. Because Dealix is AI-augmented and founder-led, the primary constraint is founder time, not cash.

### Burn scenarios (planning only)

| Scenario | Monthly cash burn (SAR) | Confidence | Assumptions |
|---|---|---|---|
| Lean | 1,500 – 4,000 | High | LLM APIs + infra only, no hires, no paid acquisition. |
| Moderate | 8,000 – 20,000 | Medium | + 1 hire (delivery lead or engineer) after triggers fire. |
| Growth | 25,000 – 60,000 | Low | + 2–3 hires + paid acquisition + compliance/legal. |

### Runway implication
- With lean burn and founder capital, runway is long (many months) — the binding constraint is founder capacity, not cash.
- With moderate burn, runway depends on revenue: if 2–3 subscriptions are active by month 6, the business can approach contribution-margin breakeven.
- With growth burn, runway shortens and requires either revenue acceleration or capital.

No capital raise is assumed in these scenarios. If capital is raised, it changes the growth scenario, not the lean/base scenarios.

---

## 9. Hiring Plan

Hiring is trigger-based. No hire is made on forecast alone.

| Role | Trigger | Confidence | What they own |
|---|---|---|---|
| Delivery lead | 2 concurrent paid pilots | High | Client Delivery OS execution, pilot quality. |
| Sales / founder associate | 1 recurring subscription after pilot | Medium | Outreach drafting support, pipeline hygiene, reply triage. |
| Engineer #2 | 3 concurrent client builds | Medium | Agent runtime, LLM gateway, OS builds. |
| Compliance / ops lead | First enterprise pilot or regulator engagement | Medium | PDPL, ZATCA, contracts, audit trails. |
| Customer success | 5 active subscriptions | Medium | Renewals, expansion, proof pack cadence. |

### Hiring sequence (most likely order)
1. Delivery lead (trigger: 2 concurrent pilots)
2. Sales / founder associate (trigger: 1 subscription)
3. Engineer #2 (trigger: 3 concurrent builds)
4. Compliance / ops lead (trigger: enterprise or regulator)
5. Customer success (trigger: 5 subscriptions)

Actual order depends on which triggers fire first.

---

## 10. Outbound & Safety Posture

All outbound is draft-only by default. Send flags (default state for every environment):

- `EXTERNAL_SEND_ENABLED=false`
- `EMAIL_SEND_ENABLED=false`
- `WHATSAPP_SEND_ENABLED=false`
- `WHATSAPP_ALLOW_LIVE_SEND=false`
- `SMS_SEND_ENABLED=false`
- `OUTBOUND_MODE=draft_only`

Controlled Live Outbound OS is enabled only when:
1. Opt-in is complete for the target.
2. Legal review of outreach content is done.
3. `EXTERNAL_SEND_ENABLED=true` + the relevant channel flag is set for a specific environment.
4. Founder has signed off on the cutover.

No autonomous external sends. No cold WhatsApp without opt-in. No guaranteed ROI. No fake clients.

---

## 11. Related Documents

- `DEALIX_STARTUP_ARCHITECTURE.md` — full system architecture
- `DEALIX_COMPANY_OS_AR.md` / `DEALIX_COMPANY_OS_EN.md` — company as an OS
- `FOUNDER_OPERATING_SYSTEM_AR.md` — founder operating system
- `SAUDI_B2B_MARKET_STRATEGY.md` — Saudi B2B market strategy
- `DAILY_OPERATING_RHYTHM.md` — daily / weekly / monthly rhythm
- `docs/ops/CONTROLLED_LIVE_OUTBOUND.md` — controlled live outbound gates
- `docs/company/PRICING.md` — pricing detail
- `docs/company/UNIT_ECONOMICS.md` — unit economics detail