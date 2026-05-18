# Sprint Proof Pack — Format & Evidence Standard | معيار Proof Pack

<!-- Workstream D — Tier-1 Proof Pack format. Owner: Founder. Created: 2026-05-18 -->
<!-- Code surface: auto_client_acquisition/proof_os/ + proof_architecture_os/proof_pack_v2.py -->
<!-- Source of truth for product claims: docs/CANONICAL_PRODUCT_NARRATIVE.md -->

> **What this is.** The format of the Proof Pack delivered at the end of the
> 499 SAR 7-Day Revenue Proof Sprint. It is the customer-facing evidence
> artifact and the freeze's exit condition (a customer-approved Proof Pack at
> evidence level L3+). It has exactly **14 canonical sections**.
>
> **ما هذا.** صيغة الـ Proof Pack المُسلَّم في نهاية سبرنت الـ499 ريال. هو
> أصل الأدلة الموجَّه للعميل، وشرط الخروج من التجميد.

---

## 1. Structure — the 14 canonical sections | البنية

Defined in code at
`auto_client_acquisition/proof_architecture_os/proof_pack_v2.py`
(`PROOF_PACK_V2_SECTIONS`). All 14 are mandatory; an empty section lowers the
score.

| # | Section key | Content | Bilingual |
|---|---|---|---|
| 1 | `executive_summary` | What was done, what was found, the headline outcome | AR + EN |
| 2 | `problem` | The revenue-ops problem the customer brought | AR + EN |
| 3 | `inputs` | Data the customer provided (described, not pasted) | AR + EN |
| 4 | `source_passports` | Each Source Passport + its `validate()` result | AR + EN |
| 5 | `work_completed` | The 7-day step log (Passport → Retainer) | AR + EN |
| 6 | `outputs` | Top 10 ranked accounts (anonymized) + the 5 drafts | AR + EN |
| 7 | `quality_scores` | DQ score breakdown + Proof score | AR + EN |
| 8 | `governance_decisions` | Every `governance_os.decide` result | AR + EN |
| 9 | `blocked_risks` | Anything blocked / redacted and why | AR + EN |
| 10 | `value_metrics` | Value events with explicit tier labels | AR + EN |
| 11 | `limitations` | What was NOT done; data caveats | AR + EN |
| 12 | `recommended_next_step` | The single best next move | AR + EN |
| 13 | `retainer_expansion_path` | Retainer eligibility result + path | AR + EN |
| 14 | `capital_assets_created` | Reusable assets registered this engagement | AR + EN |

Assemble with `proof_os.build_empty_proof_pack_v2()` →
`proof_os.merge_proof_pack_v2(base, updates)`.

---

## 2. Score & tier | الدرجة والتصنيف

| Function | Result |
|---|---|
| `proof_os.proof_pack_completeness_score(sections)` | integer 0-100 = share of non-empty sections |
| `proof_os.proof_strength_band(score)` | band name |
| `proof_os.proof_pack_score_with_governance_penalty(sections, governance_blocked=True)` | caps score at 69 when a governance BLOCK is unresolved |

**Bands:**

| Score | Band | Meaning |
|---|---|---|
| ≥ 85 | `case_candidate` | eligible to seed a case study (only with `client_confirmed` value) |
| 70-84 | `sales_support` | usable in sales conversations |
| 55-69 | `internal_learning` | internal only |
| < 55 | `weak_proof` | not deliverable |

**Delivery gate:** a Proof Pack is delivered to the customer only at
`proof_score >= 70`. Below 70 → revise (return to the weakest section's source
step) and re-assemble. This matches Day 6 of `SPRINT_RUNBOOK_7DAY.md`.

---

## 3. Evidence requirements | متطلبات الأدلة

Every claim in the pack must trace to a step that produced it:

