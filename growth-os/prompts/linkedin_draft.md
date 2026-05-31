# Prompt: LinkedIn Message Draft
**Used by:** asset-generator agent (assisted_manual mode only)
**Output:** channel_assets.jsonl (channel: linkedin)

IMPORTANT: This prompt generates a draft for the FOUNDER to send manually.
The system NEVER sends LinkedIn messages directly. This is non-negotiable.

---

## System Context

You are preparing a LinkedIn message for the founder to review and send manually. The message must be:
- Under 200 words
- Conversational and peer-level (not a sales pitch)
- Specific to the recipient's sector and role
- Free of guaranteed claims

The founder will:
1. Read this draft
2. Personalize it based on the recipient's actual LinkedIn profile
3. Send it manually from their LinkedIn account

---

## Draft Prompt

**English version (most LinkedIn in GCC is English):**

```
Write a short LinkedIn message for a founder to send to a {buyer_title} at {company_name}, 
a {sector} company in {country}.

Context about the recipient's likely situation:
{brief_text_en}

Top pain points for their sector:
{top_pains}

Goal: Start a conversation — NOT close a sale.

Writing rules:
- 150-200 words maximum
- Peer-level tone — as if one professional to another
- One specific observation about their sector (not the company — avoid "I researched your company")
- One soft question — not a hard sell
- No mention of pricing
- No sales language ("I'd love to tell you about...")
- End with a question that is easy to say yes or no to
- Do NOT include links in the first message

Format:
[Greeting with name if known, otherwise "Hi {buyer_title}"]
[1 sentence: what you noticed or have in common]
[1-2 sentences: the pain/challenge you help with]
[1 sentence: what you do briefly — no jargon]
[1 question: easy yes/no or "is this relevant to you?"]
```

**Arabic version (for SA consulting or legal where Arabic preferred):**

```
اكتب رسالة LinkedIn قصيرة لمؤسس ليرسلها يدوياً إلى {buyer_title} في {company_name}،
وهي شركة في قطاع {sector} في {country}.

السياق:
{brief_text_ar}

قواعد الكتابة:
- 100-150 كلمة كحد أقصى
- أسلوب مهني ومتكافئ — مهني يتحدث إلى مهني آخر
- ملاحظة واحدة محددة عن قطاعهم
- سؤال واحد — ليس عرضاً مباشراً
- لا ذكر للأسعار
- لا روابط في الرسالة الأولى
- اختم بسؤال سهل الإجابة بنعم أو لا
```

---

## Package for Founder (Assisted Manual)

The full package sent to outputs/founder_review/ includes:

```yaml
draft_message: "[the message above]"
recipient_title: "{buyer_title}"
company_name: "{company_name}"
sector_context: "{brief_text_en}"
suggested_subject_or_opener: "[first 10 words of message]"
compliance_checklist:
  - "Message is peer-level — not a pitch"
  - "No pricing mentioned"
  - "No links in first message"
  - "One clear question at end"
  - "Founder manually reviews LinkedIn profile before sending"
  - "Founder sends manually — system does not touch LinkedIn"
founder_instructions:
  - "Review recipient's LinkedIn profile before sending"
  - "Customize the opener if you see a relevant recent post or event"
  - "Send from your personal LinkedIn account manually"
  - "Log the send in memory/execution_logs.jsonl after sending"
```

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
