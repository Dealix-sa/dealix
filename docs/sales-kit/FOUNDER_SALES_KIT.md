# Dealix — Founder Sales Kit — حقيبة المبيعات للمؤسس

> **One place. Zero re-drafting.** This is the single entry point for the
> warm-list motion to land the first paid pilot — the 499 SAR 7-Day Revenue
> Proof Sprint + a customer-approved Proof Pack. Open this file first.
>
> **Constraints (non-negotiable):** every message is a DRAFT for Sami to
> review and send himself. No external sends by any tool. No scraping, no
> cold WhatsApp, no LinkedIn automation, no bulk outreach. Warm list only.
> No guarantees, no "نضمن", no auto-reply / 45-second / auto-book claims.
> Arabic-first. Entry offer is the Free Diagnostic, then the 499 SAR Sprint.
>
> **Doctrine sources of truth:** [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md),
> [`docs/POSITIONING_AND_ICP.md`](../POSITIONING_AND_ICP.md),
> [`docs/ops/launch_content_queue.md`](../ops/launch_content_queue.md).

---

## 0. The runsheet — الترتيب الذي يتبعه المؤسس

| خطوة | ماذا تفعل | المرجع | أين تسجّل |
|------|-----------|--------|-----------|
| 1 | افتح القائمة الموحّدة وحدّد 5 جهات اتصال دافئة لليوم | §1 أدناه + `docs/ops/pipeline_tracker.csv` | — |
| 2 | لكل جهة: اكتب رسالة الدخول الدافئ بصوتك، اختر متغيراً | §2 | `pipeline_tracker.csv` (`sent_at`, `message_version`) |
| 3 | أرسل يدوياً على القناة التي تستخدمها العلاقة أصلاً — 5/يوم بحد أقصى | §2 | `sent_at` |
| 4 | عند وصول رد: تابِع خلال 30 دقيقة، صنّفه (مهتم/غير مهتم/يطلب تفاصيل) | §3 + [`WARM_LIST_WORKFLOW.md`](./WARM_LIST_WORKFLOW.md) §4 | `reply_status` |
| 5 | لمن لم يردّ: متابعة Day +2 / +5 / +10 ثم توقّف | §3 | `next_followup` |
| 6 | "أخبرني المزيد" → مكالمة تأهيل 20 دقيقة + بوابة التأهيل | §4 | `reply_status=qualified` |
| 7 | `ACCEPT` → أرسل رابط التشخيص المجاني (15 دقيقة) | [`WARM_LIST_WORKFLOW.md`](./WARM_LIST_WORKFLOW.md) §5 | `demo_booked_at` |
| 8 | بعد التشخيص (24 ساعة) واعتماده → أرسل عرض السبرنت | §5 + [`SPRINT_PROPOSAL_499.md`](./SPRINT_PROPOSAL_499.md) | `plan`, `payment_status` |
| 9 | قبول → فاتورة Moyasar 50% → بدء السبرنت → Proof Pack → 50% المتبقية | [`SPRINT_PROPOSAL_499.md`](./SPRINT_PROPOSAL_499.md) §3 | `revenue_sar`, `payment_status` |
| 10 | كل يوم تواصل: اكتب فقرة إغلاق يومية (مرسَل/ردود/تحويلات/أكبر اعتراض) | [`WARM_LIST_WORKFLOW.md`](./WARM_LIST_WORKFLOW.md) §6 | `friction_log` |

**Runsheet in English:** open the unified list (§1), draft a warm message
per contact (§2), send manually (5/day max), handle replies within 30 min
(§3), follow up on the +2/+5/+10 cadence then stop, qualify on a 20-min call
(§4), send the diagnostic link on `ACCEPT`, send the 499 SAR proposal after
the diagnostic (§5), invoice 50/50 via Moyasar. Log every step in
`docs/ops/pipeline_tracker.csv`.

---

## 1. Unified warm-list pipeline — القائمة الموحّدة

**Single source of truth: [`docs/ops/pipeline_tracker.csv`](../ops/pipeline_tracker.csv)**
— the live tracker, 50 rows. The two lead docs are archive-only sources that
already fed this tracker; do not work from them:

