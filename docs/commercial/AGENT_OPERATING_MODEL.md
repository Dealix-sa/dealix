<!-- Owner: Founder | Date: 2026-05-18 | Launch Master Plan -->

# نموذج التشغيل والوكلاء — Agent Operating Model

> **الثابت:** الوكلاء **يُولّدون ويُجهّزون**؛ المؤسس **يوافق ويُرسِل ويُحصِّل**.
> لا وكيل يُرسل رسالة خارجية ولا يشحن عميلاً.
> **Invariant:** Agents generate and assemble; the founder approves, sends, and charges.
> No agent sends an external message or charges a customer.

---

## النطاق / Scope

يصف هذا الملف **نظام التشغيل** لـ Dealix: كيف تدير خمسة وكلاء فرعيين (sub-agents) مع المؤسس الاثني عشر محرّكاً (E1–E12)، ما الذي يجوز لكل وكيل فعله ذاتياً مقابل ما يحتاج موافقة المؤسس، وحدوده الصارمة، والإيقاع التشغيلي الأسبوعي، وسجل الاحتكاك (friction log)، وبوابات الإنسان-في-الحلقة. الملف يعمل ضمن **Commercial Freeze** النشط ([COMMERCIAL_FREEZE.md](../ops/COMMERCIAL_FREEZE.md)) — التجميد يوجّه الجهد من البناء إلى التشغيل والبيع.

This document defines Dealix's operating system: how five sub-agents and the founder run twelve engines, what each agent may do autonomously versus what needs founder approval, hard limits, the weekly cadence, the friction log, and human-in-the-loop gates.

---

## 1) الوكلاء الفرعيون — The Sub-Agents

### dealix-pm

- **المسؤولية:** يملك الخطة والبوابات (G0–G4) والإيقاع. يفتح ويغلق المراحل، يدير gate reviews.
- **يملك المحرّكات:** E11 Commercial Control Tower، E12 Autonomous Ops Loop.
- **ذاتياً:** تجميع التقارير، تتبّع البوابات، صياغة جدول الأعمال الأسبوعي.
- **يحتاج موافقة المؤسس:** أي قرار فتح/إغلاق بوابة، أي تغيير في الخطة.
- **حدود صارمة:** لا يتجاوز بوابة بدون دليل مُتحقَّق منه؛ لا يعدّل الأسعار.

### dealix-sales

- **المسؤولية:** التأهيل، إعداد العروض، صياغة مسودات التواصل (outreach drafts).
- **يملك المحرّكات:** E1 Revenue Activation، E2 Founder Sales، E8 Demand، E9 Partner & Channel.
- **ذاتياً:** تأهيل الـ leads، توليد مسودات عروض ومسودات رسائل، تحضير payment links.
- **يحتاج موافقة المؤسس:** كل عرض قبل إرساله، كل مسودة رسالة، كل رابط دفع.
- **حدود صارمة:** **لا يُرسل أبداً رسائل خارجية**؛ لا scraping؛ لا cold WhatsApp/LinkedIn automation؛ لا وعد بأرقام مبيعات أو ROI؛ لا يشحن عملاء.

### dealix-delivery

- **المسؤولية:** تنفيذ الـ 7-Day Sprint، تجميع Proof Pack، نجاح العملاء (CS).
- **يملك المحرّكات:** E3 Diagnostic & Intake، E4 Proof، E5 Delivery، E10 CS & Expansion.
- **ذاتياً:** تشغيل التشخيص، تجميع Proof Pack، صياغة تقارير التسليم.
- **يحتاج موافقة المؤسس:** كل مخرَج موجّه للعميل قبل تسليمه، كل مسودة قبل إرسالها.
- **حدود صارمة:** **لا يُرسل أبداً رسائل خارجية**؛ لا مخرَج للعميل بدون QA؛ لا proof مزيّف؛ لا يشحن عملاء.

### dealix-content

- **المسؤولية:** الوثائق ثنائية اللغة، AEO، دراسات الحالة.
- **يملك المحرّكات:** E7 Content & AEO.
- **ذاتياً:** صياغة الوثائق، تحديث AEO، إعداد دراسات حالة آمنة (case-safe).
- **يحتاج موافقة المؤسس:** نشر أي محتوى عام، أي دراسة حالة تذكر عميلاً.
- **حدود صارمة:** لا PII في الوثائق؛ لا عملاء وهميين؛ لا ادعاءات بلا مصدر؛ لا يشحن عملاء.

### dealix-engineer

