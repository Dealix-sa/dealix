# Trust Control System

## Purpose
Govern every Dealix interaction so that promises are honest, AI outputs are reviewed, and customer data is handled responsibly.

## Principles
- No guaranteed sales or revenue claims.
- Every AI-assisted output is human-reviewed before it leaves Dealix.
- Customer data never enters the public repo.
- Approvals are recorded, not assumed.

## Layers

### 1. Claims Layer
- Marketing, sales, and proposal content avoids guarantee language.
- Trust notes are appended to samples, proposals, and delivery reports.
- The doctrine verifier blocks language that breaches the trust standard.

### 2. AI Output Layer
- Outputs that touch a customer (DMs, emails, proposals, samples, reports) pass a human review.
- Edits are recorded in the daily execution log when material.
- Map → Measure → Manage → Govern flow per NIST AI RMF.

### 3. Data Layer
- No client data, leads, or contacts in public files or commits.
- Private records live in `dealix-ops-private/` only.
- Pre-commit and gitleaks scans guard the public repo.

### 4. Approval Layer
- Material customer-facing actions land in `founder/approvals_waiting.md`.
- Approvals require the founder's explicit recording.
- Approval queue is reviewed once per day as part of the daily gate.

### 5. Incident Layer
- Any trust incident is logged with date, surface, harm, fix.
- Incidents trigger one playbook update.

## Daily Trust Gate
The founder confirms:
1. Approvals queue reviewed.
2. No guarantee language was sent today.
3. No customer data left the private repo.
4. AI-assisted outputs were reviewed before send.

## Weekly Trust Gate
The founder confirms:
- Trust incidents (if any) are logged and addressed.
- Doctrine and trust verifiers pass.
- One playbook updated based on this week's evidence.

## Evidence
- `docs/00_constitution/`
- `docs/trust/`
- `dealix-ops-private/founder/approvals_waiting.md`
- `dealix-ops-private/learning/weekly_intelligence_review.md`

## Last Reviewed
2026-05-23
