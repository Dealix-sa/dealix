# 7-Day Revenue Proof Sprint — Delivery Runbook | دليل تشغيل سبرنت إثبات الإيراد

<!-- Workstream D — Tier 0-1 Delivery Machine. Owner: Founder. Created: 2026-05-18 -->
<!-- Scope: tier-1 delivery finish (permitted under docs/ops/COMMERCIAL_FREEZE.md). -->
<!-- Source of truth for product claims: docs/CANONICAL_PRODUCT_NARRATIVE.md -->

> **Purpose.** This runbook makes the 499 SAR 7-Day Revenue Proof Sprint
> push-button: once a deal is closed, every step below is executed in order,
> writes to a real ledger, and produces an evidenced Proof Pack.
>
> **الغرض.** يجعل هذا الدليل تسليم سبرنت الإيراد (499 ريال) قابلاً للتنفيذ
> بضغطة زر: بمجرد إغلاق الصفقة تُنفَّذ كل خطوة بالترتيب، وتُكتب إلى سجل حقيقي،
> وتُنتج Proof Pack مدعوماً بالأدلة.

---

## 0. Doctrine guardrails — non-negotiable | الضوابط غير القابلة للتفاوض

These hold at **every** step. A step that would violate one of them STOPS and
escalates to the founder. They are enforced in code, not just policy.

1. No external message is sent by Dealix. Drafts only. The founder sends.
2. No auto-booking of meetings.
3. No guaranteed-outcome claims (`governance_os.claim_safety` REDACTS / BLOCKS).
4. No scraping, no LinkedIn automation, no cold WhatsApp, no purchased lists.
5. No PII in `proof_ledger` summaries — text is sanitized before it is stored.
6. No engagement closes without a Proof Pack **and** ≥ 1 Capital Asset.
7. Value-ledger tiers are never auto-promoted (estimated → observed → verified
   → client_confirmed only on real evidence).
8. Every human override is recorded to `friction_log`.
9. External sends queue through `approval_center` — never direct.
10. `verified` value events require a `source_ref`; `client_confirmed` requires
    a signed `confirmation_ref`.
11. Estimated value is never presented to the customer as achieved value.

> **Freeze note.** This is a tier-1 *delivery* runbook (permitted). It builds no
> new product code, no new `*_os` modules, no rung 2-5 capability.

---

## 1. The pipeline at a glance | المسار العام

```
Day 1  Kickoff + Source Passport ........ data_os.source_passport
Day 2  Data import + DQ score ........... data_os.import_preview + data_quality_score
Day 3  Account scoring (top 10) ......... revenue_os.account_scoring
Day 4  Draft generation + governance .... revenue_os.draft_pack + governance_os.decide
Day 5  Proof Pack assembly ............. proof_os (14 sections) + proof_score
Day 6  Founder handoff review .......... proof_score band gate
Day 7  Capital asset + retainer ........ capital_os.add_asset + adoption_os.retainer_readiness
```

Cross-cutting throughout: `value_os.add_event` for every measurable outcome,
`friction_log.emit` for every human override.

---

## 2. Pre-flight (Day 0) — deal closed | قبل الانطلاق

| Item | Detail |
|---|---|
| Trigger | 499 SAR payment confirmed (Moyasar) + signed pilot scope |
| Create | `customer_id` and `engagement_id` (format `eng_<customer>_<seq>`) |
| Owner | Founder |
| Ledger | none yet — IDs only |
| Output | engagement record; Day-1 kickoff scheduled within 24h |

---

## 3. Day-by-day steps | الخطوات يوماً بيوم

### Day 1 — Kickoff + Source Passport

| Field | Value |
|---|---|
| **Inputs** | Customer pipeline-data description; data owner; intended use; PII flag; sensitivity; retention; AI-access + external-use permissions |
| **Action** | Build a `SourcePassport`; run `data_os.source_passport.validate(passport)` |
| **Module** | `auto_client_acquisition/data_os/source_passport.py` |
| **Outputs** | `SourcePassportValidation` (`is_valid`, `reasons`, `missing`) |
| **Ledger written** | Passport recorded for the `source_passports` Proof Pack section (Day 5) |
| **Owner** | Founder |
| **Gate** | If `is_valid == False` → **BLOCK**. Send the customer the `missing`/`reasons` list and request a corrected data-handling answer. Do not proceed. |
| **Friction** | If the founder had to override or hand-edit a passport field → `friction_log.emit(customer_id, kind="data_passport", severity=..., notes=...)` |

