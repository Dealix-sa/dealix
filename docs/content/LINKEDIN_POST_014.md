# LinkedIn Post 014 — A REQUIRE_APPROVAL Pattern / قرار يتطلب موافقة، مفصَّلاً

> Bilingual long-form for the founder voice. AR first, EN second. No emojis. No model names. Week 5, Wednesday — Case-safe pattern lane. Anonymized; no client named.
>
> Cross-link: [LINKEDIN_CADENCE_PLAN.md](./LINKEDIN_CADENCE_PLAN.md), [LINKEDIN_POST_013.md](./LINKEDIN_POST_013.md), [case_001_anonymized.md](../case-studies/case_001_anonymized.md).

---

**Title — العنوان**

المسوّدة جهزت في 12 دقيقة. الموافقة استغرقت 4 ساعات. هذا هو التصميم / The draft was ready in 12 minutes. Approval took 4 hours. That is the design.

---

## العربية أولاً

### نمط آمن، بلا اسم

> **هذا نمط مُجمَّع من منهجية ديليكس. لا يصف عميلاً بعينه ولا يُسمّي أحداً.**

سؤال نسمعه كثيراً: "إذا كان النظام يُنتج المسوّدة في دقائق، لماذا لا يُرسلها مباشرة؟ لماذا أنتظر؟" الجواب هو قرار `REQUIRE_APPROVAL`، وهذا النمط يشرح لماذا الانتظار ميزة لا عيب.

### ما حدث

سبرنت لعميل في الخدمات المهنية. ضمن المخرَجات، مسوّدة رسالة لحساب راكد عالي الترتيب. أنتجت المنظومة المسوّدة في حوالي 12 دقيقة من لحظة توفّر البيانات النظيفة.

لم تخرج المسوّدة. منظومة الحوكمة وسمتها `DRAFT_ONLY` ثم `REQUIRE_APPROVAL`: لا تُكمَل قبل اعتماد إنسان مُسمّى من جانب العميل.

### الساعات الأربع

استغرقت الموافقة قرابة أربع ساعات. ماذا حدث فيها؟

- قرأ مسؤول المبيعات لدى العميل المسوّدة، وعدّل جملة افتتاحية ليجعلها أقرب لصوت الشركة.
- لاحظ أن المسوّدة تشير إلى مشروع سابق؛ تحقّق أن الإشارة دقيقة وأن جواز المصدر يسمح بذكرها.
- قرّر أن التوقيت غير مناسب لهذا الحساب تحديداً، وأجّل الإرسال يوماً.

أربع ساعات لم تكن تأخيراً تقنياً. كانت أربع ساعات من حُكم بشري على رسالة ستحمل اسم شركة العميل.

### لماذا هذا هو التصميم

لو أرسل النظام المسوّدة في الدقيقة الثانية عشرة، لكان وفّر أربع ساعات وخاطر بثلاثة أشياء: جملة افتتاحية لا تُشبه العميل، إشارة قد تكون غير دقيقة، وتوقيت سيّئ. الفجوة بين "جاهز" و"مُرسَل" ليست بطئاً في المنظومة؛ إنها المساحة التي يُمارَس فيها الحُكم.

ديليكس لا يُرسل رسائل خارجية نيابة عن أحد. المسوّدة تُنتَج بسرعة؛ القرار يبقى بطيئاً بقدر ما يتطلّبه الحُكم البشري.

### الدرس للمؤسس

السرعة التي تهمّك ليست سرعة إنتاج المسوّدة، بل سرعة وصولك إلى قرار جيّد. منظومة تُنتج بسرعة وتنتظر اعتمادك تمنحك الاثنين: مادة جاهزة، وسيطرة كاملة على ما يحمل اسمك.

### دعوة

ابدأ بتشخيص مجاني خلال 24 ساعة. سترى قرار `REQUIRE_APPROVAL` مُطبَّقاً عليك قبل أن تدفع ريالاً — لا مخرَج يخرج بلا اعتمادك.

---

## English

### A case-safe pattern, no name

> **This is an aggregated pattern from the Dealix methodology. It describes no specific customer and names no one.**

A question we hear often: "If the system produces the draft in minutes, why not send it directly? Why do I wait?" The answer is the `REQUIRE_APPROVAL` decision, and this pattern explains why the wait is a feature, not a flaw.

### What happened

A sprint for a customer in professional services. Among the deliverables, a draft message for a high-ranked dormant account. The runtime produced the draft in roughly 12 minutes from the moment clean data was available.

The draft did not leave. The Governance Runtime tagged it `DRAFT_ONLY` then `REQUIRE_APPROVAL`: it does not complete before a named human on the customer's side approves it.

### The four hours

Approval took about four hours. What happened in them?

- The customer's sales lead read the draft and edited an opening line to bring it closer to the company's voice.
- They noticed the draft referenced a prior project; they verified the reference was accurate and that the Source Passport permitted mentioning it.
- They decided the timing was wrong for this specific account and deferred the send by a day.

Those four hours were not a technical delay. They were four hours of human judgment on a message that would carry the customer's company name.

### Why this is the design

Had the system sent the draft at minute twelve, it would have saved four hours and risked three things: an opening line that does not sound like the customer, a reference that might be inaccurate, and bad timing. The gap between "ready" and "sent" is not slowness in the runtime; it is the space where judgment is exercised.

Dealix does not send external messages on anyone's behalf. The draft is produced fast; the decision stays as slow as human judgment requires.

### The lesson for the founder

The speed that matters to you is not the speed of producing the draft; it is the speed of reaching a good decision. A runtime that produces fast and waits for your approval gives you both: ready material, and full control over what carries your name.

### CTA

Start with a free 24-hour diagnostic. You will see the `REQUIRE_APPROVAL` decision applied to you before you pay a riyal — no output leaves without your approval.

---

`#RevenueOps` `#B2B`

#السعودية #عمليات_الإيراد

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
