# Prompt: Telegram Bot Flow
**Used by:** asset-generator agent (opt-in bot only)
**Output:** channel_assets.jsonl (channel: telegram)

IMPORTANT: Telegram is OPT-IN BOT ONLY. User must initiate conversation with /start.
No random DMs. No group posting without admin invite.

---

## Bot Conversation Flow

### Step 1: Welcome (after /start)

```
Arabic:
مرحباً، أنا مساعد ديليكس. أساعد الشركات في {country} على تحديد فجوات العمليات.

ماذا يصف عملك بشكل أفضل؟
1. خدمات قانونية
2. إدارة مرافق
3. استشارات
4. عقارات
5. لوجستيات
6. أخرى

English:
Hello, I am Dealix's assistant bot. I help B2B companies in {country} identify operational gaps.

Which best describes your business?
1. Legal services
2. Facility management
3. Consulting
4. Real estate
5. Logistics
6. Other
```

### Step 2: Sector-Specific Follow-Up

```
After user selects sector {sector}:

Arabic:
شركات {sector} في {country} كثيراً ما تواجه:
- {pain_1}
- {pain_2}  
- {pain_3}

هل أي من هذه التحديات يعكس وضعكم الحالي؟
أ. نعم، هذا يشبه وضعنا
ب. لا، لدينا تحدٍّ مختلف
ج. أريد معرفة المزيد أولاً

English:
{sector} companies in {country} often face:
- {pain_1}
- {pain_2}
- {pain_3}

Does any of this resonate with your current situation?
A. Yes, this sounds familiar
B. No, our challenge is different
C. Tell me more first
```

### Step 3: Offer Introduction

```
If user responds A (resonates):

Arabic:
نقدم تشخيصاً مجانياً خلال 48 ساعة يحدد أبرز 3 فجوات في عملياتكم.
هل تريد حجز تشخيص مجاني؟ [نعم] [لاحقاً]

English:
We offer a free 48-hour diagnostic that maps your top 3 operational gaps.
Would you like to book a free diagnostic? [Yes] [Maybe later]
```

### Step 4: Collection (Consent-First)

```
If user clicks Yes:

Arabic:
ممتاز. أحتاج فقط إلى:
1. اسم شركتك
2. بريد عمل للتواصل

ملاحظة: معلوماتك تُستخدم فقط لإرسال التشخيص وفق سياسة الخصوصية.

English:
Great. I just need:
1. Your company name
2. A business email to send results

Note: Your info is used only to deliver the diagnostic, per our privacy policy.
```

---

## Opt-Out

```
Any time: user types /stop or "stop" or "توقف"

Response:
"لقد أوقفنا جميع الرسائل. لن تتلقى أي رسائل أخرى. / 
We've unsubscribed you. No further messages will be sent."

Action: Add to suppression list immediately.
```

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
