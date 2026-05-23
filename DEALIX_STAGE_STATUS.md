# Dealix Stage Status

> Owner: Founder. Updated weekly during the CEO review.
> Verify: `scripts/verify_stage_status.py`.

This file is the public, machine-checkable answer to "where are we?"

---

## Stages

| Stage | Definition | Exit criteria |
|-------|------------|---------------|
| 0 — Founder clarity | Doctrine, decision rules, offer ladder exist | `readiness/gates/gate_00_founder_clarity.md` |
| 1 — Offer | One paid offer defined end-to-end | `readiness/gates/gate_01_offer.md` |
| 2 — Delivery | Delivery playbook + QA checklist for the offer | `readiness/gates/gate_02_delivery.md` |
| 3 — Product | Generator scripts, agents, registers cover the offer | `readiness/gates/gate_03_product.md` |
| 4 — Trust | Approval matrix + claim guard + audit working | `readiness/gates/gate_04_trust.md` |
| 5 — Sales | Outreach + qualification + proposal flow rehearsed | `readiness/gates/gate_05_sales.md` |
| 6 — First client | One paid sprint completed, feedback captured | `readiness/gates/gate_06_first_client.md` |
| 7 — Retainer | One recurring monthly client | `readiness/gates/gate_07_retainer.md` |
| 8 — Scale | Multi-client, productized, repeatable | `readiness/gates/gate_08_scale.md` |
| 9 — Autonomous Company OS | Control plane, intelligence, learning loop healthy | `readiness/gates/gate_09_autonomous_company_os.md` |

---

## Current Status

| Field | Value |
|-------|-------|
| Stage | 0 — Founder clarity (Master Tree just laid down) |
| Last review | Created by Master Tree generator |
| Next gate | gate_00_founder_clarity |
| Blocking items | Doctrine review, offer ladder lock, first verify run green |

---

## Update Rule

Edit this file only as the output of a CEO review. The verify script
asserts the table above contains the canonical stage labels and that
the current stage maps to a real gate file under `readiness/gates/`.
