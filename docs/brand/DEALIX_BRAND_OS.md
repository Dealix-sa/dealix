# Dealix Brand Operating System | نظام تشغيل العلامة التجارية

> **Source of truth for how the Dealix brand behaves across every product, touchpoint, and audience.**
> Branch: `phase/startup-architecture-brand-os`
> Arabic is the primary positioning language. English mirrors exist for investors and international partners.
> Related: [`DEALIX_COMPANY_OS_EN.md`](../company/DEALIX_COMPANY_OS_EN.md), [`DEALIX_STARTUP_ARCHITECTURE.md`](../company/DEALIX_STARTUP_ARCHITECTURE.md), [`POSITIONING.md`](POSITIONING.md), [`BRAND_GUARDRAILS.md`](BRAND_GUARDRAILS.md)

---

## 1. Brand Purpose | الغاية

**Dealix exists to turn every commercial function inside a Saudi company from manual chaos into a measurable, provable intelligent operating system — in weeks, not years.**

We do not sell tools. We do not sell dashboards that observe. We do not sell agents that chat. We build and operate compact AI operating systems — one per commercial function — that run discovery, decision, delivery, and proof end-to-end under human approval.

The purpose is operational, not aspirational. Every claim is backed by a Proof Pack: baseline → after → documented delta. No proof, no claim.

### 1.1 Purpose pillars

| Pillar | Meaning | What it rejects |
|---|---|---|
| **Executive seriousness** | We wear a suit, not a t-shirt. The brand addresses founders and COOs as operators, not as consumers. | Playful chatbot branding, hype, "AI magic" clichés. |
| **Trustworthy by evidence** | Every public claim is proof-backed. Forecasts are scenarios with confidence levels and assumptions. | Guaranteed ROI, fake testimonials, unverified percentages. |
| **Saudi-first, Arabic-first** | Saudi LLC, SAR pricing, Asia/Riyadh timezone, PDPL-native, ZATCA-aware. Arabic is the primary language; English mirrors for investors. | Generic global templates, translated-afterthought Arabic, foreign-first positioning. |
| **Governed, not autonomous** | AI explores, analyzes, recommends. Deterministic workflows execute. Humans approve critical external commitments. | Autonomous external sending, unsupervised agents, "set it and forget it" promises. |

---

## 2. Brand Promise | وعد العلامة

### Arabic (primary)
> من فوضى الفرص والمتابعات إلى نظام إيراد واضح — محوكَم، قابل للتدقيق، مُثبَت بالأدلة.

### English (mirror)
> From the chaos of opportunities and follow-ups to a clear revenue system — governed, auditable, and proven with evidence.

### Promise contract
The promise is not a slogan; it is a contract with the market:

1. **Clear** — we replace scattered tools, spreadsheets, and WhatsApp threads with one operating system per function.
2. **Governed** — every external action passes a visible approval gate. No autonomous sends. No unsupervised commitments.
3. **Auditable** — every decision, draft, approval, and send is logged. Audit trail completeness target: 100%.
4. **Proven** — every external results claim requires a real Proof Pack: baseline → after → documented delta. No proof, no claim.

---

## 3. Brand Architecture | بنية العلامة

### 3.1 Master-brand model

Dealix uses a **master-brand architecture**. Every product carries the Dealix name and inherits the master brand's trust engine, approval gates, and voice. Products are not sub-brands with independent identities; they are governed extensions of the Dealix operating system.

```
                        DEALIX (Master Brand)
                              |
         ┌────────────────────┼────────────────────┐
         |          |          |          |          |
   Trust Kernel  Product OS Layer  Delivery  Proof
   (Layer 0)    (Layer 4)        (Layer 5) (Proof Packs)
         |          |          |          |
    PDPL · Approval   14 OSes   FastAPI   Baseline →
    Gates · Audit     (see 3.3) Workers   After → Delta
    Trails · No-                 Web      Documentation
    overclaim register
```

### 3.2 Naming convention

