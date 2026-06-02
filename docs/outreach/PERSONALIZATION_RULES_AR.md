# قواعد التخصيص — Personalization Rules
# Personalization Rules — AR + EN

**المسار:** `docs/outreach/PERSONALIZATION_RULES_AR.md`
**الجمهور:** المؤسس + كاتب المسودات + مراجع الامتثال
**آخر تحديث:** 2026-06-02
**الحالة:** نافذ

---

## المبدأ / Core Principle

**التخصيص الحقيقي يبدأ من إشارة موجودة، لا من استنتاج مصطنع.**

Real personalization starts from a signal that exists. It does not start from a generic assumption dressed up as a specific observation.

الحد الأدنى للإرسال: **مستوى P1**. أي مسودة عند مستوى P0 يحجبها المصنع تلقائياً.
Minimum level to be sendable: **P1**. A P0 draft is blocked by the factory gate.

---

## 1. مستويات التخصيص P0–P3 / Personalization Levels

### P0 — عام تماماً / Generic

**التعريف:** الرسالة يمكن أن تُرسَل لأي شركة في أي قطاع دون تغيير أي كلمة.

**Definition:** The message could be sent to any company in any sector without changing a single word.

**مثال عربي (ممنوع):**
> "السلام عليكم، نرى أن شركتكم قد تستفيد من حل لتسريع المبيعات..."

**English example (banned):**
> "Hi, I think your company could benefit from a solution to accelerate your sales..."

**القرار:** محجوب — لا تُنتج المسودة.
**Decision:** Blocked — draft is not produced.

---

### P1 — تخصيص قطاعي / Sector-Level

**التعريف:** الرسالة تُشير لقطاع محدد وألم قطاعي موثّق في `research_agent.py`. ليس ذكر اسم الشركة فقط.

**Definition:** The message references a specific sector and a documented sector-level pain from `research_agent.py`. Mentioning the company name alone does not qualify.

**الإشارات المقبولة:**
- ذكر القطاع ونوع العمل ("مكتب عقاري في الرياض")
- الإشارة لنوع leads الشائع في القطاع ("استفسارات الحجوزات MICE")
- الإشارة لقناة الاستقبال السائدة في القطاع ("واتساب + اتصالات")
- الإشارة لموسم أو ظاهرة قطاعية ("موسم العمرة لشركات الفنادق")

**مثال عربي (مقبول — P1):**
> "مكاتب الوساطة العقارية في الرياض غالباً تستقبل استفسارات عبر واتساب — لا يوجد نظام فرز موحّد يُوجّه الجاد منها للمندوب الصحيح."

**English example (acceptable — P1):**
> "Real estate brokerage offices in Riyadh typically receive inquiries through WhatsApp with no unified triage system to route qualified prospects to the right agent."

**القرار:** الحد الأدنى المسموح به للإرسال.
**Decision:** Minimum acceptable level for sending.

---

### P2 — تخصيص بإشارة شركة / Company-Level Signal

**التعريف:** الرسالة تتضمن إشارة مرتبطة بهذه الشركة تحديداً، مستندة لبيانات من المصادر المعتمدة (موقع الشركة، Google Business، منصة Maroof، مشاركات LinkedIn العامة).

**Definition:** The message contains a signal specific to this company, drawn from approved sources (company website, Google Business, Maroof platform, public LinkedIn posts).

**الإشارات المقبولة:**
- الموقع الجغرافي للشركة + تخصصها ("فندق في الطائف يخدم موسم الرحلات")
- خدمة أو منتج محدد ظاهر على موقعهم ("قاعة أفراح تتسع لـ 500 شخص")
- مرحلة نمو واضحة ("افتتاح فرع جديد ظهر في Google Maps")
- مشاركة عامة حديثة ("أعلنتم مؤخراً عن خدمة التوصيل")

**مثال عربي (مقبول — P2):**
> "شاهدنا أنكم تقدمون خدمات تموين الفعاليات في جدة — هذا النوع من العمل يعتمد على استفسارات B2B تحتاج رداً دقيقاً خلال ساعات."

**English example (acceptable — P2):**
> "I noticed your company offers event catering services in Jeddah — this type of B2B inquiry typically requires a precise response within hours to convert."

**القرار:** مستوى مفضّل — يرفع احتمال رد إيجابي بشكل ملحوظ.
**Decision:** Preferred level — meaningfully improves response probability.

---

### P3 — تخصيص عميق / Deep Personalization

**التعريف:** الرسالة تتضمن إشارة حديثة ومحددة جداً تُظهر معرفة واضحة بالشركة، مع ربط مباشر بالعرض.

**Definition:** The message contains a recent and highly specific signal demonstrating clear knowledge of the company, with a direct connection to the offer.

**الإشارات المقبولة:**
- اقتباس مباشر من منشور LinkedIn حديث للمسؤول (نص حقيقي)
- ذكر مشروع أو توسع أعلنوه في مصادر عامة مؤخراً
- إشارة لمتغير موسمي محدد للشركة يُذكر بسياق صحيح
- معلومة من اجتماع سابق أو محادثة موثّقة

**مثال عربي (مقبول — P3):**
> "قرأت تغريدتكم الأسبوع الماضي عن توسع الفرع في حي النرجس — هذه المرحلة عادةً تزيد حجم الاستفسارات قبل اكتمال الفريق."

**English example (acceptable — P3):**
> "I read your post last week about the new branch opening in Al-Narjis district — expansion phases like this typically increase inbound inquiry volume before the team is fully staffed."

**القرار:** أعلى مستوى — يُستخدم للحسابات ذات الأولوية القصوى.
**Decision:** Highest level — reserved for top-priority accounts.

