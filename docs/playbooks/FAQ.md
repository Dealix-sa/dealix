# FAQ · الأسئلة الشائعة

> Public-facing. Bilingual. The single source of truth for inbound
> questions on social, email, sales calls. Update when a new objection
> appears in `docs/sales/OBJECTION_HANDLING.md`.
>
> **Effective:** 2026-06-01

---

## القسم ١: ما هو Dealix؟ · What is Dealix?

### ما هو Dealix بالضبط؟

Dealix هو **نظام تشغيل إيرادات (Revenue OS)** للشركات السعودية في
B2B. ليس chatbot، ليس CRM، ليس automation tool. هو طبقة تنظمها
الفاوندر على outreach والمبيعات والـ proof — كل رسالة تخرج تمر
بموافقة بشرية، كل قرار له audit trail، كل رقم له مصدر مسجل.

### How does Dealix differ from existing AI tools?

Three differences:
1. **Approval-first:** every outbound message awaits founder
   approval. No autonomous send. Ever.
2. **Saudi-first:** PDPL-compliant by default, ZATCA-receipts
   integrated, Arabic-primary voice across all touchpoints.
3. **Proof-backed:** every claim ties to a `proof_ledger` event,
   never to invented benchmarks.

---

## القسم ٢: الأسعار والـ Offers · Pricing & Offers

### كم تكلفة Dealix؟

