# إطار استقبال العملاء المحتملين — Lead Intake Framework (Lawful Pipeline)

> **العربية أولاً · English parallel below.**
> كيف تبني خط أنابيب **حقيقيًا وقانونيًا**: تعريف ICP، تأهيل BANT-lite، ومصادر
> مشروعة فقط. **يُمنع صراحةً** الـ scraping والبيانات المُلفّقة والقوائم المشتراة.

---

## ١. العميل المثالي — ICP (AR)

**القطاع المستهدف:** خدمات B2B في المملكة العربية السعودية.

| البُعد | المعيار المثالي |
|--------|------------------|
| نوع النشاط | خدمات B2B (استشارات، تسويق، توظيف، تدريب، تقنية، توزيع، عقارات تجارية) |
| الحجم | فريق ٥–١٥٠، إيراد متكرر أو مشاريع متكررة |
| نضج البيانات | لديهم قائمة عملاء/فرص في CRM أو Excel (حتى لو غير منظمة) |
| صانع القرار | مؤسس / COO / GM / مدير مبيعات — حاضر في القرار |
| الألم | فرص تتسرّب، متابعة ضعيفة، بيانات غير مستثمرة |
| الاستعداد للحوكمة | يقبل نموذج "مسودات + موافقة بشرية"، لا يطلب أتمتة خارجية |
| الموقع | الرياض، جدة، الدمام/الخبر أولًا |

**خارج النطاق (Out of ICP):** من يطلب scraping، أو واتساب بارد جماعي، أو ضمان
صفقات، أو إرسالًا خارجيًا نيابة عنه بلا موافقة. هؤلاء يُرفضون بنظافة.

## ٢. تأهيل BANT-lite (AR)

أربعة أسئلة سريعة قبل أي عرض مدفوع:

| الحرف | السؤال | إشارة "نعم" |
|-------|--------|-------------|
| **B — Budget** | هل هناك ميزانية ولو صغيرة للتجربة (٤٩٩ ر.س فأكثر)؟ | يذكر رقمًا أو يقبل Sprint |
| **A — Authority** | هل تتحدث مع صانع القرار أو لديه وصول مباشر له؟ | مؤسس/COO/GM حاضر |
| **N — Need** | هل الألم واضح وملموس (فرص تتسرّب، بيانات مبعثرة)؟ | يصف مشكلة محددة |
| **T — Timing** | هل التوقيت الآن أم خلال ٣٠–٦٠ يومًا؟ | يحدد نافذة قريبة |

**قاعدة القرار:**
- ٤/٤ نعم → اعرض Sprint ٤٩٩ أو Command Sprint.
- ٢–٣ نعم → ابدأ بالتشخيص المجاني (diagnostic_only).
- ميزانية فقط بلا ألم/سلطة → reframe، حدّد نطاقًا أصغر.
- يطلب ممارسة محظورة → reject / refer_out.

> راجع شجرة القرار الكاملة:
> [`../docs/29_sales_os/QUALIFICATION_DECISION_TREE.md`](../docs/29_sales_os/QUALIFICATION_DECISION_TREE.md)
> وبطاقة ICP: [`../docs/29_sales_os/ICP_SCORECARD.md`](../docs/29_sales_os/ICP_SCORECARD.md).

## ٣. مصادر مشروعة — Lawful Sourcing (AR)

استخدم هذه المصادر **فقط**، وكلها بأساس تواصل مشروع:

1. **شبكة المؤسس المباشرة** — من تعرفهم فعليًا. الأقوى تحويلًا.
2. **الإحالات** — اطلب من كل عميل/معرفة اسمين. أحالك طرفٌ = أساس مشروع.
3. **الوارد من الموقع** — من ملأ نموذج التشخيص في `dealix.me/diagnostic.html` (وافق على التواصل).
4. **دلائل الغرف التجارية والجمعيات** — قوائم أعضاء منشورة علنًا لغرض التواصل المهني.
5. **بحث يدوي بأساس موافقة** — تحديد شركة مناسبة يدويًا، ثم التواصل عبر قناة عامة
   مهنية (نموذج "اتصل بنا" على موقعها، أو معرفة مشتركة)، لا عبر بيانات مستخرجة.
6. **الفعاليات والمؤتمرات** — من تبادلت معه التعريف وجهًا لوجه.

**لكل عميل محتمل سجّل `lawful_source`** في `target_segments.csv` و`pipeline_tracker.csv`.
بلا مصدر مشروع = لا تواصل.

## ٤. محظورات صريحة — Explicit Prohibitions (AR)

- ❌ **لا scraping** — لا استخراج آلي لأي بيانات اتصال من أي موقع أو منصة.
- ❌ **لا بيانات مُلفّقة** — لا أسماء شركات أو أرقام أو أشخاص مخترَعين.
- ❌ **لا قوائم مشتراة** ولا قواعد بيانات بلا أساس تواصل.
- ❌ **لا واتساب بارد جماعي** ولا رسائل لأرقام لا تملك أساس التواصل معها.
- ❌ **لا أتمتة LinkedIn** ولا أدوات تخالف شروط المنصّات.
- ❌ **لا إرسال خارجي نيابة عن العميل** بلا موافقته الصريحة.

