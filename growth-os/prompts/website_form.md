# Prompt: Website Contact Form
**Used by:** asset-generator agent (1 per domain per day, human review before send)
**Output:** channel_assets.jsonl (channel: website_forms)

IMPORTANT: Max 1 submission per domain per day. Min 60 min between submissions.
Human review required before any submission. No CAPTCHA bypass.

---

## Form Submission Prompt

```
Write a website contact form submission for {company_name} in the {sector} sector.

Form context:
- Company website: {domain}
- Form type: {form_type} (contact|inquiry|demo_request|general)
- Language: {language}

Company context:
{brief_text_en}

Rules:
- Professional and brief — match the form's purpose
- Identify as Dealix clearly
- One specific question or value proposition
- No sales pressure
- No fake urgency
- Must be honest about who we are and why we're reaching out

Arabic version:
اكتب رسالة لنموذج الاتصال في موقع {company_name}:

يجب أن تشمل:
- الاسم: {sender_name} من ديليكس
- البريد الإلكتروني: {sender_email}
- الموضوع: {subject}
- الرسالة: 60-80 كلمة تشرح من نحن وما نقدمه وطلب مكالمة سريعة
- لا ادعاءات مبالغ فيها

English version:
Message template:
Subject: [Specific pain observation for their sector]

Hi,

My name is {sender_name} from Dealix. We help {sector} companies in {country} 
identify operational gaps in 48 hours through a free diagnostic.

I noticed {company_name} [sector-relevant observation — keep it general, not stalker-ish].

Would a brief 15-minute call make sense to explore if this is relevant to your team?

Best regards,
{sender_name}
Dealix
{contact_info}

[To opt out of future messages, please reply with STOP]
```

---

## Pre-Submission Checklist

- [ ] Domain not in suppression list
- [ ] Less than 1 submission to this domain today
- [ ] At least 60 minutes since last submission to any domain
- [ ] Human reviewed draft
- [ ] Sender identity is honest (Dealix, not disguised)
- [ ] Opt-out instruction included

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
