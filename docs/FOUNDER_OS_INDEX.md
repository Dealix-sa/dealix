# Dealix Founder OS — Index / فهرس نظام تشغيل المؤسس

> خريطة واحدة تربط Dealix كـ **نظام تشغيل مؤسس** بالأصول الموجودة فعلًا في الريبو
> (سكربتات، وثائق، workflows، وAPI). هذه الوثيقة **إضافية ولا تكرّر** الدستور — للدستور
> التشغيلي ارجع لـ [`AGENTS.md`](../AGENTS.md)، وللأمان [`SECURITY.md`](../SECURITY.md).
>
> A single map tying Dealix-as-a-Founder-OS to assets that **already exist** in the repo.
> This file is additive and does **not** duplicate doctrine — see [`AGENTS.md`](../AGENTS.md).

**Status:** additive layer · **Owner:** founder · **Last reviewed:** 2026-06-02

---

## 1) لماذا هذا الملف / Why this exists

الريبو يحتوي **393 سكربت تشغيلي** و**50+ workflow** وعشرات وثائق `docs/commercial`. القوة موجودة،
لكن المؤسس يحتاج **مدخلًا واحدًا**: "وش أشغّل، ومتى، ووين الوثيقة." هذا الملف هو ذلك المدخل.

The power already exists; this index is the one front door: *what to run, when, and where the doc lives.*

---

## 2) الوكلاء الستة → الأصول الحالية / The six agents → existing assets

نموذج "6 وكلاء" من خطة المؤسس، **مربوط بما هو منفّذ فعلًا** (لا إنشاء مكرر):

| الوكيل / Agent | المخرج اليومي / Daily output | يعيش في / Lives in (verified paths) |
| --- | --- | --- |
| **Founder Chief of Staff** | أولويات اليوم + المقاييس الخمسة | `scripts/dealix_founder_daily_brief.py` · `scripts/founder_daily_five_metrics.py` · `scripts/founder_cadence.sh` · `reports/company_os/daily/CEO_BRAIN_TODAY.md` |
| **Revenue Agent** | فرص + رسائل + عروض | `scripts/run_founder_revenue_day.sh` · `scripts/run_founder_commercial_day.sh` · `docs/POSITIONING_AND_ICP.md` · `docs/V7_FIRST_10_WARM_OUTREACH_PACK.md` · `scripts/warm_list_outreach.py` · `ledgers/prospects.json` |
| **Product Agent** | PRs صغيرة قابلة للاختبار | `api/` · `frontend/` · `tests/` · دليل البنية في [`AGENTS.md`](../AGENTS.md) §"Repo anatomy" |
| **QA / Security Agent** | بوابات CI + فحص أسرار | `.github/workflows/ci.yml` · `.github/workflows/security.yml` · `.github/workflows/codeql.yml` · `scripts/check_env_contract.py` · `scripts/security_smoke.py` |
| **Market Research Agent** | تموضع + قطاعات | `docs/commercial/MARKET_INTELLIGENCE_MASTER_INDEX_AR.md` · `docs/SECTOR_PLAYBOOKS.md` · `docs/POSITIONING_AND_ICP.md` |
| **Delivery Agent** | تسليم متكرر بلا فوضى | `docs/PILOT_DELIVERY_SOP.md` · `docs/ONBOARDING_FLOW.md` · `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` · `ops/founder-ceo-os/` |

> الخلاصة: خطة "الوكلاء الستة" **ليست عملًا جديدًا** — هي عدسة فوق نظام قائم. هذا الفهرس يوصّلك للأصل مباشرة.

---

## 3) المسارات التجارية → أين تعيش / Business tracks → where they live

| Track | Where it lives (verified) |
| --- | --- |
| Revenue Engine | `docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md` · `docs/commercial/FOUNDER_SALES_PLAYBOOK_AR.md` · API `GET /api/v1/revenue-os/catalog` |
| Offer ladder & pricing | `docs/OFFER_LADDER_AND_PRICING.md` · `docs/pricing.md` · `os/03_OFFERS.yml` |
| Outreach (draft-only) | `docs/V7_FIRST_10_WARM_OUTREACH_PACK.md` · `data/templates/warm_intro_whatsapp_ar.md` · `scripts/warm_list_outreach.py` |
| Objection handling | `docs/OBJECTION_HANDLING_V6.md` · `auto_client_acquisition/revenue_graph/objection_library.py` |
| Client delivery | `docs/PILOT_DELIVERY_SOP.md` · `docs/SALES_OPS_SOP.md` · `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` |
| Compliance & Security | `SECURITY.md` · `docs/SECURITY_RUNBOOK.md` · `scripts/check_env_contract.py` |
| Founder reporting | `scripts/founder_weekly_metrics_bundle.py` · `reports/company_os/` · `ledgers/` |
| Decision quality | API `GET /api/v1/decision-passport/golden-chain` · `GET /api/v1/business-now/snapshot` |

