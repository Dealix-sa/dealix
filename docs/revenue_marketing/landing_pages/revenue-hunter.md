## Revenue Hunter Pilot — صفحة الهبوط

**Path:** `/dealix-revenue-hunter`  
**Audience:** B2B Saudi/MENA SMEs (10–200 employees)  
**Offer ID:** `revenue_hunter_pilot`  
**Starting price:** 999 SAR

---

### نسخة عربية (الأساس)

#### العنوان الرئيس

> "Revenue Hunter Pilot — 10 فرص محكومة، خلال 7 أيام، بـ 999 ريالاً."

#### الألم

فرق B2B السعودية تخسر أسبوعاً كاملاً كل شهر في بحث يدوي عن الفرص: مصادر متفرّقة، أولويات مزاجية، وسجلّات مفقودة. النتيجة: قمع متعب، توقّعات مكسورة، وفريق يحرق وقته.

#### الوعد

نسلّمك 10 فرص محكومة خلال 7 أيام عمل. كل فرصة لها سبب، إشارة سوق، درجة ملاءمة، وسجل أدلة. تستطيع شرحها لمدير الإيراد بثقة، بدون "AI قال". لا أرقام مضمونة — فرص مُثبتة بأدلة.

#### لمن هذا العرض؟

- شركات B2B بين 10 و 200 موظف.
- فرق مبيعات تبحث عن فرص بشكل يدوي اليوم.
- مؤسسون يريدون اختبار ديلكس قبل الالتزام بعقد شهري.
- وكالات تختبر الكيت قبل برنامج White-label.

#### المخرجات

- قائمة 10 فرص محكومة بصيغة Notion + CSV.
- لكل فرصة: ملف العميل، الإشارة، الألم المُفترض، نص رسالة افتتاح (مسوّدة).
- درجة ملاءمة من 0 إلى 100 + شرح مبسّط للدرجة.
- سجل أدلة قابل للتدقيق لكل قرار.
- مكالمة تسليم 45 دقيقة مع المؤسس.

#### كيف يعمل؟

1. **اليوم 1:** تدفع 999 ريالاً عبر Moyasar وتملأ نموذج النطاق (15 سؤالاً).
2. **اليوم 2–5:** نطبّق مصفوفة التسجيل (راجع `dealix/revenue_marketing/scoring.py`)، نُخرج 30 مرشّحاً، نصفّيهم يدوياً إلى 10.
3. **اليوم 6:** مراجعة داخلية للحوكمة وسجل الأدلة.
4. **اليوم 7:** تسليم القائمة + مكالمة 45 دقيقة + خيار الانتقال إلى Monthly Revenue Command.

#### الدليل (placeholder)

> "{{tenant_case_count}} باي‌لوت سابق، {{evidenced_opportunities_count}} فرصة مُسلَّمة، {{conversion_rate_pct}}% منها وصلت لمرحلة تفاوض خلال 30 يوماً."

(الأرقام تُملأ من لوحة التحكم بعد كل 10 باي‌لوت. الإصدار الحالي لا يحمل أرقاماً حتى نراكم بيانات كافية.)

#### السعر الابتدائي

**999 ريالاً سعودياً** — دفعة واحدة، تشمل الـ 10 فرص ومكالمة التسليم. لا اشتراك، لا تجديد تلقائي.

#### CTA الرئيسي

> **"ابدأ الباي‌لوت — 999 ريالاً"** → `/checkout/revenue-hunter-pilot`

#### أسئلة شائعة

1. **هل تستخدمون scraping؟** لا. نعتمد على إشارات معلنة + بيانات يقدّمها العميل + تكامل CRM إن وجد. كل مصدر موثَّق.
2. **ماذا لو لم تصل أي فرصة لمرحلة تفاوض؟** نعيد التشخيص مجاناً مرة واحدة بناء على تعديل النطاق.
3. **هل ترسلون الرسائل نيابة عنا؟** لا. نسلّم مسوّدات. الإرسال يبقى بيدك، بمراجعة بشرية.
4. **هل تخزّنون بيانات عملائنا؟** نعم، داخل بيئة tenant مخصّصة بسجل أدلة. نحذف عند الطلب وفق `docs/14_trust_os/`.

#### ملاحظة الثقة

كل قرار داخل Revenue Hunter Pilot يمرّ بسجل أدلة وموافقات. لا أتمتة إرسال خارجي بدون موافقة المؤسس. لا scraping، لا قوائم WhatsApp جاهزة، لا أتمتة LinkedIn. القيمة التقديرية ليست قيمة مُتحقَّقة.

---

### English Version (parallel)

#### Headline

> "Revenue Hunter Pilot — 10 governed opportunities, in 7 days, for 999 SAR."

#### Pain

Saudi B2B teams lose a full week each month on manual opportunity hunting: scattered sources, mood-based priorities, missing logs. The result: a tired funnel, broken forecasts, and a team burning hours.

#### Promise

We deliver 10 governed opportunities within 7 business days. Each carries a reason, a market signal, a fit score, and an evidence ledger entry. You can defend it to your revenue leader confidently — not "AI said so" but a documented chain. No guaranteed numbers — evidenced opportunities.

#### Who It's For

- B2B companies, 10–200 employees.
- Sales teams hunting opportunities manually today.
- Founders trialing Dealix before a monthly commitment.
- Agencies testing the kit before a White-label program.

#### Deliverables

- 10 governed opportunities in Notion + CSV.
- Per opportunity: customer profile, signal, assumed pain, opening-message draft.
- Fit score 0–100 + plain-language score explanation.
- Auditable evidence ledger per decision.
- 45-minute handover call with the founder.

#### How It Works

1. **Day 1:** You pay 999 SAR via Moyasar and complete a 15-question scope form.
2. **Days 2–5:** We apply the scoring matrix (see `dealix/revenue_marketing/scoring.py`), surface 30 candidates, manually filter to 10.
3. **Day 6:** Internal governance and evidence-ledger review.
4. **Day 7:** Delivery of the list + 45-minute call + option to step up to Monthly Revenue Command.

#### Proof (placeholder)

> "{{tenant_case_count}} prior pilots, {{evidenced_opportunities_count}} opportunities delivered, {{conversion_rate_pct}}% reached negotiation within 30 days."

(Figures populate from the dashboard after every 10 pilots. The current release carries no numbers until enough data accumulates.)

#### Starting Price

**999 SAR** — one-time, includes the 10 opportunities and the handover call. No subscription, no auto-renewal.

#### Primary CTA

> **"Start the pilot — 999 SAR"** → `/checkout/revenue-hunter-pilot`

#### FAQ

1. **Do you scrape?** No. We rely on public signals + customer-provided data + CRM integration if available. Every source is logged.
2. **What if no opportunity reaches negotiation?** We re-run the diagnostic once at no cost based on a scope revision.
3. **Do you send messages on our behalf?** No. We hand off drafts. Sending stays with you, under human review.
4. **Do you store our customer data?** Yes, inside a dedicated tenant with an evidence ledger. We delete on request per `docs/14_trust_os/`.

#### Trust Note

Every decision inside Revenue Hunter Pilot passes an evidence ledger and approvals. No external send automation without founder approval. No scraping, no ready-made WhatsApp lists, no LinkedIn automation.

---

**Disclosure / إفصاح:** Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

Cross-links: `docs/revenue_marketing/offers_ladder.md`, `docs/revenue_marketing/message_variants.md`, `docs/revenue_marketing/outreach_playbook.md`, `docs/14_trust_os/`.
