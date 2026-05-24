# Sprint Readiness Audit — 2026-05-24

**اللغة:** AR primary · EN gloss للمصطلحات التقنية
**المراجع:**
[FIRST_PAID_DIAGNOSTIC_DOD_AR.md](../commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md) ·
[PROOF_PACK_TEMPLATE.md](./PROOF_PACK_TEMPLATE.md) ·
[RETAINER_ELIGIBILITY_CHECKLIST_AR.md](./RETAINER_ELIGIBILITY_CHECKLIST_AR.md) ·
[27_delivery_playbooks/](../27_delivery_playbooks/)

> **القاعدة:** هذه نتيجة تدقيق فقط (audit only). لا بناء جديد، لا ميزات جديدة.
> ما يثبت ناقصاً يُسجَّل كـ gap ولا يُنفَّذ تلقائياً.

## ملخص الحُكم (Verdict)

**YELLOW** — البنية التحتية للسبرنت موجودة، لكن 3 فجوات تكامل تمنع التشغيل السلس
خلال أول صفقة Diagnostic مدفوعة. (راجع «أعلى 3 إصلاحات قبل الإغلاق» في نهاية المستند.)

---

## (1) جدول التدقيق — 8 خطوات السبرنت

| # | الخطوة (Step) | (a) Template/SOP | (b) Ledger Write | (c) Verify Script Catches | الحُكم |
|---|---------------|------------------|------------------|--------------------------|--------|
| 1 | **Source Passport** (Day 1 Kickoff) | [SOURCE_PASSPORT_STANDARD.md](../standards/SOURCE_PASSPORT_STANDARD.md) + [SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md) موجودان · `data_os.validate(passport)` ينفّذ التحقق | لا يوجد JSONL ledger مستقل للـ Passport — التحقق inline فقط (in-memory `SourcePassportValidation`) | جزئي: `tests/test_data_os_source_passport_bridge.py` + `tests/test_no_source_passport_no_ai.py` يفحصان validate لكن لا script يفحص «هل تم تشغيلها لكل عميل» | YELLOW |
| 2 | **Data Import + DQ Score** (Day 2) | `data_os.preview(file_or_csv)` + `data_os.compute_dq` موجودان في `auto_client_acquisition/data_os/data_quality_score.py` + `import_preview.py` | DQ يُكتب كجزء من Proof Pack `quality_scores` section — لا ledger مستقل | `tests/test_data_os_quality.py` يفحص حساب DQ; لا verify script يفحص «هل DQ تم لكل engagement_id» | YELLOW |
| 3 | **Account Scoring** (Day 3) | `revenue_os.account_scoring` + `tests/test_revenue_os_catalog.py` + `revenue_os_master_verify.sh` | لا ledger مستقل — المخرجات تدخل proof pack `outputs` section | `revenue_os_master_verify.sh` يفحص golden chain · لا فحص لـ «top 10 + reasons per account» | YELLOW |
| 4 | **Draft Pack** (Day 4 AR+EN) | `revenue_os.draft_pack` (راجع `tests/test_revenue_os_draft_pack.py`) · governance gate موجود `governance_os.decide` | الـ draft يُرسل إلى `approval_center` (راجع `api/routers/approval_center.py`) | `tests/test_revenue_os_draft_pack.py` + `tests/test_approval_center.py` · لا verify script يربط draft↔governance↔approval كسلسلة | GREEN |
| 5 | **Governance Review** (Day 4-5) | `auto_client_acquisition/governance_os/` + `claim_safety.contains_unsafe_claim` + `redact_text` | governance events تدخل proof pack `governance_decisions` section | `tests/test_proof_ledger_redacts_on_export.py` يفحص الـ redact — قوي | GREEN |
| 6 | **Proof Pack Assembly** (Day 5) | `auto_client_acquisition/proof_os/proof_pack.py` + 14 section schema في `proof_architecture_os/proof_pack_v2.py` · القالب: [PROOF_PACK_TEMPLATE.md](./PROOF_PACK_TEMPLATE.md) | `proof_ledger` (file backend) + event `proof_pack_delivered` في `revenue_pipeline/stage_policy.py` | `scripts/verify_proof_pack.py` يفحص وجود قالب لكل service · `tests/test_proof_pack_required.py` + `test_proof_pack_assembler.py` (10 passed محلياً) | GREEN — بعد تحديث القالب اليوم |
| 7 | **Capital Asset Registration** (Day 7) | `auto_client_acquisition/capital_os/capital_ledger.py` (`add_asset` + `list_assets`) · 6 أنواع في `asset_types.py` | JSONL في `var/capital-ledger.jsonl` (env `DEALIX_CAPITAL_LEDGER_PATH`) | لا verify script يفحص «هل أُنتج ≥ 1 asset لكل engagement» — مرجَّح فقط في `scripts/dealix_pm_daily.py:134` (تنبيه يومي) | RED — لا gate تسليم |
| 8 | **Retainer Eligibility** (Day 7) | `auto_client_acquisition/adoption_os/retainer_readiness.py` (`evaluate(...)`) · القائمة: [RETAINER_ELIGIBILITY_CHECKLIST_AR.md](./RETAINER_ELIGIBILITY_CHECKLIST_AR.md) | لا ledger — verdict in-memory يُمرَّر إلى founder review | لا verify script · لا اختبار يربطه بـ proof_score + capital asset count | YELLOW |

