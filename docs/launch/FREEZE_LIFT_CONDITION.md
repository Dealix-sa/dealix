# Freeze-Lift Condition — شرط رفع التجميد

> Phase E deliverable. The precise, unambiguous condition that lifts the
> Commercial Freeze and lawfully unlocks Tier 2+ build. This document does not
> change the freeze — it states it exactly. Sources of truth:
> `docs/ops/COMMERCIAL_FREEZE.md` and `docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`.

---

## 1. The rule today — القاعدة الحالية

The Commercial Freeze is **ACTIVE** (started 2026-05-16). It freezes **rungs
2–5** of the offer ladder: Data-to-Revenue Pack (Tier 2), Managed Ops (Tier 3),
Executive Command Center (Tier 4), Agency Partner OS (Tier 5). No new feature
PRs, routers, modules, dashboards, or architecture docs for those rungs ship
during the freeze.

The rung 0–1 *delivery finish* is explicitly permitted — it serves the freeze's
own exit condition. During the freeze, the only build-on-demand allowed is a
**sales asset** matched to a recorded market signal, capped in size, per
`docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`.

---

## 2. The exact lift condition — شرط الرفع بالضبط

The freeze, as written in `docs/ops/COMMERCIAL_FREEZE.md` §Exit, lifts on a
**single** event:

> **One paid pilot is delivered AND its Proof Pack is customer-approved at
> evidence level L3 or above.**

This document operationalizes the standing "3 proven paid pilots" trigger
referenced by the activation program. The two are reconciled as follows:

- **Freeze lift (Tier 0–1 motion proven):** triggered by the **first** proven
  paid pilot. This ends the freeze per `COMMERCIAL_FREEZE.md` §Exit and hands
  governance to the 90-day plan.
- **Tier 2+ build unlock (full ladder unfrozen):** triggered by **three** proven
  paid pilots. Until three are banked, Tier 2–5 build stays gated even after the
  freeze formally lifts — the 90-day plan, not improvisation, governs what
  unlocks between pilot 1 and pilot 3.

A build is never justified by anticipation. Per
`CONDITIONAL_BUILD_TRIGGERS.md` §0: **no signal → no build**.

---

## 3. What counts as a "proven paid pilot" — ما الذي يُحتسب

A pilot counts toward the trigger **only if ALL of the following are true**.
Each is verifiable; none may be asserted without its artifact.

| # | Criterion | Verifying artifact |
|---|---|---|
| 1 | **Real, named customer.** A distinct legal entity, not a friend test, not a discount-to-zero arrangement. | `docs/ledgers/CLIENT_LEDGER.md` entry |
| 2 | **Paid.** A real invoice cleared — Tier 1 (499) or above. Cleared = funds received and reconciled, not invoiced-only. | `docs/ops/pipeline_tracker.csv` (stage=Paid) + `docs/ops/manual_payment_log.md` or Moyasar record |
| 3 | **Delivered.** The engagement's deliverable was rendered and handed to the customer (Diagnostic report and/or Sprint deliverable). | `docs/ledgers/DELIVERY_LEDGER.md` entry |
| 4 | **Proof Pack assembled.** A full 14-section Proof Pack with a computed score ≥ 70. | Proof Pack file + `docs/ledgers/PROOF_LEDGER.md` |
| 5 | **Customer-approved at L3+.** The customer has explicitly approved the Proof Pack at evidence level **L3 or above** (the proof ladder is L0–L5; there is no L6). | Approval recorded with identity + timestamp; `PROOF_LEDGER.md` |
| 6 | **At least one Capital Asset.** The engagement produced ≥ 1 reusable Capital Ledger asset. | `docs/ledgers/CAPITAL_LEDGER.md` entry |
| 7 | **Zero doctrine violations.** No non-negotiable was breached in the audit trail of the engagement. | `docs/ledgers/GOVERNANCE_LEDGER.md` clean |

Three **independent** pilots — three different customers — are required for the
Tier 2+ build unlock. Three engagements with the same customer count as one.

---

## 4. What unlocks — ما الذي يُفتح

**On the first proven paid pilot (freeze lifts):**
- The Commercial Freeze formally ends. The motion is proven.
- Governance hands to `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`.
- Tier 0–1 may continue at full pace; Tier 2+ build remains gated until three.

**On the third proven paid pilot (Tier 2+ build unlocks):**
- Lawful to build Tier 2 (Data-to-Revenue Pack) delivery automation.
- Lawful to build Tier 3 (Managed Revenue Ops) recurring-delivery capability.
- Tier 4–5 remain unlocked by their own ladder conditions (Tier 4 after 3
  completed pilots; Tier 5 after 3 Proof Packs — see sales-pack README ladder).
- Every Tier 2+ build still passes its own doctrine guards: Proof Pack ≥ 70,
  Capital Asset, `governance_decision` on every output, approval-gated sends.

---

## 5. What does NOT lift the freeze — ما لا يرفع التجميد

- A signed proposal with no cleared payment. (Not paid.)
- A cleared payment with no delivered Proof Pack. (Not proven.)
- A Proof Pack scored ≥ 70 but not customer-approved at L3+. (Not approved.)
- Three engagements with one customer. (Not independent.)
- A founder belief that demand exists. Run `L4_TRUTH_CHECK.md` first.
- Spare engineering time. Per the freeze: building instead of selling has
  negative expected value until a pilot proves the motion.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
