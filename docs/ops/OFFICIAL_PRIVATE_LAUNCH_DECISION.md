# Dealix — Official Private Launch Decision / قرار الإطلاق الخاص الرسمي
<!-- PHASE: Launch | Owner: Founder | Date: 2026-06-07 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** لا إطلاق عام قبل إثبات مدفوع. لا ضمانات. لا ادعاءات مبالغ فيها.
> Estimated outcomes are not guaranteed outcomes — النتائج التقديرية ليست نتائج مضمونة.

> **نطاق هذه الوثيقة:** قرار موثّق بالأدلة لإغلاق الإطلاق *الخاص*. لا تستبدل بوّابة
> `docs/ops/COMMERCIAL_GO_LIVE_GATE.md` ولا `docs/ops/GO_LIVE_CHECKLIST_AR.md` — بل تُلخّص
> الحالة الحقيقية وتربط بهما. كل "أخضر" أدناه شُغّل فعليًا؛ كل "خارجي" لا يُكمله إلا
> المؤسس في لوحة المزوّد. This is an evidence-backed decision record; it links to —
> does not replace — the existing go-live gate and checklist.

---

## 1. الحكم / Verdict

| القرار / Decision | الحالة / Status | الشرط / Condition |
|---|---|---|
| **Private Launch** (ديمو خاص + تشخيص + Sprint مدفوع بموافقة) | **NO-GO الآن → GO بعد §4 + §5** | إغلاق `make security-smoke` + إكمال خطوات المؤسس |
| **Public Launch** (إطلاق عام / mass) | **NO-GO** | لا إطلاق عام قبل أول Proof Pack مدفوع + أدلة إنتاج |

السبب المباشر لكون Private Launch "NO-GO الآن": البوّابة الحتمية `make security-smoke`
حمراء على `main` (تفاصيل §3 و§3.1)، وعدد من الخطوات أسرار/قرارات مؤسس خارج الريبو (§4).

---

## 2. تصحيحات على خطة الإغلاق الملصقة / Corrections to the pasted runbook

الخطة الأصلية كُتبت دون سياق الريبو. التحقّق المباشر أظهر ثلاثة فروقات تغيّر القصة الصادقة:

1. **`/healthz` لم يُحذف.** لا يزال alias حيًّا في `api/routers/health.py` (يدعم `?deep=1`)،
   و`railway.json` لا يزال يستخدم `/healthz` كمسار healthcheck. PR #650 ينقل **صفحات الـ
   landing الثلاث فقط** من `/healthz` إلى `/health` + `/health/deep`. القناة الصحيحة للـ
   smoke الخارجي تبقى `/health` و`/health/deep`.
2. **PR #638 و#650 كلاهما `draft` وحالتهما `mergeable_state: "unstable"`** — أي لا تعارض دمج
   (`mergeable: true`) لكن فحوص CI ليست كلها خضراء. "mergeable" ≠ "checks green".
3. **PR #650 يوثّق قرار P0 معلّق للـ money-safety:** الـ rung-0 Free Diagnostic
   (`amount_halalas == 0`) يصطدم مع invariant "كل الخطط موجبة الحساب". هذا يمنع CI الأخضر
   بالكامل ويحتاج **قرار مؤسس**، لا تعديل اختبار.

---

## 3. الأدلة — بوّابات شُغّلت محليًا / Evidence — gates run locally (base `7bd43c3`)

| البوّابة / Gate | الأمر / Command | النتيجة / Result | الطبيعة / Nature |
|---|---|---|---|
| Env contract | `make env-check` | ✅ PASS (exit 0) | حقيقي — verified locally |
| Security smoke | `make security-smoke` | ❌ FAIL | **حقيقي / REAL — يُغلقه المؤسس (§3.1)** |
| Alembic single head | `make alembic-heads` | ⚠️ لم يُشغّل محليًا | بيئي — alembic CLI غير مثبّت بالـ sandbox؛ يمر في CI |
| Doctor (مركّب) | `make doctor` | ❌ FAIL | مركّب — يفشل عند alembic-heads (بيئي) ثم security-smoke (حقيقي) |
| API contract | `make api-contract-check` | ⚠️ لم يُشغّل محليًا | بيئي — `fastapi` غير مثبّت بالـ sandbox؛ يمر في CI |
| Prod verify (مركّب) | `make prod-verify` | ❌ FAIL | مركّب — العائق الملزِم security-smoke؛ يحتاج كامل الاعتماديات |
| Doctrine-guard battery | `pytest tests/test_no_*.py …` | ⚠️ يُشغّل في CI | على `main` حارس تسرّب الأسرار (pytest) أحمر — يعالجه PR #650 (الجانب pytest فقط) |
| In-process API smoke | `python scripts/smoke_inprocess.py` | ⚠️ يُشغّل في CI | بيئي — `fastapi` غير مثبّت؛ PR #650 أثبت `/health` 200 |

