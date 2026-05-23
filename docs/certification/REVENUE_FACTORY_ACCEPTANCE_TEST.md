# Revenue Factory Acceptance Test

## Purpose

Verify that Dealix's revenue factory actually moves leads toward cash —
not just that the files exist.

## Stage A — Intelligence Ready

- `$PRIVATE_OPS/intelligence/lead_intelligence_base.csv` exists.
- ≥100 lead records.
- ≥5 sectors tagged.
- Each row has `priority` ∈ {A, B, C} and `source`.

## Stage B — Outreach Ready

- `$PRIVATE_OPS/outreach/outreach_queue.csv` exists.
- ≥25 rows with `approval_status=approved`.
- Suppression respected (`$PRIVATE_OPS/security/suppression.csv` if present).
- No banned claims (`guaranteed`, `نضمن`, `مضمون`, etc.) in `message_body`.
- `$PRIVATE_OPS/runtime/approval_center.md` exists.

## Stage C — Conversation Ready

- `$PRIVATE_OPS/outreach/conversation_log.csv` exists.
- ≥1 row with `send_status=sent` or `send_status=draft`.
- Follow-up queue file exists.

## Stage D — Conversion Ready

- `$PRIVATE_OPS/sales/sample_queue.csv` exists.
- `$PRIVATE_OPS/sales/proposal_queue.csv` exists.
- `$PRIVATE_OPS/finance/payment_capture_queue.csv` exists.

## Stage E — Business Ready

- Payment / PO / written approval evidence path exists.
- `$PRIVATE_OPS/delivery/delivery_queue.csv` exists (after start condition).

## Rule

Do not call the factory operational unless **Stage B** passes.
Do not scale unless **Stage D** passes for the leading sector.

## Scripts

- `scripts/verify_revenue_runtime.py --private-ops $PRIVATE_OPS` — Stages A–D schema gates.
- `scripts/verify_business_evidence.py --private-ops $PRIVATE_OPS` — Stage E aggregates.
- `scripts/generate_ceo_verification_brief.py --private-ops $PRIVATE_OPS` — surfaces the top constraint as a single next action.
