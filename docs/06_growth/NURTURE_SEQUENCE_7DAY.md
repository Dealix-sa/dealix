# Nurture Sequence — 7 Day — تسلسل الرعاية ٧ أيام

> A 7-day manual nurture sequence. Every touch is manual-review friendly and routes to a tool or diagnostic.
> تسلسل رعاية يدوي لمدة ٧ أيام. كل تواصل قابل للمراجعة البشرية ويوجّه إلى أداة أو تشخيص.
>
> Part of the Growth OS — see `docs/06_growth/GROWTH_OS.md` §6 (Nurture Sequences).
> CTA routing per `docs/00_platform_truth/CTA_MAP.md`.

---

## القاعدة — Rule

كل تواصل يُكتب كمسودة، يُراجع بشرياً، ويُرسل **فقط** بموافقة صريحة وعبر قناة وافق عليها المستلم.
لا إرسال تلقائي، لا واتساب بارد، لا أتمتة لينكدإن، لا قوائم مشتراة، لا ندرة مصطنعة، لا نتائج مضمونة.
المستلم هنا شركة سبق أن تفاعلت طوعاً (مثلاً أكملت Business OS Score) — وليس قائمة باردة.

Every touch is written as a draft, human-reviewed, and sent **only** with explicit approval through a channel the recipient opted into.
No auto-send, no cold WhatsApp, no LinkedIn automation, no purchased lists, no fake scarcity, no guaranteed results.
The recipient is a company that already engaged voluntarily (e.g. completed a Business OS Score) — never a cold list.

---

## Entry condition — شرط الدخول

يبدأ التسلسل بعد فعل طوعي: إكمال Business OS Score أو طلب معلومات. كل مسودة تمر على `draft_gate.py` وسجل الادعاءات قبل الإرسال.

The sequence starts after a voluntary action: completing a Business OS Score or requesting information. Every draft passes `draft_gate.py` and the Claims Register before sending.

---

## The 7 touches — التواصلات السبعة

| Day | Goal (AR) | Goal (EN) | Draft content | Channel | CTA |
|---|---|---|---|---|---|
| 1 | تأكيد النتيجة وشكر | Confirm score, thank | "وصلك Business OS Score. هذي قراءته باختصار." Human-review draft of their result summary. | Opted-in email | business-os-score (re-view) |
| 2 | توضيح أكبر فجوة | Clarify the biggest gap | اربط نتيجتهم بصفحة إجابة (مثلاً `revenue-leakage` أو `proof-gap`). | Opted-in email | business-os-score |
| 3 | قيمة تعليمية بلا طلب | Educational value, no ask | شارك شرحاً من Answer Library يطابق فجوتهم. لا CTA بيعي اليوم — قيمة فقط. | Opted-in email | (soft) diagnostic |
| 4 | نمط إثبات case-safe | Case-safe proof pattern | شارك نمطاً من Proof Pack مُعتمد (بلا PII) يشبه وضعهم. | Opted-in email | diagnostic |
| 5 | دعوة للتشخيص | Invite to diagnostic | "إذا حاب نقرأ وضعك بدقة أكثر، احجز تشخيصاً." مسودة مخصصة لفجوتهم. | Opted-in email/WhatsApp (opted-in only) | diagnostic |
| 6 | معالجة اعتراض | Address an objection | أجب على اعتراض شائع (الوقت/CRM موجود) بإعادة تأطير من سجل الادعاءات. | Opted-in email | diagnostic |
| 7 | جسر إلى Command Sprint | Bridge to Command Sprint | اشرح ماذا يستلمون في Proof Pack خلال ٧ أيام. دعوة واضحة واحدة. | Opted-in email | command-sprint |

---

## Touch-writing rules — قواعد كتابة كل تواصل

- لغة آمنة فقط من `CLAIMS_REGISTER.md`: "نساعدك توضح next actions"، "نرتب فرصك ومتابعتك وإثباتك"، "نسلم Proof Pack خلال Command Sprint".
- CTA واحد لكل تواصل. لا CTA خارجي ولا إجراء تلقائي.
- لا أرقام مبيعات مضمونة. كل قيمة "تقديرية".
- إن لم يرد المستلم أو طلب التوقف، يتوقف التسلسل فوراً — احترام الموافقة إلزامي.

- Safe language only from `CLAIMS_REGISTER.md`: "we help you clarify next actions", "we organize your opportunities, follow-up, and proof", "we deliver a Proof Pack within the Command Sprint".
- One CTA per touch. No external CTA, no automatic action.
- No guaranteed sales numbers. Every value is "estimated".
- If the recipient does not respond or asks to stop, the sequence halts immediately — consent is mandatory.

---

## What this sequence is NOT — ما ليس عليه هذا التسلسل

- ليس حملة إرسال جماعي ولا أتمتة. كل تواصل قرار بشري.
- ليس واتساب بارد — قناة الواتساب تُستخدم فقط مع من وافق صراحةً.
- ليس وعداً بنتائج — بل دعوة لقراءة أوضح وقرار تنفيذي تالٍ.

- Not a blast campaign or automation. Each touch is a human decision.
- Not cold WhatsApp — the WhatsApp channel is used only with explicit opt-in.
- Not a results promise — an invitation to a clearer reading and the next executive decision.

---

## Cross-references — مراجع

- `docs/06_growth/GROWTH_OS.md`
- `docs/06_growth/ANSWER_LIBRARY.md`
- `docs/06_growth/CONTENT_CALENDAR_30DAY.md`
- `docs/governance/CLAIMS_REGISTER.md`
- `docs/governance/FORBIDDEN_ACTIONS.md`
- `docs/governance/APPROVAL_MATRIX.md`
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `docs/00_platform_truth/CTA_MAP.md`

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
