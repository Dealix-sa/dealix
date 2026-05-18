<!-- Owner: Founder | Generated: 2026-05-18 | Workstream E (Revenue Operating System) -->
<!-- Status: DRAFT QUEUE — awaiting founder approval. No external sends. -->

# Warm List Draft Queue — طابور مسودات القائمة الدافئة

> هذا الملف هو **طابور موافقة**. كل رسالة هنا **مسودة فقط** — لا تُرسَل أي رسالة
> خارجية حتى يوافق المؤسس على الصف يدوياً. لا واتساب بارد، لا scraping، لا أتمتة
> LinkedIn، لا إرسال جماعي.
>
> This file is an **approval queue**. Every message here is a **draft only** — no
> external message is sent until the founder manually approves the row. No cold
> WhatsApp, no scraping, no LinkedIn automation, no bulk send.

Conforms to: [`NARRATIVE_VCURRENT.md`](./NARRATIVE_VCURRENT.md) ·
[`WARM_LIST_WORKFLOW.md`](./WARM_LIST_WORKFLOW.md) ·
[`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) ·
the 11 non-negotiables.

---

## 0. STATUS — WARM LIST IS EMPTY / القائمة الدافئة فارغة

**The warm list is not populated.** The designated source file `data/warm_list.csv`
does not exist; only `data/warm_list.csv.template` exists, and it carries a single
placeholder row (`Founder Friend One` — a fictitious example, not a real contact).
The `CEO_TOP50_TRACKER.csv` confirms task #15 `fill_first_20_warm_contacts` is still
`NEXT_7` (not done).

**The qualification verdicts below could not be run against real targets** because
there are no real targets. Running the 8-question scorer requires discovery answers
(pain, owner, data, governance, budget, safe-methods, proof path, retainer path) —
none of which exist for a placeholder.

> **What was deliberately NOT used as a warm list:** `docs/ops/pipeline_tracker.csv`
> contains 50 named tech founders (Lucidya, Foodics, Salla, Tamara, etc.), but its
> `channel` column is `LinkedIn` / `Twitter DM`, its `message_version` is
> `first_dm_v1`, and rows 30-50 are explicitly TBD ("Identify via search"). That is
> a **cold prospecting list**, not a warm relationship list. Treating it as a warm
> list and drafting outreach to those founders would be **cold LinkedIn outreach** —
> a non-negotiable violation. It is excluded on purpose. See section 4.

**Founder action required:** populate section 2 with 5-15 real personal contacts
(people you have met at least once or have a named introduction to), then approve
rows for send. Section 3 gives ready-to-personalize Arabic draft patterns.

---

## 1. How to use this queue — كيف تُستخدم

1. Fill one row per warm contact in **Section 2**. The audience rule
   (`WARM_LIST_WORKFLOW.md` §1): a person you have met at least once, in person or
   by named introduction. No purchased lists. No scraped lists.
2. For each contact, run the qualification gate. Until a discovery call happens you
   only have **pre-call intelligence** — most rows will sit at `DIAGNOSTIC_ONLY` or
   `pre-call (unscored)`, which is correct: the warm message itself only offers the
   **Free Mini Diagnostic** (`free_mini_diagnostic`, 0 SAR). The 499 SAR
   `revenue_proof_sprint_499` is offered **after** a "yes, tell me more", never in
   the first message.
3. Pick a draft pattern from **Section 3**, personalize every `[bracket]`, and paste
   it into the row. Founder voice — not a bulk template.
4. Leave `Status = awaiting founder approval` until you have personally reviewed and
   decided to send. Then change it to `approved — sent <date>` or `held` / `dropped`.
5. Send only through the channel where the relationship already exists. One message
   per contact. No automated follow-up.

### Qualification gate reference (the 8 questions)

Scorer: `auto_client_acquisition/sales_os/qualification.qualify(...)`. Weights sum
to 100: pain_clear 15, owner_present 15, data_available 15, accepts_governance 10,
has_budget 10, wants_safe_methods 10, proof_path_visible 15, retainer_path_visible 10.

| Score / signal | Verdict | Recommended offer |
|---|---|---|
| Any doctrine trigger (cold WhatsApp / scraping / guaranteed sales / LinkedIn automation) or declines safe methods | `REJECT` | decline politely, cite the non-negotiable |
| Governance not accepted | `REFER_OUT` | refer to a partner |
| Score >= 85 | `ACCEPT` | `revenue_proof_sprint_499` |
| Score 70-84, data available | `REFRAME` | shape a smaller first step |
| Score 70-84, no data | `DIAGNOSTIC_ONLY` | `free_mini_diagnostic` |
| Score 45-69 | `DIAGNOSTIC_ONLY` | `free_mini_diagnostic` |
| Score < 45 | `REFER_OUT` | not enough fit |
| No discovery call yet | `pre-call (unscored)` | `free_mini_diagnostic` (the warm message only ever offers this) |

> Note: the warm **outreach message** is offered to every qualifying warm contact
> regardless of pre-call score, because it only invites a free diagnostic. The
> qualification verdict gates what happens **after** the reply — whether a 499 SAR
> sprint is proposed. It never gates whether you may say hello to a person you know.

---

## 2. The queue — الطابور

> Fill one row per real warm contact. Until then this table is the template.
> `Pre-call score` = your honest pre-call estimate; the real score is set by
> `qualify(...)` after the 20-minute discovery call.

| # | Target (name / role / company / sector) | Relationship basis (consent record) | Pre-call score (est.) | Verdict | Recommended offer | Draft message (AR, founder voice) | Channel | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | _[name] / [role] / [company] / [sector]_ | _[e.g. met at LEAP 2025]_ | _[est.]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _paste from Section 3, personalize every [bracket]_ | _WhatsApp / email — existing channel_ | awaiting founder approval |
| 2 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 3 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 4 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 5 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 6 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 7 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 8 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 9 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 10 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 11 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 12 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 13 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 14 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |
| 15 | _[...]_ | _[...]_ | _[...]_ | `pre-call (unscored)` | `free_mini_diagnostic` (0 SAR) | _[...]_ | _[...]_ | awaiting founder approval |

---

## 3. Draft message patterns — أنماط المسودات (founder voice, governed)

> Personalize every `[bracket]`. ≤ 3 Arabic sentences. No "مندوب مبيعات AI"،
> no "45 ثانية", no "1 ريال", no `نضمن`/guaranteed. The first message offers only
> the **free diagnostic** — never the price.

### Pattern A — warm contact who runs a B2B company

**العربية:**

> السلام عليكم [الاسم]، إن شاء الله بخير. أعمل على Dealix — رادار عمليات محكوم
> يوضّح لشركات B2B السعودية ما حدث بعد وصول العميل المحتمل: مَن ردّ، مَن ينتظر،
> ما الخطوة التالية — كل إرسال خارجي بموافقتك. أعرض تشخيصاً مجانياً ثنائي اللغة
> لخط الإيراد عند [الشركة]، يُسلَّم خلال 24 ساعة باعتماد شخصي مني. هل يناسبك أن
> أرسله، أو ترتيب مكالمة 20 دقيقة لنرى إن كان مفيداً لكم؟

**English (secondary):**

> Dealix is a governed operations radar for Saudi B2B — it shows what happened
> after a lead arrives, drafts the next message, and queues every send for your
> approval. I would like to run a free bilingual diagnostic on [company]'s revenue
> pipeline, delivered in 24 hours with my personal sign-off. Shall I send it, or
> set a 20-minute call?

### Pattern B — warm contact who can refer (agency / network connector)

**العربية:**

> السلام عليكم [الاسم]. أبني Dealix — رادار عمليات محكوم لشركات B2B السعودية،
> مسودات فقط والموافقة دائماً للعميل، لا رسائل باردة ولا scraping. أبحث عن
> 2-3 شركات تجرّب تشخيصاً مجانياً لخط الإيراد. مَن يخطر ببالك ممن قد يفيده هذا؟

**English (secondary):**

> Building Dealix — a governed B2B operations radar for Saudi companies; drafts
> only, the customer approves every send, no cold outreach, no scraping. Looking
> for 2-3 companies to try a free revenue-pipeline diagnostic. Anyone come to mind?

### Pattern C — warm contact in a regulated/data-sensitive sector

**العربية:**

> السلام عليكم [الاسم]. أعمل على Dealix — يعرض حالة كل عميل محتمل بعد وصوله
> ويقترح الخطوة التالية، مع سلسلة أدلة قابلة للمراجعة، ومتوافق مع نظام حماية
> البيانات الشخصية من اليوم الأول. هل يناسبك تشخيص مجاني 30 دقيقة لخط الإيراد
> عند [الشركة]، بدون أي التزام؟

**English (secondary):**

> Dealix surfaces the state of every lead after it arrives and suggests the next
> step, with an auditable evidence chain, PDPL-aware from day one. Would a free
> 30-minute diagnostic of [company]'s revenue pipeline be useful — no commitment?

### Reply-handling note

If a warm contact replies "tell me more", do **not** improvise a price in chat.
Use the qualifying reply in `WARM_LIST_WORKFLOW.md` §4.1, run a 20-minute discovery
call, then run `qualify(...)`. Only a verdict of `ACCEPT` (score >= 85) leads to a
`revenue_proof_sprint_499` proposal. `DIAGNOSTIC_ONLY` / `REFRAME` stay on the free
diagnostic until its recommendation field says otherwise.

---

## 4. Excluded / deferred targets — أهداف مستبعدة أو مؤجلة

| Source | Decision | Reason |
|---|---|---|
| `data/warm_list.csv.template` row `Founder Friend One` | **Excluded** | Fictitious placeholder, not a real contact. Cannot be qualified or messaged. |
| `docs/ops/pipeline_tracker.csv` rows 1-29 (Lucidya, Foodics, Salla, Tamara, Mozn, agencies, etc.) | **Deferred — not a warm list** | Channel is LinkedIn / Twitter DM with `first_dm_v1`. Messaging them as "warm" contacts is cold LinkedIn outreach — a non-negotiable violation. Eligible only if the founder confirms a genuine prior relationship for a specific row, which then moves into Section 2 with a real `relationship basis`. |
| `docs/ops/pipeline_tracker.csv` rows 30-50 (TBD "identify via search") | **Rejected as warm targets** | Not yet identified; "identify via search" is cold sourcing by definition. |

---

## 5. Disclaimer — الإفصاح

Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
