# Email Deliverability System

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external action.

## Purpose

Protect Dealix's sending reputation while running approved outbound and follow-up. Deliverability is a precondition for distribution; without it, every other system in the factory is wasted.

## Setup Requirements

- A dedicated sending domain or subdomain, separated from the primary domain that hosts auth and billing.
- SPF record published.
- DKIM keys rotated and published.
- DMARC policy starting at `p=none` for monitoring, then progressing to `p=quarantine` once the baseline is clean.
- Reverse DNS configured.
- Bounce processing wired into the suppression list.
- Opt-out link in every message.
- Reply classification feeds the reply router.

## Warmup Plan

- Start at 10–25 approved messages per day from the warmed sending identity.
- Increase only if bounce rate, complaint rate, and "negative reply" rate stay below thresholds.
- Reduce or pause if any negative signal trends up.
- New sending identity restarts warmup; never inherit reputation across identities.

## Sending Volume Budget

The budget is daily, per identity, and enforced before the approval queue surfaces drafts. The budget is:

- Day 1–7: up to 25 sends/day per identity.
- Day 8–21: up to 50 sends/day per identity if metrics are clean.
- Day 22+: up to 100 sends/day per identity if metrics remain clean for 7 consecutive days.

A founder override is possible but writes to `AuditLogRecord` with a written reason.

## Core Rules

- No bulk unsolicited sending.
- No purchased personal-data lists.
- No untracked sending — every message is rendered through the gateway and logged.
- No contact after opt-out, ever.
- Prefer relevance over volume — a 5% reply rate at 25/day beats 0.5% at 250/day.
- Suppression checks happen at draft time and again at send time.

## Reply Classification (feeds reply router)

| Class | Signal | Routing |
|-------|--------|---------|
| Positive | Asks a question, requests a sample, asks for a call | Sample / proposal factory |
| Objection | Disagrees but engages | Founder reply queue |
| Defer | Asks to be contacted later | Follow-up worker with future date |
| Not now | Polite no | Suppress with reason "not interested" |
| Opt-out | Stop / unsubscribe / remove | Suppression with reason "opt-out" |
| Bounce | Hard bounce | Suppression with reason "bounce"; pause identity if trend |
| Complaint | Marked as spam / complaint loop | Suppression with reason "complaint"; halt identity, investigate |

## Runtime Wiring

- Safe send gateway pattern (extend the WhatsApp pattern): `auto_client_acquisition/whatsapp_safe_send.py`.
- Outreach window enforcement: `auto_client_acquisition/outreach_window.py`.
- Gmail and LinkedIn drafts (not sent until approved): `db/models.py::GmailDraftRecord`, `LinkedInDraftRecord`.
- Outreach queue (gated by approval): `db/models.py::OutreachQueueRecord`.
- Suppression: `db/models.py::SuppressionRecord` and `docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`.
- Approval policy engine: `auto_client_acquisition/approval_center/approval_policy.py`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Bounce rate | < 2% rolling 7 days | reply classification |
| Complaint rate | < 0.1% rolling 7 days | reply classification |
| Reply rate | tracked; experimented against | reply classification |
| Positive reply rate | tracked; experimented against | reply classification |
| Opt-out rate | tracked; investigated if trending up | suppression writes |
| Sends per identity per day vs budget | within budget | gateway logs |

## Cross-Links

- `docs/distribution/DEALIX_DISTRIBUTION_OS.md`
- `docs/distribution/EXPERIMENT_ENGINE.md`
- `docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/runtime/REVENUE_FACTORY_RUNTIME.md`

## Open Items

- A dedicated sending domain or subdomain is not yet provisioned; current drafts target Gmail user-side composition rather than an outbound gateway. This must be decided before any volume scale.
- SPF / DKIM / DMARC verification scripts are not in `scripts/`; add as part of the deliverability rollout.
- The reply router is a partial stub today (see `docs/runtime/REVENUE_FACTORY_RUNTIME.md` worker #10); its output is what this system depends on.
- A bounce / complaint feedback ingestion pipeline is not yet wired.
