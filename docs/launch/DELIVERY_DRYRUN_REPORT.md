# Delivery Dry-Run Report — Rung 0–1 Readiness / تقرير التشغيل التجريبي

> **HYPOTHETICAL / CASE-SAFE DRY-RUN — نموذج افتراضي**
>
> Purpose: prove the Dealix delivery machine works and measure Time-to-Proof
> **before** the first real paying customer. Run on synthetic data only — no
> real customer, no PII, no external send, no charge.
>
> Freeze compliance: this exercise is the "Rung 0–1 delivery finish" + "Proof
> Pack assembly" work explicitly **permitted** by `docs/ops/COMMERCIAL_FREEZE.md`.

**Run date:** 2026-05-18
**Engagement:** 7-Day Revenue Intelligence Sprint (Rung 1, 499 SAR tier)
**Customer handle:** `DRYRUN-AGENCY-A` (synthetic Saudi marketing agency)
**Engagement ID:** `ENG-DRYRUN-RUNG1-001`

---

## 1. Headline Result / النتيجة الرئيسية

| Question | Answer |
|---|---|
| Did the machine produce a Proof Pack? | **Yes** — 14/14 sections assembled |
| Proof score | **100 / 100** |
| Proof tier / band | **`case_candidate`** (completeness band) |
| Score ≥ 70? | **Yes** |
| Data Quality score | **96.0 / 100** |
| Doctrine guards held? | **Yes** — unsafe-claim BLOCK, value-tier discipline, no-external-send all enforced |
| **Go / No-Go verdict (Rung 0–1 delivery readiness)** | **GO** — with the gaps in Section 4 logged and tracked |

The Proof Pack is at
[`docs/assets/proof_packs/DRYRUN_RUNG1_PROOF_PACK.md`](../assets/proof_packs/DRYRUN_RUNG1_PROOF_PACK.md).

## 2. Time-to-Proof / الزمن حتى الدليل

| Measure | Value |
|---|---|
| Automated compute (wall clock, Passport→Proof Pack) | **< 1 second** |
| Calendar Time-to-Proof — the real metric | **7 working days** (the Rung 1 sprint is a 7-day engagement by design) |

**Interpretation.** The *software* path — Source Passport validation → DQ score →
account scoring → draft pack → governance check → 14-section Proof Pack assembly —
is effectively instantaneous. Time-to-Proof is therefore **not constrained by
compute**; it is constrained by the human-paced 7-day sprint cadence: customer
data handoff, founder review of drafts, customer review call, and the consent /
approval gates. Realistic first-customer Time-to-Proof: **7 calendar days**, of
which the machine contributes seconds.

## 3. What Worked / ما الذي نجح

- **Source Passport gate** — `data_os.source_passport.validate` accepted a
  well-formed synthetic passport (`is_valid = True`) and would BLOCK an invalid
  one.
- **Data Quality score** — `data_os.compute_dq` produced a real 0–100 score
  (96.0) with four transparent sub-scores; the deliberate near-duplicate row
  correctly pulled `duplicate_inverse` down to 90.0.
- **Account scoring** — `revenue_os.scoring.score_account_row` ranked all 10
  accounts deterministically with human-readable reasons and risks. The weak
  synthetic row (no source, stale) correctly fell to rank 10 with
  `missing_source` + `incomplete_row` risks.
- **Bilingual draft pack** — `revenue_os.draft_pack` produced AR+EN email,
  LinkedIn, and call-script drafts, all draft-only / review-required.
- **Governance** — every draft passed `governance_os.runtime_decision.decide`
  and `claim_safety`; the **negative-control unsafe claim was correctly BLOCKED**
  by the NO_GUARANTEED_CLAIMS gate.
- **Value-tier discipline** — `value_os` recorded `observed` and `estimated`
  events, and **rejected** a `verified` write with no `source_ref`
  (`ValueDisciplineError`). No tier auto-promotion.
- **Friction log** — 3 friction events emitted and PII-sanitized via the
  canonical redactor.
- **Capital asset** — 1 reusable `scoring_rule` asset registered (minimum met).
- **Proof Pack** — all 14 canonical v2 sections assembled and scored.

## 4. Friction / Gaps Found / الاحتكاك والثغرات

Recorded to the friction log (`auto_client_acquisition/friction_log`). **No
product code was changed** — per the brief, gaps are reported, not fixed.

