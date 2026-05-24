# Approval levels — A1/A2/A3 ↔ L1-L4 mapping

The Dealix codebase encodes agent autonomy as **L1-L4** in
`auto_client_acquisition/agent_governance/agent_registry.py`
(`AutonomyLevel`). Public and customer-facing materials use the simpler
**A1/A2/A3** classification. This document is the single source of truth
for translation.

## Definitions

### Internal autonomy levels (`AutonomyLevel`)

| Level | Code | Meaning |
|---|---|---|
| `L1_DRAFT_ONLY` | L1 | Agent may draft text/code but never call external tools |
| `L2_TOOL_USE_WITH_HUMAN_APPROVAL` | L2 | Agent may execute tools after explicit human approval |
| `L3_TOOL_USE_PROACTIVE` | L3 | Agent may execute selected tools without per-call approval, within budget/scope policy |
| `L4_INTERNAL_AUTOMATION_ONLY` | L4 | Agent runs fully autonomously, but only against internal/admin surfaces — never customer-facing actions |

### External approval classes

| Class | Maps to | Meaning |
|---|---|---|
| **A1** | `L1_DRAFT_ONLY` | Draft is shown to a human. Nothing happens until the human acts. |
| **A2** | `L2` or `L3` with founder approval | Action is queued. Founder approval recorded in audit log before the integration adapter is called. |
| **A3** | `L4_INTERNAL_AUTOMATION_ONLY` | Agent runs autonomously, but **never** initiates an external customer-facing action. External actions remain A2. |

## Practical rules

1. **External customer-facing sends** (WhatsApp, email, SMS, payment
   creation, calendar invite) are **always at least A2**. There is no
   A3 path that hits a customer.
2. **Internal-only automation** (run a verifier, refresh a snapshot,
   index a doc) can be A3.
3. **Audit log entry is required** for any A2 transition before the
   adapter is called. `auto_client_acquisition/safe_send_gateway/middleware.py`
   exposes the canonical `enforce_consent_or_block` guard.
4. **PDPL opt-out** overrides every approval level — A2 cannot bypass it.

## Verifier coverage

- `scripts/verify_live_send_safety.py` checks that the safe-send
  middleware, approval policy, and Moyasar HMAC are wired.
- It does **not** enforce A1/A2/A3 labelling on each agent — that is
  documentation-level, not code-level. The code-level invariants are
  `AutonomyLevel` + `ToolCategory` whitelist/blacklist.