- [`dealix_leads_20_real.md`](./dealix_leads_20_real.md) — STALE banner; rows 1–21.
- [`dealix_leads_50_expanded.md`](./dealix_leads_50_expanded.md) — STALE banner; sector ideas behind rows 30–50.

Do **not** invent new leads. To add a lead, append one row to the CSV with a
recorded `relationship_basis` (the consent record — see WARM_LIST_WORKFLOW §3).

### Prioritized motion (work the tracker in this order)

| Tier | Tracker rows | Who | Why first | Channel |
|------|--------------|-----|-----------|---------|
| **A — warmest, contact first** | 1, 9, 10 (Lucidya) | عبدالله العسيري + co-founders | اسم القرابة = أعلى احتمال رد دافئ حقيقي | LinkedIn / علاقة قائمة |
| **B — named warm founders** | 2–8, 11 | Foodics, Salla, Zid, Lean, BRKZ, Sary, Retailo | مؤسسون مسمّون، B2B، يطابقون ICP الأساسي | القناة التي تعرفهم بها |
| **C — named, lighter warmth** | 12–21 | Tamara, Mozn, Mnzil, Logexa, Nana, Jahez, Merit, Bayzat, SiFi, Hakbah | مسمّون لكن يحتاجون أساس علاقة مؤكد قبل الإرسال | تأكّد من `relationship_basis` أولاً |
| **D — agency partners** | 22–29 | وكالات تسويق/استشارات | مسار ICP الثانوي — رسالة الشريك، لا عرض السبرنت مباشرة | LinkedIn / علاقة قائمة |
| **E — sector slots, identify before sending** | 30–50 | `TBD` rows | لا ترسل حتى تُملأ بشخص حقيقي + أساس علاقة | — |

**Rule:** 5 contacts/day, 4 days for Tiers A–C. Tier E rows are placeholders
— a `TBD` row is not a lead until a real named person and `relationship_basis`
are filled in. Tier E sector ideas come from `dealix_leads_50_expanded.md`.

> **ICP note:** rows 38–39 (medical clinics) and 49–50 (salon/gym) fall under
> the *Excluded ICP* (healthcare = Tier 3 later; B2C-leaning services). Treat
> as low priority; qualify hard or skip — see POSITIONING_AND_ICP §4.

---

## 2. Warm-intro outreach drafts — مسودات الدخول الدافئ

Use the founder-voice messages already drafted and reconciled in
[`docs/ops/launch_content_queue.md`](../ops/launch_content_queue.md):

- **Warm founder DM** → launch_content_queue "LINKEDIN DM #1" (highest priority).
- **By sector** → DM #2 (SaaS/tech), #3 (platforms/distribution), #4 (B2B
  services/consulting), #5 (contracting/industrial).
- **Agency partners** → "AGENCY DMs — قابلة للتخصيص".
- **One-line warm ask** → [`WARM_LIST_WORKFLOW.md`](./WARM_LIST_WORKFLOW.md) §2
  (AR + EN). Use this when the relationship is light — one question, no deck.

Three picks the founder can choose between for the first touch:

