# Founder Launch Operating Runbook — دليل تشغيل الإطلاق للمؤسس

> Phase E deliverable. One concise runbook for running the Paid Private Beta.
> It does not duplicate the daily cadence — that lives in
> `docs/sales-kit/founder-sales-pack/04_FOUNDER_DAILY_CADENCE.md` and is
> cross-referenced here. This runbook covers what *runs* the launch.

---

## 1. What runs the launch — ما الذي يُشغّل الإطلاق

Three machines, in sequence. Nothing here is autonomous; the founder approves
every external step.

**A. The funnel**
`Landing → Free Diagnostic (Tier 0) → 499 Sprint (Tier 1) → Pilot.`
The narrative is the *governed revenue-operations radar*: approval-first,
drafts-only, Proof-backed. Entry offer is the 499 SAR Revenue Intelligence
Sprint. No legacy "1 SAR / 45-second AI sales rep" framing anywhere.

**B. The payment path (interim — manual evidence)**
Moyasar API is inactive until KYC clears. Until then, every payment runs the
manual evidence path in `docs/ops/MANUAL_PAYMENT_SOP.md`:
1. Customer says yes → send a manual HTML/PDF invoice by email.
2. Customer pays via bank transfer, STC Pay, or a Moyasar hosted invoice.
3. Founder receives bank notification, reconciles, logs payment in
   `docs/ops/pipeline_tracker.csv` (stage=Paid) and `docs/ops/manual_payment_log.md`.
4. Onboard manually per `docs/ops/FIRST_CUSTOMER_ONBOARDING_CHECKLIST.md`.
When Moyasar KYC clears, run `python scripts/moyasar_live_cutover.py` and
confirm `launch-status` reports `moyasar.mode == "live"` before the next
proposal. Manual path is valid for the first 10 customers.

**C. Proof Pack delivery (email)**
On engagement close, assemble the 14-section Proof Pack (score ≥ 70, ≥ 1
Capital Asset), render to HTML/PDF, and email it to the customer. Reference
template: `clients/_TEMPLATE/06_proof_pack.md`. Record the delivery in
`docs/ledgers/DELIVERY_LEDGER.md` and `docs/ledgers/PROOF_LEDGER.md`. Request
explicit customer approval at evidence level L3+ — this is the artifact that
counts toward the freeze-lift condition.

---

## 2. Operating cadence — الإيقاع التشغيلي

The **daily and weekly sales rhythm is defined in
`docs/sales-kit/founder-sales-pack/04_FOUNDER_DAILY_CADENCE.md`** — pipeline
review, draft-approval block, follow-ups, discovery calls, qualify-and-propose,
daily wrap. Run that file as-is. Do not duplicate it.

This runbook adds only the **launch-specific** overlays:

| Frequency | Launch overlay (in addition to the cadence) |
|---|---|
| Daily | After Block F wrap, update the conversion scoreboard in `docs/launch/CONVERSION_TRACKING_FRAMEWORK.md`. |
| Daily | If a proposal goes out, confirm payment path: manual SOP if Moyasar still in test. |
| Weekly (Thu) | During the cadence's 30-min review, also run the friction-log review and check progress against the 90-day MRR arc. |
| Per close | Assemble + email Proof Pack; record in DELIVERY + PROOF ledgers; seek L3+ approval. |
| Per pilot | Check it against the 7 "proven paid pilot" criteria in `docs/launch/FREEZE_LIFT_CONDITION.md` §3. |

---

## 3. Paid Private Beta rules — قواعد الإطلاق الخاص المدفوع

1. **Real customers only.** No friends-test, no discount-to-zero. A pilot that
   does not count toward the freeze-lift trigger is not a beta customer.
2. **Sell only the active ladder:** Tier 0 (Free Diagnostic), Tier 1 (499
   Sprint), Tier 2 (1,500 Data Pack), Tier 3 (Managed Ops). Tiers 2–5 are sold
   but **not built** — the Commercial Freeze is active. Never promise Tier 2+
   automation that does not exist; deliver founder-assisted.
3. **Manual payment path** until Moyasar KYC clears. Cap: first 10 customers.
4. **Drafts-only, approval-first.** Every outreach message and every proposal is
   a draft the founder reads and approves before it leaves their hands. No
   automated sends. No scraped or purchased lists.
5. **No guaranteed outcomes.** State methodology metrics only — never "we will
   close X deals" or "guaranteed revenue."
6. **Every output carries `governance_decision`.** Every customer-facing
   markdown ends with the bilingual disclaimer.
7. **No project closure without** a 14-section Proof Pack (score ≥ 70) and at
   least one Capital Ledger asset.
8. **Honor all 11 non-negotiables** (sales-pack README §non-negotiables). If a
   request needs a violation, refuse cleanly and offer the safe alternative.

---

## 4. Where the founder approves outreach — أين يعتمد المؤسس التواصل

- **Outreach drafts:** approved in **Block B** of the daily cadence — the
  founder personalizes up to 5 warm drafts/day from
  `01_WARM_OUTREACH_FRAMEWORK.md`, reads each as the recipient, self-approves,
  and sends **manually** on the channel the relationship already uses.
- **Proposals:** approved in **Block E** — `qualify(...)` returns a decision,
  the matching proposal from `03_PROPOSAL_TEMPLATES.md` is rendered, and the
  founder gives it a final review before sending.
- **System-routed sends** (if any go through the platform) pass `approval_center`
  first — logged with identity + timestamp. Transactional confirmations are
  pre-whitelisted; all outreach requires explicit approval.
- **Hard limits:** max 5 new outreach drafts/day, max 3 discovery calls/day.

---

## 5. Escalation — التصعيد

| Situation | Action |
|---|---|
| Moyasar KYC clears | Run `moyasar_live_cutover.py`; verify live mode. |
| A doctrine non-negotiable would be violated | Refuse, log in friction log, offer safe alternative. |
| First proven paid pilot closed | Apply `FREEZE_LIFT_CONDITION.md` §3; freeze lifts. |
| Revenue clearly stalling vs the 90-day arc | Stop any building; double down on the sales cadence. |
| High-severity friction signal | Surface in the Thu weekly review; decide one change. |

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
