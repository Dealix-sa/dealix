# Dealix — هرم الوكلاء وتشغيل العمليات الذاتي
# Dealix — Agent Org & Autonomous Operations Blueprint
<!-- Owner: dealix-ceo | العربية أولاً — Arabic primary -->

> **القاعدة الحاكمة:** الوكلاء يستكشفون، يحلّلون، ويوصون. سير العمل الحتمي
> ينفّذ. **الإنسان (المؤسس) يوافق على الخطوات الحرجة.** "التشغيل الذاتي
> الكامل" يعني أتمتة كل شيء **حتى بوّابة الموافقة** — والبوّابة ليست عائقاً،
> هي خندق المنتج التنافسي (لماذا تثق مؤسسة سعودية بـDealix بدل أداة أجنبية).
>
> Agents explore, analyze, recommend. Deterministic workflows execute.
> The human founder approves critical moves. "Full self-operating ops" means
> automation up to the approval gate — that gate is the moat, not friction.

---

## 1. الهرم — Org Chart

```
                    ┌─────────────────────────┐
                    │   Founder (human)        │  ← يملك كل الموافقات الحرجة
                    └────────────┬────────────┘
                    ┌────────────┴────────────┐
                    │      dealix-ceo          │  Tier 0 — Apex Orchestrator
                    │  (single accountability) │
                    └────────────┬────────────┘
        ┌──────────┬─────────────┼─────────────┬──────────┬──────────┐
   ┌────┴───┐ ┌────┴───┐   ┌─────┴──┐    ┌─────┴──┐ ┌─────┴──┐ ┌─────┴──┐
   │  CRO   │ │  COO   │   │  CFO   │    │  CTO   │ │  CMO   │ │  CCO   │  Tier 1
   │revenue │ │delivery│   │finance │    │  tech  │ │marketing│ │governance│ Chiefs
   └────┬───┘ └────┬───┘   └────┬───┘    └────┬───┘ └────┬───┘ └────┬───┘
        │          │            │             │          │          │
  ┌─────┴─────┐┌───┴──────┐┌────┴─────┐  ┌────┴────┐┌────┴───┐┌─────┴────┐ Tier 2
  │ sales     ││ delivery ││ data-    │  │engineer ││content ││ qa       │ Specialists
  │ lead-     ││ customer-││ analyst  │  │         ││        ││ proof-   │
  │ researcher││ success  │└──────────┘  └─────────┘└────────┘│ curator  │
  │ proposal- ││ proof-   │                                   └──────────┘
  │ writer    ││ curator  │
  └───────────┘└──────────┘

  dealix-pm — program manager: tracks the 90-day plan & weekly cadence across all chiefs.
```

**19 وكيلاً** عبر 3 طبقات: 1 تنفيذي أعلى + 6 رؤساء + 11 متخصصاً تنفيذياً (+ pm).

---

## 2. الأدوار في سطر — Roster

| الوكيل | الطبقة | يملك | يفوّض إلى / يرفع إلى |
|---|---|---|---|
| `dealix-ceo` | 0 | الاستراتيجية، الأولوية، بوّابات القرار | ← المؤسس / → الرؤساء الـ6 |
| `dealix-cro` | 1 | الإيراد: قمع، تأهيل، عروض، تحويل | → sales, lead-researcher, proposal-writer |
| `dealix-coo` | 1 | التسليم: Sprint، Managed Ops، السعة، البقاء | → delivery, customer-success, proof-curator |
| `dealix-cfo` | 1 | النموذج المالي، اقتصاديات الوحدة، حقيقة الإيراد | → data-analyst |
| `dealix-cto` | 1 | المنصة، البنية، CI، جاهزية الإنتاج | → engineer, qa |
| `dealix-cmo` | 1 | العلامة، المحتوى، التموضع، التواصل | → content |
| `dealix-cco` | 1 | الدستور، الـ11 مبدأ، الامتثال، التدقيق — **حق نقض** | → qa |
| `dealix-pm` | — | تتبّع خطة 90 يوم والإيقاع الأسبوعي | ↔ كل الرؤساء |
| `dealix-sales` | 2 | تأهيل، حركة بيع المؤسس، مسودات تواصل | ← cro |
| `dealix-lead-researcher` | 2 | إيجاد وإثراء حسابات ICP (بلا scraping) | ← cro |
| `dealix-proposal-writer` | 2 | تصيير العروض عبر السلّم | ← cro |
| `dealix-delivery` | 2 | تشغيل Sprint الـ7 أيام | ← coo |
| `dealix-customer-success` | 2 | onboarding، الإيقاع، NPS، churn | ← coo |
| `dealix-proof-curator` | 2 | تجميع Proof Pack، تسجيل Capital Asset | ← coo |
| `dealix-data-analyst` | 2 | DQ، تحليل القمع، أرقام المالية | ← cfo / coo |
| `dealix-engineer` | 2 | كود، اختبارات، routers، migrations | ← cto |
| `dealix-content` | 2 | وثائق، SOPs، LinkedIn، دراسات حالة | ← cmo |
| `dealix-qa` | 2 | الاختبارات، حرّاس العقيدة، جاهزية الإصدار | ← cto / cco |

