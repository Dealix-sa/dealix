# customers/ — per-engagement workspaces

Each customer engagement gets its own workspace here, created by:

```bash
python scripts/create_customer_workspace.py --name "Acme Trading"
```

Every workspace contains the canonical 12-file spine that carries an engagement
from intake to upsell:

| File | Purpose |
|---|---|
| `00_intake.md` | Intake & Source Passport |
| `01_company_intelligence.md` | Sourced company facts |
| `02_diagnostic_summary.md` | Diagnostic scorecard result |
| `03_command_sprint_scope.md` | Locked sprint scope |
| `04_revenue_map.md` | Scored accounts / opportunities |
| `05_proof_register.md` | Evidence register |
| `06_approval_register.md` | Approval gate (non-negotiable #8) |
| `07_next_action_board.md` | Today's one move |
| `08_executive_command_brief.md` | One-page decision brief |
| `09_delivery_log.md` | Daily delivery log |
| `10_proof_pack.md` | Proof Pack (score ≥ 70) |
| `11_upsell_recommendation.md` | Next-rung recommendation |

## Privacy

- Real customer workspaces may contain commercial data — **never** PII in logs
  (non-negotiable #6).
- `dry-run-client/` is a synthetic example produced by the E2E dry run
  (`scripts/run_dealix_e2e_dry_run.py`); it contains no real data.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
