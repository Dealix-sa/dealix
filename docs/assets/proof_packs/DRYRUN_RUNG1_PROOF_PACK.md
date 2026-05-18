# Proof Pack — Rung 1 Dry-Run / حزمة الأدلة — تشغيل تجريبي للدرجة 1

> **HYPOTHETICAL / CASE-SAFE DRY-RUN — نموذج افتراضي — تشغيل تجريبي**
>
> This Proof Pack was produced by an internal delivery dry-run on **synthetic
> data**. There is **no real customer**, no PII, no signed confirmation, and no
> external send. It exists to verify that the Rung 0–1 delivery machine works
> before the first real paying customer.
>
> هذه حزمة أدلة من تشغيل تجريبي داخلي على **بيانات اصطناعية**. لا يوجد عميل
> حقيقي، ولا بيانات شخصية، ولا تأكيد موقّع، ولا أي إرسال خارجي.

| Field | Value |
|---|---|
| Engagement | 7-Day Revenue Intelligence Sprint (Rung 1, 499 SAR tier) |
| Customer handle | `DRYRUN-AGENCY-A` (synthetic Saudi marketing agency) |
| Engagement ID | `ENG-DRYRUN-RUNG1-001` |
| Run date | 2026-05-18 |
| Audience | `internal_only` |
| Approval status | `approval_required` (no founder approval recorded — dry-run) |
| Consent for publication | `False` for every event (synthetic data) |
| **Proof score** | **100 / 100** |
| **Proof tier / band** | **`case_candidate`** (completeness band; see Limitations) |
| Freeze compliance | Rung 0–1 delivery finish + Proof Pack assembly — permitted by `docs/ops/COMMERCIAL_FREEZE.md` |

---

## 1. Executive Summary / الملخص التنفيذي

**EN —** Hypothetical / case-safe dry-run. The 7-Day Revenue Intelligence Sprint
was executed end-to-end on 10 synthetic leads for a hypothetical Saudi marketing
agency (`DRYRUN-AGENCY-A`). The Source Passport validated, Data Quality scored
**96.0/100**, all 10 accounts were ranked, and a bilingual draft pack was
generated and governance-checked. No external sends, no PII, no charges.

**AR —** نموذج افتراضي. نُفِّذت رحلة "7 أيام لذكاء الإيراد" من البداية للنهاية
على 10 عملاء محتملين اصطناعيين لوكالة تسويق سعودية افتراضية. جواز المصدر اجتاز
التحقق، ودرجة جودة البيانات 96.0/100، وتم ترتيب الحسابات العشرة، وأُنشئت حزمة
مسودات ثنائية اللغة خضعت لفحص الحوكمة. لا إرسال خارجي ولا بيانات شخصية ولا رسوم.

## 2. Problem / المشكلة

**EN —** The synthetic agency cannot tell which of its leads deserve effort
first. Its pipeline is unranked, contains near-duplicate records, and has no
documented source provenance.

**AR —** الوكالة الافتراضية لا تستطيع تحديد أي العملاء المحتملين يستحق الجهد
أولًا. خط الأنابيب غير مُرتَّب، ويحتوي سجلات شبه مكررة، وبلا مصدر موثّق.

## 3. Inputs / المدخلات

**EN —** 10 synthetic lead/opportunity rows across 8 sectors and 4 Saudi cities
(Riyadh, Jeddah, Dammam, Khobar), 8 columns. All rows are explicitly labelled
synthetic / case-safe and carry **zero PII**. One row is a deliberate
near-duplicate to exercise the dedupe path.

**AR —** 10 صفوف عملاء محتملين اصطناعية عبر 8 قطاعات و4 مدن سعودية، 8 أعمدة.
كل الصفوف اصطناعية وخالية تمامًا من البيانات الشخصية. أحد الصفوف مكرر عمدًا.

## 4. Source Passports / جوازات المصدر

| Field | Value |
|---|---|
| `source_id` | `dryrun-agency-crm-export-2026-05` |
| `source_type` | `customer_provided_crm_export` |
| `owner` | `DRYRUN-AGENCY-A` |
| `allowed_use` | `revenue_intelligence`, `account_scoring`, `draft_generation` |
| `contains_pii` | `False` |
| `ai_access_allowed` | `True` |
| `external_use_allowed` | `False` |
| **`validate()` result** | **`is_valid = True`**, reasons `()`, missing `()` |

Validated via `data_os.source_passport.validate(passport)` →
`source_passport_valid_for_ai`. The passport passed the sovereignty gate, so AI
processing of the synthetic table was permitted.

## 5. Work Completed / العمل المنجز

| Day | Step | Module used |
|---|---|---|
| 1 | Source Passport validation | `data_os.source_passport` |
| 2 | Import + Data Quality score | `data_os.data_quality_score.compute_dq` |
| 3 | Account scoring (top 10) | `revenue_os.scoring.score_account_row` |
| 4 | Bilingual draft pack | `revenue_os.draft_pack.build_revenue_draft_pack` |
| 4 | Governance check per draft | `governance_os.runtime_decision.decide` + `claim_safety` |
| 5 | Proof Pack assembly (14 sections) | `proof_os.proof_pack` + `proof_os.proof_score` |
| 7 | Capital asset registration | `capital_os.capital_ledger.add_asset` |
| 7 | Retainer readiness | `adoption_os.retainer_readiness.evaluate` |

## 6. Outputs / المخرجات

**Ranked top-10 accounts (anonymized):**