- **Master brand:** Dealix (ديليكس)
- **Product naming:** `[Function] OS` — e.g., Revenue Command Room OS, Client Delivery OS, AI Trust & Compliance OS.
- **Arabic product naming:** `[الوظيفة]` — e.g., غرفة قيادة الإيرادات, نظام تسليم العملاء.
- **No product-level logos.** All products use the Dealix master logo. Products are differentiated by naming and function, not by visual identity.
- **No product-level taglines.** The master brand promise applies to every product.

### 3.3 The 14 product operating systems

Each product is a self-contained OS with defined inputs, outputs, approval gates, and proof artifacts. They share the same trust engine and draft-only-by-default outbound posture.

| # | Product (EN) | المنتج (AR) | Brand role |
|---|---|---|---|
| 1 | Revenue Command Room OS | غرفة قيادة الإيرادات | Flagship — daily revenue command |
| 2 | Company Brain OS | دماغ الشركة | Foundation — knowledge + memory layer |
| 3 | WhatsApp / Inbox Follow-up OS | نظام متابعة الواتساب والبريد | Touchpoint — approval-gated follow-ups |
| 4 | Email Outreach Review OS | نظام مراجعة بريد التواصل | Touchpoint — drafted outbound, approval before send |
| 5 | SMS Notification / Follow-up OS | نظام إشعارات ومتابعة SMS | Touchpoint — drafted SMS, `SMS_SEND_ENABLED=false` default |
| 6 | AI Trust & Compliance OS | نظام الثقة والامتثال | Trust pillar — PDPL, audit trails, no-overclaim register |
| 7 | Client Delivery OS | نظام تسليم العملاء | Delivery — discovery → build → test → success report |
| 8 | Controlled Live Outbound OS | نظام التواصل الحي المُحكم | Expansion — strictly gated live outbound, default off |
| 9 | Founder Decision Desk | مكتب قرارات المؤسس | Decision layer — daily queue, escalation, delegation |
| 10 | Company Diagnosis Sprint | سبرنت تشخيص الشركة | Entry point — paid 1-week diagnostic |
| 11 | Offer Intelligence OS | نظام ذكاء العروض | Commercial — offer ladder, pricing engine |
| 12 | Market & Competitor Watch OS | نظام مراقبة السوق والمنافسين | Intelligence — sector radar, regulatory updates |
| 13 | Proposal + Contract OS | نظام العروض والعقود | Commercial — ZATCA-aware invoicing, Moyasar links |
| 14 | Executive Proof Pack OS | نظام حزم الإثبات التنفيذية | Proof — baseline → after → documented delta |

### 3.4 Bundling and the trust engine

Products are sold individually and in bundles (2–3 OSes typical for subscription). All 14 share:
- The same **trust kernel** (Layer 0): PDPL controls, approval classes, audit trails, no-overclaim register.
- The same **approval gates**: no autonomous external sending. Every external action requires human approval + correct send flags.
- The same **proof discipline**: Proof Packs are the renewal artifact and the only basis for external results claims.

---

## 4. Brand Expressions | تعبيرات العلامة

The brand expresses across six surfaces. Each surface has defined rules and references.

### 4.1 Expression map

| Surface | Owner doc | Key rules |
|---|---|---|
| **Website** | [`WEBSITE_MESSAGING.md`](WEBSITE_MESSAGING.md) | Arabic-first, English mirror. Disclosure on every public page. No fake clients or ROI. |
| **Voice & tone** | [`VOICE_AND_TONE.md`](VOICE_AND_TONE.md) | Confident, precise, operational, Arabic-first. No hype words. |
| **Visual identity** | [`VISUAL_DIRECTION.md`](VISUAL_DIRECTION.md), [`VISUAL_IDENTITY.md`](VISUAL_IDENTITY.md), [`COLOR_SYSTEM.md`](COLOR_SYSTEM.md), [`TYPOGRAPHY.md`](TYPOGRAPHY.md) | Dark executive theme. Navy primary, Gold accent, Emerald for proof only. |
| **Sales & delivery** | [`DEALIX_PRESENTATION_STYLE_GUIDE_AR.md`](DEALIX_PRESENTATION_STYLE_GUIDE_AR.md) | 12-slide deck max. One message per slide. Proof, not hype. Every offer shows pain, outcome, deliverables, price, next step. |
| **WhatsApp / client comms** | [`../whatsapp/`](../whatsapp/) | Approval-gated drafts. No live send by default. Human review before any external message. |
| **Positioning** | [`POSITIONING.md`](POSITIONING.md) | AI Operating Systems for B2B. Not a chatbot, CRM, agency, or dashboard. |

