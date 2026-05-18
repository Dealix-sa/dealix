# Commercial Activation — 30 / 60 / 90 Operating Plan
# خطة تشغيل التفعيل التجاري — ٣٠ / ٦٠ / ٩٠ يوماً

<!-- Workstream H | Owner: Founder | Last reviewed: 2026-05-18 -->
<!-- Planning/ops document. Proposes no new product features. Respects the Commercial Freeze. -->

> **EN.** This is the operating plan for the Commercial Activation Program — the
> program turning the already-shipped, already-verified Dealix platform into a
> founder-approved revenue motion. It does not set new targets: every number
> below is lifted unchanged from
> [`../../dealix/registers/90_day_execution.yaml`](../../dealix/registers/90_day_execution.yaml)
> and [`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md).
> All targets are goals, not guarantees.
>
> **AR.** هذه خطة تشغيل برنامج التفعيل التجاري — البرنامج الذي يحوّل منصة Dealix
> الجاهزة والمُتحقَّق منها إلى حركة إيراد تعمل بموافقة المؤسس. لا تضع أهدافاً
> جديدة: كل رقم أدناه منقول كما هو من المصفوفة التنفيذية وخطة الـ٩٠ يوماً.
> كل الأهداف غايات، لا ضمانات.

---

## 0. Frame — الإطار

The platform constraint is no longer code; it is **founder-led selling**. The
Commercial Freeze ([`COMMERCIAL_FREEZE.md`](COMMERCIAL_FREEZE.md)) redirects all
effort from building to operating and selling, until the first paid pilot proves
the motion. This plan governs that motion's rhythm and decision gates.

القيد لم يَعُد الكود — بل البيع بقيادة المؤسس. التجميد التجاري يحوّل الجهد من
البناء إلى التشغيل والبيع حتى يُثبت أول Pilot مدفوع أن الحركة تعمل.

The offer ladder this plan moves customers along
([`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)):

| # | Offer | Price (SAR) | Freeze status |
|---|-------|-------------|---------------|
| 0 | Free AI Ops Diagnostic | 0 | Delivery-finish permitted |
| 1 | 7-Day Revenue Proof Sprint | 499 | Delivery-finish permitted |
| 2 | Data-to-Revenue Pack | 1,500 | **Frozen** |
| 3 | Managed Revenue Ops | 2,999–4,999 / mo | **Frozen** |
| 4 | Executive Command Center | 7,500–15,000 / mo | **Frozen** |
| 5 | Agency Partner OS | Custom + rev-share | **Frozen** |

During the freeze the program sells and delivers **rungs 0–1 only**. Rungs 2–5
are *marketed* but no new build for them ships. See §4 (Freeze-Lift Gate).

---

## 1. 30 / 60 / 90 Milestones — محطات ٣٠ / ٦٠ / ٩٠

All figures are the goal / minimum pairs already recorded in the source plans.
Where the plan records "goal" and "minimum (الحد الأدنى)", both are shown.

### Day 30 — First paid Sprint sold and delivered
**اليوم ٣٠ — بيع وتسليم أول Sprint مدفوع**

The single milestone that matters: **one paid 499 SAR 7-Day Revenue Proof Sprint
closed, delivered, and its Proof Pack assembled.** This is also the
Commercial Freeze exit condition (see §4).

| Metric | Goal | Minimum |
|--------|------|---------|
| Warm intros sent | 5 | 3 |
| Diagnostics run (rung 0) | 6 | — |
| Demos run | 6 | — |
| Pilots delivered (rung 1) | 2 | 1 (with decision date) |
| Proof Events documented | 3 | 1 |
| Case studies ready | 1 | — |
| Sprint revenue | 998 SAR (2 × 499) | 499 SAR |
| MRR | 998 SAR | 499 SAR |

Day-30 done = **at least one paid pilot delivered + one Proof Pack at evidence
level L3 or above.** Until that exists, the freeze stays on and the program does
not move to rung-2 work.

### Day 60 — A small ramp of Sprints + first Proof Packs
**اليوم ٦٠ — نمو محدود في الـ Sprints + أول حِزم إثبات**

