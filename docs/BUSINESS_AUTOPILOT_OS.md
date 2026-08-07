# Dealix Business Autopilot OS — خريطة التشغيل الشاملة

> **ما هذا المستند؟** هو الترجمة العملية لرؤية «الشركة تشتغل بنفسها» (12 ماكينة) إلى **النظام المحكوم القائم فعلاً** في هذا المستودع. كل ماكينة هنا تشير إلى وحدات/سكربتات/واجهات API **موجودة ومُختبَرة**، وليست إعادة اختراع موازية.
>
> **What this is:** the practical mapping of the "company runs itself" vision (12 machines) onto the **already-built, governed system** in this repo. Every machine below points to **existing, tested** modules / scripts / API routes — not a parallel re-invention.
>
> **القاعدة:** لا نضيف ماكينة جديدة إذا وُجد ما يكافئها؛ نعيد الاستخدام ونربط. أي أتمتة تخضع لـ **القوانين غير القابلة للتفاوض** و **سلّم الأسعار المعتمد** و **السلسلة الذهبية**.

**المراجع العليا (deeper references):**
- الدستور: [`docs/00_constitution/`](00_constitution/README.md) — القوانين السبعة + غير القابل للتفاوض + معادلة التشغيل.
- نموذج التشغيل: [`docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md`](strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md) — الثمانية محركات ↔ الكود.
- التشغيل اليومي: [`docs/commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md`](commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md) — جدول الـ24 ساعة + ما يعمل تلقائياً مقابل ما يحتاج موافقة.
- شركة جاهزة: [`docs/company/DEALIX_COMPANY_READY_MASTER_AR.md`](company/DEALIX_COMPANY_READY_MASTER_AR.md).
- دليل الوكلاء: [`AGENTS.md`](../AGENTS.md).

---

## 0) القاعدة الذهبية — لماذا توجد كل أتمتة؟

كل أتمتة في Dealix يجب أن تنتج **واحدة على الأقل** من هذه النتائج، وإلا لا تُبنى:

1. ليدز مؤهَّلة أكثر (more qualified leads)
2. تحويل أفضل (better conversion)
3. تسليم أسرع (faster delivery)
4. تكلفة تشغيل أقل (lower operating cost)
5. احتفاظ أعلى بالعميل (higher retention)
6. حِمل ذهني أقل على المؤسس (lower founder cognitive load)
7. مخاطر نشر/أمان أقل (lower deploy/security risk)

**معادلة التشغيل (Operating Equation):**

```text
Dealix = Data + Workflow + AI + Governance + Proof
```

**السلسلة الذهبية (Golden Chain):**

```text
إشارة → Lead → Decision Passport → إجراء معتمد → تسليم → Proof → توسعة → تعلّم
Signal → Lead → Decision Passport → Approved Action → Delivery → Proof → Expansion → Learning
```

API ثابتة للسلسلة الذهبية: `GET /api/v1/decision-passport/golden-chain` · `GET /api/v1/decision-passport/evidence-levels`.

**بوابة القرار (3 من 6 على الأقل):** Does it **sell / deliver / prove / govern / compound / scale**? إن لم تتحقق 3 — لا تنفّذ. (راجع [`docs/00_constitution/DECISION_PRINCIPLES.md`](00_constitution/DECISION_PRINCIPLES.md)).

---

## 1) غير قابل للتفاوض — 11 قانوناً (مفروضة بالاختبارات)

هذه ليست توصيات؛ هي حدود **مفروضة في الكود عبر اختبارات تمر** (`tests/test_no_*` + حُرّاس الحوكمة). أي مخالفة تُسقط CI.

1. لا **scraping** أنظمة.
2. لا **WhatsApp بارد** (cold) آلي.
3. لا **LinkedIn** آلي.
4. لا ادعاءات **بلا مصدر / مزيّفة**.
5. لا **ضمان** نتائج بيع.
6. لا **PII في السجلات**.
7. لا إجابة معرفة **بلا مصدر**.
8. لا **إجراء خارجي بلا موافقة**.
9. لا **وكيل بلا هوية**.
10. لا **مشروع بلا Proof Pack**.
11. لا **مشروع بلا أصل رأس مالي (Capital Asset)**.

