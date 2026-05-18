# Warm List Qualification — تأهيل القائمة الدافئة

> **STATUS: ANALYSIS ONLY. NOTHING SENT.** This document qualifies the 20-name prospect list
> against current Dealix doctrine. No outreach is sent as a result of this file. Every
> sendable draft lives in `OUTREACH_DRAFTS_QUEUED.md` and requires founder review + manual
> send.
>
> **هذا المستند تحليلي فقط. لا يُرسَل شيء.** يؤهّل هذا الملف قائمة الـ20 اسماً مقابل
> الدكترين الحالي. كل مسوّدة قابلة للإرسال موجودة في `OUTREACH_DRAFTS_QUEUED.md` وتتطلب
> مراجعة المؤسس وإرسالاً يدوياً.

---

## 1. Source-list integrity finding — ملاحظة على سلامة القائمة / CRITICAL

**EN —** The file `dealix_leads_20_real.md` is a **legacy, off-doctrine artifact**. Its own
header states the list was built from *Crunchbase, TechCrunch, LinkedIn, Tracxn, Wamda,
MENAbytes, Wellfound* — i.e. it is a **cold-sourced prospect list**, not a warm list. It also
carries retired doctrine: "1 SAR pilot", "999 SAR" pricing, "AI sales rep that replies in 45
seconds", and "auto-book demos", and it instructs first contact via cold LinkedIn DM.

Per `WARM_LIST_WORKFLOW.md §1`, the warm list is defined as **20 personal contacts the founder
has met at least once, in person or by named introduction** — no scraped lists, no "found you
on LinkedIn" first contact. The 20 companies below therefore **cannot be treated as warm leads
or contacted cold**. They are reclassified here as a **target/ICP reference list**: each entry
becomes a real lead **only** when the founder can attach a genuine warm path (prior personal
relationship, or a named, opted-in introduction).

