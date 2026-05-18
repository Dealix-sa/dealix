# Wave 6 — Sprint → Pack / Monthly Upsell (AR/EN)
<!-- Owner: Founder | Updated: 2026-05-18 | Arabic primary -->

**Scripts + certificate for converting a paid 7-Day Revenue Proof Sprint (Rung 1, 499 SAR) customer up the ladder — to the Data-to-Revenue Pack (Rung 2, 1,500 SAR) or Managed Revenue Ops (Rung 3, 2,999–4,999 SAR/month) — every upsell gated on a documented Proof Pack.**

> **Pricing source of truth:** `docs/OFFER_LADDER_AND_PRICING.md`. Rung 1
> Sprint = 499 SAR · Rung 2 Data-to-Revenue Pack = 1,500 SAR · Rung 3
> Managed Revenue Ops = 2,999–4,999 SAR/month · Rung 4 Executive Command
> Center = 7,500–15,000 SAR/month.

> **Gate:** no upsell offer is made before the customer's Day-7 Proof Pack
> is documented in `/proof_ledger`. No documented proof = no upsell. Company
> status: zero paying customers today — these scripts are ready for the
> first paid Sprint, not used before one exists.

> **Hard rules during the upsell call:**
> No guarantees. No live automation promises. No fake metrics. Approval-first throughout. KPI commitment ≠ guarantee.

---

## When to use this script

- During the Day 7 review call of the 7-Day Revenue Proof Sprint
- After the customer has seen the Proof Pack
- After payment_confirmed for the Sprint (revenue ground truth)
- Before sending any monthly invoice

---

## Section 1 — After the Proof Pack (opening)

**AR (Saudi):**
> "هذا الـ Proof Pack من ٧ أيّام Sprint. كل واقعة موثّقة. الآن السؤال: هل تبي تشغّل هذا بشكل دائم أو تكتفي بالـ Sprint؟"

**EN:**
> "This is your Proof Pack from the 7-day Sprint. Every event documented. Now the question: do you want to run this permanently, or stop at the Sprint?"

**Listen for:**
- "أبيها مستمرّة" → go to Section 2A (Managed Revenue Ops)
- "ممتاز بس مكلّف" → go to Section 2B (price objection)
- "ما حسّيت بقيمة" → go to Section 2C (proof gap)
- "أبي ضمانات" → go to Section 2D (KPI commitment vs guarantee)
- "أبي WhatsApp تلقائي" → go to Section 2E (live automation gap)

---

## Section 2A — Customer wants to continue

**AR:**
> "ممتاز. عندنا باقتين شهريّتين:
>
> **Managed Revenue Ops** — ٢٬٩٩٩–٤٬٩٩٩ ريال شهرياً (يُحدّد بالنطاق). يضمّ مسودات شهرية معتمَدة + founder call أسبوعي + Pipeline Audit أسبوعي + Proof Pack شهري.
>
> **Executive Command Center** — ٧٬٥٠٠–١٥٬٠٠٠ ريال شهرياً (يُفتح بعد ≥٣ pilots مكتملة). كل ميزات Managed + ECC dashboard كامل + monthly business review.
>
> أيّهم يناسبك؟"

**EN:**
> "Great. Two monthly tiers:
>
> **Managed Revenue Ops** — 2,999–4,999 SAR/month (scoped within the band). Includes monthly approved drafts + 1 founder call/week + weekly Pipeline Audit + monthly Proof Pack.
>
> **Executive Command Center** — 7,500–15,000 SAR/month (unlocks after ≥3 completed pilots). Everything in Managed + full ECC dashboard + monthly business review.
>
> Which suits you?"

**KPI commitment (NOT guarantee):**
> "إذا اخترت Managed، عندنا التزام: لو ما تحقّق +٢٠٪ على المؤشّر المتّفق عليه خلال ٣٠ يوم، أشتغل مجّاناً حتى يتحقّق. هذا التزام، مو ضمان."

---

## Section 2B — Price objection ("مكلّف")

**AR:**
> "السعر مقابل founder access مباشر + نظام تشغيل إيراد جاهز + Proof Pack شهري موثّق. للمقارنة فقط: راتب موظّف مبيعات في السوق غالباً ٨٬٠٠٠+ ريال شهرياً قبل التأمينات والتدريب — وManaged Revenue Ops ضمن نطاق ٢٬٩٩٩–٤٬٩٩٩ ريال."
>
> "كل درجة تُفتح بدليل موثّق من السابقة — تدفع للشهر التالي بعد ما رأيت Proof Pack الحالي. لا ضمانات، لكن لا التزام أعمى أيضاً."

