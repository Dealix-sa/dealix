# Dealix Product Distribution OS — نظام تصريف المنتجات

> الإصدار: v1 (P0) — طبقة المسودات المعتمدة أولًا (approval-first drafts).

## 1. الهدف

تحويل Dealix من منتج **ينتظر الطلب** إلى نظام **يصرّف المنتجات** عبر دورة كاملة:

```
اختيار القطاع
→ ملاءمة العميل المحتمل (prospect fit)
→ فرضية الألم
→ مسودة رسالة
→ موافقة المؤسس
→ إرسال يدوي (نسخ)
→ طابور المتابعة
→ مكالمة استكشاف
→ تشخيص
→ عرض
→ Proof Pack
→ رابط دفع
→ Onboarding
→ تقرير أسبوعي للعميل
→ تجديد / Upsell
```

هذا **ليس** spam ولا scraping ولا أتمتة إرسال. إنه نظام مبيعات مؤسسي **يعتمد الموافقة أولًا**.

## 2. القاعدة الذهبية

> الذكاء الاصطناعي يستكشف ويحلّل ويقترح. الأنظمة الحتمية (deterministic) تنفّذ.
> الإنسان يوافق على كل التزام خارجي حسّاس.

لا إرسال خارجي تلقائي في هذا الإصدار. نؤتمت: **توليد المسودات + الموافقات + طابور المتابعة + تتبّع الإثبات** فقط.

## 3. التكامل مع نواة الريبو (لا إعادة اختراع)

طبقة التصريف **تستدعي الحُرّاس الموجودة** بدل تكرار القواعد، فتُحكم بنفس عقيدة الـ CI:

| الحارس / المصدر | الموقع في الريبو | الدور في التصريف |
| --- | --- | --- |
| `policy_check_draft` | `auto_client_acquisition.governance_os` | يمنع لغة القنوات الممنوعة والادعاءات قبل كتابة أي مسودة |
| `enforce_doctrine_non_negotiables` | `auto_client_acquisition.safe_send_gateway` | يؤكّد أن وضع التشغيل نظيف (لا cold WhatsApp / LinkedIn automation / scraping / إرسال بدون موافقة) |
| `pii_flags_for_row` | `auto_client_acquisition.data_os` | نظافة PII — لا بيانات شخصية في المسودات |
| `validate_pipeline_step` | `auto_client_acquisition.revenue_os.anti_waste` | (P1) يرفض خطوات الـ pipeline التي تخالف السلسلة الذهبية |
| `EvidenceLevel` | `auto_client_acquisition.proof_engine.evidence` | كل مسودة مولّدة = **L1** (مسودة داخلية، غير جاهزة للعميل) |

أي مسودة يُطلقها أحد الحُرّاس تتحوّل تلقائيًا إلى `needs_edit` ولا يمكن اعتمادها قبل إصلاحها.

## 4. مستوى الإثبات (Evidence Level)

تتبع طبقة التصريف نفس سلّم `EvidenceLevel` في الريبو:

| المستوى | المعنى |
| --- | --- |
| L0 | مخطط — لم يُنفَّذ |
| **L1** | **مسودة داخلية — غير جاهزة للعميل (وضع كل مسودة مولّدة)** |
| L2 | راجعها العميل — خاص |
| L3 | وافق العميل |
| L4 | موافقة نشر عام — دراسة حالة |
| L5 | دليل إيراد/توسعة |

المسودة لا تتجاوز L1 إلا بعد مراجعة بشرية حقيقية.

## 5. ما الذي يشمله الإصدار v1 (P0)

| المكوّن | الملف |
| --- | --- |
| نظرة عامة | `docs/distribution/PRODUCT_DISTRIBUTION_OS_AR.md` |
| مواصفة المسودات | `docs/distribution/DRAFT_SYSTEM_SPEC_AR.md` |
| دليل الموافقة | `docs/distribution/DRAFT_APPROVAL_RUNBOOK_AR.md` |
| مخطط JSON | `dealix/contracts/schemas/distribution_draft.schema.json` |
| مولّد المسودات | `scripts/generate_distribution_drafts.py` |
| مراجعة الطابور | `scripts/review_draft_queue.py` |
| مثال العملاء المحتملين | `data/distribution/prospects.example.json` |
| دفتر المسودات (append-only) | `data/drafts/drafts.jsonl` |
| التقارير | `reports/distribution/` |
| اختبارات العقيدة | `tests/test_distribution_drafts.py` |
| أوامر Make | `distribution-drafts` / `draft-queue` / `distribution-day` |

> ملاحظة اتفاقيات: المخطط مُوضَع تحت `dealix/contracts/schemas/` (مكان مخططات الريبو القائم) وليس مجلدًا جديدًا في الجذر، التزامًا باتفاقيات المشروع.

## 6. التشغيل اليومي

```bash
# توليد المسودات + مراجعة الطابور دفعة واحدة
make distribution-day

# ثم افتح التقارير:
#   reports/distribution/DRAFT_GENERATION_REPORT.md
#   reports/distribution/DRAFT_QUEUE_REVIEW.md
```

ثم يتّخذ المؤسس القرار: **اعتماد / تعديل / رفض** لكل مسودة، والنسخ اليدوي للمعتمد فقط.

## 7. القواعد الصارمة (Hard Rules)

- ❌ لا cold WhatsApp automation.
- ❌ لا LinkedIn automation.
- ❌ لا scraping.
- ❌ لا PII في السجلات أو المسودات.
- ❌ لا ادعاءات نتائج مضمونة.
- ❌ لا إرسال خارجي بدون موافقة.
- ✅ كل القنوات **يدوية** (`*_manual` / `phone_script` / `proposal_pdf` / `internal_note`).

## 8. الخارطة (ما بعد v1)

- **P1**: واجهة طابور المسودات، محرّك المتابعة (`validate_pipeline_step`)، مصنع العروض، مؤشرات التصريف.
- **P2**: جسور خارجية تجريبية (n8n dry-run)، HubSpot draft sync، تسليم Calendly/Payment، تعلّم Win/Loss أسبوعي.

التفاصيل التشغيلية في `DRAFT_SYSTEM_SPEC_AR.md` و`DRAFT_APPROVAL_RUNBOOK_AR.md`.
