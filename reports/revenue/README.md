# Revenue Reports

This directory contains the output of the Dealix revenue machine scripts.

## What lives here

- `latest.md` — the most recent daily CEO revenue report (Markdown)
- `latest.json` — the most recent daily CEO revenue report (JSON)
- `command_room.html` — the Revenue Command Room HTML dashboard
- `<YYYY-MM-DD>/` — dated report folders containing the report for that day

## How reports are generated

Reports are produced by the revenue scripts in `scripts/revenue/`:

1. `validate_targets.py` — validates that every prospect has a valid `source_url`
2. `score_targets.py` — scores prospects and writes `score_summary.json`
3. `generate_outreach_drafts.py` — writes draft emails to `outbox/<date>/`
4. `generate_proposal_brief.py` — writes proposal briefs for hot leads
5. `generate_daily_revenue_report.py` — writes the daily CEO report
6. `run_revenue_day.py` — orchestrator that produces `latest.md` and `latest.json`
7. `build_revenue_command_room.py` — builds `command_room.html`

## Rules

- **No external send.** All artifacts are drafts written to disk for human review.
- **source_url required.** No prospect is accepted without a traceable public source.
- **Drafts only.** A human must review and manually send any outreach.

## Safety

The revenue scripts are scanned by `tests/test_revenue_day_no_auto_send.py`
which forbids `requests.post`, `smtplib`, `httpx.post`, `send_email(...)`, and
similar patterns. Any script that mentions "send" must qualify it with
"draft", "never", "no external", or "review".