**EN:**
> "The price reflects direct founder access + a ready revenue operations system + a documented monthly Proof Pack. For comparison only: a sales hire often costs 8,000+ SAR/month before insurance and training — Managed Revenue Ops sits within the 2,999–4,999 SAR band."
>
> "Each rung opens on documented evidence from the last — you commit to the next month after seeing the current Proof Pack. No guarantees, but no blind commitment either."

---

## Section 2C — Proof gap ("ما حسّيت بقيمة")

**AR:**
> "صحيح ممكن السبب: ٧ أيّام قصيرة لإثبات قيمة دائمة. عندنا خياران:
>
> 1. **Sprint extension** — أيّام إضافيّة بنفس السعر، نركّز على المؤشّر اللي تبيه يتحرّك.
> 2. **استرجاع كامل** — ١٠٠٪ خلال ١٤ يوم، بدون أسئلة.
>
> أيّهم تفضّل؟"

**EN:**
> "Fair — 7 days may be too short to prove durable value. Two options:
>
> 1. **Sprint extension** — additional days at the same rate, focused on the KPI you want to move.
> 2. **Full refund** — 100% within 14 days, no questions.
>
> Which?"

---

## Section 2D — Customer wants guarantees

**AR:**
> "Dealix لا يعطي ضمانات. لو لقيت شركة AI تضمن لك ٤×/١٠× — اسأل عن الـ small print. الـ AI لا يمكن أن يضمن نتيجة بسبب متغيّرات السوق + حالة فريقك + جودة بياناتك.
>
> اللي نقدمه: **التزام KPI** — لو ما تحقّق +٢٠٪ على مؤشّرك، أشتغل مجّاناً حتى يتحقّق. هذا أقوى من ضمان لأنه ربط مع نتيجة فعليّة."

**EN:**
> "Dealix offers no guarantees. If you find an AI company guaranteeing 4x/10x — ask about the small print. AI cannot guarantee outcomes given market variables + your team state + your data quality.
>
> What we offer: **KPI commitment** — if +20% lift on your KPI is not achieved, founder works free until it is. Stronger than a guarantee because it ties to actual outcome."

---

## Section 2E — Customer asks for WhatsApp automation

**AR:**
> "Dealix لا يفعّل WhatsApp تلقائي للعملاء. السبب: PDPL + meta policy للـ WhatsApp Business + risk على رقمك (banned). كل رسالة تصدر منك يدوياً (موافقتك). البديل العملي:
>
> - Dealix يجهّز لك draft الردّ السعودي خلال ٤٥ ثانية بعد وصول رسالة العميل
> - Dealix يقترح وقت الإرسال (يحترم quiet hours + 24h window)
> - أنت تضغط زرّ واحد على الجوّال = تمّ الإرسال
>
> هذا الفرق بين 'نظام يحترم الخصوصيّة' و'spam bot'."

**EN:**
> "Dealix does not enable WhatsApp customer outbound automation. Reason: PDPL + Meta WhatsApp Business policy + risk to your number (banned). Every message goes through you manually. Practical alternative:
>
> - Dealix drafts a Saudi-Arabic reply within 45 seconds of customer message
> - Dealix suggests send time (respects quiet hours + 24h window)
> - You tap one button on mobile = sent
>
> This is the difference between 'privacy-respecting system' and 'spam bot'."

---

## Section 3 — Closing

### If customer commits

**AR:**
> "ممتاز. أرسل لك Service Agreement + رابط بنكي للدفع الأوّل خلال ساعة. نبدأ Managed Revenue Ops بكره. الباقي يشتغل تلقائياً + بموافقتك على كل خطوة."

**EN:**
> "Great. I'll send the Service Agreement + bank link for the first payment within an hour. Managed Revenue Ops starts tomorrow. Everything runs + every step requires your approval."

**Founder homework after this call:**
1. Run `dealix_demo_outcome.py --outcome paid --evidence-note "..."` (after payment confirmed)
2. Update PaymentState via `dealix_payment_confirmation_stub.py`
3. Send Service Agreement + bank link manually
4. Schedule first Founder Call (within 7 days)

