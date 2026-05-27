# Hermes Agent OS — نظام وكلاء Dealix

Hermes هو طبقة وكلاء داخلية تعمل لصالح المؤسس. الهدف ليس أن تتحرك عشوائيًا، بل أن تجمع الإشارات، تراجع الأدلة، تنتج تقارير، وتضع قائمة قرارات تحتاج موافقة.

## القاعدة الأساسية

- القراءة والتحليل مسموحة.
- الكتابة الداخلية في `docs/hermes/runtime/` مسموحة.
- أي تواصل خارجي يحتاج موافقة.
- أي deploy أو rollback يحتاج موافقة.
- أي تعامل مع أسرار أو بيانات حساسة يحتاج موافقة.
- أي claim عام يحتاج evidence.

## الوكلاء

| Agent | الدور |
|---|---|
| Founder Chief of Staff | أجندة المؤسس وقرارات اليوم |
| Revenue Pipeline Agent | فرص الإيراد والتأهيل والمتابعة |
| Customer Success Agent | نجاح العملاء والتحويل إلى retained value |
| Product Strategy Agent | ربط المنتج بالإيراد والثقة |
| Reliability SRE Agent | الصحة والنشر والنسخ الاحتياطي |
| Security and Compliance Agent | الأسرار، OWASP، المخاطر، الموافقات |
| AI Governance Agent | تقييم أدوات AI وحدود الاستقلالية |
| Finance and Unit Economics Agent | التسعير والتكلفة والهامش |
| Integration and Vendor Agent | مزودين وتكاملات وفallbacks |
| Documentation and Proof Agent | الأدلة والوثائق وإثباتات الإطلاق |
| Growth Experiments Agent | تجارب نمو منخفضة المخاطر |
| Hermes Orchestrator | يلخص، يوجه، وينتج action queue |

## الملفات الأساسية

- `dealix/hermes/agents.yaml`
- `dealix/hermes/policies.yaml`
- `dealix/hermes/tools.yaml`
- `scripts/hermes_generate_reports.py`
- `docs/hermes/runtime/`

## التشغيل المحلي

```bash
python scripts/hermes_generate_reports.py
```

لتقرير وكيل واحد:

```bash
python scripts/hermes_generate_reports.py --agent reliability-sre-agent
```

## التشغيل على السيرفر

السكريبت آمن افتراضيًا: يقرأ ملفات الريبو وينتج تقارير داخلية فقط. يمكن تشغيله عبر cron أو systemd timer.

## مخرجات Hermes

- `docs/hermes/runtime/hermes_digest.md`
- `docs/hermes/runtime/hermes_action_queue.md`
- تقرير مستقل لكل وكيل.

## متى نسمح بالاستقلالية؟

| نوع العمل | استقلالية؟ |
|---|---|
| تلخيص داخلي | نعم |
| ترتيب backlog | نعم |
| كتابة تقرير داخلي | نعم |
| إرسال رسالة عميل | لا، موافقة مطلوبة |
| deploy/rollback | لا، موافقة مطلوبة |
| التعامل مع أسرار | لا، موافقة مطلوبة |
| تغيير إنتاج | لا، موافقة مطلوبة |

## دورة 24 ساعة

1. صباحًا: توليد digest وaction queue.
2. أثناء اليوم: مراجعة health/deploy/security/customer signals.
3. عند وجود incident: تشغيل reliability + security agents.
4. نهاية الأسبوع: weekly review وربط القرارات بالإيراد والثقة.

## مبدأ التصميم

Hermes يخدم المؤسس، لكنه لا يتجاوز المؤسس. كل ما له أثر خارجي أو مالي أو إنتاجي يمر عبر قائمة موافقات واضحة.