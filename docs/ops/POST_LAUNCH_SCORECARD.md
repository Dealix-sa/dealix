# Post-Launch Scorecard — لوحة ما بعد الإطلاق + شجرة المقاييس + معالم 30/60/90

<!-- Owner: Founder | Cadence: T+1/T+7/T+30 reliability + weekly KPI tree + 30/60/90 milestones -->
<!-- Arabic primary · English secondary -->

> Filled by the release captain (currently founder). Single source of truth for "did launch actually go well" **and** for the commercial KPI tree (warm touch → retainer).

**الحالة الصريحة / Honest baseline:** Dealix أُطلقت تقنيًا، **0 عملاء يدفعون**، الإيراد محجوب حتى اكتمال Moyasar KYC. كل الأرقام أدناه أهداف تشغيلية — **لا ضمانات**. أي رقم لم يتحقق = `insufficient_data`.

## How to use / كيفية الاستخدام
- شجرة KPI (§A) تُراجَع **أسبوعيًا** في الاجتماع التشغيلي.
- معالم 30/60/90 (§B) تُراجَع عند كل معلم — مطابقة لخطة الـ 90 يوم.
- جداول الموثوقية (T+1/T+7/T+30) تُملأ عند كل معلم — انسخ القالب أسفل الملف.
- أرقام صلبة فقط. أي صف **أحمر** يولّد action item بمالك وتاريخ.

**روابط الإيقاع / Cadence links:** [`daily_scorecard.md`](daily_scorecard.md) · [`DAILY_OPERATING_LOOP.md`](DAILY_OPERATING_LOOP.md) · [`../operating_rhythm/WEEKLY_OPERATING_MEETING.md`](../operating_rhythm/WEEKLY_OPERATING_MEETING.md) · [`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md)

---

## A. شجرة المقاييس / KPI Tree — Warm Touch → Retainer

القمع الكامل من أول لمسة دافئة إلى أول retainer. كل مقياس له: تعريف، هدف، وطريقة قياس.
The full funnel from first warm touch to first retainer. Each metric has a definition, target, and measurement method.

```
[1] Warm touches sent
        │  conversion: reply rate
        ▼
[2] Positive replies
        │  conversion: diagnostic booking rate
        ▼
[3] Free Diagnostics booked  (Rung 0)
        │  conversion: diagnostic show rate
        ▼
[4] Free Diagnostics completed
        │  conversion: diagnostic → paid close rate
        ▼
[5] Paid 499 Sprints closed  (Rung 1 — 7-Day Revenue Proof Sprint)
        │  conversion: payment completion rate
        ▼
[6] Sprints paid & delivered
        │  conversion: proof documentation rate
        ▼
[7] Documented Proof Packs  (proof event, governed)
        │  conversion: proof → retainer rate
        ▼
[8] Retainer clients  (Rung 3 — Managed Revenue Ops, 2,999–4,999 SAR/mo)
```

| # | المقياس / Metric | التعريف / Definition | الهدف / Target | كيف يُقاس / How measured |
|---|------------------|----------------------|----------------|--------------------------|
| 1 | Warm touches sent | رسائل دافئة (معرفة/إحالة/موافقة) أُرسلت — لا outreach بارد | ~10/يوم، ~250/30 يوم | عدّ صفوف `pipeline_tracker.csv` بـ `sent_at` |
| → | Reply rate | ردود ÷ لمسات | ≥ 5% | `daily_scorecard.md` weekly funnel |
| 2 | Positive replies | ردود تُبدي اهتمامًا قابلًا للتأهيل | ≥ 1–2/يوم | tracker status = "Replied" |
| → | Diagnostic booking rate | تشخيص محجوز ÷ ردود إيجابية | ≥ 40% من الردود | tracker status = "Diagnostic Booked" |
| 3 | Free Diagnostics booked (Rung 0) | مكالمات تشخيص مجاني محجوزة عبر Calendly | يوم 30: 6 تراكمي | حجوزات Calendly + tracker |
| → | Diagnostic show rate | تشخيص منجز ÷ محجوز | ≥ 70% | tracker status = "Diagnostic Done" |
| 4 | Free Diagnostics completed | مكالمات تشخيص أُجريت فعليًا (سكربت `FIRST_3_DIAGNOSTIC_SCRIPT.md`) | يوم 30: 6 · يوم 60: 12 · يوم 90: 20 | tracker + daily scorecard |
| → | Diagnostic → paid close rate | Sprints مدفوعة ÷ تشخيص منجز | ≥ 20% | حساب أسبوعي |
| 5 | Paid 499 Sprints closed (Rung 1) | عملاء التزموا/دفعوا 499 SAR للـ 7-Day Revenue Proof Sprint | يوم 7: 1 · يوم 30: 2–3 · يوم 60: 5 · يوم 90: 10 | tracker + `manual_payment_log.md` |
| → | Payment completion rate | دفعات مستلمة ÷ دفعات مطلوبة | ≥ 80% | Moyasar dashboard / سجل الدفع اليدوي |
| 6 | Sprints paid & delivered | Sprints اكتمل تسليمها (Proof Pack مُسلَّم) | = عدد Sprints المُغلقة | `PILOT_DELIVERY_SOP.md` DoD |
| → | Proof documentation rate | Proof Packs موثقة ÷ Sprints مُسلّمة | 100% (DoD صارم) | WEEKLY_PROOF_REVIEW.md |
| 7 | Documented Proof Packs | أحداث إثبات محوكمة (governance status + بلا PII + بلا claim مزيّف) | يوم 30: 3 · يوم 60: 8 · يوم 90: 15 | proof_score.py + WEEKLY_PROOF_REVIEW.md |
| → | Proof → retainer rate | تحويل من Sprint مُثبَت إلى retainer | ≥ 25% (هدف) | حساب شهري |
| 8 | Retainer clients (Rung 3) | عملاء Managed Revenue Ops شهري (2,999–4,999 SAR) | يوم 30: 0 · يوم 60: 2 · يوم 90: 3 | عقود موقّعة + MRR |

**قاعدة التشخيص / Diagnostic rule:** أصلح **أضيق** نقطة في القمع أولًا (انظر إشارات الاختناق في `DAILY_OPERATING_LOOP.md`).

---

## B. معالم 30/60/90 يوم / 30·60·90 Milestone Scorecard

> الأرقام **مطابقة** لـ [`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md). أهداف تشغيلية لا ضمانات.

