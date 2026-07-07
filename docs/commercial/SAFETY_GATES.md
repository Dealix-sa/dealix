# Autonomous OS — Safety Gates

The Autonomous Growth OS is safe **by construction**. This document lists the
concrete gates and how to verify them. They align with the non-negotiable
Outbound Safety Policy in `CLAUDE.md` and `.claude/rules/dealix-safety.md`.

## Layered gates

### 1. Environment tripwire
`SafetyGate.assert_draft_only()` runs at the start of every cycle. It raises if
`EXTERNAL_SEND_ENABLED=true` without `OUTBOUND_MODE=controlled_live`, halting the
run before any planning occurs.

### 2. Forbidden-action gate
A permanent deny-list (`FORBIDDEN_ACTIONS`) blocks cold outreach, mass/auto
send, LinkedIn automation, contact scraping, auto-invoicing, and auto-charging.
These can never be queued — not even for approval.

### 3. External-channel gate
Any step targeting `whatsapp`, `email`, `sms`, `linkedin`, or `phone` is routed
to the approval queue as a **draft**. The package contains no send capability.

### 4. Risk ceiling
Any step at or above `risk = 0.4`, or explicitly flagged `requires_approval`, is
routed to approval. Ambiguous risk defaults to approval.

### 5. No-secret model routing
`ModelRouter` decides providers by checking only the **presence** of an env var,
never its value. Local-first (Ollama / self-hosted) is preferred. No secret is
read, logged, or embedded in a routing decision.

### 6. Gitignored runtime
All generated artifacts (drafts, queues, proof logs, reports) are written under
`company/runtime/autonomous_os/`, which is gitignored. Nothing generated is
committed.

### 7. Append-only audit trail
`ProofLogger` records every plan, draft, approval request, block, and decision
as JSONL. The Learning Loop reads only this trail and produces transparent,
inspectable counters — no black-box behaviour.

## Verification

```bash
# Safety-critical unit tests (draft-only, forbidden blocked, approval routing):
python3 -m pytest tests/test_autonomous_os.py -q --noconftest

# Baseline outbound gate (must remain PASS):
python3 scripts/verify_no_auto_external_send.py

# No secrets leaked:
python3 scripts/ops/security_smoke_ci.py

# End-to-end draft-only run:
python3 scripts/autonomous_os_daily.py
```

Expected: outbound gate `PASS`, no external send, all forbidden actions blocked,
external actions pending in the approval queue, nothing sent.

## Stop conditions

Halt and report immediately if any of the following becomes true:

- A change would let the OS send an external message directly.
- A forbidden action would become routable to approval or auto-draft.
- The environment tripwire would need to be weakened to run.
- Any generated draft contains fabricated metrics or guaranteed-ROI claims.
