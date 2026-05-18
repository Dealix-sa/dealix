# Founder Action Checklist — Sami only | إجراءات المؤسس

**Created:** 2026-05-18 — workstream W5, Commercial Launch Plan (first-paid-pilot track).
**Scope:** ONLY the actions that require the human founder. Everything else is done by the
platform or other workstreams. **North Star:** first PAID pilot delivered + customer-approved
Proof Pack (L3+) — this is also the exit condition of the ACTIVE Commercial Freeze
(`docs/ops/COMMERCIAL_FREEZE.md`).

> The platform is verified sell-ready (gates 0–8 PASS, `DEALIX_READY_FOR_SALES=true`). The
> only thing between Dealix and revenue is the list below. Nothing here can be automated or
> delegated.

---

## P0 — Blocks revenue directly (do first)

### 1. Send the first warm-intro messages
- **What:** Personally send the prepared warm-intro drafts to your warm list. Drafts are
  prepared by another workstream and live in `docs/ops/launch_content_queue.md` /
  `docs/ops/today_send_queue.md`. You review, approve, and send from your own identity.
- **Why it blocks revenue:** Zero outreach sent = zero pipeline = zero pilot. This is the
  single highest-leverage action; the platform cannot send for you (no cold automation by
  doctrine).
- **Time:** ~30–45 min to review + send 5–10 messages.

### 2. Conduct the diagnostic calls (rung 0 — Free AI Ops Diagnostic)
- **What:** Take the discovery calls that result from the intros. Use
  `docs/sales/DISCOVERY_SCRIPT.md`. Goal: qualify one prospect into a paid rung-1 pilot.
- **Why it blocks revenue:** The diagnostic is the bridge from intro to a paid Sprint. No
  call → no pilot.
- **Time:** ~30 min per call.

### 3. Approve outbound drafts before they leave
- **What:** Any external message (email/WhatsApp/LinkedIn) routes through the approval
  step. You are the approver. Review content + recipient, then approve.
- **Why it blocks revenue:** By doctrine no external send happens without founder approval;
  unapproved drafts sit idle and the motion stalls.
- **Time:** ~5 min per batch.

---

## P1 — Required for a clean paid pilot (do this week)

### 4. Moyasar account activation / KYC
- **What:** Complete the KYC submission in `docs/ops/MOYASAR_KYC_CHECKLIST.md` (Phase 1):
  CR, national address, ID, signatory letter, corporate bank IBAN, VAT certificate,
  business description; submit at dashboard.moyasar.com → Settings → Verification.
- **Why it blocks revenue:** Live payments currently fail with `account_inactive_error`.
  No activation → cannot charge a real customer → cannot close a paid pilot in production.
- **Test-key option (do NOT wait on KYC to verify the flow):** Set `MOYASAR_SECRET_KEY`
  to a Moyasar **`sk_test_`** key in a non-production env. This exercises the full
  payment → delivery → audit-link path with **no real money** — so the rung 0–1 delivery
  finish can be proven now, while KYC is in the 1–3 business-day approval window.
  Live cutover stays founder-flipped only (`MOYASAR_MODE=production` + `sk_live_`).
- **Time:** ~1–2 h to gather documents + submit; then 1–3 business days for Moyasar approval.

### 5. Set SENTRY_DSN
- **What:** Create the Sentry project, copy the DSN, set it as a Railway env var.
  See `docs/ops/SENTRY_SETUP.md`.
- **Why it blocks revenue:** Without error monitoring, a silent failure during the first
  paid pilot (e.g. a dropped payment webhook) goes unseen — risking the pilot and the
  Proof Pack.
- **Time:** ~15 min.

### 6. Create the UptimeRobot monitor
- **What:** Add an UptimeRobot monitor on `https://api.dealix.me/healthz` with alert
  contact. See `docs/ops/UPTIMEROBOT_SETUP.md`.
- **Why it blocks revenue:** A backend outage during a pilot demo or payment kills trust;
  the monitor gives early warning.
- **Time:** ~10 min.

---

## How to know you are done

All six items closed **and** one paid pilot delivered with a customer-approved Proof Pack
(L3+). At that point the Commercial Freeze ends and the next 90-day plan governs
(`docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`).

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