| المعلم / Milestone | الهدف الملموس / Concrete target | الحالة / Status |
|--------------------|----------------------------------|-----------------|
| **Day 7** | أول 7-Day Revenue Proof Sprint مدفوع (499 SAR) مُغلق أو مجدول؛ 3 تشخيصات؛ 5 warm intros | ⚪️ |
| **Day 30** | ~2–3 Sprints مدفوعة؛ 6 تشخيصات تراكمية؛ 3 أحداث إثبات موثقة؛ أول case study (مجهول/بموافقة)؛ إيراد ~998 SAR | ⚪️ |
| **Day 60** | 5 Sprints مدفوعة تراكميًا؛ 12 تشخيصًا؛ 8 أحداث إثبات؛ **أول Proof Pack منشور**؛ أول 2 عملاء Managed Ops (retainer)؛ MRR ~5,998 SAR | ⚪️ |
| **Day 90** | 10 عملاء تراكميًا؛ 20 تشخيصًا؛ 15 حدث إثبات؛ **أول case study منشورة + أول retainer مستقر**؛ 3 عملاء Managed Ops؛ MRR ~8,997–14,997 SAR؛ أول lead من قناة شريك | ⚪️ |

| المقياس / Metric | يوم 7 | يوم 30 | يوم 60 | يوم 90 |
|------------------|-------|--------|--------|--------|
| Diagnostics (تراكمي) | 3 | 6 | 12 | 20 |
| Paid 499 Sprints | 1 | 2–3 | 5 | 10 |
| Proof Events موثقة | 1 | 3 | 8 | 15 |
| Managed Ops retainers (Rung 3) | 0 | 0 | 2 | 3 |
| MRR (SAR) | — | ~998 | ~5,998 | ~8,997–14,997 |
| Case studies منشورة | 0 | 1 | 2 | 3 |

