# Proposal Cover Email — {{ customer_name }} / بريد تقديم العرض

<!-- Bilingual cover email that accompanies a rendered proposal. Rendered per-customer with Jinja2. -->
<!-- Required variables: customer_name, founder_name, proposal_name, price_sar, delivery_days, engagement_id, proposal_attachment_name. -->
<!-- Draft only — sent manually by the founder after founder review. No auto-send. -->

**To / إلى:** {{ customer_name }}
**Subject / الموضوع:** {{ customer_name }} — عرض {{ proposal_name }} (`{{ engagement_id }}`)
**Attachment / المرفق:** {{ proposal_attachment_name }}

---

## العربية أولاً

مرحباً {{ customer_name }}،

مرفق عرض **{{ proposal_name }}** المُعدّ خصيصاً لشركتكم.

**ملخّص العرض:**

- السعر: **{{ price_sar }} ريال سعودي** — سعر ثابت، شامل، فاتورة متوافقة مع هيئة الزكاة والضريبة (ZATCA).
- مدة التسليم: **{{ delivery_days }} يوماً**.
- معرّف المشروع: `{{ engagement_id }}`.

**ما يضمنه العرض:** منهجية ومقاييس أثر تدقيقي — لا نتائج مبيعات. Dealix لا يَعِد بصفقات مُغلقة أو تسريع pipeline. النتائج التقديرية ليست نتائج مضمونة.

**للقبول:** ردّ بمعرّف المشروع `{{ engagement_id }}` وكلمة "مقبول". يصلكم رابط الدفع عبر ميسر خلال نفس يوم العمل.

إذا كان لديكم سؤال على أي بند، أنا متاح لمكالمة قصيرة قبل القرار.

{{ founder_name }} — مؤسس Dealix

---

## English

Hello {{ customer_name }},

Attached is the **{{ proposal_name }}** proposal prepared specifically for your company.

**Proposal summary:**

- Price: **{{ price_sar }} SAR** — fixed, all-inclusive, ZATCA-compliant invoice.
- Delivery: **{{ delivery_days }} days**.
- Engagement ID: `{{ engagement_id }}`.

**What the proposal promises:** methodology and audit-trail metrics — not sales outcomes. Dealix does not promise closed deals or pipeline acceleration. Estimated outcomes are not guaranteed outcomes.

**To accept:** reply with the engagement ID `{{ engagement_id }}` and "accepted". A Moyasar payment link will follow within the same business day.

If you have a question on any clause, I am available for a short call before you decide.

{{ founder_name }} — Founder, Dealix

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**

**This email is a draft for founder approval before send / هذا البريد مسودّة بانتظار موافقة المؤسس قبل الإرسال.**
