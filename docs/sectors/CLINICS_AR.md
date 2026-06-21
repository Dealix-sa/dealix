# دليل قطاع — العيادات — Clinics Playbook

> دليل تشغيلي داخلي. كل الرسائل أدناه **مسودات** ينسخها المؤسس ويعدّلها ويرسلها يدوياً. لا إرسال آلي، لا قوائم مشتراة، لا ضمانات.
> Internal operating playbook. Every message below is a DRAFT sent manually. No auto-send, no purchased lists, no guarantees.
>
> **تنبيه خاص:** بيانات المرضى حساسة. نتعامل مع **بيانات تجارية/استفسارات** فقط (B2B وعلاقات الإحالة)، لا سجلات صحية، تحت DPA وامتثال PDPL.
> **Special note:** Patient data is sensitive. We handle commercial/inquiry data only (B2B and referral relationships), never clinical records, under DPA and PDPL compliance.
>
> المرجع: [README القطاعات](README.md) · [حزم RevOps](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · [الكتالوج](../../autonomous_growth/product_catalog.py)

---

## 1. الألم الرئيسي / Core pain

**عربي:** العيادة (تجميل، أسنان، تخصصات اختيارية) تستقبل استفسارات حجز كثيرة عبر قنوات متعددة، لكن الاستفسار يبرد قبل تأكيد الموعد، والمتابعة تعتمد على موظف استقبال مشغول. مصادر الإحالة (شركات تأمين، عيادات محيلة، شركات لباقات الموظفين) غير مرتّبة. النتيجة: استفسارات جيدة تضيع، وعلاقات B2B قيّمة بلا متابعة منظّمة.

**English:** A clinic (aesthetic, dental, elective specialties) receives many booking inquiries across channels, but inquiries cool before the appointment is confirmed, and follow-up depends on a busy receptionist. Referral sources (insurers, referring clinics, corporate wellness buyers) are unorganized. Result: good inquiries are lost and valuable B2B relationships go untracked.

---

## 2. صاحب القرار / Decision maker

- **الأساسي:** مالك العيادة / المدير الطبي التنفيذي أو مدير العمليات. — Clinic owner / executive medical director or operations manager.
- **المؤثّر:** مدير التسويق أو مسؤول علاقات الشركات/التأمين. — Marketing manager or corporate/insurance relations lead.
- **بوّاب:** الاستقبال الذي يستقبل الاستفسارات. — Front desk that fields inquiries.

---

## 3. مؤشرات أن العميل مناسب / Good-fit signals

- خدمات اختيارية بهامش جيد (تجميل، أسنان، لياقة طبية). — Elective, higher-margin services.
- استفسارات حجز متكررة + علاقات B2B (تأمين/شركات). — Recurring booking inquiries plus B2B relationships.
- يشكو من «استفسارات لا تتحول لمواعيد». — Complains inquiries don't become appointments.
- عملية وعي بالخصوصية ومستعدة لتوقيع DPA. — Privacy-aware, willing to sign a DPA.

---

## 4. مؤشرات أنه غير مناسب / Disqualifiers

- يطلب التعامل مع **سجلات/بيانات صحية للمرضى** — خارج النطاق تماماً. — Asks us to handle clinical/patient records — fully out of scope.
- يطلب جمع/شراء قوائم مرضى أو إرسال بارد — نرفض. — Wants purchased patient lists or cold blasts — declined.
- يريد ضمان عدد حجوزات. — Wants a guaranteed booking count.
- لا قناة استفسار ولا علاقات إحالة. — No inquiry channel, no referral relationships.

---

## 5. أول منتج نبيعه / First product to sell

**Revenue Intelligence Sprint — 499 ريال** (سبرينت ذكاء الإيرادات).
المصدر: [`product_catalog.py`](../../autonomous_growth/product_catalog.py).

- **لماذا:** عتبة منخفضة وإثبات سريع على **بيانات الاستفسارات وعلاقات الإحالة** (لا بيانات سريرية): ترتيب الاستفسارات حسب الجاهزية و3 فرص B2B/إحالة قابلة للتطبيق.
- **بديل أعلى عند الجاهزية ووجود فروع:** Managed Ops (2,999–4,999/شهر) لإدارة شهرية للعمليات التجارية مع تقارير — انظر [الكتالوج](../../autonomous_growth/product_catalog.py).
- **مدخل مجاني:** Free Diagnostic (0).

> لا تُسعّر خارج هذه الأرقام. الحساسية الصحية تُبرز حوكمة Dealix — استخدمها كنقطة ثقة لا كادعاء.

---

## 6. زاوية الرسالة / Message angle

**عربي:** «استفسارات منظّمة وعلاقات إحالة مرتّبة — بخصوصية أولاً». الرسالة تركّز على الانضباط والخصوصية: نرتّب الاستفسارات والإحالات التجارية، لا نلمس بيانات المرضى، وكل رسالة مسودة لموافقتكم.

**English:** "Organized inquiries and referral relationships — privacy first." The angle: discipline and privacy. We organize commercial inquiries and referrals, never touch patient data, and every message is a draft for your approval.

---

## 7. اعتراضات متوقعة / Expected objections (+ safe responses)

| الاعتراض | رد آمن (لا ضمانات) |
|---|---|
| «بيانات مرضانا حساسة» | «لا نتعامل مع بيانات سريرية إطلاقاً — فقط استفسارات تجارية وعلاقات إحالة، تحت DPA.» |
| «هل تضمنون حجوزات؟» | «لا نضمن أرقاماً. نرتّب الاستفسارات ونحدد 3 فرص، مسودات لموافقتكم.» |
| «الاستقبال يتابع أصلاً» | «الـ Sprint يعطي الاستقبال أولوية واضحة ومسودات جاهزة بدل التخمين.» |
| «نخاف على سمعتنا من رسائل عشوائية» | «لا إرسال آلي ولا بارد. كل رسالة تعتمدونها بأنفسكم قبل أي تواصل.» |

---

## 8. الدليل المطلوب / Proof required (L0–L5)

- **أول لمسة:** PDPL + DPA outline + تموضع (طبقة 1–2) — **L0/L1**، عيّنات فقط. الامتثال أولاً (انظر [Proof Stack](../commercial/operations/PROOF_STACK_ORDER_AR.md)).
- **بعد رد إيجابي:** عيّنة Proof Pack بلا بيانات — **L1**.
- **بعد التسليم:** `diagnostic_delivered` = **L1**؛ موافقة مسودة = **L2**.
- **حالة نجاح:** لا أرقام حجوزات منسوبة قبل **L4/L5** بموافقة موقّعة.

---

## 9. أول workflow للتنفيذ / First workflow to run

1. تأهيل + تأكيد أن النطاق **بيانات تجارية فقط**. — Qualify; confirm commercial-data-only scope.
2. اتفاق Sprint (499) بنطاق مكتوب وDPA. — Agree the 499 Sprint with a written scope and DPA.
3. استلام تصدير استفسارات/جهات إحالة (بلا حقول سريرية). — Receive inquiry/referral export (no clinical fields).
4. ترتيب الاستفسارات + تحديد فرص الإحالة B2B. — Rank inquiries, surface B2B referral opportunities.
5. توليد **مسودات** متابعة محترمة (لا إرسال). — Generate respectful follow-up DRAFTS.
6. تسليم + تسجيل `diagnostic_delivered`. — Deliver and log.

---

## 10. رسائل عربية جاهزة / Ready Arabic messages (مسودات فقط)

**أول تواصل:**
«مساء الخير [الاسم]. كثير من العيادات تستقبل استفسارات حجز جيدة لكنها تبرد قبل تأكيد الموعد، وعلاقات الإحالة (تأمين/شركات) غير مرتّبة. نعمل على ترتيب الاستفسارات التجارية وتحديد 3 فرص إحالة قابلة للتطبيق — بدون أي تعامل مع بيانات المرضى، وتحت اتفاقية حماية بيانات. 499 ريال. تستحق 15 دقيقة؟»

**متابعة 1:**
«[الاسم]، متابعة سريعة. أقدر أرسل مثال ترتيب أولوية (بدون أي بيانات) تشوف الشكل والحدود. تناسبك مكالمة قصيرة؟»

**متابعة 2:**
«[الاسم]، باختصار: نرتّب استفساراتكم التجارية وعلاقات الإحالة، 499 ريال، مسودات لموافقتكم بلا إرسال خارجي ولا بيانات سريرية. أرد متى ما ناسبك.»

**الإغلاق (Breakup):**
«[الاسم]، ما أبي أزعجك. أغلق الموضوع وأبقى متاحاً لو حبيتم ترتيب الاستفسارات وعلاقات الإحالة لاحقاً. شكراً ووفقكم الله.»

---

## 11. رسائل إنجليزية جاهزة / Ready English messages (DRAFTS only)

**First touch:**
"Hi [Name]. Many clinics receive solid booking inquiries that cool before the appointment is confirmed, while referral relationships (insurers/corporates) stay unorganized. We organize the commercial inquiries and surface 3 actionable referral opportunities — with no handling of patient data, under a data-protection agreement. 499 SAR. Worth 15 minutes?"

**Follow-up 1:**
"[Name], quick nudge. I can share a sample priority ranking (no data at all) so you see the format and the boundaries. Would a short call work?"

**Follow-up 2:**
"[Name], in short: we organize your commercial inquiries and referral relationships — 499 SAR, drafts for your approval, no external send and no clinical data. Reply whenever suits."

**Breakup:**
"[Name], I won't intrude. I'll close this and stay available if organizing inquiries and referral relationships becomes useful later. Thank you, and best wishes."

---

## 12. أسئلة discovery / Discovery questions

1. ما الخدمات الاختيارية الأعلى أولوية لديكم؟ — Which elective services are top priority?
2. من أين تأتي الاستفسارات، وأين تُسجَّل؟ — Where do inquiries come from and where are they logged?
3. ما علاقات الإحالة الحالية (تأمين/شركات/عيادات)؟ — What referral relationships exist today?
4. من يتابع الاستفسار حالياً، وما متوسط زمن الرد؟ — Who follows up, and what's the typical response time?
5. ما الحقول التي **لا** يمكن مشاركتها (نتأكد من الحدود)؟ — Which fields cannot be shared (we confirm boundaries)?
6. من سيستخدم قائمة الأولوية بعد التسليم؟ — Who will use the priority list afterward?

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
