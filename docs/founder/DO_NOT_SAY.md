# DO NOT SAY — Founder/CEO Hypergrowth Layer Doctrine

This file lists language that is **never** permitted in any document, script,
component, or API response inside the Founder/CEO Hypergrowth Operating
Layer (P0 + P1). It is enforced three ways:

1. Static lint test — [`tests/test_no_founder_layer_promises.py`](../../tests/test_no_founder_layer_promises.py)
2. Verifier regex check — [`scripts/verify_founder_ceo_hypergrowth_layer.py`](../../scripts/verify_founder_ceo_hypergrowth_layer.py)
3. Existing doctrine tests — [`tests/test_no_guaranteed_claims.py`](../../tests/test_no_guaranteed_claims.py), [`tests/test_no_cold_whatsapp.py`](../../tests/test_no_cold_whatsapp.py)

See also: [`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md).

---

## Forbidden phrases (case-insensitive)

The verifier and lint test reject any document containing the patterns below
(this file itself is exempt because it must quote them for enforcement).

### Revenue / outcome guarantees

- "guaranteed revenue"
- "guaranteed ROI"
- "we guarantee"
- "we will pay you back"
- "نضمن" / "مضمون"

**Rationale.** Dealix records intent and decisions; outcomes depend on the
customer's market, team, and execution. Guarantees create unbounded
financial and regulatory exposure.

### External-action automation

- "auto-send" / "auto send"
- "automated outreach"
- "scraped"

**Rationale.** No agent in the Hypergrowth Layer initiates external messages.
Drafts are queued for human approval through the existing
[`approval_center`](../../auto_client_acquisition/approval_center/). Lead
data is sourced through documented integrations, not scraping.

### Money movement claims

- "we transfer funds on behalf of"

**Rationale.** Dealix never holds customer money. Money flows through
[`docs/revenue/INVOICE_FLOW.md`](../revenue/INVOICE_FLOW.md) and the Moyasar
verifier; the CEO layer records intent only.

---

## What to say instead

| Avoid | Use |
|---|---|
| "guaranteed ROI" | "ROI estimate based on assumptions in [STRATEGIC_ASSUMPTIONS_REGISTER](STRATEGIC_ASSUMPTIONS_REGISTER.md)" |
| "auto-send" | "queued for founder approval" |
| "automated outreach" | "draft prepared by agent; sent only after human approval" |
| "scraped" | "sourced via documented integration" or "manually researched" |
| "we transfer funds" | "Moyasar processes the payment; we record the event" |

---

## Decision-log entry on any policy update

Any change to this file must be logged via
`scripts/founder_decision_log_append.py` so the doctrine evolution stays
auditable. See [DECISION_LOG_SYSTEM](DECISION_LOG_SYSTEM.md).
