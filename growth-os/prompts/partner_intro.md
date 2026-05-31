# Prompt: Partner Introduction
**Used by:** asset-generator agent (referral channel)
**Output:** channel_assets.jsonl (channel: partners)

---

## System Context

You are drafting a message from the Dealix founder to a potential referral partner. The partner would refer B2B clients in exchange for a formal referral agreement (no hidden incentives, full disclosure).

---

## Partner Intro Prompt

**Arabic:**
```
اكتب رسالة تعريف بالشراكة لمؤسس ديليكس يرسلها إلى {partner_name}، 
{partner_role} في {partner_company}.

السياق:
- ديليكس: عمليات ذكاء اصطناعي محوكمة للشركات السعودية
- الشركاء المناسبون: محاسبون قانونيون، مستشارون استراتيجيون، بائعو برمجيات ERP، مستشارو التحول الرقمي
- نموذج الشراكة: إحالة رسمية مع اتفاقية شفافة

قواعد الكتابة:
- 100-130 كلمة
- مهني ومتكافئ
- اشرح من نحن وما نفعله في جملتين
- اشرح سبب ملاءمة الشراكة لعملاء {partner_name}
- اقترح مكالمة استكشاف لا التزاماً فورياً
- لا وعود بإيرادات أو عمولات في الرسالة الأولى
```

**English:**
```
Write a partner introduction message from the Dealix founder to {partner_name}, 
{partner_role} at {partner_company}.

Context:
- Dealix: Governed AI Operations for Saudi B2B companies
- Ideal partners: Chartered accountants, strategy consultants, ERP vendors, digital transformation advisors
- Partnership model: Formal referral agreement with full disclosure

Rules:
- 120-150 words
- Professional and peer-level
- Two sentences: who Dealix is and what we do
- Why this partnership serves their clients
- Suggest an exploratory call — no immediate commitment
- No revenue promises or commission figures in first message
- Full disclosure: the partner must inform referred clients of the referral relationship

Message structure:
[Greeting]
[Who Dealix is — 2 sentences]
[Why we think there is a fit with their client base]
[One specific type of client we serve well]
[Invitation for a 15-minute call]
[Note: partner must disclose referral relationship to clients]
```

---

## Referral Compliance Rule

All partner messages must include this disclosure note:
"Any referral arrangement will be formally documented. Partners must disclose their referral relationship to referred clients."

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
