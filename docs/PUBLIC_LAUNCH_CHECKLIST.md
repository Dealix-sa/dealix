# قائمة التدشين التجاري العام — Dealix · Public Commercial Launch Checklist

> آخر تحقّق: **2026-05-28** · فرع `claude/commercial-launch-prep-a2kJT` · commit `646129d` · حُكم رسمي: **`DEALIX_OFFICIAL_LAUNCH_VERDICT=FAIL`** (تفاصيل أدناه)
> Last verification: see `docs/LAUNCH_EXECUTION_LOG.md` for the full execution log; raw evidence in `docs/launch-evidence/2026-05-28/`.

علامة الحالة: ✅ مُثبَّت بدليل · 🟡 مُنفَّذ ولكن دليلٌ ناقص أو مشروط · ⛔ حاجز قبل الإطلاق · ⏸ خارج النطاق التقني (يتطلب فعلًا بشريًا)

---

## قانوني · Legal

- 🟡 سياسة خصوصية منشورة — موجودة في `docs/legal/` و landing/legal؛ يحتاج تحقّق رابط عام مباشر بعد نشر `dealix.me`
- 🟡 شروط استخدام — موجودة في `docs/legal/TERMS_*`؛ نفس ملاحظة الرابط العام
- 🟡 DPA للشركات — قالب موجود في `docs/legal/dpa/`؛ يحتاج توقيع لكل عميل
- ✅ إجراءات PDPL (تصدير/حذف/قمع) موثقة ومُختبرة — `dealix/registers/no_overclaim.yaml` + tests/governance/ (passing). دليل: `docs/launch-evidence/2026-05-28/16_pytest_11_non_negotiables.txt`

## منتج · Product

- ✅ صفحة تسعير عامة متسقة مع `pricing.py` و`PRICING_STRATEGY.md` — `frontend/src/app/[locale]/pricing/` + `docs/OFFER_LADDER_AND_PRICING.md`. 7 عروض حية. دليل: `docs/launch-evidence/2026-05-28/14_run_founder_commercial_day.txt` (`DEALIX_GTM_STACK_VERDICT=PASS`)
- ✅ Onboarding self-serve أو مبيعات داخلية قابلة للتكرار — Sprint 499 SAR موجود orchestrator كامل 10 خطوات (`auto_client_acquisition/delivery_factory/delivery_sprint.py`)
- 🟡 حدود استخدام واضحة (rate limits، quotas) — `slowapi` مفعّل في `api/main.py`؛ لكن لا quotas مُنفّذة لكل rung (P2 polish)

## فوترة · Billing

- ⏸ Moyasar live + webhooks مراقَبة — sandbox فقط حاليًا؛ يتطلّب live cutover: `docs/MOYASAR_LIVE_CUTOVER.md`. دليل: `docs/launch-evidence/2026-05-28/11_founder_weekly_metrics_bundle.txt` يُظهر `moyasar_live` red في Truth Matrix (المتوقَّع).
- 🟡 فواتير واسترداد محددة — قوالب ZATCA موجودة (`integrations/zatca.py`); ينتظر sandbox→live

## تشغيل · Operations

- ✅ SLOs (uptime، زمن استجابة API) — `docs/SLO.md` + `/api/v1/transformation/kpi-snapshot` يبثّ metrics
- ✅ on-call + runbooks — `docs/ops/DEPLOY_NOW.md`, `docs/ops/LAUNCH_OPERATOR_RUNBOOK.md`, `docs/ops/FOUNDER_GO_LIVE_DAY0_AR.md`, `docs/ON_CALL.md` كلها حاضرة وموثّقة
- ✅ نسخ احتياطي واختبار استعادة — `docs/ops/BACKUP_RESTORE.md` + `scripts/docker_host_backup.sh`

## GTM

- ✅ مسار «أول 100» من `docs/GTM_PLAYBOOK.md` — `/api/v1/business/gtm/first-10` و `first-100` حيّة. دليل: `14_run_founder_commercial_day.txt`
- ✅ شراكات وكالة إن انطبقت — `partnership_os` + Referral Wave 14D.1 (`auto_client_acquisition/partnership_os/referral_store.py`)

## معيار «جاهز للإطلاق العام» · Public Launch Ready Criteria

