# Demo Follow-Up Email — {{ customer_name }} / بريد متابعة بعد العرض التوضيحي

<!-- Bilingual email template. Rendered per-customer with Jinja2. -->
<!-- Required variables: customer_name, founder_name, sector, demo_date, diagnostic_link, sprint_price_sar, engagement_id, calendly_link. -->
<!-- Draft only — sent manually by the founder after founder review. No auto-send. -->

**To / إلى:** {{ customer_name }}
**Subject / الموضوع:** {{ customer_name }} — الخطوة التالية بعد العرض التوضيحي / your next step after the Dealix demo

---

## العربية أولاً

مرحباً {{ customer_name }}،

شكراً على وقتك في العرض التوضيحي يوم {{ demo_date }}. كما رأيت، Dealix لا يبيع وعداً — يُسلّم قراراً مُحوكَماً قابلاً للتدقيق على بيانات قطاع {{ sector }}.

**خطوتك التالية، بلا التزام:**

- **التشخيص المجاني** — تقرير من صفحة واحدة خلال 24 ساعة: 3 أولويات إيراد + توصية الخطوة التالية. ابدأ من هنا: {{ diagnostic_link }}
- إذا أعجبك التشخيص، نُتبعه بعرض **سبرنت ذكاء الإيرادات** بسعر ثابت **{{ sprint_price_sar }} ريال** ومدة 7 أيام: 10 حسابات مُرتَّبة، مسودات ثنائية اللغة، حزمة إثبات من 14 قسماً، وأصل قابل لإعادة الاستخدام.

ما لا نقدّمه: لا واتساب بارد، لا أتمتة LinkedIn، لا ضمان صفقات. كل مخرَج يبقى مسودة حتى موافقتك الصريحة.

لحجز مكالمة قصيرة لمراجعة التشخيص: {{ calendly_link }}

إذا لم يكن التوقيت مناسباً، ردّ بكلمة "لاحقاً" وسأتوقف عن المتابعة باحترام.

{{ founder_name }} — مؤسس Dealix
معرّف المشروع المرجعي: `{{ engagement_id }}`

---

## English

Hello {{ customer_name }},

Thank you for your time in the demo on {{ demo_date }}. As you saw, Dealix does not sell a promise — it delivers a governed, auditable revenue decision on {{ sector }} data.

**Your next step, with no commitment:**

- **The Free Diagnostic** — a one-page report within 24 hours: three revenue priorities plus a recommended next step. Start here: {{ diagnostic_link }}
- If the diagnostic is useful, we follow it with a **Revenue Intelligence Sprint** proposal at a fixed price of **{{ sprint_price_sar }} SAR** over 7 days: 10 ranked accounts, a bilingual draft pack, a 14-section Proof Pack, and at least one reusable capital asset.

What we do not offer: no cold WhatsApp, no LinkedIn automation, no guaranteed deals. Every output stays a draft until your explicit approval.

To book a short call to review the diagnostic: {{ calendly_link }}

If the timing is not right, reply "later" and I will respectfully stop following up.

{{ founder_name }} — Founder, Dealix
Reference engagement ID: `{{ engagement_id }}`

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**

**This email is a draft for founder approval before send / هذا البريد مسودّة بانتظار موافقة المؤسس قبل الإرسال.**
