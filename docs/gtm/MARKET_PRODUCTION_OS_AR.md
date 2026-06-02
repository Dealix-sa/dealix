# Dealix Market Production OS — خريطة تشغيل السوق (طبقة GTM)

> **هذه الوثيقة طبقة تشغيل (operating map)، وليست دستوراً جديداً.**
> الدستور الوحيد الحاكم هو [`DEALIX_OPERATING_CONSTITUTION.md`](../DEALIX_OPERATING_CONSTITUTION.md).
> إذا تعارض أي سطر هنا مع الدستور، **الدستور يفوز**. مهمة هذا الملف أن يربط
> رؤية «إنتاج السوق من كل الزوايا» بالأنظمة **القائمة فعلاً** في المستودع،
> لا أن يبني نسخة موازية لها.

**Status:** Foundation (PR 1). يوحّد الرؤية مع الكود القائم. لا يخترع أسعاراً، ولا
وحدات جديدة، ولا قواعد جديدة فوق الدستور.

---

## 0. لماذا هذا الملف موجود (وماذا لا يفعل)

رؤية «Dealix = Market Production Company OS» صحيحة كنموذج ذهني — لكن **~80% منها
مبنيّ مسبقاً** في المستودع تحت أسماء أخرى (Golden Loop، 7 طبقات، 9 أنظمة، بوابات
الإرسال الآمن). لذلك:

| يفعل ✅ | لا يفعل ❌ |
|---|---|
| يربط الرؤية بالوحدات والمسارات الحقيقية | يكرّر وحدات موجودة بأسماء جديدة |
| يجيب الأسئلة العشرة التشغيلية بمسارات حقيقية | يخترع سلّم تسعير رابعاً |
| يصنّف القواعد: دستورية (ثابتة) مقابل تشغيلية | يكتب دستوراً منافساً |
| يحدّد الفجوات الحقيقية فقط للبناء القادم | يضيف 100 ملف سطحي يفاقم التشتّت |

قاعدة `AGENTS.md` الصريحة: *"Prefer fixing or clarifying existing code over adding
new features."* — هذا الملف يلتزم بها.

---

## 1. الفكرة في سطر واحد

> **«إنتاج السوق» ليس نظاماً جديداً؛ هو تشغيل [الحلقة الذهبية](../DEALIX_OPERATING_CONSTITUTION.md)
> (المادة 2) يومياً كآلة GTM، تحت [القانون الثالث](../DEALIX_OPERATING_CONSTITUTION.md)
> (ذكاء مستقل، تنفيذ بموافقة بشرية).**

الحلقة الذهبية (Article 2) هي بالضبط دورة إنتاج السوق التي وصفتها:

```
Market Signal → Target Score → Offer Match → Action → Approval
  → Diagnostic → Pilot → Delivery → Proof Event → Finance Truth
  → Weekly Executive Decisions → Better Targeting
```

«الأنظمة الاثنا عشر» في رؤيتك هي **زوايا نظر (views)** على هذه الحلقة الواحدة،
وليست اثني عشر صندوقاً مستقلاً.

---

## 2. القاعدة الحاكمة: ينتج بكثافة، يرسل بحكمة

هذه أهم قاعدة، ومصدرها الدستور لا هذا الملف:

- **القانون الثالث (Article 3, Law 3):** النظام يحلّل ويرتّب ويصيغ المسودات ويقيس
  ويتعلّم **تلقائياً**. أما **الإرسال / التحصيل / النشر / استخدام الشعار** فيتطلب
  **موافقة المؤسس الصريحة**.
- **أنماط الإجراء المسموحة فقط (Article 5):** `suggest_only` · `draft_only` ·
  `approval_required` · `approved_manual` · `blocked`. أي `auto_send` / `auto_charge`
  / `auto_dm` = **مخالفة دستورية** تُعاد فوراً.

ترجمة ذلك إلى رقمك «250»:

