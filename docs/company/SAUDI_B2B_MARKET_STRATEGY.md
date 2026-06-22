# Dealix — Saudi B2B Market Strategy

> **Saudi B2B market analysis, ICP, market size, go-to-market, competitive landscape, positioning.**
> Branch: `phase/startup-architecture-brand-os`
> No fake clients, testimonials, or guaranteed ROI. All market sizes are estimates with explicit assumptions and confidence levels. All outbound is draft-only by default.

---

## 1. Market Context

Saudi Arabia is undergoing an accelerated digitization push under Vision 2030. The SME and mid-market segment is large, underserved by software that fits Saudi operating reality (PDPL, ZATCA, Arabic-first, Asia/Riyadh, SAR pricing), and increasingly open to AI-augmented operations.

Dealix is positioned as a Saudi B2B AI Operating Systems company — not a chatbot, CRM, agency, or dashboard. The wedge is diagnosis-led: a paid Company Diagnosis Sprint (SAR 4,999) that converts to a Pilot (SAR 14,999) and then to a monthly subscription.

---

## 2. Target Sectors

Eight target sectors, chosen for operational pain that Dealix's product OSes can address, Saudi market depth, and B2B buying motion.

| # | Sector | Why it fits Dealix | Primary OS wedge |
|---|---|---|---|
| 1 | Clinics (private clinics, small medical groups) | Follow-up gaps, patient no-shows, revenue leakage, Arabic-first communication. | WhatsApp/Inbox Follow-up OS + Revenue Command Room OS |
| 2 | Real estate (brokerages, developers, property managers) | Lead leakage, slow follow-up, pipeline opacity. | Revenue Command Room OS + Email Outreach Review OS |
| 3 | Training (training centers, corporate training providers) | Enrollment funnel, follow-up, proposal generation. | Proposal + Contract OS + SMS Notification OS |
| 4 | Logistics (freight forwarders, last-mile, warehousing) | Operational coordination, notification gaps, client updates. | SMS Notification OS + Client Delivery OS |
| 5 | B2B services (consultancies, professional services) | Lead generation, proposal fatigue, executive reporting. | Revenue Command Room OS + Founder Decision Desk |
| 6 | Marketing agencies | Client delivery, proof packs, outbound for their own clients. | Client Delivery OS + Executive Proof Pack OS |
| 7 | Car dealers (independent dealers, used-car platforms) | Lead follow-up, inventory-led outreach, pipeline. | WhatsApp/Inbox Follow-up OS + Revenue Command Room OS |
| 8 | Legal / accounting firms | Client intake, document-heavy proposals, compliance. | Proposal + Contract OS + AI Trust & Compliance OS |

### Sector prioritization (planning, not commitment)

| Priority | Sector | Confidence | Rationale |
|---|---|---|---|
| Tier 1 | Clinics, Real estate, B2B services | Medium-high | Clear pain, faster sales cycle, Arabic-first communication critical. |
| Tier 2 | Training, Marketing agencies, Car dealers | Medium | Good pain fit, slightly longer or more fragmented cycles. |
| Tier 3 | Logistics, Legal/accounting | Medium | Strong pain but slower buying motion and compliance overhead. |

Prioritization is reviewed monthly via Market & Competitor Watch OS and adjusted based on actual pipeline signals.

---

## 3. Ideal Customer Profile (ICP)

### Firmographic ICP
- **Geography:** Kingdom of Saudi Arabia (primary). GCC adjacent (secondary, later).
- **Size:** 10–200 employees (SME to mid-market).
- **Revenue:** Revenue-generating, not pre-revenue.
- **Buying authority:** Founder/owner, GM, or head of function (revenue, operations, delivery) can sign.
- **Language:** Arabic is the operating language; English is secondary.
- **Systems:** Uses WhatsApp + email + phone heavily; may have a CRM but underuses it; spreadsheets are common.

### Behavioral ICP
- Feels pain from lead leakage, slow follow-up, or opaque pipeline.
- Has tried a tool/agency before and been disappointed by lack of fit or lack of proof.
- Is willing to pay for a diagnostic if the pain is real.
- Wants proof (before/after delta), not promises.
- Cares about Saudi compliance (PDPL, ZATCA, Arabic).

