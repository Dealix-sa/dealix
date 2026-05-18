# Dealix — Product Roadmap Q2-Q4 2026

**ما هو Dealix:** نظام تشغيل الإيرادات بعد وصول الـ lead والعمليات المُدارة بحوكمة — رادار متابعة قائم على الموافقة، يعمل بمبدأ المسودّة فقط. يُظهر أي عميل يحتاج رداً، ويجهّز مسودّة الرسالة التالية؛ الإنسان يراجع ويوافق ويرسل.

**مبدأ البناء:** Ship ← Measure ← Iterate (أسبوعياً)
**فلسفة التركيز:** ميزات تخدم الإيراد أولاً.
**القيد:** لا feature بدون customer request موثّق (3+ طلبات).

> **حدود ثابتة في كل المراحل:** لا رد آلي، لا حجز آلي، لا إرسال آلي، لا تأهيل BANT آلي. أي مخرَج للعميل الخارجي يمرّ بمراجعة وموافقة بشرية.

---

## رؤية المنتج

**في Q4 2026، Dealix يكون:**
- رادار المتابعة الأدق في اللهجة الخليجية لمسودّات الردود.
- متكامل مع عدد من أدوات المبيعات/الـ CRM.
- يخدم عدداً متنامياً من الشركات السعودية/الخليجية.
- مرجعاً في فئة "نظام تشغيل الإيرادات بعد الـ lead للسوق العربي".

---

## Q2 2026 (مايو - يوليو) — "Foundation + First Revenue"

### الأولويات:
1. **Launch Production** — الانتقال من beta لـ production
2. **First 20 customers** — stress test الـ product
3. **Core integrations** — HubSpot + Zoho + WhatsApp

### Features (Q2)

#### مايو — Stabilization
- [x] Backend production على Railway
- [x] Moyasar payment flow
- [ ] Customer admin dashboard (basic)
- [ ] Email notifications للـ new leads
- [ ] Weekly report automation
- [ ] Customer onboarding flow

#### يونيو — Integrations v1
- [ ] HubSpot integration (read/write contacts)
- [ ] Zoho CRM integration
- [ ] Google Calendar — اقتراح مواعيد كمسودّة للموافقة (لا حجز آلي)
- [ ] WhatsApp Business API — مسودّات صادرة بانتظار موافقة المرسِل (لا إرسال آلي)

#### يوليو — Polish
- [ ] Analytics dashboard للعملاء (conversion funnel)
- [ ] إطار اختبار A/B لقوالب المسودّات
- [ ] Multi-language support (عربي + انجليزي hybrid)
- [ ] Role-based access (admin/user/viewer)
- [ ] API للعملاء (BYO use cases)

### Q2 Milestones (مستهدفات تقديرية)
- أول مجموعة عملاء مدفوعين عبر Revenue Proof Sprint.
- استقرار تشغيلي بلا انقطاعات حرجة.
- مؤشر رضا عملاء إيجابي.

---

## Q3 2026 (أغسطس - أكتوبر) — "Growth + Polish"

### الأولويات:
1. **Inbound engine** — content + SEO
2. **Self-serve signup** — لا founder touch
3. **Retention features** — prevent churn

### Features (Q3)

#### أغسطس — Self-Serve
- [ ] Public signup (dealix.me/signup)
- [ ] مسار الدخول عبر Free Mini Diagnostic
- [ ] In-app onboarding tutorial
- [ ] Self-service integrations (no code)
- [ ] Template library (قوالب مسودّات حسب القطاع)

#### سبتمبر — Advanced Drafting
- [ ] Sentiment analysis (تمييز إن كان العميل منزعجاً) — كإشارة للمراجِع
- [ ] Multi-turn reasoning لمسودّات السيناريوهات المعقّدة
- [ ] صياغة المسودّات بنبرة قابلة للضبط (رسمية/ودّية حسب العلامة)
- [ ] Memory per lead (سياق المحادثات السابقة)

#### أكتوبر — Retention
- [ ] Health score (مؤشر مبكّر لاحتمال التسرّب)
- [ ] Success manager workflows (متابعات استباقية)
- [ ] Usage alerts (تنبيهات انخفاض النشاط)
- [ ] Expansion prompts (فرص توسّع مُثبتة بأدلة)
- [ ] إطلاق برنامج الإحالات

