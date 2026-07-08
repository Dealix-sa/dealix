# Autonomous OS — Action & Approval Policy

This policy governs how the Dealix Autonomous Growth OS classifies and routes
every action it prepares. It complements the platform-wide approval policy in
`dealix/config/approval_policy.yaml` and the safety doctrine in
`.claude/rules/dealix-safety.md`.

## Routing decision (one action → one route)

The `SafetyGate` classifies each planned step into exactly one route:

| Route | When | Where it goes | Founder action |
|-------|------|---------------|----------------|
| **AUTO_DRAFT** | internal, non-external channel, `risk < 0.4`, not flagged | Action Queue as a draft artifact | Review at leisure |
| **APPROVAL** | external channel, `kind = external_draft`, `risk ≥ 0.4`, or `requires_approval` | Approval Queue as **pending** | Approve / reject before any downstream send |
| **BLOCKED** | action is in the forbidden set | Recorded only — never queued | None; it is refused |

`AUTO_EXECUTE_RISK_CEILING = 0.4`. Unknown or ambiguous risk defaults to
approval. External channels are **always** approval-gated, even under a
controlled-live configuration.

## Forbidden actions (always BLOCKED)

`cold_outreach`, `auto_send`, `mass_send`, `bulk_broadcast`,
`linkedin_automation`, `linkedin_scrape`, `scrape_contacts`, `buy_leads`,
`auto_invoice`, `auto_charge`.

Matching is fail-closed on **fragments**, not just exact names, so descriptive
variants loaded from editable strategy YAML (e.g. `cold_outreach_sequence`,
`mass_send_campaign`, `linkedin_scrape_contacts`) are also refused. Fragments
target the harmful verb (scrape / mass_send / auto_charge …), not platform names
— drafting a LinkedIn *post* for manual review stays allowed (draft-only).

These contradict the safety doctrine and cannot be enabled by configuration.

## External channels (always APPROVAL)

`whatsapp`, `email`, `sms`, `linkedin`, `phone`. Drafts for these are prepared
for review; **the OS holds no capability to send them.**

## Approval queue lifecycle

1. **submit** → item created in state `pending` with the prepared draft, the
   routing reason, risk, channel, and offer.
2. **decide** → founder (or an authorised approver) sets `approved` or
   `rejected`, recording `decided_by`, `decided_at`, and an optional note.
3. Only an approved item may be acted on by a **separate, independently-audited**
   executor. That executor is out of scope for this package and subject to the
   platform outbound-safety gates (`EXTERNAL_SEND_ENABLED=false` by default).

Every submit and decision is written to the append-only proof log
(`proof_logger.py`) so the trail is fully auditable.

## What requires founder approval (summary)

- Any external message (WhatsApp / email / SMS / LinkedIn / phone) — draft only.
- Any proposal, Proof Pack finalisation, or invoice.
- Any step at or above the risk ceiling.
- Any security or compliance claim (must be sourced).

## Non-negotiables

- The OS never approves its own actions.
- The OS never sends anything.
- Blocked actions are never re-routed to approval.
- No fabricated metrics or guaranteed-ROI language in any draft.