| Metric | Goal | Minimum |
|--------|------|---------|
| Demos run (cumulative) | 12 | — |
| Pilots delivered (cumulative) | 5 | 3 |
| Proof Events documented | 8 | 1 |
| Managed Ops clients (rung 3) | 2 | 1 |
| MRR | 5,998 SAR (2 × 2,999) | 2,999 SAR |
| Case studies | 2 | 1 |
| Agency partner conversations | 2 | 1 |

Day-60 note: Managed Ops (rung 3) appears in the 60-day numbers **only if** the
freeze-lift gate has already cleared (§4) and the rung-1→3 decision gate (§3)
passes. If the freeze has not lifted by Day 60, the MRR for the period is
Sprint-only and the program escalates per the §5 decision rule.

### Day 90 — Ramp toward the 90-day MRR targets
**اليوم ٩٠ — التقدّم نحو أهداف الإيراد لـ ٩٠ يوماً**

| Metric | Goal | Minimum |
|--------|------|---------|
| Total customers (Sprint + Managed) | 10 | 7 |
| Demos run (cumulative) | 20 | — |
| Pilots delivered (cumulative) | 10 | — |
| Proof Events documented (cumulative) | 15 | — |
| Managed Ops retainers (rung 3) | 3 | 2 |
| MRR | 8,997–14,997 SAR | 5,998 SAR |
| Case studies published (with consent) | 2–3 | 1 |
| Agency lead source live | 1 | 0 |
| Customer satisfaction | ≥ 4.2 / 5 | ≥ 3.8 / 5 |

These are the targets in [`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md)
§"ملخص KPIs 90 يوم" and Phase 4. No number here is invented; any metric not yet
achieved is reported as `insufficient_data`, never estimated.

---

## 2. Weekly Operating Cadence — الإيقاع التشغيلي الأسبوعي

The cadence runs on the WS-E daily founder-approved autopilot
([`WS-E_AUTOPILOT_NOTES.md`](WS-E_AUTOPILOT_NOTES.md)). Every step prepares and
queues work; **nothing auto-sends** — `revenue-machine/run` is pinned to
`approval_mode: draft_only`, and only an explicit founder approval triggers a
send.

### Daily — يومياً

| When (KSA) | Cycle | What it produces | Founder action |
|------------|-------|------------------|----------------|
| 07:00 | Morning digest (`daily-revenue-machine.yml`) | Today's drafts, follow-ups due, approval-queue pending count (both stores), overdue approvals, revenue-vs-target | Review the approval queue; approve / edit / reject each draft |
| 19:00 | Evening digest (`daily-evening-digest.yml`) | What was approved/sent today, what closed, tomorrow's setup | Confirm close-of-day scorecard; note friction |
| 08:00 Sun | Weekly review (`weekly-review.yml`) | Friction-log review, readiness re-check (`verify_dealix_ready.py`, `verify_governance.py`) | Run the weekly review (below) |

### Weekly review — the founder's Sunday loop

Each Sunday the founder reviews five surfaces. This is the program's heartbeat;
skipping it is a process incident.

1. **Pipeline.** Diagnostics booked, demos run, pilots in flight, decision dates
   due. Compare against the milestone table in §1 for the current period.
2. **Approval queue.** Backlog and **overdue** count. The queue is currently two
   stores — `approval_center` (`GET /api/v1/approvals/pending`) and the
   per-channel draft tables (`dashboard/revenue-machine/today →
   approval_queue_open`); the morning digest aggregates both and labels each
   source. Target: zero items overdue (past `expires_at`).
3. **Friction log.** Review per §6 — top items by severity, recurring blockers.
4. **Readiness.** Output of `verify_dealix_ready.py` + `verify_governance.py`.
   Any red gate is a P0/P1 hotfix candidate (permitted under the freeze).
5. **Revenue vs. target.** Cumulative MRR and one-time against the §1 milestone
   for the current 30/60/90 period. Honest status only — `insufficient_data`
   for anything not yet measured.

Weekly review output: a 5-line status (phase / pipeline / approval health /
top-3 friction / next 1–3 actions) and any blocker needing a founder decision.

المراجعة الأسبوعية تغطّي خمسة أسطح: الـ pipeline، طابور الاعتماد، سجل الاحتكاك،
الجاهزية، والإيراد مقابل الهدف. تخطّيها حادثة عملية.

---

## 3. Decision Gates Between Ladder Rungs — بوّابات القرار بين درجات السلم

The ladder's golden rule: **each rung unlocks only after documented proof from
the rung below.** No upgrade before a documented result. These gates are
go / no-go checkpoints, evaluated at the weekly review.

| Gate | From → To | GO condition | NO-GO action |
|------|-----------|--------------|--------------|
| **G0** | Rung 0 → Rung 1 | Diagnostic delivered; 3 priorities surfaced; customer accepts a Sprint scope and a decision date is set | Re-qualify or close; log demand signal; do not discount |
| **G1 (Freeze-Lift)** | Rung 1 → Rung 2+ | First paid Sprint **delivered** AND its **Proof Pack exists at L3+** | Freeze stays ON; all effort stays on rungs 0–1 (see §4) |
| **G2** | Rung 1 → Rung 3 (Managed Ops) | Freeze lifted (G1 passed); Sprint customer has a documented Proof Event; founder capacity confirmed (founder-assisted delivery sustainable, see §5 capacity rule) | Stay at Sprint cadence; re-offer Managed Ops next cycle |
| **G3** | Rung 3 → Rung 4 (Command Center) | **3 pilots** delivered with Proof Packs; retainer demand recorded from a named contact | Do not market rung 4; record the demand signal only |
| **G4** | Rung 3/4 → Rung 5 (Agency Partner OS) | **3 documented Proof Packs**; `repeated_pilot_demand` satisfied (two independent `pilot_intro_requested` signals) | Do not build a partner kit; log signals in the War Room |

Every gate is evaluated against **recorded evidence**, not belief. If a "signal"
is only a belief, run [`../sales-kit/L4_TRUTH_CHECK.md`](../sales-kit/L4_TRUTH_CHECK.md)
first. Build-on-demand for any sales asset is governed by
[`../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md):
no signal → no build, and a signal never justifies a new product feature, API,
or dashboard.

