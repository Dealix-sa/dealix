# Retainer Eligibility Checklist — Managed Ops Offer

**اللغة:** AR primary · EN gloss للمصطلحات التقنية
**المرحلة:** Day 7 (نهاية Revenue Intelligence Sprint) — قبل عرض Managed Ops
**العرض المُستهدف:** 2,999–4,999 SAR / mo (Managed Ops Retainer rung)
**القرار:** founder-approved فقط · لا auto-sell · لا offer إذا فشل أي معيار

**المراجع:**
- [PROOF_PACK_TEMPLATE.md](./PROOF_PACK_TEMPLATE.md) (14 قسم — Cover Page بتوقيع المؤسس)
- [RETAINER_READINESS.md](./RETAINER_READINESS.md) (Gate 8 — معايير عامة)
- `auto_client_acquisition/adoption_os/retainer_readiness.py` — `evaluate(...)` الـ scoring الرسمي
- [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](../commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md)

---

## المعايير الإلزامية (Hard Gates — كلها يجب أن تكون TRUE)

> إذا فشل **أي** معيار من الـ 4 التالية، **لا يُعرَض** الـ Retainer.
> العميل يبقى على Sprint أو ينتقل إلى Free Diagnostic مرة أخرى.

| # | المعيار | كيف يُتحقَّق منه | Evidence Ref |
|---|---------|-----------------|--------------|
| 1 | **Proof Pack score ≥ 70** | راجع `proof_os.score(...)` على Proof Pack المسلَّم · القيمة في Cover Page §"proof_score" | `var/proof-ledger.jsonl` event `proof_pack_delivered` |
| 2 | **≥ 1 Capital Asset مسجَّل لهذا engagement_id** | `capital_os.list_assets(engagement_id=...)` يُرجع ≥ 1 صفّاً | `var/capital-ledger.jsonl` |
| 3 | **KPI baseline captured** | جدول DQ في §7 يحتوي على رقم أساس (baseline) واحد قابل للقياس لاحقاً | Proof Pack §7 `quality_scores` + §10 `value_metrics` |
| 4 | **Founder approval recorded** | Cover Page `founder_review.decision = "approved"` + `signature_line` غير فارغ | Proof Pack Cover Page |

```text
[ ] proof_pack_score >= 70                              (hard gate)
[ ] capital_assets_count(engagement_id) >= 1            (hard gate)
[ ] kpi_baseline_captured == true                       (hard gate)
[ ] founder_review.decision == "approved"               (hard gate)
```

> Pass = جميع الأربعة TRUE. Fail = أي واحد FALSE → لا Retainer offer.

---

## معايير الجودة الإضافية (Soft Gates — الموصى بها)

> هذه ترفع جودة العرض لكنها ليست hard gates. توثَّق في founder notes.

```text
[ ] adoption_score >= 70           (من adoption_os — مؤشّر استخدام المخرجات)
[ ] workflow_owner_present == true (شخص محدَّد عند العميل يتلقّى المخرجات)
[ ] governance_risk_controlled == true (لا BLOCK غير محلول في §9)
[ ] consent_on_file == true إذا الـ capital asset سيُنشر case-study
[ ] client_asks_continuation == true (إشارة pull واضحة من العميل)
[ ] monthly_value_exists == true (يوجد قيمة شهرية متكرّرة — لا عمل لمرّة واحدة)
[ ] friction events (last 7d) <= 2 high-severity
```

---

## ربط الـ Scoring بالـ Code (مرجع تقني)

ملف: `auto_client_acquisition/adoption_os/retainer_readiness.py`

```python
from auto_client_acquisition.adoption_os.retainer_readiness import evaluate

result = evaluate(
    customer_id="cus_...",
    adoption_score=72.0,           # soft gate
    proof_score=78.0,              # hard gate (>= 70 here, function uses >= 80 internally)
    workflow_owner_present=True,   # soft gate
    governance_risk_controlled=True,
)

# result.eligible          → bool
# result.recommended_offer → "monthly_retainer" | "enablement_sprint" | "proof_pilot"
# result.gaps              → list[str] (machine-readable reasons)
```

> **ملاحظة:** الـ `evaluate()` يطبّق عتبة `proof_score >= 80` (Milestone 2 gate)
> بينما هذه القائمة تستخدم `>= 70` كحدّ أدنى لـ Managed Ops 2,999 rung.
> العتبة `>= 80` تُستخدم لرفع العميل إلى rung 4,999. Founder يقرّر الـ tier.

