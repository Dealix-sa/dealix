# Cold Email Compliance — امتثال البريد البارد

جزء من: Dealix Market Production OS — انظر [docs/market_os/MARKET_PRODUCTION_OS_AR.md](../market_os/MARKET_PRODUCTION_OS_AR.md)

> القاعدة: كل رسالة صادقة، شخصية، فيها مخرج واضح للإلغاء، ومن هوية مرسِل حقيقية — وإلا لا تُرسل.

---

## 1. المبادئ الإلزامية

| المبدأ | التطبيق في Dealix |
|---|---|
| لا تضليل في الـ headers | اسم المرسِل والنطاق حقيقيان ومطابقان للهوية |
| لا subject مضلّل | الموضوع يصف المحتوى فعلًا — لا وعود كاذبة |
| لا Re:/Fwd: زائفة | ممنوع إيهام المستلم بأن هناك محادثة سابقة |
| opt-out واضح ويُحترم | one-click unsubscribe + كبح فوري للقائمة |
| هوية مرسِل صحيحة | عنوان/كيان حقيقي في تذييل الرسالة (CAN-SPAM) |
| لا قوائم مشتراة | المصادر من المؤسس أو بيانات عامة مُراجعة يدويًا |
| تخصيص حقيقي | إشارة محدّدة واحدة على الأقل لكل رسالة |

نظام CAN-SPAM يُلزم باحترام طلب opt-out خلال 10 أيام عمل ويحظر harvesting؛ ومتطلبات Gmail تُلزم بـ one-click
unsubscribe ومعدّل spam تحت 0.3%. PDPL يحكم البيانات الشخصية في السعودية. (إشارة سياسة، لا استشارة قانونية.)

---

## 2. بوابة الامتثال على كل draft

`outreach_draft.compliance_status` لا يصبح `passed` إلا إذا:

- `unsubscribe_included = true`
- `personalization_score ≥ P1`
- `risk_level ≠ high`
- الشركة/العنوان ليس في `suppression` list
- subject غير مضلّل ولا Re:/Fwd: زائفة
- كل claim له `evidence_level` مناسب (لا claim بلا دليل)

أي إخفاق → `compliance_status = failed` ولا يدخل قائمة الموافقة. انظر
[COLD_EMAIL_DRAFT_FACTORY_AR](COLD_EMAIL_DRAFT_FACTORY_AR.md) لقائمة "لا تُرسل draft إذا".

البوابة في الكود: `governance_os.policy_check_draft(text)` يحجب لغة الضمانات وcold whatsapp وLinkedIn automation.

---

## 3. الممنوعات المطلقة

purchased email lists · fake personalization · misleading subject · Re:/Fwd: كاذبة · إرسال بلا unsubscribe ·
تجاهل opt-out · cold WhatsApp automation · LinkedIn automation · scraping مخالف · claims مضمونة.

---

## 4. سجلّ ومراجعة

- كل قرار موافقة يُسجّل في `approval_action` (من اعتمد، متى).
- كل opt-out يُسجّل في `suppression` فورًا.
- المراجعة اليومية: [reports/outreach/DELIVERABILITY_REVIEW.md](../../reports/outreach/DELIVERABILITY_REVIEW.md).

انظر أيضًا: [EMAIL_DELIVERABILITY_POLICY_AR](EMAIL_DELIVERABILITY_POLICY_AR.md) · [UNSUBSCRIBE_POLICY_AR](UNSUBSCRIBE_POLICY_AR.md) · [SENDING_RAMP_PLAN_AR](SENDING_RAMP_PLAN_AR.md).

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