1. **One-line ask** (lightest) — WARM_LIST_WORKFLOW §2.
2. **Founder DM #1** (relationship-led) — launch_content_queue.
3. **Sector DM** (#2–#5, problem-led) — launch_content_queue.

The reusable inbound-reply / qualification drafts also live in
[`OUTREACH_DRAFTS_QUEUED.md`](./OUTREACH_DRAFTS_QUEUED.md) — all draft-only.

**Doctrine check (all messages):** 499 SAR Sprint as the paid entry, draft-only
delivery, no auto-send / no 45-second / no auto-book claims, no guarantees, no
"1 ريال" pilot. The launch_content_queue messages were reconciled 2026-05-18
and pass this check.

> **Older message banks** — [`docs/sales/SALES_MESSAGES.md`](../sales/SALES_MESSAGES.md)
> and [`docs/sales/FOLLOW_UP_SEQUENCE.md`](../sales/FOLLOW_UP_SEQUENCE.md) — are
> doctrine-safe (no auto-send/guarantee claims) but predate the 499 SAR /
> "10-day sprint" wording. Prefer the launch_content_queue messages; if reused,
> swap "10-day" → "7-Day 499 SAR Sprint".

---

## 3. Follow-up cadence — إيقاع المتابعة (Day +2 / +5 / +10)

Use the cadence already drafted in
[`docs/ops/launch_content_queue.md`](../ops/launch_content_queue.md) →
"FOLLOW-UP CADENCE": Day +2 (one-question nudge), Day +5 (sector pattern +
free diagnostic), Day +10 (final, then stop).

Reply handling for messages that *do* land — interested / not interested /
asks-for-info — is fully drafted in
[`WARM_LIST_WORKFLOW.md`](./WARM_LIST_WORKFLOW.md) §4 (AR + EN).

**Rules:** one outreach per contact; follow-ups only if no reply; stop after
Day +10; respond to real replies within 30 minutes; log every touch in
`pipeline_tracker.csv`. No automation — every message typed by the founder.

---

## 4. Qualification — التأهيل

Run the 20-minute qualification call + intake per
[`WARM_LIST_WORKFLOW.md`](./WARM_LIST_WORKFLOW.md) §5. Eight questions, five
decisions: `ACCEPT` / `DIAGNOSTIC_ONLY` / `REFRAME` / `REJECT` / `REFER_OUT`.

If a lead asks for cold WhatsApp, LinkedIn automation, scraping, or guaranteed
sales → `REJECT` with the safe alternative (draft-only, consent-based
outreach, evidenced opportunities). Never improvise around this.

---

## 5. The Sprint proposal — عرض السبرنت (499 ريال)

One clean proposal per qualified lead: [`SPRINT_PROPOSAL_499.md`](./SPRINT_PROPOSAL_499.md).
Bilingual, bounded scope, 11 exclusions, 50/50 payment terms, proof-metric
promise (score ≥ 80, ≥ 1 capital asset), retainer path, disclaimer. Sent only
after the Free Diagnostic recommends a sprint. Fill the blanks; never auto-send.

---

## 6. LinkedIn week-1 content — محتوى لينكدإن الأسبوع الأول

Week-1 posts are doctrine-aligned and paste-ready. **Two equivalent sets exist
— pick one, do not post both:**

- **Launch-week set (recommended for week 1):**
  [`docs/ops/launch_content_queue.md`](../ops/launch_content_queue.md) — POST 1
  (founder launch), POST 2 (agency), POST 3 (problem), plus POST 4–7 for days
  4–7. Reconciled 2026-05-18; verified doctrine-aligned (no 45-sec / 1 SAR /
  guarantee claims).
- **Evergreen set:** [`docs/content/LINKEDIN_POST_001.md`](../content/LINKEDIN_POST_001.md)
  (refusals manifesto), `LINKEDIN_POST_002.md` (Source Passport),
  `LINKEDIN_POST_003.md` — also verified clean (the "guarantee" hits in POST_001
  are the *refusal* of guarantees, which is doctrine-correct).

The full 12-week calendar is [`docs/content/LINKEDIN_CADENCE_PLAN.md`](../content/LINKEDIN_CADENCE_PLAN.md).
For week 1, post the launch-week set in order, 9–11am KSA.

---

## 7. Customer journey gates — بوابات رحلة العميل

1. Lead intake → transactional confirmation email auto-sent (whitelisted).
2. Founder reviews intake within 24h → diagnostic generated → founder approves
   → bilingual brief emailed (brief includes the 499 SAR Sprint proposal).
3. Customer accepts → 50% Moyasar invoice → Sprint kickoff.
4. Sprint delivered → Proof Pack assembled → 50% remainder invoice.
5. If retainer-readiness evaluates `eligible == true` → present the
   2,999 SAR/mo Managed Ops retainer (Rung 3 entry conditions).

---

## 8. Refuse cleanly — الرفض النظيف

> "Dealix doesn't offer [scraping / cold WhatsApp / LinkedIn automation /
> guaranteed sales]. The safe alternative is [draft-only outputs / consent-based
> outreach / evidenced opportunities]. Want me to draft the alternative pitch?"

---

> **النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.**
