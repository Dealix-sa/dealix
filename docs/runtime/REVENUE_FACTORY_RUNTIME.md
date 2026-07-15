# Revenue Factory Runtime

## Doctrine Anchor
- Non-negotiables touched: #1 (no external high-risk action without approval), #4 (no production autonomy without rollback path), #5 (no proof-level overclaiming).
- Frozen decisions touched: golden chain as default execution path, approval-first mandatory for external and irreversible actions, control-plane verification scripts as release blockers.

## Purpose

Define Dealix as a 24/7 revenue factory whose runtime workers continuously discover, enrich, score, draft, route, follow up, and convert leads into samples, proposals, payment, delivery, retention, and proof. Intelligence scales aggressively; sending, delivery, and automation scale only behind trust gates.

## Core Rule

Scale intelligence aggressively. Scale sending carefully. Scale delivery only with QA. Scale automation only with trust gates. No external commitment leaves the factory without an approval record.

## Runtime Workers

| # | Worker | Responsibility | Approval gate |
|---|--------|----------------|---------------|
| 1 | Market Intelligence Worker | Sector signals, account discovery, news, hiring, RFPs | Internal only |
| 2 | Lead Discovery Worker | Find candidate accounts and buying units | Internal only |
| 3 | Lead Enrichment Worker | Enrich firmographics, contacts, signals | Internal only |
| 4 | Lead Scoring Worker | Deterministic fit/urgency/intent scoring | Internal only |
| 5 | Suppression Worker | Apply Do-Not-Contact, opt-out, bad-fit, duplicate, risky rules before any queue write | Internal only |
| 6 | Outreach Draft Worker | Generate Gmail/LinkedIn drafts (not sent) | Internal only |
| 7 | Approval Queue Worker | Surface batches to the founder for approve / reject / edit | Founder approval |
| 8 | Sending Queue Worker | Render approved drafts into the safe-send gateway | External; gated |
| 9 | Follow-Up Worker | Schedule and surface follow-ups by cadence and reply state | Founder approval per send |
| 10 | Reply Router | Classify replies; route to sample / proposal / objection / opt-out | Internal only |
| 11 | Sample Factory | Produce sector-specific sample artifacts on positive reply | Founder approval before send |
| 12 | Proposal + Payment Capture Worker | Draft proposal, attach payment path, follow up on PO / cash | Founder approval; payment is external |
| 13 | Delivery Trigger Worker | Move paid / PO'd work into delivery lifecycle | Internal only |
| 14 | Retention Worker | Schedule feedback, retainer asks, renewal-risk review | Founder approval for ask |
| 15 | Proof & Content Worker | Produce proof candidates and content drafts | Founder approval before publish |
| 16 | CEO Command Worker | Aggregate the daily decision queue for the founder | Internal only |

## Operating Targets (warmup)

- 500 accounts in the intelligence base within the first 30 days.
- 100 leads per priority sector.
- 25–50 approved sends per day during warmup, only after deliverability checks.
- 3–5 samples per week.
- 1–3 proposals per week.
- A payment / PO follow-up record for every proposal.

These are warmup targets, not commitments to a customer. They are reviewed weekly against actual delivery.

## Human Approval Required Before External Action

- External sending (email, LinkedIn, WhatsApp)
- Proposals
- Pricing or discount changes
- Client-facing reports
- Public proof or case studies
- Refunds, contracts, legal commitments
- Sensitive data export

## Never Automatic

- Bulk unsolicited sending
- Revenue or sales outcome claims
- Scraping restricted platforms against their terms
- Payment, refund, or contract decisions
- Public client claims

## Runtime Wiring

- Daily orchestration: `.github/workflows/daily-revenue-machine.yml` (04:00 UTC / 07:00 Riyadh).
- Founder commercial daily loop: `.github/workflows/founder_commercial_daily.yml`.
- Manual trigger: `scripts/founder_revenue_day_runner.py`, `scripts/run_dealix_complete_autonomous_day.py`.
- Async queue: `core/queue/worker.py` (ARQ on Redis, 10 concurrent jobs, 5-minute timeout, 3 retries) and `core/queue/tasks.py`.
- Approval policy engine: `auto_client_acquisition/approval_center/approval_policy.py` and `founder_rules.py`.
- Outreach window enforcement: `auto_client_acquisition/outreach_window.py`.
- Safe send: `auto_client_acquisition/whatsapp_safe_send.py`.
- Local executive snapshot: `make v5-status`, `make v5-digest`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Accounts in intelligence base | 500 in 30 days | `LeadRecord` (db/models.py) |
| Drafts pending approval | < 24h queue age | `OutreachQueueRecord` |
| Approved sends per day | 25–50 warmup | `GmailDraftRecord` + audit log |
| Positive replies per week | 3+ | Reply router (to be wired) |
| Samples per week | 3–5 | Sample factory queue (to be wired) |
| Proposals per week | 1–3 | Proposal queue (to be wired) |
| Payment follow-ups outstanding | tracked daily | Revenue events |

## Cross-Links

- `docs/runtime/WORKER_QUEUE_ARCHITECTURE.md`
- `docs/data/GROWTH_DATABASE_MODEL.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`
- `docs/distribution/DEALIX_DISTRIBUTION_OS.md`
- `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md`
- `docs/transformation/01_doctrine_lock.md`

## Open Items

- Workers 9–15 are partially wired: drafts and queues exist, but reply routing, sample factory, proposal draft generation, retention triggers, and proof candidate generation are not yet end-to-end.
- The factory currently runs through GitHub Actions on a daily cadence plus manual scripts. Migration of long-running flows to Temporal / LangGraph is a future RFC, not a current commitment.
- Operating targets are warmup targets, not outcomes; treat as activity guardrails until conversion data is sufficient.
