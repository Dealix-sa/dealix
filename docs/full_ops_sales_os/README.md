# Full Ops Sales System — نظام المبيعات والتشغيل الذاتي
<!-- WAVE 18 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> **التعريف.** Full Ops = أتمتة كاملة لدورة المبيعات والتسليم والتوسّع
> **حتى بوابة الموافقة**. كل إجراء داخلي آمن (مصنّف `A0`) يُنفَّذ ذاتياً بلا
> ضغطة؛ كل إجراء خارجي يُدرَج في `approval_center` وينتظر موافقة المؤسس.
>
> **Definition.** Full Ops = full automation of the sell→deliver→expand cycle
> **up to the approval gate**. Internal-safe (`A0`) actions self-execute;
> every external action is queued in `approval_center` for founder approval.

> **لماذا ليس "إرسالاً تلقائياً بالكامل".** البند ٨ من الـ11 non-negotiables —
> *لا إجراء خارجي بلا موافقة* — محميّ باختبارات CI
> (`tests/test_doctrine_guardrails.py`). نظام يرسل خارجياً بلا موافقة يكسر
> الـCI ويخالف جوهر المنتج. الأتمتة الكاملة تقف عند الـ95%؛ الـ5% الأخيرة هي
> ضغطة موافقة بشرية واحدة (قابلة للتجميع).

---

## 1. ما هذا النظام — What this is

طبقة تنسيق (orchestration) تشغّل **الخيط الذهبي** كاملاً:

```
إشارة → Lead → تخصيب → تقييم → تأهيل → استخراج ألم → ترتيب أولويات
      → مسودّات → [بوابة موافقة] → تسليم → Proof → توسّع → تعلّم
```

النظام لا يعيد بناء أي وحدة — بل ينسّق الوحدات القائمة (`data_os`,
`sales_os`, `revenue_os`, `revenue_pipeline`, `proof_os`, `value_os`,
`adoption_os`, `client_os`, `friction_log`, `capital_os`, `governance_os`)
عبر عقود `dealix/contracts/` وتصنيفات `dealix/classifications/`.

---

## 2. ملفات هذا النظام — Subsystem Files

| ملف | موضوع |
|------|--------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | المعمارية: الحلقة الذاتية، خريطة المراحل، حدّ الأتمتة |
| [RUNTIME_AGENT_HIERARCHY.md](RUNTIME_AGENT_HIERARCHY.md) | هرم أجينتس وقت-التشغيل (Tier 0–2) |
| [BUILD_AGENT_HIERARCHY.md](BUILD_AGENT_HIERARCHY.md) | هرم أجينتس Claude Code (وقت-البناء) |
| [WAVE_PLAN.md](WAVE_PLAN.md) | خطة البناء على موجات (Wave 18+) |

---

## 3. طبقتا الأجينتس — Two Agent Layers

| الطبقة | أين | تفعل ماذا |
|--------|-----|-----------|
| وقت-التشغيل (Runtime) | `auto_client_acquisition/agent_os/` كـ `AgentCard` | تشغّل دورة المبيعات داخل المنتج للعملاء |
| وقت-البناء (Build-time) | `.claude/agents/*.md` | تبني وتختبر وتطوّر النظام نفسه |

كلتاهما مفصّلتان في الملفّين أعلاه.

---

## 4. الحدود غير القابلة للتفاوض — The 11 Non-negotiables

لا scraping؛ لا واتساب بارد آلي؛ لا أتمتة LinkedIn؛ لا ادعاءات بلا مصدر؛
لا ضمانات نتائج؛ لا PII في السجلّات؛ لا إجابات بلا مصدر؛ لا إجراء خارجي بلا
موافقة؛ لا أجينت بلا هوية؛ لا مشروع بلا Proof Pack؛ لا مشروع بلا Capital
Asset. (المصدر: `.claude/agents/dealix-pm.md`.)

---

## 5. روابط — Cross-links

- استراتيجية التصريف → [`docs/distribution_os/`](../distribution_os/README.md)
- سلم الخدمات والأسعار → [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)
- اللوحة اليومية → [`docs/ops/daily_scorecard.md`](../ops/daily_scorecard.md)

---

*Version 1.0 | Automation stops at the approval gate | Honors the 11 non-negotiables.*
