# Contract Handoff Checklist

Before a quote becomes a signed SOW:

## Customer-side
- [ ] Decision-maker named and email confirmed.
- [ ] Billing contact named.
- [ ] Customer's legal review status known (waived / pending / required).
- [ ] Customer's procurement process disclosed (any portal required?).
- [ ] PO number (if applicable) noted.

## Dealix-side
- [ ] Quote `approved` in `quotes.index.json`.
- [ ] Offer-specific SOW filled from `business/contracts/STATEMENT_OF_WORK_TEMPLATE_*.md`.
- [ ] MSA outline shared if first engagement.
- [ ] DPA outline shared if customer-specific data will be processed.
- [ ] Acceptance criteria attached.
- [ ] Kickoff slot pre-booked.

## Sign-off
- [ ] Customer signs SOW.
- [ ] Founder signs SOW.
- [ ] Both signed PDFs stored in `business/contracts/signed/` (gitignored).
- [ ] Deal moves to `won` in `deals.ledger.json` via `scripts/mark_deal_won.py`.
- [ ] Kickoff workshop confirmed in calendar.

## After sign-off
- [ ] Internal Slack message: "Closed-won: <account> — <offer>".
- [ ] Customer welcome email drafted (`scripts/generate_outreach_drafts.py` template).
- [ ] Client workspace created (`scripts/create_client_workspace.py`).
- [ ] First deliverable target date set.
