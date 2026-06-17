# Follow-Up Sequences — سلاسل المتابعة

**Version:** 1.0 | **Owner:** Founder | **Last Updated:** 2026-06-01

Cross-links: [OBJECTION_LIBRARY.md](OBJECTION_LIBRARY.md) | [DEAL_QUALIFICATION_SCORECARD.md](DEAL_QUALIFICATION_SCORECARD.md) | [../growth/DRAFT_QUEUE_SCHEMA.json](../growth/DRAFT_QUEUE_SCHEMA.json) | [../growth/OMNI_CHANNEL_GROWTH_OS.md](../growth/OMNI_CHANNEL_GROWTH_OS.md)

---

## Rules That Apply to All Sequences — قواعد مشتركة لجميع السلاسل

- Every message draft waits for founder approval before send. No auto-send.
- No more than one message per contact per channel per sequence step.
- If a contact replies at any point — stop the sequence and handle the reply directly.
- WhatsApp: opt-in + approved template only. LinkedIn: manual only.
- Mark contact as "dormant" after the last sequence step if no reply. Do not delete — park for reactivation.
- All drafts use [DRAFT_QUEUE_SCHEMA.json](../growth/DRAFT_QUEUE_SCHEMA.json) with sequence field populated.

---

## Sequence 1 — Post-Discovery Call | ما بعد مكالمة الاكتشاف

**Trigger:** Discovery call completed. Proposal not yet sent.

### Day 1 — Thank You + Summary

**Channel:** Email
**Subject AR:** شكراً على وقتك — ملخص ما ناقشناه
**Subject EN:** Thank you for your time — summary of our discussion

**Body template:**
شكراً لوقتك اليوم. خلال المكالمة ناقشنا [PAIN_POINT_1] و[PAIN_POINT_2]. سأرسل لك اقتراحاً مخصصاً خلال [N] أيام عمل يتضمن النطاق المقترح ونقاط البداية.

Thank you for your time today. We discussed [PAIN_POINT_1] and [PAIN_POINT_2]. I will send a tailored proposal within [N] business days covering the proposed scope and starting points.

**Trigger for next step:** Proposal sent (end Sequence 1, begin Sequence 2). If no proposal ready by Day 3, send Day 3 message.

---

### Day 3 — Proposal Status Update

**Channel:** Email
**Subject AR:** تحديث على الاقتراح — [COMPANY_LABEL]
**Subject EN:** Proposal update — [COMPANY_LABEL]

**Body template:**
أعمل على صياغة الاقتراح بناءً على ما ناقشناه. لديّ سؤال إضافي لضمان دقة النطاق: [SPECIFIC_CLARIFICATION_QUESTION]. هل يمكنك الإجابة بكلمة واحدة أو جملة قصيرة؟

I am finalizing the proposal based on our discussion. I have one follow-up question to ensure accurate scoping: [SPECIFIC_CLARIFICATION_QUESTION]. Can you respond in a word or short sentence?

**Trigger for next step:** If reply received → incorporate and finalize proposal. If no reply → send Day 7 message.

---

### Day 7 — Gentle Check-In

**Channel:** Email (primary) or LinkedIn manual (if email not opened)
**Subject AR:** هل أنت متاح للمراجعة؟
**Subject EN:** Available for a quick review?

**Body template:**
أعرف أن لديك جدولاً مزدحماً. الاقتراح جاهز — أرسله الآن أم تفضّل أن نحدد 15 دقيقة لمراجعته معاً؟

I know your schedule is full. The proposal is ready — shall I send it now, or would you prefer 15 minutes to review it together?

**Trigger for next step:** If reply → proceed. If no reply after Day 7 → send Day 14 message.

---

### Day 14 — Final Post-Discovery Touch

**Channel:** Email
**Subject AR:** هل هذا الوقت المناسب؟
**Subject EN:** Is this the right time?

**Body template:**
تواصلت معك عدة مرات دون رد. إذا تغيّرت الأولويات أو توقيت المشروع — هذا مفهوم تماماً. هل تريد أن أتابع معك في [90 يوماً]؟ أو يمكنني إرسال الاقتراح الآن إذا كنت مهتماً.

I have reached out a few times without a response. If priorities have shifted or the project timing has changed, that is completely understandable. Would you like me to follow up in [90 days]? Or I can send the proposal now if you are interested.

**Trigger for next step:** No reply → mark as dormant → enter Dormant Reactivation at Week 8.

---

## Sequence 2 — Post-Proposal Sent | ما بعد إرسال الاقتراح

**Trigger:** Proposal document sent to prospect. Clock starts on day of send.

### Day 2 — Confirm Receipt

**Channel:** Email
**Subject AR:** تأكيد استلام الاقتراح
**Subject EN:** Confirming proposal receipt

**Body template:**
أردت التأكد من وصول الاقتراح بشكل صحيح. هل لديك أي سؤال أوّلي بعد الاطلاع عليه؟

I wanted to confirm the proposal reached you correctly. Do you have any initial questions after reviewing it?

---

### Day 5 — Value Reinforcement

**Channel:** Email
**Subject AR:** السؤال الذي يُسأل دائماً في هذه المرحلة
**Subject EN:** The question that always comes up at this stage

**Body template:**
في كثير من الحالات، العملاء في هذه المرحلة لديهم سؤال واحد لم يُجَب عليه في الاقتراح. ما هو سؤالك؟

At this stage, most clients have one question the proposal did not fully answer. What is yours?

