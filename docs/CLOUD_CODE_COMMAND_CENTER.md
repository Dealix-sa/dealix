# Dealix Cloud Code Command Center — مركز قيادة الوكيل البرمجي

> دليل تشغيل يومي للوكلاء البرمجيين (Claude Code / Codex / Cursor) داخل Dealix،
> **بالأوامر الحقيقية للمشروع** (Python + Next.js)، لا أوامر `npm run` وهمية.
> الدستور المُلزِم في [`AGENTS.md`](../AGENTS.md) — هذا الملف **يكمّله ولا يكرّره**.
> الخريطة الموحّدة في [`docs/FOUNDER_OS_INDEX.md`](FOUNDER_OS_INDEX.md).

**Status:** additive · **Owner:** founder · **Last reviewed:** 2026-06-02

---

## 0) قبل أي تعديل / Before editing — اقرأ بالترتيب
1. [`AGENTS.md`](../AGENTS.md) — أوامر الدور، البيئة، وما لا يُعاد تشخيصه كأخطاء.
2. [`docs/FOUNDER_OS_INDEX.md`](FOUNDER_OS_INDEX.md) — وين كل أصل.
3. الـ workflows في `.github/workflows/` (خصوصًا `ci.yml`).
4. المجلدات: `api/` · `frontend/` · `auto_client_acquisition/` · `dealix/` · `scripts/` · `docs/`.

---

## 1) الأمر اليومي / The daily command (انسخه للوكيل)

```text
You are operating Dealix as a Founder OS agent.
Today’s objective: increase founder leverage and revenue readiness WITHOUT increasing technical risk.

Read first: AGENTS.md, docs/FOUNDER_OS_INDEX.md, the relevant docs/ and scripts/.

Execute:
1. Find the single highest-leverage gap (revenue, product, delivery, or security).
2. Fix it with the SMALLEST safe PR. Prefer improving existing files over creating new ones.
3. Improve one revenue asset and one operational doc IF it is genuinely missing — never duplicate.
4. Add or strengthen one test/guardrail.
5. Run the guardrails below.
6. Produce a founder-readable PR summary.

Never: merge to main · expose secrets · broad refactors · add paid deps without justification ·
silently skip tests · overwrite AGENTS.md / README / CI without an explicit request.

Final PR answers: What business value? What changed? How to test? What risk remains? What should the founder do next?
```

---

## 2) المراحل / Phases

- **Phase 1 — Reality check:** افحص السكربتات/الوثائق/الاختبارات المكسورة. لا تعتبر ما في `AGENTS.md` §"Resolved in repo" أخطاءً جديدة.
- **Phase 2 — Revenue:** حسّن أصلًا تجاريًا قائمًا (راجع جدول §3 في الفهرس) بدل إنشاء بديل.
- **Phase 3 — Product:** أعلى أثر في `api/` أو `frontend/` بأصغر تغيير، مع اختبار.
- **Phase 4 — Founder automation:** حسّن تقريرًا يساعد المؤسس يقرر (راجع `scripts/dealix_founder_daily_brief.py`).
- **Phase 5 — Guardrails:** شغّل القسم التالي كاملًا.

---

## 3) الحواجز / Guardrails (الأوامر الحقيقية)

```bash
ruff check .
black --check .
APP_ENV=test pytest -q --no-cov          # أو حزمة الانحدار السريعة في AGENTS.md §"Running tests"
python3 scripts/check_env_contract.py     # عقد البيئة (backend + apps/web)
python3 scripts/security_smoke.py         # فحص أسرار/.env سريع
python3 scripts/check_ledgers.py          # سجلات المؤسس
python3 -m compileall api dealix scripts  # نفس ما يفعله CI
```

> لا تُعطِّل اختبارًا لتُخضِّر CI. لا تُضعِف مصادقة أو تحقّقًا. فشل مغلق لا مفتوح (fail closed).

---

## 4) المهام / Missions (كلها "حسّن"، لا "أعد الإنشاء")

