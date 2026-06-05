# Targeting → Delivery Handoff

> النظام لا ينتهي عند البيع. إذا دفع العميل، ينتقل تلقائيًا إلى التسليم.

When a company pays, the targeting OS hands it to delivery by materializing a
structured customer folder. Engine: `scripts/targeting_delivery_handoff.py`.

**Hard rule:** a handoff is created **only** for a company whose outcome stage is
`paid`. The script never charges and never sends.

---

## Trigger

```bash
# Single company:
python scripts/targeting_delivery_handoff.py --company "Manar Performance Agency"

# All paid outcomes in data/targeting/outcomes.jsonl:
python scripts/targeting_delivery_handoff.py
```

---

## What it creates: `customers/{slug}/`

```
00_intake.md                 06_next_action_board.md
01_company_intelligence.md   07_executive_command_brief.md
02_diagnostic_summary.md     08_delivery_log.md
03_command_sprint_scope.md   09_proof_pack.md
04_revenue_map.md            10_upsell_recommendation.md
05_proof_register.md
```

See [../04_delivery/CUSTOMER_FOLDER_TEMPLATE.md](../04_delivery/CUSTOMER_FOLDER_TEMPLATE.md).

---

## Governance front-matter (every file)

```
- source
- evidence
- assumption
- confidence
- recommendation
- approval_required: founder
- next_action
- owner
- due_date
```

`00_intake.md` records the offer, the primary weakness → OS angle, and the paid
date. `03_command_sprint_scope.md` lists the offer deliverables.
`09_proof_pack.md` seeds the proof levels (L1→L5).

---

## Acceptance (delivery)

- [ ] Every paid target becomes a `customers/{slug}/` folder.
- [ ] Every folder has all 11 canonical files.
- [ ] Every file carries the governance front-matter.
- [ ] Every folder has a proof pack.

Tested by `tests/test_targeting_delivery_handoff.py`.
