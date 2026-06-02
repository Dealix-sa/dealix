# Dealix Market Production OS — المرجع الرئيسي — Master Reference

> الفكرة الحاسمة: **Dealix ليس أداة spam — هو نظام إنتاج سوق محكوم (Governed Market Production OS).**
> ينتج بكثافة، يفلتر بصرامة، يرسل بتدرج وبموافقة المؤسس فقط، ويتعلّم من الردود.

هذا المستند هو **العمود الفقري** لطبقة *Market Production OS*. يربط الرؤية (18 مكوّنًا) بالوحدات
الموجودة فعليًا في المستودع، ويحدّد القواعد الصارمة، والإيقاع اليومي، وما هو *جديد* مقابل ما يُعاد
استخدامه. كل ما يُبنى هنا يجب أن يحترم **اللاءات الإحدى عشرة** (انظر `AGENTS.md` ووكلاء `.claude/agents`).

---

## 0. المبدأ الحاكم — 250 مسودة، صفر إرسال تلقائي

| البُعد | القيمة | الحالة |
|---|---|---:|
| طاقة إنتاج المسودات يوميًا | **250 drafts/day** | مسموح ومطلوب |
| الإرسال التلقائي الخارجي | **0 (صفر)** في كل البيئات | محظور دائمًا |
| الإرسال الفعلي | بعد موافقة المؤسس + تدرّج الإرسال | بوابة بشرية إلزامية |

> القاعدة: `DAILY_DRAFT_TARGET = 250` و `MAX_AUTO_SENDS = 0`. المسودة كائن جاهز للمراجعة،
> وليست رسالة مُرسَلة. لا يتحول أي draft إلى send إلا عبر `approval_center` + بوابة الإرسال.

تدرّج الإرسال (Sending Ramp) — *حد أقصى* للإرسال اليدوي المعتمد، وليس إرسالًا تلقائيًا:

| المرحلة | Drafts/day | Sends/day (سقف) | الهدف |
|---|---:|---:|---|
| Week 0 | 250 | 0–20 | اختبار الجودة والرسائل |
| Week 1 | 250 | 25–50 | warm-up وإثبات أولي |
| Week 2 | 250 | 50–100 | توسيع بحذر |
| Week 3 | 250 | 100–150 | حسب صحة الدومين |
| Week 4+ | 250+ | 150–250 | فقط إذا السمعة ممتازة |

---

## 1. اللاءات الإحدى عشرة (لا تُخرَق أبدًا)

1. لا أنظمة scraping.
2. لا أتمتة WhatsApp بارد (cold).
3. لا أتمتة LinkedIn.
4. لا ادعاءات زائفة أو بلا مصدر.
5. لا ضمان نتائج مبيعات.
6. لا PII في السجلات.
7. لا إجابات معرفية بلا مصدر.
8. لا إجراء خارجي بدون موافقة.
9. لا وكيل بدون هوية (Agent Card).
10. لا مشروع بدون Proof Pack.
11. لا مشروع بدون Capital Asset.

أي طلب أو عمل يخالف واحدة منها → **يُرفض ويُقترح البديل الآمن**. لا التفاف على البوابات.

---

## 2. خريطة المكوّنات الـ 18 → الوحدات الفعلية

> المبدأ: **أعد الاستخدام قبل أن تكتب.** المستودع يحوي 200+ وحدة. الجديد هنا = طبقة تنسيق
> رقيقة (`auto_client_acquisition/market_production_os/`) + مخططات (`schemas/`) + وثائق + سير عمل CI.

