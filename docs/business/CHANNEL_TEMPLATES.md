# Dealix — Per-Channel Outreach Templates

Use ONE channel per account per day. Never duplicate across channels.
All channels: `approval_required=True` for first 30 days.

## 1. Phone Call (primary for the directory file — most leads have phone only)

**Open (Khaliji):**

> السلام عليكم، معك سامي من Dealix. اتصل في أوقاتكم؟
> [انتظر الرد]
> أنا أشتغل على Dealix — رادار عمليات إيراد عربي محوكم يخدم شركات [القطاع] السعودية — يجهّز مسودة ردّ خليجية جاهزة على الـ lead خلال دقائق، تراجعها وتعتمدها قبل الإرسال بدلاً من نصف يوم انتظار. لاحظنا [الشركة] في [المدينة] فحبيت أتأكد: هل تواجهون مشكلة وقت المتابعة على leads الـ inbound؟

**If yes:**

> ممتاز. عندنا Pilot 7 أيام بـ 499 ريال — نشغل Dealix على leadsكم نحن، تشوفون النتيجة، ثم تقرّرون. لو ما أعجبكم، استرجاع 100%. ودك 20 دقيقة هذا الأسبوع نوضح كيف يطبق على وضعكم؟

**If no / not interested:**

> فهمت. هل تتذكر أحد من معارفك في القطاع نفسه أو في شركة عقارية أخرى تواجه التحدي ده؟ نقدر نسأل تجربة تجاه باقي عملاء؟

**Always log:**
- اسم اللي رد + المنصب
- مستوى الاهتمام (1–5)
- اعتراضات
- موعد الـ follow-up

## 2. Cold Email — with mandatory opt-out

**Subject lines (A/B test):**
- `Dealix — مسودات ردّ عربية جاهزة لكل lead، أنت تعتمد`
- `[الشركة] — لا تخسرون leads بسبب وقت الرد`
- `Pilot 7 أيام بـ 499 ريال لشركات العقار السعودية`

**Body (Khaliji):**

```
السلام عليكم {الشركة},

كل lead عقاري متأخر دقيقة = احتمال خسارة العميل لمنافس.
Dealix يجهّز مسودة ردّ بالعربي الخليجي تراجعونها وتعتمدونها قبل الإرسال، وأسئلة تأهيل مُجهّزة كمسودة:
- الميزانية
- الموقع
- موعد المعاينة
ثم يسلّم ملخص العميل المؤهّل لمندوبكم جاهزاً للإغلاق.

عرضنا الافتتاحي:
Pilot 7 أيام بـ 499 ريال — نشغل Dealix على leadsكم نحن، تشوفون النتيجة، ثم تقرّرون.
لو ما اقتنعتم — استرجاع كامل 100%.

تناسبكم 20 دقيقة هذا الأسبوع؟
📅 https://calendly.com/sami-assiri11/dealix-demo

سامي
Dealix — https://dealix.me

— لإلغاء الاستلام: ردّ بـ STOP أو OPT OUT.
```

**Rules:**
- Send max 5 cold emails per day from Sami's address
- 24h between emails to same domain
- If bounce → add to suppression list
- Open rate <10% after 50 sends → stop and rewrite

## 3. WhatsApp — INBOUND ONLY (never cold)

Dealix uses WhatsApp **only for replies to incoming customer messages**, never for cold outreach. The WhatsApp template is just for warm replies after the customer has already messaged.

**Warm reply template (after inbound message):**

```
أهلاً وسهلاً {اسم العميل},

شكراً للتواصل مع {اسم الشركة}.
سيتم الرد على استفساركم خلال {time}.
في حال احتجتم استعجال الرد، يرجى الإفادة.

— {اسم الشركة}
```

**Never send:** cold WhatsApp, broadcast WhatsApp, scraping-derived numbers.

## 4. LinkedIn — Manual Research + Manual Send Only

LinkedIn forbids automation. Dealix uses LinkedIn for:
- Manual research about a target before calling/emailing
- Manual personalized notes from Sami's account

**Manual note template:**

```
أهلاً {الاسم},

لاحظت [signal personalized — e.g., funding round, hiring sales, recent post about Arabic CX].
نحن نبني Dealix — رادار عمليات إيراد عربي محوكم يجهّز مسودات ردّ خليجية على leads تراجعها وتعتمدها قبل الإرسال.
هل عندك دقيقة هذا الأسبوع نتكلم؟

سامي
```

**Rules:**
- Max 10 LinkedIn notes per day from Sami (LinkedIn rate-limits)
- Always reference one specific signal — never templated mass send
- If LinkedIn flags the account → stop immediately

## 5. Google Lead Form (post-deploy)

After `GOOGLE_LEAD_FORM_WEBHOOK_KEY` is set:
- Customer's Google Ads lead form → webhook to `/api/v1/integrations/google-lead-form`
- Dealix ingests the lead and prepares a ready Arabic draft reply
- The customer reviews and approves the draft before anything is sent — no external auto-send

## 6. Meta Lead Form (post-deploy)

Same pattern as Google Lead Form:
- `/api/v1/integrations/meta-lead-form`
- Pull leads from Facebook/Instagram lead ads
- Prepare an Arabic draft reply for the customer to review and approve before sending.

## 7. Phone Call Follow-up Draft (Pilot Pro tier)

For Pilot Pro customers: incoming missed call → Dealix prepares a draft Arabic SMS asking what they need; the customer reviews and approves it before it is sent, then a callback can be scheduled if it is a real lead.

## Channel × Sector Decision Matrix

| Sector | Day 0 channel | Day 2 bump | Day 5 value-add | Day 10 last-touch |
|---|---|---|---|---|
| real_estate | phone | email if business | case study email | manual LinkedIn note |
| construction | phone | phone | email demo invite | nothing (stop) |
| hospitality | phone or email | phone | case study | manual LinkedIn |
| food_beverage | phone | nothing | nothing | nothing (low LTV) |
| logistics | phone or email | email | demo invite | manual LinkedIn |
| saas_tech | manual LinkedIn | email | demo invite | follow-up call |
| agency_marketing | manual LinkedIn (1) | email | partner offer | call |

## What you don't ever do

- ❌ Bulk SMS (Saudi PDPL flag)
- ❌ Cold WhatsApp
- ❌ LinkedIn scraping or bot messaging
- ❌ Sending to suppressed addresses (already enforced server-side)
- ❌ Skipping the approval gate
