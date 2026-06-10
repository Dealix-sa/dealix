# Dealix — Module Status (human-readable mirror)

> **Source of truth:** `docs/registry/SERVICE_READINESS_MATRIX.yaml`.
> This file is a plain-language mirror. If the two disagree, the YAML wins and this file must be corrected.
> Gate: `scripts/verify_dealix_module_status.py` reads the YAML and fails if any artifact presents a non-live module as live.

## Status vocabulary (only these six are valid)

| Status | Meaning | May we say "live" publicly? |
|---|---|---|
| `live` | All eight readiness gates pass; usable with a real customer today | ✅ Yes |
| `pilot` | Working with design-partner customers under close supervision | ⚠️ "in pilot" only |
| `partial` | Some capability shipped, not end-to-end | ⚠️ "partial" only |
| `target` | Committed roadmap, not built | ❌ No — say "planned" |
| `blocked` | Has a known blocker | ❌ No |
| `backlog` | Not started | ❌ No |

A service may be marked `live` **only** when all eight gates are true:
`inputs · workflow · agent_role · human_approval · safe_tool_gateway · deliverable · proof_metric · test_or_evidence`.

## Layer → commercial framing

| Layer | Public framing | Where it shows up |
|---|---|---|
| Revenue OS | The Command Sprint wedge | `/command-sprint`, `/pricing`, Business OS Score tool |
| Proof OS | Trust / Proof Pack | `/security`, Proof Gap Audit tool, `customers/_template/10_proof_pack.md` |
| Governance OS | Approval-first safety | `/security`, `docs/governance/CLAIMS_REGISTER.md` |
| Delivery OS | 7-day fulfillment | `customers/_template/`, delivery SLA |
| Market Intelligence OS | Sector signals & answers | `/industries`, `/answers/*` |

## Rule for every surface

Before any page, deck, or tool calls a capability "live", confirm its `status: live` in the
readiness matrix. The CTA map and copy must describe **what the customer actually receives in a
Command Sprint today** — never a future module shown as present.