المرجع: [`docs/00_constitution/NON_NEGOTIABLES.md`](00_constitution/NON_NEGOTIABLES.md) · القوانين السبعة [`docs/00_constitution/DEALIX_LAWS.md`](00_constitution/DEALIX_LAWS.md).

> **ملاحظة على المخطط المُقترَح (blueprint):** الفكرة الأصلية اقترحت «Follow-up Engine» يرسل رسائل متابعة يومياً تلقائياً ورسائل WhatsApp. هذا **يخالف القوانين 2 و3 و8** ويُسقط اختبارات الحوكمة. البديل المعتمد: **مسودات (draft_only) في Approval Center + إرسال يدوي بعد موافقة المؤسس** (راجع الماكينة 5).

---

## 2) سلّم الأسعار المعتمد (Canonical Pricing Ladder)

السعر التجاري الموحَّد — **هو المرجع** لأي مستند عروض/مالية (لا نعتمد تسعير المخطط الأعلى تذكرةً):

| الدرجة | العرض | السعر (SAR) |
|---|---|---|
| 0 | Free AI Ops Diagnostic | 0 |
| 1 | 7-Day Revenue Proof Sprint | 499 |
| 2 | Data-to-Revenue Pack | 1,500 |
| 3 | Managed Revenue Ops | 2,999–4,999 / شهرياً |
| 4 | Executive Command Center | 7,500–15,000 / شهرياً |
| 5 | Agency Partner OS | مخصص + rev-share |

