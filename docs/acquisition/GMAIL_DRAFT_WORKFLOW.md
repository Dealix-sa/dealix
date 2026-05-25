# Gmail Draft Workflow

## Purpose
Prepare outbound messages as drafts for Sami review instead of sending automatically.

## Flow
Approved lead batch
→ outreach_send_queue.csv
→ Gmail draft queue
→ Sami review
→ send manually or approve sending

## Rules
- No draft for unapproved lead.
- No sending without explicit approval.
- No banned claims.
- No sensitive data.
- No mass spam.
- Every draft logged.

## Approval Levels
Draft creation: A1
Sending: A2
