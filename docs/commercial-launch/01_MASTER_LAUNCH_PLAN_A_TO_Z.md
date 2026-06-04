# Dealix — Master Launch Plan (A → Z)
## خطة الإطلاق الشاملة من الألف إلى الياء

> **Golden rule / القاعدة الذهبية:** AI drafts and ranks. The founder reviews and
> approves. The system never sends anything externally.
> الذكاء الاصطناعي يجهّز ويرتّب، والمؤسس يعتمد، والنظام لا يرسل خارجيًا أبدًا.

This is the single end-to-end launch plan across **every** business function.
Run the whole pipeline with:

```bash
python scripts/commercial_launch_all.py --target 400
```

It writes `LAUNCH_SNAPSHOT.md` + `.json` to `outputs/commercial_launch/<date>/`.

---

## 0. Positioning / التموضع
- **What:** Dealix is a Saudi/GCC B2B AI Revenue & Operations OS.
- **Who:** mid-market B2B firms in 5 verticals (FM, contracting/project controls,
  real estate ops, legal/professional services, consulting/training/B2B).
- **Why now:** Vision 2030 growth + fragmented workflows + reporting pressure.
- **Wedge:** AI Workflow Audit → Pilot → Department OS → Retainer → Enterprise.
- **Moat:** approval-first trust + sector playbooks + delivery OS.

---

## A. Product & Platform
- Productized ladder defined (`config/commercial_offers.json`).
- 400+ daily founder-review draft engine live (`scripts/commercial_generate_400_drafts.py`).
- Safety, quality, and compliance gates enforced and tested.
- **Gate:** all Commercial Launch OS tests green; safety audit PASS.

## B. Pricing & Packaging (SAR)
- Audit 499–2,500 · Pilot 5,000–25,000 · Department OS 25,000–150,000 ·
  Retainer 3,000–25,000/mo · Enterprise 150,000+.
- No ROI guarantees; outcomes are targets. See `02_OFFER_LADDER_SAR.md`,
  `03_PRICING_AND_PACKAGING.md`.

## C. Go-To-Market (Sales)
- Founder-led motion; 5-rung ladder; manual outreach only.
- Daily: generate → review top 50 → approve 20–50 → manual send → CRM update.
- Assets: messaging (`10`), objections (`11`), discovery (`12`), proposal (`13`),
  one-pager (`14`).

## D. Marketing & Media
- Media & Social OS (`docs/media-social-os/`): 10 pillars, 30-day calendar
  (plan only), LinkedIn/X/IG/TikTok/YouTube OS, press kit, ads **planning**.
- **No auto-publish, no bots, no scraping.**

## E. Demand Channels (Go/No-Go)
| Channel | Status |
|--------|--------|
| Cold email | NO-GO until SPF/DKIM/DMARC + manual founder send |
| Follow-up | NO-GO until a prior legitimate touch exists |
| LinkedIn | MANUAL-ONLY (no automation) |
| Website form | NO AUTO-SUBMIT |
| Paid ads | NO-GO until tracking (UTM) + legal/privacy review |
| Referral/partner | GO (manual, founder-owned) |

## F. Website & SEO
- Existing Next.js site already ships robots/sitemap/manifest/JSON-LD/OG, AR/EN.
- `site-commercial-verify` workflow gates readiness + SEO presence.
- Follow-up: add `/commercial`, `/verticals/*`, `/pricing`, `/trust`, `/contact`
  (intake-only, no external send) — see `docs/site-launch/99_SITE_LAUNCH_REPORT.md`.

## G. Lead Intake & CRM
- Schema + 14 stages (`config/crm_pipeline_schema.json`, `22_LEAD_INTAKE_AND_CRM_OS.md`).
- Public business contacts only; consent tracked; suppression honored.
- **Manual** tracking — no CRM push/send.

## H. Delivery & Operations
- Delivery OS (`15`), onboarding (`16`), pilot checklist (`17`),
  handover/success (`18`), retention/expansion (`19`).
- Every engagement: NDA/DPA first, data minimization, human approval, audit trail.

## I. Finance & Revenue
- Payment/checkout is manual, founder-owned — never auto-charged.
- Revenue/pipeline metrics are **manual inputs**, never system-assumed
  (`20_COMMERCIAL_METRICS_DASHBOARD.md`).

## J. Legal, Privacy & Compliance
- PDPL-aware; privacy-by-design; legal/professional vertical is privacy-first.
- Required before scale: privacy policy, terms, DPA template, complaint handling.
- See `21_EXTERNAL_GO_LIVE_REQUIREMENTS.md`.

## K. Trust & Safety
- Approval-first; no blind automation; no external sending from automation.
- Safety audit proves it on every run; `safety_violations` must be 0.

## L. Metrics & OKRs
- System metrics auto-generated; reply/revenue manual.
- **Launch OKRs (first 90 days, targets not guarantees):**
  - O1 Pipeline: 30+ qualified discovery calls.
  - O2 Proof: 5+ paid Audits, 2+ Pilots.
  - O3 Trust: 0 safety/compliance violations; 100% drafts approval-gated.
  - O4 Content: 60+ manually-published posts; press kit live.

## M. People & Roles
- Founder = approval owner for all external actions.
- Delivery owner per engagement; clear handover artifacts.

## N. Risk Register
- Deliverability/reputation → ramp plan + suppression.
- Privacy exposure → minimization, NDA/DPA, consent.
- Over-automation → hard safety gate (already enforced).
- Single-founder bottleneck → top-50 ranking + daily rhythm.

---

## 30 / 60 / 90 Day Plan

### Days 0–30 — Prove
- Run `commercial_launch_all.py` daily; founder approves top 20–50.
- Complete external go-live prerequisites (DNS/SPF/DKIM/DMARC, legal docs).
- Publish content manually (5x/week); ship press kit.
- Land first paid Audits.

### Days 31–60 — Repeat
- Convert Audits → Pilots; tighten objection handling from real replies.
- Add website commercial pages (one at a time, verify build each step).
- Stand up paid-ads tracking; keep ads in **planning** until review passes.

### Days 61–90 — Scale
- Convert Pilots → Department OS / Retainers.
- Rotate vertical focus by signal; expand warm/referral motion.
- Review OKRs; decide which vertical to double down on.

---

## Launch command (run everything)
```bash
python scripts/commercial_launch_all.py --target 400
python scripts/commercial_safety_audit.py
python scripts/commercial_launch_readiness.py
```

## Final Go / No-Go
**GO:** site launch, draft generation, founder review, media planning + manual
posting, paid diagnostics, discovery calls, proposals, delivery.

**NO-GO:** automated sending, cold WhatsApp, LinkedIn automation, bulk email,
website auto-submit, paid ads without tracking/legal review, processing
sensitive data before agreement.