---

### Day 10 — Decision Timeline Check

**Channel:** Email (primary) or LinkedIn manual
**Subject AR:** ما هو الجدول الزمني لقراركم؟
**Subject EN:** What is your decision timeline?

**Body template:**
أريد أن أفهم توقيت قراركم حتى أتمكن من تخطيط بداية المشروع المناسب. هل القرار في غضون أسبوعين أم أطول؟

I want to understand your decision timeline so I can plan the right project start. Is the decision within two weeks or longer?

**Trigger for next step:** If timeline > 6 months → park. If no reply → Day 21 message.

---

### Day 21 — Final Proposal Follow-Up

**Channel:** Email
**Subject AR:** هل لا يزال المشروع ضمن خططكم؟
**Subject EN:** Is the project still in your plans?

**Body template:**
مرّت ثلاثة أسابيع منذ إرسال الاقتراح. إذا تغيّر وضع الميزانية أو الأولويات — أخبرني وسنضع المشروع في قائمة الانتظار بدون ضغط. إذا كنت لا تزال مهتماً، خطوتي التالية هي [CTA_SPECIFIC].

Three weeks have passed since I sent the proposal. If the budget situation or priorities have changed, let me know and we will put the project on hold without pressure. If you are still interested, my next suggested step is [CTA_SPECIFIC].

**Trigger for next step:** No reply → dormant. Park for Dormant Reactivation at Week 8.

---

## Sequence 3 — Post-Demo or Pilot | ما بعد العرض أو التجريب

**Trigger:** Demo session completed or pilot delivered.

### Day 1 — Pilot Results Summary

**Channel:** Email
**Subject AR:** ملخص نتائج التجربة — [PROJECT_LABEL]
**Subject EN:** Pilot results summary — [PROJECT_LABEL]

**Body template:**
بناءً على التجربة التي أجريناها، هذه أبرز النتائج: [RESULT_1], [RESULT_2]. الخطوة التالية المقترحة هي [NEXT_PHASE]. هل لديك تعليقات على ما رأيته؟

Based on the pilot, these are the headline findings: [RESULT_1], [RESULT_2]. The proposed next step is [NEXT_PHASE]. Do you have feedback on what you observed?

---

### Day 7 — Decision Facilitation

**Channel:** Email
**Subject AR:** ما الذي يحتاجه فريقكم للمضي قدماً؟
**Subject EN:** What does your team need to move forward?

**Body template:**
هل هناك أشخاص آخرون في الفريق يحتاجون إلى مراجعة النتائج؟ يمكنني تقديم ملخصاً تنفيذياً موجزاً إذا كان ذلك مفيداً.

Are there other team members who need to review the results? I can prepare a brief executive summary if that would be useful.

---

### Day 21 — Final Pilot Follow-Up

**Channel:** Email
**Subject AR:** قرار المضي قدماً في [MONTH]
**Subject EN:** Decision to proceed in [MONTH]

**Body template:**
مرّت ثلاثة أسابيع من تسليم التجربة. هل اتخذتم قراراً بشأن المرحلة الكاملة؟ إذا كان هناك شرط أو معلومة إضافية تحتاجها — أخبرني.

Three weeks have passed since pilot delivery. Have you reached a decision on the full phase? If there is a requirement or additional information you need — let me know.

**Trigger for next step:** No reply → dormant. Park for Dormant Reactivation.

---

## Sequence 4 — Dormant Lead Reactivation | إعادة تنشيط العميل المحتمل الخامل

**Trigger:** No engagement for 4+ weeks following last active sequence. Contact marked dormant.

### Week 4 — Sector Insight

**Channel:** Email
**Subject AR:** تطوّر في قطاع [SECTOR] — ما قد يهمك
**Subject EN:** A development in [SECTOR] — what may interest you

**Body template:**
لاحظنا [SPECIFIC_SECTOR_OBSERVATION — e.g., "FMs in the GCC reporting a 30% increase in compliance reporting workload following new regulations"]. إذا كان هذا يعكس ما تشهده شركتكم، يستحق محادثة قصيرة.

We have observed [SPECIFIC_SECTOR_OBSERVATION]. If this reflects what your organization is experiencing, it may warrant a short conversation.

---

### Week 8 — Direct Re-Engagement

**Channel:** Email (primary) or LinkedIn manual
**Subject AR:** هل تغيّر شيء منذ آخر تواصل؟
**Subject EN:** Has anything changed since we last spoke?

**Body template:**
آخر تواصل بيننا كان في [MONTH]. هل تغيّرت أولويات شركتكم أو توفرت ميزانية جديدة؟ إذا كان الوقت مناسباً الآن — أنا هنا.

Our last contact was in [MONTH]. Have your company's priorities or budget situation changed? If the timing is right now — I am here.

---

### Week 12 — Final Re-Engagement

**Channel:** Email
**Subject AR:** آخر رسالة — ثم نضع ملفكم في الأرشيف
**Subject EN:** Final outreach — then we will archive your file

**Body template:**
هذه آخر رسالة تلقائية في سلسلتنا. إذا لم يكن الوقت مناسباً الآن، سنضع ملفكم في الأرشيف ونراجعه العام القادم. إذا تغيّر شيء في أي وقت — تواصل معي مباشرة.

This is the final message in our outreach sequence. If the timing is not right, we will archive your file and revisit next year. If anything changes at any point — reach out directly.

**After Week 12 with no reply:** Archive contact. Flag for annual review only.

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
