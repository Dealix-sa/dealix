# خريطة التدفق — رحلات العميل والمراحل

كيف ينتقل العميل داخل النظام. الانتقالات حتمية في `conversation_state.py`؛ آلة الحالة تقرر المرحلة القادمة من (المرحلة الحالية، النية).

## رحلات العميل الخمس

### A — عميل جديد / غير متأكد
يبدأ بلا هدف محدد، يختار «ما أعرف — اقترح علي».

```
new → menu → (not_sure) → assessment_in_progress → assessment_complete → recommendation
```

النتيجة: توصية واحدة واضحة مربوطة بالكتالوج، ثم خيار «أرسل لي العرض» أو «احجز مكالمة».

### B — مشكلة محددة (متابعة/حملة)
يعرف احتياجه: تجهيز متابعة أو حملة.

```
new → menu → (campaign_followup) → recommendation → (request_proposal) → proposal
```

التوصية مبنية على آخر فحص إن وُجد، وإلا تبدأ بفحص سريع.

### C — ملف / رابط
يريد رفع ملف leads أو مشاركة رابط.

```
menu → (send_file_link) → awaiting_secure_input → (approve/review_report) → draft_review
```

الملفات تُرفع عبر مسار آمن؛ لا تُطلب الأسرار في الشات (انظر [WHATSAPP_SECURITY_PRIVACY_AR.md](WHATSAPP_SECURITY_PRIVACY_AR.md)).

### D — إعداد ما بعد البيع (Onboarding)
بعد الدفع الآمن، يبدأ الإعداد: الصلاحيات، الملفات، أول workflow.

```
proposal → (approve) → payment_handoff → (approve) → onboarding
onboarding → (connect_tools) → permission_request
onboarding → (review_report) → draft_review
```

### E — دعم
لديه مشكلة تشغيلية أو يحتاج شخصًا.

```
menu → (support) → support → (human_handoff) → human_handoff
support → (review_report) → recommendation
```

التفاصيل: [WHATSAPP_SUPPORT_ESCALATION_AR.md](WHATSAPP_SUPPORT_ESCALATION_AR.md).

## جدول المراحل

| المرحلة | الوصف |
|---|---|
| `new` | جلسة جديدة قبل عرض القائمة. |
| `menu` | القائمة الرئيسية. |
| `assessment_in_progress` | فحص الجاهزية جارٍ (يبقى حتى يكتمل). |
| `assessment_complete` | اكتمل الفحص. |
| `recommendation` | عرض التوصية المربوطة بالكتالوج. |
| `permission_request` | طلب صلاحية واحدة. |
| `awaiting_secure_input` | بانتظار مدخل آمن (ملف/رابط عبر بوابة آمنة). |
| `draft_review` | مراجعة مسودة قبل أي إرسال. |
| `proposal` | عرض مبدئي بنطاق وسعر واضحين. |
| `payment_handoff` | تحويل للدفع الآمن خارج الشات. |
| `onboarding` | الإعداد بعد البيع. |
| `support` | الدعم. |
| `human_handoff` | محوّل لشخص (نهائي حتى يستأنف إنسان). |
| `closed` | مغلق. |

## التجاوزات العامة (تُقيَّم أولًا، من أي مرحلة)

| النية | النتيجة |
|---|---|
| `blocked_unsafe` | المرحلة تبقى كما هي (الرد كرت رفض، بلا تقدّم). |
| `human_handoff` | الانتقال إلى `human_handoff`. |
| `support` | الانتقال إلى `support`. |

قواعد إضافية: عند اكتمال الفحص في `assessment_in_progress` ينتقل إلى `assessment_complete`. بدء الفحص (`assessment_start`/`diagnose`) صالح من أي مرحلة غير نهائية. المرحلتان النهائيتان: `human_handoff` و`closed`.

## جدول الانتقالات (المصدر: `conversation_state.py`)

| من المرحلة | النية | إلى المرحلة |
|---|---|---|
| new | welcome / unknown | menu |
| menu | diagnose / assessment_start / not_sure | assessment_in_progress |
| menu | campaign_followup | recommendation |
| menu | connect_tools | permission_request |
| menu | review_report | recommendation |
| menu | request_proposal / book_call | proposal |
| menu | send_file_link | awaiting_secure_input |
| assessment_in_progress | assessment_answer / assessment_start | assessment_in_progress (حتى الاكتمال) |
| assessment_complete | request_proposal / book_call | proposal |
| assessment_complete | connect_tools | permission_request |
| assessment_complete | diagnose / unknown | recommendation |
| recommendation | request_proposal / book_call | proposal |
| recommendation | connect_tools | permission_request |
| recommendation | send_file_link | awaiting_secure_input |
| recommendation | assessment_start | assessment_in_progress |
| permission_request | permission_grant / send_file_link | awaiting_secure_input |
| permission_request | permission_deny | recommendation |
| awaiting_secure_input | approve / review_report | draft_review |
| awaiting_secure_input | unknown | awaiting_secure_input |
| draft_review | approve | proposal |
| draft_review | reject | recommendation |
| draft_review | edit / simplify | draft_review |
| proposal | approve | payment_handoff |
| proposal | request_proposal / book_call | proposal |
| proposal | reject | recommendation |
| payment_handoff | approve | onboarding |
| payment_handoff | reject | recommendation |
| onboarding | connect_tools | permission_request |
| onboarding | send_file_link | awaiting_secure_input |
| onboarding | review_report | draft_review |
| support | human_handoff | human_handoff |
| support | review_report | recommendation |
| support | unknown | support |

> ملاحظة: التفاوض على السعر يُكتشف عند `proposal`/`payment_handoff` مع نية `reject`/`edit` ويُصعَّد لشخص (انظر [WHATSAPP_HANDOFF_POLICY_AR.md](WHATSAPP_HANDOFF_POLICY_AR.md)).

## روابط

- النظرة الشاملة: [WHATSAPP_CLIENT_OS_AR.md](WHATSAPP_CLIENT_OS_AR.md)
- سياسة المحادثة: [WHATSAPP_CONVERSATION_POLICY_AR.md](WHATSAPP_CONVERSATION_POLICY_AR.md)
- فحص الجاهزية: [CLIENT_ONBOARDING_ASSESSMENT_AR.md](CLIENT_ONBOARDING_ASSESSMENT_AR.md)
