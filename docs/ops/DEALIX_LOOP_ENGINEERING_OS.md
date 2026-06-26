# Dealix Loop Engineering OS

## Purpose

Dealix is being turned from a collection of prompts, scripts, dashboards, and launch assets into an **agentic commercial operating system**. The operating principle is simple:

> Do not ask an AI agent to “do everything”. Build loops that plan, execute, verify, report, stop safely, and ask for human approval before any external action.

This document is the source of truth for how Dealix should apply loop engineering across revenue, company brain, delivery, trust, data connectors, and proof packs.

## Commercial doctrine

Dealix is not a chatbot, not a simple CRM, not a marketing agency, and not a dashboard-only project. Dealix builds AI operating systems for Saudi B2B companies that turn scattered sales, WhatsApp follow-up, proposals, operations, reports, and management decisions into daily workflows a company can actually run.

The operating system must remain founder-led and review-first until every production gate passes.

## Safety defaults

These defaults are part of the company identity, not just environment variables:

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

Dealix may generate research, drafts, follow-ups, proposals, briefs, proof packs, and reports. Dealix must not send, publish, charge, delete, or modify external systems without explicit human approval and a controlled-live release gate.

## Loop registry contract

Every Dealix loop must declare:

| Field | Meaning |
|---|---|
| `loop_id` | Stable identifier, for example `revenue_command_room_daily` |
| `goal` | Business result the loop exists to produce |
| `inputs` | Files, ledgers, connectors, or APIs used by the loop |
| `tools` | Scripts or functions the loop is allowed to call |
| `outputs` | Reports, ledgers, snapshots, or drafts produced |
| `verifier` | Tests or scripts proving the loop is safe and complete |
| `stop_condition` | Exact condition that ends the loop |
| `safety_gates` | Conditions that must remain true before output is usable |
| `human_review_required` | Whether a founder/client/operator must approve the next step |
| `mode` | `draft_only`, `review_only`, `controlled_live`, or `disabled` |

## Required loops

### 1. Revenue Command Room Daily Loop

**Goal:** produce founder-reviewed revenue actions every day.

**Inputs:**

- `ledgers/prospects.csv`
- `ledgers/outreach_log.csv`
- `ledgers/deals_pipeline.csv`
- `data/commercial/lead_pipeline.csv`
- public source URLs and verified account notes

**Outputs:**

- researched targets
- verified targets
- outreach drafts
- follow-up queue
- proposal queue
- `reports/revenue/latest.md`
- `reports/revenue/latest.json`
- command room snapshot

**Stop condition:** at least 10 reviewed founder actions are generated, or a safety/verifier gate fails.

**Safety:** draft-only by default; source URL and verification status are required before outreach.

### 2. Company Brain Daily Loop

**Goal:** produce a daily operating decision for the founder or client leadership team.

**Inputs:**

- revenue status
- customer pain signals
- delivery state
- market watch notes
- risk register

**Outputs:**

- daily CEO decision
- future radar
- bottleneck map
- weekly board memo
- 30-day action plan

**Stop condition:** one executive decision is produced with owner, metric, risk, and review date.

**Safety:** no deterministic prediction and no guaranteed ROI claims. Use scenario language and confidence levels.

### 3. Client Delivery Loop

**Goal:** turn a client request into a scoped, testable delivery workflow.

**Inputs:**

- intake form
- stakeholder map
- requested business outcome
- data access checklist
- acceptance criteria

**Outputs:**

- current-state map
- scope card
- solution blueprint
- delivery checklist
- proof pack

**Stop condition:** acceptance criteria and proof pack are ready for review.

**Safety:** no client data leaves approved channels; no AI output becomes final without human review.

### 4. Trust Review Loop

**Goal:** prevent unsafe AI, privacy, outreach, and claim behavior.

**Inputs:**

- draft messages
- proposal claims
- AI-generated content
- tool calls
- data access requests

**Outputs:**

- approval decision
- blocked reasons
- audit entry
- recommended safe alternative

**Stop condition:** every external action is either approved, blocked, or marked for revision.

**Safety:** blocks fake ROI, fake testimonials, missing opt-out, unverified targets, WhatsApp without opt-in/template logic, SMS automation, and any uncontrolled external send.

### 5. Market Watch Loop

**Goal:** monitor market, competitor, and sector signals and convert them into actions.

**Inputs:**

- public web sources
- CSV/manual notes
- optional Exa or other data connector results
- LinkedIn/manual observations

**Outputs:**

- market movement report
- account prioritization notes
- offer intelligence updates
- sector-specific outreach angle

**Stop condition:** three useful market signals and at least one next action are produced.

**Safety:** sources must be documented; weak assumptions must be labeled as assumptions.

### 6. Proof Pack Loop

**Goal:** prove what Dealix changed without fake claims.

**Inputs:**

- before/after operational state
- command room outputs
- delivery artifacts
- decision log
- safety gate log

**Outputs:**

- weekly proof pack
- decision ledger
- acceptance evidence
- next improvement plan

**Stop condition:** proof pack is ready for founder/client review.

**Safety:** do not claim revenue impact unless measured and attributable.

## Data connector principle

Loops should not call one vendor API directly. They should depend on a connector layer that can fall back safely:

```text
app/connectors/base.py
app/connectors/csv_source.py
app/connectors/public_web.py
app/connectors/exa_stub.py
app/connectors/hubspot_stub.py
```

Every connector must declare:

- source name
- allowed data type
- fallback source
- rate limit posture
- privacy posture
- error behavior

## Skill library principle

Each agent skill must be documented as a contract, not just a prompt:

```text
skills/prospect_research.skill.md
skills/target_verification.skill.md
skills/revenue_scoring.skill.md
skills/company_brain.skill.md
skills/proposal_brief.skill.md
skills/trust_review.skill.md
skills/proof_pack.skill.md
```

Every skill must include purpose, inputs, allowed actions, forbidden actions, output format, verifier, and example.

## PR discipline

Dealix should use one branch per operating layer:

1. `phase/loop-engineering-os`
2. `phase/data-connectors-os`
3. `phase/agentic-command-room-os`
4. `phase/customer-pain-radar`
5. `phase/ai-agent-governance-os`
6. `phase/proof-pack-os`

Do not merge large commercial packs until the release gate, CI, and conflict state are clear.

## Acceptance criteria

This doctrine is implemented when:

- every commercial loop has a registry entry
- every loop has a stop condition
- every loop has a verifier
- every external action requires approval
- every connector has a fallback
- command room displays latest generated state
- live outbound remains disabled by default
- proof packs avoid fake ROI and fake testimonials