> **المصدر المعتمد للأسعار:** [`docs/OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md) — هذا الجدول ملخّص؛ لا تُكرَّر الأرقام في أماكن متعددة.
> **إفصاح نمط التسليم:** الدرجتان 0–1 منتج مُتحقَّق يُنتج مخرجاً جاهزاً؛ الدرجات 3–5 اليوم **بقيادة المؤسس / شبه مؤتمتة** (لا تُعرض كخدمات مُدارة بالكامل) وتُفتح بشروط دخول — **لا ضمانات، لا ترقية قبل Proof حقيقي** (القانون 5/10).

هدف 90 يوماً (هدف تقديري — ليس نتيجة محقَّقة): **8–15K SAR MRR + 30–40K SAR لمرة واحدة ≈ 40–55K SAR تراكمي**.
العقود التفصيلية: [`DEALIX_REVOPS_PACKAGES_AR.md`](commercial/DEALIX_REVOPS_PACKAGES_AR.md) · الطبقات: [`PRODUCTIZED_OFFER_STACK.md`](endgame/PRODUCTIZED_OFFER_STACK.md) · صفحات الخدمات: [`sales/service_pages/`](../sales/service_pages/) · فهرس: [`sales/OFFER_STACK.md`](../sales/OFFER_STACK.md).

---

## 3) المحركات الـ12 ↔ النظام القائم (خريطة التنفيذ)

> هذه هي **القلب**: رؤية المخطط (12 ماكينة) مربوطة بالوحدات الحقيقية. حيث لا يوجد ملف `.js` — لأن المنصة **Python (FastAPI) + Next.js**، ولا يوجد `package.json` في الجذر.

| # | الماكينة (blueprint) | النظام القائم في الريبو | المخرج اليومي الفعلي |
|---|---|---|---|
| 1 | **Founder Command Center** | `auto_client_acquisition/founder_command_summary/` (daily_brief · weekly_agenda) + `api/routers/founder_command_summary.py` · `dealix/commercial_ops/founder_full_autopilot.py` · UI `/[locale]/ops/founder` ([`FounderCommandCenter.tsx`](../frontend/src/components/gtm/FounderCommandCenter.tsx)) · `scripts/dealix_founder_daily_brief.py` + `scripts/run_founder_commercial_day.sh` + `scripts/founder_daily_scorecard.py` | [`reports/company_os/daily/CEO_BRAIN_TODAY.md`](../reports/company_os/daily/CEO_BRAIN_TODAY.md) · `STRATEGIC_BRIEF_TODAY.md` · `data/founder_briefs/YYYY-MM-DD.md` |
| 2 | **Revenue Engine** | `dealix/revenue_ops_autopilot/` (war_room · account_scoring_matrix · scoring · orchestrator) · `auto_client_acquisition/revenue_os/` (source_registry · enrichment_waterfall · dedupe · action_catalog · expansion_engine) · `api/routers/revenue_ops_autopilot.py` | War Room: `GET /api/v1/ops-autopilot/war-room/today-pack` |
| 3 | **Market Research Engine** | `auto_client_acquisition/growth_beast/market_radar.py` (إشارات آمنة بلا HTTP) · `revenue_os/signal_normalizer.py` · `intelligence/signals.py` · `market_intelligence/` · [`docs/sector-reports/`](sector-reports/) | `POST /api/v1/revenue-os/signals/normalize` (مدخلات المؤسس → Why Now / Offer / Proof) |
| 4 | **Offer Engine** | المصدر المعتمد [`docs/OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md) · `auto_client_acquisition/finance_os/pricing_catalog.py` · `service_catalog/` · [`sales/OFFER_STACK.md`](../sales/OFFER_STACK.md) (فهرس) | `GET /api/v1/revenue-os/catalog` (كتالوج الإجراءات + المصادر) |
| 5 | **Outreach Engine** | `dealix/revenue_ops_autopilot/outreach_templates.py` (**draft_only**) · `data/outreach/` · `data/templates/` (warm intros) · `approval_center` + `channel_policy_gateway` | مسودات في Approval Center — **لا إرسال آلي** |
| 6 | **CRM / Pipeline** | War Room (`revenue_ops_autopilot/war_room.py`) · `crm_bridge.py` (HubSpot sync) · `api/routers/crm_v10.py` · `revenue_pipeline/` · مخزن أحداث `revenue_memory` + [`docs/ledgers/`](ledgers/README.md) (DECISION · CLIENT · DELIVERY — append-only، يحلّ محل `deals.json`) | `GET /api/v1/ops-autopilot/war-room?needs_follow_up=true` |
| 7 | **Delivery Engine** | `delivery_os` · `delivery_factory` · `service_sessions` · `revenue_ops_autopilot/proof_pack_ledger.py` · `retainer_eligibility.py` · `capital_asset_registry.py` · [`docs/delivery/`](delivery/) | Proof Pack (مراجعة بشرية) — [`PROOF_PACK_TEMPLATE.md`](delivery/PROOF_PACK_TEMPLATE.md) |
| 8 | **Finance Engine** | `auto_client_acquisition/finance_os/` · `operating_finance_os/` · `revenue_profitability/` · [`docs/finance/`](finance/) · سلّم الأسعار (§2) | تسعير + هامش — لا `payment_received` وهمي (إيراد من دفع حقيقي فقط) |
| 9 | **Product Engine** | `frontend/` Next.js (`/ops/founder` · `/cloud` · `components/revenue-autopilot/`) · `api/routers/` (120+ router) | PRs صغيرة — تخدم founder/revenue لا UI مجرّد |
| 10 | **QA / Security Engine** | [`docs/36_agent_runtime_security/`](36_agent_runtime_security/README.md) (FOUR_BOUNDARY_PROTECTION · PROMPT_INTEGRITY · TOOL/DATA/CONTEXT_BOUNDARY) · `runtime_safety_os` · `secure_agent_runtime_os` · `tool_guardrail_gateway` · `channel_policy_gateway` · `agent_identity_access_os` · `.gitleaks.toml` · `tests/test_no_*` (100+ حارس دستور) | تقارير CI/أمان + بوابات الحوكمة |
| 11 | **Deployment Engine** | Railway (`railway*.toml` · `scripts/railway_prod_bootstrap.sh` · `scripts/official_launch_verify.sh`) · [`docs/contributing/DEPLOYMENT.md`](contributing/DEPLOYMENT.md) | `OFFICIAL_LAUNCH_VERDICT=PASS` — production بموافقة بيئة |
| 12 | **Learning Engine** *(هيكل — يحتاج ربط تحليلات)* | `revenue_os/learning_weekly.py` (skeleton) · `growth_beast/experiment_engine.py` (فرضيات أسبوعية آمنة) · `growth_beast/weekly_learning.py` · `dealix/commercial_ops/revenue_learning_loop.py` · سجل: [`docs/ledgers/LEARNING_LEDGER.md`](ledgers/LEARNING_LEDGER.md) | `GET /api/v1/revenue-os/learning/weekly-template` |
| + | **Marketing Engine** (إضافي في المخطط) | `dealix/marketing_factory/` · [`docs/marketing/MARKETING_FACTORY.md`](marketing/MARKETING_FACTORY.md) · `scripts/generate_weekly_content_drafts.py` (**draft_only**) | 5 مسودات LinkedIn/أسبوع → `var/content_drafts/` (لا نشر آلي) |