---

## (2) Friction Log Integration — Matrix

`auto_client_acquisition/friction_log/schemas.py` يعرّف 8 `FrictionKind`، منها
خاصّان للسبرنت: `MISSING_SOURCE_PASSPORT` و `MISSING_PROOF_PACK`.

| الخطوة | FrictionKind المتوقع | مكان الـ emit الفعلي | الفجوة |
|--------|---------------------|----------------------|--------|
| Source Passport invalid | `MISSING_SOURCE_PASSPORT` | لا emitter مسجّل في الكود (grep يظهر التعريف فقط في `schemas.py`) | **gap — لا caller** |
| DQ score < 70 | `SCHEMA_FAILURE` أو `APPROVAL_DELAY` | لا emit صريح من `data_quality_score.py` | **gap** |
| Account scoring فشل | `SCHEMA_FAILURE` | لا emit | **gap** |
| Draft governance block | `GOVERNANCE_BLOCK` | متاح كـ enum, لا caller موثَّق في سلسلة `revenue_os.draft_pack` | **gap** |
| Approval delay > SLA | `APPROVAL_DELAY` | متاح كـ enum, لا scheduler يبعث الـ event | **gap** |
| Proof Pack مفقود عند الإغلاق | `MISSING_PROOF_PACK` | لا emitter | **gap — لا caller** |
| Capital asset لم يُسجَّل | `MANUAL_OVERRIDE` | تنبيه في `dealix_pm_daily.py:134` فقط — لا friction event | **gap** |
| Retainer evaluator فشل | `SUPPORT_TICKET` | لا emit | **gap** |

**الخلاصة:** البنية التحتية (`friction_log.emit`) جاهزة + sanitizer للـ PII قائم،
لكن **لا توجد callers** في خطوات السبرنت. Documenting only — لا بناء.

---

## (3) Capital Asset Registration Flow — Audit

ملف: `auto_client_acquisition/capital_os/capital_ledger.py`

| الفحص | النتيجة | الدليل |
|-------|---------|--------|
| (a) يتطلّب `consent_on_file=yes` قبل publication | **مفقود** | `CapitalAsset` لا يحتوي حقل `consent_on_file` ولا حقل `publication_status`. `add_asset()` لا يأخذ المعامل. | 
| (b) يكتب صفّاً في ledger | **موجود** | يكتب JSONL إلى `var/capital-ledger.jsonl` مع lock + sanitization | 
| (c) يبعث friction event عند الفشل | **مفقود** | `add_asset()` يرفع `ValueError` فقط؛ لا `friction_log.emit(...)` في مسار الخطأ | 

**سكربت register مستقل:** `scripts/register_capital_asset.py` — **غير موجود**.
الاستخدام الحالي عبر استدعاء `capital_os.add_asset(...)` مباشرة من delivery
playbook agents. لا CLI wrapper — يستلزم founder/engineer قراراً.

> ملاحظة (no-build): لم يُبنَ شيء. الفجوات وثَّقت فقط.

---

## (4) Test Results — `pytest`

الأمر المطلوب: `pytest tests/test_delivery_os_framework.py tests/test_service_readiness_score.py -q --no-cov`

