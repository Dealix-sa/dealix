# نظام حدود الأتمتة | Automation Boundaries OS

> **AR:** يحدّد هذا النظام الخط الفاصل بين ما يُسمح للأتمتة بفعله وما يبقى حصرًا بيد المؤسس. القاعدة الجوهرية: الذكاء يُحضّر، المؤسس يعتمد، والفعل الخارجي يدوي فقط. لا إرسال خارجي ولا كشط ولا تقديم نماذج آليًا.
>
> **EN:** This OS defines the line between what automation may do and what stays exclusively with the founder. Core rule: AI prepares, founder approves, external action manual only. No external sending, no scraping, no auto-submission.

## لماذا هذا النظام | Why This OS

- يمنع أي فعل خارجي تلقائي قد يضرّ بالسمعة أو يخالف الأنظمة. / Prevents any automatic external action that could harm reputation or violate regulations.
- يجعل الحدود صريحة وقابلة للتدقيق بدل أن تكون ضمنية. / Makes boundaries explicit and auditable instead of implicit.
- يحمي الثقة عبر إبقاء القرار النهائي بشريًا. / Protects trust by keeping the final decision human.

## مكوّنات النظام | OS Components

| المستند Document | الدور Role |
|---|---|
| `01_ALLOWED_AUTOMATIONS.md` | ما يُسمح به / What is allowed |
| `02_FORBIDDEN_AUTOMATIONS.md` | ما هو ممنوع / What is forbidden |
| `03_HUMAN_APPROVAL_GATES.md` | بوابات الموافقة البشرية / Human approval gates |
| `04_CHANNEL_BOUNDARIES.md` | حدود كل قناة / Per-channel boundaries |
| `05_AI_AGENT_BOUNDARIES.md` | حدود وكلاء الذكاء / AI agent boundaries |
| `99_AUTOMATION_BOUNDARIES_REPORT.md` | التقرير الإثباتي / Evidence report |

## المبدأ الحاكم | Governing Principle

> **AI prepares, Founder approves, Manual action only, No external sending.**

- الأتمتة تُنتج **مصنوعات** (مسودّات، تقارير، تشخيصات) لا **أفعالًا**. / Automation produces *artifacts* (drafts, reports, diagnostics), not *actions*.
- كل فعل خارجي يمرّ ببوابة موافقة بشرية. / Every external action passes a human approval gate.

## ملخّص الحدود | Boundary Summary

| الفئة Category | الحالة Status |
|---|---|
| توليد المسودّات والتقارير / Draft & report generation | مسموح / Allowed |
| التقييم والترتيب والتشخيص / Scoring, ranking, diagnostics | مسموح / Allowed |
| إرسال بريد/واتساب/لينكدإن / Sending email/WhatsApp/LinkedIn | ممنوع / Forbidden |
| الكشط / Scraping | ممنوع / Forbidden |
| تقديم نماذج آليًا / Auto form submission | ممنوع / Forbidden |
| إطلاق إعلانات مدفوعة / Live paid ads | ممنوع / Forbidden |

## مراجع | References

- التقرير الإثباتي / Evidence report: `99_AUTOMATION_BOUNDARIES_REPORT.md`
- الذاكرة التشغيلية / Operating memory: `../operating-memory-os/00_OPERATING_MEMORY_OS.md`
