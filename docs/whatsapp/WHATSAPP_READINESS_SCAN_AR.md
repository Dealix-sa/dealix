# فحص الجاهزية على واتساب — WhatsApp Readiness Scan

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس (سامي)
**جزء من التدفّق:** docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md (الخطوة 2)
**القوالب:** data/templates/whatsapp_templates_collection.md
**آخر تحديث:** 2026-06-02

---

## الغرض

أسئلة قصيرة 1:1 تُطرَح **بعد ردّ إيجابي أو موافقة فقط** لاختيار العرض المناسب من السلّم المعتمد. الفحص محادثة طبيعية لا استمارة طويلة — هدفه فهم كافٍ لتجهيز بطاقة عرض دقيقة.

## شرط ما قبل الفحص

- يُطرَح **فقط** بعد أن يختار العميل واتساب عقب ردّ إيجابي (انظر التدفّق).
- لا فحص بلا موافقة واردة. لا يُرسَل جماعياً.

## الأسئلة الخمسة القصيرة

| المحور | السؤال (1:1) | يُغذّي اختيار |
|--------|---------------|----------------|
| المصادر | «وين بياناتكم الحالية — CRM، جداول، ولا متفرّقة؟» | جودة البيانات / مدى التشخيص |
| حجم العملاء | «كم عميل محتمل يدخل عندكم شهرياً تقريباً؟» | حجم العمل / طبقة السلّم |
| الأدوات الحالية | «تستخدمون أي أداة الآن للمتابعة والمبيعات؟» | التكامل / هامش التنفيذ |
| صانع القرار | «مين يقرّر في موضوع زي هذا عندكم؟» | مسار الموافقة / نوع العرض |
| التوقيت | «تفكرون تبدؤون قريب ولا تستكشفون الآن؟» | الإلحاح / نقطة الدخول |

> الأسئلة تُطرَح بالتدريج في المحادثة، لا دفعة واحدة. كل رسالة تُعتمَد من المؤسس قبل الإرسال.

## كيف يُترجَم الفحص إلى عرض

| الإشارة من الفحص | العرض المرشَّح من السلّم |
|-------------------|--------------------------|
| بيانات متفرّقة، فضول، لا التزام | التشخيص المجاني (0) |
| رغبة في دليل سريع بسعر ثابت | Revenue Intelligence Sprint (499) |
| بيانات قائمة تحتاج ترتيباً | Data-to-Revenue Pack (1,500) |
| حاجة تشغيل مستمرّ | Managed Revenue Ops (2,999–4,999/شهر) |
| إعداد مخصّص أو حوكمة مؤسسية | Custom AI Setup / Enterprise Governance Review |

## الحدود

- لا بيانات شخصية حسّاسة تُطلَب أو تُخزَّن (هوية وطنية، أرقام خاصة).
- ما يُجمَع يُوثَّق مصدره ويخدم اختيار العرض فقط.
- لا «نضمن» نتيجة بناءً على الإجابات؛ الفحص يرشّح عرضاً، لا يَعِد بنتيجة.

## الخطوة التالية

بعد الفحص: اختر العرض من الجدول، وجهّز بطاقة العرض المناسبة من docs/whatsapp/WHATSAPP_ACTION_CARDS_AR.md للموافقة، وحدّث الصفّ في reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE.md.

## English summary

A short, conversational 1:1 readiness scan asked only after a positive reply or consent, to select the right offer from the canonical ladder. Five lightweight questions: data sources (CRM / sheets / scattered), monthly lead volume, current tools, decision-maker, and timeline — asked gradually in conversation, each message founder-approved, never bulk. The scan maps to offers: scattered data and curiosity → free diagnostic (0); a fast fixed-price proof → Revenue Intelligence Sprint (499); existing data needing ranking → Data-to-Revenue Pack (1,500); ongoing operations → Managed Revenue Ops (2,999–4,999/mo); custom or enterprise needs → Custom AI Setup or Enterprise Governance Review. No sensitive personal data (national ID, private numbers) is requested or stored; what is collected is source-documented and used only to select an offer. The scan recommends an offer — it never promises a result. Part of docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