**AR —** ملف `dealix_leads_20_real.md` أداة قديمة مخالفة للدكترين. ترويسته نفسها تذكر أن
القائمة بُنيت من Crunchbase وTechCrunch وLinkedIn وTracxn — أي أنها قائمة باردة مُجمَّعة لا
قائمة دافئة، وتحمل دكترين متقاعداً ("تجربة 1 ريال"، تسعير "999 ريال"، "مندوب AI يرد خلال 45
ثانية"، حجز demos آلياً) وتوجّه للتواصل البارد عبر LinkedIn DM. وفق `WARM_LIST_WORKFLOW.md §1`
القائمة الدافئة هي 20 جهة شخصية قابلها المؤسس مرة واحدة على الأقل. لذلك تُعاد تصنيف هذه الجهات
كقائمة أهداف مرجعية (ICP) — ولا تصبح lead فعلياً إلا إذا ربطها المؤسس بمسار دافئ حقيقي
(علاقة سابقة أو تعريف مُعلَن وبموافقة).

---

## 2. Qualification method — منهج التأهيل

Each prospect is run against the 8 qualification questions
(`auto_client_acquisition/sales_os/qualification.py`):

1. pain_clear · 2. owner_present · 3. data_available · 4. accepts_governance ·
5. has_budget · 6. wants_safe_methods · 7. proof_path_visible · 8. retainer_path_visible

**Doctrine note on Q6 (`wants_safe_methods`):** the *prospect* is not asking for unsafe
methods — but the **only contact instruction on file is a non-negotiable violation** (cold
LinkedIn DM as first contact). So no prospect can be `ACCEPT`ed for outreach until a warm path
is supplied. The honest verdict for the whole list is therefore a **channel/consent gate**, not
a per-company rejection of the company itself.

Verdicts used: `ACCEPT` · `DIAGNOSTIC_ONLY` · `REFRAME` · `REJECT` · `REFER_OUT`.
A 6th operational status is recorded for clarity: `WARM-PATH REQUIRED` — the company fits ICP,
but is **not yet a contactable lead** because no warm relationship exists. This is not a
qualification verdict; it is a pre-qualification gate (the company never reaches the
`qualify()` endpoint until the founder confirms a warm path).

---

## 3. Qualification table — جدول التأهيل

Recommended offer ladder: **Rung 0 Free Revenue Diagnostic (0 SAR) → Rung 1 7-Day Revenue
Intelligence Sprint (499 SAR)**. Channel column reflects **doctrine-compliant** channel, not
the legacy LinkedIn-DM instruction.

| # | Company / الشركة | Segment / الشريحة | 8-Q read | Verdict | Recommended offer / العرض | Channel / القناة | Draft status |
|---|---|---|---|---|---|---|---|
| 1 | Salla | E-commerce platform SaaS | Pain plausible, owner is CEO, data ready, governance fits, budget yes, proof+retainer visible — **but no warm path** | WARM-PATH REQUIRED | Rung 0 → 1 once warm path exists | Warm intro / referral only | Generic warm-list draft only (A.1) — not personalized until warm path confirmed |
| 2 | Zid | E-commerce platform SaaS | Same as Salla | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | Generic draft only |
| 3 | Foodics | Restaurant POS SaaS | Strong ICP, owner reachable, data ready, budget yes | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | Generic draft only |
| 4 | Lucidya | Enterprise CXM SaaS | Strong ICP. Legacy doc proposes a **fabricated family-name angle** — that is a manipulative opener, not a warm path. Strip it. | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | Generic draft only; family-name opener removed as off-doctrine |
| 5 | BRKZ | Construction-tech marketplace | Good ICP, owner is CEO, B2B revenue ops fit | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | Generic draft only |
| 6 | Sary | B2B SMB marketplace | Good ICP, fits revenue ops | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | Generic draft only |
| 7 | Retailo | B2B retail marketplace | Good ICP | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | Generic draft only |
| 8 | Rekaz | SMB vertical SaaS (booking/CRM) | ICP fits; **named owner unknown** (Q2 unconfirmed) | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | No draft — owner not identified, no warm path |
| 9 | Glamera | SMB vertical SaaS (salons/gyms) | ICP fits; **named owner unknown** | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | No draft — owner not identified |
| 10 | Lean Technologies | Open-banking / fintech infra | Regulated, governance-led fit is strong; long B2B cycle | WARM-PATH REQUIRED | Rung 0 → 1 (governance variant) | Warm intro / referral only | Generic draft only (regulated variant A.2 v3) |
| 11 | Mozn | AI/ML platform (Saudi) | AI-native buyer; **named owner unknown** | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | No draft — owner not identified |
| 12 | Mnzil | Proptech | ICP fits broker revenue ops; **named owner unknown** | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | No draft — owner not identified |
| 13 | Logexa | Logistics platform | ICP fits B2B contract ops; **named owner unknown** | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | No draft — owner not identified |
| 14 | Tamara | BNPL fintech | Regulated fintech; large/late-stage — likely Enterprise tier (AI Governance Review) not Sprint | WARM-PATH REQUIRED + REFRAME on tier | Rung 0 diagnostic; Enterprise track if scope confirms | Warm intro / referral only | No draft — tier reframe needed before any approach |
| 15 | Nana | Grocery delivery | Consumer-delivery, B2C-heavy — weak fit for B2B revenue-ops wedge | DIAGNOSTIC_ONLY (if warm path appears) | Rung 0 only; do not pitch Sprint | Warm intro / referral only | No draft — weak ICP fit |
| 16 | Jahez | Food delivery | Large public co.; B2C-heavy — weak fit for the productized wedge | DIAGNOSTIC_ONLY / REFER_OUT | Rung 0 only, or refer to a partner | Warm intro / referral only | No draft — weak ICP fit |
| 17 | Merit Incentives | HR tech | B2B HR sales cycle — plausible fit; **named owner unknown** | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | No draft — owner not identified |
| 18 | Bayzat | HR SaaS | B2B SaaS, plausible fit; **named owner unknown** | WARM-PATH REQUIRED | Rung 0 → 1 | Warm intro / referral only | No draft — owner not identified |
| 19 | SiFi | Corporate-banking fintech | Regulated fintech; governance fit; **named owner unknown** | WARM-PATH REQUIRED | Rung 0 → 1 (governance variant) | Warm intro / referral only | No draft — owner not identified |
| 20 | Hakbah | Savings fintech | Regulated fintech; partnerships-ops fit; **named owner unknown** | WARM-PATH REQUIRED | Rung 0 → 1 (governance variant) | Warm intro / referral only | No draft — owner not identified |

---

## 4. Verdict breakdown — ملخّص الأحكام

| Verdict / الحكم | Count | Companies |
|---|---|---|
| WARM-PATH REQUIRED (ICP fits; not yet contactable — needs warm path) | 16 | 1,2,3,4,5,6,7,8,9,10,11,12,13,17,18,19,20 minus the 2 below — see note |
| WARM-PATH REQUIRED + tier REFRAME (Enterprise, not Sprint) | 1 | 14 Tamara |
| DIAGNOSTIC_ONLY / weak ICP (Rung 0 ceiling) | 2 | 15 Nana, 16 Jahez |
| Hard REJECT (company itself outside scope) | 0 | — |
| REFER_OUT (better served by a partner) | 0 outright; 16 Jahez is a candidate if scope is B2C | — |

> Note: counts — 17 companies are WARM-PATH REQUIRED (rows 1–13, 17, 18, 19, 20); 1 is
> WARM-PATH REQUIRED + tier reframe (14); 2 are DIAGNOSTIC_ONLY weak-ICP (15, 16). Total = 20.

**No company on the list is a hard REJECT** — the companies themselves are legitimate Saudi
B2B businesses. The blocker is **channel/consent**: the list was cold-sourced, and the only
contact instruction on file (cold LinkedIn DM) is a constitutional violation. Zero of the 20
are sendable today.

---

## 5. What must happen before any of these become real leads — ما يلزم قبل التحوّل إلى leads

1. **Founder supplies a warm path per company** — a prior personal relationship, or a named,
   opted-in introduction from a mutual contact. Logged as `relationship_basis` in
   `engagement_ledger` (the consent record).
2. **Owner identified** for the 7 companies marked "named owner unknown" (Rekaz, Glamera,
   Mozn, Mnzil, Logexa, Merit, Bayzat, SiFi, Hakbah) — and identified via a legitimate route,
   not scraped enrichment.
3. **Run `qualify()`** only after a warm path is confirmed and an intake is collected.
4. **Then** personalize a draft in `OUTREACH_DRAFTS_QUEUED.md` and queue for founder send.

Until step 1 is satisfied per company, the **only** doctrine-compliant outreach is the
generic warm-list one-line ask (`OUTREACH_DRAFTS_QUEUED.md §A.1`) sent to the founder's
**actual** personal contacts — who may or may not overlap with this target list.

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
</content>
</invoke>