---

## 4. The Freeze-Lift Decision Gate — بوّابة رفع التجميد

**This is the program's most important gate. State it plainly:**

> **EN.** The Commercial Freeze lifts — and building service tiers 2–5
> (Data-to-Revenue Pack, Managed Revenue Ops, Executive Command Center, Agency
> Partner OS) becomes permitted — **ONLY after BOTH conditions hold:**
> 1. The **first paid pilot has been delivered** (a real 499 SAR 7-Day Revenue
>    Proof Sprint, completed end-to-end), AND
> 2. **Its Proof Pack exists** and is **customer-approved at evidence level L3
>    or above.**
>
> Until both are true, the freeze stays ACTIVE. No rung-2–5 feature PR, no new
> router/endpoint, no new product/architecture doc, no new dashboard ships. The
> only permitted work is founder-led selling, rung 0–1 delivery finish, P0/P1
> hotfixes, ledger recording, and capped build-on-demand sales assets.
>
> **AR.** يُرفع التجميد التجاري — ويُسمح ببناء درجات الخدمة ٢–٥ — **فقط بعد
> تحقّق الشرطين معاً:**
> 1. **تسليم أول Pilot مدفوع** (Sprint ٤٩٩ ريال حقيقي مكتمل من البداية للنهاية)،
> 2. **ووجود حزمة الإثبات (Proof Pack) الخاصة به** معتمدةً من العميل عند مستوى
>    دليل L3 فأعلى.
>
> حتى يتحقّق الشرطان، يبقى التجميد فعّالاً ولا يُشحن أي بناء جديد للدرجات ٢–٥.

**Cross-references — مراجع:**
- [`COMMERCIAL_FREEZE.md`](COMMERCIAL_FREEZE.md) — "Exit" / "الخروج من التجميد":
  *"the freeze ends when one paid pilot is delivered and its Proof Pack is
  customer-approved (evidence level L3 or above)."*
