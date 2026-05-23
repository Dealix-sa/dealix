# Dealix Operating Doctrine

> The contract that governs how Dealix operates as a company. Every other
> document, system, agent, workflow, and decision derives from this file.
>
> Owner: Founder / CEO. Approval level: Founder-only changes.

---

## 1. Purpose

Dealix exists to convert founder time and AI leverage into **paid revenue
from Saudi customers**, with public-grade trust and a private operations
backbone.

The doctrine answers:

1. What we will and will not do.
2. Who owns what.
3. What must be approved by a human and what can run autonomously.
4. How we know the company is healthy.
5. How we recover when something breaks.

---

## 2. The 7 Non-Negotiables

These are enforced by tests under `tests/trust/` and verify scripts under
`scripts/verify_*.py`. A failing check blocks merge to `main`.

1. **No overclaim.** No marketing language, case study, or proposal
   asserts a result, customer, certification, or metric that is not backed
   by a record in `dealix/registers/public_claims.yaml` or a private
   evidence pack. See `dealix/trust/claim_guard.py`.
2. **Never auto-execute outbound to external parties.** Every outbound
   message (email, DM, WhatsApp, LinkedIn) is *drafted* by an agent and
   queued for founder approval via `dealix/trust/approval_matrix.py`.
3. **Public/private boundary is enforced.** No client name, lead list,
   payment record, call note, or private pricing data is ever committed
   to the public repo. See `scripts/verify_public_safety.py` and
   `scripts/verify_private_boundary.py`.
4. **All sensitive actions are logged.** Approval, suppression, refund,
   data export, claim publication, and policy override write to an
   immutable audit ledger via `dealix/trust/audit.py`.
5. **Suppression list is authoritative.** Any contact on the suppression
   list cannot be messaged, regardless of source or sequence.
6. **Refunds and credits require founder approval.** No financial
   adjustment is final without an entry in `founder/approvals_waiting.md`
   resolved to `approved`.
7. **Every system has an owner, a metric, an approval level, a verify
   script, and an evidence path.** Documented under
   `docs/ops/SYSTEM_OWNERS.md`.

---

## 3. Operating Layers

| Layer | Lives under | Purpose |
|-------|-------------|---------|
| Strategy | `docs/strategy/`, `docs/founder/` | Where we play, how we win |
| Revenue | `docs/revenue/`, `docs/sales/`, `docs/offers/` | Pipeline, offers, pricing |
| Acquisition | `docs/acquisition/` | Lead sourcing, ICP, channels |
| Delivery | `docs/delivery/` | Sprint, pilot, desk playbooks |
| Trust | `docs/trust/`, `dealix/trust/`, `dealix/registers/` | Guardrails and audit |
| Client Success | `docs/client_success/` | Onboarding, retention, renewal |
| Product | `docs/product/` | What we build, defer, kill |
| Content | `docs/content/` | Founder voice, proof, demand |
| Learning | `docs/learning/` | Experiments, win/loss, memory |
| People | `docs/people/` | Roles, hiring, scorecards |
| Agents | `dealix/agents/`, `docs/agents/` | What each AI agent does |
| AI Management | `docs/ai_management/` | AI risk, oversight, change |
| Control Plane | `control_plane/`, `docs/control_plane/` | Real-time company state |
| Operating Intelligence | `operating_intelligence/` | Synthesis, priority, learning |
| Ops | `docs/ops/` | Cadence, escalation, SOPs |

---

## 4. Decision Rights

Codified in `DEALIX_DECISION_RULES.md` and enforced in
`dealix/trust/approval_matrix.py`.

| Action | Who decides |
|--------|-------------|
| Pricing, offers, public claims | Founder |
| Customer contracts | Founder |
| Refunds, credits, comp days | Founder |
| Public website / brand changes | Founder |
| Hiring | Founder |
| Capital deployment > 5,000 SAR | Founder |
| Lead scoring threshold tweaks | Ops Manager (when role exists) |
| Internal SOP updates | Ops Manager |
| Outreach copy templates | Founder approves first, contractor iterates |

---

## 5. Cadence

Documented in `docs/ops/OPERATING_CADENCE.md`. Summary:

- **Daily:** CEO Brief generated, decision queue reviewed, lead pipeline
  refreshed, approvals cleared.
- **Weekly:** CEO Review, win/loss capture, intelligence review, finance
  watch, friction log review.
- **Monthly:** Strategy update, moat review, capital allocation review,
  AI risk review, learning synthesis.

---

## 6. How We Know the Company is Healthy

`docs/founder/COMPANY_HEALTH_SCORE.md` and
`dealix/scoring/company_health_score.py` produce a single composite
score. The CEO Dashboard (`docs/founder/CEO_DASHBOARD_SPEC.md`) renders
it. If the score drops below threshold for three consecutive days, a
CEO alert fires and the priority engine reprioritizes work.

---

## 7. How We Recover

`docs/trust/INCIDENT_RESPONSE.md` and
`dealix/trust/incident_response.py` define severity tiers, communication
templates, and post-mortem requirements. Every incident produces a
learning entry routed through `control_plane/learning_router.py`.

---

## 8. Amendments

Doctrine amendments require:

1. A pull request that updates this file.
2. Approval in `founder/decision_log.md` (private repo) recording the
   rationale.
3. A passing run of `scripts/verify_full_ops.py`.

---

Last reviewed: created with the Master Tree generator.