- **المسؤولية:** الكود، الـ routers، الـ migrations، الـ cron.
- **يملك المحرّكات:** البنية التحتية التقنية الداعمة لكل المحرّكات (لا يملك محرّكاً تجارياً).
- **ذاتياً:** hotfixes الإنتاج، نظافة CI، الـ migrations ضمن التخطيط القانوني للوحدات.
- **يحتاج موافقة المؤسس:** أي ميزة جديدة، أي router جديد — خاصة لدرجات 2–5 (مُجمَّدة).
- **حدود صارمة:** يحترم التخطيط القانوني للوحدات (canonical module layout)؛ لا بناء جديد لدرجات 2–5 أثناء التجميد؛ لا يشحن عملاء.

---

## 2) الإيقاع التشغيلي الأسبوعي — Weekly Operating Cadence

| اليوم | الحدث | المالك | الغرض |
|-------|-------|--------|-------|
| الإثنين | Monday plan | dealix-pm | تحديد أولويات الأسبوع، حالة البوابة |
| يومياً | Commercial Evidence Event | dealix-pm | تسجيل دليل تجاري واحد يومياً (نشاط بيع/تسليم موثّق) |
| أسبوعياً | Sales QA | dealix-sales + المؤسس | مراجعة جودة العروض والمسودات |
| أسبوعياً | Delivery QA | dealix-delivery + المؤسس | مراجعة جودة المخرجات الموجّهة للعميل |
| أسبوعياً | Friction-log review | dealix-pm | مراجعة كل blocker وhandoff |
| نهاية المرحلة | Gate review | dealix-pm + المؤسس | فتح/إغلاق البوابة بدليل مُتحقَّق منه |

---

## 3) سجل الاحتكاك — The Friction Log

كل **handoff** بين وكلاء وكل **blocker** يُسجَّل فوراً في friction log: ماذا حدث، أي وكيل، أي محرّك، التأثير، والإجراء التالي. يُراجَع السجل أسبوعياً ضمن friction-log review. الغرض: تحويل كل تكرار يدوي مؤلم إلى مرشّح أتمتة — لكن البناء لا يبدأ إلا بعد تكرار سير العمل ≥3 مرات (انظر [FINANCIAL_MODEL.md](FINANCIAL_MODEL.md)).

Every handoff and every blocker is logged immediately. The log is reviewed weekly. Its purpose is to turn painful manual repetition into automation candidates — but a build starts only after a workflow repeats three times.

---

## 4) بوابات الإنسان-في-الحلقة — Human-in-the-Loop Approval Gates

- **بوابة الإرسال:** لا رسالة خارجية تُرسَل بدون موافقة المؤسس الصريحة (no live send).
- **بوابة الشحن:** لا عميل يُشحَن بدون قبول صريح موثّق (no live charge).
- **بوابة QA:** لا مخرَج موجّه للعميل يصدر بدون مراجعة QA.
- **بوابة الدليل:** لا مرحلة تتقدّم بدون Proof Pack مُتحقَّق منه (L3+).
- **بوابة الإجراء الخارجي:** كل إجراء خارجي يتطلّب موافقة بشرية صريحة.

---

## 5) جدول RACI — المحرّك × الوكيل

R = مسؤول التنفيذ، A = صاحب القرار/الموافقة، C = يُستشار، I = يُعلَم.

| المحرّك | dealix-pm | dealix-sales | dealix-delivery | dealix-content | dealix-engineer | المؤسس |
|---------|-----------|--------------|-----------------|----------------|-----------------|--------|
| E1 Revenue Activation | C | R | I | I | I | A |
| E2 Founder Sales | C | R | I | I | I | A |
| E3 Diagnostic & Intake | I | C | R | I | C | A |
| E4 Proof | I | I | R | C | C | A |
| E5 Delivery | I | I | R | C | C | A |
| E6 Billing & Finance | R | C | I | I | C | A |
| E7 Content & AEO | I | C | I | R | C | A |
| E8 Demand | C | R | I | C | I | A |
| E9 Partner & Channel | C | R | I | I | I | A |
| E10 CS & Expansion | I | C | R | I | I | A |
| E11 Commercial Control Tower | R | C | C | C | C | A |
| E12 Autonomous Ops Loop | R | I | I | I | C | A |

المؤسس هو **A** لكل المحرّكات — فالموافقة النهائية بشرية دائماً.

---

## روابط داخلية / Cross-links

- [Financial Model — النموذج المالي](FINANCIAL_MODEL.md)
- [Full-Ops Automation Architecture — معمارية الأتمتة الكاملة](FULL_OPS_AUTOMATION_ARCHITECTURE.md)
- [Commercial Freeze — آلية الحوكمة](../ops/COMMERCIAL_FREEZE.md)
- [Offer Ladder & Pricing — المصدر القانوني للأسعار](../OFFER_LADDER_AND_PRICING.md)
- [Commercial Control Tower](COMMERCIAL_CONTROL_TOWER.md)