---

## 4) المخرجات اليومية (Daily Outputs) — حقيقية، لا قوالب فارغة

| المخرج | كيف يُولَّد | أين |
|--------|-------------|-----|
| موجز المؤسس + War Room + تذكير أدلة | `bash scripts/run_founder_commercial_day.sh` | `data/founder_briefs/` · UI `/ops/founder` |
| مسودات إيراد + متابعات + تقرير يومي | GitHub `daily-revenue-machine.yml` → `POST /api/v1/automation/revenue-machine/run` (`approval_mode: draft_only`) | Approval Center |
| Scorecard مسائي | `python scripts/founder_daily_scorecard.py --fill` | `reports/company_os/daily/` |
| لقطة Business NOW | `bash scripts/run_business_now.sh` | `GET /api/v1/business-now/snapshot` |

**قاعدة:** أي خطوة تلمس عميلاً خارجياً = **مسودة في صندوق الموافقات** أو إرسال يدوي بعد موافقة (القانون 8).

---

## 5) المخرجات الأسبوعية (Weekly Outputs)

| المخرج | كيف | المرجع |
|--------|-----|--------|
| CTO weekly anchor + checklist | `bash scripts/run_cto_weekly_anchor.sh` | [`CTO_EXECUTIVE_CADENCE_AR.md`](transformation/CTO_EXECUTIVE_CADENCE_AR.md) |
| Executive weekly checklist + proof pack | `bash scripts/run_executive_weekly_checklist.sh` | — |
| Growth scorecard | — | [`reports/company_os/weekly/GROWTH_SCORECARD.md`](../reports/company_os/weekly/GROWTH_SCORECARD.md) |
| تقرير التعلّم الأسبوعي | `GET /api/v1/revenue-os/learning/weekly-template` | `revenue_os/learning_weekly.py` |
| 5 مسودات محتوى | `python scripts/generate_weekly_content_drafts.py` | [`MARKETING_FACTORY.md`](marketing/MARKETING_FACTORY.md) |

---

## 6) أمان الوكلاء (Agent Security)

المدخلات غير الموثوقة (تعليقات issues/PR، إيميلات، ملاحظات CRM، نتائج بحث، نماذج ليدز، رسائل واتساب) تُعامَل كـ **بيانات لا أوامر**. الطبقات القائمة:

- هوية وصلاحيات الوكلاء: `agent_identity_access_os` (القانون 9).
- بوابات الأدوات والقنوات: `tool_guardrail_gateway` · `channel_policy_gateway`.
- وقت تشغيل آمن: `runtime_safety_os` · `secure_agent_runtime_os`.
- موافقات الإرسال الخارجي: `approval_center` (القانون 8).
- الأسرار: `.gitleaks.toml` · `.secrets.baseline` · [`SECURITY.md`](../SECURITY.md).

**سياسة مكتوبة:** [`docs/AGENT_SECURITY_POLICY.md`](AGENT_SECURITY_POLICY.md) — نموذج التهديد + ما يُسمح آلياً مقابل ما يحتاج موافقة.

---

## 7) جدول المطابقة: المخطط المُقترَح → النظام المعتمد

