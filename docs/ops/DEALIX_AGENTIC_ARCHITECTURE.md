# Dealix Agentic Architecture

**Status:** Design document — describes current and planned operating loops.  
**Updated:** 2026-06-30  
**Safety rule:** All loops produce drafts and reports. No loop sends externally without founder approval.

---

## Core principle

Every Dealix agent loop follows the same pattern:

```
Inputs → AI Analysis → Draft Outputs → Human Approval Gate → Action
```

The approval gate is never skipped. Loops generate intelligence and drafts.
Humans decide and send.

---

## Operating loops

### 1. Revenue Daily Loop

**Purpose:** Surface today's best revenue opportunities and prepare follow-up drafts.

**Inputs:**
- CRM contacts and pipeline state (`company/crm/`)
- Outreach history and reply log (`company/outbox/`)
- Deal stage data and last-touch dates

**Processing:**
- Score contacts by recency, intent signals, and deal size
- Identify stale opportunities (no touch > 5 days)
- Draft WhatsApp/email follow-up messages for top 3–5 contacts

**Outputs:**
- Prioritized opportunity list (ranked, with reasoning)
- WhatsApp/email draft messages (approval-gated, never auto-sent)
- Founder daily revenue brief
- Approval cards for any action

**Trigger:** Daily (morning), or on demand via `./scripts/dealix_revenue_day.sh`

**Safety:** `EXTERNAL_SEND_ENABLED=false` enforced. All drafts require founder approval.

---

### 2. Company Brain Loop

**Purpose:** Synthesize business signals into a daily decision memo for the founder.

**Inputs:**
- Business metrics and revenue data
- Founder notes and meeting summaries
- Market signals and sector intelligence
- Customer feedback and issues

**Processing:**
- Identify top risks and opportunities
- Detect operational bottlenecks
- Propose next best actions with rationale

**Outputs:**
- Daily decision memo (5-minute read for founder)
- Bottleneck radar (top 3 operational blockers)
- Risk flags with suggested mitigations
- Prioritized action list

**Trigger:** Daily (morning), or on demand via `./scripts/dealix_micro_day.sh`

---

### 3. Client Delivery Loop

**Purpose:** Track active client engagements and surface delivery risks before they escalate.

**Inputs:**
- Client profile and scope document
- Deliverables list and completion state (`api/routers/deliverables.py`)
- Proof ledger entries
- Last client communication date

**Processing:**
- Check deliverable completion vs. timeline
- Flag overdue or at-risk items
- Draft weekly client status update

**Outputs:**
- Delivery status report per client
- Executive Proof Pack (evidence of completed work)
- Weekly client report draft (approval-gated)
- Renewal/upsell signal notes

**Trigger:** Weekly (Sunday), or on demand

---

### 4. Trust Review Loop

**Purpose:** Review all outgoing drafts and claims before they reach clients.

**Inputs:**
- Draft messages and proposals
- Claim statements and ROI mentions
- Channel type (WhatsApp, email, LinkedIn)
- Opt-in status for each contact

**Processing:**
- Flag guaranteed-ROI or fake-testimonial language
- Verify opt-in status before approving outbound
- Check PDPL compliance for data handling mentions
- Score risk level of each draft

**Outputs:**
- Approve / Edit / Block decision per draft
- Risk notes and recommended edits
- Audit event log entry
- Compliance flag if PDPL concern detected

**Trigger:** On every draft generation, before any approval card is shown.

---

### 5. Market Watch Loop

**Purpose:** Monitor the Saudi B2B market for targeting opportunities and competitive signals.

**Inputs:**
- Sector notes and public market data
- Competitor observations (manual input)
- Existing CRM for whitespace analysis
- Dealix offer performance data

**Processing:**
- Identify sectors with high pain-to-solution fit
- Surface companies matching the ICP
- Draft offer intelligence brief

**Outputs:**
- Weekly market brief
- Prioritized target company list (review-gated, no auto-outreach)
- Offer intelligence notes
- Competitive positioning summary

**Trigger:** Weekly (Sunday), or on demand

---

## Subagent definitions

Each subagent is a scoped Claude Code agent role used in the repository workflow.

### Repo Auditor

**Goal:** Verify repo health — secrets, safety gates, CI status.  
**Allowed files:** `scripts/ops/`, `.github/`, `Makefile`, `pyproject.toml`  
**Forbidden:** Modifying security scripts, disabling CI steps.  
**Verification:** `make full-repo-test`  
**Output:** Pass/fail report with exact failing gate and log path.

---

### CI Fixer

