# Channel Portfolio System

The Channel Portfolio System measures every channel in the Distribution
War Machine, rebalances intensity, and surfaces channel-level decisions
to the founder. It is the read layer that keeps the rest of the machines
honest.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Maintain a real, dated, current view of how each channel is performing —
and recommend rebalancing decisions when channels saturate, degrade, or
under-deliver.

## 2. Input

Sources:

- `outreach/outreach_queue.csv`, `outreach/email_queue.csv`,
  `outreach/linkedin_queue.csv`, `outreach/contact_form_queue.csv`,
  `outreach/followup_queue.csv` (drafts and sends).
- `outreach/reply_routing.csv` (replies and routing).
- `customer_success/referral_queue.csv` (partner channel).
- `marketing/engagement_log.csv`, `marketing/content_calendar.csv`
  (content channel).
- `growth/offer_channel_fit.csv` (caps).
- `sales/proposal_queue.csv` (downstream outcome).

## 3. Output

`distribution/channel_scorecard.csv` columns:

- `channel_id` — LI | EM | CF | WARM | CC | PA | EV
- `period` — ISO week or month
- `drafts_produced`
- `drafts_approved`
- `sends`
- `replies_positive`
- `replies_negative`
- `opt_outs`
- `qualified_calls`
- `proposals_sent`
- `closed_won`
- `closed_lost`
- `intensity_cap`
- `intensity_used`
- `recommendation` — hold | reduce | raise | freeze
- `notes`
- `last_reviewed_at`

`distribution/sector_scorecard.csv` mirrors the same shape but indexed
by `sector_id`.

## 4. Source of truth

`distribution/channel_scorecard.csv` and
`distribution/sector_scorecard.csv` in the private ops runtime.

## 5. Approval class

A1. The portfolio system observes and recommends; it does not change
caps without founder approval. Cap changes are entered manually and
ledgered.

## 6. Trust gate

- Read-only access to underlying queues; the system never writes to
  outreach files.
- Cap-change recommendations require founder approval before any cap
  is changed in `growth/offer_channel_fit.csv`.
- Distress-signal interlock: if a sector or channel shows distress
  signals (sudden opt-out spike, complaint, deliverability event), the
  recommendation defaults to `freeze` and an incident is opened.

## 7. Owner

`performance_analyst`. Allowed write target: `distribution/`.

## 8. Worker

`scripts/dealix_channel_portfolio.py` (planned). The worker:

1. Aggregates inputs.
2. Computes per-channel and per-sector metrics.
3. Produces recommendations using the rules below.
4. Writes to the scorecards.

## 9. Recommendation rules

- `freeze`: any of: deliverability drop, complaint, opt-out spike >2x
  baseline, suppression bleed.
- `reduce`: reply quality below band for 2 consecutive weeks, or
  intensity_used near intensity_cap with declining marginal returns.
- `raise`: reply quality above band for 4 consecutive weeks, and
  intensity_used at cap, and downstream qualified-call rate intact.
- `hold`: everything else.

## 10. KPI

- Portfolio Net Reply Yield (per channel per quarter).
- Cost-to-Reply (operator minutes per positive reply).
- Channel Stability (number of `freeze` events per quarter; target: 0).
- Cap-Change Hygiene (changes are all founder-approved).

## 11. Failure mode

- Recommendations ignored. Performance Analyst raises in the weekly
  brief; founder consults.
- Cap change applied without ledger entry. Trust Guardian flags.
- Source feed gap (queue not updated). Worker raises stale data
  warning.
- Drift in scoring (caps misaligned with reality). Quarterly retune.

## 12. Recovery path

- For ignored recommendations: founder triage; if the recommendation
  was wrong, calibration; if right, cap change applied with ledger.
- For unauthorised cap change: revert; ledger entry; rule tightened.
- For stale feed: feed re-synced; affected scorecards re-computed.

## 13. Cadence

| Cadence | Activity |
|---|---|
| Daily | Refresh scorecards |
| Weekly | Recommendations posted; founder review |
| Monthly | Calibration |
| Quarterly | Portfolio reset |

## 14. Saudi-specific overlays

- Warm and partner channels typically outperform direct; the portfolio
  intentionally tolerates lower volume on those channels because each
  reply has higher downstream conversion.
- LinkedIn saturation in some sectors triggers earlier `reduce`
  recommendations.
- Bilingual sub-scorecards: drafts in Arabic vs. English are tracked
  separately to spot language-specific saturation.

## 15. Non-negotiables

- No autonomous cap changes.
- No external action originates here.
- No omission of distress signals.
- A3 not used.

The portfolio system is the brake on the war machine, not the
accelerator. It is supposed to be cautious, by design.
