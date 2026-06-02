# Dealix Product Distribution OS v1 — ماكينة التصريف بالموافقة أولاً

**الغرض:** نظام تشغيلي يومي يحوّل المرشّحين (prospects) إلى **مسودات محكومة** (governed drafts) جاهزة للمراجعة — **ولا يُرسل شيئاً تلقائياً**. كل تواصل خارجي يبقى فعلاً بشرياً يدوياً بعد موافقة المؤسس.

**الوعد التشغيلي:** كل صباح يُولّد النظام مسوداتٍ، طابوراً للمراجعة، طابور متابعات مستحقّة، ومقاييس قِمع. المؤسس يقرأ 4 تقارير تحت `reports/distribution/`، يوافق/يعدّل/يرفض، ثم **ينسخ ويُرسل يدوياً**.

**الكود (يُبنى في هذا الـ PR):** حزمة [`auto_client_acquisition/distribution_os/`](../../auto_client_acquisition/distribution_os/) + سكربتات رفيعة في [`scripts/`](../../scripts/) + مخططات JSON تحت [`schemas/`](../../schemas/).

**مراجع عليا:** [DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md](../commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md) · [DAILY_COMMERCIAL_LOOP_AR.md](../ops/DAILY_COMMERCIAL_LOOP_AR.md) · الدستور المعماري: [master-architecture.md](../blueprint/master-architecture.md).

---

## 1) ما هو — التدفق الكامل

النظام «ماكينة تصريف» (distribution machine): سلسلة مراحل حتمية تبدأ من البحث وتنتهي بالتجديد، وفي كل مرحلة تنتج **مسودة** لا إجراءً خارجياً.

```
بحث ← مرشّح ← مسودة ← موافقة ← إرسال يدوي بعد الموافقة ← متابعة
   ← تشخيص ← عرض ← حزمة إثبات ← دفع ← تسليم ← تجديد
```

| المرحلة | المخرَج | مَن ينفّذ |
|---------|---------|-----------|
| Research (بحث) | إشارات سوق + قطاع (مجمّعة، بلا PII) | الذكاء يستكشف |
| Prospect (مرشّح) | سجل مرشّح + سبب الملاءمة | الذكاء يرشّح |
| Draft (مسودة) | نص محكوم `pending_approval` | مصنع المسودات |
| Approval (موافقة) | approve / edit / reject | **المؤسس** |
| Manual Send (إرسال يدوي) | نسخ يدوي بعد الموافقة | **المؤسس** |
| Follow-up (متابعة) | متابعات مستحقّة فقط | محرّك المتابعة |
| Diagnostic (تشخيص) | ملخص تشخيصي للعميل | الذكاء + مراجعة |
| Proposal (عرض) | هيكل عرض بحدود حوكمة | مصنع العروض |
| Proof Pack (حزمة إثبات) | إثبات بمستوى L0–L5 | مصنع الإثبات |
| Payment (دفع) | متابعة رابط دفع يدوية | **المؤسس** |
| Delivery (تسليم) | تقرير + رسالة onboarding | تسليم/تجديد |
| Renewal (تجديد) | فرصة تجديد/توسعة | تسليم/تجديد |

**قاعدة جوهرية:** القيمة التقديرية في أي مخرَج هي تقدير عمل، لا التزام.

---

## 2) الأنظمة الفرعية التسعة

| # | النظام الفرعي | المسؤولية | مرجع |
|---|----------------|-----------|------|
| 1 | Market Intelligence | إشارات قطاع مجمّعة، أنماط، لا PII | [DISTRIBUTION_METRICS_AR.md](DISTRIBUTION_METRICS_AR.md) |
| 2 | Prospect | سجل المرشّح وسبب الملاءمة | [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) |
| 3 | Draft Factory | توليد مسودات محكومة لكل قناة يدوية | [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) |
| 4 | Approval | بوابة المؤسس: approve/edit/reject | [DRAFT_APPROVAL_RUNBOOK_AR.md](DRAFT_APPROVAL_RUNBOOK_AR.md) |
| 5 | Follow-up | جدولة المتابعات المستحقّة فقط | [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md) |
| 6 | Proposal | هيكل عرض بحدود حوكمة وبلا ضمان | [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) |
| 7 | Proof Pack | إثبات جاهزية بمستويات L0–L5 | [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md) |
| 8 | Revenue Metrics | قِمع وأرقام من أدلة فقط | [DISTRIBUTION_METRICS_AR.md](DISTRIBUTION_METRICS_AR.md) |
| 9 | Delivery / Renewal | تسليم، تقرير أسبوعي، تجديد/توسعة | [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) |

سياسة الجودة العابرة لكل الأنظمة: [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md).

---

## 3) كيف يتطابق مع الطبقات الخمس

القاعدة الحاكمة (الدستور): **الذكاء يستكشف ويحلّل ويوصي · سير العمل الحتمي ينفّذ · البشر يوافقون على الالتزامات الخارجية.** كل مكوّن من الـ OS يعيش في طبقة واحدة، والعبور بين الطبقات عبر عقود لا عبر استدعاء مباشر.