| # | المكوّن | يُعاد استخدامه (موجود) | الجديد في هذه الطبقة |
|---|---|---|---|
| 1 | Brand OS | `docs/brand/`, `docs/BRAND_PRESS_KIT.md`, `design-systems/dealix`, `DESIGN_SYSTEM.md` | `docs/market_production_os/01_BRAND_OS_AR.md` |
| 2 | Product Catalog OS | `docs/commercial/offers/`, `revenue_os/source_registry`+`action_catalog`, سلّم `sales_os` الخماسي | `02_PRODUCT_CATALOG_OS_AR.md` |
| 3 | Sector Intelligence OS | `docs/sector-reports/`, `revenue_os/saudi_targeting_profile`, `vertical_playbooks` | `03_SECTOR_INTELLIGENCE_OS_AR.md` + `seeds/sectors.yaml` |
| 4 | Prospect Research OS | `revenue_os/targeting`+`account_scoring`, `data_os.SourcePassport` | `04_*`, `prospect_score.py`, `schemas/prospect.schema.json` |
| 5 | Signal Detection OS | `revenue_os/signal_normalizer`, `radar_events`, `market_intelligence` | `05_*`, `schemas/{job,company}_signal.schema.json` |
| 6 | Cold Email Draft Factory (250/day) | `revenue_os/draft_pack`, `marketing_factory` | `06_*`, `draft_factory.py`, `schemas/outreach_draft.schema.json` |
| 7 | Compliance & Deliverability Gate | `governance_os.policy_check_draft`, `channel_policy_gateway`, `safe_send_gateway`, `revenue_os/anti_waste` | `07_*`, `quality_gate.py` |
| 8 | Founder Approval Queue | `approval_center` (policy/store/renderer/founder_rules) | `08_*`, `approval_queue.py` |
| 9 | Sending Ramp OS | `safe_send_gateway`, `approval_center` | `sending_ramp.py` (داخل `08_*`) |
| 10 | Reply Handling OS | `support_inbox`, `customer_inbox_v10`, `customer_loop` | `09_*`, `reply_router.py`, `schemas/reply.schema.json` |
| 11 | Job/Buying Signal OS | `radar_events`, `revenue_os/signal_normalizer` | مدمج في `05_*` + `schemas/job_signal.schema.json` |
| 12 | Content Production OS | `gtm_os/content_calendar`, `marketing_factory`, `docs/content/` | `11_*` |
| 13 | Press OS | `docs/BRAND_PRESS_KIT.md` (قاعدة: 3 جهات + 7 أيام) | `12_*` |
| 14 | Partnerships OS | `partnership_os`, `docs/partners/`, `docs/partner_os/` | `13_*` |
| 15 | WhatsApp Post-Reply OS | `whatsapp_decision_bot`, `channel_policy_gateway/whatsapp.py` | `10_WHATSAPP_*` (consent-only) |
| 16 | Saudi PDPL Privacy Guard | `compliance_os`, `docs/commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md` | `17_PDPL_PRIVACY_GUARD_AR.md` |
| 17 | Founder GTM Control Room | واجهة `/[locale]/ops/founder` + `/ops/marketing` + `/ops/approvals` (موجودة) | تعيين تبويبات (وثيقة `14_*`) — لا واجهة جديدة |
| 18 | Metrics + Learning Loop | `revenue_os/learning_weekly`, `docs/commercial/NORTH_STAR_METRICS_AR.md` | `14_*`, `report.py` (Daily/Weekly GTM report) |
| + | Agent Team | `agent_os/agent_registry` + `AgentCard` | `data/agents/market_production_agents.jsonl` + سكربت تسجيل |

---

## 3. المعمارية — تدفّق الإنتاج

```txt
Brand OS
→ Product Catalog OS
→ Sector Intelligence OS
→ Prospect Research OS  (prospect_score: 7 عوامل /100)
→ Signal Detection OS
→ 250/day Draft Factory  (send_status = "draft" دائمًا)
→ Quality + Compliance Gate  (governance + anti_waste + deliverability)
→ Founder Approval Queue  (Top-50 ترتيب)
→ Sending Ramp OS  (سقف يومي حسب الأسبوع + صحة الدومين)
→ Reply Handling OS  (تصنيف + إجراء + suppression)
→ WhatsApp Post-Reply OS  (بعد reply/consent فقط)
→ Proposal + Proof OS  (sales_os + proof_os)
→ Content + Press + Partnerships OS
→ Founder GTM Control Room  (/ops/*)
→ Weekly Learning Loop
```

كل كائن مُنتَج يحمل حقل `governance_decision` (لا إخراج بدون قرار حوكمة)، و `evidence_level`
(L0–L5)، و `compliance_status`, و `approval_status`, و `send_status` (افتراضيًا `draft`).

---

## 4. مقياس Prospect (مجموع = 100)

| العامل | الوزن |
|---|---:|
| sector_fit | 20 |
| likely_lead_flow | 20 |
| decision_maker_clarity | 15 |
| pain_signal | 15 |
| payment_ability | 15 |
| personalization_signal | 10 |
| risk_low | 5 |

الحدّ الأدنى للتأهيل: **60/100**. أقل من ذلك → `nurture` أو `do_not_contact`.

مستويات التخصيص (Personalization): `P0` قطاع فقط · `P1` شركة+قطاع · `P2` ألم من
موقع/وظيفة/محتوى · `P3` trigger حديث · `P4` proof/offer مخصص. **لا تُنتَج مسودة أقل من P1.**

---

## 5. تسعير — مصدر الحقيقة الوحيد (السلّم الخماسي)

> ⚠️ لا تخترع سعرًا. التسعير الرسمي هو سلّم `sales_os` الخماسي (انظر `.claude/agents/dealix-sales.md`).
> أي أرقام أعلى في خطط قديمة = نطاق *Custom/Enterprise* فقط، ولا تتعارض مع السلّم.

| الدرجة | العرض | السعر (SAR) | إشارة العميل |
|---|---|---|---|
| 0 | Free AI Ops Diagnostic | 0 | أول تواصل |
| 1 | 7-Day Revenue Intelligence Sprint | 499 | ألم واضح + مالك + بيانات جاهزة |
| 2 | Data-to-Revenue Pack | 1,500 | + تصدير CRM/CSV + معالجة PII |
| 3 | Managed Revenue Ops | 2,999–4,999/mo | Proof ≥ 80 + adoption ≥ 70 |
| 4 | Custom AI Setup | 5,000–25,000 + 1,000/mo | نطاق خارج السلّم |
| Enterprise | AI Governance Review | 25,000–50,000 | بنك/مؤسسة كبيرة/منظّم |

