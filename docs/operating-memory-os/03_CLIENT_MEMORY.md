# ذاكرة العميل | Client Memory

> **AR:** ذاكرة العميل تحفظ سياق كل علاقة عميل بصيغة منظمة: من هو، ما احتياجه، أين وصلت العلاقة، وآخر تفاعل. الهدف استمرارية المعرفة دون الاعتماد على ذاكرة بشرية متفرقة، مع احترام صارم للخصوصية.
>
> **EN:** Client Memory preserves the context of each client relationship in a structured form: who they are, their need, where the relationship stands, and the last interaction. The goal is knowledge continuity without relying on scattered human memory, with strict privacy respect.

## بنية السجل | Record Structure

| الحقل Field | الوصف Description |
|---|---|
| `id` | معرّف العميل / client id |
| `client_name` | الاسم / name |
| `segment` | القطاع/الشريحة / segment |
| `need` | الحاجة المعلنة / stated need |
| `relationship_stage` | lead \| conversation \| proposal \| active \| dormant |
| `last_interaction` | تاريخ ونوع آخر تفاعل / date & type of last interaction |
| `notes` | ملاحظات غير حساسة / non-sensitive notes |

## ما يُسمح وما لا يُسمح | Allowed vs Not Allowed

- **يُسمح:** سياق العمل، الاحتياج، مرحلة العلاقة، ملخصات اجتماعات بموافقة. / Allowed: business context, need, stage, approved meeting summaries.
- **لا يُسمح:** بيانات شخصية حساسة، أو بيانات مكتسبة عبر كشط. / Not allowed: sensitive personal data, or scraped data.
- **لا يُسمح:** تخزين بيانات حساسة دون اتفاق موثّق. / Not allowed: processing sensitive data without a documented agreement.

## دورة الحياة | Lifecycle

1. يُنشأ السجل عند أول تفاعل حقيقي (وارد، لا كشط). / Created on first real interaction (inbound, not scraped).
2. يُحدَّث `last_interaction` بعد كل تواصل يدوي. / `last_interaction` updated after each manual contact.
3. `relationship_stage` يتقدّم بموافقة المؤسس فقط. / Stage advances only on founder approval.
4. يُؤرشَف عند الخمول الطويل. / Archived on prolonged dormancy.

## الاستخدام | Usage

- يُستدعى قبل أي مسودة رسالة أو مقترح للعميل. / Recalled before any draft message or proposal.
- يُربط بسجلات ذاكرة الإيراد عبر `id`. / Linked to revenue records via `id`.

## حدود الأمان | Safety Boundaries

- **لا إرسال تلقائي** لأي رسالة عبر البريد/واتساب/لينكدإن. / No automated sending via email/WhatsApp/LinkedIn.
- AI prepares, Founder approves, Manual action only, No external sending.
- لا كشط لجمع بيانات العملاء. / No scraping to collect client data.
- لا أسرار أو معرّفات دفع في الملاحظات. / No secrets or payment identifiers in notes.