- [`../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md)
  §3 "What ends the freeze" — same exit condition; until then every build
  passes the conditional-build gate.

**On lift.** When G1 clears, the founder records the decision in
[`../ledgers/DECISION_LEDGER.md`](../ledgers/DECISION_LEDGER.md), and the next
90-day plan governs what unlocks. Lifting the freeze does **not** auto-open
rungs 2–5 — each still passes its own gate (G2/G3/G4 in §3) on documented proof.

**Verification before declaring G1 passed:** the Proof Pack must be a real
assembled artifact (not a draft), customer-approved, L3+. The weekly readiness
check (`verify_governance.py`) and the friction log must show **zero doctrine
violations** associated with the pilot delivery.

---

## 5. Decision Rules — قواعد القرار

Evaluated at the weekly review alongside the §3 gates.

- **If first paid pilot is delivered + Proof Pack L3+ exists →** clear G1; the
  freeze lifts; proceed to the post-freeze 90-day plan and the §3 gates.
- **If MRR is materially behind the §1 minimum for the current period (e.g.
  Day 60 with no paid pilot) →** stop preparing any rung-2+ work; double down on
  the sales motion — warm-list re-engagement, diagnostic→Sprint conversion,
  content cadence. Surface this honestly to the founder; do not inflate.
- **If founder delivery time per Sprint exceeds a sustainable load after the
  early customers →** halt new Sprint sales and escalate sprint-delivery
  friction to the top of the weekly review. Do not sell capacity that does not
  exist. (Note: sprint *automation* is a rung-2–5-adjacent build — it stays
  frozen; the response is to slow sales, not to build.)
- **If any of the 11 non-negotiables would be violated by an in-flight request
  or work item →** refuse the work and propose the safe alternative. Never
  improvise around a non-negotiable: no scraping, no cold WhatsApp automation,
  no LinkedIn automation, no un-sourced claims, no guaranteed outcomes, no PII
  in logs, no source-less answers, no external action without approval, no
  agent without identity, no project without a Proof Pack, no project without a
  Capital Asset.

---

## 6. Friction-Log Review Rhythm — إيقاع مراجعة سجل الاحتكاك

**Capture (continuous).** Friction is logged as it occurs — by the founder
during selling/delivery and by the daily autopilot. Anything that slowed a
deal, a delivery, an approval, or a readiness check is a friction event with a
severity (high / medium / low) and a source reference.

**Review (weekly).** The `weekly-review.yml` workflow runs the friction-log
review every Sunday (08:00 KSA) as part of the §2 weekly loop. The founder:

1. Reads the aggregated friction events from the last 14 days.
2. Surfaces every **high-severity** item as an escalation in the weekly status.
3. Identifies **recurring** items — the same friction across two or more weeks
   becomes a candidate P0/P1 hotfix (permitted under the freeze) or, if it would
   need new product code, a recorded demand signal (not a build — see
   [`../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md)).
4. Confirms **zero doctrine violations** in the period — any violation is itself
   a high-severity friction event and blocks the freeze-lift gate (§4).

**Escalate.** High-severity or recurring friction with revenue or doctrine
impact goes into the weekly status with a proposed action and, where a founder
decision is needed, an explicit blocker line.

الالتقاط مستمر، والمراجعة أسبوعية ضمن حلقة الأحد: قراءة أحداث الـ١٤ يوماً،
إبراز عالي الخطورة، رصد المتكرّر، تأكيد غياب أي خرق للعقيدة.

---

## 7. Document Control — ضبط الوثيقة

- **Scope.** Planning/ops document. Proposes no new product feature, module,
  router, endpoint, or dashboard. Respects the Commercial Freeze and the 11
  non-negotiables.
- **Review.** Revisit after Day 30, Day 60, Day 90, and immediately on a
  freeze-lift event.
- **Source of truth.** Milestone numbers from
  [`../../dealix/registers/90_day_execution.yaml`](../../dealix/registers/90_day_execution.yaml)
  and [`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md);
  product definition from [`../CANONICAL_PRODUCT_NARRATIVE.md`](../CANONICAL_PRODUCT_NARRATIVE.md);
  freeze rules from [`COMMERCIAL_FREEZE.md`](COMMERCIAL_FREEZE.md) and
  [`../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md).

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
