# Founder Daily Runbook · دليل الفاوندر اليومي

> The exact ritual the founder follows every operating day. Bilingual.
> Doctrine-anchored. Updated when a friction signal shows up.
>
> **Effective:** 2026-06-01 · **Time required:** 30-45 min/day

---

## 🌅 Morning Ritual · طقس الصباح (07:30 KSA · 25 min)

### Step 1 — Health pulse (2 min)
```bash
curl -fs https://api.dealix.me/health
curl -fs https://dealix.sa/                   # frontend up?
```
Both must return 200. If not → page on-call (you).

### Step 2 — Cockpit scan (5 min)
```bash
make cockpit                                  # CLI version
# OR open: https://dealix.sa/ar/ops/cockpit
```

7 panels in order:
1. **Revenue today** — is there a paid txn since 00:00? log if yes.
2. **MRR current** — has it moved vs yesterday's snapshot?
3. **Pending approvals** — open `/api/v1/approvals/pending`
4. **Friction signals 7d** — is any new code recurring?
5. **Fleet activity 24h** — did agents run? if 0, check cron.
6. **Renewals due** — any subscription needing your confirmation today?
7. **Next action** — what does business_now recommend?

If the red-lines banner is non-empty: address **before anything else**.

### Step 3 — Approval queue (10 min)
Open `/api/v1/approvals/pending` (or
`/ar/ops/approvals` UI).

For each pending item:
- Read the proposed message
- Check recipient context (last interaction, ICP fit)
- One of: **approve / edit / reject** with reason
- Target: queue empty by 09:00 KSA

**Doctrine:** if you don't have time to review, the queue stays. NEVER
bulk-approve without reading. NEVER mark "approve all" if you skim.

### Step 4 — 1 warm-intro DM (5 min)
Open WhatsApp or LinkedIn (manually, no automation).
Pick ONE warm intro from `docs/ops/pipeline_tracker.csv` filtered to
"awaiting first DM".
Send a personal message — no template. Reference something specific
about their company.
Log: update `pipeline_tracker.csv` → `last_status_change` + reason.

### Step 5 — Sprint customer block (~3 min status check)
If you have an active Sprint customer:
```bash
curl -fs -H "X-API-Key: $ADMIN" \
  https://api.dealix.me/api/v1/sprint/$SPRINT_ID/checklist | jq '.current_step, .steps[].status'
```
Confirm yesterday's deliverable was marked done. If not, mark it now
with the evidence_link.

---

## 🌞 Midday Commercial Review · المراجعة التجارية وقت الظهر (13:00 KSA · 15 min)

### Step 6 — Pipeline movement (5 min)
Open `docs/ops/pipeline_tracker.csv`.
For each row: did `reply_status` change since this morning?

Three buckets:
- **Replied positive** → next action: book demo (record in
  approval_center as draft)
- **Replied objection** → check
  `docs/sales/OBJECTION_HANDLING.md` for matching script
- **No reply 5+ days** → queue Day-3 or Day-7 follow-up draft

### Step 7 — Friction log review (3 min)
```bash
curl -fs -H "X-API-Key: $ADMIN" \
  https://api.dealix.me/api/v1/friction-log | jq '.top_signals'
```
For each new signal:
- Was it a real friction or a false positive?
- If real: log in `docs/reference/KNOWN_LIMITATIONS.md` if not there
- If false positive: file a fix issue

### Step 8 — Inbound triage (7 min)
Email + WhatsApp + LinkedIn DMs.
SLA: respond within 30 min during business hours.

For each:
- Customer existing → handle directly
- Prospect new → check
  `docs/playbooks/FAQ.md` for the matching answer, paste, personalize
- Spam → archive
- Press / partnership inquiry → flag in pipeline_tracker for tomorrow

---

## 🌙 Evening Trust Review · مراجعة الثقة المسائية (18:00 KSA · 10 min)

### Step 9 — No-overclaim audit (3 min)
Open `dealix/registers/no_overclaim.yaml`.
Did any claim today move from `Pilot` → `Production` status?
If yes: verify the proof_ledger has the supporting events. If not:
move back to `Pilot`.

### Step 10 — Doctrine attestation (2 min)
Did any decision today push against a doctrine non-negotiable?
- "Was tempted to autonomous send" → log + commit to keep approval
- "Considered cold WhatsApp" → log + reassign as warm intro track
- "Wanted to invent a metric for Twitter" → log + use is_estimate

