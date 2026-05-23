# Objection Library System

The Objection Library is a versioned catalogue of common objections, the evidence-forward responses Dealix uses to address them, and the failure responses we explicitly avoid.

**Source of truth:** `$PRIVATE_OPS/objection_library.csv`
**Owner:** Founder + Revenue Lead
**Trust gate:** A1 — library entries are reviewed monthly by founder before publication to the agent.

## Structure

Each entry contains:

| Field | Type | Notes |
|-------|------|-------|
| `objection_id` | string | Stable identifier |
| `objection_text_en` | text | Canonical English form |
| `objection_text_ar` | text | Canonical Arabic form |
| `category` | enum | Price, trust, fit, timing, authority, evidence |
| `recommended_response_en` | text | Bullet structure |
| `recommended_response_ar` | text | Mirror of EN |
| `evidence_required` | enum | None, case-safe, public source, founder note |
| `avoid_patterns` | array | Phrases we never use |
| `last_reviewed_by` | string | Founder or Revenue Lead |
| `last_reviewed_at` | timestamp | ISO 8601 |

## Categories

- **Price.** "Too expensive." Response anchors to the offer ladder rung and the explicit deliverables. No discounting without founder approval.
- **Trust.** "I don't know who you are." Response anchors to the trust pack (`docs/14_trust_os/`) and to a case-safe summary (`docs/07_proof_os/CASE_SAFE_SUMMARY.md`). No name-dropping of customers who have not approved attribution.
- **Fit.** "We're not in that sector." Response checks ICP fit and may decline politely. No stretching of fit.
- **Timing.** "Not this quarter." Response logs the timing and schedules a documented follow-up.
- **Authority.** "I'm not the decision-maker." Response asks for an introduction or a follow-up call with the decision-maker.
- **Evidence.** "Where are your numbers?" Response provides estimated patterns with the disclaimer that estimated value is not Verified value. No fabricated metrics.

## Avoid patterns

The library explicitly enumerates phrases that Dealix never uses:

- "Guaranteed revenue."
- "Pay only if it works." (without contract language)
- "Our customers see X% conversion." (without verified attribution)
- "Limited time offer." (urgency manufactured rather than real)
- "Trust us." (no trust without evidence)

The Brand Guardian agent (`docs/ai/BRAND_GUARDIAN_AGENT.md`) rejects drafts that contain avoid patterns.

## Update cadence

- Weekly: Revenue Lead proposes new entries based on inbound replies.
- Monthly: Founder reviews and approves changes.
- Quarterly: A red-team review (`docs/ai/EVAL_RED_TEAM_SYSTEM.md`) tests entries against adversarial framing.

## Failure modes

- **Stale entry:** an entry references a deprecated offer or price. Detection: monthly review. Recovery: archive and replace.
- **Conflict with brand voice:** an entry uses banned language. Detection: lint at publish time. Recovery: rewrite, re-approve.
- **Over-confident response:** the response promises an outcome. Detection: founder review. Recovery: rewrite to evidence-forward, estimated language.

## Recovery path

If the Objection Library becomes inconsistent (entries contradict, language drifts), the founder freezes publication and runs a full review. The Reply Routing System (`docs/revenue/REPLY_ROUTING_SYSTEM.md`) falls back to manual triage with no attached responses until the library is re-certified.

## Metrics

- Entry count by category.
- Median age since last review.
- Acceptance rate of suggested responses (sent vs edited vs rejected).
- Adversarial pass rate from quarterly red-team.

## Disclaimer

Library responses are starting points, not scripts. Every send is a human decision. Dealix does not guarantee outcomes. Estimated value is not Verified value.
