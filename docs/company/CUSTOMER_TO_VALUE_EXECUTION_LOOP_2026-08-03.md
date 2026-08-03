# Customer-to-Value Execution Loop

## Purpose

Customer-to-Value turns an approved commercial commitment into a governed operating path for onboarding, activation, adoption, delivery, acceptance, measurable value, renewal, and learning.

It does not create a second CRM, customer-success database, workflow engine, approval center, or proof ledger. It consumes the canonical Dealix entities and closes into OutcomeEvent, ProofEvent, LearningEvent, and DailyCommand.

## Operating path

```text
Approved commitment
→ baseline
→ onboarding plan
→ kickoff approval
→ access and security readiness
→ activation
→ adoption and health
→ risk triage
→ acceptance package
→ customer acceptance request approval
→ delivery completion proof
→ customer value proof
→ renewal or stop recommendation
→ renewal communication approval
→ learning and Daily Command
```

## Business capabilities

- Scope-to-plan conversion.
- Baseline and target outcome definition.
- Named owners, milestones, access requirements, and acceptance criteria.
- Data-minimization and security readiness checks.
- Activation checkpoints.
- Adoption, stakeholder engagement, and delivery-health measurement.
- Risk and exception triage.
- Customer acceptance preparation.
- Separate delivery-completion and customer-value evidence.
- Renewal, extension, or stop recommendation.
- Executive command and improvement learning.

## Recognition boundaries

Dealix must distinguish:

- work started;
- workflow activated;
- customer using the workflow;
- delivery completed;
- customer accepted delivery;
- customer value measured;
- renewal recommended;
- renewal approved;
- renewal committed.

Synthetic runs may exercise the process but cannot establish real delivery, acceptance, value, revenue, renewal, or customer claims.

## Approval boundaries

Specific approval is required before:

- customer kickoff or access request;
- customer acceptance request;
- renewal or extension communication;
- any production change, payment action, contract commitment, or external send.

Draft-only mode stops at the first external-effect stage.

## Company value

This loop helps service, software, consulting, industrial, logistics, and B2B operating companies reduce onboarding delay, surface adoption risk early, preserve evidence, prevent premature success claims, and prepare renewals from measured outcomes rather than anecdotes.

## Verification

```bash
python scripts/commercial/run_company_loop_simulation.py --loop customer_to_value --mode synthetic
python scripts/commercial/run_company_loop_simulation.py --loop customer_to_value --mode draft_only
pytest -q tests/test_customer_to_value_loop.py tests/test_company_loops_registry.py
ruff check scripts/commercial/run_company_loop_simulation.py tests/test_customer_to_value_loop.py
```
