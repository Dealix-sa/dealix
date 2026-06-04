# نظام إدارة الأزمات ومفتاح الإيقاف | Crisis OS

## الغرض | Purpose

**عربي:** نظام إدارة الأزمات (Crisis OS) هو طبقة الحماية العليا في Dealix. يوفّر إجراءات واضحة لإيقاف أي نشاط فوري عند ظهور خطر، وحماية السمعة والبيانات والعملاء. كل إجراء يبقى يدويًا وتحت موافقة المؤسس، ولا يتم أي إرسال خارجي تلقائي.

**English:** The Crisis OS is the top protection layer in Dealix. It provides clear procedures to halt any activity the moment a risk appears, and to protect reputation, data, and clients. Every action remains manual and founder-approved; no external sending happens automatically.

---

## المبادئ الأساسية | Core Principles

- **الذكاء الاصطناعي يُجهّز، المؤسس يوافق | AI prepares, Founder approves** — لا قرار خارجي بدون مراجعة بشرية.
- **إجراء يدوي فقط | Manual action only** — لا إرسال آلي للبريد أو واتساب أو لينكدإن.
- **لا استخلاص بيانات | No scraping** — لا جمع بيانات آلي من مصادر خارجية.
- **لا إطلاق إعلانات مدفوعة حيّة | No live paid ads** — التخطيط فقط حتى موافقة صريحة.
- **لا أرقام وهمية | No fake traction** — لا ادعاءات غير مثبتة ولا ضمان عائد.
- **لا أسرار | No secrets** — لا تخزين مفاتيح API أو بيانات حساسة في المخرجات.

---

## مكونات النظام | System Components

| الملف | Path | الغرض | Purpose |
|------|------|-------|---------|
| سياسة مفتاح الإيقاف | `01_KILL_SWITCH_POLICY.md` | إيقاف كل الطبقات | Kill all layers |
| سياسة إيقاف التواصل | `02_OUTREACH_STOP_POLICY.md` | إيقاف كل التواصل | Stop all outreach |
| دليل الحوادث الأمنية | `03_SECURITY_INCIDENT_PLAYBOOK.md` | استجابة أمنية (PDPL) | Security response |
| دليل حوادث السمعة | `04_REPUTATION_INCIDENT_PLAYBOOK.md` | حماية السمعة | Reputation defense |
| دليل فشل التسليم | `05_CLIENT_DELIVERY_FAILURE_PLAYBOOK.md` | تعافي التسليم | Delivery recovery |
| تقرير الأدلة | `99_CRISIS_OS_REPORT.md` | إثبات الجاهزية | Evidence report |

---

## متى يُفعّل النظام | When to Activate

- اشتباه في تسريب بيانات أو وصول غير مصرّح به.
- شكوى عامة أو خطر على السمعة.
- فشل في تسليم خدمة لعميل.
- خطأ في مصنع المسودات أو جداول العمل.
- أي إشارة خطر يرصدها تقرير السلامة.

---

## مسار التصعيد | Escalation Path

1. **رصد** الإشارة (تلقائي أو يدوي).
2. **تجميد** النشاط المتأثر عبر مفتاح الإيقاف المناسب.
3. **تجهيز** ملخص الحادث بواسطة الذكاء الاصطناعي.
4. **مراجعة المؤسس** واتخاذ القرار.
5. **استئناف** بعد موافقة المؤسس فقط.

> ملاحظة | Note: لا يُستأنف أي نشاط دون موافقة صريحة من المؤسس وتوثيقها في تقرير الأدلة.
