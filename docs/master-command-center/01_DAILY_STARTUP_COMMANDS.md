# أوامر التشغيل اليومية | Daily Startup Commands

## الغرض | Purpose

**عربي:** هذا الملف يحدد الأوامر التي يشغّلها المؤسس يوميًا لتجهيز عمل اليوم في Dealix. كل أمر يُنتج مخرجات للمراجعة والاعتماد فقط — لا يُرسل ولا ينشر شيئًا خارجيًا تلقائيًا. التنفيذ الخارجي يدوي وبموافقة المؤسس دائمًا.

**English:** This file defines the commands the founder runs daily to prepare the day's work in Dealix. Each command produces outputs for review and approval only — nothing is sent or published externally on its own. External action is always manual and founder-approved.

---

## المبدأ الحاكم | Governing Principle

> الذكاء الاصطناعي يُجهّز، المؤسس يوافق، الإجراء يدوي فقط، لا إرسال خارجي تلقائي.
> AI prepares, Founder approves, Manual action only, No automated external sending.

---

## تسلسل التشغيل اليومي | Daily Run Sequence

شغّل الأوامر بالترتيب التالي | Run the commands in this order:

```bash
# 1) توليد مسودات تجارية (للمراجعة فقط)
python scripts/commercial_generate_400_drafts.py --target 400

# 2) بناء صف إجراءات المؤسس
python scripts/founder_action_queue_generate.py

# 3) لوحة الإيراد للمؤسس
python scripts/founder_revenue_dashboard.py

# 4) موجز المدير التنفيذي اليومي
python scripts/daily_ceo_brief_generate.py

# 5) التحقق من تنفيذ الإيراد
python scripts/revenue_execution_verify.py
```

---

## ماذا يفعل كل أمر | What Each Command Does

| الأمر Command | المخرَج Output | السلامة Safety |
|---|---|---|
| `commercial_generate_400_drafts.py --target 400` | مسودات تجارية للمراجعة | لا إرسال، مسودات فقط Drafts only |
| `founder_action_queue_generate.py` | قائمة إجراءات اليوم للمؤسس | يدوي Manual approval |
| `founder_revenue_dashboard.py` | لوحة حالة الإيراد | قراءة فقط Read-only |
| `daily_ceo_brief_generate.py` | موجز قرارات اليوم | للمراجعة For review |
| `revenue_execution_verify.py` | تحقق من أن التنفيذ يسير | تحقق Verification |

---

## ماذا يراجع المؤسس | What the Founder Reviews

1. **صف الإجراءات Action queue:** اختر أهم المهام؛ نفّذ التواصل يدويًا فقط.
2. **المسودات Drafts:** راجع الصياغة — لا ادعاءات غير مثبتة، لا ضمان عائد.
3. **لوحة الإيراد Revenue:** تابع الأرقام الحقيقية فقط.
4. **الموجز Brief:** قرارات اليوم وأولوياته.
5. **التحقق Verify:** عالج أي إخفاق يظهره `revenue_execution_verify.py`.

---

## أين المخرجات | Where Outputs Live

- المسودات وصف الإجراءات والتقارير تُكتب في مسارات المخرجات المعتمدة للسكربتات (راجع تشغيل كل سكربت محليًا).
- لا تُخزَّن أي أسرار أو مفاتيح API في المخرجات. No secrets in outputs.

---

## حدود السلامة اليومية | Daily Safety Boundaries

- لا إرسال آلي للبريد/واتساب/لينكدإن. كل تواصل يدوي. No automated sending.
- لا كشط بيانات، لا إطلاق إعلانات حية. No scraping, no live ads.
- لا أرقام نجاح وهمية في أي مخرَج. No fake traction.

> إن ظهر أي خطر، انتقل إلى `docs/crisis-os/01_KILL_SWITCH_POLICY.md`.
