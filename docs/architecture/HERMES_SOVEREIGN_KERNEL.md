# Hermes Sovereign Kernel v1

## Purpose

Hermes turns the Dealix sovereign operating vision into a small, enforceable kernel that can sit above the current Revenue Ops Autopilot, Approval Center, Evidence ledger, War Room, and future agent workforce.

This is not a replacement for the existing system. It is the unifying layer that makes every commercial, product, partner, market, training, customer success, venture, and API action follow one value loop.

```text
Sami Sovereign Layer
└── Hermes Universal Kernel
    ├── Signal Layer
    ├── Opportunity Layer
    ├── Decision Layer
    ├── Execution Layer
    ├── Trust Layer
    ├── Outcome Layer
    ├── Asset Layer
    └── Scale / Kill Layer
```

## Definition

Dealix is a sovereign universal value machine:

```text
Anything enters
→ it is understood
→ it becomes an opportunity or is archived
→ it is scored financially and strategically
→ it passes sovereignty and trust
→ it becomes execution
→ the result is measured
→ the result becomes an asset
→ the asset is scaled, sold, reused, or killed
```

Every object must produce at least one of:

```text
Money
Data
Asset
Partner
Access
Trust
Learning
```

If it produces none, it is noise.

## Why this exists

The current repository already has strong parts:

- Revenue Ops Autopilot
- War Room
- Approval Center
- Evidence events
- Proof Packs
- Founder Command Center concepts
- Sovereign Operating Model documents
- Backend v5 draft work with approvals and audit logs

Hermes v1 gives them a single operating spine so Dealix does not become scattered features.

## Core loop

```text
Signal
→ Opportunity
→ Decision
→ Execution
→ Trust
→ Outcome
→ Asset
→ Scale / Kill
```

## Core objects

### Signal

A Signal is anything that may have value.

Examples:

- founder idea
- customer message
- GitHub issue
- partner lead
- tender
- market news
- competitor movement
- risk event
- training request
- API opportunity
- personal wealth opportunity

Required fields:

- source
- signal_type
- title
- content
- confidence
- sensitivity
- owner

### Opportunity

An Opportunity is a scored Signal that may deserve action.

Opportunity score:

```text
0.25 cash_speed
+ 0.20 strategic_value
+ 0.20 repeatability
+ 0.15 data_moat
- 0.10 difficulty
- 0.10 risk
```

### Decision

A Decision turns an opportunity into execute, defer, kill, scale, or request_more_info.

### Execution

Execution is the planned action. It must have:

- action_type
- permission_level
- sovereignty_level
- expected_result
- external_action flag
- approval requirement

### Outcome

No execution is complete without an outcome.

Valid outcome examples:

- drafted
- sent_manual
- replied
- booked
- won
- lost
- paid
- ignored
- risk_blocked

### Asset

Every meaningful outcome should create an asset candidate:

- template
- playbook
- report
- policy
- training material
- sector kit
- workflow
- proof pack
- case study candidate

## Sovereignty levels

```text
S0_SAFE_INTERNAL       read, summarize, classify, draft internally
S1_INTERNAL           update internal records, create drafts, score objects
S2_SAMI_APPROVAL      outbound drafts, pricing proposals, partner pitch, client-facing docs
S3_HIGH_RISK_APPROVAL sensitive data, public claims, enterprise pricing, external commitments
S4_SOVEREIGN_ONLY     public API, marketplace, MCP server, strategic partnership, venture launch
S5_NEVER_AUTONOMOUS   money transfer, signing, data leak, false partnership claim, legal commitment
```

## Non-negotiable rules

1. Every input enters Signal Inbox.
2. Every Signal becomes Opportunity or Archive.
3. Every Opportunity has a score.
4. Every Execution has sovereignty and trust checks.
5. Every external action requires approval.
6. Every Execution requires an Outcome.
7. Every Outcome requires Asset Review.
8. Every Tool requires registry before production use.
9. Every Agent requires owner, max sovereignty level, allowed tools, forbidden tools, and KPIs.
10. Every MCP connector requires review and audit.
11. Every customer needs a value report.
12. Every partner needs fit score.
13. Every offer needs buyer, pain, price, deliverables, metric, and upsell path.

## Actions that no agent may execute autonomously

### S4 - Sovereign only

- Open public API
- Launch marketplace
- Enable MCP server
- Sign strategic partnership
- Approve enterprise pricing
- Export sensitive data
- Change company strategy
- Grant agent permissions
- Run external automation
- Launch a new venture

### S5 - Never autonomous

- Move money
- Sign on behalf of Sami
- Leak or export restricted data
- Claim a partnership that does not exist
- Make external legal commitments
- Send production outbound communication without approval

## How this maps to the current repo

```text
Current Revenue Ops Autopilot  → Money Engine v1
Current War Room               → Command Page v1
Current Approval Center        → Sovereign Approval Center v1
Current Evidence Events        → Outcome Ledger v1
Current Proof Packs            → Asset Review v1
Current Sovereign Docs         → Constitution / Doctrine
New Hermes Core                → Universal kernel above all engines
```

## First implementation boundaries

Hermes v1 intentionally does not launch:

- public API marketplace
- autonomous external sends
- autonomous payments
- unrestricted MCP
- broad data export
- unsupervised agent workforce

Hermes v1 does implement:

- universal object schemas
- opportunity and money scoring
- sovereignty classification
- permission decision object
- trust check object
- action routing to execute, hold, block, or approval
- tests for S4/S5 and outcome/asset rules

## Future engine mapping

```text
Money Engine                  -> revenue opportunities and cash actions
Product Factory               -> pain-to-offer-to-asset loop
Partner Engine                -> partner fit, pitch, onboarding, revenue share
Market Intelligence Engine    -> market signal to campaign/report/lead list
Training Engine               -> workshop to materials to upsell
Customer Success Engine       -> health, value report, renewal, upsell
Venture Engine                -> vertical test, first 50, scale/kill
API Infrastructure Engine     -> internal APIs first, public API only S4
Marketplace Engine            -> asset catalog only until S4 approval
```

## Definition of done for Hermes v1

Hermes v1 is accepted when:

- S4 actions are held for Sami only.
- S5 actions are blocked.
- external actions require approval.
- opportunities can be scored deterministically.
- outcomes are required after executions.
- asset review is required after meaningful outcomes.
- existing Revenue Ops can map leads/evidence to Signal/Opportunity/Outcome without rewriting the current pipeline.
