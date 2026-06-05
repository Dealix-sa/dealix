# Dealix — Platform Truth

> Canonical identity document. Every page, doc, deck, and sales asset must agree with this file.
> If any artifact contradicts this document, the artifact is wrong.
> Last verified: keep `MODULE_STATUS.md` and `docs/registry/SERVICE_READINESS_MATRIX.yaml` in sync with the claims here.

---

## 1. What Dealix is

**Dealix is a Saudi-first AI Business Operating System.**

دييلكس هو **نظام تشغيل أعمال بالذكاء الاصطناعي، سعودي أولاً**.

Dealix helps Saudi companies clarify their opportunities, organize follow-up and proof,
prepare human-review-ready drafts, and reach the next executive decision faster — under
governance, with human approval for every external action.

The **first commercial wedge** is the **Dealix Command Sprint**: a 7-day, fixed-scope
engagement that produces a Revenue Map, Proof Register, Approval Register, Next Action
Board, and an Executive Command Brief — delivered as a **Proof Pack**.

---

## 2. The Business OS layer map

Dealix is one operating system expressed in layers. Only one layer is the commercial wedge today.

| Layer | Role | Status today |
|---|---|---|
| **Revenue OS** | Commercial wedge — opportunities, follow-up, offers, next actions | Wedge (sold via Command Sprint) |
| **Proof OS** | Trust layer — evidence, proof register, proof pack | Trust layer |
| **Governance OS** | Safety layer — approvals, forbidden actions, claims register | Safety layer |
| **Delivery OS** | Fulfillment layer — 7-day sprint factory, delivery log | Fulfillment layer |
| **Market Intelligence OS** | Growth intelligence layer — sector signals, answer library | Growth intelligence layer |

> "Revenue OS" is the **wedge, not the whole identity**. Dealix is the Business OS; Command
> Sprint is how a customer first experiences it.

The authoritative, per-service status (live / pilot / partial / target / blocked / backlog)
lives in `docs/registry/SERVICE_READINESS_MATRIX.yaml` and is summarized in
`docs/00_platform_truth/MODULE_STATUS.md`. **Never present a non-live module as live.**

---

## 3. What Dealix is NOT

These statements are **forbidden** anywhere in the product, website, or sales material:

- ❌ Dealix is **not** a CRM.
- ❌ Dealix is **not** a chatbot.
- ❌ Dealix is **not** a WhatsApp bot / cold-WhatsApp tool.
- ❌ Dealix is **not** a marketing agency.
- ❌ Dealix is **not** a generic AI tool.
- ❌ Dealix is **not** only a Revenue OS.
- ❌ Dealix is **not** only a targeting engine.
- ❌ Dealix does **not** have all modules live. (Status is governed by the readiness matrix.)

دييلكس **ليس**: CRM، ولا شات بوت، ولا بوت واتساب، ولا وكالة تسويق، ولا أداة ذكاء اصطناعي عامة،
وليس فقط Revenue OS، وليس فقط محرك استهداف، وليست كل وحداته فعّالة الآن.

---

## 4. Claims discipline (hard rules)

Dealix never claims and never implies:

- 🚫 Guaranteed revenue / guaranteed sales / guaranteed results / guaranteed ROI.
- 🚫 Automatic external sending (auto-send), cold WhatsApp, LinkedIn automation, scraping, list blasting.
- 🚫 "AI works with no human involvement" / "replaces your team."
- 🚫 Fake proof, fake testimonials, or fabricated scarcity.

The **safe language** Dealix uses instead:

- ✅ "We help you clarify your next actions."
- ✅ "We organize your opportunities, follow-up, and proof."
- ✅ "We prepare human-review-ready drafts."
- ✅ "We deliver a Proof Pack within the Command Sprint."

Enforcement source of truth: `docs/governance/CLAIMS_REGISTER.md`,
`auto_client_acquisition/governance_os/draft_gate.py`, and the
`scripts/verify_dealix_positioning.py` gate.

---

## 5. First sellable wedge — Dealix Command Sprint

- **Format:** 7-day, fixed-scope engagement.
- **Outputs:** Revenue Map · Proof Register · Approval Register · Next Action Board · Executive Command Brief → assembled as a **Proof Pack**.
- **Promise:** clarity and a human-review-ready operating picture — **not** a revenue guarantee.
- **Delivery contract:** every paid customer gets a folder under `customers/<name>/` (from `customers/_template/`) and a Proof Pack path.

---

## 6. Audience

- **ICP:** Saudi SMEs and mid-market companies with existing opportunities but unclear
  follow-up, offers, proof, or next executive decision.
- **Language:** Arabic-first, English-ready. Default locale is `ar`.

---

## 7. Cross-references

- Module status: `docs/00_platform_truth/MODULE_STATUS.md`
- Daily cockpit: `docs/00_platform_truth/LAUNCH_CONTROL_TOWER.md`
- Claims & governance: `docs/governance/CLAIMS_REGISTER.md`, `docs/governance/FORBIDDEN_ACTIONS.md`
- Delivery template: `customers/_template/`
- Sales kit: `sales/`
- Verification: `scripts/verify_dealix_positioning.py`, `verify_dealix_cta_map.py`, `verify_dealix_module_status.py`, `verify_dealix_growth_assets.py`, `verify_dealix_launch_readiness.py`
