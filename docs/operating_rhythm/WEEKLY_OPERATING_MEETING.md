# Dealix Weekly Operating Meeting — الاجتماع التشغيلي الأسبوعي

<!-- Owner: Founder | Cadence: weekly, fixed day/time | Status: canonical weekly meeting -->
<!-- Arabic primary · English secondary -->

> **القاعدة:** اجتماع تشغيلي **واحد** أسبوعيًا — 45–60 دقيقة، يوم ثابت (مقترح: الأحد 09:00).
> لا يُغلق الاجتماع قبل إنتاج المخرجات الإلزامية السبعة في الأسفل.
>
> **Rule:** Exactly **one** operating meeting per week — 45–60 min, fixed day/time (suggested: Sunday 09:00).
> The meeting does not close until the seven mandatory outputs below are produced.

**الحالة الصريحة / Honest baseline:** Dealix أُطلقت تقنيًا، **0 عملاء يدفعون**، الإيراد محجوب حتى اكتمال KYC في Moyasar. هذا الاجتماع يقيس التقدّم نحو أول pilot مدفوع — بصدق، بلا تجميل.

---

## 0. التحضير قبل الاجتماع (المؤسس، 10 دقائق) — Pre-read

قبل بدء الاجتماع، جهّز الأرقام — لا تجمعها أثناء الاجتماع:

- [ ] Daily Scorecard للأسبوع مُعبّأ — `docs/ops/daily_scorecard.md`
- [ ] لقطة قمع KPI (warm touch → diagnostic → 499 → proof → retainer) — `docs/ops/POST_LAUNCH_SCORECARD.md`
- [ ] مخرَج friction log للأسبوع — `python -m auto_client_acquisition.friction_log` aggregate (انظر §6)
- [ ] قائمة Proof Packs المُسلّمة + درجاتها — `docs/operating_rhythm/WEEKLY_PROOF_REVIEW.md`
- [ ] قائمة قرارات CEO المفتوحة — `docs/operating_rhythm/DECISION_QUEUE.md`

---

## 1. جدول الأعمال — Agenda (45–60 min)

| # | البند | المدة | المصدر |
|---|-------|-------|--------|
| 1 | قرارات CEO الثلاثة (Top 3 Decisions) | 10 min | DECISION_QUEUE.md |
| 2 | قمع الإيراد (Revenue / pipeline funnel) | 8 min | POST_LAUNCH_SCORECARD.md |
| 3 | التسليم النشط (Active delivery + blockers) | 7 min | pipeline_tracker.csv |
| 4 | مراجعة الإثبات (Proof Packs + scores) | 5 min | WEEKLY_PROOF_REVIEW.md |
| 5 | الحوكمة (Governance risks) | 5 min | WEEKLY_GOVERNANCE_REVIEW.md |
| 6 | مراجعة الاحتكاك (Friction log) | 5 min | friction_log aggregate |
| 7 | إشارات المنتجة (Productization signals) | 3 min | FEATURE_CANDIDATE_LOG.md |
| 8 | تخصيص رأس المال (Capital allocation) | 3 min | — |
| 9 | قائمة الإيقاف (Stop / Kill) | 4 min | ../company/STOP_DOING.md |
| 10 | الالتزامات (Commitments) | 5 min | this doc |

---

## 2. المخرجات الإلزامية — Mandatory outputs (gate before close)

**لا يُغلق الاجتماع** قبل تسجيل كل صف صراحةً في محضر الأسبوع:

| المخرج / Output | العدد / المعيار | ملاحظة |
|-----------------|------------------|--------|
| قرارات CEO / CEO decisions | **3** بالضبط | قرار مغلق، له مالك، لا «للنقاش لاحقًا» |
| التزامات قابلة للمتابعة / actionable commitments | **3** بالضبط | كل التزام: مالك + تاريخ + تعريف «تمّ» |
| مخاطرة نُخفّضها / risk reduced | **1** على الأقل | إجراء ملموس يقلّل احتمال أو أثر مخاطرة |
| proof نقوّيه / proof strengthened | **1** | proof pack جديد أو ترقية tier أو مصدر تحقق |
| شيء نُوقفه / one thing killed | **1** | نشاط/قناة/مهمة نتوقف عنها هذا الأسبوع |

> **إشارة تحذير:** إذا خرج الاجتماع بلا «شيء نُوقفه»، غالبًا التركيز ضاع تحت التوسّع. القتل إلزامي.
> **Warning signal:** if the meeting closes with nothing killed, focus has likely been lost to sprawl. The kill is mandatory.

---

## 3. قالب المحضر — Meeting minutes template (copy each week)

```markdown
## Weekly Operating Meeting — Week N — YYYY-MM-DD

### Honest one-liner
[State plainly where the business is: e.g. "0 paid, 1 diagnostic booked, Moyasar KYC pending."]

### 1. Top 3 CEO Decisions
| # | Decision | Owner | Rationale |
|---|----------|-------|-----------|
| 1 | | Founder | |
| 2 | | | |
| 3 | | | |

### 2. Revenue funnel (this week)
| Stage | This week | WoW Δ | Target |
|-------|-----------|-------|--------|
| Warm touches | | | |
| Free diagnostics done | | | |
| Paid 499 Sprints closed | | | |
| Proof Packs documented | | | |
| Retainer (Rung 3) conversations | | | |

### 3. Active delivery
- Active Sprints/pilots: __
- Blockers (owner + ETA): __

### 4. Proof
- Proof Packs delivered this week: __
- Avg proof score: __  | Weakest proof + fix: __
- 1 proof strengthened this week: __

### 5. Governance
- Pulled from WEEKLY_GOVERNANCE_REVIEW.md — open items: __
- 1 risk reduced this week: __

### 6. Friction log review
- Top 3 friction kinds (count): __
- WoW delta: __  | Total cost (minutes): __
- Friction-reduction action chosen: __ (owner + date)

### 7. Productization signals
- Repeated manual steps logged → FEATURE_CANDIDATE_LOG.md: __

### 8. Capital allocation
- Where founder hours go next week (1 sentence): __

### 9. Killed this week
- 1 thing stopped: __ (why: __)

### 10. Commitments (exactly 3)
| # | Commitment | Owner | Due | Done = |
|---|------------|-------|-----|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
```