### Anti-ICP (not a fit now)
- Pre-revenue startups with no operational pain to diagnose.
- Enterprises > 200 employees with multi-year procurement cycles (handled later via enterprise track).
- Companies that want a guaranteed ROI percentage (Dealix does not offer this).
- Companies that want autonomous cold spam (Dealix does not do this).

---

## 4. Market Size Estimates

All estimates carry explicit assumptions and confidence levels. These are planning inputs, not commitments.

### Saudi SME count (assumption base)
- Assumption: Saudi SMEs numbered roughly 1.0–1.3 million registered establishments (Vision 2030 / Monsha'at reporting era). Confidence: medium. This is a broad base, not the addressable market.
- Dealix does not target all SMEs. It targets SMEs with 10–200 employees in 8 sectors with revenue and operational pain.

### Serviceable addressable market (SAM) — planning estimate

| Sector | Estimated SMEs in sector with 10–200 employees (KSA) | Confidence | Assumptions |
|---|---|---|---|
| Clinics | 8,000 – 15,000 | Low-medium | Private clinics + small medical groups; MoH-licensed; estimate from sector reports, not verified census. |
| Real estate | 10,000 – 20,000 | Low-medium | Brokerages, small developers, property managers; active licensees. |
| Training | 3,000 – 8,000 | Low | Licensed training centers + corporate training providers. |
| Logistics | 5,000 – 12,000 | Low-medium | Freight forwarders, last-mile, warehousing SMEs. |
| B2B services | 15,000 – 30,000 | Low | Consultancies, professional services (broad, hard to bound). |
| Marketing agencies | 2,000 – 6,000 | Low | Active agencies serving Saudi clients. |
| Car dealers | 2,000 – 5,000 | Low | Independent dealers + used-car platforms. |
| Legal / accounting | 4,000 – 10,000 | Low | Law firms + accounting/tax firms. |
| **Total SAM (8 sectors)** | **~49,000 – 106,000** | **Low** | Sum of sector ranges; overlaps and boundary effects mean this is a rough planning band, not a precise count. |

### Serviceable obtainable market (SOM) — 12-month planning

| Scenario | Target accounts reached (12mo) | Diagnostics booked | Confidence | Assumptions |
|---|---|---|---|---|
| Conservative | 400 | 8 | Medium | Manual draft-only outreach, ~2% diagnostic conversion. |
| Base | 1,000 | 16 | Low-medium | Manual + controlled outreach after month 4, ~1.6% diagnostic conversion. |
| Stretch | 2,500 | 30 | Low | Controlled live outbound enabled by month 5, ~1.2% diagnostic conversion at higher volume. |

These are planning scenarios. Actual reach and conversion are tracked in `ledgers/outreach_log.csv` and `ledgers/deals_pipeline.csv` and used to refine the model.

---

## 5. Go-to-Market Approach

### Phase 1 — Diagnosis-led land (current, months 1–3)
- All outreach is draft-only and human-approved.
- Target Tier 1 sectors (clinics, real estate, B2B services).
- Motion: research → draft → founder approval → manual send → reply → diagnosis booking.
- No paid acquisition.
- Tooling: Revenue Command Room OS + Email Outreach Review OS + WhatsApp/Inbox Follow-up OS (draft mode).

### Phase 2 — Controlled outreach + pilot conversion (months 4–6)
- Enable Controlled Live Outbound OS only after opt-in + legal review + flag enablement.
- Expand to Tier 2 sectors.
- Convert diagnostics → pilots → subscriptions.
- Begin sector-specific offer ladders via Offer Intelligence OS.

### Phase 3 — Bundle expansion + proof-led renewals (months 6–12)
- For subscribed clients, expand to 2–3 OSes.
- Executive Proof Pack OS drives renewals.
- Market & Competitor Watch OS feeds sector prioritization.

### Phase 4 — Vertical depth + partnerships (months 12+)
- Deepen 2–3 verticals (e.g., clinics, real estate).
- Agency partner program for delivery capacity.
- Enterprise track for > 200-employee clients.

### Channels
| Channel | Mode | Default state |
|---|---|---|
| Email | Drafted, approval-gated | `EMAIL_SEND_ENABLED=false` |
| WhatsApp | Drafted, approval-gated, opt-in required | `WHATSAPP_SEND_ENABLED=false`, `WHATSAPP_ALLOW_LIVE_SEND=false` |
| SMS | Drafted, approval-gated | `SMS_SEND_ENABLED=false` |
| In-person / referrals | Manual | Always allowed (not automated) |
| Content (AR-first) | Organic | Always allowed |
| Paid acquisition | Not in months 1–3 | Off |

No cold WhatsApp without opt-in. No autonomous sends. Every channel is draft-only until its flag is explicitly enabled for a specific environment.

---

## 6. Competitive Landscape

Dealix does not claim competitors are bad; it claims a different category.

| Category | Examples (generic) | What they do | Why Dealix differs |
|---|---|---|---|
| CRMs | Generic CRM tools | Store contacts, pipeline. | Dealix runs the function, not just stores it. Diagnosis-led, proof-led, Arabic-first, PDPL-native. |
| Chatbot tools | Generic bot builders | Scripted chat. | Dealix is an operating system, not a bot. Approval-first, no autonomous external sends. |
| Agencies | Marketing/sales agencies | Manual outreach/ops. | Dealix is productized, measurable, and proof-led; agencies are labor-based and often opaque. |
| Dashboards / BI | Generic analytics | Report on data. | Dealix executes, not just reports. Baseline → after → documented delta. |
| Automation tools | Generic automation | Trigger/action flows. | Dealix is AI-augmented, Arabic-first, Saudi-compliant, with trust engine and no-overclaim register. |

### Positioning statement (AR-first)

> ديالكس شركة سعودية لأنظمة تشغيل الأعمال بالذكاء الاصطناعي. لا تبيع أداة، بل تُشغّل وظيفة كاملة — من الاكتشاف إلى القرار إلى التسليم إلى الإثبات — بضوابط سعودية (PDPL، زاتكا، عربي أولاً، ريال سعودي).

English mirror:

> Dealix is a Saudi B2B AI Operating Systems company. It does not sell a tool — it operates a full function, from discovery to decision to delivery to proof, with Saudi-native controls (PDPL, ZATCA, Arabic-first, SAR).

---

## 7. Positioning Pillars

1. **Operating system, not a tool.** Dealix runs the function end-to-end.
2. **Diagnosis-led.** Paid diagnostic before any commitment.
3. **Proof-led.** Baseline → after → documented delta. No guaranteed ROI.
4. **Saudi-native.** PDPL, ZATCA, Arabic-first, SAR, Asia/Riyadh.
5. **Approval-first.** AI recommends; humans approve external commitments.
6. **Draft-only by default.** All outbound send flags off.
7. **Arabic-first.** Primary language is Arabic; English mirrors for investors/partners.

---

## 8. Market Risks & Assumptions

| Risk | Impact | Confidence | Mitigation |
|---|---|---|---|
| Sector estimates are imprecise | Medium | High (estimates are low-confidence) | Track actual pipeline data; refine SAM quarterly. |
| Saudi SME digitization slower than expected | Medium | Medium | Diagnosis-led wedge works even with low digitization. |
| Buyer expects guaranteed ROI | Medium | Medium | Clear no-overclaim posture; proof packs replace promises. |
| WhatsApp opt-in friction | Medium | Medium | Draft-only default; controlled live outbound only after opt-in. |
| Competitor enters same category | Low-medium | Low | Moat is Saudi-native trust + 14-OS bundle + proof system, not a single feature. |
| Regulatory change (PDPL/ZATCA) | Medium | Low-medium | Compliance/ops lead hire trigger; continuous watch via Market & Competitor Watch OS. |

---

## 9. Related Documents

- `DEALIX_STARTUP_ARCHITECTURE.md` — full system architecture
- `STARTUP_OPERATING_MODEL.md` — operating model, pricing, runway
- `DAILY_OPERATING_RHYTHM.md` — daily / weekly / monthly rhythm
- `docs/company/ICP.md` — ICP detail
- `docs/company/POSITIONING.md` — positioning detail
- `docs/company/SAUDI_MARKET_POSITIONING_AR.md` — Arabic Saudi positioning
- `docs/company/SECTOR_PLAYBOOKS.md` — sector playbooks