| Rank | Handle | Score | Sector | City | Top reasons | Risks |
|---|---|---|---|---|---|---|
| 1 | Account-A | 100 | retail | Riyadh | source_present, sector_icp_match, city_icp_match | — |
| 2 | Account-B | 100 | healthcare | Jeddah | source_present, sector_icp_match, city_icp_match | — |
| 3 | Account-C | 100 | logistics | Dammam | source_present, city_icp_match, company_identified | sector_outside_icp |
| 4 | Account-D | 100 | technology | Riyadh | source_present, sector_icp_match, city_icp_match | — |
| 5 | Account-E | 100 | food_beverage | Riyadh | source_present, sector_icp_match, city_icp_match | — |
| 6 | Account-F | 100 | real_estate | Jeddah | source_present, city_icp_match, company_identified | sector_outside_icp |
| 7 | Account-G | 100 | education | Riyadh | source_present, sector_icp_match, city_icp_match | — |
| 8 | Account-H | 100 | retail | Khobar | source_present, sector_icp_match, city_icp_match | — |
| 9 | Account-I | 100 | retail | Riyadh | source_present, sector_icp_match, city_icp_match | — |
| 10 | Account-J | 79 | technology | Riyadh | sector_icp_match, city_icp_match, company_identified | incomplete_row, missing_source |

**Bilingual draft pack** — AR+EN email, AR+EN LinkedIn note, AR+EN call script
for the top account. **Every draft is draft-only / review-required. No external
send, no automation.**

## 7. Quality Scores / درجات الجودة

**Data Quality Score: 96.0 / 100**

| Sub-score | Value |
|---|---|
| Completeness | 97.5 |
| Duplicate-inverse | 90.0 |
| Format consistency | 100.0 |
| Source clarity | 100.0 |

Account scores range **79–100**. DQ ≥ 70, so no founder DQ-review gate was
triggered.

## 8. Governance Decisions / قرارات الحوكمة

- 6 customer-facing drafts (AR+EN email, LinkedIn, call script) were each checked
  via `governance_os.runtime_decision.decide(action="generate_draft", ...)` and
  `governance_os.claim_safety.audit_claim_safety`. **All 6 returned `allow` /
  claim_safety `ALLOW`** with zero issues.
- **Negative control:** a deliberately unsafe claim
  (`"نضمن لك زيادة المبيعات — guaranteed revenue growth in 7 days"`) was injected.
  The governance layer correctly returned **`block`** (NO_GUARANTEED_CLAIMS gate)
  and claim_safety returned **`BLOCK`**. The unsafe claim never reached an output.
- `governance_blocked` for the customer-facing pack = `False` (no real block on
  delivered drafts; the block applied only to the negative-control probe).

## 9. Blocked / Risks / المخاطر والمحظورات

- The negative-control guaranteed-outcome claim was **BLOCKED** by the
  NO_GUARANTEED_CLAIMS gate — the doctrine guard works.
- One synthetic account (Account-J, lowest rank) was flagged
  `missing_source` + stale (>90 days since contact) and **excluded from outreach
  priority**.
- No external-send risk: `external_use_allowed = False` on the passport; all
  drafts are review-only.

## 10. Value Metrics / مقاييس القيمة

| Metric | Amount | Tier | Note |
|---|---|---|---|
| Duplicate rows detected | 1 | `observed` | Measured in `data_os` dedupe path |
| Accounts scored | 10 | `observed` | Measured in `revenue_os` scoring |
| Pipeline-lift projection | ~not quantified | `estimated` | Range only; never used externally |

No `verified` or `client_confirmed` events: a dry-run has no signed client data.
A `verified`-tier write with no `source_ref` was attempted as a negative control
and was correctly **rejected** by `value_os` tier discipline
(`ValueDisciplineError`).

## 11. Limitations / القيود

**EN —** This is a **hypothetical dry-run on synthetic data**. There is no real
customer, no signed confirmation, and no verified outcomes. All numbers are
either `observed`-in-workflow or `estimated`; **none are `client_confirmed`** and
this pack is **not case-study eligible**. The proof score of 100 reflects
**section completeness only** (`proof_pack_completeness_score` measures the share
of the 14 sections that are non-empty); it does **not** measure the strength of
the underlying evidence. A real engagement would not reach the `case_candidate`
band on completeness alone — see the Delivery Dry-Run Report for this gap.

**AR —** هذا تشغيل تجريبي افتراضي على بيانات اصطناعية. الدرجة 100 تعكس اكتمال
الأقسام فقط، لا قوة الأدلة. هذه الحزمة غير مؤهلة لدراسة حالة.

## 12. Recommended Next Step / الخطوة التالية الموصى بها

For a **real** engagement: collect a signed Source Passport from the customer,
import the real CRM export, and convert `observed` metrics to `verified` via a
customer cross-check before any external claim is made. Queue any external send
through `approval_center` for founder approval.

## 13. Retainer / Expansion Path / مسار التوسّع

On a real engagement reaching `proof_score ≥ 80` **and** `adoption_score ≥ 70`
with a named workflow owner, the **Managed Ops retainer (2,999 SAR/mo)** is the
expansion path. This dry-run is **not eligible** —
`adoption_os.retainer_readiness.evaluate` returned `eligible = False`, recommended
offer `proof_pilot`, gaps: `adoption_score_below_70`, `workflow_owner_missing`
(expected for a synthetic run with no live adoption signal).

## 14. Capital Assets Created / الأصول الرأسمالية المُنشأة

| Asset ID | Type | Reusable | Description |
|---|---|---|---|
| `cap_b8719e5d0178` | `scoring_rule` | Yes | Saudi marketing-agency ICP sector/city scoring profile used in Day 3, reusable across agency-sector engagements |

Registered via `capital_os.capital_ledger.add_asset`. Minimum of 1 reusable
capital asset per engagement — satisfied.

---

*Hypothetical / case-safe dry-run. Internal-only. No customer name, no PII, no
external send, no charge. Produced 2026-05-18 to verify Rung 0–1 delivery
readiness.*

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
