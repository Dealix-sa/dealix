# The Dealix Doctrine — A Manifesto

> The 11 non-negotiables in plain language. Bilingual. Public.
> Designed to be uncomfortable for shortcut-seekers and clarifying
> for the right customers.
>
> **Effective:** 2026-06-01

---

## Arabic — العربية

### المبدأ الجذري

في B2B السعودي، **الـ trust ليس feature — هو السوق نفسه**. أي vendor
يعتقد أنه يستطيع شراء النمو على حساب الـ trust لم يفهم القاعدة
الأساسية. Dealix لا يُبيع نمو — يُبيع discipline.

### الـ ١١ خط أحمر

#### #1 — لا إرسال تلقائي للخارج (no_live_send)
نحن لا ندفع رسالة إلى أي قناة خارجية تلقائيًا — أبدًا. لا
WhatsApp، لا email، لا LinkedIn، لا SMS. كل draft تنتظر موافقة
human قبل المغادرة.

**ما يكلفه:** ١٥ دقيقة/يوم للموافقات.
**ما يقدمه:** صفر مفاجآت سيئة، صفر damage control.

#### #2 — لا WhatsApp بارد (no_cold_whatsapp)
WhatsApp في السعودية = غرفة مهنية، ليس channel marketing. cold
WhatsApp يكسر brand بشكل لا يُسترجع. نرفض إنتاج draft لـ contact
بدون warm consent مسجل.

#### #3 — لا scraping (no_scraping)
صفر web scraping. صفر بيانات من مصادر بدون إذن. كل lead يأتي من
input مرخص (form submission، event، referral، partner).

#### #4 — لا إثبات مزيف (no_fake_proof)
كل رقم في case study أو report يستند إلى event مسجل في
proof_ledger. لو الـ event غير موجود، الرقم لا يُنشر — حتى لو
"نعرف أنه صحيح."

#### #5 — لا بيانات بدون موافقة (no_unconsented_data)
كل lead يحمل Source Passport يسجل lawful basis. لو الـ basis
ناقص، الـ agent يرفض إنتاج رسالة.

#### #6 — لا ضمانات بدون إثبات (no_unverified_outcomes)
لا نعد بـ revenue، lead count، conversion rate. نعد بـ proof
events ضمن timeline محدد. الضمانات هي كذب في B2B.

#### #7 — لا أسعار مخفية (no_hidden_pricing)
كل السعر منشور علنًا. لا "اتصل بنا للسعر." لا discount غامض. كل
الشروط في public.

#### #8 — لا أخطاء صامتة (no_silent_failures)
كل error يُسجل، يُراجع، يُكشف. لا "تم كل شي بنجاح" خفي. الـ
audit trail يكشف الحقيقة.

#### #9 — لا agents بدون حدود (no_unbounded_agents)
كل agent له guardrails صريحة. لا "ذكاء عام بدون قيود." الـ
boundary هي feature، ليست قيد.

#### #10 — لا تغييرات بدون مراجعة (no_unaudited_changes)
كل commit يمر بـ CI gate. كل تعديل في الـ doctrine يحتاج founder
sign-off + ٣٠ يوم إشعار للعملاء.

#### #11 — لا LinkedIn automation (no_linkedin_automation)
لا auto-connect، لا auto-DM، لا auto-comment، لا scraping. حتى
publishing الـ posts نستخدم LinkedIn UI الأصلي.

### لماذا هذه الـ ١١ بالتحديد؟

كل واحد منها يجاوب على سؤال "ماذا فعل vendor كسر brand عميل
سعودي؟" في السنوات الـ ٥ الماضية. الـ doctrine ليس نظري — هو سجل
الفشل المتراكم.

### ما الذي يحدث لو طلب عميل خرق إحداها؟

نرفض. حتى لو السعر مرتفع. حتى لو خسرنا الـ deal. لأن الـ doctrine
**هي المنتج**. شركة بدون doctrine = أداة، ليست شريك.

### كيف نضمن الـ doctrine لا تتآكل؟

- **CI gate:** `tests/test_doctrine_guardrails.py` يكسر merge على
  أي PR يخرق non-negotiable.
- **Source code public:** github.com/VoXc2/dealix — أي عميل أو
  competitor يستطيع التحقق.
- **No-overclaim register:** `dealix/registers/no_overclaim.yaml`
  يسجل كل claim علني + status (Planned/Pilot/Production).
- **Quarterly review:** الفاوندر يراجع الـ doctrine كل ربع. لو
  ظهرت non-negotiable جديدة، تُضاف بـ ٣٠ يوم إشعار.