| Section | Evidence it must carry |
|---|---|
| `source_passports` | The passport fields + `SourcePassportValidation` outcome |
| `quality_scores` | `DataQualityScore` components, not just a headline number |
| `outputs` | Account `reasons` per account; drafts shown verbatim |
| `governance_decisions` | The `RuntimeDecision` for every draft |
| `blocked_risks` | The trigger reason for every block / redaction |
| `value_metrics` | Each event's `kind`, `amount`, `unit`, and **tier** |
| `capital_assets_created` | `asset_id` + `asset_type` from the capital ledger |

A pack assembled from prose alone (no traceable step) is invalid — see the
anti-patterns in `dealix/masters/evidence_pack_spec.md` §10.

---

## 4. Estimate-vs-verified discipline | انضباط التقدير مقابل التحقّق

This is the load-bearing rule of the `value_metrics` section.

| Tier | May appear in customer Proof Pack? | Requirement |
|---|---|---|
| `estimated` | **Internal labelling only.** If shown, it MUST be labelled "estimated / تقديري" and never as an achieved result | range, no source |
| `observed` | Yes — measured inside the Dealix workflow (e.g. "17 duplicate rows removed") | internal measurement |
| `verified` | Yes — cross-checked against the customer's own data | `source_ref` REQUIRED |
| `client_confirmed` | Yes, and case-study eligible | signed `confirmation_ref` REQUIRED |

Rules:

- **Tiers are never auto-promoted.** An estimated number does not become
  observed because the founder believes it; it is promoted only on real
  evidence. `value_os.value_ledger` raises `ValueDisciplineError` if a
  `verified` event has no `source_ref` or a `client_confirmed` event has no
  `confirmation_ref`.
- A 499 SAR Sprint typically ends with `observed` and `estimated` events; a
  `verified` or `client_confirmed` value usually appears only after the
  customer confirms in writing — that is what makes a Proof Pack
  case-study-eligible (L3+) and is the freeze exit condition.
- The footer of every pack states: *Estimated value is not Verified value.*

---

## 5. Doctrine constraints on the pack | قيود الدوكترين

- **No PII in summaries.** Names, emails, phone numbers, national IDs are
  redacted before storage (`friction_log/sanitizer.py` style sanitization);
  the customer's own data is described, not pasted.
- **No guaranteed-outcome claims** anywhere in the 14 sections —
  `governance_os.claim_safety.audit_claim_safety` must pass on the assembled
  text; any `forbidden_claim:` hit → BLOCK → redact → reassemble.
- **Anonymized accounts** in `outputs` (Account A, B, C …) for any version that
  may travel beyond the customer; the customer's private copy may show their
  own names.
- **Drafts are drafts.** The pack states explicitly that no message was sent by
  Dealix and that the founder approves every send.

---

## 6. Output & handoff | التسليم

- Canonical format: structured sections (JSON-backed), rendered to a
  bilingual one-document Proof Pack (HTML / PDF) for founder handoff.
- Arabic PDF respects RTL and Gulf business typography.
- Export of a Proof Pack is an S2+ action (customer commercial data) and is
  logged — see `dealix/masters/evidence_pack_spec.md` §8.
- Delivered at Day 6 once `proof_score >= 70` and the founder has reviewed it.

---

## 7. Assembly checklist | قائمة التجميع

- [ ] All 14 sections non-empty.
- [ ] Section 4 carries each Source Passport + its validation outcome.
- [ ] Section 7 shows DQ component breakdown, not just a headline.
- [ ] Section 8 lists every governance decision; Section 9 lists every block.
- [ ] Section 10 labels every value event with its tier; no estimated value
      presented as achieved.
- [ ] Section 14 names ≥ 1 registered capital asset.
- [ ] Claim-safety check passes on the full assembled text.
- [ ] No PII in any summary; accounts anonymized where the pack may travel.
- [ ] `proof_score >= 70`; governance penalty applied if any block is open.
- [ ] Bilingual AR + EN throughout; footer disclaimer present.

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
