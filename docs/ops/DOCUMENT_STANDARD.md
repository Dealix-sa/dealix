# Dealix Document Standard

Every operating document must include the following sections. Any operating file that is missing **Purpose + Owner + Metrics + Evidence** is considered not ready and will fail the document quality verifier (`scripts/verify_document_quality.py`).

## Purpose
Why this document exists. State the operating role this file plays inside the Dealix Company OS.

## Owner
Who owns this system today. A single human accountable name (founder or designated operator).

## Review Cadence
Daily, weekly, monthly, or quarterly. How often this file is reviewed and refreshed.

## Inputs
What this system needs to operate (signals, data, decisions, or other documents it depends on).

## Outputs
What this system produces (decisions, templates, rules, evidence, or downstream actions).

## Rules
Non-negotiable rules that govern this system. What it must always do, and what it must never do.

## Metrics
How performance is measured. Numbers, ratios, or completion criteria. No vague claims.

## Evidence
What proves this system is working today. Link to files, logs, payments, deliveries, or customer feedback.

## Last Reviewed
YYYY-MM-DD. Updated every time the file is reviewed.

---

## Enforcement

- `scripts/verify_document_quality.py` checks every operating document for the required sections.
- `scripts/fill_empty_docs_with_standard.py` seeds empty markdown files with a minimum-viable template.
- `scripts/verify_company_os_deep.py` enforces deep content checks on the core 12 files.
- CI runs all three on every PR via `.github/workflows/dealix-company-os.yml`.

## Owner
Sami (Founder).

## Review Cadence
Quarterly.

## Inputs
- Operating doctrine changes.
- New systems added to Dealix Company OS.
- Failure modes seen in past audits.

## Outputs
- Updated document standard.
- Adjusted verifier rules.

## Rules
- Public docs must not include private customer data.
- Every operating file must declare an Owner.
- Every operating file must declare Metrics and Evidence.

## Metrics
- Percentage of operating files passing `verify_document_quality.py`.

## Evidence
- Latest CI run on `main` shows all document quality checks passing.

## Last Reviewed
2026-05-23