### Q3 Milestones (مستهدفات تقديرية)
- نمو قاعدة العملاء.
- نسبة معتبرة من التسجيلات عبر المسار الذاتي.
- تدفّق inbound عضوي يتجاوز الاكتساب المدفوع.

---

## Q4 2026 (نوفمبر - يناير 2027) — "Scale + Expansion"

### الأولويات:
1. **Geographic expansion** — UAE
2. **Enterprise features** — F500 ready
3. **Fundraise** — Seed round closing

### Features (Q4)

#### نوفمبر — Enterprise
- [ ] SSO (SAML, Google, Microsoft)
- [ ] Role hierarchy (multi-team orgs)
- [ ] Audit logs
- [ ] Custom domain (app.yourcompany.com)
- [ ] White-label option (مرتبط بـ Agency Partner OS بعد 3 حزم إثبات)
- [ ] التزامات SLA تشغيلية موثّقة

#### ديسمبر — UAE Launch
- [ ] Arabic dialect UAE tuning
- [ ] Telr/PayTabs integration (UAE payments)
- [ ] UAE-specific onboarding content
- [ ] Partnership with 1 UAE VC/accelerator
- [ ] Case studies from UAE

#### يناير 2027 — Intelligence Layer
- [ ] Lead prioritization signals (إشارات ترتيب أولوية المتابعة)
- [ ] Conversation insights (ما الذي ينجح وما لا ينجح)
- [ ] Industry benchmarks (مقارنة مجمّعة)
- [ ] Predictive pipeline (توقّع تقديري للربع القادم)
- [ ] تحسين القوالب بناءً على نتائج المراجعة البشرية

### Q4 Milestones (مستهدفات تقديرية)
- توسّع قاعدة العملاء داخل السعودية مع أول عملاء في الإمارات.
- إغلاق جولة تمويل أولية.

---

## 🚫 ما نُؤجّله (Not Now)

لضمان التركيز، هذه الأشياء **ممنوعة** قبل Y2:

- ❌ Mobile app (web-only)
- ❌ Voice-only interface (chat/WhatsApp كافٍ)
- ❌ Video AI (غير ضروري للـ B2B sales)
- ❌ Custom ML models (Claude كافٍ)
- ❌ On-premise deployment (SaaS only)
- ❌ Support for English-only customers
- ❌ Free tier (premium positioning)

---

## 📊 Framework للقرارات

### قبل أي feature جديد، اسأل:

1. **Revenue Impact:** هل يجلب عملاء جدد أو يحتفظ بحاليين؟
2. **Frequency:** كم عميل طلبه؟ (minimum 3)
3. **Effort:** هل ينجز في < 2 أسابيع؟
4. **Opportunity Cost:** ما الذي لن نفعله بدلاً؟
5. **Competitive:** هل يُميّزنا أم يلحق بالمنافس؟

### Scoring:
- Revenue impact (40%)
- Customer requests (25%)
- Dev effort inverse (20%)
- Strategic differentiation (15%)

**Minimum score: 7/10 to ship**

---

## 🔄 Release Cadence

### Weekly (كل ثلاثاء):
- Bug fixes
- Minor improvements
- A/B test results applied

### Monthly:
- 1 major feature launch
- Customer newsletter مع updates
- Webinar demo لعملاء حاليين

### Quarterly:
- Roadmap review مع team
- Customer advisory board meeting
- Retrospective + planning

---

## 📈 تتبع التقدم

### OKRs لكل quarter

**Q2 OKRs (مثال):**
- **O:** Launch Dealix للإنتاج بنجاح
  - **KR1:** أول مجموعة عملاء مدفوعين (Free Mini Diagnostic ← Revenue Proof Sprint ← Growth Ops Monthly)
  - **KR2:** استقرار تشغيلي عالٍ بلا انقطاعات حرجة
  - **KR3:** 3 integrations live
  - **KR4:** مؤشر رضا عملاء إيجابي

**تحديث أسبوعي، مراجعة شهرية، retrospective quarterly.**

---

## 🧪 Experiments Queue

### Pending tests (نجربها بعد MVP):

1. **Diagnostic-to-Sprint conversion:** صياغات مختلفة لعرض Revenue Proof Sprint (499 ريال)
2. **Onboarding video:** مع vs بدون
3. **عمق المسودّة:** ملخّص مختصر vs ملخّص موسّع لكل lead
4. **توقيت اقتراح المتابعة:** فوري vs مع تأخير قصير
5. **شكل المراجعة:** مسودّة واحدة vs بدائل متعددة للموافقة
6. **Language mix:** عربي فقط vs ثنائي
7. **قوالب المسودّات:** نبرة رسمية vs ودّية حسب القطاع