ملاحظة صدق: البوّابات الموسومة "بيئي" تفشل هنا فقط لغياب اعتماديات الـ sandbox (لا Postgres،
لا fastapi، لا alembic CLI) — وتمر في CI. العائق **الوحيد غير-البيئي وغير-المُعالَج بالـ PRs
المعلّقة** هو `make security-smoke`.

### 3.1 عائق security-smoke — تفصيل دقيق / The security-smoke blocker

`make security-smoke` يشغّل `scripts/security_smoke.py` (حارس "خفيف")، وهو **آلية مختلفة** عن
حارس pytest `tests/test_v7_secret_leakage_guard.py` الذي يعدّله PR #650. لذلك **حتى بعد دمج
#650 سيبقى `make security-smoke` أحمر** ما لم يُعالَج هذا الحارس تحديدًا. الفشل حقيقي وقابل
لإعادة الإنتاج، من فئتين:

1. **ملفات env قوالب مُتعقَّبة في git:** `.env.prod.example`, `.env.staging.example`,
   `.env.railway.example`. السكربت (الأسطر 86–92) يمنع أي `.env*` عدا `.env.example` بالضبط.
2. **مطابقات بادئة أسرار في تجهيزات اختبار/وثائق/سكربتات** (بادئات مفاتيح الدفع الحيّة، ورموز
   GitHub، ومفاتيح Google/AWS — أسماء البادئات محذوفة هنا عمدًا حتى لا تُطابِق الحارس نفسه) —
   قيم وهمية/placeholder تحقّق منها PR #650 سطرًا-سطرًا للحارس المكافئ في pytest، لكن قائمة
   السماح الخشنة في `security_smoke.py` (الأسطر 55–61، علامات `REPLACE`/`example`/`placeholder`/
   `test-`/`CHANGE_ME` فقط) لا تلتقطها.