---

## 6. الإيقاع اليومي (واقعي)

| الوقت | المرحلة | المخرج |
|---|---|---|
| 07:30 | Research | prospects + job signals + sector triggers |
| 08:30 | Draft Factory | توليد 250 مسودة (`send_status=draft`) |
| 09:00 | Gates | brand + personalization + compliance + deliverability |
| 10:00 | Approval | المؤسس يعتمد 30–50 |
| 11:00 | Sending | دفعة محدودة معتمدة فقط (ضمن سقف الأسبوع) |
| 13:00 | Replies | تصنيف الردود + الإجراء التالي |
| 15:00 | Channels | partners + press + job signals |
| 18:00 | Content | LinkedIn + proof + founder insights |
| 21:00 | Report | تقرير GTM اليومي |

### 7 مخرجات يومية إلزامية
1) 250 drafts · 2) Top-50 approval queue · 3) Sending batch plan · 4) Reply queue ·
5) Job signal report · 6) Content calendar · 7) Daily GTM report.

### مراجعة أسبوعية
أفضل قطاع · أفضل عرض · أفضل subject · أفضل CTA · أفضل مصدر إشارة · أسوأ مصدر bounce · تجارب الأسبوع القادم.

---

## 7. القواعد الصارمة للإرسال والامتثال

**ممنوع:** قوائم بريد مشتراة · عناوين/مواضيع مضللة · `Re:`/`Fwd:` زائفة · إرسال بدون unsubscribe ·
تجاهل opt-out · الإرسال لقائمة suppression · ادعاءات بلا دليل · WhatsApp بارد · أتمتة LinkedIn ·
scraping يخالف الشروط.

**شرط الإرسال (كلها معًا):** `approval` + `unsubscribe_included` + `domain_health_ok` +
`suppression_check` + `personalization ≥ P1` + `risk_level ∈ {low, medium}`.

**Deliverability DNS:** SPF · DKIM · DMARC · custom tracking domain · valid reply-to ·
unsubscribe endpoint · suppression list · bounce handling · Postmaster Tools.

> المراجع الفنية (deliverability/CAN-SPAM/DMARC/suppression) موثّقة في `07_COMPLIANCE_DELIVERABILITY_OS_AR.md`.

---

## 8. الكود والاختبارات (الجزء الملموس)

- الوحدة الجديدة: `auto_client_acquisition/market_production_os/` —
  `schemas.py`, `prospect_score.py`, `quality_gate.py`, `draft_factory.py`,
  `sending_ramp.py`, `approval_queue.py`, `reply_router.py`, `stores.py`, `report.py`.
- المخططات: `schemas/*.schema.json` (prospect, outreach_draft, job_signal, company_signal,
  reply, sending_batch, suppression, approval_action, email_account).
- البوابة تُركّب الأنوية الموجودة: `governance_os.policy_check_draft` +
  `governance_os.audit_claim_safety` + `revenue_os.anti_waste.validate_pipeline_step`.
- الاختبارات: `tests/test_market_production_os.py` + حارس عقيدة جديد
  `tests/test_no_auto_send_market_production.py` (يثبت أن المصنع لا يُرسل تلقائيًا أبدًا).
- سير عمل CI: `.github/workflows/gtm-quality-gate.yml`, `gtm-draft-day.yml`, `weekly-gtm-review.yml`.
- سكربتات: `scripts/gtm_quality_gate.py`, `scripts/run_gtm_draft_day.py`.

تشغيل سريع:
```bash
python3 scripts/run_gtm_draft_day.py --dry-run        # ينتج مسودات + تقرير (لا إرسال)
python3 scripts/gtm_quality_gate.py --check-samples    # يفشل عند خرق أي قاعدة
APP_ENV=test pytest tests/test_market_production_os.py tests/test_no_auto_send_market_production.py -q
```

---

## 9. ترتيب التنفيذ (Phases)

1. **السوق والهوية:** Brand · Product Catalog · Sector Intelligence.
2. **البحث والإنتاج:** Prospect Research · Signal Detection · 250/day Draft Factory.
3. **الحماية والإرسال:** Compliance Gate · Deliverability · Approval Queue · Sending Ramp.
4. **الرد والتحويل:** Reply Handling · WhatsApp Post-Reply · Proposal + Proof.
5. **القنوات الإضافية:** Content · Press · Partnerships · Job Signals.
6. **الإدارة:** Founder GTM Control Room · Metrics · Weekly Learning.

---

## روابط الطبقة
- [README — الفهرس](README.md)
- المكوّنات: `01_…` حتى `17_…` في هذا المجلد.
- العقيدة: [`../../AGENTS.md`](../../AGENTS.md) · وكلاء `.claude/agents/`.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