### Day 2 — Data import + DQ score

| Field | Value |
|---|---|
| **Inputs** | Customer pipeline file (CSV / export). SYNTHETIC or customer-provided only — never scraped |
| **Action** | `data_os.import_preview.preview(raw_csv)` → `data_os.data_quality_score.compute_dq_from_preview(preview)` |
| **Modules** | `auto_client_acquisition/data_os/import_preview.py`, `data_os/data_quality_score.py` |
| **Outputs** | `DataQualityScore` — `overall`, `completeness`, `duplicate_inverse`, `format_consistency`, `source_clarity` |
| **Ledger written** | DQ result → Proof Pack `quality_scores` section. Duplicates removed → `value_os.add_event(kind="duplicates_removed", tier="observed")` |
| **Owner** | Founder |
| **Gate** | If `overall < 70` → founder reviews DQ before scoring; decide repair vs. proceed-with-caveat. Record the decision. |
| **Friction** | DQ-driven founder review → `friction_log.emit(kind="data_quality", severity="medium", ...)` |

### Day 3 — Account scoring (top 10)

| Field | Value |
|---|---|
| **Inputs** | Cleaned account rows from Day 2 |
| **Action** | Score each row with `revenue_os.account_scoring.score_account_row(row)`; rank; take top 10 |
| **Module** | `auto_client_acquisition/revenue_os/account_scoring.py` (re-exported as `revenue_os.score_account_row`) |
| **Outputs** | Per account: `score`, `reasons`, `risks`, `components`. Top 10 ranked list |
| **Ledger written** | Ranked list → Proof Pack `outputs` section. Each account carries explicit `reasons` |
| **Owner** | Founder reviews the ranking |
| **Rule** | Every account in the top 10 MUST have a non-empty `reasons` list. In customer-facing output the accounts are anonymized (Account A, B, C …) unless the customer's own data is shown back to them privately |
| **Friction** | Manual re-rank or score override → `friction_log.emit(kind="scoring_override", ...)` |

### Day 4 — Draft generation + governance

| Field | Value |
|---|---|
| **Inputs** | Top-ranked account rows from Day 3 |
| **Action** | `revenue_os.draft_pack.build_revenue_draft_pack(top_account_row)` → AR + EN email, call script, follow-up plan. Then for **every** draft: `governance_os.runtime_decision.decide(action="generate_draft", context={"text": draft})` |
| **Modules** | `auto_client_acquisition/revenue_os/draft_pack.py`, `governance_os/runtime_decision.py`, `governance_os/claim_safety.py` |
| **Outputs** | 5 governed drafts (AR + EN), each with a `RuntimeDecision` |
| **Ledger written** | Every governance decision → Proof Pack `governance_decisions` section; any block → `blocked_risks` section |
| **Owner** | Founder |
| **Gate** | If `decide(...)` returns `block` OR `audit_claim_safety(text).suggested_decision == BLOCK` → **REDACT** the unsafe claim, regenerate the draft, re-run the check. A draft never leaves the redact loop until clean. Drafts are **draft-only** — they are queued in `approval_center`, never sent by Dealix |
| **Friction** | Any redact loop or manual rewrite → `friction_log.emit(kind="draft_redaction", ...)` |

> **Coverage note (see WS-D_VERIFICATION).** `governance_os.decide` reliably
> blocks Arabic guaranteed-claim phrasing and the English `guaranteed`
> adjective forms, but the founder MUST still read every English draft for
> verb-form promises ("we guarantee …"). Treat the automated gate as a floor,
> not a ceiling.

### Day 5 — Proof Pack assembly

| Field | Value |
|---|---|
| **Inputs** | Source Passport (D1), DQ score (D2), ranked accounts (D3), governed drafts + decisions (D4), value events, friction events |
| **Action** | `proof_os.build_empty_proof_pack_v2()` → fill all 14 sections → `merge_proof_pack_v2(...)`; then `proof_os.proof_pack_completeness_score(...)` and `proof_strength_band(...)` |
| **Modules** | `auto_client_acquisition/proof_os/proof_pack.py`, `proof_os/proof_score.py` (14 sections in `proof_architecture_os/proof_pack_v2.py`) |
| **Outputs** | A 14-section Proof Pack + integer `proof_score` (0-100) + band |
| **Ledger written** | The assembled Proof Pack is the deliverable record for the engagement |
| **Owner** | Founder |
| **Gate** | If any governance BLOCK is unresolved, use `proof_pack_score_with_governance_penalty(..., governance_blocked=True)` which caps the score at 69 — a blocked pack cannot present as case-ready |
| **14 sections** | `executive_summary`, `problem`, `inputs`, `source_passports`, `work_completed`, `outputs`, `quality_scores`, `governance_decisions`, `blocked_risks`, `value_metrics`, `limitations`, `recommended_next_step`, `retainer_expansion_path`, `capital_assets_created` |

