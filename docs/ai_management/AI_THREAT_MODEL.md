# Dealix AI Threat Model

## Purpose
Identify AI-specific threats before expanding agents and automation.

## Owner
Sami / AI Governance owner.

## Review Cadence
Monthly or before adding new agent capabilities.

## Threats

### 1. Prompt Injection
Risk:
Untrusted input changes agent behavior or bypasses instructions.

Controls:
- do not let agents execute external actions directly.
- separate untrusted content from instructions.
- require approval for external outputs.
- log risky outputs.

### 2. Sensitive Information Disclosure
Risk:
Agent exposes client, lead, payment, or private strategy data.

Controls:
- private data stays in dealix-ops-private.
- public repo boundary checks.
- no real dashboard JSON committed.
- redact outputs before public use.

### 3. Overclaiming
Risk:
Agent writes guaranteed revenue or compliance claims.

Controls:
- claim guard.
- safe language library.
- approval matrix.
- banned terms scan.

### 4. Tool Misuse
Risk:
Agent calls tools or scripts in unsafe sequence.

Controls:
- action router.
- approval router.
- A3 never auto-execute.
- logs and manual review.

### 5. Data Poisoning / Bad Inputs
Risk:
Bad lead data causes bad decisions.

Controls:
- evidence required for A-priority leads.
- QA checklist.
- source validation.
- weekly review.

## Rules
- Agents prepare; humans approve critical moves.
- No A3 action can be autonomous.
- No external claim without evidence.
- No private data in public outputs.

## Metrics
- blocked unsafe outputs.
- trust flags.
- approval escalations.
- AI incidents.
- eval pass rate.

## Evidence
- approval logs.
- evals.
- incident reports.
- public safety checks.
- trust tests.

## Last Reviewed
2026-05-23
