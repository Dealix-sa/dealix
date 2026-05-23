# نموذج تشغيل الرئيس التنفيذي — CEO Operating Model

> The 14-layer architecture of Dealix and how the founder runs it.

## Purpose
Define how the founder operates Dealix as a layered system, not a to-do list. Each layer has owners, inputs, outputs, evidence, and a verifier. The CEO's job is to keep every layer green or visibly red — never silent.

## Owner
Founder/CEO.

## Inputs
- Daily Command Brief (`DAILY_COMMAND_BRIEF.md`)
- Weekly CEO Review (`WEEKLY_CEO_REVIEW.md`)
- KPI Tree state (`CEO_KPI_TREE.md`)
- Layer health from each domain's command center

## Outputs
- Layer status (Green / Amber / Red) in `dealix-ops-private/state/layers.json`
- Decisions logged in `docs/founder/decisions/`
- Bets list updated in `docs/strategy/STRATEGIC_BETS.md`

## Rules
1. Every layer has exactly one owner. No shared ownership.
2. A layer is Red if its verifier fails or its evidence is older than 7 days.
3. A Red layer blocks new bets in that domain until resolved.
4. No layer skips its cadence even if "nothing happened" — log "no change, evidence X".
5. CEO touches every layer at least monthly via the Monthly Strategy Review.

## Metrics
- Layers green: target ≥ 11 of 14 weekly.
- Verifier pass rate: ≥ 90% across all layers per month.
- CEO-touch coverage: 100% of layers per month.

## Cadence
Daily Command Brief → Weekly CEO Review (Sunday) → Monthly Strategy Review (last day of month) → Quarterly bet rebalance.

## Evidence
- `docs/founder/`, `docs/strategy/`, `docs/revenue/`, `docs/finance/`
- `dealix-ops-private/state/` for state snapshots
- Decision log under `docs/founder/decisions/YYYY-MM-DD_<slug>.md`

## Verifier
`make ceo-os-verify` — runs all layer verifiers and prints layer matrix.

## Runtime Command
`make ceo-daily` then `make ceo-week-close` Sundays.

---

## The 14 Layers

| # | Layer | Owner doc |
|---|---|---|
| 01 | Founder Command | `docs/founder/CEO_COMMAND_CENTER.md` |
| 02 | Strategy & Market | `docs/strategy/STRATEGIC_THESIS.md` |
| 03 | Revenue & Sales | `docs/revenue/REVENUE_COMMAND_CENTER.md` |
| 04 | Finance & Capital | `docs/finance/FINANCE_COMMAND_CENTER.md` |
| 05 | Delivery & Sprint Factory | `docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md` |
| 06 | Trust & Governance | `docs/14_trust_os/TRUST_OS.md` |
| 07 | Customer & Retention | `docs/customer/` |
| 08 | Product & Roadmap | `docs/product/` |
| 09 | Data & Evidence | `docs/data/` |
| 10 | People & Roles | `docs/people/` |
| 11 | Legal & Compliance | `docs/legal/` |
| 12 | Brand & Voice | `docs/brand/` |
| 13 | Learning & Library | `docs/learning/` |
| 14 | Risk & Continuity | `docs/risk/` |

## How layers connect
Strategy (02) sets bets → Revenue (03) executes the offer ladder → Finance (04) gates capital → Delivery (05) produces proof → Trust (06) validates → Learning (13) feeds back to Strategy.

## CEO daily loop
1. Open Command Center.
2. Read Daily Brief.
3. Answer the 6 daily questions.
4. Touch one Amber/Red layer.
5. Log one decision OR one kill.

## CEO weekly loop
Sunday: Run Weekly CEO Review. Update KPI Tree. Move bets. Run Business Audit. Publish brief to `dealix-ops-private/weekly/`.

## CEO monthly loop
Last working day: Monthly Strategy Review → Board Pack → Moat Review → KILL_LIST sweep → Capital Allocation reset.

## Non-negotiables enforced here
- No guaranteed revenue claims.
- No automated external sends without human approval.
- Evidence-based claims only — every metric cites its source.
- A3 actions (irreversible, public, customer-facing) require Go/No-Go gate.

## Cross-links
- `CEO_COMMAND_CENTER.md`
- `CEO_KPI_TREE.md`
- `CEO_BUSINESS_AUDIT.md`
- `docs/strategy/STRATEGIC_THESIS.md`
- `docs/revenue/REVENUE_COMMAND_CENTER.md`
- `docs/finance/FINANCE_COMMAND_CENTER.md`
