# Dealix · Go-Live Master Checklist · قائمة التحقق الشاملة للتدشين

> The single source of truth for "are we ready to launch?". Tick boxes
> in order. Don't skip — each gate depends on the prior.
>
> **Status as of:** 2026-06-01 · **Owner:** Founder · **ETA to live:** 7 days

---

## 🟢 DONE — Code & infrastructure (Claude شحنها)

### Backend
- [x] FastAPI app with 162 routers (100% mounted)
- [x] Moyasar checkout endpoint + HMAC webhook
- [x] ZATCA Phase 2 receipt skeleton
- [x] 10 agents wired (intake/ICP/pain/qual/prospector/CRM/booking/followup/outreach/proposal)
- [x] Draft→Approve→Deliver loop via `approval_center`
- [x] Source Passport for PDPL
- [x] Proof Ledger (L0-L5 framework)
- [x] Source code public on GitHub
- [x] 11 doctrine non-negotiables enforced in CI
- [x] Unified founder cockpit endpoint `/api/v1/founder/dashboard/cockpit`
- [x] Daily KPI snapshot + weekly scorecard cron
- [x] Red-line alerts (4 thresholds)
- [x] Sprint checklist tracker (10 steps)
- [x] Invite email with `email_allow_live_send` gate

### Frontend
- [x] Bilingual checkout page (5 plans)
- [x] Public status page (`/[locale]/status`)
- [x] Founder cockpit page (`/[locale]/ops/cockpit`)
- [x] Customer portal, login, register, dashboard
- [x] Free Diagnostic intake

### Docs & playbooks (22 files in `docs/playbooks/` index)
- [x] Doctrine manifesto (public)
- [x] PDPL public statement
- [x] Refund + cancellation policy
- [x] Public FAQ (8 sections)
- [x] First 7 days launch runbook
- [x] Founder daily runbook
- [x] Investor 1-pager (not-raising posture)
- [x] Inbound Q&A bank (21 Qs bilingual)
- [x] Capital asset register (YAML)
- [x] Onboarding email sequence (Day 0/1/3/5/7)
- [x] Sales playbook complete (Objection/Follow-up/Proposal/Demo/Case Study)
- [x] Agency partner outreach drafts (3)
- [x] LinkedIn library (10 posts bilingual)

### CI/CD
- [x] Doctrine gate in CI
- [x] Daily KPI snapshot workflow (cron 04:30 UTC)
- [x] Weekly scorecard workflow (cron Sun 06:00 UTC)
- [x] Frontend verify job
- [x] Railway Docker builds job

---

## 🟡 BLOCKED ON FOUNDER ACTION

### Day 0 — Critical path (1 hour total)

- [ ] **Submit Moyasar KYC** at dashboard.moyasar.com (30 min)
  - Need: CR (commercial registration) PDF
  - Need: Bank statement (last 3 months)
  - Need: ID copy
  - Expected wait: 1-3 business days

- [ ] **Set Railway production env vars** (15 min)
  ```
  ENVIRONMENT=production
  APP_SECRET_KEY=<generate fresh 64-byte hex>
  JWT_SECRET_KEY=<generate fresh 64-byte hex>
  ADMIN_API_KEYS=<one strong random>
  APP_URL=https://api.dealix.me
  CORS_ORIGINS=https://dealix.sa,https://www.dealix.sa
  ```

- [ ] **Confirm DNS records** (15 min)
  - `dealix.sa` → frontend Railway service
  - `api.dealix.me` → API Railway service
  - `dealix.me` → marketing/landing

### Day 3 (after Moyasar approval)

- [ ] **Add Moyasar live keys to Railway**
  ```
  MOYASAR_SECRET_KEY=sk_live_***
  MOYASAR_WEBHOOK_SECRET=***
  DEALIX_MOYASAR_MODE=live
  ```

- [ ] **Register webhook in Moyasar dashboard**
  URL: `https://api.dealix.me/api/v1/webhooks/moyasar`
  Events: payment_paid, payment_refunded, payment_failed, payment_captured

- [ ] **First 1 SAR live transaction** (smoke test)
  Card: founder's own. Verify payment_ops + receipt email.

### Week 1 — Launch sequence

- [ ] LinkedIn post #1 scheduled (Tuesday 09:00 KSA)
- [ ] LinkedIn post #2 scheduled (Thursday 09:00 KSA)
- [ ] LinkedIn post #3 scheduled (Saturday 09:00 KSA)
- [ ] DM 5 warm-intro contacts (manual)
- [ ] Free Diagnostic E2E test (founder submits a test)
- [ ] Update `pipeline_tracker.csv` with first 5 names

---

## 🔵 NEEDS FOUNDER INPUT (لا أقدر أكمل بدونها)

To finish the highest-level launch readiness, I need from you:

### Identity & contact
1. **CR number** (or status of registration)
2. **Bank account name** (for Moyasar payout records — not actual account number)
3. **Personal Calendly URL** (or Calendly username so I link it)
4. **WhatsApp Business number** (for warm channel)
5. **LinkedIn profile URL**
6. **Twitter/X handle** (existing or new)
7. **Email forwarding setup:** which provider for `hello@`, `support@`,
   `privacy@`, `security@`, `refunds@`, `cancel@` (Google Workspace?
   Resend domain auth?)

