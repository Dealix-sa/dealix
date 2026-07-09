# Dealix Full Company OS — Execution Baseline

## Mission

Create a single safe execution spine that lets Dealix run a daily internal operating cycle:

```text
Company Brain
-> Opportunity scoring
-> Draft generation
-> Approval queue
-> Proof log
-> Self-improvement notes
-> Daily command report
```

This baseline does not replace existing Dealix commercial PRs. It creates a small, runnable kernel that can interoperate with the existing work and gives Claude Code / GitHub Actions one safe command to verify.

## Current implementation slice

Branch:

```text
feat/full-company-os-execution
```

Added files:

```text
dealix/full_company_os/__init__.py
dealix/full_company_os/kernel.py
scripts/commercial/run_full_company_os.py
scripts/commercial/verify_full_company_os.py
data/full_company_os/targets.example.json
docs/commercial/FULL_COMPANY_OS_EXECUTION_BASELINE.md
docs/commercial/FULL_COMPANY_OS_IMPLEMENTATION.md
.github/workflows/full-company-os.yml
```

## What this slice intentionally does

- Builds a Company Brain for Dealix.
- Loads safe founder/example targets.
- Scores opportunities.
- Matches offers from the Dealix offer ladder.
- Generates draft messages only.
- Generates founder approval queue items.
- Generates proof events.
- Generates self-improvement recommendations.
- Writes `reports/full_company_os/<date>/` and `reports/full_company_os/latest.*`.

## What this slice intentionally does not do

- No email sending.
- No WhatsApp sending.
- No SMS sending.
- No LinkedIn automation.
- No social posting.
- No payment capture.
- No revenue recognition.
- No production mutation.
- No PR merge automation.
- No secret reading or printing.
- No scraping.
- No fake proof.
- No promised results.

## Why this matters

The existing repo already has several advanced commercial/OS PRs. This slice gives the repo a compact kernel that is easy to run, easy to verify, and safe to use as a shared foundation before expanding or merging larger layers.

## Recommended operating order

1. Stabilize production trust: production smoke, Railway config, OpenSSF/security checks.
2. Close the first manual paid sprint path: payment evidence before revenue.
3. Run client acquisition queue from safe/warm sources.
4. Run this Full Company OS daily command.
5. Review approvals manually.
6. Log proof and learning.
7. Only later add controlled-live execution through a separate approval PR.

## Verification commands

```bash
python scripts/commercial/run_full_company_os.py --client dealix --mode draft-only --limit 10
python scripts/commercial/verify_full_company_os.py
```

## Definition of done for this PR

- Runner generates opportunities, drafts, approvals, proof, improvements, and a daily report.
- Verifier passes.
- Workflow runs in draft-only mode.
- No live outbound, payment, posting, merge, or production mutation behavior is introduced.
