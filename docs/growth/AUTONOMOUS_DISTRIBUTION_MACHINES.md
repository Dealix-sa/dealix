# Autonomous Distribution Machines — Posture

> "Autonomous" inside Dealix means **semi-autonomous**: the machine plans, drafts, scores, ranks and recommends, but **does not act externally** without explicit founder approval.

## 1. Why semi-autonomous

- OWASP LLM Top 10 calls out **Excessive Agency** as a leading risk: giving an LLM unchecked tools and actions causes unintended outcomes.
- KSA B2B is high-trust; one autonomous mis-send can undo months of brand work.
- The economic value comes from **drafting at machine speed**, not sending at machine speed.

## 2. Allowed actions per machine

| Action class | Allowed without approval |
|---|---|
| Internal data writes (drafts, queues, scores, recommendations) | Yes |
| Internal data reads | Yes |
| External writes (email, LinkedIn, contact form, payment, proof publish) | **No** |
| Pricing commits | **No** |
| Contract / refund commits | **No** |

## 3. Approval gates

Every external action enters `/approvals` with:

- Target account
- Channel
- Draft content (AR + EN)
- Suppression check status
- Brand check status
- Trust check status

Founder approves, declines, or defers.

## 4. Audit

Every approval, decline, defer, and post-send outcome is appended to the audit log.

## 5. Kill switches

- **Global** — single flag halts all external action.
- **Per-machine** — pauses one machine.
- **Per-channel** — pauses one channel (e.g., LinkedIn).
- **Per-account** — suppresses an account permanently.

## 6. Eval requirements

Each machine ships an eval suite covering:

- Brand voice conformance.
- Suppression honour.
- Bilingual symmetry.
- Personalisation accuracy.
- Prompt-injection resistance on inbound payloads.

The Eval Guardian blocks release on failure.