### If customer needs more time

**AR:**
> "تمام. عندنا الـ Proof Pack جاهز عندك — راجعه مع شريكك/المدير المالي. خلّيني أتابع معاك يوم الخميس، أو موعد يناسبك."

**EN:**
> "OK. The Proof Pack is yours — review it with your partner/CFO. I'll follow up Thursday, or pick a time that works for you."

**Founder homework:**
- `dealix_demo_outcome.py --outcome follow_up --next-action "Thursday 10am call scheduled"`

### If customer says no

**AR:**
> "لا بأس. الـ Proof Pack من ٧ أيّام يبقى عندك — لو في يوم احتجت تتطلع، تعرف وين تجدنا. هل تسمح أبعث لك تحديثات شهرية عن الميزات الجديدة؟"

**EN:**
> "No problem. The 7-day Proof Pack stays with you — if you need it later, you know where to find us. May I send monthly feature updates?"

**Founder homework:**
- `dealix_demo_outcome.py --outcome not_now --next-action "monthly newsletter opt-in" --notes "..."`

---

## What to NEVER say during the upsell call

- ❌ "AI سيحلّ كل مشاكلك" → say "Dealix يحلّ ٧٠٪ من المشاكل التشغيليّة، الباقي يحتاج قرارك"
- ❌ "نضمن إيراد X ريال" → say "نلتزم بـ KPI lift +٢٠٪، لا ضمانات"
- ❌ "نبعث WhatsApp تلقائي" → say "Dealix يجهّز draft، أنت ترسل بضغطة"
- ❌ "نسحب بيانات منافسيك" → say "Dealix لا يقوم بـ scraping أبداً (PDPL + قانوني)"
- ❌ "أتمتة LinkedIn" → say "LinkedIn يدوي فقط، لا أتمتة"

## What to ALWAYS say

- ✅ "كل قرار خارجي بموافقتك"
- ✅ "Proof Pack موثّق — لا أرقام مخترعة"
- ✅ "Saudi-PDPL compliant"
- ✅ "founder access مباشر"
- ✅ "ضمان استرجاع ١٠٠٪ خلال ١٤ يوم"

---

## Section 4 — Rung 1 → Rung 2 upsell (Data-to-Revenue Pack, 1,500 SAR)

> Use when the Sprint Proof Pack shows the customer has **untapped data**
> (a CRM export, a customer list, sales history) but is **not yet ready for
> a monthly commitment**. The Pack is a one-time project — a softer next
> step than Rung 3.

**Gate:** offer this only if the Day-7 Proof Pack documents at least one
real proof event. No documented proof = no offer.

**AR (Saudi):**
> "من Proof Pack واضح إن عندكم بيانات عملاء ومبيعات ما استُثمرت بعد. قبل أي
> اشتراك شهري، فيه خطوة مشروع واحد: **Data-to-Revenue Pack — ١٬٥٠٠ ريال**.
> نحلّل الـ pipeline كامل، نرسم خريطة فرص مرتّبة، ونجهّز ١٠ مسودات استهداف
> مخصّصة + playbook مبيعات. مشروع واحد، لا التزام شهري. بعده تقرّر بهدوء إذا
> تبي Managed Revenue Ops."

**EN:**
> "Your Proof Pack shows you have customer and sales data that isn't being
> used yet. Before any monthly subscription, there's a one-time project
> step: the **Data-to-Revenue Pack — 1,500 SAR**. We do a full pipeline
> analysis, a ranked opportunity map, 10 tailored targeting drafts, and a
> custom sales playbook. One project, no monthly commitment. After it, you
> decide calmly whether Managed Revenue Ops fits."

**If customer asks "why not jump straight to monthly?":**
> "تقدر — لكن القاعدة عندنا: لا ترقية قبل دليل. الـ Pack يعطيك إثبات إضافي
> على قيمة البيانات قبل أي التزام شهري. لو نتيجته أقنعتك، الانتقال لـ
> Managed Revenue Ops يصير قراراً مبنيّاً على دليلين، لا واحد."
> / "You can — but our rule is no upgrade before evidence. The Pack gives
> you a second documented proof point before any monthly commitment."

