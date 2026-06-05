# Dealix — Module Status Map

> **Status:** CANONICAL · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> The honest status of every module. This file prevents the most dangerous
> mistake: telling a customer everything is ready when some of it is a future
> vision. **Never sell above the status declared here.**

---

## Status legend

| Status | Meaning | Allowed to sell? |
|---|---|---|
| `LIVE` | Usable now | Yes |
| `BETA` | Usable internally / in supervised delivery | Yes, as a delivered service |
| `INTERNAL` | Serves the founder/team only | No — internal use only |
| `DOCS_ONLY` | Idea / document only | No |
| `DEPRECATED` | Not used | No |
| `BLOCKED` | Needs a dependency / security / fix | No until unblocked |
| `FUTURE` | Later | No |

---

## Module status

| Module | Status | Notes |
|---|---|---|
| Command OS | `BETA` | Delivered as the Executive Command Brief inside the Sprint. |
| Revenue OS | `LIVE / BETA` | Lead/ICP/follow-up engines exist; sold as a service, not self-serve SaaS. |
| Proof OS | `BETA` | Evidence registers + Proof Pack templates; claim validation manual. |
| Governance OS | `BETA` | Approval policy, claims register, audit concepts in place. |
| Client OS | `INTERNAL` | Delivered as "Client Brain Lite" inside the Sprint. |
| Delivery OS | `INTERNAL` | Delivered as "Delivery Lite"; full SLA engine is roadmap. |
| Support OS | `DOCS_ONLY` | Spec written; not delivered yet. |
| Finance OS | `DOCS_ONLY / BETA` | ZATCA-aware advisory only; **not** a billing provider. |
| Data OS | `BETA` | Intake/normalization/consent/retention concepts; PDPL-aware. |
| Knowledge OS | `INTERNAL` | SOPs/playbooks captured for internal delivery. |
| Agent OS | `BETA` | Registry + contracts; see `AGENTS.md` and Agent OS spec. |
| Partner OS | `FUTURE` | Do not open before 3 approved Command Packs. |
| Academy OS | `FUTURE` | Adoption content exists; productized program is later. |
| Venture OS | `FUTURE` | Long-horizon expansion. |

---

## How to update this file

1. Change status **only** with evidence (a passing test, a delivered engagement,
   or an explicit founder decision).
2. When a module is promoted to `LIVE`, add a claim to
   `dealix/registers/no_overclaim.yaml` with the supporting evidence.
3. Re-state `last_reviewed` at the top.
4. If README / website / deck implies a higher status than this file, the
   README / website / deck is wrong — fix it, not this file.

---

## Quick "sellable now" summary

- **Sell now:** Command Sprint (Revenue + Proof + Command + Governance Lite +
  Client/Delivery Lite).
- **Roadmap, do not sell as ready:** Support OS, Finance OS as a billing provider,
  Partner OS, Academy OS, Venture OS.