---

## 3a. مراجعة سجل الاحتكاك — Friction log review process (Agenda item 6)

كل أسبوع يستهلك الاجتماع مخرَج `auto_client_acquisition/friction_log` لتقليل احتكاك التسليم. سجل الاحتكاك يلتقط **كل مرة احتاج فيها التسليم تدخلًا بشريًا أو تعثّر** — أنواعه: `governance_block`, `approval_delay`, `schema_failure`, `manual_override`, `retry`, `support_ticket`, `missing_source_passport`, `missing_proof_pack`.

Each week the meeting consumes the friction log to reduce delivery friction.

### الخطوات / Steps

1. **قبل الاجتماع — استخرج الإجمالي / Pre-meeting — pull the aggregate.**
   لكل عميل نشط، استدعِ `aggregate()` لنافذة 7 أيام:
   ```python
   from auto_client_acquisition.friction_log import aggregate
   agg = aggregate(customer_id="<id>", window_days=7)
   # agg.total, agg.by_kind, agg.by_severity, agg.top_3_kinds,
   # agg.total_cost_minutes, agg.week_over_week_delta
   ```
   (الملاحظات مُنقّاة تلقائيًا عند `emit` عبر `sanitize_notes` — بلا PII في الناتج.)

2. **في الاجتماع — اقرأ 3 أرقام / In-meeting — read 3 numbers (2 min):**
   - `top_3_kinds` — أكثر 3 أنواع احتكاك تكرارًا.
   - `total_cost_minutes` — الوقت البشري الضائع على التدخلات.
   - `week_over_week_delta` — هل الاحتكاك يرتفع أم ينخفض؟

3. **اختر إجراءً واحدًا لتقليل الاحتكاك / Pick one friction-reduction action (3 min):**
   عالج **النوع الأعلى تكرارًا**، لا الأحدث. القاعدة:

   | إشارة / Signal | الإجراء / Action |
   |----------------|------------------|
   | `manual_override` متكرر | المهمة مرشّحة للأتمتة → `FEATURE_CANDIDATE_LOG.md` (يغذّي بند 7) |
   | `governance_block` متكرر | بند للمراجعة الأسبوعية للحوكمة — هل العملية أم القاعدة تحتاج تعديلًا؟ |
   | `approval_delay` متكرر | راجع SLA طابور الموافقة / approval_center |
   | `schema_failure` / `missing_source_passport` | أصلح التحقّق المسبق في الـ onboarding |
   | `missing_proof_pack` | فجوة في DoD التسليم — أصلح `PILOT_DELIVERY_SOP.md` |
   | `week_over_week_delta` موجب (ارتفاع) | الاحتكاك يتراكم — يصبح أحد قرارات CEO الثلاثة |

4. **سجّل المخرَج / Record the output.** الإجراء المختار يصبح أحد **الالتزامات الثلاثة** (مالك + تاريخ)، ويُقيَّد في محضر §6.

> أنماط الاحتكاك المتكررة هي **إشارات منتجة**: ما يتكرر يدويًا اليوم يصبح ميزة غدًا.

---

## 4. حلقة الفحص الذاتي — Self-check loop (ask every week)

ما الأكثر جاهزية للبيع؟ · ما الذي يمنع البيع الآن؟ · أكبر فجوة تسليم؟ · أكثر خطوة يدوية متكررة؟ · أكثر مخرَج يحتاج QA؟ · أكبر مخاطرة حوكمة؟ · ما الذي يقرّبنا من أول retainer؟

---

## 5. الربط — Linked cadence docs

- اليومي / Daily: [`../ops/DAILY_OPERATING_LOOP.md`](../ops/DAILY_OPERATING_LOOP.md) · [`DAILY_CEO_CHECK.md`](DAILY_CEO_CHECK.md)
- الإثبات / Proof: [`WEEKLY_PROOF_REVIEW.md`](WEEKLY_PROOF_REVIEW.md)
- الحوكمة / Governance: [`WEEKLY_GOVERNANCE_REVIEW.md`](WEEKLY_GOVERNANCE_REVIEW.md)
- المنتجة / Productization: [`WEEKLY_PRODUCTIZATION_REVIEW.md`](WEEKLY_PRODUCTIZATION_REVIEW.md)
- الإيراد الجيد / Bad revenue council: [`BAD_REVENUE_COUNCIL.md`](BAD_REVENUE_COUNCIL.md)
- المقاييس / Metrics + 30·60·90: [`../ops/POST_LAUNCH_SCORECARD.md`](../ops/POST_LAUNCH_SCORECARD.md)
- خطة 90 يوم / 90-day plan: [`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md)

> **Canonical note:** This is the single weekly operating meeting for Dealix.
> `docs/company/WEEKLY_OPERATING_REVIEW.md` is a pointer to this file — do not maintain a parallel agenda there.
</content>
</invoke>
