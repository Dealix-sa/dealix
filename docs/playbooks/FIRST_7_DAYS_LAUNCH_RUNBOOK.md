# First 7 Days Launch Runbook · دليل التدشين السبعة أيام

> The exact sequence of actions for the founder from "PR merges" to
> "first paying customer's Sprint completed". Day-by-day, hour-by-hour.
> Bilingual.
>
> **Pre-requisite:** all PRs (#521, #522, #524) merged. Code deployed
> on Railway production.

---

## Day 0 (Monday) — Revenue activation · يوم 0 — تفعيل الإيراد

### 09:00 KSA — Moyasar KYC
- [ ] Open dashboard.moyasar.com → log in
- [ ] Upload CR (commercial registration)
- [ ] Upload bank statement (latest 3 months)
- [ ] Submit live-mode application
- [ ] **Expected wait:** 1-3 business days for approval

### 10:30 KSA — Railway production env setup
- [ ] Open railway.app → Dealix project → API service → Variables
- [ ] Set (one at a time, save after each):
  ```
  ENVIRONMENT=production
  APP_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
  JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
  ADMIN_API_KEYS=<paste a 32-char random>
  APP_URL=https://api.dealix.me
  CORS_ORIGINS=https://dealix.sa,https://www.dealix.sa
  ```
- [ ] **Don't set Moyasar keys yet** — wait for KYC approval
- [ ] Trigger redeploy
- [ ] Verify: `curl -fs https://api.dealix.me/health` → 200

### 13:00 KSA — Pipeline tracker prep
- [ ] Open `docs/ops/pipeline_tracker.csv`
- [ ] Add 5 warm-intro names you'll DM this week
- [ ] For each: company, name, sector, reason-to-contact
- [ ] Status = "pending_first_dm"

### 14:00 KSA — Inbound prep
- [ ] Open `docs/playbooks/INBOUND_QA_BANK.md`
- [ ] Skim sections A-G; you'll need them this week
- [ ] Bookmark for fast paste

### 16:00 KSA — First LinkedIn post (manual schedule)
- [ ] Open `docs/sales-kit/linkedin_posts/post_04_no_autonomous_send.md`
- [ ] Copy AR primary version
- [ ] Open LinkedIn UI → Create post → paste
- [ ] Schedule for **Tuesday 09:00 KSA**
- [ ] Confirm schedule, log in pipeline_tracker

### 17:30 KSA — Evening trust review
- [ ] `make cockpit` — should show no errors
- [ ] Log founder time in `data/founder_trust_log.jsonl`
- [ ] Close laptop

**Gate Day 0:** Moyasar KYC submitted ✓, Railway env set ✓,
5 names in pipeline ✓, first LinkedIn post scheduled ✓.

---

## Day 1 (Tuesday) — First outbound + first content live

### 07:30 KSA — Morning ritual
- [ ] Full ritual per `FOUNDER_DAILY_RUNBOOK.md` Steps 1-5
- [ ] Approve any test approvals to verify queue UX

### 09:00 KSA — LinkedIn post #1 publishes (automated by LinkedIn UI)
- [ ] Verify it published
- [ ] Pin to profile
- [ ] Reply to first 3 comments within 30 min

### 10:00 KSA — First warm intro DM #1
- [ ] Pick #1 from pipeline_tracker
- [ ] WhatsApp manually (warm consent assumed for warm intros only)
- [ ] Message:
  > السلام عليكم {name}، {personalized reference}. أعمل في Dealix —
  > نظام تشغيل إيرادات للـ B2B السعودي. {one specific reason this
  > matters to them}. لو الموضوع يستحق ١٥ دقيقة، احجز:
  > {calendly_url}. ملاحظة: لا pitch، فقط نقاش.
- [ ] Log: pipeline_tracker → status="dm_sent_day1"

### 14:00 KSA — Inbound triage
- [ ] Check email + LinkedIn + WhatsApp for any replies
- [ ] If Moyasar approval email arrived → proceed to Day 2 prep
- [ ] If LinkedIn post got DMs from prospects → use FAQ bank to
  reply within 30 min

### 17:00 KSA — Evening review
- [ ] Update KNOWN_LIMITATIONS if any new gap surfaced
- [ ] Plan tomorrow's DM #2

**Gate Day 1:** Post #1 live ✓, DM #1 sent ✓, inbound triaged ✓.

---

## Day 2 (Wednesday) — DM #2 + Free Diagnostic prep

### Morning ritual + DM #2 (same pattern as Day 1)

### 11:00 KSA — Free Diagnostic test
- [ ] Open `https://dealix.sa/ar/dealix-diagnostic`
- [ ] Submit a test diagnostic as if you're a prospect
- [ ] Verify the response email arrives
- [ ] Verify the diagnostic shows up in
  `/api/v1/diagnostic/intent`
- [ ] If anything broken → fix before any prospect uses it

### 15:00 KSA — Sprint kickoff prep
- [ ] Open `docs/delivery/client_onboarding/email_sequence/day_0_welcome.md`
- [ ] Make sure your name + Calendly URL merged correctly
- [ ] Save a customized version per known warm intro

---

## Day 3 (Thursday) — Post #2 publishes, DM #3 + follow-up #1

### 09:00 KSA — LinkedIn post #2 publishes
- [ ] Post #2 should be a Counter-narrative (e.g.
  `post_07_no_cold_whatsapp.md`)
- [ ] Verify it published
- [ ] Engage with comments

### 10:00 KSA — DM #3 + Follow-up on DM #1
- [ ] If DM #1 got reply → respond via FAQ bank
- [ ] If DM #1 silent → don't follow up yet (use Day 7 protocol)
- [ ] Send DM #3 to next warm intro

