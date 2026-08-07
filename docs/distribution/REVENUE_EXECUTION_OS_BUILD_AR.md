# Revenue Execution OS — ما تم بناؤه + الخارطة + الفريق + التشغيل

هذه الوثيقة هي فهرس التنفيذ لطبقة **Revenue Execution OS** (التوزيع): ما شُحن في
هذه الدفعة، خارطة الـ PRs، فريق الوكلاء وصلاحياتهم، التشغيل اليومي، وخطة E2E.

المرجع المفاهيمي: [REVENUE_EXECUTION_OS_AR.md](REVENUE_EXECUTION_OS_AR.md).

---

## 0) قرار مهم — مصدر الحقيقة للأسعار (Pricing reconciliation)

الخطة الأصلية اقترحت أسعاراً تقريبية (Diagnostic 1.5k–5k، Follow-up 8k–18k…).
المستودع **عنده مصدر حقيقة قائم بالفعل**، فاعتمدناه بدل اختراع أسعار جديدة (التزاماً
بقاعدة الخطة: «لا تترك agent يخترع عرض أو سعر»):

- **كود مصدر الحقيقة:** [`autonomous_growth/product_catalog.py`](../../autonomous_growth/product_catalog.py) — السلّم الخماسي: Free Diagnostic (0) → Sprint (499) → Data Pack (1,500) → Managed Ops (2,999–4,999/شهر) → Custom AI (5,000–25,000).
- **عقود مصدر الحقيقة:** [`DEALIX_REVOPS_PACKAGES_AR.md`](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) — Diagnostic (3,500) → Lead Intelligence Sprint (9,500) → Pilot (22,000) → RevOps OS (15k–25k/شهر) → Enterprise (85k+).

`distribution_os.catalog` يقرأ من `product_catalog.py` ولا يخترع أي سعر. **إن أراد
المؤسس اعتماد أرقام الخطة، يُعدَّل `product_catalog.py` في مكان واحد** فينعكس على
كل المقترحات وتسليمات الدفع تلقائياً.

---

## 1) ما تم بناؤه (File inventory)

### الوحدة الأساسية — `auto_client_acquisition/distribution_os/`
طبقة تنسيق تُعيد استخدام `governance_os` / `proof_os` / `sales_os` / `payment_ops`
والكتالوج القائم، ولا تملك أي قدرة إرسال خارجي.

| ملف | الدور |
|-----|-------|
| `_store.py` | مخزن JSONL مشترك (نمط `value_ledger`/`renewal_scheduler`) + `DEALIX_*_PATH` |
| `catalog.py` | سطح الكتالوج (لا أسعار جديدة) + سلّم + `next_rung`/`price_band` |
| `prospect.py` | دورة حياة المؤهَّل + بوابة التأهيل (12 حالة) |
| `draft_factory.py` | مصنع المسودات (11 نوعاً، قوالب AR/EN) — **لا دالة إرسال** |
| `draft_quality.py` | بوابة الجودة (claims/قناة/طول/PII) → `governance_status` |
| `followup.py` | محرّك المتابعة (Day 0/2/4/7) + قائمة المستحق |
| `proposal.py` | مصنع المقترحات (مربوط بالكتالوج + بوابة موافقة) |
| `proof_pack.py` | حزمة إثبات + مستويات أدلة L0–L5 |
| `payment_handoff.py` | تسليم دفع (6 موافقات) — **لا شحن** |
| `delivery_handoff.py` | تسليم ما بعد البيع (scope/metric/owner) |
| `renewal.py` | يعيد استخدام `renewal_scheduler` + سلّم الـ upsell |
| `win_loss.py` | تعلّم الفوز/الخسارة + أسئلة الأسبوع |
| `metrics.py` | مقاييس يومية + أسبوعية (قراءة فقط) |

### السطح الخارجي
- **API:** [`api/routers/distribution.py`](../../api/routers/distribution.py) — 19 مساراً تحت `/api/v1/distribution/*`، كل استجابة فيها `governance_decision`، **بدون أي مسار إرسال/شحن**.
- **Schemas:** [`schemas/`](../../schemas/) — 9 مخططات JSON Schema (تطابق الـ dataclasses).
- **Scripts:** `scripts/check_draft_quality.py` · `scripts/distribution_metrics.py` · `scripts/distribution_day.py` · `scripts/agent_security_gate.py`.
- **Makefile:** `make distribution-day` · `make draft-quality` · `make distribution-metrics`.
- **Workflows:** `distribution_quality_gate.yml` · `agent_security_gate.yml` · `distribution_draft_day.yml` · `distribution_weekly_review.yml` (كلها least-privilege `contents: read`).
- **n8n:** [`integrations/n8n/distribution_blueprint.json`](../../integrations/n8n/distribution_blueprint.json) (`active: false`).
- **Tests:** `tests/test_distribution_os_*.py` · `tests/test_distribution_api.py` · `tests/test_agent_security_gate.py`.
- **Docs:** `docs/commercial/PRODUCT_CATALOG_AR.md` + `OFFER_LADDER_AR.md` + `PRICING_GUARDRAILS_AR.md` + `APPROVAL_POLICY_AR.md` · `docs/distribution/*` (15 وثيقة) · `docs/sectors/*` (10 قطاعات + فهرس) · `docs/delivery/DELIVERY_HANDOFF_AR.md` · `docs/references/REVENUE_EXECUTION_REFERENCE_LIBRARY.md`.

