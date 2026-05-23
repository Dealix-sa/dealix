# Lead Outreach Autopilot OS

## Purpose
Run the end-to-end lead → outreach → reply → sample → proposal loop with
the system doing the heavy lifting and the founder approving external
commitments.

## Components
1. Source target registry — `acquisition/source_targets.csv`
2. Research queue — `acquisition/lead_research_queue.csv`
3. Lead batches — `acquisition/lead_batches/*.csv`
4. Outreach send queue — `outreach/outreach_send_queue.csv`
5. Gmail draft queue — `outreach/gmail_draft_queue.csv`
6. Follow-up queue — `outreach/followup_queue.csv`
7. Reply log — `outreach/reply_log.csv`
8. Sample quality log — `delivery/sample_quality_log.csv`
9. Proposal tracker — `sales/proposal_tracker.csv`
10. Pipeline tracker — `pipeline/pipeline_tracker.csv`
11. Approval queue — `founder/outreach_approval_queue.md`
12. CEO daily report — `founder/daily_acquisition_report.md`

## Daily Loop
1. `make acquisition-autopilot`
   - refresh source targets
   - refresh research queue
   - render daily acquisition report
2. Sami picks the sector to advance.
3. `make build-lead-batch SECTOR="ERP CRM"`
4. Sami reviews batch and marks `approval_status = Approved` for A/B leads.
5. `make outreach-queue BATCH=... CHANNEL=Email`
6. Drafts get prepared in Gmail draft queue (no auto-send).
7. Sami approves and sends, then marks `status = Sent` and `sent_date`.
8. `make outreach-autopilot`
   - route replies
   - schedule follow-ups for sent leads
   - generate sample tasks for positive replies
   - re-render daily report

## Hard Rules
- No external send without Sami approval.
- No scraping against any platform's terms.
- No banned claims (no guarantees, no fabricated results).
- No automated proposals — proposals always reviewed.
- No sensitive data in research notes.
- Every external action logs to its ledger.

## Definitions
- **Lead Score**: 0–100 fit score (sector, size, ICP match, public signal).
- **Priority A**: clear ICP, decision maker reachable, public signal of need.
- **Priority B**: strong sector fit, decision maker discoverable.
- **Priority C**: lower fit; queued for nurture only.

## Failure Modes Watched
- Pipeline starvation (<25 leads)
- Pending approvals piling up
- Followups overdue >3 days
- Positive replies with no sample task
- Sample tasks without quality score

## Hand-Off Points to Sami
- Sector selection
- Message tone approval
- Send/draft decision
- Pricing / proposal sign-off
- Public claim sign-off
