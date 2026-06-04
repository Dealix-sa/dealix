# صفحة تحكّم المؤسس | Founder One-Page Control

## الغرض | Purpose

**عربي:** صفحة واحدة تخبر المؤسس بكل ما يحتاجه لإدارة Dealix: ماذا يشغّل يوميًا، ماذا يراجع، أين المخرجات، ومتى يبيع ويوقف ويرفع السعر ويوظّف ويتوسّع ويطلق إعلانًا — ومتى لا يفعل شيئًا. كل تنفيذ خارجي يدوي وبموافقة المؤسس، ولا إرسال خارجي تلقائي.

**English:** One page telling the founder everything needed to run Dealix: what to run daily, what to review, where outputs are, and when to sell, stop, raise price, hire, expand, launch an ad — and when to do nothing. Every external action is manual and founder-approved; no automated external sending.

---

## المبدأ الحاكم | Governing Principle

> الذكاء الاصطناعي يُجهّز، المؤسس يوافق، الإجراء يدوي فقط، لا إرسال خارجي تلقائي.
> AI prepares, Founder approves, Manual action only, No automated external sending.

---

## ماذا تشغّل يوميًا | Run Daily

```bash
python scripts/commercial_generate_400_drafts.py --target 400
python scripts/founder_action_queue_generate.py
python scripts/founder_revenue_dashboard.py
python scripts/daily_ceo_brief_generate.py
python scripts/revenue_execution_verify.py
```

## ماذا تراجع | Review

- صف الإجراءات: نفّذ أهم 3–5 مهام تواصل **يدويًا**.
- المسودات: لا ادعاءات غير مثبتة، لا ضمان عائد.
- لوحة الإيراد والموجز: أرقام حقيقية فقط.

## أين المخرجات | Where Outputs Are

- مخرجات السكربتات في مسارات الإخراج المعتمدة محليًا (مسودات، صف، تقارير).
- لا أسرار أو مفاتيح API في أي مخرَج. No secrets in outputs.

---

## متى تقرر | Decision Triggers

| الموقف Situation | الإشارة Signal | القرار Decision |
|---|---|---|
| متى تبيع Sell | خط أنابيب صحي + تسليم مستقر | تواصل يدوي مكثّف Push outreach (manual) |
| متى توقف Stop | شكوى/تسريب/خطأ تواصل | فعّل Crisis OS kill switches |
| متى ترفع السعر Raise price | طلب يفوق السعة + إثبات قيمة | ارفع السعر تدريجيًا |
| متى توظّف Hire | تسليم متكرر يتجاوز طاقتك | وظّف دعم تسليم |
| متى توسّع قطاعًا Expand vertical | قطاع حالي مستقر ومربح | ادخل قطاعًا مجاورًا |
| متى تطلق إعلانًا Launch ad | قناة عضوية مثبتة + ميزانية | خطّط واعتمد يدويًا (لا إطلاق حي تلقائي) |
| متى لا تفعل شيئًا Do nothing | لا إشارة واضحة / تسليم تحت ضغط | حافظ على الإيقاع، ركّز على الجودة |

---

## أوقات أخرى | Other Cadence

- **أسبوعيًا:** `weekly_board_report_generate.py`، `market_intelligence_brief_generate.py`، `master_startup_command_verify.py`.
- **شهريًا:** مراجعة شاملة وقرارات توسّع (انظر `03_MONTHLY_STARTUP_COMMANDS.md`).

---

## خطوط حمراء | Hard Stops

- لا إرسال آلي للبريد/واتساب/لينكدإن. No automated sending.
- لا كشط، لا إطلاق إعلانات حية تلقائيًا، لا نشر تلقائي.
- لا أرقام وهمية، لا ضمان عائد، لا ادعاءات غير مثبتة.
- لا أسرار في أي مخرَج. عند الخطر: `docs/crisis-os/01_KILL_SWITCH_POLICY.md`.

> اطبع هذه الصفحة. هي لوحة قيادتك اليومية.