> أساس الامتثال: نظام حماية البيانات الشخصية (PDPL). راجع
> [`../docs/ops/PDPL_RETENTION_POLICY.md`](../docs/ops/PDPL_RETENTION_POLICY.md)
> و [`../docs/29_sales_os/OBJECTION_NO_SCRAPING.md`](../docs/29_sales_os/OBJECTION_NO_SCRAPING.md).

---

## 1. ICP (EN)

**Target sector:** B2B services in the Kingdom of Saudi Arabia.

| Dimension | Ideal criterion |
|-----------|-----------------|
| Business type | B2B services (consulting, marketing, recruitment, training, tech, distribution, commercial real estate) |
| Size | Team of 5–150, recurring revenue or repeat projects |
| Data maturity | Has a client/opportunity list in a CRM or Excel (even if messy) |
| Decision maker | Founder / COO / GM / sales lead — present in the decision |
| Pain | Opportunities leaking, weak follow-up, unused data |
| Governance readiness | Accepts "drafts + human approval"; does not demand external automation |
| Location | Riyadh, Jeddah, Dammam/Khobar first |

**Out of ICP:** anyone demanding scraping, bulk cold WhatsApp, guaranteed deals,
or external sending on their behalf without consent. Decline these cleanly.

## 2. BANT-lite (EN)

Four quick questions before any paid offer:

| Letter | Question | "Yes" signal |
|--------|----------|--------------|
| **B — Budget** | Is there a budget, even small, to try (499 SAR+)? | Names a figure or accepts the Sprint |
| **A — Authority** | Are you speaking to the decision maker or someone with direct access? | Founder/COO/GM present |
| **N — Need** | Is the pain clear and concrete (leaking opportunities, scattered data)? | Describes a specific problem |
| **T — Timing** | Is the timing now or within 30–60 days? | States a near window |

**Decision rule:**
- 4/4 yes → offer the 499 Sprint or a Command Sprint.
- 2–3 yes → start with the free diagnostic (diagnostic_only).
- Budget only, no pain/authority → reframe, scope smaller.
- Requests a prohibited practice → reject / refer_out.

> Full decision tree:
> [`../docs/29_sales_os/QUALIFICATION_DECISION_TREE.md`](../docs/29_sales_os/QUALIFICATION_DECISION_TREE.md)
> and ICP scorecard: [`../docs/29_sales_os/ICP_SCORECARD.md`](../docs/29_sales_os/ICP_SCORECARD.md).

## 3. Lawful Sourcing (EN)

Use **only** these sources, each with a lawful basis to contact:

1. **Founder's direct network** — people you actually know. Highest conversion.
2. **Referrals** — ask every client/contact for two names. A warm referral is a lawful basis.
3. **Inbound from the site** — anyone who filled the diagnostic form at `dealix.me/diagnostic.html` (consented to contact).
4. **Chamber & association directories** — publicly published member lists intended for professional contact.
5. **Manual research on a consent basis** — identify a fitting company by hand, then reach out via a public professional channel (their "contact us" form, or a mutual connection), never via scraped data.
6. **Events & conferences** — people you exchanged introductions with in person.

**Record `lawful_source` for every lead** in `target_segments.csv` and `pipeline_tracker.csv`.
No lawful source = no contact.

## 4. Explicit Prohibitions (EN)

- ❌ **No scraping** — no automated extraction of any contact data from any site or platform.
- ❌ **No fabricated data** — no invented company names, numbers, or people.
- ❌ **No purchased lists** or databases without a basis to contact.
- ❌ **No bulk cold WhatsApp** and no messages to numbers you have no basis to contact.
- ❌ **No LinkedIn automation** or tools that violate platform terms.
- ❌ **No external sending on a customer's behalf** without their explicit approval.

> Compliance basis: Personal Data Protection Law (PDPL). See
> [`../docs/ops/PDPL_RETENTION_POLICY.md`](../docs/ops/PDPL_RETENTION_POLICY.md)
> and [`../docs/29_sales_os/OBJECTION_NO_SCRAPING.md`](../docs/29_sales_os/OBJECTION_NO_SCRAPING.md).

---

## روابط — Related

- بذور القطاعات (تُملأ من مصادر مشروعة): [`target_segments.csv`](target_segments.csv)
- إجراء المسوّدات اليومية: [`DAILY_DRAFTS_SOP_AR.md`](DAILY_DRAFTS_SOP_AR.md)
- حزمة المسوّدات: [`daily_drafts/SAMPLE_PACK_AR.md`](daily_drafts/SAMPLE_PACK_AR.md)
- سكربت مكالمة الاكتشاف: [`CALL_KIT_AR.md`](CALL_KIT_AR.md)
- تأهيل المبيعات: [`../docs/29_sales_os/SALES_QUALIFICATION.md`](../docs/29_sales_os/SALES_QUALIFICATION.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