### Day 6 — Founder handoff review

| Field | Value |
|---|---|
| **Inputs** | Assembled Proof Pack + score from Day 5 |
| **Action** | Founder reviews the Proof Pack against the customer's signed scope |
| **Outputs** | Decision: deliver or revise |
| **Ledger written** | Handoff decision noted on the engagement record |
| **Owner** | Founder |
| **Gate** | `proof_score >= 70` → deliver to customer. `proof_score < 70` → revise (return to the weakest section's source step) and re-assemble. No engagement closes below 70 |
| **Friction** | A revise loop → `friction_log.emit(kind="proof_revision", ...)` |

### Day 7 — Capital asset + retainer eligibility

| Field | Value |
|---|---|
| **Inputs** | Closed Proof Pack; adoption signals; proof_score |
| **Action** | Register ≥ 1 reusable artifact via `capital_os.add_asset(customer_id, engagement_id, asset_type, ...)`. Then `adoption_os.retainer_readiness.evaluate(customer_id, adoption_score, proof_score, workflow_owner_present, governance_risk_controlled)` |
| **Modules** | `auto_client_acquisition/capital_os/capital_ledger.py`, `capital_os/asset_types.py`, `adoption_os/retainer_readiness.py` |
| **Outputs** | `CapitalAsset` record(s); `RetainerReadiness` (`eligible`, `recommended_offer`, `gaps`) |
| **Ledger written** | Capital ledger (asset) + Proof Pack `capital_assets_created` section |
| **Owner** | Founder |
| **Gate** | Engagement cannot close with 0 capital assets. If `eligible == True` → present the 2,999 SAR/mo Managed Ops offer. If `False` → share `gaps` with the customer, do not pitch the retainer |
| **Asset taxonomy** | Choose from the 6 types in `CapitalAssetType`: `scoring_rule`, `draft_template`, `governance_rule`, `proof_example`, `sector_insight`, `productization_signal` |

---

## 4. Cross-cutting ledgers | السجلات المستعرضة

| Ledger | Module | When written |
|---|---|---|
| Value ledger | `value_os/value_ledger.py` (`add_event`) | Every measurable outcome, with tier |
| Friction log | `friction_log/store.py` (`emit`) | Every human override; notes auto-sanitized |
| Capital ledger | `capital_os/capital_ledger.py` (`add_asset`) | Day 7, ≥ 1 reusable asset |
| Proof Pack | `proof_os/proof_pack.py` | Day 5 assembly, 14 sections |

### Value-ledger tier discipline

| Tier | Use | Requirement |
|---|---|---|
| `estimated` | internal only; never shown to customer as achieved | range, no source |
| `observed` | measured inside the Dealix workflow (e.g. 17 dupes removed) | internal reports |
| `verified` | cross-checked against customer data | `source_ref` REQUIRED |
| `client_confirmed` | signed confirmation; case-study eligible | `confirmation_ref` REQUIRED |

Tiers are never auto-promoted. `value_ledger` raises `ValueDisciplineError`
if a `verified` event lacks `source_ref` or a `client_confirmed` event lacks
`confirmation_ref`.

---

## 5. Roles | الأدوار

| Role | Responsibility |
|---|---|
| Founder | Owns every step, every gate, every external send. Sole approver |
| Dealix system | Drafts, scores, assembles, ledgers. Sends nothing |
| Customer | Provides data + Source Passport answers; reviews; signs confirmations |

---

## 6. Done definition | تعريف الإنجاز

The Sprint is delivered when ALL hold:

- [ ] Source Passport validated (Day 1).
- [ ] DQ score computed; if < 70, founder-reviewed (Day 2).
- [ ] Top 10 accounts ranked, each with reasons (Day 3).
- [ ] 5 drafts generated; every draft passed governance / redacted clean (Day 4).
- [ ] 14-section Proof Pack assembled; `proof_score >= 70` (Day 5-6).
- [ ] ≥ 1 Capital Asset registered (Day 7).
- [ ] Retainer eligibility evaluated; offer presented only if eligible (Day 7).
- [ ] Value events recorded with correct tiers; friction events logged.

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
