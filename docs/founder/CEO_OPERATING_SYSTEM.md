# CEO Operating System

> How the founder operates the company day-by-day, week-by-week, quarter-by-quarter.
> This is the meta-doc that connects every other Founder OS file.

## Principle

Dealix is not a SaaS. Dealix is a **Company Operating System** that runs the company **around** the founder. The founder is the highest-leverage component, not the bottleneck.

This OS exists to:
1. Decide for me (with my pre-stated rules)
2. Prepare for me (with AI drafts)
3. Protect me (with trust gates)
4. Measure for me (with scorecards)
5. Teach me (with weekly learning reviews)

## Three Loops

The founder runs three loops, every period:

### Daily Loop (07:30 – 18:00)
- 07:30 → Read `DAILY_COMMAND_BRIEF.md` (generated overnight)
- 08:00 → Approve / reject overnight queue (outreach drafts, proposals, claims)
- 12:00 → Sales follow-ups + new outreach
- 14:00 → Delivery work (one client at a time, no context-switching)
- 17:00 → Close out: log decisions, append to execution ledger
- 18:00 → End-of-day close report appended

### Weekly Loop (Sunday)
- Read `WEEKLY_CEO_REVIEW.md` template
- Score each Super System (Revenue, Delivery, Trust, Learning) — use `readiness/scorecards/`
- Update `RISK_REGISTER.md`
- Make one BUILD / FIX / KILL / DEFER decision per system
- Refresh `FOCUS_POLICY.md` if priorities shifted

### Monthly Loop (last Sunday)
- Read `MONTHLY_STRATEGY_UPDATE.md` (learning rollup)
- Review pricing experiments
- Review hiring triggers — pull or hold?
- Review stage status (`DEALIX_STAGE_STATUS.md`)
- Append one board memo to `BOARD_MEMO_TEMPLATE.md`

## The Three Hard Rules

1. **The day starts in the Brief, not in GitHub.**
2. **Every decision gets logged the same day.**
3. **Every kill gets a written reason.**

## What This OS Refuses To Let The Founder Do

- Start the day reactively (inbox-first)
- Make a decision > 5K SAR without writing it down
- Ship a feature that fails the Strategy Filter
- Send an external message that fails the Approval Matrix
- Accept a customer commitment without a Delivery Playbook

## Inputs This OS Needs Every Day

- Pipeline state (auto from `pipeline/`)
- Cash state (auto from `revenue/`)
- Delivery state (auto from `delivery/`)
- Trust state (auto from `trust/`)
- Approval queue (auto from agents)

## Outputs This OS Produces Every Day

- One Daily Brief (read by founder)
- One updated Decision Log (written by founder)
- One updated Execution Ledger (written by founder + agents)
- One next-day approval queue (drafted by agents)

## When This OS Is Working

Signal you'll notice:
- You wake up knowing the one thing to do today
- You don't open GitHub, Notion, or Slack to find it
- You finish the day with cash collected, proof produced, or learning logged
- You can take a 3-day break without the company stalling

## When This OS Is Broken

Signal you'll notice:
- The day starts with "what should I do?"
- Decisions get made in chat and never logged
- Friday arrives with no idea what happened Tuesday
- Two systems are doing the same work and the founder is the connector

If you see those signals, run `python scripts/verify_founder_os.py` and fix the first failing check.
