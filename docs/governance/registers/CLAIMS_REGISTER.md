# Claims Register / سجل الادّعاءات

**Purpose:** A single, auditable list of every external-facing claim Dealix
makes, with the evidence that backs it. If a claim is not in this register
with verified evidence, it may **not** be used in sales, marketing, the
website, or a Proof Pack.

**Related:** [`../../37_saudi_layer/FORBIDDEN_ARABIC_CLAIMS.md`](../../37_saudi_layer/FORBIDDEN_ARABIC_CLAIMS.md) ·
[`../APPROVAL_POLICY.md`](../APPROVAL_POLICY.md) ·
[`../../03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md`](../../03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md)

## Rules / القواعد
- **No source → no claim.** Every row needs checkable evidence.
- No guaranteed-revenue or guaranteed-outcome wording.
- No customer name without written publication consent.
- No future/unbuilt module described as live.
- Status `verified` is required before a claim goes external (A3/A4).

## Register / السجل
| # | Claim / الادّعاء | Type | Evidence / الدليل | Status | Owner | Last reviewed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Dealix runs a 7-day Command Sprint that produces a Proof Pack | capability | `customers/_template/`, `scripts/run_dealix_e2e_dry_run.py` | verified | founder | 2026-06-06 |
| 2 | All external actions are approval-gated | governance | `docs/03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md` | verified | founder | 2026-06-06 |

## Forbidden phrasing / صياغات ممنوعة
- "Guaranteed", "نضمن", "مضمون" tied to revenue or outcomes.
- "Used by <named customer>" without consent on file.
- "Live now" for anything not actually shipped.
