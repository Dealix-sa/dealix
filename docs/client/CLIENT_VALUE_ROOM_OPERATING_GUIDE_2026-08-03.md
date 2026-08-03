# Dealix Client Value Room — Operating Guide

## Purpose

The Client Value Room is the customer-facing transparency contract for every Dealix diagnostic, pilot, implementation, and managed-service engagement.

It answers nine questions continuously:

1. What is happening?
2. Why is it happening?
3. Who owns it?
4. What is blocked?
5. What needs customer approval?
6. What was delivered?
7. What was accepted?
8. What value is proven, directional, missing, negative, or inconclusive?
9. What decision comes next?

It is not a marketing dashboard and must not hide uncertainty, failed hypotheses, missing data, or unresolved risks.

## Client-visible surfaces

### Executive summary

Shows:

- overall engagement state;
- current phase;
- value status;
- top verified outcomes;
- high and critical risks;
- decisions required from the client;
- next checkpoint.

### Scope and success contract

Shows:

- scope in;
- scope out;
- client and Dealix owners;
- baseline;
- target metrics;
- acceptance criteria;
- rollback or stop rule.

Scope changes must enter the approval process. They cannot be silently absorbed into delivery.

### Live work

Each material work item shows:

- current stage;
- owner;
- status;
- expected date;
- dependency;
- evidence reference;
- whether the customer must act.

The view exposes business-relevant progress, not credentials, private internal notes, or sensitive implementation detail.

### Decision and approval center

Each decision request must include:

- the decision;
- why it is needed;
- available options;
- Dealix recommendation;
- business impact;
- risk;
- deadline;
- approver;
- rollback or reversal path.

No external message, material scope change, commercial term, sensitive production change, payment action, or policy change is implied by silence.

### Risk and exception center

Shows:

- severity;
- business impact;
- current root-cause status;
- owner;
- mitigation;
- target resolution date;
- action required from the client.

Risks must be visible when they are material, not only during weekly reporting.

### Delivery and acceptance

The room keeps four states separate:

```text
activity
!= delivery completion
!= customer acceptance
!= customer value
```

Delivery completion requires completion evidence.
Customer acceptance requires explicit customer evidence.
Customer value requires baseline, measurement source, measurement window, confidence, and outcome evidence.

### Value realization

Each value metric contains:

- metric name;
- baseline;
- target;
- current result;
- unit;
- measurement window;
- authoritative source;
- confidence;
- evidence references;
- value status.

Supported value statuses:

- `baseline_missing`;
- `baseline_established`;
- `measurement_active`;
- `directional_signal`;
- `outcome_verified`;
- `customer_accepted`;
- `not_achieved`;
- `inconclusive`.

Directional signals are visible but are not claimable as proven value.
Negative and inconclusive outcomes remain visible.

### Activity and evidence timeline

Material events are normalized into a chronological timeline containing:

- event ID;
- type;
- timestamp;
- actor;
- object;
- summary;
- source;
- evidence references;
- visibility level.

### Renewal and expansion

Renewal, extension, stop, or expansion recommendations show:

- recommendation;
- supporting evidence;
- unresolved risks;
- proposed future scope;
- decision date;
- approval status.

The room never sends or accepts a renewal decision automatically.

## Open standards alignment

Dealix aligns internal contracts with four open standards without requiring a new runtime dependency in this slice:

### CloudEvents

Used as the event-envelope model for material operating events. This improves portability across connectors and reduces custom event formats.

### OpenTelemetry

Used as the observability alignment for correlating service, environment, tenant, loop, action, outcome, logs, metrics, and traces.

### OpenLineage

Used as the lineage model for showing how inputs, runs, jobs, and outputs contributed to a customer-visible result.

### OpenFeature

Used as the rollout-control model for tenant-specific capabilities, pilots, risk tiers, and safe degradation without binding Dealix to one feature-flag provider.

## Data protection

Never expose:

- secret or credential values;
- other-tenant information;
- unredacted personal data;
- private internal notes;
- exploit details;
- hidden reasoning or model chain of thought.

Personal, security-sensitive, and third-party confidential data require redaction.

## Operating cadence

- Timeline: near real time when sources support it.
- Work status: daily on business days.
- Risk and approval items: upon material change.
- Executive summary: weekly or upon material change.
- Value review: at the agreed measurement checkpoint.
- Renewal readiness: before the agreed decision window.

## Verification

```bash
python -m pytest -q tests/test_client_value_room.py
python scripts/commercial/build_client_value_room.py --input engagement.json --output client-value-room.json
```

## Safety outcome

The Client Value Room is draft-only in this implementation. It generates a reviewable artifact and performs zero customer communication, production mutation, payment action, or renewal send.