### إعلان مفتوح

نحن نتعهد علنًا:
- لو خرقنا واحدة من الـ ١١، نعلن ذلك في ٢٤ ساعة.
- post-mortem في ٧ أيام.
- refund الكامل لأي عميل تأثر، بدون أسئلة.

---

## English

### The root principle

In Saudi B2B, **trust isn't a feature — it's the market itself**.
Any vendor who thinks they can buy growth at the cost of trust has
missed the foundation. Dealix doesn't sell growth — it sells
discipline.

### The 11 red lines

#### #1 — No autonomous outbound (no_live_send)
We never push a message to any external channel automatically —
ever. Not WhatsApp, not email, not LinkedIn, not SMS. Every draft
waits for human approval before leaving.

**What it costs:** 15 min/day on approvals.
**What it gives:** zero bad surprises, zero damage control.

#### #2 — No cold WhatsApp (no_cold_whatsapp)
WhatsApp in Saudi = professional room, not marketing channel.
Cold WhatsApp breaks brand irrecoverably. We refuse to draft for
contacts without recorded warm consent.

#### #3 — No scraping (no_scraping)
Zero web scraping. Zero data from unauthorized sources. Every lead
comes from a licensed input (form submission, event, referral,
partner).

#### #4 — No fake proof (no_fake_proof)
Every number in a case study or report ties to a recorded event in
the proof_ledger. If the event doesn't exist, the number doesn't
publish — even if "we know it's true."

#### #5 — No unconsented data (no_unconsented_data)
Every lead carries a Source Passport recording lawful basis. If
the basis is missing, the agent refuses to draft a message.

#### #6 — No unverified guarantees (no_unverified_outcomes)
We don't promise revenue, lead count, conversion rate. We promise
proof events within a defined timeline. Guarantees are lies in B2B.

#### #7 — No hidden pricing (no_hidden_pricing)
All prices public. No "contact us for pricing." No vague discounts.
All terms public.

#### #8 — No silent failures (no_silent_failures)
Every error logged, reviewed, surfaced. No quiet "all is well."
The audit trail reveals truth.

#### #9 — No unbounded agents (no_unbounded_agents)
Every agent has explicit guardrails. No "general intelligence
unconstrained." The boundary is a feature, not a limit.

#### #10 — No unaudited changes (no_unaudited_changes)
Every commit passes CI gate. Every doctrine modification requires
founder sign-off + 30-day customer notice.

#### #11 — No LinkedIn automation (no_linkedin_automation)
No auto-connect, no auto-DM, no auto-comment, no scraping. Even
publishing posts uses LinkedIn's native UI.

### Why these 11 specifically?

Each one answers "what did a vendor do to break a Saudi customer's
brand?" over the last 5 years. The doctrine isn't theoretical —
it's the accumulated failure record.

### What happens if a customer asks us to break one?

We refuse. Even if the price is high. Even if we lose the deal.
Because the doctrine **IS the product**. A company without doctrine
= a tool, not a partner.

### How we ensure the doctrine doesn't erode

- **CI gate:** `tests/test_doctrine_guardrails.py` breaks merge on
  any PR that violates a non-negotiable.
- **Source code public:** github.com/VoXc2/dealix — any customer
  or competitor can verify.
- **No-overclaim register:** `dealix/registers/no_overclaim.yaml`
  tracks every public claim + status (Planned/Pilot/Production).
- **Quarterly review:** founder reviews the doctrine every
  quarter. New non-negotiables added with 30-day customer notice.

### Open commitment

We publicly pledge:
- If we break one of the 11, we announce it within 24 hours.
- Post-mortem within 7 days.
- Full refund to any affected customer, no questions.

---

## What this manifesto is not

- A marketing claim — it's enforced in code
- A nice-to-have — it's the differentiator that wins Saudi B2B
- A static document — it evolves, but only with audit chain

## What this manifesto means for you

If you're a **customer:** you can demand evidence of any of the 11
at any time. We owe you the answer in 48h.

If you're a **partner:** these 11 apply to your engagements with
our shared customers. Sign the partner agreement = adopt the
doctrine.

If you're a **competitor:** you can copy the code. The code without
the founder discipline behind it is just code.

If you're an **investor:** the doctrine is non-negotiable in any
funding round. We'd rather not raise than dilute it.

---

## Read this once. Re-read quarterly.

If a single decision in your day at Dealix is ambiguous, return to
this document. The answer is in here.

— Sami, founder