| الطبقة (Plane) | ماذا يضع فيها الـ OS | الحدّ |
|----------------|----------------------|-------|
| **Decision** | بحث السوق، ترشيح المرشّحين، اقتراح زاوية العرض، صياغة نص المسودة | يستكشف ويوصي؛ لا يُرسل، لا يلتزم |
| **Execution** | السكربتات الحتمية: توليد المسودات، بناء الطوابير، حساب المتابعات المستحقّة | ينفّذ سير العمل؛ لا يقرّر بدل المؤسس |
| **Trust** | بوابات الجودة، فحص الادّعاءات، سياسة القنوات، حالة `pending_approval`، السجل | يحجب أي مسودة تكسر السياسة |
| **Data** | سجلات المرشّحين والمسودات والمتابعات، مخططات JSON، التقارير | مصدر حقيقة حتمي؛ بلا PII في السجلات |
| **Operating** | أهداف Makefile، تشغيل CI، الفحص اليومي `make doctor` | يضمن أن الماكينة نفسها صحّية وقابلة للتدقيق |

**ترجمة عملية:** الذكاء قد يقترح أن نراسل شركة في قطاع معيّن بزاوية معيّنة → السكربت الحتمي يصوغ المسودة بالحالة `pending_approval` → الـ Trust Plane يفحصها ويحجب أي ادّعاء ممنوع → المؤسس وحده يوافق ثم ينسخ ويُرسل يدوياً. لا حلقة وكيل (agent loop) تُحدِث التزاماً خارجياً.

---

## 4) كيف يستخدمه المؤسس يومياً

ثلاثة أوامر، ثم مراجعة أربعة تقارير.

```bash
# 1) فحص صحّة الماكينة (الطبقة التشغيلية)
make doctor

# 2) يوم التصريف الكامل: توليد مسودات + طوابير + متابعات + مقاييس
make distribution-day

# 3) بوابة الجودة على المسودات قبل المراجعة
make draft-quality
```

`make distribution-day` يشغّل [`scripts/distribution_day.py`](../../scripts/distribution_day.py) الذي يستدعي بالترتيب:
[`generate_distribution_drafts.py`](../../scripts/generate_distribution_drafts.py) →
[`review_draft_queue.py`](../../scripts/review_draft_queue.py) →
[`generate_followup_queue.py`](../../scripts/generate_followup_queue.py) →
[`distribution_metrics.py`](../../scripts/distribution_metrics.py).

ثم يراجع المؤسس **أربعة تقارير** تحت [`reports/distribution/`](../../reports/distribution/):

| التقرير | الغرض | الدليل |
|---------|-------|--------|
| `DRAFT_QUEUE_REVIEW.md` | قائمة المسودات للموافقة/التعديل/الرفض | [DRAFT_APPROVAL_RUNBOOK_AR.md](DRAFT_APPROVAL_RUNBOOK_AR.md) |
| `FOLLOWUP_QUEUE.md` | المتابعات المستحقّة اليوم فقط | [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md) |
| `DRAFT_QUALITY_REPORT.md` | نتائج بوابة الجودة (محجوب/مقبول) | [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) |
| `DISTRIBUTION_METRICS.md` | المقاييس والقِمع | [DISTRIBUTION_METRICS_AR.md](DISTRIBUTION_METRICS_AR.md) |

أهداف يدوية مرجعية (يومياً): وافِق ~10 مسودات، عدّل ~3، ارفض ~5، انسخ وأرسِل ~10 يدوياً، احجز مكالمتَي discovery، تابِع 5.

أوامر مفردة عند الحاجة: `make distribution-drafts`، `make draft-queue`، `make followup-queue`، `make proposal-drafts`، `make distribution-metrics`.

---

## 5) قيود السلامة (غير قابلة للتفاوض)

- **لا إرسال خارجي تلقائي.** لا توجد قناة أتمتة إطلاقاً؛ كل القنوات يدوية.
- **لا واتساب بارد** (cold WhatsApp) — هذا نمط **ممنوع** يحجبه فحص الجودة.
- **لا أتمتة لينكدإن** — نمط **ممنوع**؛ التواصل عبر لينكدإن يدوي فقط.
- **لا كشط بيانات** (scraping) ولا قوائم مشتراة.
- **لا ادّعاءات مضمونة** — تُستبدل بـ «فرص مُثبتة بأدلة» / evidenced opportunities.
- **لا PII في السجلات** — لا بريد ولا هاتف ولا هوية ولا أسماء حقيقية في المخرجات.
- **كل مسودة تبدأ `pending_approval`** — لا حالة «أُرسل عبر تكامل» في النظام بالتصميم.

السياسة التفصيلية وكلمات الحجب: [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md). حوكمة القنوات في الكود: [`channel_policy.py`](../../auto_client_acquisition/governance_os/channel_policy.py).

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

*آخر تحديث: 2026-06-02 — يُبنى في هذا الـ PR مع الحزمة والسكربتات والمخططات.*
