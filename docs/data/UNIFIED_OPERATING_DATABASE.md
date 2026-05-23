# Unified Operating Database

## Purpose
Create one operating source of truth for revenue, delivery, finance, trust, and productization.

## Core Tables

### accounts
All discovered companies.

### contacts
Public business contact paths and decision-maker hypotheses.

### signals
Market, sector, technology, hiring, funding, expansion, compliance, or buyer signals.

### lead_scores
Fit score, priority, reason, and next action.

### suppression_list
Opt-outs, bad-fit, duplicate, risky, or do-not-contact records.

### outreach_queue
Messages pending approval, draft, sent, or follow-up.

### conversation_log
Replies, objections, routing, and next action.

### sample_queue
Sample tasks triggered by positive replies.

### proposal_queue
Proposal drafts, approval state, amount, and due date.

### payment_capture_queue
Payment, PO, and written approval follow-ups.

### delivery_queue
Paid or approved work ready for delivery.

### retention_queue
Feedback, retainer, renewal, proof, referral.

### proof_library
Approved proof, anonymized proof, case study candidates.

### ai_audit_log
AI actions, prompts, outputs, approval class, evidence, model.

### ceo_decision_log
CEO decisions and outcomes.

## Rule
The dashboard reads from this database.
Workers write to this database.
CEO acts from this database.