---

## 4) الإيقاع / Cadence — الأوامر الحقيقية / the real commands

> هذه أوامر **موجودة في الريبو**. لِما لا يعمل عندك مباشرة راجع متطلبات البيئة في [`AGENTS.md`](../AGENTS.md).

### يوميًا — صباح / Morning
```bash
bash scripts/run_founder_commercial_day.sh     # الحركة التجارية الصباحية (canonical)
python3 scripts/founder_daily_five_metrics.py  # المقاييس الخمسة
python3 scripts/dealix_founder_daily_brief.py   # موجز المؤسس
```

### يوميًا — إيراد / Revenue day
```bash
bash scripts/run_founder_revenue_day.sh        # commercial + business-now
```

### أسبوعيًا / Weekly
```bash
bash scripts/founder_weekly_loop.sh            # بوابات الأحد
bash scripts/founder_cadence.sh                # morning / evening / weekly
```

### حواجز قبل أي PR / Guardrails before any PR
```bash
ruff check .
black --check .
APP_ENV=test pytest -q --no-cov                # أو حزمة الانحدار السريعة في AGENTS.md
python3 scripts/check_env_contract.py
python3 scripts/security_smoke.py
python3 scripts/check_ledgers.py               # سجلات المؤسس (هذه الطبقة)
```

### بوابات الإطلاق / Launch gates
```bash
bash scripts/verify_dealix_commercial_go_live.sh   # يطبع DEALIX_OFFICIAL_LAUNCH_VERDICT
bash scripts/revenue_os_master_verify.sh           # يطبع DEALIX_REVENUE_OS_VERDICT
bash scripts/dealix_capability_verify.sh
bash scripts/production_smoke.sh
```

---

## 5) السجلات / Ledgers

طبقة خفيفة لتتبّع القرارات والوقائع بصيغة قابلة للتحقق — تفاصيلها في [`ledgers/README.md`](../ledgers/README.md):

| Ledger | غرضه |
| --- | --- |
| `ledgers/prospects.json` | خط أنابيب الفرص (يبدأ فارغًا — لا اختلاق) |
| `ledgers/deals.json` | الصفقات بالريال (المؤسس فقط) |
| `ledgers/experiments.json` | حلقة التعلّم: فرضية + مقياس |
| `ledgers/risks.json` | سجل المخاطر |

محميّة بـ `python3 scripts/check_ledgers.py` و `tests/test_ledgers_schema.py` (داخل بوابة `pytest` الحالية).

---

## 6) الحوكمة / Governance (لا تكرار — إحالة فقط)

- **الدستور التشغيلي:** [`AGENTS.md`](../AGENTS.md) — أوامر التطوير، البيئة، ما لا يُعاد تشخيصه كأخطاء.
- **الأمان والأسرار:** [`SECURITY.md`](../SECURITY.md) · [`docs/SECURITY_RUNBOOK.md`](SECURITY_RUNBOOK.md) · `.gitleaks.toml` · `.secrets.baseline`.
- **تشغيل الوكيل البرمجي:** [`docs/CLOUD_CODE_COMMAND_CENTER.md`](CLOUD_CODE_COMMAND_CENTER.md).

---

## 7) "وش أشغّل لـ…" / Quick lookup

| أبي… / I want to… | شغّل / Run |
| --- | --- |
| أعرف أولويات اليوم | `python3 scripts/dealix_founder_daily_brief.py` |
| أجهّز يوم إيراد | `bash scripts/run_founder_revenue_day.sh` |
| أتأكد ما فيه تسريب أسرار | `python3 scripts/security_smoke.py` |
| أتحقق من عقد البيئة | `python3 scripts/check_env_contract.py` |
| أتحقق جاهزية الإطلاق التجاري | `bash scripts/verify_dealix_commercial_go_live.sh` |
| أتحقق من السجلات | `python3 scripts/check_ledgers.py` |
| أفهم بنية الكود | [`AGENTS.md`](../AGENTS.md) §"Repo anatomy" |

---

## 8) ما الذي أضافته هذه الطبقة / What this additive layer added

أُضيف فقط ما كان **ناقصًا فعلًا** — بدون لمس `AGENTS.md` أو `README` أو `ci.yml`:

- `docs/FOUNDER_OS_INDEX.md` (هذا الملف) — الخريطة الموحّدة.
- `docs/CLOUD_CODE_COMMAND_CENTER.md` — دليل تشغيل الوكيل البرمجي بالأوامر الحقيقية.
- `ledgers/` — سجلات + schemas + validator + اختبار CI.

> أي بند آخر في خطة "Founder OS" كان **منفّذًا مسبقًا** بصيغة أرقى؛ هذا الفهرس يوصّلك له بدل إعادة إنشائه.