---

## 2. ما يُحظر تحت مسمى "تخصيص" / What Is Banned as Fake Personalization

| الصياغة الممنوعة | سبب الحظر |
|---|---|
| "رأيت موقعكم" دون ذكر شيء محدد | عامة تماماً — لا قيمة معلوماتية |
| "لاحظت نشاطكم في السوق" | مبهم، ينطبق على أي شركة |
| "أثرى بروفايلكم على LinkedIn" | مطوّل لا مضمون — لا إشارة حقيقية |
| "I saw your impressive website" | Generic filler — no specific signal |
| "نعلم أنكم تسعون للنمو" | كل شركة تسعى للنمو — لا إشارة |
| "فريقكم المتميز" | مديح فارغ — لا إشارة |
| "شهدنا نجاحاتكم المتعددة" | مجاملة بدون مصدر |
| Re: أو Fwd: في موضوع رسالة لا تعقيب فعلي عليها | تضليل مباشر — محظور من المصنع |

---

## 3. قائمة تدقيق التخصيص / Personalization Checklist

قبل كل مسودة يُجاب على هذه الأسئلة:

- [ ] هل ذُكرت إشارة يمكن ربطها بهذه الشركة تحديداً؟
- [ ] هل مصدر الإشارة مذكور في `personalization_note` وفي `sources_used`؟
- [ ] هل الإشارة حقيقية (موقع، بحث يدوي، Google Business) لا مفترضة؟
- [ ] هل الرسالة مختلفة عما يمكن إرساله لمنافس مباشر لهذه الشركة؟
- [ ] هل `personalization_score` ≥ P1 في حقول المسودة؟
- [ ] هل سطر الموضوع يعكس محتوى الرسالة بصدق؟

إذا كانت إجابة أي سؤال "لا" — المسودة لا تُنتج.

---

## 4. أمثلة مقارنة / Side-by-Side Examples

### مثال 1 — قطاع الفنادق / Hospitality Sector

| المستوى | النص العربي | النص الإنجليزي | القرار |
|---|---|---|---|
| P0 — ممنوع | "نعرض عليكم حلاً لتحسين مبيعاتكم" | "We offer a solution to improve your sales" | محجوب |
| P1 — مقبول | "فنادق موسم رمضان + الإجازات تستقبل استفسارات قاعات وضيافة تحتاج رداً سريعاً على مدار الساعة" | "Hotels during Ramadan and holiday seasons receive venue and hospitality inquiries that require around-the-clock fast responses" | مسموح |
| P2 — مفضّل | "فندقكم في أبها يخدم زوار موسم الربيع — الاستفسارات عن قاعات المؤتمرات والإفطار الجماعي تحتاج ردّاً قبل أن يلتفت العميل لمنافس" | "Your Abha property serves spring season visitors — conference hall and group iftar inquiries need a response before the prospect turns to a competitor" | مسموح + مفضّل |

### مثال 2 — قطاع اللوجستيات / Logistics Sector

| المستوى | النص العربي | النص الإنجليزي | القرار |
|---|---|---|---|
| P0 — ممنوع | "نستطيع مساعدتكم في تطوير عملياتكم" | "We can help you improve your operations" | محجوب |
| P1 — مقبول | "شركات الشحن السعودية تستقبل RFQ يومياً — تأخير عشر دقائق في الرد يرسل العميل لمنافس" | "Saudi freight companies receive daily RFQs — a ten-minute response delay sends the client to a competitor" | مسموح |
| P3 — أعلى مستوى | "قرأت في بيان شراكتكم الأسبوع الماضي أنكم تتوسعون لخدمة الشحن البري بين المدن — هذا التوسع عادةً يضاعف حجم RFQ الواردة قبل اكتمال نظام تتبع العملاء" | "I read in your partnership announcement last week that you're expanding into inter-city road freight — this type of expansion typically doubles inbound RFQ volume before customer tracking systems are in place" | مسموح + أولوية |

---

## 5. العلاقة بمصنع المسودات / Connection to Draft Factory

- حقل `personalization_score` في `outreach_draft` يحمل قيمة P0–P3
- حقل `personalization_note` يحفظ الإشارة الفعلية المستخدمة
- حقل `sources_used` في `CompanyBrief` يوثّق مصدر الإشارة
- المصنع في `daily_targeting.py` يحجب أي مسودة بـ P0
- مراجع الموافقة يتحقق من المستوى قبل الموافقة على الإرسال

راجع: [`docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md`](./COLD_EMAIL_DRAFT_FACTORY_AR.md) — القسم 3: بوابة المنع

---

## روابط ذات صلة

- [`docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md`](./COLD_EMAIL_DRAFT_FACTORY_AR.md) — بوابة منع المسودات
- [`docs/outreach/COLD_EMAIL_SEQUENCES_AR.md`](./COLD_EMAIL_SEQUENCES_AR.md) — القوالب مع فتحات التخصيص
- [`docs/outreach/COLD_EMAIL_SEQUENCES_EN.md`](./COLD_EMAIL_SEQUENCES_EN.md) — النسخة الإنجليزية للقوالب
- [`docs/outreach/PROSPECT_RESEARCH_OS_AR.md`](./PROSPECT_RESEARCH_OS_AR.md) — كيف تُجمع الإشارات
- [`docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md`](./COLD_EMAIL_COMPLIANCE_AR.md) — قواعد الامتثال الكاملة
- [`docs/gtm/MARKET_PRODUCTION_OS_AR.md`](../gtm/MARKET_PRODUCTION_OS_AR.md) — الفهرس الرئيسي
- `auto_client_acquisition/email/research_agent.py` — `sources_used` و`personalization_note`

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
