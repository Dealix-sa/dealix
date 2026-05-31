# Post 06 — PDPL lawful basis for B2B outreach · الأساس القانوني لـ PDPL في الـ outreach B2B

**Cluster:** Technical Proof
**Best day:** Tuesday 09:00 KSA
**Expected length:** AR 750 words · EN 550 words

---

## Arabic

نظام حماية البيانات الشخصية السعودي (PDPL) دخل حيز التنفيذ الكامل في
سبتمبر ٢٠٢٤. مع ذلك، تواصلت مع ٢٠ شركة B2B في آخر شهرين، ١٤ منها لا
تستطيع شرح "ما هو الـ lawful basis لرسالة outreach الأخيرة التي
أرسلتموها؟"

هذه نقطة ضعف خطيرة لسببين:
- العقوبات في PDPL تصل إلى ٥ مليون ر.س لكل مخالفة.
- الـ enforcement بدأ فعلًا — وثقت SDAIA حالات في Q4 ٢٠٢٤.

**ما هي الـ lawful bases المعتمدة في PDPL لـ B2B outreach؟**

١. **Legitimate interest** — الأكثر شيوعًا، يغطي معظم الحالات.
   الشرط: balancing test موثق بين مصلحة المعالج وحقوق الـ data
   subject.

٢. **Consent** — للحالات الحساسة (consumers، minors، بيانات صحية أو
   مالية). شرطه: granular، documented، withdrawable.

٣. **Contractual necessity** — لو الـ outreach مرتبط بعقد قائم.

٤. **Legal obligation** — نادر في B2B outreach.

٥. **Public interest** — نادر.

٦. **Vital interest** — لا ينطبق على outreach.

**الـ B2B vs B2C — فرق جوهري:**

في B2C، الـ consent هو القاعدة. في B2B السعودي تحت PDPL، الـ
legitimate interest غالبًا كافية إذا:

- الـ data subject في موقع وظيفي مرتبط بـ purchasing decisions
- المراسلة على business email/phone (لا personal)
- الـ message له صلة واضحة بـ professional role
- تم تسجيل suppression mechanism (opt-out)
- balancing test موثق وتمت مراجعته

**ما الذي يجب توثيقه لكل lead:**

- Source: من أين جاءت بيانات الـ contact (event، referral، public
  business directory، etc.)
- Capture date + time
- Lawful basis claim + justification (≤ ٢٠٠ حرف)
- Suppression status (active/opted_out/never_contacted)
- Channel preference (email-only/whatsapp-warm/none)

**هذا ما بنيناه في Dealix كـ "Source Passport":**

كل lead يدخل النظام يحمل source_passport يجاوب على هذه الأسئلة قبل
أي رسالة خارجية. لو الـ passport ناقص، الـ agent يرفض إنتاج draft.
الـ compliance_gate يكسر pipeline بصمت لو الأساس القانوني غير
موثق.

**ماذا تفعل لو شركتك ليس عندها هذا التوثيق اليوم؟**

١. **توقف عن الـ outreach التلقائي فورًا** — كل رسالة بدون lawful
   basis = exposure مالي محتمل.

٢. **اعمل audit للـ CRM الحالي** — كم % من الـ leads يحمل source
   مسجل؟ غالبًا أقل من ٣٠٪.

٣. **ضع suppression list** — كل من طلب opt-out يدخل قائمة محترمة
   عبر كل channels.

٤. **وثّق balancing test** لكل category من الـ outreach (sales،
   marketing، event invites). نموذج جاهز:
   `docs/registers/compliance_saudi.yaml#balancing_test_templates`.

٥. **عيّن DPO** لو شركتك تعالج بيانات > ٥٠٠٠ data subject سعودي. هذا
   مطلب صريح من PDPL لشركات الحجم المتوسط/الكبير.

**النقطة النهائية:** PDPL ليست عقبة تنظيمية — هي **filter جودة**. الشركات
التي توثق lawful basis بشكل صحيح تجد أن جودة الـ pipeline تتحسن
لأنها تركز على الـ leads المستحقة. الـ outreach العشوائي يقل
لكن الـ conversion rate يرتفع.

---

## English

Saudi Personal Data Protection Law (PDPL) entered full enforcement
September 2024. Yet of 20 B2B companies I've spoken with in the
last 2 months, 14 cannot explain "what was the lawful basis for the
last outreach message you sent?"

This is a serious gap for two reasons:
- PDPL penalties reach 5 million SAR per violation.
- Enforcement has begun — SDAIA documented Q4 2024 cases.

**Approved lawful bases under PDPL for B2B outreach:**

1. **Legitimate interest** — most common, covers most cases.
   Requires: documented balancing test between controller interest
   and data subject rights.

2. **Consent** — for sensitive cases (consumers, minors, health or
   financial data). Must be granular, documented, withdrawable.

3. **Contractual necessity** — if outreach ties to an existing
   contract.

4-6. Legal obligation / public interest / vital interest — rare
in B2B outreach.

**B2B vs B2C — critical distinction:**

In B2C, consent is the default. In Saudi B2B under PDPL,
legitimate interest is usually sufficient if:

- The data subject holds a role connected to purchasing decisions
- Contact is via business email/phone (not personal)
- The message has clear connection to professional role
- Suppression mechanism (opt-out) is logged
- A balancing test is documented and reviewed

**Documentation required per lead:**

- Source: where the contact data came from (event, referral, public
  business directory, etc.)
- Capture date + time
- Lawful basis claim + justification (≤ 200 chars)
- Suppression status (active/opted_out/never_contacted)
- Channel preference (email-only/whatsapp-warm/none)

**Dealix builds this as a "Source Passport":**

Every lead enters the system with a source_passport answering
these questions BEFORE any outbound message. If the passport is
incomplete, the agent refuses to produce a draft. The
compliance_gate breaks the pipeline silently if lawful basis is
undocumented.

**What to do if your company lacks this today:**

1. **Stop autonomous outreach immediately** — every message without
   lawful basis = potential financial exposure.
2. **Audit your current CRM** — what % of leads has a recorded
   source? Usually under 30%.
3. **Build a suppression list** — every opt-out request honored
   across all channels.
4. **Document a balancing test** per outreach category (sales,
   marketing, event invites). Template:
   `docs/registers/compliance_saudi.yaml#balancing_test_templates`.
5. **Appoint a DPO** if your company processes > 5,000 Saudi data
   subjects. This is an explicit PDPL requirement.

**Bottom line:** PDPL isn't a regulatory hurdle — it's a quality
filter. Companies that correctly document lawful basis find their
pipeline quality improves because they focus on leads that deserve
it. Random outreach decreases; conversion rate rises.

---

## CTA options

- AR: "نشرح Source Passport في Dealix لو شركتك تحتاج جاهزية PDPL.
  DM."
- EN: "Happy to walk through the Source Passport in Dealix for PDPL
  readiness. DM."