- 🟡 تجربة pilot ناجحة متكررة — Sprint orchestrator كامل + 13 إصدار alembic؛ ينتظر أول 3 pilots موقّعين عمليًا
- ⛔ CI أخضر على `main` — حُكم اليوم: 3 ثغرات جراحية صغيرة تمنع `PASS`:
  1. `frontend/src/lib/opsAdmin.ts` مفقود → `npm run build` يفشل
  2. `dealix/commercial_ops/paths.py` ينقص ثابتين → اختبار يُجمع بخطأ
  3. `tests/test_founder_commercial_digest.py::test_scope_requested_within_days` تاريخ ثابت قديم
  تفاصيل في `docs/LAUNCH_EXECUTION_LOG.md` · الإصلاحات المقترَحة هناك.
- ⏸ مراجعة أمنية خارجية (موصى بها) — قرار المؤسس

---

## بوّابات تقنية أُثبتت بأدلة في هذا التشغيل · Technical gates with captured evidence

| البوّابة | الحُكم | الدليل |
|---|---|---|
| Single Alembic head | `OK (013)` | `02_check_alembic_single_head.txt` |
| Founder Operating System | `PASS` | `01_verify_dealix_commercial_go_live.txt` |
| Founder Strongest Plan (138 tasks) | `PASS` | `08_founder_strongest_plan_status.txt` |
| Daily Ops (dry-run) | `READY` | `13_run_dealix_daily_ops_dryrun.txt` |
| GTM Public Surfaces | `PASS` | `01_verify_dealix_commercial_go_live.txt` |
| Founder Commercial Day | `OK` | `14_run_founder_commercial_day.txt` |
| GTM Stack | `PASS` | `14_run_founder_commercial_day.txt` |
| Full Autonomous Ops Stack | `PASS` | `14_run_founder_commercial_day.txt` |
| Commercial Value Map | `OK` | `10_commercial_value_map_status.txt` |
| CTO Weekly Anchor | `OK` | `12_run_cto_weekly_anchor.txt` |
| Business NOW | `OK` | `12_run_cto_weekly_anchor.txt` |
| Commercial FE/BE smoke (4 endpoints 200) | `PASS` | `01_verify_dealix_commercial_go_live.txt` |
| 11 non-negotiables (73 / 75 + 2 skipped) | substantial pass | `16_pytest_11_non_negotiables.txt` |

## بوّابات FAIL مع جذر السبب · FAIL gates with root cause

| البوّابة | الحُكم | الجذر | التصنيف |
|---|---|---|---|
| `DEALIX_OFFICIAL_LAUNCH_VERDICT` | FAIL | ينحدر من 3 الإصلاحات الجراحية | بلوكر تقني صغير |
| `OFFICIAL_LAUNCH_VERDICT` | FAIL | `fe_build: FAIL` (`@/lib/opsAdmin` مفقود) | بلوكر تقني |
| `COMPANY_READY_VERDICT` | FAIL | اختبار تاريخ ثابت قديم | فيكسرة بايتة |
| `MARKET_LAUNCH_READY` | BLOCKED | `FORBIDDEN_CLAIMS` + `NO_LINKEDIN_SCRAPER` strings | دين عقيدة، يُحلّ بمراجعة landing |
| `make prod-verify` (security-smoke) | FAIL | يكتشف `sk_live_*` في فيكسرات اختبار متعمَّدة | إيجابي كاذب |
| `FOUNDER_WEEKLY_METRICS_VERDICT` | BLOCKED | Truth Matrix يحتاج credentials حيّة (Moyasar live, WhatsApp, Gmail) | متوقَّع: نطاق المؤسس |
| Frontend `npm run build` | FAIL | `frontend/src/lib/opsAdmin.ts` غير ملتزم في git (history فارغ) | بلوكر تقني |

---

## التحقّق من إكمال هذه القائمة

```bash
# إعادة إنتاج الحُكم
APP_ENV=test bash scripts/verify_dealix_commercial_go_live.sh
# المتوقَّع بعد الإصلاحات الـ3: DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS
```

سجل التنفيذ القانوني: [`docs/LAUNCH_EXECUTION_LOG.md`](LAUNCH_EXECUTION_LOG.md)
حزمة الأدلة الكاملة: [`docs/launch-evidence/2026-05-28/`](launch-evidence/2026-05-28/)
