# Approval Matrix — مصفوفة الموافقات A0/A1/A2/A3

## Purpose
Define the four autonomy classes for every action Dealix takes, and the approval required for each. The matrix is the operating rule referenced by every agent, operator, and policy.

## Owner
Founder.

## Inputs
- Action description from the requester.
- Reversibility assessment.
- External-facing flag.

## Outputs
- Routing decision (A0/A1/A2/A3).
- Logged approval (when A2 or A3).

## Rules (numbered)
1. Four classes only: A0 fully autonomous, A1 logged autonomy, A2 reviewed before execution, A3 explicit human approval required.
2. When in doubt, escalate one class up.
3. Any action that touches external parties is at minimum A2.
4. Any irreversible action is A3.
5. A3 approvals are logged with requester, action, decider, timestamp, rationale.
6. Verbal A3 approvals are not valid. Approvals are in writing.
7. A class assignment is reviewed monthly under `docs/trust/AUDIT_POLICY.md`.

## Metrics
- A3 median decision time.
- A3 approval rate.
- A2 actions reviewed within SLA.
- Misclassification incidents per quarter (target 0).

## Cadence
Continuous. Reviewed monthly.

## Evidence (paths)
- `docs/trust/registers/a3_log.md`
- `docs/trust/registers/a2_log.md`

## Verifier
Founder for A3. Head of Delivery for A2.

## Runtime Command
`make trust.approval.route ACTION=<id>` prints the recommended class.

## Class definitions and examples

**A0 — fully autonomous.** Reversible, internal, low blast radius. Examples:
- Drafting an internal markdown note.
- Running a schema validation script.
- Computing scores on a research row using published rubrics.
- Scaffolding a sprint folder.

**A1 — logged autonomy.** Reversible, internal, but the log matters for audit. Examples:
- Adding a row to the lead table.
- Updating a sector note.
- Drafting a message variant for QA.
- Updating an internal checklist.

**A2 — reviewed before execution.** Reversible but consequential, or touching external-facing artifacts that have not yet been published. Examples:
- Publishing a sector report on the public site.
- Sending a delivery narrative to a client for first review.
- Publishing a case study (anonymized).
- Raising an agent from A1 to A2.

**A3 — explicit human approval required.** Irreversible, external, or trust-critical. Examples:
- Sending outreach on behalf of a client.
- Publishing a named case study.
- Posting to Dealix-owned public channels (LinkedIn, X).
- Changing a banned-phrase rule.
- Granting an agent A2 capability for the first time.
- Modifying the approval matrix itself.

## Operating substance
The matrix is the single most-referenced trust document. Every agent prompt, every SOP, every runbook either points to this file or assigns each step a class explicitly. The cost of vagueness here is incident exposure later.

The reversibility test is the first cut. If the action can be undone by anyone in the team in under an hour with no external trace, it is at most A1. If the action leaves a public artifact (a post, a message sent, a published file), it is at least A2. If the action cannot be undone (a message landed in a real inbox, a number was wired, a named claim was published), it is A3.

The blast-radius test is the second cut. An action that affects one internal file is lower class than an action that affects every sprint. An action that affects one prospect is lower class than an action that affects an entire sector.

A3 approvals are kept short and frequent rather than long and rare. We would rather approve five A3 actions in a day than batch them weekly and lose accountability for each. The log captures the rationale so future audits can re-evaluate the decision in context.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
