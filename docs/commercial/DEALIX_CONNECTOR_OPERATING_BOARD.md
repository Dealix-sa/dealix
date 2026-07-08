# Dealix Connector Operating Board

## Purpose

This document defines how Dealix should use Slack, Google Contacts, Airtable/Sheets, GitHub, Gmail, and Calendar as the first practical Company OS layer.

## Current connector assumptions

- GitHub is the implementation source of truth.
- Slack is an internal command center.
- Airtable/Sheets is an operating board for structured execution.
- Google Contacts is only a warm-contact source when records exist.
- Gmail is a draft and radar layer, not an auto-send layer.
- Calendar is the daily rhythm layer.

## Tables to mirror in Airtable or Sheets

### Strategy Backlog

Fields:

- Strategy
- Area
- Priority
- Status
- Autonomy Level
- Safe Next Step
- GitHub Link

### Action Queue

Fields:

- Action
- Owner
- Status
- Risk Level
- Due Date
- Output
- Evidence Link

### Approval Queue

Fields:

- Approval Item
- Type
- Status
- Risk
- Decision
- Due Date
- Channel

### Opportunity Graph

Fields:

- Company
- Segment
- Offer Match
- Score
- Reason
- Stage
- Source URL
- Next Action

### Proof Ledger

Fields:

- Proof Event
- Entity
- Evidence
- Source URL
- Risk
- Date

### Self Improvement

Fields:

- Learning Event
- Area
- Failure Type
- Root Cause
- Improvement
- Autonomy Bucket
- Status

### Contacts Radar

Fields:

- Name
- Company
- Role
- Email
- Phone
- Source
- Status
- Notes

## Initial seed rows

### Strategy Backlog

1. Production Trust Spine — P0 — L4 Repo Execute — Verify Railway/CI/smoke safety.
2. Company OS Foundation — P0 — L3 Internal Execute — Create daily report, drafts, approvals, proof log.
3. Autonomous Growth OS — P1 — L3 Internal Execute — Generate action queue/content queue safely.
4. Self-Improvement Layer — P1 — L3 Internal Execute — Detect failures and propose improvements.
5. Revenue Command Pilot — P0 — L2 Draft — Prepare first closeable 14-day pilot.
6. Skill System — P1 — L2 Draft — Reusable Dealix operating instructions.

### Action Queue

1. Run production trust triage.
2. Verify Company OS daily runner.
3. Verify Autonomous Growth daily runner.
4. Verify Self-Improvement daily runner.
5. Produce first 14-day internal Proof Pack template.
6. Prepare Slack daily command brief.
7. Build Contacts Radar from warm contacts only.

### Approval Queue

1. Approve first outbound message template.
2. Approve first Revenue Command Pilot offer.
3. Approve any production config mutation.
4. Approve any PR merge.
5. Approve any external message send.

## Slack operating model

Create or use `#dealix-command-os`.

Daily message format:

```markdown
*Dealix Command OS — Daily Brief*

*P0 Trust*
- Current blocker:
- Safe next step:

*Money Now*
- Offer:
- Target:
- Approval needed:

*Approvals*
- Item 1:
- Item 2:

*Proof*
- Evidence captured:

No live outbound, no merge, no production mutation without explicit approval.
```

## Contacts policy

If Google Contacts returns no Dealix-specific records, do not invent contacts. Add a backlog task: build warm Contacts Radar from known people, opt-in replies, inbound leads, and customer records.

## GitHub source-of-truth issues

Use GitHub issues for durable execution:

- Master execution issue
- Production trust issue
- Money Now issue
- Connector board issue
- Self-improvement issue

## Safety checks

Before any external execution, confirm:

- The target is opt-in or warm.
- The message is approved.
- The channel is allowed.
- Opt-out language is present when appropriate.
- Proof and source links are logged.
- No guaranteed claims exist.