**حالة / Status legend:** 🟢 محقّق · 🟡 ضمن 10% أسفل الهدف · 🔴 أكثر من 10% أسفل (action item) · ⚪️ لم يُقَس بعد.

أي صف 🔴 → action item في الاجتماع التشغيلي الأسبوعي (مالك + تاريخ).

---

## T+30 — _<fill date>_

### Business (revenue + acquisition)

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| MRR (excluding pilots) | ≥ 10,000 SAR | _fill_ | ⚪️ |
| Paying customers (Starter+) | ≥ 10 | _fill_ | ⚪️ |
| Active pilots | ≥ 30 | _fill_ | ⚪️ |
| Pilot → Paid conversion | ≥ 25% | _fill_ | ⚪️ |
| Landing → Demo conversion | ≥ 2% | _fill_ | ⚪️ |
| Demo → Pilot conversion | ≥ 30% | _fill_ | ⚪️ |
| CAC (blended) | ≤ 500 SAR | _fill_ | ⚪️ |
| LTV / CAC | ≥ 3.0 | _fill_ | ⚪️ |
| Net revenue churn | ≤ 5% | _fill_ | ⚪️ |
| NPS (sampled) | ≥ +40 | _fill_ | ⚪️ |

### Reliability

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| Uptime (30-day) | ≥ 99.5% | _fill_ | ⚪️ |
| P95 API latency | < 500ms | _fill_ | ⚪️ |
| SEV-1 incidents | 0 | _fill_ | ⚪️ |
| SEV-2 incidents | ≤ 2 | _fill_ | ⚪️ |
| Mean time to recover (SEV-1/2) | < 30 min | _fill_ | ⚪️ |
| Webhook success rate | ≥ 99% | _fill_ | ⚪️ |
| DLQ depth max in window | ≤ 5 | _fill_ | ⚪️ |
| Backups: 30/30 hourly successful | yes | _fill_ | ⚪️ |
| Restore drill passed (this quarter) | yes | _fill_ | ⚪️ |

### Security & Compliance

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| Critical CVEs in deps | 0 | _fill_ | ⚪️ |
| Secrets leaked (gitleaks finds) | 0 | _fill_ | ⚪️ |
| Failed admin-auth attempts (anomalies) | ≤ 5 / day | _fill_ | ⚪️ |
| DSAR requests received | n/a | _fill_ | ⚪️ |
| DSAR responded within 30 days | 100% | _fill_ | ⚪️ |
| PDPL incidents | 0 | _fill_ | ⚪️ |
| Sentry events with PII | 0 | _fill_ | ⚪️ |

### Channels

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| Email send-day total | ≤ 50 / sender | _fill_ | ⚪️ |
| Email bounce rate | < 5% | _fill_ | ⚪️ |
| Email reply rate | ≥ 8% | _fill_ | ⚪️ |
| WhatsApp delivery rate | ≥ 95% | _fill_ | ⚪️ |
| WhatsApp opt-out rate | < 5% | _fill_ | ⚪️ |
| Calendly bookings | ≥ 20 / month | _fill_ | ⚪️ |

### Action items

| # | Item | Owner | Due |
|---|------|-------|-----|
| 1 | _fill_ | _fill_ | _fill_ |

### Notes
_Free-text retro of the month._

---

## T+7 — _<fill date>_

(same template, week scope; bar: 1/4 of T+30 numbers)

---

## T+1 — _<fill date>_

(same template, day scope; bar: 1/30 of T+30 numbers, plus mandatory 100% backup success, 0 SEV-1)

---

## Status legend

- 🟢 met or beat target
- 🟡 within 10% below target
- 🔴 > 10% below target — triggers action item
- ⚪️ not yet measured

---

## Template (copy when filling)

```markdown
## T+N — YYYY-MM-DD

### Business
| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| ... |

### Reliability
...

### Security & Compliance
...

### Channels
...

### Action items
| # | Item | Owner | Due |

### Notes
```
