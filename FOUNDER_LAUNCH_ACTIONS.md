# Dealix — Founder Launch Actions (Manual Critical Path)

**Owner:** Sami Assiri (founder, sole identity holder)
**Last updated:** 2026-05-22
**Status:** 5 items block `REVENUE VERIFIED`. None can be automated by a repo agent.

This is **not** a daily loop — it's the critical-path checklist. For the daily loop see [`docs/ops/TODAY.md`](docs/ops/TODAY.md). The 11 non-negotiables (`.claude/agents/dealix-pm.md` §Non-negotiables) explicitly forbid automating items 1, 2, 3, and 4 below — manual founder action is doctrine, not limitation.

Do these in order. Each item is self-contained.

---

## 1. Moyasar KYC Activation

**Why:** Unlocks live payments. The single biggest unlock — every other revenue automation depends on it.

**Time:** 30 min to submit + 1-3 business days for Moyasar approval.

**Steps:** Full checklist in [`docs/ops/MOYASAR_KYC_CHECKLIST.md`](docs/ops/MOYASAR_KYC_CHECKLIST.md) (Phase 1, items 1.1-1.9). Highlights:

1. Open https://dashboard.moyasar.com → Settings → Verification.
2. Upload: CR (Sijill Tijari) · National Address (Wasel) · National ID · authorized-signatory letter · corporate Saudi IBAN + bank letter · VAT certificate · business description.
3. Submit and record ticket # in `docs/ops/manual_payment_log.md`.

**Instant unblock (recommended in parallel):** create a Moyasar **sandbox** account → grab the `sk_test_...` key. Send it to me here. I update `MOYASAR_SECRET_KEY` in Railway → full automated round-trip can be verified today with test cards.

**Done when:** Moyasar dashboard shows `Active`, or sandbox key is in Railway env and `bash scripts/moyasar_live_test.sh` returns a working `payment_url`.

**What Claude does next:** put the new key into Railway env, run the 1-SAR test, verify the webhook round-trip, flip `Revenue (Moyasar live) → 🟢 LIVE` in `docs/ops/COMPANY_CONTROL_CENTER.md`.

---

## 2. Sentry DSN

**Why:** Production error tracking. The SDK is already initialised in code; it's idle without a DSN.

**Time:** 5 min. Full steps in [`docs/ops/SENTRY_SETUP.md`](docs/ops/SENTRY_SETUP.md).

**Steps:**

1. Go to https://sentry.io → create org if needed → new project named `dealix` → platform `Python / FastAPI`.
2. Copy the DSN (starts with `https://...@...ingest.sentry.io/...`).
3. Send the DSN to me here.

**Done when:** `SENTRY_DSN` is set in Railway and a test exception appears in the Sentry UI.

**What Claude does next:** add `SENTRY_DSN` to Railway env, trigger `/_test_sentry`, confirm the issue appears in Sentry, update the control-center table.

---

## 3. UptimeRobot Monitor

**Why:** External 5-min uptime check on `api.dealix.me`, independent of Railway.

**Time:** 10 min. Full steps in [`docs/ops/UPTIMEROBOT_SETUP.md`](docs/ops/UPTIMEROBOT_SETUP.md).

**Steps:**

1. https://uptimerobot.com → sign up / log in → Add New Monitor.
2. Type: HTTPS · URL: `https://api.dealix.me/health` · Interval: 5 min · Alert: phone + email.
3. Save.

**Done when:** Monitor shows "Up" with at least one successful check and an alert contact is configured.

**What Claude does next:** flip `Monitoring (UptimeRobot)` to ✅ in `docs/ops/COMPANY_CONTROL_CENTER.md`.

---

## 4. First LinkedIn DMs (Manual Send Only)

**Why:** The acquisition machine runs on warm, personalised, **manually-sent** founder messages. Automating LinkedIn outreach violates non-negotiable #3 and would destroy the founder's account reputation.

**Time:** 3 min per DM. Cap: 5 per hour. Today's queue: 10 ready.

**Steps:**

1. Open [`docs/ops/today_send_queue.md`](docs/ops/today_send_queue.md) — 10 messages already drafted in Arabic, personalised by name/company/affinity.
2. The 5 Tier-A direct messages (DM #1-#5) target:
   - DM #1 — Abdullah Al-Assiri (Lucidya CEO) — surname affinity, highest probability.
   - DM #2 — Ahmad Al-Zaini (Foodics CEO).
   - DM #3 — Nawaf Hariri (Salla CEO).
   - DM #4 — Hisham Al-Falih (Lean Technologies CEO).
   - DM #5 — Ibrahim Manna (BRKZ Founder).
3. The 5 Tier-B agency partner DMs: Peak Content, Digital8, Brand Lounge, Qatar Digital, Wavy Saudi.
4. Copy → open LinkedIn (or WhatsApp for partner targets) → paste → personalise the opening line if needed → send.
5. After each send: update `docs/ops/pipeline_tracker.csv` row with `sent_at` timestamp and channel.
6. If a reply arrives: respond within 30 minutes (cap from `launch_content_queue.md` Execution Rule 5).

**Done when:** at least the 5 Tier-A DMs are sent and logged in `pipeline_tracker.csv`.

**What Claude does next:** when a prospect replies and asks for a Risk Score or Proof Pack, you brief me with the company name → I generate the Proof Pack from real customer data (no fake data, no fabricated metrics — non-negotiable #4).

---

## 5. PostHog Real Key (if still on placeholder)

**Why:** Real analytics from the landing site. Today's value is small; do this last.

**Time:** 5 min.

**Steps:**

1. https://posthog.com → create project `dealix` if missing.
2. Copy the Project API Key (`phc_...`).
3. Send it to me.

**Done when:** `POSTHOG_API_KEY` in Railway is the real key, not a placeholder; first event appears in PostHog.

**What Claude does next:** put it in Railway env, redeploy, verify a test event lands.

---

## After all 5 items are done

Send me a single message: "Founder actions 1-5 complete." I will:

1. Re-run the live API trust probes (`scripts/verify_railway_health.py` etc.).
2. Update `DEALIX_COMPANY_OPERATIONAL_STATE.md` to flip "Revenue (Moyasar live)" → 🟢 LIVE.
3. Update the launch-truth table in that file.
4. Notify you in this conversation when `REVENUE VERIFIED` is reached.

Until then: keep selling via the manual payment path (`docs/ops/MANUAL_PAYMENT_SOP.md`) — that path is fully operational today.

---

## Hard guardrails (do not break)

- **No LinkedIn automation tools.** Sales Navigator search is fine; bots that send DMs are forbidden (non-negotiable #3).
- **No cold WhatsApp blasting.** WhatsApp messages only to people who have opted in or after a LinkedIn handshake (non-negotiable #2).
- **No fake KPIs or seeded "evidence."** Do not log a payment in the evidence tracker that did not actually happen. Doctrine forbids this (non-negotiable #4) — and it corrupts every downstream report.
- **No external action without approval.** Anything Claude sends on your behalf goes through `approval_center` first (non-negotiable #8).
- **Stop on Proof Pack failures.** No paid engagement closes without a Proof Pack with score ≥ 70 + at least one Capital Asset (non-negotiables #10, #11).

---

**Owner contact:** sami.assiri11@gmail.com · WhatsApp/LinkedIn via founder identity.
