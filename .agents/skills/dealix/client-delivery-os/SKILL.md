---
name: dealix-client-delivery-os
description: Deliver Dealix client projects through intake, diagnosis, scope cards, blueprint, build, validation, proof pack, handoff, and managed operations.
---

# Dealix Client Delivery OS

## When to use

Use this skill when the user asks to:

- handle a new client request
- turn a client idea into a scoped workflow
- build a delivery sprint
- create client intake, diagnosis, blueprint, proof pack, or handoff files
- automate the client delivery process
- make Dealix operate like a professional services/productized OS company

## Delivery doctrine

Do not begin with "what should we build?"

Begin with:

> What business outcome must the client get, and what workflow proves it?

Dealix delivers operating systems, not loose documents or one-off scripts.

## Files to inspect first

```text
docs/company/
docs/delivery/
docs/ops/
business/products/
scripts/delivery/
app/delivery/
clients/
reports/delivery/
reports/proof/
sales/
tests/*delivery*
```

## Required delivery phases

### 1. Intake

```text
clients/<client>/00_intake.md
clients/<client>/01_business_context.md
clients/<client>/02_current_tools.md
clients/<client>/03_pain_points.md
clients/<client>/04_requested_outcomes.md
clients/<client>/05_risks_and_constraints.md
```

### 2. Diagnosis

```text
clients/<client>/diagnosis/CURRENT_STATE_MAP.md
clients/<client>/diagnosis/BOTTLENECKS.md
clients/<client>/diagnosis/OPPORTUNITY_MAP.md
clients/<client>/diagnosis/RISK_REGISTER.md
clients/<client>/diagnosis/FIRST_WORKFLOW_RECOMMENDATION.md
clients/<client>/diagnosis/GO_NO_GO.md
```

### 3. Scope card

Every request must become a scope card:

```text
Request Name:
Business Outcome:
Primary User:
Current Pain:
Workflow Affected:
Inputs:
Outputs:
AI Role:
Human Review Required:
Data Sources:
Integrations:
Acceptance Criteria:
Out of Scope:
Risks:
Delivery Timeline:
Owner:
```

### 4. Blueprint

```text
clients/<client>/solution/SYSTEM_BLUEPRINT.md
clients/<client>/solution/WORKFLOW_MAP.md
clients/<client>/solution/DATA_MODEL.md
clients/<client>/solution/ROLES_AND_PERMISSIONS.md
clients/<client>/solution/AI_BEHAVIOR_POLICY.md
clients/<client>/solution/REPORTING_MODEL.md
clients/<client>/solution/ACCEPTANCE_CRITERIA.md
```

### 5. Proof pack

```text
clients/<client>/proof/PROOF_PACK.md
clients/<client>/proof/DELIVERY_LOG.md
clients/<client>/proof/BEFORE_AFTER.md
clients/<client>/proof/ACCEPTANCE_RESULTS.md
clients/<client>/proof/NEXT_30_DAYS.md
```

## Governance rules

- Flag sensitive data.
- Do not request more client data than needed.
- Never store secrets in repo.
- Mark personal/customer data clearly.
- Require human approval before external communications.
- Do not fabricate client results.

## Suggested commands

```bash
python scripts/delivery/onboard_client.py --client <client> || true
python scripts/delivery/run_delivery_day.py --client <client> || true
python scripts/delivery/generate_proof_pack.py --client <client> || true
make delivery-onboard CLIENT=<client> || true
make delivery-day CLIENT=<client> || true
make delivery-proof CLIENT=<client> || true
```

## Definition of done

A delivery sprint is complete when intake is documented, diagnosis is clear, one workflow is scoped, blueprint is created, acceptance criteria are testable, proof pack is generated, next 30 days are defined, and risks are visible.

## Final response format

```text
Client Delivery OS Status:
- client:
- phase:
- artifacts created:
- acceptance criteria:
- proof pack:
- risks:
- next action:
```
