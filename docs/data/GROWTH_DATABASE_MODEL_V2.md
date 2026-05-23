# Growth Database Model v2

## Relationship to existing docs
Extends, but does not replace:
- `docs/data/SOVEREIGN_DATA_MODEL.md` — the canonical sovereign data model.
- `docs/data/DATA_READINESS_STANDARD.md` — the data-readiness scoring rules.

This document defines the **commercial** data subset that powers the v2 revenue runtime. Schema reference: `schemas/growth_database.schema.json`.

## Purpose
Define Dealix commercial data model from market universe to cash and retention.

## Core Objects

### market_accounts
All discovered companies.

Fields:
- account_id
- company
- website
- country
- city
- sector
- business_type
- offer
- source
- discovered_at

### lead_intelligence
Researched and scored accounts.

Fields:
- account_id
- fit_score
- priority
- why_fit
- buyer_titles
- public_contact_path
- research_notes
- last_researched
- status

### outreach_queue
Messages prepared or approved for sending.

Fields:
- outreach_id
- account_id
- channel
- recipient_or_contact_path
- message
- approval_status
- send_status
- sent_at
- next_action

### suppression_list
Do-not-contact and risk controls. Cross-references `docs/trust/SUPPRESSION_AND_OPTOUT_SYSTEM.md`.

Fields:
- company
- contact
- reason
- source
- date
- status

### conversation_log
Replies and routed next actions.

Fields:
- account_id
- channel
- reply_type
- summary
- next_action
- routed_to
- date

### sample_queue
Positive replies requiring sample packs.

### proposal_queue
Qualified opportunities requiring proposal drafts.

### payment_capture_queue
Proposals requiring payment / PO / written approval.

### delivery_queue
Paid or approved client work.

### retention_queue
Feedback, retainer, proof, referral, renewal.

## Rule
Pipeline is not the database.
Pipeline is the active commercial subset.
