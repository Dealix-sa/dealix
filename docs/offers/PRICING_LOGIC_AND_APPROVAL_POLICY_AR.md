# Pricing Logic and Approval Policy

> **Status:** Hard rule. No price goes out without founder approval.

## The policy in one sentence

> Every price in a draft is `draft_only` until the founder approves a number for the specific deal.

## The four states

| State | Meaning | When used |
| --- | --- | --- |
| `draft_only` | No number. Founder quotes per deal. | First 5 deals in any new vertical. |
| `approved_range_required` | A SAR range is approved for this offer. Founder finalizes per deal. | After 5 deals, ranges are approved. |
| `founder_approval_required` | Per-deal approval; no range yet. | Custom Enterprise, anything > SAR 100k. |
| `final_approved` | Reserved. Never used in week 1. | Not applicable. |

## How the founder sets the first range

The founder sets a range only **after** completing 5 deals in a vertical at `draft_only`. The process:

1. List the 5 deal outcomes (what was offered, what was signed, what was paid).
2. Pick the median + the range.
3. Document the range in this file under the offer section.
4. Update the offer card with `pricing_status: approved_range_required`.
5. From the 6th deal onwards, the founder uses the range as a guide, not a floor.

## How a draft is structured (no final price in the draft)

A proposal draft **always** has:

- `pricing_status` field (one of the 4 states).
- If `draft_only`: a placeholder `__FILL_AT_APPROVAL__`.
- If `approved_range_required`: the SAR range, with a note: "Final price set at founder approval."
- If `founder_approval_required`: a note: "Per-deal approval; no range yet."

A proposal draft **never** has:

- A final number that the founder has not signed.
- A payment link.
- A discount that the founder has not approved.
- A "starting at" price in any public copy.

## The discount policy

Discounts exist. They are **founder-approved, deal-specific, and time-bounded**.

| Type | Cap | Approval |
| --- | --- | --- |
| Pilot discount | 20% | founder |
| Multi-offer bundle | 15% | founder |
| Long-term commitment (12+ months) | 10% | founder |
| Strategic logo (named account) | 25% | founder + counsel |
| Sector entry discount (first 3 in a new vertical) | 30% | founder |

A discount is always:

- Time-bounded (expiry date in the proposal).
- Reversible (the founder can withdraw it before signature).
- Logged in `templates/launch/approval_queue.example.json`.

## The negotiation policy

Negotiation is **a process, not a moment**. The founder is the closer for any deal > SAR 50k.

Phases:

1. **Discovery** — read-only, no price.
2. **Audit deliverable** — the report; no price.
3. **Audit debrief** — 30 min; no price; offer the next step (pilot).
4. **Pilot proposal** — `draft_only` with `pricing_status` field.
5. **Founder review** — founder sets the number.
6. **Send** — manual, with approval logged.
7. **Counter** — if the client counters, the founder decides the next number.
8. **Close** — payment handoff (no auto-link); founder approves the handoff.
9. **Kickoff** — the deal enters delivery.

The 9 phases are not negotiable. The duration of each phase is.

## The "no price in chat" rule

- No email, LinkedIn DM, phone call, or WhatsApp message carries a final price.
- Pricing conversations happen in a proposal doc, after the founder approves.
- The first time the client hears a number, it is in a `pricing_status: draft_only` proposal marked "subject to founder approval."

## The "no price in marketing" rule

- No public landing page carries a SAR amount.
- No public one-pager carries a SAR amount.
- No founder LinkedIn post carries a SAR amount.
- The pricing page (when it exists) is a `pricing_status: draft_only` page that says "تبدأ من X" with a note "السعر النهائي يعتمد على النطاق."

## The audit trail

Every pricing decision is logged in `templates/launch/approval_queue.example.json`:

```json
{
  "approval_id": "apr_001",
  "deal_id": "deal_2024_001",
  "offer": "WHATSAPP_FOLLOWUP_OS",
  "pricing_status_at_draft": "draft_only",
  "approved_price_sar": 32000,
  "discount_pct": 0,
  "approver": "founder",
  "approved_at_iso": "2024-12-01T10:00:00Z",
  "expiry_iso": "2024-12-15T23:59:59Z",
  "evidence_ref": "proof_pack_2024_agency_01"
}
```

This file is **append-only** in spirit. Do not edit history. Add a new row to reverse a decision.

## The kill criteria

The pricing policy fails (i.e. we have a problem) if:

- A draft is sent with a final price and no `pricing_status` field.
- A payment link is generated without founder approval.
- A discount is applied that is not in the table above.
- A "starting at" price appears in public copy without the approval note.

If any of these happen, the founder reviews the preflight logs, fixes the source, and updates this policy.

## Why this exists

Because the single biggest risk in a sales motion is **a number going out that does not match the value delivered**. A "starting at SAR 5k" promise that turns into a 6-week engagement at SAR 80k is how trust dies. The policy exists to make sure the number is always honest, always defensible, always owned.
