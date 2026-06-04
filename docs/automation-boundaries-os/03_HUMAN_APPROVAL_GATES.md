# بوابات الموافقة البشرية | Human Approval Gates

> **AR:** بوابة الموافقة البشرية هي نقطة توقّف إلزامية يمرّ بها كل ناتج قبل أن يتحول من مسودّة إلى فعل. لا يتجاوز أي مصنوع البوابة دون اعتماد صريح من المؤسس. هذه البوابات هي ما يحوّل "AI prepares" إلى "Founder approves".
>
> **EN:** A human approval gate is a mandatory stop every output passes before turning from draft into action. No artifact crosses the gate without explicit founder approval. These gates are what turn "AI prepares" into "Founder approves."

## البوابات الأساسية | Core Gates

| البوابة Gate | متى When | المُعتمِد Approver |
|---|---|---|
| Draft → Send | قبل أي تواصل خارجي / before any external contact | المؤسس / Founder |
| Proposal → Deliver | قبل تسليم عرض لعميل / before delivering a proposal | المؤسس / Founder |
| Plan → Launch | قبل أي إطلاق (إعلان/قناة) / before any launch | المؤسس / Founder |
| Data → Store | قبل تخزين بيانات حسّاسة / before storing sensitive data | المؤسس + اتفاق / Founder + agreement |
| Decision → Commit | قبل اعتماد قرار في الذاكرة / before committing a decision | المؤسس / Founder |

## تدفّق البوابة | Gate Flow

1. **Prepare** — تُنتج الأتمتة مسودّة موسومة `draft`. / Automation produces a `draft`-tagged artifact.
2. **Present** — تُعرَض على المؤسس مع السياق والمصدر. / Presented to founder with context & source.
3. **Decide** — يعتمد أو يرفض أو يعدّل. / Approve, reject, or revise.
4. **Record** — يُسجَّل القرار ومن اعتمده وزمنه. / Decision, approver, and time recorded.
5. **Act (manual)** — ينفّذ المؤسس الفعل الخارجي يدويًا. / Founder performs the external action manually.

## ما لا يمكن أن يتجاوز البوابة | What Cannot Bypass a Gate

- أي إرسال خارجي (بريد/واتساب/لينكدإن). / Any external send.
- أي تقديم نموذج أو إطلاق إعلان. / Any form submit or ad launch.
- أي معالجة بيانات حسّاسة بلا اتفاق. / Any sensitive-data processing without agreement.

## سجلّ الموافقات | Approval Log

| الحقل Field | الوصف Description |
|---|---|
| `artifact_id` | المصنوع المعني / the artifact |
| `gate` | البوابة / the gate |
| `decision` | approved \| rejected \| revised |
| `approved_by` | المؤسس / founder |
| `timestamp` | الطابع الزمني / timestamp |

## قاعدة الأمان | Safety Rule

> لا فعل خارجي بلا بوابة، ولا بوابة بلا اعتماد بشري موثّق.
> No external action without a gate; no gate without a documented human approval.