---

## 3. RACI — من يفعل ماذا

| النشاط | R (منفّذ) | A (مسؤول) | C (يُستشار) | I (يُبلَّغ) |
|---|---|---|---|---|
| ملء القمع وتأهيل العملاء | sales, lead-researcher | cro | data-analyst | ceo |
| تصيير عرض | proposal-writer | cro | cfo (السعر) | ceo |
| تسليم Sprint 7 أيام | delivery | coo | data-analyst | cro, ceo |
| تجميع Proof Pack | proof-curator | coo | cco | ceo |
| النموذج المالي والتوقّع | data-analyst | cfo | — | ceo |
| كود وبنية تحتية | engineer | cto | cco | ceo |
| محتوى وإعلان تدشين | content | cmo | cco | ceo |
| مراجعة حوكمة قبل أي إصدار | qa | cco | cto | ceo |
| **أي إرسال/شحن خارجي** | — | **المؤسس (إنسان)** | cco | ceo |

---

## 4. التشغيل الذاتي — الإيقاع — Autonomous Operating Cadence

### الحلقة اليومية — Daily Loop
1. `dealix-ceo` يُستدعى → يقرأ حالة الشركة + `git log` + سجلّ الاحتكاك.
2. يحدّد الهدف الأهم اليوم ويبني قائمة مهام عبر `TodoWrite`.
3. يفوّض بالتوازي للرؤساء المعنيين عبر أداة `Agent`.
4. كل رئيس يفوّض لمتخصصيه؛ المتخصصون ينتجون مخرجات (تحليل، كود، مسودات، Proof Pack).
5. `dealix-cco` + `dealix-qa` يفحصان كل مخرَج قبل الشحن.
6. `dealix-ceo` يدمج، يحلّ التعارضات، commit + push، ويرفع تقريراً من 5 أسطر للمؤسس.

### الدورة الأسبوعية — Weekly Cycle (يديرها `dealix-pm`)
- السبت/الأحد: CRO يجهّز القمع — أبحاث + مسودات تواصل (تنتظر موافقة المؤسس).
- الإثنين/الثلاثاء: المؤسس يوافق ويرسل؛ COO يجهّز التسليم.
- الأربعاء/الخميس: demos (المؤسس) + تسليم Sprints الجارية.
- الجمعة: مراجعة — pm يجمع السجلّات، cfo يحدّث التوقّع، cco يؤكّد 0 انتهاكات.

### بوّابات القرار — Decision Gates
- **Go-Live**: ≥1 فاتورة Moyasar مدفوعة + ≥1 Proof Pack ≥70 + ≥1 ملخّص حالة آمن + 0 انتهاكات عقيدة.
- إيراد < 25K ريال يوم 60 → `cfo` يوصي `ceo` بإيقاف بناء عروض جديدة والتركيز على البيع.
- وقت المؤسس/Sprint > 5 ساعات بعد العميل الخامس → `coo` يوقف بيع Sprints جديدة، أتمتة التسليم تصير أولوية P0.

---

## 5. خريطة بوّابات الموافقة — Approval-Gate Map

كل سهم يعبر بوّابة موافقة بشرية إجبارية ⛔ — لا وكيل يتجاوزها:

| الإجراء | يُؤتمت حتى | ⛔ بوّابة المؤسس | يُنفَّذ بعدها |
|---|---|---|---|
| تواصل خارجي (بريد/واتساب) | مسودة جاهزة في `approval_center` | المؤسس يراجع ويوافق | المؤسس يرسل بنفسه |
| شحن العميل (Moyasar) | فاتورة test-mode مولّدة | المؤسس يفعّل الوضع الحي | الدفع الحقيقي |
| نشر محتوى/إعلان | مسودة كاملة | المؤسس يوافق | النشر |
| استخدام شهادة عميل | مسودة + طلب إذن | إذن موقّع | الاستخدام العلني |
| ترقية درجة في السلّم | توصية مدعومة بإثبات | المؤسس يقرّ | فتح الدرجة |

كل ما عدا ذلك (تحليل، تسجيل، تصيير مسودة، فحص حوكمة، تجميع Proof Pack) **يُؤتمت بالكامل**.

---

## 6. كيف تُستدعى المنظمة — How to Invoke

- أمر واسع/غامض ("شغّل الشركة"، "نمِّ الإيراد") → استدعِ `dealix-ceo`.
- هدف في مجال واحد → استدعِ الرئيس المعني مباشرة (`dealix-cro` للإيراد، إلخ).
- مهمة محدّدة → استدعِ المتخصص مباشرة.
- "ما الحالة / ما التالي" → استدعِ `dealix-pm`.

كل وكيل ملفّه في `.claude/agents/dealix-*.md` ويحمل هويته وأدواته وشروط رفضه.

---

*كل الوكلاء يلتزمون الـ11 مبدأ غير القابل للتفاوض. حق النقض على العقيدة بيد
`dealix-cco` ولا يتجاوزه إلا المؤسس كتابةً.*

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
