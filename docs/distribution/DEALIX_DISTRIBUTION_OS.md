# Dealix Distribution OS

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external action.

## Purpose

Own every path from market discovery to cash conversion as a portfolio of distribution channels. Each channel is measured, double-downed, fixed, killed, or deferred on a weekly cadence.

## Operating Principle

Distribution is a portfolio, not a single channel. No channel runs without weekly inspection. No channel scales without experiment evidence.

## Distribution Channels

| # | Channel | Description | Approval gate |
|---|---------|-------------|---------------|
| 1 | Founder outbound | Direct founder-to-buyer outreach | Founder sends; record kept |
| 2 | Contact forms | Inbound from landing pages | Auto-acknowledged; founder follows up |
| 3 | LinkedIn manual | One-to-one founder LinkedIn outreach | Founder sends; record kept |
| 4 | Email drafts | Outreach + follow-up + sample / proposal | Per-message approval |
| 5 | Referral partners | Warm intros from partners | Founder follows up; partner motion in `docs/partners/` |
| 6 | Content inbound | Content-led demand into landing pages | Auto-acknowledged; founder qualifies |
| 7 | Sector reports | Lead magnets for priority sectors | Per-report approval before publish |
| 8 | Strategic account plays | ABM motion against named accounts | Per-account approval |
| 9 | Client expansion | Existing client growth motion | Per-ask approval |
| 10 | Proof-based demand | Inbound triggered by case study / proof | Per-publication approval |

## Weekly Decision Loop

For each channel, weekly: double down / fix / kill / defer.

- **Double down** — channel produced qualified replies or cash; allocate more time and budget.
- **Fix** — channel produced activity but no conversion; change message, audience, or offer.
- **Kill** — channel produced no signal across the experiment window; reallocate.
- **Defer** — channel needs an upstream prerequisite (proof, asset, partner) before retrying.

A weekly distribution review writes its conclusion to the war room file (`docs/founder/REVENUE_WAR_ROOM_OS.md`) and updates the experiment registry.

## Operating Metrics (per channel, per week)

- Leads discovered
- Leads enriched
- Leads approved into outreach
- Messages drafted
- Messages sent (after approval)
- Replies
- Positive replies
- Samples requested
- Proposals drafted
- Payment / PO follow-ups
- Cash collected
- Retention asks
- Referrals received

Targets per channel are set per experiment in `docs/distribution/EXPERIMENT_ENGINE.md`, not hard-coded.

## Core Rules

- No channel runs without a named owner.
- No channel scales without an experiment record.
- No external send happens without an approval record.
- No "guarantee" or outcome-promise language enters any drafted message.
- Suppression list is checked at the channel boundary, not at send time.

## Runtime Wiring

- WhatsApp safe send: `auto_client_acquisition/whatsapp_safe_send.py`.
- Outreach window: `auto_client_acquisition/outreach_window.py`.
- Automation router: `api/routers/automation.py`.
- Autonomous growth orchestrator: `autonomous_growth/orchestrator.py`.
- Distribution agents: `autonomous_growth/agents/distribution`.
- Daily commercial loop: `.github/workflows/founder_commercial_daily.yml`.
- Daily revenue machine: `.github/workflows/daily-revenue-machine.yml`.
- Founder daily brief: `scripts/dealix_founder_daily_brief.py`.
- Founder cadence: `scripts/founder_cadence.sh` and `.ps1`.

## Cross-Links

- `docs/distribution/EMAIL_DELIVERABILITY_SYSTEM.md`
- `docs/distribution/EXPERIMENT_ENGINE.md`
- `docs/distribution/ABM_STRATEGIC_ACCOUNT_MACHINE.md`
- `docs/partners/PARTNER_REVENUE_MACHINE.md`
- `docs/founder/REVENUE_WAR_ROOM_OS.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/transformation/01_doctrine_lock.md`

## Open Items

- A unified weekly distribution scorecard view across all 10 channels is not yet rendered in any one place; today it is reconstructed from multiple Action runs and the v5 digest.
- Content inbound and proof-based demand channels depend on the proof worker, which is partially wired.
- The experiment registry referenced here lives in `docs/distribution/EXPERIMENT_ENGINE.md`; the executable side of the registry (queries against the database) is not yet wired.