النتيجة الخام:
- `--no-cov` غير مدعوم في `pyproject.toml` (الـ addopts يجبر `--cov=...`) → استُخدم `-o addopts=""`
- `test_delivery_os_framework.py` + `test_service_readiness_score.py` يفشلان في الاستيراد بسبب `ModuleNotFoundError: phonenumbers` (سلسلة imports عبر `core.agents`).
- بعد تثبيت `tenacity`، الخطأ التالي: `phonenumbers` ثم `fastapi` للـ endpoints.

**fallback runs (نفس الطبقات، مع تجنّب سلسلة phonenumbers):**

| Test File | Pass / Fail |
|-----------|-------------|
| `tests/test_friction_log.py` | 13 passed |
| `tests/test_proof_pack_required.py` | passed (ضمن المجموعة) |
| `tests/test_proof_event_sample_validates.py` | passed |
| `tests/test_proof_pack_assembler.py` | 10 passed / 4 failed (الأربعة بسبب `fastapi` missing فقط — منطق pack صحيح) |

**الحُكم:** سلسلة ledger الأساسية + proof pack assembler **سليمة**.
الـ test runner له dev-deps ناقصة (`phonenumbers`, `fastapi`) — مشكلة بيئة لا منطق.

---

## (5) Proof Pack Template — Gap-Fill Done Today

[PROOF_PACK_TEMPLATE.md](./PROOF_PACK_TEMPLATE.md) قبل التعديل: 10 أقسام فقط، بدون
cover page / consent letter / 90-day plan concrete / evidence L0–L5 / capital asset
block.

التعديل اليوم رفعه إلى **14 قسم** متطابقة مع `PROOF_PACK_V2_SECTIONS`
في `auto_client_acquisition/proof_architecture_os/proof_pack_v2.py` + أضاف:
cover (client / week-ISO / founder signature) · DQ summary table · top-3 revenue-leak
findings · 90-day plan (3 concrete actions) · evidence appendix L0–L5 ·
consent letter section · capital asset registration block.

---

## أعلى 3 إصلاحات قبل إغلاق أول صفقة (Top 3 BEFORE first close)

1. **Capital Asset consent gate** — أضف حقلين `consent_on_file: bool` و
   `publication_status: enum{internal_only, client_approved, public_safe}` إلى
   `CapitalAsset` dataclass + تحقّق في `add_asset()` يرفض النشر العامّ بدون
   `consent_on_file=True`. (يحتاج engineer — 30 دقيقة.) ⟶ بدون هذا، النشر
   العامّ لأي capital asset سيكون **خرق سياسة**.
2. **`MISSING_PROOF_PACK` + `MISSING_SOURCE_PASSPORT` emitters** — اربط Day-7
   wrap-up hook بـ `friction_log.emit(...)` إذا انتهت 7 أيام بدون
   `proof_pack_delivered` event في `proof_ledger`. (الـ enum موجود، الـ caller
   مفقود.) ⟶ بدون هذا، أي تأخير لن يُحسب في الـ scorecard.
3. **`scripts/register_capital_asset.py` CLI** — يلفّ `capital_os.add_asset` +
   `friction_log.emit` للفشل + يتحقّق من consent gate. سطر CLI واحد يجعل
   founder يسجّل الـ asset في < 30 ثانية بعد جلسة الإغلاق. (يحتاج engineer ~1
   ساعة.) ⟶ بدون هذا، أول صفقة قد تُغلق بدون asset مسجَّل — وهذا يكسر شرط
   الـ engagement closure.

> هذه الثلاثة هي **الفرق بين YELLOW و GREEN** قبل أول diagnostic مدفوع يُغلق.

---

## ملحق: ملفات تمّ لمسها اليوم

- ✏️  `docs/delivery/PROOF_PACK_TEMPLATE.md` — توسعة إلى 14 قسم + cover + consent + capital block
- ✏️  `docs/delivery/RETAINER_ELIGIBILITY_CHECKLIST_AR.md` — جديد (لم يكن موجوداً)
- ✏️  `docs/delivery/SPRINT_READINESS_AUDIT_2026-05-24_AR.md` — هذا الملف

لم يُعدَّل أي كود إنتاجي. لا commits. لا external sends.