The log is `data/founder_trust_log.jsonl` (gitignored). Honest
review only.

### Step 11 — Tomorrow's queue (5 min)
What's the ONE thing tomorrow must include?
- If Sprint customer day-N → log it
- If LinkedIn post Tuesday → confirm draft ready
- If demo booked → review prep
- If nothing scheduled: pick 1 from `docs/playbooks/FOUNDER_NEXT_STEPS.md`

Close laptop. Doctrine #1: do not check WhatsApp after 22:00 unless
emergency.

---

## 📅 Weekly Ritual · الطقس الأسبوعي (Sunday 09:00 KSA · 30 min)

1. **Weekly scorecard:** `python scripts/weekly_scorecard.py` → read
   `data/scorecards/YYYY-WW.md`
2. **Top friction signals:** identify the #1 friction this week. What
   one fix would eliminate it?
3. **Content cadence:** confirm 3 LinkedIn posts scheduled (Tue/Thu/Sat
   09:00 KSA). Use `docs/sales-kit/linkedin_posts/INDEX.md`.
4. **KPI dashboard refresh:** copy `metrics:` block from latest
   scorecard into `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` Week-by-week
   table.
5. **Capital ledger update:** new proof events at L4+ this week →
   add to `dealix/registers/capital_assets.yaml` (founder writes; no
   automation).

---

## 📆 Monthly Ritual · الطقس الشهري (Last Friday 16:00 KSA · 2 hours)

1. **30-60-90 plan check:** open
   `docs/playbooks/FOUNDER_NEXT_STEPS.md`. Update which milestones hit,
   which slipped, why.
2. **Customer NPS rollup:** for each active customer, run
   `/api/v1/nps/{customer_handle}/summary`. Any below 7 → schedule
   recovery call.
3. **Renewal preparation:** for each subscription month-end this month,
   review the customer's proof events. Send the renewal confirmation
   email draft (NOT autosent) 7 days before charge.
4. **Refund audit:** any refund requests this month? Were they handled
   per `docs/contributing/REFUND_POLICY.md`?
5. **Quarterly compliance review (if last Friday of quarter):** PDPL
   posture, ZATCA receipt sample audit, retention deletion run.

---

## 🚨 Emergency Procedures · إجراءات الطوارئ

### If a doctrine non-negotiable was broken:
1. **STOP** all outbound immediately
2. Log in `data/incidents/INC-{date}.md` with what happened
3. Notify any affected customers within 24h
4. Don't resume until written postmortem completed

### If Moyasar webhook stops delivering:
1. Check Moyasar dashboard → webhook tab → recent deliveries
2. If failing: rotate the webhook secret (regenerate on Moyasar +
   update Railway env)
3. Replay missed events via `POST /api/v1/webhooks/moyasar/replay`
4. Customer receipts: re-issue manually within 24h

### If a customer complaint goes public:
1. Read the full thread before responding
2. Apologize once, factually, in 24h
3. Propose remediation within 48h
4. Postmortem within 7 days, published with permission
5. Update doctrine if the complaint exposed a real gap

### If you receive a regulatory notice (SDAIA / CITC / ZATCA):
1. **Do not respond directly without legal review**
2. Email `legal@dealix.me` (or your Saudi lawyer) within 24h
3. Pause any related automation
4. Document the notice + response in
   `docs/registers/compliance_saudi.yaml#regulatory_notices`

---

## 📊 Metrics the founder watches daily

| Metric | Source | Target | Red line |
|--------|--------|--------|----------|
| Revenue today (SAR) | cockpit | > 0 on operating days | 0 SAR for 7 consecutive days |
| MRR (SAR) | cockpit | growing month-over-month | declining 2+ months |
| Pending approvals | cockpit | < 10 by 09:00 | > 20 at any time |
| Friction signals (7d) | cockpit | trending down | spike > 30 in a week |
| Customer NPS avg | `/api/v1/nps` | > 8 | < 7 |
| Founder hours/week | manual log | < 35 by month 3 | > 50 for 2+ weeks |

---

## 🎯 The single founder discipline

> **"If I cannot read a message before it sends, it does not send."**

This single rule resolves 90% of ambiguous situations. When in doubt
about approving an autonomous flow, re-read this sentence.

The other rules are decorations. This is the trunk.

---

**Updates:** this runbook evolves. Date every change in
`docs/playbooks/FOUNDER_NEXT_STEPS.md#changelog`.