### 4.2 Touchpoint principles (apply to every surface)

1. **Arabic-first.** Arabic is the primary language. English mirrors exist but are never the lead. Never half-translate — AR and EN must be parallel and equal-weight.
2. **Disclosure always.** Every public page and external document carries: "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة."
3. **Proof over promise.** Use Proof Pack language ("documented delta", "baseline → after") over outcome language ("transform", "skyrocket").
4. **Governed over autonomous.** Describe the approval gate, not the "AI agent that does it all."
5. **Saudi-native.** SAR pricing, PDPL references, ZATCA awareness, Riyadh timezone. Never present as a foreign company.

### 4.3 Forbidden expression patterns

| Forbidden | Why | Use instead |
|---|---|---|
| "حوّل عملك" / "Transform your business" | Hype, no proof | "نظام إيراد محوكَم مع إثبات قابل للتدقيق" |
| "خارق" / "Supercharge" | Hype | "عمليات محوكمة مع إثبات قابل للتدقيق" |
| "مدعوم بالذكاء الاصطناعي" as a slogan / "AI-powered" as a slogan | Every B2B product is; it is not a differentiator | Name the specific OS and its approval-gated workflow |
| "نتائج مذهلة فورًا" / "Instant amazing results" | Fake, unverifiable | "قيمة تقديرية موثّقة المصدر" + disclosure |
| "نضمن لك مبيعات" / "Guaranteed sales" | Prohibited by no-overclaim register | "فرص مُثبتة بأدلة" |
| Generic AI robot imagery | Chatbot positioning, not OS positioning | Dashboards, decision rooms, revenue maps, proof packs |

---

## 5. Brand Governance | حوكمة العلامة

### 5.1 Governance authority

- **Brand owner:** Founder / CEO (current stage).
- **Brand custodian:** Founder until a brand/ops lead is hired (trigger: first enterprise pilot or regulator engagement).
- **Source of truth for tokens:** `frontend/tailwind.config.ts` (live design tokens). Docs explain and organize; they do not change code.
- **Source of truth for messaging:** This file + [`POSITIONING.md`](POSITIONING.md) + [`VOICE_AND_TONE.md`](VOICE_AND_TONE.md) + [`BRAND_GUARDRAILS.md`](BRAND_GUARDRAILS.md).

### 5.2 The no-overclaim register

Strictly forbidden in any brand expression, by any person, on any surface:

1. **Guaranteed ROI** — no guarantee of revenue, sales, or return.
2. **Specific percentages as guarantees** — "increase revenue by 300%" is prohibited. Scenario-based forecasts with confidence levels and assumptions are allowed.
3. **Fake clients or testimonials** — no invented names, logos, quotes, or case studies. No real client is named without a signed Proof Publication Consent (see [`../wave8/PROOF_PUBLICATION_CONSENT_TEMPLATE.md`](../wave8/PROOF_PUBLICATION_CONSENT_TEMPLATE.md)).
4. **Certified compliance claims** — Dealix is PDPL-aware and ZATCA-aware, not "PDPA-certified" or "ZATCA-certified." We build controls; we do not hold regulator certifications we have not earned.
5. **Autonomous sending claims** — never imply the system sends without human approval. The default state is `OUTBOUND_MODE=draft_only`.

### 5.3 Approval matrix for brand expressions

