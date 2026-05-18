# Delivery Ledger

Every **client-facing artifact** ships through QA + governance, then lands here. IDs: `O-###`.

## Rule

Outputs must be:

- **QA scored**
- **Governance checked**
- **Logged**
- **Tied** to proof pack ID / path

| ID | Client | Service | Output | Date | QA Score | Governance | Delivered | Notes |
|----|--------|---------|--------|------|----------|------------|-----------|-------|
| O-001 | Client A | Lead Intelligence | Executive Report | | 91 | Pass | Yes | |
| O-002 | Client A | Lead Intelligence | Outreach Drafts | | 88 | Draft-only | Yes | |
| O-DR1 | SYNTHETIC (dry run) | Revenue Intelligence Sprint | Sample Proof Pack | 2026-05-18 | 100 | Pass (allow_with_review) | N/A — dry run, no send | Workstream H rehearsal on synthetic data. Artifact: [`../sales-kit/SAMPLE_PROOF_PACK_DEMO.md`](../sales-kit/SAMPLE_PROOF_PACK_DEMO.md). All 8 sprint steps passed; time-to-proof 0.22s; 1 capital asset registered; retainer not eligible (adoption 0). NOT a real customer. |

Link: [`../delivery/DELIVERY_DECISION.md`](../delivery/DELIVERY_DECISION.md), workbench `05_outputs/`.