| # | Severity | Gap | Impact | Recommendation |
|---|---|---|---|---|
| G1 | HIGH | **Import cascade pulls heavyweight stack.** Importing canonical package `__init__.py` files (`data_os`, `revenue_os`, …) transitively pulls `core.llm.router`, `httpx`, `pydantic`, `pydantic-settings`. A clean delivery environment cannot `import auto_client_acquisition.data_os` without the full app stack installed. | A delivery operator on a minimal box hits `ModuleNotFoundError`. The dry-run had to load OS code via direct leaf-module imports to stay hermetic. | Either add the missing deps to `requirements.txt` for delivery boxes, or decouple the canonical-module `__init__.py` files from `core.llm` / agent imports. |
| G2 | MED | **`proof_os` has no `assemble()` entry point.** The playbook references `proof_os.assemble(engagement_id, customer_id, source_passport, dq_score, value_events, governance_events, …)`. The actual surface is `build_empty_proof_pack_v2` + `merge_proof_pack_v2` + `proof_pack_completeness_score` + `proof_strength_band`. | Proof Pack assembly had to be hand-composed from primitives; no single audited orchestration function. | Add a thin `proof_os.assemble(...)` orchestrator (a wrapper, not new logic) so delivery is one documented call. |
| G3 | MED | **Proof score measures completeness only.** `proof_pack_completeness_score` returns the share of the 14 sections that are non-empty. A pack with all sections filled scores 100 / `case_candidate` regardless of evidence strength. The dry-run scored 100 on synthetic data. | A weak engagement could *look* case-ready on score alone. The `case_candidate` band name overstates a completeness-only metric. | Treat proof score as a **completeness gate**, not an evidence-strength signal. Gate `case_candidate` on `client_confirmed` value events existing, not just on section fill. |
| G4 | LOW | **`CapitalAssetType` enum is missing 2 of the 8 taxonomy types.** The enum has 6 members; `qa_rubric` and `arabic_style_pattern` from the doctrine taxonomy are absent. `add_asset` accepts plain strings, so it still works. | A typo'd asset type would not be caught by the enum. | Add `QA_RUBRIC` and `ARABIC_STYLE_PATTERN` to `capital_os.asset_types.CapitalAssetType`. |
| G5 | LOW | **Account scorer saturates at 100.** 9 of 10 synthetic accounts scored exactly 100; the scorer's points sum is clamped to 100, so well-formed rows are indistinguishable at the top. | Top-of-list ranking gives no tie-break signal for "best of the best". | Acceptable for Rung 1 (the goal is a ranked shortlist, not fine-grained ordering). Consider a tie-break component if a real customer needs strict ordering. |

## 5. Doctrine Guard Check / فحص ضوابط العقيدة

| Guard | Result |
|---|---|
| No external send without approval | Held — all drafts draft-only; `external_use_allowed = False` |
| No cold WhatsApp / LinkedIn / scraping | Held — `draft_pack` enforces doctrine; LinkedIn output is a draft only |
| No fake / guaranteed claims | Held — negative-control claim BLOCKED by NO_GUARANTEED_CLAIMS gate |
| No PII in proof ledger / friction summaries | Held — synthetic data has no PII; friction notes pass `redact_text` |
| No tier auto-promotion in value ledger | Held — `verified` write without `source_ref` rejected |
| No engagement close without Proof Pack + ≥1 Capital Asset | Held — 14-section Proof Pack + 1 `scoring_rule` asset |
| Commercial Freeze respected | Held — only Rung 0–1 delivery + Proof Pack assembly; no Rung 2–5 build, no new product code |

**No doctrine guard failed.** The gaps in Section 4 are ergonomics / packaging
issues, not doctrine violations.

## 6. Go / No-Go Verdict / قرار المضي

**Verdict: GO for Rung 0–1 delivery readiness.**

The delivery machine ran the full 7-day Sprint playbook end-to-end on synthetic
data and produced a scored 14-section Proof Pack with every doctrine guard
holding. The machine works.

**Conditions attached:**

1. **G1 (HIGH)** must be resolved before a delivery operator runs this on a
   clean box — either ship the deps or decouple the imports. Until then, the
   delivery runbook must pin the environment.
2. **G3 (MED)** — communicate internally that proof score is a *completeness*
   gate, not an evidence-strength score. Do not show a real customer a "100 /
   case_candidate" pack as if it were verified proof.
3. G2, G4, G5 are tracked but do not block the first paid pilot.

**Time-to-Proof to expect with the first real customer: 7 calendar days**, with
the software contributing seconds and the human review / consent cadence
contributing the rest.

---

*Hypothetical / case-safe dry-run. No real customer, no PII, no external send, no
charge. The run script and JSON summary are kept outside the repo (`/tmp`) and
are not committed.*

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