| Expression type | Approver | Condition |
|---|---|---|
| Website copy (public) | Founder | Must pass guardrails check + disclosure present |
| Sales deck | Founder | 12-slide max, proof-backed claims only |
| External results claim | Founder | Real Proof Pack: baseline → after → documented delta |
| Client case study / testimonial | Founder + client sign-off | Signed Proof Publication Consent on file |
| Partner co-branded material | Founder | Must follow [`BRAND_GUARDRAILS.md`](BRAND_GUARDRAILS.md) co-branding rules |
| Live outbound enablement | Founder | `EXTERNAL_SEND_ENABLED=true` + per-channel flags + opt-in + legal review |
| Hire-based brand role change | Founder | Trigger actually fired (see company OS hiring triggers) |

### 5.4 Brand consistency checks (pre-publication)

Before any external material ships, verify:

- [ ] Arabic is primary; English mirror is parallel and equal-weight (not a half-translation).
- [ ] Disclosure line present: "Estimated value is not Verified value."
- [ ] No hype words ("transform", "supercharge", "AI-powered" as slogan, "instant", "amazing").
- [ ] No guaranteed ROI, no fake clients, no specific percentages as guarantees.
- [ ] No "certified compliance" claims (PDPL-aware, not certified).
- [ ] Visuals use Navy primary, Gold sparingly, Emerald for proof only. No generic AI robot imagery.
- [ ] Logo used per [`LOGO_USAGE.md`](LOGO_USAGE.md). Safe space respected. No recoloring, rotating, or stretching.
- [ ] Fonts per [`TYPOGRAPHY.md`](TYPOGRAPHY.md). No italic for Arabic. RTL for Arabic, LTR for English.
- [ ] Every forecast is a scenario with confidence level + assumptions (not a guarantee).

### 5.5 Brand drift signals (red flags)

The brand is drifting if any of these appear:
- English becomes the primary language on Saudi-market-facing surfaces.
- The disclosure line is missing from a public page.
- A product gets its own logo or tagline (violates master-brand architecture).
- Emerald appears as a brand color instead of a proof/success signal.
- Gold is used for large background fills.
- Any claim uses "guaranteed", "certified", or a specific percentage without a scenario caveat.
- Imagery shifts to chatbot/robot visuals instead of dashboards, decision rooms, and proof packs.

---

## 6. How Brand Connects to Every Product | ربط العلامة بكل منتج

### 6.1 The brand-product connection model

Every product inherits the master brand and must express it through four layers:

```
┌─────────────────────────────────────────────────────┐
│  Master Brand: Dealix                                │
│  Promise · Purpose · Voice · Visual Identity         │
├─────────────────────────────────────────────────────┤
│  Product: [Function] OS                               │
│  ┌───────────┬───────────┬───────────┬───────────┐  │
│  │ Trust     │ Approval  │ Proof     │ Voice &   │  │
│  │ Kernel    │ Gates     │ Artifacts │ Tone      │  │
│  │ (shared)  │ (shared)  │ (per OS)  │ (shared)  │  │
│  └───────────┴───────────┴───────────┴───────────┘  │
├─────────────────────────────────────────────────────┤
│  Touchpoint: [Surface]                               │
│  Website · WhatsApp · Sales deck · Proof Pack        │
└─────────────────────────────────────────────────────┘
```

### 6.2 Per-product brand expression checklist

For each of the 14 products, the brand must be expressed through:

1. **Naming** — `[Function] OS` in EN, `[الوظيفة]` in AR. Uses master Dealix logo.
2. **Trust inheritance** — the product's docs and UI reference the shared trust kernel (PDPL, approval gates, audit trails, no-overclaim register).
3. **Approval gates** — the product's workflow shows visible approval gates. UI badges: Approved = Emerald, Pending = Gold, Rejected = destructive red.
4. **Proof artifacts** — the product produces or feeds Proof Packs. No external claim is made without a documented delta.
5. **Voice** — the product's copy follows [`VOICE_AND_TONE.md`](VOICE_AND_TONE.md). Confident, precise, operational, Arabic-first.
6. **Visual** — the product's UI follows [`VISUAL_DIRECTION.md`](VISUAL_DIRECTION.md). Navy primary, Gold accent, Emerald for proof states only.

