# Human Approval Policy

> **Status:** CANONICAL · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> Approval-first is the core of Dealix's safety posture. This policy governs every
> agent, workflow, and person in the system.

---

## 1. Operating rule

> AI explores, analyzes, and recommends. Deterministic workflows execute. Humans
> approve critical external commitments.

## 2. Approval classes

| Class | Description | Needs approval? |
|---|---|---|
| A0 | Internal draft | No |
| A1 | Internal analysis | No |
| A2 | Customer-facing draft (message, proposal, reply) | **Yes — before it leaves Dealix** |
| A3 | External action (anything that touches a third party) | **Yes — always** |
| A4 | Financial / legal / security action | **Yes + logged record** |
| A5 | Destructive action (delete, overwrite, irreversible) | **Forbidden unless explicitly authorized in writing** |

## 3. What always requires human approval

- Sending any message to a customer or their contacts.
- Pricing commitments and discounts (also see `PRICE_AUTHORITY.md`).
- Contract or legal/regulatory communications.
- Sensitive data exports.
- Publishing any proof, case study, or claim.
- Any irreversible or destructive operation.

## 4. What is forbidden outright

- Automatic WhatsApp sending.
- Bulk / cold email sending.
- Scraping platforms that do not allow it.
- Changing pricing without documentation.
- Publishing a case study without customer approval.
- Deleting data without a logged record.

## 5. How approval is recorded

Each approved action records: `actor`, `approval_class`, `approver`, `timestamp`,
`input_class`, and a link to the artifact. A4/A5 additionally record the reason.

## 6. Agent enforcement

Every agent declares its highest approval class in its `.agent-contract.md`. An
agent may not perform an action above its declared class. See
`docs/02_operating_systems/AGENT_OS.md`.

## 7. Relationship to other docs

- External actions detail: `EXTERNAL_ACTIONS_POLICY.md`
- Claims: `CLAIMS_REGISTER.md` + `dealix/registers/no_overclaim.yaml`
- Data lifecycle: `DATA_RETENTION.md`, `PRIVACY_AND_PDPL_READINESS.md`
