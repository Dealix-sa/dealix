# Prompt: WhatsApp Approved Template
**Used by:** asset-generator agent
**Output:** channel_assets.jsonl (channel: whatsapp)

IMPORTANT: WhatsApp outbound requires:
1. Opt-in confirmed and stored in opt_ins.jsonl
2. Approved template (approved by Meta before use)
3. No cold outreach — opt-in is non-negotiable

---

## System Context

You are drafting a WhatsApp Business template for initial outreach to contacts who have ALREADY opted in. The template must:
- Be under 80 words
- Use approved template format (header, body, footer, button)
- Never assume opt-in if it is not confirmed
- Include a simple opt-out in the footer

---

## Template Prompt

**Arabic version (primary for SA):**

```
اكتب قالب WhatsApp Business بالعربية لشركة {company_name} في قطاع {sector}.

متطلبات القالب:
- الطول: 60-80 كلمة للجسم
- الهيكل: رأس + جسم + تذييل + زر
- الأسلوب: مختصر ومباشر (أقل رسمية من البريد الإلكتروني)
- لا ضمانات
- زر CTA: "نعم، أنا مهتم" أو "احجز مكالمة سريعة"
- التذييل: "للإيقاف اكتب توقف"

متغيرات القالب (تُعبأ قبل الإرسال):
{{1}} = اسم المستلم أو المسمى الوظيفي
{{2}} = اسم الشركة
{{3}} = القطاع أو نقطة الألم المحددة

مثال:
الرأس: تشخيص عمليات ديليكس — 48 ساعة
الجسم: مرحباً {{1}}، شركات {{3}} كثيراً ما تخسر وقتاً في التقارير اليدوية. نقدم تشخيصاً مجانياً خلال 48 ساعة لتحديد أبرز 3 فجوات في عمليات {{2}}. هل يناسبك ذلك؟
التذييل: للإيقاف اكتب توقف
الزر: نعم، مهتم
```

**English version:**

```
Write a WhatsApp Business template in English for {company_name} in the {sector} sector.

Template requirements:
- Body: 50-80 words
- Structure: Header + Body + Footer + Button
- Tone: Brief and direct (less formal than email)
- No guaranteed claims
- CTA button: "Yes, I'm interested" or "Book a quick call"
- Footer: "Reply STOP to unsubscribe"

Template variables (filled before send):
{{1}} = recipient name or title
{{2}} = company name
{{3}} = sector or specific pain point

Example:
Header: Dealix Ops Diagnostic — 48h
Body: Hi {{1}}, {sector} companies often lose hours to manual reporting. We offer a free 48-hour diagnostic to identify the top 3 operational gaps at {{2}}. Would that be useful?
Footer: Reply STOP to unsubscribe
Button: Yes, interested
```

---

## Meta Template Approval Checklist

Before submitting for Meta approval:
- [ ] No personal data in template body
- [ ] Variables are clearly marked {{1}}, {{2}}, {{3}}
- [ ] Opt-out in footer (STOP / توقف)
- [ ] No misleading claims
- [ ] Template is for informational/marketing category (select correctly)
- [ ] Template matches Dealix Business Account name

---

## Opt-In Verification (MUST PASS BEFORE SEND)

```python
# This check MUST run before any WhatsApp send
assert contact.get("opt_in_status") == True, "BLOCKED: No opt-in — cold WhatsApp forbidden"
assert contact.get("template_approved") == True, "BLOCKED: Template not Meta-approved"
```

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