---

## 2) خارطة الـ PRs (Roadmap status)

| PR | المحتوى | الحالة في هذه الدفعة |
|----|---------|----------------------|
| 1 | Commercial source of truth | ✅ docs/commercial |
| 2 | Sector playbooks | ✅ docs/sectors (10) |
| 3 | Prospect OS | ✅ `prospect.py` + schema + example |
| 4 | Draft Factory | ✅ `draft_factory.py` |
| 5 | Draft Quality Gate | ✅ `draft_quality.py` + `check_draft_quality.py` |
| 6 | Follow-up Engine | ✅ `followup.py` |
| 7 | Proposal + Proof | ✅ `proposal.py` + `proof_pack.py` |
| 8 | Payment + Delivery + Renewal | ✅ `payment_handoff.py` + `delivery_handoff.py` + `renewal.py` |
| 9 | Metrics + Win/Loss | ✅ `metrics.py` + `win_loss.py` |
| 10 | Workflows | ✅ 4 workflows + agent security gate |
| 11 | Distribution API | ✅ `api/routers/distribution.py` |
| 12 | Founder Revenue Control Room UI | 📄 Spec جاهز ([FOUNDER_REVENUE_CONTROL_ROOM_AR.md](FOUNDER_REVENUE_CONTROL_ROOM_AR.md)) — البناء يتبع الـ API |
| 13 | n8n external automation | ✅ blueprint (`active:false`) + README |
| 14 | E2E | ✅ API schema tests + خطة Playwright (أدناه) |

---

## 3) فريق الوكلاء وصلاحياتهم (Agent team — §22)

التوثيق فقط؛ التنفيذ يتم عبر الوحدات أعلاه والبوابات. لا وكيل يرسل خارجياً.

| Agent | يكتب في | يرسل خارجياً؟ | يحتاج موافقة؟ |
|-------|---------|:---:|:---:|
| Revenue Commander | تقارير | لا | لا |
| Sector Prioritization | docs/data | لا | لا |
| Prospect Scoring | prospects | لا | لا |
| Draft Factory | drafts | لا | **نعم** |
| Draft Quality Guard | تقارير | لا | لا |
| Follow-up | followups | لا | **نعم** |
| Proposal | proposals | لا | **نعم** |
| Proof Pack | proof packs | لا | **نعم** |
| Payment Handoff | handoffs | لا | **نعم** |
| Delivery Handoff | onboarding | لا | **نعم** |
| Renewal | renewals | لا | **نعم** |
| Win/Loss | تقارير | لا | لا |
| Distribution Metrics | تقارير | لا | لا |
| Agent Security Reviewer | تقارير/فحص workflows | لا | نعم للتغييرات الحساسة |

الوكلاء المتخصّصون الموجودون في الريبو ([`.claude/agents/`](../../.claude/agents/)):
`dealix-pm` · `dealix-engineer` · `dealix-content` · `dealix-sales` · `dealix-delivery`.

---

## 4) التشغيل اليومي (§24)

```bash
make doctor                 # صحة البيئة
make distribution-day       # أمر اليوم → reports/distribution/DISTRIBUTION_DAY.md
make draft-quality          # بوابة الجودة → DRAFT_QUALITY_GATE.md
make distribution-metrics   # المقاييس → DISTRIBUTION_METRICS.md
```

ثم القرار اليومي: Approve/Reject/Needs-edit للمسودات، Mark-copied بعد الإرسال
اليدوي، تابع المؤهّلين، ولّد المقترحات وحزم الإثبات، جهّز تسليم الدفع.

---

## 5) خطة E2E (§14)

- **مُنفّذ الآن:** اختبارات API بالـ schema/سلوك في `tests/test_distribution_api.py`
  (تدفّق approval-first: prospect → draft → approve → mark-copied؛ بوابة تسليم الدفع؛
  رفض المنتج خارج الكتالوج؛ لا مسار إرسال/شحن).
- **Playwright (عند بناء الواجهة):** سيناريو «approval-first»: فتح
  `/[locale]/ops/revenue-control` → ظهور مسودة `pending_approval` → الضغط Approve →
  Mark-copied → التأكد من **عدم وجود زر Send** ومن أن مسودة `blocked` لا تُوافَق.
  يتبع نمط [`playwright_smoke.yml`](../../.github/workflows/playwright_smoke.yml).

---

> العقيدة (الـ 11 غير قابلة للتفاوض) مفروضة باختبارات: لا إرسال خارجي في v1، لا واتساب
> بارد، لا أتمتة لينكدإن، لا scraping، كل المسودات بانتظار الموافقة، لا ضمانات، لا PII
> في السجلات، أدلة L0–L5، كل عرض مربوط بمنتج من الكتالوج، لا نشر إنتاج، لا أسرار مكشوفة.
