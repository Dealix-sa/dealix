# دليل قطاع — مجموعات المطاعم — Restaurant Groups Playbook

> دليل تشغيلي داخلي. التركيز على **الإيراد التجاري B2B** خلف الواجهة (تموين، امتياز/فرنشايز، عقود موردين/شركات، فعاليات)، لا الزبون الفردي اليومي. كل الرسائل **مسودات** ترسَل يدوياً. لا إرسال آلي، لا قوائم مشتراة، لا ضمانات.
> Internal operating playbook. Focus on the B2B commercial revenue behind the storefront (catering, franchise, supplier/corporate contracts, events), not the daily walk-in customer. Every message is a DRAFT sent manually. No auto-send, no purchased lists, no guarantees.
>
> المرجع: [README القطاعات](README.md) · [حزم RevOps](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · [الكتالوج](../../autonomous_growth/product_catalog.py)

---

## 1. الألم الرئيسي / Core pain

**عربي:** مجموعة المطاعم تستقبل طلبات تجارية متفرقة (تموين فعاليات، عقود شركات، استفسارات امتياز، عروض موردين) عبر قنوات مختلفة، لكنها تُعامَل كرسائل عابرة لا كخط فرص. لا أحد يتتبّع طلب تموين بقيمة عالية أو مستثمر امتياز جاد. النتيجة: عقود B2B متكررة وقيّمة تضيع بين ازدحام التشغيل اليومي.

**English:** A restaurant group receives scattered commercial requests (event catering, corporate contracts, franchise inquiries, supplier offers) across channels, but treats them as one-off messages, not an opportunity pipeline. Nobody tracks a high-value catering request or a serious franchise investor. Result: valuable, recurring B2B contracts are lost amid daily operations.

---

## 2. صاحب القرار / Decision maker

- **الأساسي:** المالك / الرئيس التنفيذي للمجموعة أو مدير التطوير. — Group owner/CEO or development director.
- **المؤثّر:** مدير التموين والمبيعات المؤسسية. — Catering and corporate-sales manager.
- **في الامتياز:** مسؤول تطوير الامتياز. — Franchise development lead.

---

## 3. مؤشرات أن العميل مناسب / Good-fit signals

- مجموعة بعدة فروع/علامات وطموح B2B. — Multi-branch/brand group with B2B ambition.
- خط تموين/فعاليات أو برنامج امتياز قائم. — Active catering/events line or franchise program.
- استفسارات تجارية متكررة بلا تتبّع. — Recurring commercial inquiries, untracked.
- يقول «نستقبل طلبات تموين بس ما نلحق عليها». — "We get catering requests but can't keep up."

---

## 4. مؤشرات أنه غير مناسب / Disqualifiers

- مطعم واحد بلا أي خط B2B. — Single outlet with no B2B line.
- يريد أتمتة تسويق للزبون الفردي أو رسائل بريد جماعي باردة — خارج النطاق. — Wants consumer marketing automation or cold blasts — out of scope.
- يطلب ضمان عدد عقود تموين. — Wants a guaranteed catering-contract count.
- لا بيانات استفسارات ولا نية لجمعها مشروعاً. — No inquiry data and no lawful intent to gather it.

---

## 5. أول منتج نبيعه / First product to sell

**Revenue Intelligence Sprint — 499 ريال** (سبرينت ذكاء الإيرادات).
المصدر: [`product_catalog.py`](../../autonomous_growth/product_catalog.py).

- **لماذا:** عتبة منخفضة لإثبات القيمة على **خط الفرص التجاري** (تموين/شركات/امتياز): ترتيب الطلبات حسب القيمة و3 فرص قابلة للتطبيق — قبل أي التزام أكبر.
- **بديل أعلى عند الجاهزية (عدة فروع/علامات):** Managed Ops (2,999–4,999/شهر) لإدارة شهرية لخط الفرص التجاري مع تقارير — [الكتالوج](../../autonomous_growth/product_catalog.py).
- **مدخل مجاني:** Free Diagnostic (0).

> لا تُسعّر خارج هذه الأرقام. النطاق تجاري B2B، لا تسويق استهلاكي.

---

## 6. زاوية الرسالة / Message angle

**عربي:** «عقود التموين والامتياز خلف الزحمة». الرسالة: مطبخكم وعلامتكم يجذبان طلبات تجارية قيّمة، لكنها تضيع في التشغيل اليومي. نرتّب خط الفرص ونحدد الأعلى قيمة — لا نعد بعقود.

**English:** "Catering and franchise contracts behind the rush." The angle: your kitchen and brand attract valuable commercial requests that get lost in daily ops. We organize the opportunity pipeline and surface the highest-value ones — not a contracts promise.

---

## 7. اعتراضات متوقعة / Expected objections (+ safe responses)

| الاعتراض | رد آمن (لا ضمانات) |
|---|---|
| «نحن مطاعم، نبيع للزبون مباشرة» | «نركّز على الجانب التجاري: تموين وعقود شركات وامتياز — لا الزبون الفردي اليومي.» |
| «هل تضمنون عقوداً؟» | «لا نضمن أرقاماً. نرتّب الطلبات التجارية ونحدد 3 فرص عالية القيمة، مسودات لموافقتكم.» |
| «طلباتنا تجي وتروح» | «هذا بالضبط ما نرتّبه: نمسك الطلب القيّم قبل أن يبرد بمتابعة منظّمة.» |
| «خصوصية بيانات عملائنا» | «تحت DPA، داخلي فقط، بلا إرسال خارجي ولا تسويق جماعي.» |

---

## 8. الدليل المطلوب / Proof required (L0–L5)

- **أول لمسة:** تموضع + امتثال (طبقة 1–2) — **L0/L1**، عيّنات فقط.
- **بعد رد إيجابي:** عيّنة Proof Pack بلا بيانات — **L1**.
- **بعد التسليم:** `diagnostic_delivered` = **L1**؛ موافقة مسودة = **L2**.
- **حالة نجاح:** لا أرقام عقود منسوبة قبل **L4/L5** بموافقة موقّعة.

---

## 9. أول workflow للتنفيذ / First workflow to run

1. تأهيل + تأكيد وجود خط فرص B2B. — Qualify; confirm a B2B opportunity line.
2. اتفاق Sprint (499) بنطاق مكتوب (تموين/امتياز/شركات). — Agree the 499 Sprint scoped to B2B lines.
3. استلام تصدير الطلبات التجارية تحت DPA. — Receive commercial-request export under DPA.
4. ترتيب حسب القيمة + تحديد 3 فرص. — Rank by value, surface 3 opportunities.
5. توليد **مسودات** متابعة (لا إرسال). — Generate follow-up DRAFTS.
6. تسليم + تسجيل `diagnostic_delivered`. — Deliver and log.

---

## 10. رسائل عربية جاهزة / Ready Arabic messages (مسودات فقط)

**أول تواصل:**
«مساء الخير [الاسم]. مجموعات المطاعم تستقبل طلبات تجارية قيّمة — تموين، عقود شركات، استفسارات امتياز — لكنها غالباً تضيع في زحمة التشغيل. نرتّب خط الفرص التجاري ونحدد أعلى 3 فرص قابلة للتطبيق — 499 ريال، مخرجات داخلية فقط، تركيز على B2B لا الزبون الفردي. تستحق 15 دقيقة؟»

**متابعة 1:**
«[الاسم]، متابعة سريعة. أقدر أرسل مثال ترتيب فرص تجارية (بدون أي بيانات) تشوف الشكل. تناسبك مكالمة قصيرة؟»

**متابعة 2:**
«[الاسم]، باختصار: نمسك طلبات التموين والعقود القيّمة قبل ما تبرد، ونرتّبها، 499 ريال، مسودات لموافقتكم بلا إرسال خارجي. أرد متى ما ناسبك.»

**الإغلاق (Breakup):**
«[الاسم]، ما أبي أثقّل عليك. أغلق الموضوع وأبقى متاحاً لو حبيتم ترتيب خط الفرص التجاري لاحقاً. شكراً ووفقكم.»

---

## 11. رسائل إنجليزية جاهزة / Ready English messages (DRAFTS only)

**First touch:**
"Hi [Name]. Restaurant groups receive valuable commercial requests — catering, corporate contracts, franchise inquiries — that often get lost in the daily rush. We organize the B2B opportunity pipeline and surface the top 3 actionable opportunities — 499 SAR, internal outputs only, focused on B2B, not the walk-in customer. Worth 15 minutes?"

**Follow-up 1:**
"[Name], quick nudge. I can share a sample commercial-opportunity ranking (no data at all) so you see the format. Would a short call work?"

**Follow-up 2:**
"[Name], in short: we catch valuable catering and contract requests before they cool, and organize them — 499 SAR, drafts for your approval, no external send. Reply whenever suits."

**Breakup:**
"[Name], I won't crowd you. I'll close this and stay available if organizing the commercial pipeline becomes useful later. Thanks, and best of luck."

---

## 12. أسئلة discovery / Discovery questions

1. ما خطوط الإيراد التجارية لديكم (تموين/امتياز/شركات)؟ — Which commercial revenue lines exist (catering/franchise/corporate)?
2. كم طلباً تجارياً تستقبلون شهرياً، ومن أي قنوات؟ — Monthly commercial-request volume and channels?
3. كيف تتابعون طلب التموين القيّم اليوم؟ — How do you follow up a high-value catering request today?
4. هل لديكم برنامج امتياز نشط أو خطة له؟ — Active franchise program or a plan for one?
5. من يملك المبيعات المؤسسية في المجموعة؟ — Who owns corporate sales across the group?
6. من سيستخدم خط الفرص المرتّب؟ — Who will use the organized pipeline?

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
