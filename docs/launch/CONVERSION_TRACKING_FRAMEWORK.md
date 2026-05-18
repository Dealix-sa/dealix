# Conversion Tracking Framework — إطار تتبّع التحويل

> Phase F deliverable. How first-revenue progress is tracked: funnel stages,
> the 90-day MRR arc, the weekly cadence, and the friction-log review.
> This is a **framework the founder fills as real deals move** — every number
> below starts empty. No metric here is fabricated. No real customer exists yet.

---

## 1. The funnel — مراحل القمع

| Stage | Definition | Source of truth |
|---|---|---|
| Landing | Visitor reached the landing page. | Web analytics |
| Free Diagnostic | Tier 0 intake submitted; 24h clock running. | Diagnostic intake log |
| 499 Sprint | Tier 1 proposal accepted; first invoice cleared. | `docs/ops/pipeline_tracker.csv` (stage=Paid) |
| Pilot | Sprint delivered; Proof Pack assembled + customer-approved L3+. | `PROOF_LEDGER.md` / `DELIVERY_LEDGER.md` |

Stage definitions are consistent with the pipeline stages in
`docs/sales-kit/founder-sales-pack/04_FOUNDER_DAILY_CADENCE.md` §2 — this
framework rolls those operational stages into the four revenue-relevant ones.

---

## 2. The funnel scoreboard — لوحة القمع

Founder fills weekly. Counts are cumulative unless noted. Start = 0.

| Stage | Week 1 | Week 2 | Week 3 | Week 4 | … |
|---|---|---|---|---|---|
| Warm drafts sent | | | | | |
| Replies received | | | | | |
| Discovery calls held | | | | | |
| Free Diagnostics delivered | | | | | |
| 499 Sprints sold (paid) | | | | | |
| Pilots delivered (Proof Pack L3+) | | | | | |

**Conversion ratios** (compute from the row above; watch for the biggest drop):
- Drafts → replies
- Replies → calls
- Calls → Diagnostics
- Diagnostics → paid Sprint
- Sprint → completed Pilot

---

## 3. The 90-day MRR arc — قوس الإيراد لـ90 يوماً

The intended revenue progression. These are **targets, not results** — the
founder records actuals against them. The arc is sequential: each milestone
unlocks the credibility for the next.

| Milestone | Target | Records as | Status (founder fills) |
|---|---|---|---|
| M1 — First 499 Sprint | First Tier 1 invoice cleared | One-time 499 SAR | ☐ Not yet |
| M2 — First 1,500 Data Pack | First Tier 2 project sold | One-time 1,500 SAR | ☐ Not yet |
| M3 — First Managed Ops retainer | First Tier 3 customer signed | Recurring MRR (2,999–4,999/mo) | ☐ Not yet |
| M4 — ~15,000 SAR MRR | Stacked Managed Ops retainers | Recurring MRR | ☐ Not yet |

**Pilot trigger overlay:** three proven paid pilots (per
`docs/launch/FREEZE_LIFT_CONDITION.md` §3) unlock Tier 2+ build. Track the
pilot count alongside MRR — it gates what may be built.

| | Count (founder fills) |
|---|---|
| Proven paid pilots banked | 0 / 3 |
| Freeze status | ACTIVE |

---

## 4. Weekly cadence — الإيقاع الأسبوعي

Runs inside the Thursday 30-minute review already defined in
`04_FOUNDER_DAILY_CADENCE.md` §8. Each Thursday the founder:

1. Updates the §2 funnel scoreboard with the week's real counts.
2. Computes the §2 conversion ratios; names the single biggest drop-off.
3. Updates the §3 MRR arc with any milestone reached.
4. Runs the §5 friction-log review.
5. Decides **one** change to test next week — script, offer framing, or target
   segment. One change, not a list.

---

## 5. Friction-log review — مراجعة سجلّ الاحتكاك

The daily wrap (cadence Block F) writes one paragraph to the friction log:
messages sent, replies, the day's biggest verbatim objection (anonymized), and
one change or "no change." The weekly review reads the last 7 entries and:

- Identifies any **high-severity** friction (a repeated blocking objection, a
  doctrine-pressure request, a payment-path failure) and escalates it per the
  runbook §5 escalation table.
- Looks for the **first sector pattern** — a recurring objection or need across
  contacts in one segment. That pattern is a Capital Ledger asset candidate.
- Confirms no PII leaked into the log (non-negotiable #6).

Aggregate review (programmatic, when the internal log is wired):
`python -c "from auto_client_acquisition.friction_log.aggregator import aggregate; print(aggregate(customer_id='dealix_internal', window_days=14).to_dict())"`

---

## 6. Rules for this scoreboard — قواعد اللوحة

- **No fabricated numbers.** Every cell is blank until a real event fills it.
- **Paid means cleared**, not invoiced — funds received and reconciled.
- **A pilot counts** only if it meets all 7 criteria in `FREEZE_LIFT_CONDITION.md` §3.
- **Never report a metric that implies a real customer outcome when none exists.**
- Honest status always — a stalled week is recorded as stalled.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
