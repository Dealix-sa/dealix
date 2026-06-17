# Data Retention & Deletion — What We Keep, How Long, How to Erase — سياسة الاحتفاظ بالبيانات وحذفها

> Governance OS status: **BETA**. Enforced in controlled trials.
> حالة نظام الحوكمة: **BETA**. مُطبّقة في التجارب المحكومة.

Cross-links: [`MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md) · [`GOVERNANCE_OS.md`](../05_governance_os/GOVERNANCE_OS.md) · [`PRIVACY_AND_PDPL_READINESS.md`](./PRIVACY_AND_PDPL_READINESS.md) · [`RESEARCH_SOURCE_POLICY.md`](./RESEARCH_SOURCE_POLICY.md)

---

## EN — Why retention clarity is a differentiator

A post-PDPL study of Saudi e-commerce found that only about 31% of sampled sites disclosed all four checked privacy elements: retention period, right to erasure, right to a copy, and a complaints mechanism. Most businesses leave these unclear. Dealix states all four plainly. Clear retention and deletion is a genuine differentiator, and this document is where we make it explicit.

### What data we keep

- **Engagement records.** Project scope, deliverables, Proof Pack contents, and approval logs needed to run and account for the work.
- **Operational data.** Anonymized outreach records, opt-out flags, and decision logs — referenced by label, never by raw personal identifier.
- **Minimal contact data.** Only the contact information a customer knowingly provides for the engagement, held to fulfil it.

### What we do not keep

- **No PII in logs.** Logs reference people by anonymized label. Raw personal identifiers do not enter operational or system logs.
- **No client data in model training.** Customer or third-party data is never used to train models. The engagement is the boundary of its use.
- **No harvested personal data.** Nothing collected by scraping or behind a login enters our records, per [`RESEARCH_SOURCE_POLICY.md`](./RESEARCH_SOURCE_POLICY.md).

### How long we keep it

| Data type | Retention | Trigger to delete |
|---|---|---|
| Active engagement data | Duration of the engagement | Engagement ends, then retention window |
| Proof Pack & approval records | Retained for accountability of delivered work | Erasure request or end of agreed window |
| Anonymized operational logs | Limited, time-boxed window | End of window, then deletion |
| Opt-out flags | Kept to honor the opt-out | Retained to prevent re-contact |

A specific retention window is agreed in writing per engagement. We do not keep data "just in case."

### The four rights we make explicit

- **Right to a copy.** A data subject may request a copy of the personal data we hold about them.
- **Right to erasure.** A data subject may request deletion; we delete within the agreed window, except where a lawful basis requires limited retention (and we say which).
- **Retention period.** Stated per engagement, not left implicit.
- **Complaints mechanism.** A named channel to raise a privacy concern, with a committed response path.

Honoring these rights is operational, not aspirational. Requests route through the approval flow in [`HUMAN_APPROVAL_POLICY.md`](./HUMAN_APPROVAL_POLICY.md) so a named human owns each one.

---

## AR — لماذا وضوح الاحتفاظ فارق حقيقي

وجدت دراسة للتجارة الإلكترونية السعودية بعد PDPL أن نحو 31% فقط من المواقع المعاينة أفصحت عن العناصر الأربعة المفحوصة: مدة الاحتفاظ، حق المحو، حق الحصول على نسخة، وآلية الشكاوى. معظم الأعمال تترك ذلك غامضاً. تذكر Dealix الأربعة بوضوح. وضوح الاحتفاظ والحذف فارق حقيقي، وهذا المستند هو حيث نجعله صريحاً.

### ما البيانات التي نحتفظ بها

- **سجلات الارتباط.** نطاق المشروع، المُخرجات، محتويات حزمة الإثبات، وسجلات الموافقة اللازمة لتشغيل العمل ومحاسبته.
- **بيانات تشغيلية.** سجلات تواصل مجهولة، أعلام إلغاء الاشتراك، وسجلات القرار — يُشار إليها بوسم لا بمعرّف شخصي خام.
- **بيانات تواصل دنيا.** فقط معلومات التواصل التي يقدّمها العميل عن علم للارتباط، تُحفظ لإتمامه.

### ما لا نحتفظ به

- **لا بيانات شخصية في السجلات.** تشير السجلات إلى الأشخاص بوسم مجهول. لا تدخل المعرّفات الشخصية الخام السجلات التشغيلية أو النظامية.
- **لا بيانات عملاء في تدريب النماذج.** لا تُستخدم بيانات العميل أو طرف ثالث في تدريب النماذج أبداً. الارتباط هو حدّ استخدامها.
- **لا بيانات شخصية محصودة.** لا يدخل سجلاتنا أي شيء جُمع بالكشط أو خلف تسجيل دخول، وفق [`RESEARCH_SOURCE_POLICY.md`](./RESEARCH_SOURCE_POLICY.md).

### كم نحتفظ بها

| نوع البيانات | الاحتفاظ | مُحفّز الحذف |
|---|---|---|
| بيانات الارتباط النشط | مدة الارتباط | انتهاء الارتباط ثم نافذة الاحتفاظ |
| حزمة الإثبات وسجلات الموافقة | تُحفظ لمحاسبة العمل المُسلَّم | طلب محو أو انتهاء النافذة المتفق عليها |
| السجلات التشغيلية المجهولة | نافذة محدودة زمنياً | انتهاء النافذة ثم الحذف |
| أعلام إلغاء الاشتراك | تُحفظ لاحترام إلغاء الاشتراك | تُبقى لمنع إعادة التواصل |

تُتفق نافذة احتفاظ محددة كتابةً لكل ارتباط. ولا نحتفظ بالبيانات "تحسّباً".

### الحقوق الأربعة التي نجعلها صريحة

- **حق الحصول على نسخة.** لصاحب البيانات أن يطلب نسخة من بياناته الشخصية لدينا.
- **حق المحو.** لصاحب البيانات أن يطلب الحذف؛ نحذف خلال النافذة المتفق عليها، إلا حيث يتطلب أساس نظامي احتفاظاً محدوداً (ونبيّن أيّها).
- **مدة الاحتفاظ.** تُذكر لكل ارتباط، لا تُترك ضمنية.
- **آلية الشكاوى.** قناة مُسمّاة لرفع شأن خصوصية، مع مسار استجابة ملتزم.

احترام هذه الحقوق تشغيلي لا طموحي. تمرّ الطلبات عبر مسار الموافقة في [`HUMAN_APPROVAL_POLICY.md`](./HUMAN_APPROVAL_POLICY.md) ليملك كلّاً منها إنسان مُسمّى.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