| البند | الحكم |
|---|---|
| **250 مسودة/يوم** | مسموح كـ `draft_only` — لا حدّ دستوري على إنتاج المسودات |
| **250 إرسالة/يوم** | **ممنوع تلقائياً.** الإرسال `approval_required` + محكوم بمنحنى تسخين |
| من يضغط «إرسال»؟ | المؤسس فقط، عبر [`approval_center`](../../auto_client_acquisition/approval_center/) |

---

## 3. الحواجز الصلبة والقواعد التشغيلية

### 3.1 الحواجز الدستورية الثمانية (لا تُقلب — Article 4)

مصدرها [الدستور](../DEALIX_OPERATING_CONSTITUTION.md) ومُنفَّذة في
[`governance_os/rules/`](../../auto_client_acquisition/governance_os/rules/):

```
NO_LIVE_SEND        NO_LIVE_CHARGE      NO_COLD_WHATSAPP    NO_LINKEDIN_AUTOMATION
NO_SCRAPING         NO_FAKE_PROOF       NO_FAKE_REVENUE     NO_UNAPPROVED_TESTIMONIAL
```

محميّة باختبارات حقيقية (تفشل الـ CI عند الخرق):
[`test_no_cold_whatsapp.py`](../../tests/test_no_cold_whatsapp.py) ·
[`test_no_linkedin_automation.py`](../../tests/test_no_linkedin_automation.py) ·
[`test_no_scraping_engine.py`](../../tests/test_no_scraping_engine.py) ·
[`test_no_guaranteed_claims.py`](../../tests/test_no_guaranteed_claims.py) ·
[`test_no_pii_in_logs.py`](../../tests/test_no_pii_in_logs.py) ·
[`test_no_source_no_answer.py`](../../tests/test_no_source_no_answer.py) ·
[`test_forbidden_actions.py`](../../tests/test_forbidden_actions.py) ·
[`test_doctrine_guardrails.py`](../../tests/test_doctrine_guardrails.py).

### 3.2 الدوكترين التشغيلي الأوسع («اللا‑تفاوضيات» الإحدى عشرة)

ملفات الوكلاء في [`.claude/agents/`](../../.claude/agents/) تشير إلى **«11 non‑negotiables»**
(لا scraping، لا cold WhatsApp، لا LinkedIn automation، لا claims غير موثّقة، لا ضمان
نتائج، لا PII في logs، لا إجابة بلا مصدر، لا إجراء خارجي بلا موافقة، لا وكيل بلا هوية،
لا مشروع بلا Proof Pack، لا مشروع بلا Capital Asset).

> ⚠️ **عدم تطابق يحتاج توحيداً:** الدستور (Article 4) يقنّن **8 حواجز ثابتة**، بينما
> الوكلاء يذكرون **11 لا‑تفاوضية**. ليست متناقضة (الـ8 حواجز تقنية ثابتة؛ الـ11 دوكترين
> تشغيلي أوسع) لكن **لا يوجد لها بيت رسمي واحد في `docs/`**. → بند قرار في §10.

### 3.3 قواعد GTM التشغيلية (طبقة فوق الحواجز، ليست حواجز جديدة)

رؤيتك تضيف قواعد تسليم بريد ضرورية. هذه **سياسة تشغيلية** (operational policy)،
لا حواجز دستورية جديدة، وتنطبق على مسار الإرسال:

```
لا قوائم مشتراة            لا subject مضلّل           لا fake Re:/Fwd:
opt-out في كل رسالة         احترام unsubscribe فوراً    suppression list محدّثة
SPF + DKIM + DMARC          bounce handling             دومين/سب‑دومين إرسال منفصل
```

مرجعها التنظيمي خارجياً (سياق فقط، ليست وعود Dealix): **CAN‑SPAM Act**، معيار
**DMARC**، ونظام حماية البيانات الشخصية السعودي **PDPL**. مُنفّذة جزئياً اليوم في
[`leadops_spine/compliance_gate.py`](../../auto_client_acquisition/leadops_spine/compliance_gate.py)
و[`email/compliance.py`](../../auto_client_acquisition/email/compliance.py)
و[`email/deliverability_check.py`](../../auto_client_acquisition/email/deliverability_check.py).