**توصية إصلاح آمنة (قرار مؤسس — خارج نطاق هذه الحزمة):** إمّا (أ) مزامنة قائمة السماح في
`scripts/security_smoke.py` مع منطق المسار في حارس pytest، أو (ب) نقل القوالب env إلى `docs/`
أو `.gitignore`. لم تُنفَّذ هنا لأن تعديل حارس أمني / حذف ملفات مُتعقَّبة قرار حسّاس
(doctrine: surface-don't-delete) ويخص محيط الحوكمة المُسلَّم للمؤسس.

---

## 4. عوائق يملكها المؤسس فقط / Founder-only blockers (NOT automatable)

أسرار / مال / قرارات GitHub-UI لا يجوز لوكيل تنفيذها. متتبَّعة كـ **#467–#471** (انظر PR #650 §4).

- [ ] **ترتيب الدمج:** ادمج `#638` أولًا (يضيف `claude-code.yml` + `CLAUDE.md` → يفعّل Claude Code)،
      ثم أضِف السر **`ANTHROPIC_API_KEY`** (Settings → Secrets → Actions)، ثم `#650`.
  - تحذير: كلاهما `draft` + CI `unstable`. #638 يُظهر 9 ملفات / 427 حذفًا مقابل وصف "ملفّين" —
    راجع الـ diff كاملًا قبل الدمج.
  - تحذير: #650 يترك قرار **free-tier money-safety (P0)** مفتوحًا (rung-0 = 0 ريال مقابل "كل
    الخطط موجبة"). احسم موضع الـ free-tier وزامِن `tests/test_billing_amounts.py` +
    `tests/test_billing_moyasar_safety.py` قبل أن يصير CI أخضر بالكامل.
- [ ] **إغلاق `make security-smoke`** حسب §3.1 (قرار مؤسس على محيط الحوكمة).
- [ ] **الأسرار** (GitHub Secrets، لا ملفات): قائمة P1–P6 في `docs/ops/PRODUCTION_ENV_TEMPLATE.md`
      (`DATABASE_URL`, `APP_SECRET_KEY`, `ADMIN_API_KEYS`, `MOYASAR_SECRET_KEY`,
      `MOYASAR_WEBHOOK_SECRET`, `REDIS_URL`, ومفتاح LLM واحد على الأقل).
- [ ] **حماية main + Environments:** طبّق حسب `docs/ops/CI_PERMISSIONS_AND_BRANCH_PROTECTION.md`.
- [ ] **DNS/TLS** لـ `api.dealix.me` متحقَّق في لوحة المزوّد.
- [ ] **Moyasar:** إكمال KYC ثم `python scripts/moyasar_live_cutover.py` (مؤسس فقط)؛ تحقّق من
      الدفع + webhook بأوراق اعتماد حقيقية.
- [ ] **Warm list:** املأ `data/warm_list.csv` ثم drafts فقط عبر القنوات المعتمدة (approval-gated).
- [ ] **النشر + smoke:** Railway `up` → `curl /health`, `/health/deep`, `/api/v1/pricing/plans`
      → `make production-smoke PRODUCTION_BASE_URL=...`. (ملاحظة: healthcheck الـ Railway = `/healthz`.)

**لا تلقائيًا أبدًا / Never automatic:** رسائل العملاء، الدفع الحي، الالتزامات الخارجية.

---

## 5. النطاق المسموح للإطلاق الخاص / Allowed private-launch scope

مسموح بعد §4: ديمو خاص · تشخيص مجاني · 7-Day Revenue Proof Sprint (499 ريال) · dry-run
للأتمتة · workflows بموافقة أولًا · lead scoring داخلي · ادعاءات مدعومة بأدلة.

**غير مسموح بعد / Not allowed yet:** إطلاق عام · cold WhatsApp · scraping بلا أساس قانوني ·
ادعاءات إيراد مضمون · مدفوعات حيّة تلقائية · التزامات خارجية تلقائية.

(مرآة للـ 11 non-negotiables في `dealix/commercial_ops/doctrine.py` + الثمان بوّابات الدستورية
في `docs/BRAND_PRESS_KIT.md`.)

---

## 6. خطة التراجع / Rollback plan

1. عطّل workflow الإنتاج.  2. أرجِع آخر commit إصدار.  3. عطّل مداخل checkout/الدفع.
4. دوّر الأسرار المتأثرة.  5. جمّد workflows الإرسال الخارجي.  6. انشر مذكرة حادثة داخلية.
7. استعد آخر نشر سليم معروف (Railway redeploy لآخر-أخضر ≈ 30 ثانية — انظر `docs/ops/DEPLOY_RUNBOOK.md`).

---

## 7. خطة أول إيراد — متوافقة مع السلّم الرسمي / First-revenue plan (ladder-aligned)

- **المدخل:** Free AI Ops Diagnostic → **7-Day Revenue Proof Sprint (499 ريال)** = بوابة الـ pilot.
- **الترقية:** Data-to-Revenue Pack (1,500) → Managed Revenue Ops (2,999–4,999/شهر).
- **الارتباط الراقي:** Executive Command Center (7,500–15,000/شهر، **بعد 3 pilots** —
  انظر `sales/COMMAND_SPRINT_OFFER.md`).
- **الهدف:** أول Sprint مدفوع واحد، أول Proof Pack واحد، أول عرض retainer واحد.
- لا upsell قبل Proof؛ لا إيراد قبل `invoice_paid` (non-negotiable).

> تنبيه: هذا يختلف عن "Command Sprint لمرة واحدة بـ 7,500–15,000 ريال" في الخطة الملصقة —
> ذاك كان يتعارض مع السلّم الرسمي، فأُعيد ضبطه إلى Executive Command Center الشهري.

---

## 8. مراجع (لا تكرار) / Cross-references

- `docs/ops/COMMERCIAL_GO_LIVE_GATE.md` — بوّابة go-live الرسمية (6 فئات).
- `docs/ops/LAUNCH_READINESS_EXECUTION_2026_06_06.md` — يقدّمه PR #650 (الحالة الصادقة للاختبارات).
- `docs/ops/PRODUCTION_SECRETS_CHECKLIST.md` · `docs/ops/PRODUCTION_ENV_TEMPLATE.md` — الأسرار.
- `docs/ops/DEPLOY_RUNBOOK.md` — خطوات النشر + التراجع.
- `docs/ops/CI_PERMISSIONS_AND_BRANCH_PROTECTION.md` — صلاحيات CI + حماية main + Environments.
- `docs/OFFER_LADDER_AND_PRICING.md` — السلّم الرسمي للعروض.

_Estimated value is not Verified value — القيمة التقديرية ليست قيمة مُتحقَّقة._