| Mission | الهدف | ابدأ من / Start from |
| --- | --- | --- |
| إغلاق فجوة توثيق | اربط ناقصًا بالفهرس | `docs/FOUNDER_OS_INDEX.md` |
| Revenue Engine | حسّن أصل تجاري قائم | `docs/commercial/FOUNDER_SALES_PLAYBOOK_AR.md` · `docs/OFFER_LADDER_AND_PRICING.md` |
| Outreach (draft-only) | حسّن رسائل (بدون إرسال خارجي) | `docs/V7_FIRST_10_WARM_OUTREACH_PACK.md` · `scripts/warm_list_outreach.py` |
| Saudi B2B positioning | عمّق التموضع/القطاعات | `docs/POSITIONING_AND_ICP.md` · `docs/SECTOR_PLAYBOOKS.md` |
| Founder dashboard | تشغيل من الواجهة | `frontend/` · مسارات `/ops/founder` في `AGENTS.md` |
| Security hardening | صلاحيات/أسرار | `scripts/check_env_contract.py` · `SECURITY.md` |
| Deployment reliability | نشر متوقَّع | `scripts/production_smoke.sh` · `docs/SECURITY_RUNBOOK.md` |
| Client delivery | تسليم متكرر | `docs/PILOT_DELIVERY_SOP.md` · `docs/ONBOARDING_FLOW.md` |

---

## 5) إيقاع 3 PRs يوميًا / Three-PR rhythm

| PR | الوقت | النوع |
| --- | --- | --- |
| PR 1 | صباحًا | Revenue / sales asset |
| PR 2 | وسط اليوم | Product / automation |
| PR 3 | آخر اليوم | QA / docs / security |

كل PR **صغير** وقابل للمراجعة والاختبار والتراجع. لا تعدّل عشرات الملفات دفعة واحدة.

---

## 6) (اختياري) workflow وكيل Claude — مُحصَّن / opt-in & hardened

> ⚠️ **غير مفعّل افتراضيًا.** هذا snippet جاهز للصق *إذا* قرّر المؤسس تفعيله عمدًا.
> يفتح PRs فقط — **لا يدمج في main**. صلاحياته أدنى ما يلزم، ويتطلّب سرّ `ANTHROPIC_API_KEY`.
> سبب إبقائه موثّقًا لا حيًّا: تفعيل أتمتة بصلاحيات `write` + أسرار على ريبو عام قرار أمني واعٍ
> (راجع `ledgers/risks.json` RISK-0002).

```yaml
# .github/workflows/claude-founder-agent.yml  — انسخه فقط عند التفعيل المتعمَّد
name: Claude Founder Agent (opt-in)
on:
  workflow_dispatch:
    inputs:
      mission:
        description: "Dealix mission for Claude"
        required: true
        type: string
permissions:
  contents: write          # لإنشاء فرع/PR فقط — لا صلاحيات أوسع
  pull-requests: write
jobs:
  claude:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - name: Run Claude Code
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          direct_prompt: |
            Read AGENTS.md and docs/FOUNDER_OS_INDEX.md first.
            Mission: ${{ inputs.mission }}
            Make a small, safe, revenue-focused change. Do NOT merge to main.
            Run guardrails in docs/CLOUD_CODE_COMMAND_CENTER.md §3.
            Update docs only when business logic changes; never duplicate existing docs.
            PR must include: business impact, technical summary, test evidence, security risk, rollback plan.
```

عند التفعيل: **Actions → Claude Founder Agent (opt-in) → Run workflow**، واكتب الـ mission.

---

## 7) الممنوعات / Forbidden (مختصر — التفصيل في `AGENTS.md`)
```text
Never commit .env files · never print secrets · never weaken auth ·
never disable tests to green CI · never remove commercial scripts ·
never overwrite AGENTS.md / README / CI without explicit request ·
never invent CRM numbers · never add paid deps without cost/risk note ·
never enable real external sends (WhatsApp/LinkedIn) in any environment.
```
