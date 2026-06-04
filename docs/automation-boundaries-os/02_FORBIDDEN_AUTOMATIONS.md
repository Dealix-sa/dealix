# الأتمتة الممنوعة | Forbidden Automations

> **AR:** يعدّد هذا المستند الأفعال التي لا يجوز للأتمتة تنفيذها مطلقًا. القاسم المشترك أنها **أفعال خارجية** تترك أثرًا في العالم: إرسال، تقديم، كشط، إطلاق. كل هذه تبقى يدوية وبموافقة المؤسس أو لا تحدث.
>
> **EN:** This document lists actions automation must never perform. Common thread: they are *external actions* that leave a mark in the world — sending, submitting, scraping, launching. All stay manual with founder approval, or do not happen.

## القائمة الممنوعة | Forbidden List

| العملية Operation | السبب Reason |
|---|---|
| Send email | فعل خارجي يمسّ السمعة والامتثال / external action affecting reputation & compliance |
| Send WhatsApp | تواصل مباشر يتطلب موافقة بشرية / direct contact requiring human approval |
| Automate LinkedIn | يخالف شروط المنصّة ويضرّ الثقة / violates platform terms, harms trust |
| Submit forms | تقديم آلي قد يلتزم بما لم يُراجَع / auto-commit to unreviewed content |
| Scrape | جمع بيانات غير مشروع / illegitimate data collection |
| Launch ads (live) | صرف مالي وأثر عام بلا موافقة / spend & public impact without approval |
| Process sensitive data without agreement | خرق خصوصية / privacy breach |

## لماذا هذه ممنوعة | Why These Are Forbidden

- تترك أثرًا خارجيًا لا يمكن التراجع عنه بسهولة. / They leave hard-to-reverse external effects.
- تخالف قواعد الأمان الأساسية للمشروع. / They violate the project's core safety rules.
- تنزع القرار النهائي من يد المؤسس. / They remove the final decision from the founder.

## البديل المعتمد | Approved Alternative

| بدل أن Instead of | افعل Do |
|---|---|
| إرسال بريد آليًا / auto-send email | توليد مسودّة + إرسال يدوي / draft + manual send |
| كشط بيانات / scraping | إدخال يدوي من مصدر مشروع / manual entry from legitimate source |
| تقديم نموذج / auto-submit | مسودّة جاهزة للتقديم اليدوي / ready draft for manual submit |
| إطلاق إعلان / launch ad | خطة إعلان للمراجعة / ad plan for review |

## قاعدة عدم التجاوز | No-Override Rule

> لا يوجد علم (flag) أو إعداد يفعّل هذه العمليات آليًا. أي طلب بذلك يُرفَض ويُسجَّل.
> No flag or setting enables these automatically. Any such request is rejected and logged.

> **AI prepares, Founder approves, Manual action only, No external sending.**

## معالجة المخالفات | Violation Handling

- يُرفَض الطلب الممنوع فورًا ويُعرَض البديل المعتمد. / The forbidden request is refused immediately and the approved alternative offered.
- يُسجَّل الرفض في سجل التدقيق مع السبب. / The refusal is logged in the audit trail with reason.
- لا يوجد تجاوز إداري يفعّل العملية الممنوعة. / No admin override enables the forbidden operation.

## مراجع | References

- المسموح / Allowed: `01_ALLOWED_AUTOMATIONS.md`
- التقرير الإثباتي / Evidence report: `99_AUTOMATION_BOUNDARIES_REPORT.md`