### 14:00 KSA — Moyasar live keys (if approval received)
**Trigger:** if Moyasar email "live mode approved" arrived
- [ ] Copy `MOYASAR_SECRET_KEY` from dashboard
- [ ] Copy `MOYASAR_WEBHOOK_SECRET` from Webhooks tab
- [ ] Railway → Variables → add both
- [ ] Add `DEALIX_MOYASAR_MODE=live`
- [ ] Redeploy
- [ ] Verify: `curl -fs -H "X-API-Key: $ADMIN" \
  https://api.dealix.me/api/v1/pricing/plans | jq '.mode'` → "live"

### 15:00 KSA — Register webhook
- [ ] Moyasar dashboard → Webhooks → Add
- [ ] URL: `https://api.dealix.me/api/v1/webhooks/moyasar`
- [ ] Events: payment_paid, payment_refunded, payment_failed, payment_captured
- [ ] Click Test → should return 200

### 16:00 KSA — First 1-SAR live transaction
- [ ] Open `https://dealix.sa/ar/checkout`
- [ ] Click "تجربة بريال واحد"
- [ ] Enter your real email
- [ ] Pay with your own real card
- [ ] Wait for redirect + receipt email
- [ ] Verify:
  ```bash
  curl -fs -H "X-API-Key: $ADMIN" \
    https://api.dealix.me/api/v1/payment-ops/list?limit=1 | jq .
  ```
- [ ] **First SAR captured** — log in capital_assets.yaml under
  financial_capital

---

## Day 4 (Friday) — Demo prep + Saturday post

### Morning ritual

### 11:00 KSA — Demo preparation
- [ ] Re-read `docs/sales/DEMO_SCRIPT.md`
- [ ] Open `https://dealix.sa/ar/ops/cockpit` to verify it loads
  cleanly
- [ ] Prepare `data/demos/saudi_b2b_demo.csv` (or use existing)

### 14:00 KSA — Follow-up draft #1 for DM #1 (3-day silence)
- [ ] Use `docs/sales/FOLLOW_UP_SEQUENCE.md` Touch 2 (Day 3 nudge)
- [ ] Queue in `approval_center` (NOT sent yet)
- [ ] Approve & send manually

### 17:00 KSA — Saturday LinkedIn post #3 prep
- [ ] Pick a Case-safe pattern post (e.g.
  `post_09_icp_ranking_pattern.md`)
- [ ] Schedule for Saturday 09:00 KSA

---

## Day 5 (Saturday) — Post #3 publishes

### 09:00 KSA — Post #3 publishes
- [ ] Verify
- [ ] Engage with weekend comments (Saudi B2B less active but
  still present)

### 11:00 KSA — Week 1 reflection (45 min)
- [ ] Open `docs/playbooks/FOUNDER_NEXT_STEPS.md`
- [ ] Write 1 paragraph: what worked, what didn't
- [ ] Commit changes to git (founder time + lessons)

---

## Day 6 (Sunday) — Weekly ritual + planning

### 09:00 KSA — Weekly scorecard
- [ ] `python scripts/weekly_scorecard.py`
- [ ] Read `data/scorecards/2026-W22.md`
- [ ] Note any red lines

### 10:00 KSA — Next week planning
- [ ] Schedule 3 LinkedIn posts for week 2
- [ ] Identify next 5 warm intros
- [ ] If any reply from week 1 → block calendar for demo

### 12:00 KSA — Friction review
- [ ] Curl `friction-log` → identify top signal
- [ ] If actionable → file a fix in week 2 plan

---

## Day 7 (Monday) — Week 2 starts

### 09:00 KSA — Full daily ritual
### 14:00 KSA — Follow-up #2 on Day-1 DMs (Day 7 protocol)
- [ ] Use `FOLLOW_UP_SEQUENCE.md` Touch 3 (Day 7 decision)
- [ ] Queue + send manually
- [ ] After 72h silence → mark as nurture (90-day pause)

### 17:00 KSA — Week 1 wrap
- [ ] Update `docs/playbooks/FOUNDER_NEXT_STEPS.md` week-1 results
- [ ] If any prospect converted to demo → prepare per Demo Script
- [ ] If 0 conversions yet → review messaging quality, NOT volume

---

## Success criteria at end of Day 7

Hard criteria:
- [ ] Moyasar live mode active ✓
- [ ] At least 1 SAR captured ✓
- [ ] 3 LinkedIn posts live ✓
- [ ] 5+ warm intro DMs sent ✓
- [ ] 0 doctrine breaches ✓
- [ ] Weekly scorecard generated ✓

Soft criteria (great if hit, not blocking):
- [ ] 1 demo booked
- [ ] 1 Free Diagnostic submitted by a prospect
- [ ] 1 LinkedIn post > 1K impressions
- [ ] Founder hours <50

---

## What if week 1 results are zero?

**Don't panic. The doctrine ensures slow start.**

Most common failure modes in week 1:
1. **DM messaging too generic** → rewrite with more specific
   personalization
2. **LinkedIn post timing wrong** → try Thursday/Saturday instead of
   Tuesday
3. **Warm intros not actually warm** → check the relationship quality
   honestly
4. **FAQ replies feel canned** → personalize harder before paste

Don't change the doctrine. Don't enable autonomous send. Don't
discount.

Iterate on messaging quality, not on speed.

---

## What happens on Day 8+

Move to standard cadence in `FOUNDER_DAILY_RUNBOOK.md`:
- Daily morning + midday + evening ritual
- 3 LinkedIn posts/week
- 1 warm intro DM/day (5-7/week)
- Sprint customers as they appear
- Weekly scorecard every Sunday

The first 7 days are a launch sequence. Day 8+ is the long game.