نشر السعر علنًا — لا hidden pricing (doctrine #7):

| Offer | Price | What you get |
|-------|-------|--------------|
| Free Diagnostic | 0 SAR | 1-page report in 24-48h |
| 1 SAR Pilot | 1 SAR | Transaction smoke test |
| 7-day Sprint | 499 SAR | Top-10 prospects + DQ Report + Proof Pack |
| Starter monthly | 999 SAR/mo | Baseline managed ops |
| Growth monthly | 2,999 SAR/mo | Full managed ops + weekly report |
| Scale monthly | 7,999 SAR/mo | Executive command center |
| Custom AI | 5-25K SAR | Scoped engagement (4+ weeks) |

كل الأسعار شاملة VAT (ZATCA-compliant).

### Can I try before I buy?

Three ways:
1. **Free Diagnostic** — 6 questions, 24h reply, no commitment.
2. **1 SAR pilot** — verify Moyasar checkout + receipt flow.
3. **7-day Sprint with refund guarantee** — 499 SAR refundable if no
   proof events recorded.

### What's the refund policy?

See `docs/contributing/REFUND_POLICY.md`. Summary:
- Sprint refundable if no proof events captured in 7 days.
- Monthly: month 1 fully refundable; months 2-3 prorated; auto-mode
  needs 14-day notice.
- 1-SAR pilot non-refundable by design.

---

## القسم ٣: الـ Doctrine والـ Compliance

### What are the "11 non-negotiables"?

Eleven things Dealix never does (enforced in code with CI tests):

1. **no_live_send** — no autonomous external messages
2. **no_cold_whatsapp** — WhatsApp only with warm consent
3. **no_scraping** — public data only via licensed APIs
4. **no_fake_proof** — every metric ties to a ledger event
5. **no_unconsented_data** — PDPL lawful basis on every lead
6. **no_unverified_outcomes** — no guaranteed-results claims
7. **no_hidden_pricing** — all terms public upfront
8. **no_silent_failures** — every error logged + audited
9. **no_unbounded_agents** — hard guardrails on every agent
10. **no_unaudited_changes** — review required on every commit
11. **no_linkedin_automation** — manual outreach only

Full doctrine: [/AGENTS.md](../AGENTS.md).

### كيف تضمنون PDPL compliance؟

Three layers:
- **Source Passport** على كل lead قبل أي رسالة (lawful basis مسجل)
- **Suppression list** محترمة قبل كل send
- **Auto-delete** للبيانات بعد ٩٠ يوم من إنهاء العلاقة (إلا لو
  وقّعت retention agreement)
- **DPO appointed** قبل أول S3 customer (per PDPL §27)

### Where is my data stored?

Postgres encrypted at-rest, hosted in **Saudi Arabia (Riyadh)** via
Railway's KSA region. Data never leaves the Saudi perimeter without
the customer's explicit consent and a signed DPA with the receiving
party (e.g. OpenAI's DPA before any LLM call on customer data).

---

## القسم ٤: الـ Integrations والـ Tech

### What integrations does Dealix support?

Wired and tested:
- **Payments:** Moyasar (Mada, Visa, Mastercard, Apple Pay)
- **CRM:** HubSpot (optional, sync on lead create)
- **Calendar:** Calendly
- **WhatsApp:** Meta Cloud API, Green API, Ultramsg, Fonnte (all
  gated behind `whatsapp_allow_live_send=False` by default)
- **Email:** Resend, SendGrid, SMTP, Gmail OAuth (gated)
- **LLM:** Anthropic Claude (primary), OpenAI, Groq, Deepseek

NOT supported (by doctrine, never):
- LinkedIn automation (any third-party tool)
- Scraping (Apollo, ZoomInfo, etc.)
- Cold-list providers without explicit consent records

### هل أستطيع استخدام بياناتي على نموذج LLM ثالث؟

نعم — إذا وقّعت على DPA معه (مثلاً OpenAI DPA لو تختار GPT-4 بدلاً
من Claude). Dealix يمرر فقط البيانات الضرورية، ويسجل في
`proof_ledger` كل LLM call مع المزود + الـ DPA reference.

### Can I self-host Dealix?

Custom AI engagements support on-premise / VPC deploys with a
6-12 week implementation timeline. Pricing starts at 15K SAR + monthly
license. Email `sami.assiri11@gmail.com` for details.

---

## القسم ٥: الـ Founder operating reality

### How long does the founder spend on Dealix daily?

Realistic data from our own dogfooding:

- **Week 1:** ~25 min/day (training the agents on voice)
- **Week 3+:** ~5-7 min/day (mostly approving drafts that already
  match)
- **Month 2+:** ~3 min/day (queue auto-rejects clear mismatches)

If you're not willing to spend even 5 min/day on outbound, Dealix
isn't for you. We're not a "set and forget" tool — and any vendor
claiming that for B2B outreach is lying.

### What happens when my Sprint ends?

You get:
1. Final Proof Pack (14 sections, bilingual, downloadable)
2. Portable assets (HubSpot import, email templates, scripts)
3. One of three paths:
   - **Continue** with Managed Ops (999/2,999/7,999 SAR/mo)
   - **Custom AI** project (5-25K SAR)
   - **End** — data auto-deletes in 90 days

No upsell pressure. The Sprint stands on its own value.

### What if I don't have a tech team?

Sprint is fully founder-led — no engineering needed on your side.
Managed Ops adds:
- Weekly setup call (45 min)
- Slack/WhatsApp DM channel with the Dealix founder
- Monthly review video

We work with your existing tools (HubSpot, Gmail, etc.) — no rip-
and-replace.

---

## القسم ٦: الـ Partners والـ Ecosystem

### Do you work with marketing agencies?

Yes — but with strict rules (see
`docs/AGENCY_PARTNER_PROGRAM.md`):
- **Referral partner:** 15% rev-share on closed deals
- **Implementation partner:** 20-25% (requires ≥3 proof packs first)
- **Co-selling partner:** 25-30% (requires shared sales process
  certification)

Gold rule: no formal partnerships before 3 reference Proof Packs
exist.

### Can I become a Dealix customer AND partner?

Yes — common path. Many agencies start by running their own client
on a Sprint, see the value, then become referral partners.

---

## القسم ٧: المستقبل والـ Roadmap

### Are you raising funding?

Currently **founder-funded**. No external capital. Decisions are
optimized for customer value, not investor return on a clock.

### How big do you plan to get?

Goal at 90 days: **2-3 managed-ops customers + 8,000-10,000 SAR MRR**.
Goal at 1 year: **15-25 customers + 80-120K SAR MRR**. We grow as
fast as proof events accumulate — never faster.

### What if Dealix shuts down?

Customer data is portable from day 1:
- HubSpot export anytime
- Email templates as raw markdown
- Proof Pack as bilingual PDF
- All Postgres tables exported as CSV on request

No lock-in. If a better tool exists, take your data and go.

---

## القسم ٨: متى تتواصلون معي؟ · When will you contact me?

### Inbound rules

- We respond to WhatsApp/email within **30 min** during business
  hours (Sun-Thu 09:00-17:00 KSA).
- After hours: best effort, definitely within 24h.
- No autonomous follow-ups. If you went quiet, we go quiet (90-day
  silent window).

### How do I unsubscribe / opt-out?

- Email link in every message (always)
- WhatsApp: reply "stop" (logged in suppression_list within 30 sec)
- LinkedIn: just remove the connection (we don't re-add)
- Or email `unsubscribe@dealix.me` for blanket opt-out

All channels respect the same suppression list. Once you opt out
of one, you're out of all.

---

## لا تجد سؤالك؟ · Don't see your question?

- WhatsApp: founder direct (link on dealix.sa)
- Email: `hello@dealix.me`
- Calendly: 15-min Q&A slot — no pitch, just questions
- Twitter/X: @dealix_sa (DMs open)

Or open an issue at github.com/VoXc2/dealix/issues — we read every
one.

---

## Internal note

Every Q here was asked at least once in real conversation. We add
new Qs when an objection appears in `docs/sales/OBJECTION_HANDLING.md`.
Quarterly review for accuracy.