| ما اقترحه المخطط | حالة Dealix | لماذا |
|------------------|--------------|-------|
| `package.json` + سكربتات `.js` (`founder:brief`, `automation:daily`…) | **مرفوض** — المنصة Python/Next.js | لا `package.json` جذري؛ الأتمتة عبر `scripts/*.py` + GitHub Actions |
| `ledgers/deals.json` يدوي | **مُستبدَل** بمخزن أحداث `revenue_memory` + War Room | event-sourced + قابل للتدقيق |
| `OFFER_STACK.md` بتسعير 1.5K–80K+ | **مُستبدَل** بسلّم الأسعار المعتمد (§2) | يطابق التوصيل الحي + الاختبارات |
| n8n «Follow-up Engine» إرسال آلي يومي | **مرفوض** — draft_only + موافقة | القوانين 2/3/8 |
| Market Research بـ scraping/HTTP | **مُستبدَل** بإشارات آمنة (`market_radar.py`) | القانون 1 |
| `AGENT_SECURITY_POLICY.md` | **مُعتمَد ومُضاف** (محتوى محكوم) | يخدم القانون 8/9 |
| `BUSINESS_METRICS.md` | **مُعتمَد ومُضاف** (مربوط بالموجود) | بدون vanity metrics |
| Founder Command / Weekly Board | **موجود مسبقاً** (§4، §5) | لا تكرار |

---

## 8) الفجوات الحقيقية (Genuine Gaps) — وحالتها

> بعد مسح الوحدات: 17 من 18 مفهوماً في المخطط **موجود ومُختبَر**. الأصل: لا نبني إلا ما لا يوجد، ولا يخالف الدستور.

| الفجوة | الحالة | الإجراء |
|--------|--------|---------|
| خريطة شاملة تربط رؤية الـ12 ماكينة بالنظام | ✅ **مُضاف** | `docs/BUSINESS_AUTOPILOT_OS.md` (هذا الملف) |
| سياسة أمان وكلاء موحّدة + نموذج تهديد المدخلات غير الموثوقة | ✅ **مُضاف** (يربط `docs/36_agent_runtime_security/`) | [`docs/AGENT_SECURITY_POLICY.md`](AGENT_SECURITY_POLICY.md) |
| فهرس مؤشرات أعمال للمؤسس (مربوط بالـ12 metric board) | ✅ **مُضاف** | [`docs/BUSINESS_METRICS.md`](BUSINESS_METRICS.md) |
| فهرس عروض موحّد في `sales/` | ✅ **مُضاف** (يشير للمصدر المعتمد) | [`sales/OFFER_STACK.md`](../sales/OFFER_STACK.md) |
| ملف ICP سعودي B2B موحّد | ✅ **مُضاف** | [`sales/ICP_SAUDI_B2B.md`](../sales/ICP_SAUDI_B2B.md) |
| **Learning Engine** — ربط التحليلات بالتقرير الأسبوعي | ⏳ **مفتوح** (هيكل جاهز) | `revenue_os/learning_weekly.py` skeleton ينتظر backend تحليلات؛ لا تُختلق أرقام قبل الربط (القانون 4/7) |

---

## 9) المراجع (References)

- الدستور والقوانين: [`docs/00_constitution/`](00_constitution/)
- نموذج التشغيل (8 محركات ↔ كود): [`docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md`](strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md)
- التشغيل اليومي المحكوم: [`docs/commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md`](commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md)
- شركة جاهزة (ابدأ هنا): [`docs/company/DEALIX_COMPANY_READY_MASTER_AR.md`](company/DEALIX_COMPANY_READY_MASTER_AR.md)
- مؤشرات الأعمال: [`docs/BUSINESS_METRICS.md`](BUSINESS_METRICS.md)
- سياسة أمان الوكلاء: [`docs/AGENT_SECURITY_POLICY.md`](AGENT_SECURITY_POLICY.md)
- دليل الوكلاء: [`AGENTS.md`](../AGENTS.md)

---

*Dealix = Founder OS + Revenue OS + Delivery OS + Automation OS — نظام بزنس محكوم، لا مجرد كود.*
*كل رقم حقيقي فقط؛ القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.*