---

## شجرة القرار (Decision Tree)

```text
proof_score >= 70 ?
├── NO  → لا Retainer · أعد للـ Sprint · سجّل closed_lost(reason="proof_below_70")
└── YES → capital_assets >= 1 ?
         ├── NO  → BLOCK · founder يسجّل أصلاً واحداً قبل العرض
         └── YES → kpi_baseline_captured ?
                  ├── NO  → BLOCK · ارجع لـ §7 وأضف baseline
                  └── YES → founder_review == "approved" ?
                           ├── NO  → BLOCK · انتظر مراجعة المؤسس
                           └── YES → proof_score >= 80 ?
                                    ├── YES → عرض 4,999 SAR/mo (Managed Ops Plus)
                                    └── NO  → عرض 2,999 SAR/mo (Managed Ops Standard)
```

---

## ما يدخل في عرض Managed Ops (للعميل)

> هذا ليس قائمة بيع — هذا ما **يجب** أن يحويه العرض المكتوب للعميل قبل الإغلاق.

### Includes (شهرياً)

- تحسينات workflow ضمن النطاق المتفق (max 3 changes/mo)
- تقرير شهري (proof pack مصغَّر — 4 أقسام: §7 quality · §10 value · §12 next step · §14 capital)
- QA على مخرجات AI (governance review على كل draft خارجي)
- فحوصات حوكمة دورية (`governance_os.decide` على كل action تلقائي)
- ساعات دعم متفق عليها (يحدَّد بحسب tier — 2,999 vs 4,999)
- backlog مرئي للعميل (change requests queue)

### Excludes (يحتاج SOW منفصل)

- تكاملات جديدة (HubSpot/Salesforce setup من الصفر)
- workflows جديدة كلياً خارج الـ scope الأصلي
- enterprise custom development
- on-site visits / live training

---

## قائمة تحقّق ما قبل عرض Retainer (founder copy-paste)

```text
Engagement ID:    eng_____________________
Customer ID:      cus_____________________
Decision date:    ____ / ____ / 2026

HARD GATES
[ ] proof_pack_score >= 70                        (actual: ___)
[ ] capital_assets_count >= 1                     (actual: ___)
[ ] kpi_baseline_captured == true
[ ] founder_review.decision == "approved"

SOFT GATES (سجّل العدد المتحقّق)
[ ] adoption_score >= 70                          (actual: ___)
[ ] workflow_owner_present
[ ] governance_risk_controlled
[ ] client_asks_continuation
[ ] monthly_value_exists
[ ] friction high-sev (7d) <= 2                   (actual: ___)

DECISION
[ ] offer_4999_managed_ops_plus    (proof_score >= 80 + ≥ 5 soft gates)
[ ] offer_2999_managed_ops_std     (proof_score 70-79 + ≥ 3 soft gates)
[ ] hold — recommend enablement_sprint
[ ] closed_lost — reason: ___________________

Founder signature: ________________________________
```

---

## أحداث لازمة في الـ Ledger

| Event | متى | أين يُكتب |
|-------|------|-----------|
| `proof_pack_delivered` | عند تسليم القالب الموقَّع | `proof_ledger` (file backend) |
| `capital_asset_registered` | عند نجاح `add_asset(...)` | `var/capital-ledger.jsonl` |
| `retainer_evaluated` | بعد `evaluate(...)` | (gap اليوم — لا ledger مخصَّص) |
| `upsell_offered` أو `closed_lost` | بعد قرار المؤسس | `revenue_pipeline/stage_policy.py` flow |
| `friction_log.emit(MISSING_PROOF_PACK)` | إذا انتهى Day 7 بدون proof_pack_delivered | `var/friction-log.jsonl` (gap — لا caller حالياً) |

---

## ممنوعات قبل عرض Retainer

- لا عرض Retainer قبل `payment_received` للـ Sprint الأصلي
- لا عرض Retainer إذا proof_score < 70 (حتى لو العميل طلب)
- لا case study بدون consent letter موقَّع (راجع PROOF_PACK_TEMPLATE §E)
- لا تخفيض سعر تحت 2,999 SAR/mo (يكسر سلّم المؤسس)
- لا upsell متعدّد — عرض **واحد** فقط في كل اجتماع ختام
