# كيت مكالمة الاكتشاف — Discovery Call Kit (20 minutes)

> **العربية أولاً · English parallel below.**
> سكربت مكالمة ٢٠ دقيقة: افتتاح → تأهيل (BANT-lite) → تشخيص الألم → عرض السلّم
> والمسار المخصص → معالجة أهم ٦ اعتراضات → إغلاق إلى تشخيص/Sprint مدفوع أو مكالمة
> تالية محجوزة. بنهايته متتبّع مكالمة بسيط.

> يوسّع هذا الكيت السكربت المختصر في
> [`../docs/29_sales_os/DISCOVERY_CALL_SCRIPT.md`](../docs/29_sales_os/DISCOVERY_CALL_SCRIPT.md)
> ولا يكرره. التأهيل مبني على
> [`LEAD_INTAKE_FRAMEWORK_AR.md`](LEAD_INTAKE_FRAMEWORK_AR.md).

---

## مخطّط الوقت — Time Map (20 min)

| الدقائق | المرحلة |
|---------|---------|
| ٠–٢ | افتتاح وتأطير — Open & frame |
| ٢–٧ | تأهيل BANT-lite — Qualify |
| ٧–١٢ | تشخيص الألم — Diagnose pain |
| ١٢–١٦ | عرض السلّم + المسار المخصص — Present ladder + custom path |
| ١٦–١٩ | معالجة الاعتراضات — Objections |
| ١٩–٢٠ | إغلاق — Close |

---

## ١. الافتتاح — Open (0–2) (AR)

```
شكرًا على وقتك [الاسم]. عشرين دقيقة فقط، بلا عرض بيع طويل.
هدفي أفهم كيف تدير [الشركة] فرص المبيعات اليوم، وأشوف إن كان فيه ملاءمة.
إن لم تكن، أقول لك بصراحة. نبدأ؟
```

## ٢. التأهيل — Qualify BANT-lite (2–7) (AR)

اسأل بهدوء، سجّل الإشارات:

- **الحاجة (N):** "كيف تتابعون الفرص الآن — CRM، Excel، واتساب؟ أين تشعر أنها تتسرّب؟"
- **السلطة (A):** "من يقرّر عادةً في مثل هذه المبادرات — أنت أم فريق؟"
- **الميزانية (B):** "هل جرّبتم أدوات/خدمات مشابهة؟ ما الميزانية المعتادة للتجربة؟"
- **التوقيت (T):** "هل هذا أولوية الآن أم خلال ٣٠–٦٠ يومًا؟"

> راجع قاعدة القرار في [`LEAD_INTAKE_FRAMEWORK_AR.md`](LEAD_INTAKE_FRAMEWORK_AR.md) §٢.

## ٣. تشخيص الألم — Diagnose (7–12) (AR)

```
سمعتك تقول إن [أعِد صياغة ألمه: مثلًا "الفرص مبعثرة والمتابعة تضيع"].
لو رتبنا بياناتكم الحالية وأظهرنا أفضل ١٠ فرص مرتبة بأولوية، مع مسودات
عربية جاهزة للموافقة — هل يوفّر ذلك وقت فريقك ويكشف فرصًا تفوتكم اليوم؟
```
استمع أكثر مما تتكلم. اربط كل ألم بمخرَج محدد.

## ٤. عرض السلّم + المسار المخصص — Present (12–16) (AR)

| الدرجة | السعر | المخرج |
|--------|-------|--------|
| التشخيص المجاني | ٠ ر.س / ٢٤ ساعة | صفحة واحدة: ٣ فرص + مسودة + خطر |
| Sprint إثبات الإيرادات | ٤٩٩ ر.س / ٧ أيام | Company Brain، أفضل ١٠ فرص، ٥ مسودات، Proof Pack |
| Data-to-Revenue Pack | ١٬٥٠٠ ر.س | بيانات نظيفة، أفضل ٢٠ فرصة، ١٠ مسودات |
| Growth Ops | ٢٬٩٩٩ ر.س/شهر | تشغيل شهري مستمر بالموافقة |
| **Command Sprint (مخصص)** | **٧٬٥٠٠–١٥٬٠٠٠ ر.س لمرة واحدة** | بقيادة المؤسس: عملية إيرادات واحدة → تدفق مدعوم بـAI بنقطة موافقة + SOP + Proof Pack |

```
نبدأ صغيرًا لنثبت القيمة: تشخيص مجاني، ثم Sprint ٤٩٩ ر.س. وإن أردت مسارًا
تنفيذيًا أعمق بقيادتي مباشرة، Command Sprint طبقة تأسيس لمرة واحدة فوق السلّم —
ليست خدمة مُدارة كاملة. أي مسار أقرب لاحتياجك الآن؟
```