---

## 4. الخريطة الكبرى: رؤيتك ← ما هو قائم فعلاً

العمود «الحالة»: **LIVE** = كود قائم · **PARTIAL** = موجود لكن ناقص الربط ·
**GAP** = غير موجود (مرشّح للبناء).

| زاوية الرؤية (Your spec) | الموجود فعلاً | الحالة |
|---|---|---|
| Brand OS | [`docs/brand/`](../brand/) · `docs/BRAND_PRESS_KIT.md` · `frontend/.../styles/dealix-brand.css` | LIVE |
| Offer OS / التسعير | المادة 9 + [`DEALIX_REVOPS_PACKAGES_AR.md`](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · `service_catalog.py` | LIVE (تعارض تسعير — §6) |
| Sector OS | `docs/SECTOR_PLAYBOOKS.md` · [`revenue_graph/sector_playbooks.py`](../../auto_client_acquisition/revenue_graph/sector_playbooks.py) · `saudi_layer/saudi_sector_taxonomy.py` | LIVE |
| Signal OS | [`revenue_os/signal_normalizer.py`](../../auto_client_acquisition/revenue_os/signal_normalizer.py) · `market_intelligence/signal_detectors.py` · `POST /revenue-os/signals/normalize` | LIVE |
| Prospect OS | `sales_os/icp_score.py` · `agents/icp_matcher.py` · `lead_inbox.py` · `POST /api/v1/leads` | LIVE |
| Draft Factory | [`revenue_os/draft_pack.py`](../../auto_client_acquisition/revenue_os/draft_pack.py) · `leadops_spine/draft_builder.py` · `api/routers/drafts.py` | LIVE |
| Compliance Gate | [`leadops_spine/compliance_gate.py`](../../auto_client_acquisition/leadops_spine/compliance_gate.py) · `email/compliance.py` | LIVE |
| Deliverability OS | [`email/deliverability_check.py`](../../auto_client_acquisition/email/deliverability_check.py) | PARTIAL (لا منحنى تسخين/Postmaster موثّق) |
| Approval Queue | [`approval_center/`](../../auto_client_acquisition/approval_center/) · `api/routers/approval_center.py` · `frontend/.../ops/approvals` | LIVE |
| Safe‑Send Gateway | [`safe_send_gateway/`](../../auto_client_acquisition/safe_send_gateway/) · [`channel_policy_gateway/`](../../auto_client_acquisition/channel_policy_gateway/) | LIVE |
| Reply OS | [`email/reply_classifier.py`](../../auto_client_acquisition/email/reply_classifier.py) · `customer_inbox_v10/reply_suggestion.py` | LIVE |
| WhatsApp Conversion (بعد الاهتمام) | [`whatsapp_decision_bot/`](../../auto_client_acquisition/whatsapp_decision_bot/) · `channel_policy_gateway/whatsapp.py` | LIVE |
| Content OS | `growth_beast/content_engine.py` · `proof_to_market/case_study_exporter.py` | PARTIAL (لا ربط بقائمة الموافقة) |
| Press OS | `docs/BRAND_PRESS_KIT.md` | PARTIAL (لا قاعدة جهات إعلامية) |
| Partnership OS | [`partnership_os/`](../../auto_client_acquisition/partnership_os/) · `docs/AGENCY_PARTNER_PROGRAM.md` | LIVE |
| Privacy / PDPL | `docs/PRIVACY_PDPL_READINESS.md` · `security_privacy/` · `compliance_os_v12/` | LIVE |
| Finance OS | [`operating_finance_os/`](../../auto_client_acquisition/operating_finance_os/) · `revenue_profitability/` · `api/routers/finance_os.py` | PARTIAL (لا «CAC by offer») |
| Delivery Handoff | `delivery_os/handoff.py` · `api/routers/onboarding.py` | LIVE |
| Founder GTM Cockpit | [`frontend/.../ops/`](../../frontend/src/app) (founder · war‑room · marketing · sales · partners · approvals · evidence) | LIVE |
| Agent Registry | `agent_os/agent_registry.py` · `agent_os/agent_card.py` · `api/routers/agent_governance.py` | LIVE |
| Evidence L0–L5 / Anti‑Waste | [`proof_engine/evidence.py`](../../auto_client_acquisition/proof_engine/evidence.py) · [`revenue_os/anti_waste.py`](../../auto_client_acquisition/revenue_os/anti_waste.py) | LIVE |
| Proof Pack / Capital Asset | `proof_architecture_os/` · `proof_os/proof_pack.py` · `value_os/value_ledger_postgres.py` | LIVE |
| Suppression / opt‑out | `consent_table.py` · `email/compliance.py` · [`data/outreach/`](../../data/outreach/) فارغ | PARTIAL (لا قائمة مزروعة) |

---

## 5. الأسئلة العشرة — بمسارات حقيقية

| السؤال | المادة الحاكمة | الوحدة الحقيقية | نمط الإجراء |
|---|---|---|---|
| **كيف نبحث؟** | A2 (Signal) | `revenue_os/signal_normalizer.py` — مدخلات المؤسس، **لا scraping** | `suggest_only` |
| **كيف نختار الشركات؟** | A2 (Target Score) | `sales_os/icp_score.py` · `agents/icp_matcher.py` | `suggest_only` |
| **كيف نطابق العرض؟** | A12 (Service Test) | `growth_beast/offer_intelligence.py` + التسعير من §6 | `suggest_only` |
| **كيف نكتب الرسائل؟** | A3 L3 | `revenue_os/draft_pack.py` · `leadops_spine/draft_builder.py` | `draft_only` |
| **كيف نمنع السبام؟** | A4 + §3.3 | `leadops_spine/compliance_gate.py` · `email/compliance.py` · `governance_os/rules/` | `blocked` عند الخرق |
| **كيف نرسل؟** | A3 L3 + A5 | `safe_send_gateway/` → `approval_center/` (250 مسودة OK / 250 إرسال محكوم) | `approval_required` |
| **كيف نتعامل مع الردود؟** | A2 (loop) | `email/reply_classifier.py` · `customer_inbox_v10/reply_suggestion.py` | `suggest_only` |
| **كيف نحوّل للواتساب/البوابة؟** | A4 (NO_COLD_WHATSAPP) | `whatsapp_decision_bot/` — **بعد رد/موافقة فقط** | `approval_required` |
| **كيف نقيس؟** | A8 (Revenue Truth) | `operating_finance_os/` · `revenue_profitability/` · `NORTH_STAR_METRICS_AR.md` | تقرير |
| **كيف نتعلم؟** | A17 | حلقة التعلّم الأسبوعية (§8) · `revenue_os` learning · `GET /revenue-os/learning/weekly-template` | تقرير |

---

## 6. العروض والتسعير — لا اختراع، قرار مطلوب

التسعير محكوم بـ **مصدرين رسميين قائمين**، وهذا الملف **لا يضيف ثالثاً**:

1. **الدستور — المادة 9:** Rung 1 = **499 ريال**.
2. **مصدر الحقيقة للأسعار** [`DEALIX_REVOPS_PACKAGES_AR.md`](../commercial/DEALIX_REVOPS_PACKAGES_AR.md):
   Diagnostic 3,500 · Sprint **9,500** · Pilot 22,000 · RevOps 15K–25K/شهر · Enterprise 85K+.

> 🚩 **تعارض تسعير حقيقي مطلوب حسمه (founder decision).** ثلاثة سلالم تتعايش الآن:
>
> | المصدر | Sprint/الدخول | الأعلى |
> |---|---|---|
> | الدستور A9 + وكلاء الـsales | **499** | 5K–25K |
> | `DEALIX_REVOPS_PACKAGES_AR.md` | **9,500** | 85K+ |
> | رؤيتك الجديدة في هذه الجلسة | 8,000–18,000 | 90K+ |
>
> قاعدة غير قابلة للمساومة: **الوكلاء لا يخترعون أسعاراً** (المادة 12 تشترط حقل
> «Price» من مصدر معتمد). لذلك لم أكتب أرقامك الجديدة كأنها معتمدة. **القرار لك** —
> أيّ سلّم هو القانوني، ثم نوحّد المصدرين ونحدّث الوكلاء عليه.

كل عرض، قبل البيع، يجب أن يجتاز **اختبار الخدمة (المادة 12)** بحقوله الاثني عشر:
`ICP · Pain · Offer · Inputs · Workflow · Deliverables · Proof · Price · Margin ·
Support scope · Upsell path · Blocked claims`.

---

## 7. مستويات الأدلة (L0–L5) وقاعدة منع الهدر

من [`proof_engine/evidence.py`](../../auto_client_acquisition/proof_engine/evidence.py):

```
L0_PLANNED            L1_INTERNAL_DRAFT    → لا تُستخدم في تسويق خارجي
L2_CUSTOMER_REVIEWED  → داخلي
L3_CUSTOMER_APPROVED  → دليل مبيعات خاص بالعميل
L4_PUBLIC_APPROVED    → دراسة حالة عامة (بعد موافقة) — الحدّ الأدنى للنشر العام
L5_REVENUE_EXPANSION  → توسعة/إيراد (بعد التزام كتابي ودفع)
```

قواعد منع الهدر من [`revenue_os/anti_waste.py`](../../auto_client_acquisition/revenue_os/anti_waste.py):

```
no_passport_no_action   → لا إجراء خارجي بلا Source/Decision Passport
upsell_without_proof     → لا upsell بلا Proof Event مسجّل (≥1)
public_proof_below_L4    → لا نشر عام تحت L4 + موافقة
```

تطبيق GTM: لا مسودة تدخل قائمة الموافقة بلا `evidence_level`، ولا claim يُنشر تحت
مستواه المطلوب.

---

## 8. الإيقاع — مربوط بسكربتات قائمة (لا جدولة جديدة)

إيقاعك اليومي/الأسبوعي يُنفَّذ عبر الأدوات الموجودة، لا عبر كرون جديد:

| طقسك المقترح | الأداة القائمة |
|---|---|
| الإيقاع اليومي (صباح/مساء/أسبوعي) | `bash scripts/founder_cadence.sh` |
| الحلقة الأسبوعية (بوابات الأحد) | `bash scripts/founder_weekly_loop.sh` |
| 3 قرارات/دور يومياً | المادة 14 · `GET /api/v1/role-command-v125/today/{role}` |
| موجز المؤسس اليومي | `python scripts/dealix_pm_daily.py` |

حلقة التعلّم الأسبوعية (§24 من رؤيتك): أوقف أسوأ 20% من الرسائل، ضاعف أفضل 20%،
حدّث الـsector playbooks / objection bank / proof library. هذه **عملية**، تُسجَّل في
تقرير التعلّم لا في كود جديد.

---

## 9. خارطة الطريق: نوسّع، لا نعيد البناء

أعِد ترتيب «21 PR» في رؤيتك إلى **سدّ فجوات حقيقية** فقط. كل ما هو LIVE في §4 **لا
يُعاد بناؤه**.

| الأولوية | الفجوة الحقيقية (GAP/PARTIAL) | العمل المقترح |
|---|---|---|
| P0 | منحنى تسخين الإرسال + SPF/DKIM/DMARC + Postmaster | وثيقة سياسة `docs/gtm/SENDING_RAMP_OS_AR.md` + ربطها بـ `deliverability_check.py` |
| P0 | توحيد التسعير (§6) | حسم المؤسس → تحديث `DEALIX_REVOPS_PACKAGES_AR.md` + الدستور A9 + وكلاء sales |
| P1 | بيت رسمي واحد للّا‑تفاوضيات (8 مقابل 11) | فقرة في الدستور أو `docs/` تربط الـ8 الثابتة بالـ11 التشغيلية |
| P1 | قائمة suppression مزروعة + عقد مخطط للـoutreach | بذرة في `data/outreach/` + schema في الوحدة المسؤولة |
| P2 | ربط Content engine بقائمة الموافقة | جسر `growth_beast/content_engine.py` → `approval_center/` |
| P2 | «CAC by offer» في Finance | استعلام/لوحة فوق `operating_finance_os/` |
| P3 | قاعدة جهات إعلامية للـPress | امتداد لـ`BRAND_PRESS_KIT.md` (بدون bulk press spam) |

> لا توجد حاجة لـ«Market Production OS foundation» جديد ككود — هذه الوثيقة **هي** ذلك
> الأساس، وهي تشير إلى البنية القائمة.

---

## 10. قرارات مطلوبة من المؤسس

1. **التسعير:** أيّ من السلالم الثلاثة هو القانوني؟ (لتوحيد A9 + REVOPS + الوكلاء)
2. **التسمية:** هل نتبنّى مسمّيات «12 OS» كطبقة GTM، أم نُبقي تسمية «7 طبقات / 9 أنظمة»
   القائمة ونعدّ هذا الملف مجرد فهرس؟ (توصيتي: الإبقاء على القائم + هذا الملف كفهرس)
3. **أول 3 فجوات:** هل نبدأ بـ P0 (منحنى التسخين + حسم التسعير) كما في §9؟
4. **اللا‑تفاوضيات:** نثبّت «11» في `docs/` رسمياً، أم نُبقي «8 حواجز» الدستورية هي
   المرجع ونصف الـ11 كدوكترين تشغيلي؟

---

## 11. ما الذي **لا** نبنيه (نطاق سلبي)

- ❌ سلّم تسعير رابع (أو كتابة أرقام غير معتمدة كأنها معتمدة).
- ❌ وحدات «OS» مكرّرة لما هو LIVE في §4.
- ❌ دستور منافس — الدستور واحد: [`DEALIX_OPERATING_CONSTITUTION.md`](../DEALIX_OPERATING_CONSTITUTION.md).
- ❌ أي `auto_send` / `auto_charge` / `auto_dm` / cold WhatsApp / LinkedIn automation / scraping.

---

## مراجع

**داخلية (مصادر الحقيقة):**
- [`docs/DEALIX_OPERATING_CONSTITUTION.md`](../DEALIX_OPERATING_CONSTITUTION.md) — الدستور (17 مادة)
- [`docs/DEALIX_CONSTITUTION_TRUTH_AUDIT.md`](../DEALIX_CONSTITUTION_TRUTH_AUDIT.md) — مادة ↔ كود ↔ حالة
- [`docs/commercial/DEALIX_REVOPS_PACKAGES_AR.md`](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) — مصدر أسعار الإيراد
- [`docs/commercial/DEALIX_AI_OPERATING_COMPANY_AR.md`](../commercial/DEALIX_AI_OPERATING_COMPANY_AR.md) — الأنظمة التسعة
- [`docs/commercial/CODE_MAP_OS_TO_MODULES_AR.md`](../commercial/CODE_MAP_OS_TO_MODULES_AR.md) — أنظمة ↔ وحدات ↔ راوترات
- [`docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md`](../strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md) — نموذج التشغيل الأشمل
- [`docs/brand/DEALIX_VISUAL_IDENTITY_AR.md`](../brand/DEALIX_VISUAL_IDENTITY_AR.md) — الهوية والنبرة

**خارجية (سياق سوق فقط — ليست وعود أو مقاييس Dealix؛ بموجب القانون الثاني واختبار
`no_guaranteed_claims`):** معايير CAN‑SPAM وDMARC لتسليم البريد، ونظام حماية البيانات
الشخصية السعودي (PDPL) للخصوصية، وأنماط تعاون الإنسان/الذكاء في النشر واسع النطاق.
تبقى سياقاً للتصميم، ولا تتحوّل إلى أرقام أداء تخص Dealix.

---

*هذه الوثيقة تخضع للدستور. عند أي شك، ارجع إلى المادة 1.*