### Warm intro list (the most important)
8. **10-15 warm intro candidates** with:
   - Name (in Arabic ideally)
   - Company
   - Sector
   - How you know them (1 line)
   - Best channel (LinkedIn / WhatsApp / Email)
   - Suggested message hook (one specific thing about them)

   → I'll draft personalized DMs ready for your one-click approval.

### Agency partner targets
9. **Top 5 Saudi marketing/sales agencies** to approach as partners
   - Name, founder name, sector focus, your prior interaction (if any)
   - → I'll draft personalized outreach for each.

### Sector focus
10. **Top 3 sectors to prioritize** in the first 90 days
    Options seen in code: SaaS, fintech, logistics, agencies,
    manufacturing, healthcare, real estate, e-commerce
    → I'll write a dedicated positioning brief per sector.

### Brand assets
11. **Logo** (SVG or PNG) — current or stub OK
12. **Brand colors** (primary + accent in HEX) — current or "design later"
13. **Founder photo** for LinkedIn/website
14. **Brand voice sample** (1-2 paragraphs you wrote yourself) — so I
    can calibrate generated Arabic to match your voice

### Production env confirmations
15. **Anthropic API key in Railway?** (for Claude — primary LLM router)
16. **Resend or SendGrid?** Pick one for transactional email
17. **PostHog project?** (analytics — optional but recommended)
18. **Sentry DSN?** (error tracking — optional)

### Customer signals
19. **Any existing customer conversations?** (even informal — I can log
    them in pipeline_tracker.csv to preserve continuity)
20. **Any prior offers verbally made?** (we honor commitments —
    needs to be in proof_ledger)

---

## 🟣 OPTIONAL — Nice to have before launch

These multiply quality but don't block first SAR:

- [ ] **Press kit** — for journalists (logos, founder bio, screenshots)
- [ ] **Demo video** (90 sec) — for inbound + LinkedIn
- [ ] **Saudi tech directory listings** (Lean Tech, Founders Mena, etc.)
- [ ] **Twitter/X content library** (10 tweets — Claude can draft when
      handle confirmed)
- [ ] **Sector positioning briefs** (3-5 — Claude can draft when
      sectors picked)
- [ ] **WhatsApp Business catalog** (5 SAR Pilot card)
- [ ] **Customer success welcome video** (10 sec founder selfie)

---

## 🟠 INTENTIONALLY DEFERRED

Per doctrine + scope discipline:

- ❌ **Cold outreach lists** — never, doctrine #2
- ❌ **LinkedIn automation tool** — never, doctrine #11
- ❌ **Scraping connector** — never, doctrine #3
- ❌ **Investor pitch deck** — not raising (per INVESTOR_ONE_PAGER.md)
- ❌ **Multi-language beyond AR + EN** — focus first
- ❌ **Mobile app** — web-first until product/market fit

---

## Launch verification gates

### Gate 1: Code ✅ (today)
- [x] CI passes the doctrine gate
- [x] All routers mounted
- [x] Frontend builds
- [x] All playbook docs written

### Gate 2: Infrastructure (Day 0-3)
- [ ] Railway deployed with latest main
- [ ] All env vars set
- [ ] DNS records resolving
- [ ] /health returns 200 in production

### Gate 3: Payment (Day 3-5)
- [ ] Moyasar KYC approved
- [ ] Live keys in Railway
- [ ] Webhook registered + tested
- [ ] First 1 SAR captured + reflected in `/api/v1/payment-ops/list`

### Gate 4: First outbound (Day 5-7)
- [ ] 3 LinkedIn posts live
- [ ] 5 warm intro DMs sent
- [ ] First Free Diagnostic submitted by a non-founder
- [ ] Inbound replies handled within 30 min SLA

### Gate 5: First demo (Day 7-14)
- [ ] 1 demo booked
- [ ] Demo executed per `DEMO_SCRIPT.md`
- [ ] Pipeline_tracker updated with outcome
- [ ] Founder time logged

### Gate 6: First revenue (Day 14-30)
- [ ] 1 paid Sprint (499 SAR or 1 SAR pilot for verification)
- [ ] ZATCA receipt issued + verified
- [ ] Customer entered Sprint flow
- [ ] First proof event captured

### Gate 7: Sprint completion (Day 21-37)
- [ ] First customer's Sprint completed
- [ ] Proof Pack delivered
- [ ] NPS captured
- [ ] Decision: continue to Managed Ops? case study?

---

## How to use this document

1. **Founder reads top-to-bottom** once.
2. **Tick boxes only when verified.** Don't pre-tick.
3. **The blocked-on-founder section is the bottleneck.** Everything
   else is ready.
4. **Re-read every Monday morning** until Gate 7 hit.

---

## What I (Claude) need from you NOW

To maximize parallel work while you do the founder-only steps, the
most valuable inputs to send me:

**Priority 1 (unblocks 80% of remaining content):**
- Warm intro list (item 8 above)
- Top 3 sectors (item 10)

**Priority 2 (improves quality):**
- LinkedIn URL + Calendly URL (items 5, 3)
- Brand voice sample (item 14)

**Priority 3 (nice but skippable):**
- Logo, colors, photo (items 11-13)

Send any of these in chat — I'll draft sector briefs + personalized
warm intro DMs + Twitter library + brand voice calibration in the
next session.

For credentials (env vars, API keys, KYC docs): **DO NOT paste in
chat or commit to git.** Set them on Railway directly. I never need
to see them.
