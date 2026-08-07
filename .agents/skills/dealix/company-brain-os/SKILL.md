---
name: dealix-company-brain-os
description: Build or run the Dealix Company Brain OS: an executive decision system that turns company, revenue, delivery, market, and risk signals into daily CEO decisions and weekly board memos.
---

# Dealix Company Brain OS

## When to use

Use this skill when the user asks to:

- build a Company Brain, CEO dashboard, founder desk, or decision room
- summarize company state into daily decisions
- connect revenue, delivery, market, customer, and risk signals
- create executive memos or board reports
- diagnose bottlenecks across a company
- turn Dealix into a real operating company instead of scattered scripts

## Positioning

Dealix Company Brain OS is not a chatbot. It is a decision layer above company workflows.

It should answer:

```text
What is the most important decision today?
Why now?
What changed?
What is the risk if we delay?
What action should the founder or operator take?
How do we verify the result?
```

## Files to inspect first

```text
docs/company/
docs/brand/
business/products/
scripts/brain/
scripts/revenue/
scripts/commercial/
scripts/delivery/
reports/brain/
reports/revenue/
reports/commercial/
reports/command_room/
ledgers/
app/commercial/
apps/web/app/
```

## Required outputs

A Brain OS run should produce:

```text
reports/brain/latest.md
reports/brain/latest.json
reports/brain/weekly_board_memo.md
reports/brain/founder_decision_desk.md
```

If these paths do not exist, create equivalent paths that match the repo structure.

## Decision model

Each executive decision must include:

```text
decision_title
context
signal_source
why_now
expected_impact
risk_if_ignored
recommended_action
owner
time_horizon
success_metric
review_date
confidence
```

## Company signal categories

Read or model these categories:

- revenue pipeline
- follow-up queue
- proposals and offers
- delivery backlog
- customer pain
- market and competitor movement
- compliance and trust risks
- product gaps
- website or funnel gaps
- founder operating bottlenecks

## Safety rules

- Do not invent metrics or proof.
- Clearly label assumptions.
- Do not claim guaranteed ROI.
- Do not fabricate clients, case studies, testimonials, or market data.
- Keep outbound disabled unless a separate controlled-live gate is explicitly approved.
- Prefer operational next actions over abstract strategy.

## Suggested commands

```bash
python scripts/brain/run_company_brain_day.py || true
python scripts/commercial/run_startup_os_day.py || true
python scripts/revenue/run_revenue_day.py || true
make company-day || true
make command-room || true
npm --prefix apps/web run verify || true
```

## Definition of done

The output is complete when the founder can open one report and know:

- what happened
- what matters
- what decision to make
- what to do today
- what not to do
- what to review next

## Final response format

```text
Company Brain OS Status:
- inspected signals:
- decisions generated:
- reports generated:
- blockers:
- next founder actions:
- safety status:
```
