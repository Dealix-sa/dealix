# سياسة الموافقة البشرية — Human Approval Policy

> **القاعدة / The Rule:** كل إجراء خارجي يواجه العميل يُصاغ ويُجدوَل — ثم يوافق عليه إنسان قبل الإرسال.
> **Every customer-facing external action is DRAFTED and QUEUED; a human (founder) approves before send.**
> **صفر إرسال تلقائي في أي بيئة. Zero auto-send in any environment** (dev, staging, prod).

Canonical: `CLAUDE.md` Hard rules, `docs/00_constitution/NON_NEGOTIABLES.md`,
`docs/00_constitution/WHAT_DEALIX_REFUSES.md`. Status labels: `docs/00_platform_truth/MODULE_STATUS_MAP.md`.

## ما يُعتبر إجراءً خارجيًا / What counts as an external action

Any action that leaves Dealix and reaches a third party:
- a **message** (in-app, SMS), an **email**, a **WhatsApp** message,
- an **invoice** or payment request,
- a **publish** (web page, social post, customer name/logo/quote — see `PROOF_PACK_POLICY.md`).

If it touches a customer or the public, it is an external action and it goes through the gate.

## بوابة الموافقة / The approval gate

1. **Draft** — the system (or operator) generates the artifact. Status: `DRAFT`.
2. **Queue** — the artifact enters the approval queue. It is **never** sent on creation.
3. **Review** — a human (founder, or a founder-delegated approver named in writing) inspects it:
   recipient, content, claims (each claim must have a row in `CLAIMS_REGISTER.md`), timing, opt-in basis
   (see `NO_SPAM_POLICY.md`).
4. **Decision** — Approve / Edit-and-approve / Reject. No silent expiry into "send".
5. **Send** — only an approved artifact is released, by an explicit human action.

There is **no code path, flag, cron, or environment** that sends an external action without a recorded human approval.
Auto-send is not a feature behind a toggle — it does not exist.

## جواز القرار / Decision Passport entry

Every approved action writes a **Decision Passport** record (immutable log):

| Field | Description |
|---|---|
| `action_id` | Unique ID of the queued artifact |
| `action_mode` | One of the 5 modes below |
| `surface` | Channel (email / WhatsApp / invoice / publish / in-app) |
| `recipient` | Who receives it (or "public" for publish) |
| `claims_refs` | Row IDs in `CLAIMS_REGISTER.md` for every claim in the artifact |
| `opt_in_basis` | Warm relationship / opt-in proof (per `NO_SPAM_POLICY.md`) |
| `drafted_by` | Human or agent that drafted |
| `approved_by` | Founder / delegated approver (required, never empty) |
| `decision` | Approve / Edit-and-approve / Reject |
| `timestamp` | Decision time |

A send without a complete Decision Passport entry (especially `approved_by`) is a **policy breach** and must be blocked.

## أنماط الإجراء الخمسة / The 5 action modes

1. **Suggest** — system proposes; nothing is queued. Lowest risk.
2. **Draft** — system writes the artifact; sits in queue; awaits human.
3. **Approve-to-send** — human approves a drafted external action; then it sends. **Default for all external actions.**
4. **Scheduled-after-approval** — approved once, released at a chosen time; still human-approved before any send.
5. **Blocked** — refused by policy (e.g. cold automation, fake proof). Logged, never executed.

There is intentionally **no "Auto" mode.**

## بوابات قبل الإطلاق / Approval gates before launch

- No external send path may ship until approval-gate tests prove **zero auto-send** across all environments.
- Any new external channel requires a founder sign-off row before first use.
- Cross-checks: `CLAIMS_REGISTER.md` (claims), `NO_SPAM_POLICY.md` (contact basis), `PROOF_PACK_POLICY.md` (publishing).