> **حوكمة دائمة:** كل المخرجات بموافقة بشرية. لا إرسال خارجي تلقائي، لا scraping،
> لا واتساب بارد، لا ضمان صفقات — "فرص مُثبتة بأدلة".

## ٥. معالجة أهم ٦ اعتراضات — Top 6 Objections (16–19) (AR)

1. **"السعر مرتفع."**
   "نقلّل النطاق قبل الخصم. Sprint ٤٩٩ ر.س هو أصغر التزام، واسترداد كامل خلال ١٤
   يومًا. إن لم نُظهر ≥١٠ فرص، نواصل بلا مقابل."
   → [`../docs/29_sales_os/OBJECTION_PRICE_TOO_HIGH.md`](../docs/29_sales_os/OBJECTION_PRICE_TOO_HIGH.md)

2. **"عندنا CRM بالفعل."**
   "ممتاز — لا نستبدله. نقرأ بياناتكم ونحوّلها إلى فرص مرتبة ومسودات جاهزة.
   الـCRM يخزّن؛ نحن نُخرج قرارًا."

3. **"نبي أتمتة واتساب."**
   "لا نقدّم واتساب آليًا ولا رسائل جماعية — هذا spam ويخالف السياسات. نقدّم
   مسودات بموافقتك ترسلها أنت يدويًا."
   → [`../docs/29_sales_os/OBJECTION_NO_WHATSAPP_AUTOMATION.md`](../docs/29_sales_os/OBJECTION_NO_WHATSAPP_AUTOMATION.md)

4. **"اسحبوا لنا بيانات/جهات اتصال (scraping)."**
   "لا نفعل scraping إطلاقًا — بيانات بلا مصدر مشروع = لا تواصل. نلتزم بنظام حماية
   البيانات (PDPL). نعمل على بياناتكم أنتم أو مصادر مشروعة موثّقة."
   → [`../docs/29_sales_os/OBJECTION_NO_SCRAPING.md`](../docs/29_sales_os/OBJECTION_NO_SCRAPING.md)

5. **"ما عندي وقت."**
   "لهذا التشخيص ٢٤ ساعة وبلا مجهود منك تقريبًا — ٦ أسئلة. نحن من يقوم بالعمل،
   وأنت تراجع وتقرر."

6. **"أرسل لي معلومات فقط."**
   "أرسلها — وأقترح خطوة أصغر تثبت القيمة بدل قراءة ملف: تشخيص مجاني على بيانات
   [الشركة] نفسها. أحجز لك ٢٠ دقيقة الأسبوع القادم نراجع نتيجته؟"

## ٦. الإغلاق — Close (19–20) (AR)

```
بناءً على كلامك، أقترح [التشخيص المجاني / Sprint ٤٩٩ / مكالمة نطاق Command Sprint].
أبدأ اليوم؟ أرسل لك نموذج التشخيص الآن، أو نحجز ٢٠ دقيقة [اليوم/الوقت]؟
```
أغلِق على واحدة: دفع تشخيص/Sprint، أو مكالمة تالية بموعد محدد. لا تترك المكالمة بلا خطوة.

---

## 1. Open (0–2) (EN)

```
Thanks for your time, [Name]. Just twenty minutes, no long pitch.
My goal is to understand how [Company] handles sales opportunities today and see
if there's a fit. If there isn't, I'll tell you straight. Shall we start?
```

## 2. Qualify — BANT-lite (2–7) (EN)

Ask calmly, note the signals:

- **Need (N):** "How do you track opportunities now — CRM, Excel, WhatsApp? Where do they leak?"
- **Authority (A):** "Who usually decides on initiatives like this — you or a team?"
- **Budget (B):** "Have you tried similar tools/services? What's a typical budget to test?"
- **Timing (T):** "Is this a priority now or within 30–60 days?"

> See the decision rule in [`LEAD_INTAKE_FRAMEWORK_AR.md`](LEAD_INTAKE_FRAMEWORK_AR.md) §2.

## 3. Diagnose (7–12) (EN)

```
I heard you say [reflect their pain: e.g. "opportunities are scattered and
follow-up slips"]. If we organized your current data and surfaced the top 10
ranked opportunities, with ready-for-approval Arabic drafts — would that save
your team time and reveal opportunities you're missing today?
```
Listen more than you talk. Tie each pain to a concrete deliverable.

## 4. Present ladder + custom path (12–16) (EN)

