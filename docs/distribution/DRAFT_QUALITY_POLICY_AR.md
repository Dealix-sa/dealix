# Draft Quality Policy — سياسة بوابة جودة المسودات

**الغرض:** القواعد التي تفرضها بوابة الجودة على كل مسودة **قبل** أن تصل طابور المراجعة. أي مسودة تخالف القاعدة **تُحجَب** ولا يراها المؤسس. الهدف: حماية السمعة والامتثال، ومنع أي ادّعاء أو قناة ممنوعة من الخروج حتى كمسودة.

**المنفّذ:** [`scripts/check_draft_quality.py`](../../scripts/check_draft_quality.py) — يعيد استخدام دوال الحوكمة القائمة:
[`auto_client_acquisition.governance_os.policy_check_draft`](../../auto_client_acquisition/governance_os/policy_check.py) +
[`auto_client_acquisition.governance_os.audit_claim_safety`](../../auto_client_acquisition/governance_os/claim_safety.py).
المخرَج: `reports/distribution/DRAFT_QUALITY_REPORT.md` (محجوب/مقبول لكل مسودة).

**التشغيل:** `make draft-quality`.

**مراجع:** النموذج: [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) · المراجعة: [DRAFT_APPROVAL_RUNBOOK_AR.md](DRAFT_APPROVAL_RUNBOOK_AR.md) · النظرة العامة: [PRODUCT_DISTRIBUTION_OS_AR.md](PRODUCT_DISTRIBUTION_OS_AR.md).

> **ملاحظة سياق:** هذه وثيقة **سياسة حجب**. الكلمات الممنوعة المذكورة أدناه مُدرَجة **بوصفها أنماطاً ممنوعة (ممنوع)** ليتعرّف عليها الفحص ويحجبها — لا تُكتب أبداً كوعد إيجابي في أي مسودة أو مادة عميل.

---

## 1) القواعد المفروضة (BLOCK = حجب فوري)

| # | القاعدة | ما تحجبه | المصدر في الكود |
|---|---------|----------|------------------|
| 1 | حجب الادّعاءات المضمونة / المبالَغة | أي وعد بنتيجة مضمونة | `audit_claim_safety` → `forbidden_claim:` |
| 2 | حجب لغة القناة الممنوعة | واتساب بارد، أتمتة لينكدإن، إرسال جماعي | `is_channel_forbidden` (`FORBIDDEN_CHANNEL_MARKERS`) |
| 3 | حجب مصطلحات الكشط/الإرسال الآلي | كشط بيانات، قوائم مشتراة، إرسال تلقائي بلا موافقة | `audit_draft_text` → `forbidden_term:` |
| 4 | اشتراط `approval_required = true` | أي مسودة تحاول تخطّي الموافقة | مخطط المسودة + الفحص |
| 5 | اشتراط مستوى إثبات صالح `L0`–`L5` | مستوى مفقود أو خارج المدى | تعداد `EvidenceLevel` |
| 6 | اشتراط قناة يدوية صالحة | أي قناة خارج القائمة اليدوية | تعداد `channel` |

أي إخفاق في القواعد 1–3 يجعل الحكم **BLOCK** (انظر `PolicyVerdict.BLOCK`). القواعد 4–6 شروط بنيوية: المسودة التي تخالفها لا تُعتبر صالحة أصلاً.

---

## 2) الأنماط الممنوعة (للتعرّف والحجب فقط — ممنوع كتابتها كوعد)

### ادّعاءات مضمونة (تُحجَب فوراً)

`نضمن` · `نضمن لك` · `نضمن النتائج` · `guaranteed` (sales/results/ROI) · أي صياغة «دليل/شهادة مزيّفة» (fake proof / fake testimonial).

**البديل المسموح:** «فرص مُثبتة بأدلة» / **evidenced opportunities** — نَصِف ما يمكن إثباته، لا نتيجة نَعِد بها.

### لغة قناة ممنوعة (تُحجَب)

`cold whatsapp` (واتساب بارد) · `linkedin automation` (أتمتة لينكدإن) · `blast` (إرسال جماعي).

**البديل المسموح:** قنوات يدوية صريحة — واتساب لجهة تعرفها يدوياً، لينكدإن يدوي، بريد ترسله بنفسك.

### مصطلحات كشط/إرسال آلي (تُحجَب)

كشط البيانات (scraping) · قوائم مشتراة (purchased list) · إرسال تلقائي بلا موافقة (auto-send / send automatically without approval).

**البديل المسموح:** مصادر Tier-1 مشروعة + مسودة + موافقة + إرسال يدوي.

> لا تظهر هذه الكلمات في أي مسودة عميل أو مادة تسويق. وجودها هنا حصراً لتغذية الفحص الحتمي حتى **يمنعها**.

---

## 3) الشروط البنيوية (يجب أن تتحقق)

| الشرط | القيمة المطلوبة |
|-------|------------------|
| `approval_required` | `true` دائماً — لا استثناء |
| `evidence_level` | ضمن `L0`–`L5` (انظر [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md)) |
| `channel` | قناة يدوية من تعداد [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) §2 |
| `next_action` | غير فارغة |
| PII في `body`/`subject` | غير مسموح |

---

## 4) المخرَج: `DRAFT_QUALITY_REPORT.md`

لكل مسودة، يطبع التقرير سطراً:

```text
[PASS]  drf_2026_0001  channel=email           evidence=L1  approval_required=true
[BLOCK] drf_2026_0007  reason=forbidden_claim:guaranteed results
[BLOCK] drf_2026_0011  reason=forbidden_channel_language (blast)
```

- **PASS** → تنتقل المسودة إلى `pending_approval` وتظهر في طابور المراجعة.
- **BLOCK** → لا تظهر للمؤسس؛ تُسجَّل مع سبب الحجب لإصلاح المولّد.

---

## 5) كيف تُصلِح BLOCK

| السبب | الإصلاح |
|-------|---------|
| `forbidden_claim:*` | احذف الوعد المضمون؛ استبدله بـ «فرص مُثبتة بأدلة» |
| `forbidden_channel_language` | احذف لغة الواتساب البارد/أتمتة لينكدإن/الإرسال الجماعي |
| `forbidden_term:*` | احذف ذكر الكشط/القوائم المشتراة/الإرسال الآلي |
| قناة غير صالحة | بدّل إلى قناة يدوية صحيحة |
| مستوى إثبات مفقود | عيّن `L0`–`L5` المناسب |

الإصلاح يكون في **مُولّد المسودات** ([`scripts/generate_distribution_drafts.py`](../../scripts/generate_distribution_drafts.py)) أو في قالب الزاوية — لا في تجاوز البوابة.

---

## 6) قاعدة ذهبية

> بوابة الجودة لا تُعطَّل ولا تُتجاوز. إن حجبت مسودة، فالمسودة خطأ — وليست البوابة. الحوكمة سبب اختيار Dealix، لا عائق أمامه.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

*يُبنى في هذا الـ PR. آخر تحديث: 2026-06-02.*