### 6.3 Product-to-touchpoint mapping

| Touchpoint | Primary products involved | Brand expression focus |
|---|---|---|
| Website (homepage, product pages) | All 14 | Category creation, proof discipline, disclosure |
| WhatsApp client comms | #3, #7, #8 | Approval-gated drafts, human review, no live send by default |
| Sales deck | #10, #11, #13, #14 | Diagnosis → pilot → subscription → proof pack lifecycle |
| Proof Pack (renewal artifact) | #14, #1, #7 | Baseline → after → documented delta. The only basis for results claims. |
| Command Room (daily ops) | #1, #2, #9 | Executive seriousness, governed operations, daily rhythm |
| Compliance surface | #6 | PDPL-aware (not certified), audit trails, no-overclaim register |

---

## 7. Brand Lifecycle | دورة حياة العلامة

### 7.1 Stage: Founder-led (current)

- Founder is brand owner, custodian, and approver.
- All outbound is draft-only by default (`OUTBOUND_MODE=draft_only`).
- No public results claims until first real Proof Pack exists.
- Arabic-first on all Saudi-market surfaces. English mirrors for investor-facing materials.

### 7.2 Stage: First pilots (trigger: 2 concurrent paid pilots)

- Brand expressions may reference the pilot stage honestly ("in pilot", "P1 offer").
- Proof Packs from pilots become the first permissible results claims — only with client consent.
- Delivery lead may be hired (trigger-based, not forecast-based).

### 7.3 Stage: Recurring subscriptions (trigger: 1 recurring subscription)

- Brand may describe the subscription model publicly.
- Case studies require signed Proof Publication Consent.
- Brand governance expands: a brand/ops lead may be hired (trigger: first enterprise pilot or regulator engagement).

### 7.4 Stage: Expansion (trigger: 5 active subscriptions)

- Bundled OS messaging becomes primary (2–3 OSes per client).
- Brand consistency checks become a recurring operational rhythm, not a one-time gate.
- Customer success role may be hired (trigger: 5 active subscriptions).

---

## 8. Related Documents | وثائق ذات صلة

- [`POSITIONING.md`](POSITIONING.md) — positioning statement, category creation, competitive frame
- [`VOICE_AND_TONE.md`](VOICE_AND_TONE.md) — voice characteristics, tone by context, do's and don'ts
- [`WEBSITE_MESSAGING.md`](WEBSITE_MESSAGING.md) — homepage hierarchy, hero message, CTA strategy
- [`BRAND_GUARDRAILS.md`](BRAND_GUARDRAILS.md) — prohibited claims, visual/messaging guardrails, co-branding rules
- [`VISUAL_DIRECTION.md`](VISUAL_DIRECTION.md) — color, typography, layout, component, imagery direction
- [`BRAND_GUIDELINES_AR.md`](BRAND_GUIDELINES_AR.md) — comprehensive Arabic brand guidelines (v2.0)
- [`COLOR_SYSTEM.md`](COLOR_SYSTEM.md) — full color palette with WCAG compliance
- [`TYPOGRAPHY.md`](TYPOGRAPHY.md) — font stack, size scale, RTL/LTR rules
- [`VISUAL_IDENTITY.md`](VISUAL_IDENTITY.md) — consolidated visual identity guide
- [`LOGO_USAGE.md`](LOGO_USAGE.md) — logo usage rules, clear space, incorrect uses
- [`../company/DEALIX_COMPANY_OS_EN.md`](../company/DEALIX_COMPANY_OS_EN.md) — company operating system (English mirror)
- [`../company/DEALIX_STARTUP_ARCHITECTURE.md`](../company/DEALIX_STARTUP_ARCHITECTURE.md) — full system architecture

---

> **آخر تحديث**: 1 يونيو 2026 | **الإصدار**: 1.0 | **اللغة الأساسية**: العربية
> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**