| Rung | Price | Deliverable |
|------|-------|-------------|
| Free Mini Diagnostic | 0 SAR / 24h | One page: 3 opportunities + draft + risk |
| Revenue Proof Sprint | 499 SAR / 7d | Company Brain, top 10 opportunities, 5 drafts, Proof Pack |
| Data-to-Revenue Pack | 1,500 SAR | Clean data, top 20 opportunities, 10 drafts |
| Growth Ops | 2,999 SAR/mo | Ongoing monthly run under approval |
| **Command Sprint (custom)** | **7,500–15,000 SAR one-time** | Founder-led: one revenue process → AI-assisted flow with an approval point + SOP + Proof Pack |

```
We start small to prove value: free diagnostic, then a 499 SAR Sprint. If you
want a deeper executive path led by me directly, a Command Sprint is a one-time
setup layer above the ladder — not a full managed service. Which path fits your
need right now?
```

> **Always-on governance:** all deliverables are human-approved. No automatic
> external sending, no scraping, no cold WhatsApp, no guaranteed deals —
> "evidenced opportunities".

## 5. Top 6 Objections (16–19) (EN)

1. **"The price is high."**
   "We cut scope before discount. The 499 SAR Sprint is the smallest commitment,
   with a full refund within 14 days. If we don't surface ≥10 opportunities, we
   keep working at no charge."
   → [`../docs/29_sales_os/OBJECTION_PRICE_TOO_HIGH.md`](../docs/29_sales_os/OBJECTION_PRICE_TOO_HIGH.md)

2. **"We already have a CRM."**
   "Great — we don't replace it. We read your data and turn it into ranked
   opportunities and ready drafts. The CRM stores; we produce a decision."

3. **"We want WhatsApp automation."**
   "We don't offer automated WhatsApp or bulk messages — that's spam and breaches
   policy. We provide drafts you approve and send manually yourself."
   → [`../docs/29_sales_os/OBJECTION_NO_WHATSAPP_AUTOMATION.md`](../docs/29_sales_os/OBJECTION_NO_WHATSAPP_AUTOMATION.md)

4. **"Scrape contacts/data for us."**
   "We never scrape — source-less data means no outreach. We comply with the PDPL.
   We work on your own data or documented lawful sources."
   → [`../docs/29_sales_os/OBJECTION_NO_SCRAPING.md`](../docs/29_sales_os/OBJECTION_NO_SCRAPING.md)

5. **"I don't have time."**
   "That's why the diagnostic takes 24h and almost no effort from you — 6
   questions. We do the work; you review and decide."

6. **"Just send me info."**
   "I will — and I'd suggest a smaller value-proving step instead of reading a
   file: a free diagnostic on [Company]'s own data. Shall I book you 20 minutes
   next week to review the result?"

## 6. Close (19–20) (EN)

```
Based on what you said, I suggest [free diagnostic / 499 Sprint / Command Sprint
scoping call]. Shall I start today? I'll send the diagnostic form now, or we book
20 minutes [day/time]?
```
Close on one: a paid diagnostic/Sprint, or a next call with a set time. Never leave
the call without a next step.

---

## متتبّع المكالمة — Call Tracker Template

انسخ هذا الجدول لكل مكالمة، أو أضِف صفًا في `../docs/ops/pipeline_tracker.csv`.

| الحقل | القيمة |
|-------|--------|
| التاريخ / Date | |
| الجهة (الاسم) / Contact | |
| الشركة / Company | |
| القطاع / Sector | |
| المصدر المشروع / Lawful source | |
| BANT (B/A/N/T) | _/_/_/_ |
| الألم الأساسي / Core pain | |
| الدرجة المعروضة / Rung offered | D / S / Pack / Ops / Command Sprint |
| الاعتراض الرئيسي / Main objection | |
| نتيجة الإغلاق / Close outcome | paid / next-call / no-fit |
| الخطوة التالية + الموعد / Next action + date | |
| ملاحظات / Notes | |

---

## روابط — Related

- إطار الاستقبال: [`LEAD_INTAKE_FRAMEWORK_AR.md`](LEAD_INTAKE_FRAMEWORK_AR.md)
- إجراء المسوّدات اليومية: [`DAILY_DRAFTS_SOP_AR.md`](DAILY_DRAFTS_SOP_AR.md)
- حزمة المسوّدات: [`daily_drafts/SAMPLE_PACK_AR.md`](daily_drafts/SAMPLE_PACK_AR.md)
- بذور القطاعات: [`target_segments.csv`](target_segments.csv)
- السكربت المختصر: [`../docs/29_sales_os/DISCOVERY_CALL_SCRIPT.md`](../docs/29_sales_os/DISCOVERY_CALL_SCRIPT.md)
- التعامل مع الاعتراضات: [`../docs/29_sales_os/OBJECTION_HANDLING.md`](../docs/29_sales_os/OBJECTION_HANDLING.md)
- السلّم والأسعار: [`../docs/OFFER_LADDER_AND_PRICING.md`](../docs/OFFER_LADDER_AND_PRICING.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
