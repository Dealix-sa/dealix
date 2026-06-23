# Dealix Company Operating System

## Purpose

The Dealix Company Operating System is the unified reference that connects strategy with sales, delivery, compliance, and learning. It defines how Dealix operates as one machine built to serve B2B companies in the Saudi market with operational AI systems — not as a chatbot, CRM, or marketing agency. The system spans: Revenue Command Room OS, Company Brain OS, WhatsApp/Inbox Follow-up OS, AI Outreach & Targeting OS, AI Trust & Compliance OS, Client Delivery OS, Controlled Live Outbound OS, Founder Decision Desk, Proposal+Contract+Payment OS, Executive Proof Pack OS, Offer Intelligence OS, Market & Competitor Watch OS, Customer Pain Radar, Operations Bottleneck Scanner.

## Owner

Founder / CEO. Responsible for daily system updates and team adherence.

## Daily Usage

- Morning (30 min): run `make company-day`, review the command room dashboard, review drafts in `outbox/YYYY-MM-DD/`.
- During the day: send approved drafts manually, update `ledgers/outreach_log.csv`, log replies in `ledgers/reply_log.csv`.
- Evening (15 min): update `ledgers/deals_pipeline.csv`, review `reports/revenue/YYYY-MM-DD/daily_ceo_report.md`.

## Inputs

- `ledgers/prospects.csv` — opportunities
- `ledgers/deals_pipeline.csv` — pipeline
- `ledgers/outreach_log.csv` — outreach sends
- `ledgers/reply_log.csv` — replies
- `data/outreach/saudi_icp_segments.json` — ICP segments
- `scripts/revenue/run_daily_revenue_machine.py` — daily machine

## Outputs

- `outbox/YYYY-MM-DD/*.md` — approved drafts for manual send
- `reports/revenue/YYYY-MM-DD/` — revenue and operations reports
- `reports/command_room/index.html` — command room dashboard
- documented operating decisions in founder log

## Workflow

1. Run the daily machine to collect data and generate drafts.
2. Review the command room and set the day's priorities.
3. Approve drafts manually before any send (approval-first).
4. Send manually via approved channels only.
5. Log every reply, meeting, and proposal.
6. Evening: update pipeline and daily report, note blockers.
7. Weekly: strategic review and source-of-truth refresh.

## Acceptance Criteria

- Every send is logged in `outreach_log.csv` before end of day.
- No draft is sent without explicit approval.
- Command room builds daily without errors.
- Daily report is saved before close of day.
- Every pipeline deal has an owner and next-action date.

## Risks

- Relying on automated sends without human approval can damage brand and compliance.
- Stale ledger data leads to wrong decisions.
- Skipping approval steps breaks trust with clients and regulators.
- Gap between strategy and daily delivery.

## What Not To Do

- Do not send any draft without approval.
- Do not claim guaranteed revenue or assured returns.
- Do not use fabricated testimonials or results.
- Do not describe Dealix as a chatbot, CRM, or marketing agency.
- Do not bypass PDPL requirements or approval-first rules.

## Next Action

Run `make company-day`, then review `reports/command_room/index.html` and assign action owners for the day.

## Related Files

- `docs/company/DEALIX_COMPANY_OS_AR.md`
- `docs/company/COMMAND_ROOM_RUNBOOK_AR.md`
- `docs/company/FOUNDER_OPERATING_SYSTEM_AR.md`
- `docs/company/DEALIX_SOURCE_OF_TRUTH.md`
- `docs/brand/DEALIX_BRAND_OS.md`