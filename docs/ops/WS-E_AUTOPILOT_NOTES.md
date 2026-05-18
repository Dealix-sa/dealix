# WS-E — Daily Founder-Approved Autopilot — Operating Notes

**Workstream:** E (Daily Founder-Approved Autopilot)
**Status:** shipped (workflow + glue only — no product code)
**Last updated:** 2026-05-18

This file documents how the consolidated daily cycle fits together and
records one structural gap found while wiring the morning digest. It is an
ops note, not a product/architecture doc — it ships under the Commercial
Freeze because it only describes existing endpoints and the glue around
them.

---

## 1. The daily cycle

Three GitHub Actions workflows form one founder-approved loop. Every step
prepares and queues work; nothing auto-sends. The founder approves from the
approval surface; only an explicit approval triggers a send.

### Morning — `.github/workflows/daily-revenue-machine.yml` (04:00 UTC / 07:00 KSA)

1. Generate today's drafts — `POST /api/v1/automation/revenue-machine/run`
   with `approval_mode: draft_only`.
2. Schedule follow-ups — `POST /api/v1/automation/followups/run`.
3. Generate daily report — `POST /api/v1/automation/daily-report/generate`.
4. Export drafts to CSV.
5. **Consolidated founder digest** (added by WS-E) — one digest summarizing
   drafts generated, follow-ups due, approval-queue pending count, overdue
   approvals, and revenue-vs-target. Emails the founder only.
6. Upload artifacts.
7. Open an issue on failure.

### Evening — `.github/workflows/daily-evening-digest.yml` (16:00 UTC / 19:00 KSA)

Runs `scripts/dealix_evening_digest.py`, which reports what was
approved/sent today, what closed, and tomorrow's setup. Reuses
`scripts/founder_daily_scorecard.py` for the close-of-day scorecard.
Emails the founder only.

### Weekly — `.github/workflows/weekly-review.yml` (Sunday 05:00 UTC / 08:00 KSA)

Runs the friction-log review and a readiness re-check by invoking existing
scripts: `scripts/weekly_brief_runner.py --all-active`,
`scripts/verify_dealix_ready.py`, and `scripts/verify_governance.py`. No new
code — pure orchestration of scripts that already exist.

---

## 2. Approval-queue fragmentation gap

**Finding:** the founder approval queue is **not** a single endpoint today.
Drafts produced by the daily run land in two distinct stores:

| Store | Backing | Endpoint | Holds |
|-------|---------|----------|-------|
| `approval_center` | `ApprovalStore` (in-memory; Postgres-backed `approval_tickets` via `migrations/versions/20260515_103_approval_tickets.py`) | `GET /api/v1/approvals/pending` | Generic `approval_required` actions routed through the command center. |
| Draft tables | Postgres `GmailDraftRecord`, `LinkedInDraftRecord`, `OutreachQueueRecord` | `GET /api/v1/dashboard/revenue-machine/today` (`approval_queue_open` field) | Per-channel drafts produced by `revenue-machine/run`. |

The `revenue-machine/run` orchestrator writes drafts directly into the
per-channel draft tables; it does **not** also create a row in
`approval_center`. So `GET /api/v1/approvals/pending` does **not** reflect
the full daily draft backlog, and `dashboard/revenue-machine/today` does not
reflect non-draft approval tickets.

**Decision (freeze-compliant):** do **not** build a unifying endpoint, table,
or router — that would be new product code, which the Commercial Freeze
forbids. Instead, the morning digest **aggregates from both existing
endpoints**:

- `pending_approval_center` = `approvals/pending → count`
- `pending_drafts` = `dashboard/revenue-machine/today → approval_queue_open`
- `pending_total` = the sum (reported as the unified founder backlog)

The digest labels each source explicitly so the number is not misleading.

**Overdue approvals:** `approval_center` rows carry `expires_at`; the daily
machine already exposes `POST /api/v1/approvals/expire-sweep`. The digest
calls `approvals/pending` and counts rows whose `expires_at` is in the past
as `overdue` (the sweep itself remains a separate operational call).

**Recommended follow-up (post-freeze):** when the freeze lifts, route
`revenue-machine/run` drafts through `approval_center` so a single
`GET /api/v1/approvals/pending` is the one true founder queue. Tracked here
so it is not lost; no code change ships for it during the freeze.

---

## 3. Doctrine guarantees

- No workflow step sends an external message. `revenue-machine/run` is
  pinned to `approval_mode: draft_only`.
- Digests email the founder only (`DEALIX_FOUNDER_EMAIL`) — never prospects.
- All three workflows skip gracefully when their required secrets are
  unset, mirroring `daily-revenue-machine.yml`'s `secrets_gate` pattern.

---

## 4. Glue scripts (WS-E)

- `scripts/dealix_autopilot_morning_digest.py` — aggregates the consolidated
  morning digest from the two existing approval surfaces plus the daily-run
  JSON artifacts, and emails the founder. No product modules.
- `scripts/dealix_evening_digest.py` — close-of-day digest; reuses
  `scripts/founder_daily_scorecard.py`.

Both are pure orchestration / composition. They add no API routers, no DB
tables, and no service tiers.

