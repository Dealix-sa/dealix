# Prompt: Webinar Invite
**Used by:** asset-generator agent
**Output:** channel_assets.jsonl

---

## System Context

Draft a webinar invitation for a Dealix knowledge-sharing session targeting B2B operators in Saudi Arabia. Webinars are free, educational, and not sales calls.

---

## Invite Prompt

**Arabic:**
```
اكتب دعوة ويبينار لجلسة ديليكس التعليمية المجانية:

عنوان الجلسة: {webinar_title}
التاريخ والوقت: {date_time}
المدة: {duration}
موضوع الجلسة: {topic}
القطاع المستهدف: {sector}

قواعد الكتابة:
- الطول: 100-130 كلمة
- يجب أن يبدو تعليمياً — ليس إعلانياً
- أبرز ما سيتعلمه المشارك (3 نقاط تعلم)
- لا وعود بنتائج — هذه جلسة إرشادية
- اشمل رابط التسجيل المجاني
- اشمل طريقة إلغاء الاشتراك

قالب:
[العنوان: ما ستتعلمه في الجلسة — وليس اسم ديليكس]
[الجسم: 3 نقاط تعلم واضحة]
[التفاصيل: التاريخ، الوقت، المدة]
[الدعوة: "سجّل مجاناً"]
[التذييل: "لإلغاء الاشتراك اضغط هنا"]
```

**English:**
```
Write a webinar invitation for a free Dealix educational session:

Session title: {webinar_title}
Date and time: {date_time}
Duration: {duration}
Topic: {topic}
Target sector: {sector}

Rules:
- 120-150 words
- Educational tone — not promotional
- Highlight 3 specific learning points
- No outcome promises — this is a knowledge-sharing session
- Include free registration link
- Include unsubscribe option

Template:
[Subject: What you'll learn in 45 minutes about {topic}]

[Opening: The challenge {sector} companies face with {pain}]
[3 learning points:
  1. How to identify your biggest {sector} operational gaps
  2. What a governed AI workflow looks like in practice
  3. Case study: estimated impact (not guaranteed)]
[Details: Date, time, duration, free]
[CTA: Register free — link]
[Footer: To unsubscribe click here]

Note: Case study must be labeled "estimated — not a guarantee"
```

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