**Goal:** Fix failing required CI gates without disabling or hiding failures.  
**Allowed files:** Source files referenced in the failing test, `pyproject.toml`, `requirements.txt`  
**Forbidden:** Making tests skip, marking gates optional, deleting assertions.  
**Verification:** Re-run `make full-repo-test` until required gates all pass.  
**Output:** Diff of changes + test run showing PASS.

---

### Railway Deploy Doctor

**Goal:** Diagnose Railway deployment failures and produce a fix plan.  
**Allowed files:** `railway.toml`, `Dockerfile`, `scripts/ops/check_railway_production_env.py`, `docs/ops/RAILWAY_RECOVERY_RUNBOOK.md`  
**Forbidden:** Removing `_validate_production_secrets`, weakening security, committing secret values.  
**Verification:** `make railway-env-check`  
**Output:** Ordered list of what is missing/wrong + exact steps to fix in Railway UI.

---

### Revenue OS Engineer

**Goal:** Build or improve revenue loop scripts and CRM integrations.  
**Allowed files:** `company/crm/`, `company/outbox/`, `company/lead_research/`, `scripts/dealix_revenue_day.sh`  
**Forbidden:** Enabling live outbound, committing customer data to repo.  
**Verification:** `python3 scripts/verify_no_auto_external_send.py`  
**Output:** Working script + dry-run evidence.

---

### Company Brain Engineer

**Goal:** Build or improve daily founder brief and intelligence reports.  
**Allowed files:** `company/`, `scripts/dealix_micro_day.sh`, `reports/command_room/`  
**Forbidden:** Auto-sending reports externally, committing runtime outputs.  
**Verification:** Script runs without error in dry-run mode.  
**Output:** Generated report sample (local only, not committed).

---

### Frontend Command Room Engineer

**Goal:** Improve the Next.js command room frontend.  
**Allowed files:** `apps/web/`  
**Forbidden:** Starting `npm run dev`, hardcoding secrets, adding live-send UI without approval gate.  
**Verification:** `npm --prefix apps/web run verify`  
**Output:** TypeScript compiles clean, build passes, no new lint errors.

---

### Trust & Safety Reviewer

**Goal:** Audit all outgoing drafts and repo claims for safety and compliance.  
**Allowed files:** `sales/`, `docs/`, `.claude/rules/`, `scripts/verify_no_auto_external_send.py`  
**Forbidden:** Approving auto-send, approving fake ROI claims, weakening safety rules.  
**Verification:** `python3 scripts/ops/security_smoke_ci.py`  
**Output:** Approve / Edit / Block decision per item reviewed.

---

### Sales Asset Builder

**Goal:** Create and maintain Arabic sales documents for founder use.  
**Allowed files:** `sales/`  
**Forbidden:** Fake testimonials, guaranteed revenue claims, auto-sending drafts.  
**Verification:** Spot-check for placeholder language and guarantee claims.  
**Output:** Markdown file ready for founder review before any external use.

---

### Documentation Steward

**Goal:** Keep docs accurate, non-duplicated, and aligned with actual code.  
**Allowed files:** `docs/`, `CLAUDE.md`, `.claude/rules/`, `README*.md`  
**Forbidden:** Claiming unimplemented features, removing safety warnings, duplicating runbooks.  
**Verification:** Cross-reference doc claims against actual code paths.  
**Output:** Updated doc with accurate file paths and commands.

---

## MCP tool access policy

Every MCP tool call must:
1. Be logged to the audit event log.
2. Require explicit scope — no tool gets broad unrestricted access.
3. Respect outbound safety: no tool can send externally without `EXTERNAL_SEND_ENABLED=true` AND founder approval.
4. Handle secrets via environment variables only — never expose values in tool inputs/outputs.

Connector risk levels:

| Connector | Risk | Default |
|-----------|------|---------|
| Local CSV / file read | Low | Allowed |
| Railway Postgres (read) | Low | Allowed |
| Railway Postgres (write) | Medium | Requires scope |
| Gmail (draft only) | Low | Allowed |
| Gmail (send) | High | Blocked — requires controlled-live approval |
| Google Calendar (read) | Low | Allowed |
| Google Calendar (write) | Medium | Requires approval |
| WhatsApp Business (template draft) | Low | Allowed |
| WhatsApp Business (send) | High | Blocked — requires controlled-live approval |
| LinkedIn (read/research) | Medium | Manual only |
| LinkedIn (auto-DM/scraping) | Forbidden | Never |
| Web research / Exa | Low | Allowed |
| HubSpot (read) | Low | Allowed |
| HubSpot (write) | Medium | Requires scope |
