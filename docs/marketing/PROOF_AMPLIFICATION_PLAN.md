# Proof Amplification Plan

How a stored, approved proof item becomes a public asset.

## Path

`proof/proof_library.csv` (approved) → `marketing/content_ideas.csv` (drafted) → `marketing/content_calendar.csv` (scheduled) → publish.

## Forms

- Anonymous benchmark snippet (no customer name)
- Named case study (requires `proof_approval_queue.csv` row marked approved with `customer_consent = true`)
- Joint webinar (requires customer approval + legal review)
- Press release (requires founder + legal approval)

## Guardrails

- No proof item may be amplified before its row in `proof_approval_queue.csv` reads `approved`.
- Anonymous benchmarks may use ranges only, never single-customer numbers.
- Bilingual parity on every public proof page.