كل experiment: 2 أسابيع، عيّنة كافية، إما ship أو kill.

---

## 🎨 UX Principles

كل feature يُبنى على هذه المبادئ:

1. **Arabic-first:** الـ UI عربي افتراضي، RTL صحيح
2. **3-click rule:** أي action أساسي في < 3 clicks
3. **No jargon:** لغة بسيطة، ليست تقنية
4. **Mobile-responsive:** يشتغل على جوال الـ CEO
5. **Empty states:** كل شاشة بلا بيانات = tutorial
6. **Error messages:** مفيدة، ليست "Error 500"
7. **Feedback loops:** كل action يعطي confirmation
8. **Undo-able:** كل destructive action قابل للتراجع

---

## 🏗️ Technical Debt Backlog

نعترف بها، نعالجها بذكاء:

### High priority:
- [ ] Refactor conversation memory (scalability)
- [ ] Improve test coverage (currently 70%, target 90%)
- [ ] API rate limiting per customer

### Medium:
- [ ] Migrate من Postgres لـ Postgres + Redis للـ caching
- [ ] Add observability (distributed tracing)
- [ ] Refactor email templates (maintainability)

### Low:
- [ ] Migrate to Python 3.13 (when stable)
- [ ] Evaluate serverless for specific endpoints

**قاعدة:** 20% من كل sprint لـ tech debt.

---

## 🤝 الشراكات المستهدفة

### Q2-Q3:
- **Salla App Store** — Dealix كـ app في منصتهم
- **Zid** — مشابه
- **STC Business** — bundle في عروضهم للـ SMBs
- **Misk Academy** — تدريب founders

### Q4:
- **SDAIA** — certification حكومية
- **Monshaat** — subsidized pricing للـ startups
- **Y Combinator Alumni Saudi** — warm intros

---

## 💬 Customer Feedback Channels

- **In-app:** Intercom-style chat widget
- **Monthly:** 1:1 call مع كل عميل Growth+
- **Weekly:** Async Slack/WhatsApp
- **Quarterly:** NPS survey
- **Annual:** Customer Advisory Board (top 5 accounts)

**كل feedback → Notion database → priority review weekly.**

---

## 🎯 نقاط التحقق النجاح

### Q2 end:
- [ ] أول مجموعة عملاء مدفوعين
- [ ] الرادار يُظهر leads المتابعة ويجهّز المسودّة خلال زمن قصير من الإشارة
- [ ] لا انقطاعات تشغيلية تتجاوز 5 دقائق
- [ ] 3+ حزم إثبات (proof packs) — case-safe ما لم يوافق العميل على الذكر بالاسم

### Q3 end:
- [ ] نمو قاعدة العملاء
- [ ] نسبة معتبرة من التسجيلات ذاتية الخدمة
- [ ] inbound عضوي يتجاوز الاكتساب المدفوع
- [ ] دقّة قابلة للقياس في اللهجة الخليجية لمسودّات الردود

### Q4 end:
- [ ] توسّع قاعدة العملاء داخل السعودية
- [ ] أول عملاء في سوق الإمارات
- [ ] إغلاق جولة تمويل أولية
- [ ] فريق 5-7 أشخاص

---

## 🚀 Long-term Vision (2027-2030)

**2027:** $24M ARR، 500 عملاء، 3 أسواق (KSA, UAE, Kuwait)
**2028:** $60M ARR، 1,200 عملاء، 5 أسواق، Voice AI
**2029:** $120M ARR، 2,500 عملاء، الخليج كامل، AI-native
**2030:** $300M ARR، الرائد في MENA للـ sales automation

**Exit options (2030+):**
- IPO على Saudi Exchange (Tadawul)
- Acquisition من Salesforce / HubSpot / Local tech giant
- Continue as independent profitable business

---

## 📝 Roadmap Review Cadence

- **Weekly (الاثنين):** progress check
- **Monthly (آخر أسبوع):** adjust priorities
- **Quarterly:** major revision + customer advisory input
- **Annual:** strategic re-planning

---

**اكتمال هذا الـ roadmap = خارطة طريق واضحة. الحين نحتاج نمشي عليها.**

ابدأ بـ Q2 بأولوية واحدة فقط: **Launch Production.**
