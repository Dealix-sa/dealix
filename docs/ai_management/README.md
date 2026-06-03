# AI Management

## Purpose
Govern how AI is used across Dealix - which models, which data, which risks, and how the company stays inside trust and regulatory boundaries.

## Owner
Sami / Trust owner.

## Review Cadence
Monthly, plus after any incident or material capability change.

## Inputs
- Model and provider inventory.
- Data classification and flow maps.
- Use-case register (where AI is used in the company).
- Trust OS Approval Matrix and Autonomy Policy.
- External regulation and customer requirements.

## Outputs
- Approved model and provider list.
- Use-case register with risk class per use case.
- Data-flow rules (what data may go to which provider).
- Logging, monitoring, and incident response policy.

## Rules
- New AI use cases require risk classification before launch.
- High-risk use cases (legal, financial, sensitive personal data) require A2 founder approval.
- A3 actions (full compliance claims, guaranteed revenue, legal commitments) are never AI-executed.
- Data sent to external providers is governed by data classification and customer agreements.
- Model and prompt changes affecting customer outputs are versioned and reviewed.

## Metrics
- Number of AI use cases in production by risk class.
- Incidents per quarter (rate and severity).
- Time to detect and respond to an AI incident.
- % of high-risk use cases with current approval on file.

## Evidence
- use-case register in this folder.
- model/provider inventory.
- incident response log.
- trust/approval_log.csv.
- evaluation results.

## Last Reviewed
YYYY-MM-DD
