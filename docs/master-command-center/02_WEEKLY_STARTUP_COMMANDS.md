# أوامر التشغيل الأسبوعية | Weekly Startup Commands

## الغرض | Purpose

**عربي:** يحدد هذا الملف الأوامر التي يشغّلها المؤسس أسبوعيًا لمراجعة الأداء وتجهيز قرارات الأسبوع في Dealix. كل المخرجات للمراجعة والاعتماد، ولا إرسال خارجي تلقائي. الهدف: صورة أسبوعية واضحة للمجلس وللسوق ولصحة التشغيل.

**English:** This file defines the commands the founder runs weekly to review performance and prepare the week's decisions in Dealix. All outputs are for review and approval, with no automated external sending. Goal: a clear weekly picture of the board, the market, and operating health.

---

## المبدأ الحاكم | Governing Principle

> الذكاء الاصطناعي يُجهّز، المؤسس يوافق، الإجراء يدوي فقط, لا إرسال خارجي تلقائي.
> AI prepares, Founder approves, Manual action only, No automated external sending.

---

## تسلسل التشغيل الأسبوعي | Weekly Run Sequence

```bash
# 1) تقرير المجلس الأسبوعي
python scripts/weekly_board_report_generate.py

# 2) موجز ذكاء السوق
python scripts/market_intelligence_brief_generate.py

# 3) التحقق من أوامر مركز القيادة
python scripts/master_startup_command_verify.py
```

---

## ماذا يفعل كل أمر | What Each Command Does

| الأمر Command | المخرَج Output | السلامة Safety |
|---|---|---|
| `weekly_board_report_generate.py` | تقرير أداء أسبوعي للمجلس | للمراجعة For review |
| `market_intelligence_brief_generate.py` | موجز إشارات السوق | لا كشط No scraping |
| `master_startup_command_verify.py` | تحقق من اكتمال المركز وأدلته | تحقق Verification |

---

## مراجعة المؤسس الأسبوعية | Weekly Founder Review

1. **تقرير المجلس Board report:** اتجاه الإيراد، خط الأنابيب، المخاطر.
2. **ذكاء السوق Market intel:** إشارات حقيقية فقط؛ لا استنتاجات مبالغ فيها.
3. **التحقق Verify:** عالج أي فجوة يكشفها `master_startup_command_verify.py`.
4. **قرارات الأسبوع Weekly decisions:** التسعير، التركيز، التوظيف (انظر الملف الشهري للقرارات الأكبر).

---

## أسئلة القرار الأسبوعية | Weekly Decision Questions

| السؤال Question | الإشارة Signal |
|---|---|
| هل نبيع أكثر؟ Sell more? | خط أنابيب صحي + تسليم مستقر |
| هل نوقف قناة؟ Stop a channel? | شكاوى أو ضعف تحويل |
| هل نراجع التسعير؟ Revisit pricing? | طلب أعلى من السعة |

---

## حدود السلامة | Safety Boundaries

- لا إرسال آلي ولا نشر تلقائي لأي تقرير. No automated sending/publishing.
- لا كشط بيانات السوق؛ مصادر مشروعة فقط. No scraping.
- لا أرقام وهمية ولا ضمان عائد في تقارير المجلس. No fake traction / guaranteed ROI.
- لا أسرار أو مفاتيح API في أي مخرَج. No secrets in outputs.

> ملاحظة: `master_startup_command_verify.py` يتحقق من اكتمال مركز القيادة وأدلته.