**Never say:** that the Pack "guarantees" found revenue. The Pack documents
a ranked opportunity map and drafts — opportunities evidenced by data, not
promised outcomes.

**Founder homework after a Pack sale:**
1. Confirm payment, then log the proof event in `/proof_ledger`.
2. Deliver per `docs/OFFER_LADDER_AND_PRICING.md` Service 2 scope (5–7
   business days).
3. Issue the Sprint Completion Certificate addendum (see below) on Pack
   delivery if not already issued.

---

## Section 5 — Sprint Completion Certificate (TEMPLATE)

> ⚠️ **قالب فارغ.** يُصدر فقط بعد إتمام Sprint مدفوع فعلي، ويُملأ بأدلة من
> Proof Pack الموثّق. لا يُصدر مسبقاً، ولا يحتوي أرقام نتائج بلا دليل.
> Empty template — issued only after a real paid Sprint, filled from the
> documented Proof Pack. Never pre-issued, never contains unevidenced
> result numbers.

The certificate is a closing asset: it gives the customer a tangible record
of what was delivered and naturally opens the upsell conversation. It is
**not** a results guarantee.

```markdown
# شهادة إتمام Sprint — Sprint Completion Certificate
## Dealix — 7-Day Revenue Proof Sprint

تشهد Dealix بأن:
This certifies that:

**العميل / Client:** [اسم الشركة / company name]
**الخدمة / Service:** 7-Day Revenue Proof Sprint (Rung 1 — 499 SAR)
**الفترة / Period:** [تاريخ البداية] — [تاريخ النهاية]
**معرّف Sprint / Sprint ID:** [SPR-NNN]
**معرّف Proof Pack / Proof Pack ID:** [PLX-NNN]

---

### المخرجات المُسلّمة / Deliverables completed
- [ ] تقرير تشخيصي مفصّل / Detailed diagnostic report
- [ ] [N] مسودات تواصل جاهزة للموافقة / outreach drafts ready for approval
- [ ] Proof Pack موثّق (اليوم 7) / documented Day-7 Proof Pack
- [ ] تقرير تنفيذي / executive report
- [ ] خطة 30 يوماً / 30-day plan

> كل بند أعلاه يُؤشَّر فقط إذا سُلِّم فعلاً وموثّق في Proof Pack.

### أعلى مستوى دليل تحقّق / Highest evidence level reached
[L1 | L2 | L3 | L4 | L5] — راجع `docs/PROOF_AND_CASE_STUDY_SYSTEM.md`.

### ملاحظة الإفصاح / Disclosure
هذه الشهادة توثّق **ما سُلِّم**، لا تَعِد بنتيجة. Dealix لا يضمن مبيعات.
This certifies **what was delivered**; it is not a results guarantee.
Dealix makes no guaranteed-sales claims.

---

**اعتمدها / Issued by:** سامي — مؤسّس Dealix
**التاريخ / Date:** [ ]
**التوقيع / Signature:** ____________________

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
```

**كيف تُستخدم في الإغلاق / How to use it in closing:**

**AR:** "هذي شهادة إتمام Sprint — توثّق كل ما سلّمناه في السبعة أيّام. خذها
سجلّاً لشركتك. ومنها نكمّل: تبي تبني على هذا الأساس بـ Data-to-Revenue Pack
أو Managed Revenue Ops؟"

**EN:** "This is your Sprint Completion Certificate — a record of everything
delivered in the 7 days. Keep it for your company. From here we continue:
do you want to build on it with the Data-to-Revenue Pack, or Managed Revenue
Ops?"

---

## Upsell decision map — أين توجّه العميل

| إشارة من Proof Pack / Signal | الدرجة المقترحة / Suggested rung |
|---|---|
| بيانات غير مستثمرة، لا استعداد لالتزام شهري | Rung 2 — Data-to-Revenue Pack (1,500 SAR) |
| يريد تشغيلاً مستمراً + متابعة شهرية | Rung 3 — Managed Revenue Ops (2,999–4,999 SAR/mo) |
| C-Suite يريد رادار قرار يومي (بعد ≥3 pilots) | Rung 4 — Executive Command Center |
| لم يحسّ بقيمة كافية | استرجاع 100٪ خلال 14 يوم — Section 2C |

> القاعدة فوق كل شيء: لا درجة تُعرض قبل دليل موثّق من الدرجة السابقة.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
