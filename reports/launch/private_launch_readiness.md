# Private Launch Readiness — جاهزية الإطلاق الخاص

The decision record for whether Dealix can begin a **Private Manual Launch**
(founder-led, human-in-the-loop, approval-gated) — distinct from a Public Launch.

## What "Private Manual Launch" means

- Founder personally drives every customer conversation.
- Every external action is drafted and **approved by a human** before sending
  (non-negotiable #8).
- No public marketing automation, no website-driven self-serve.
- Goal: land the first paid sprints and produce the first Proof Packs.

## Readiness gates

| Gate | How to verify | Required for Private Launch |
|---|---|---|
| Positioning | `python scripts/verify_dealix_positioning.py` | Yes |
| Module status | `python scripts/verify_dealix_module_status.py` | Yes |
| Growth assets | `python scripts/verify_dealix_growth_assets.py` | Yes |
| Launch readiness | `python scripts/verify_dealix_launch_readiness.py` | Yes (score ≥ 85) |
| Full verification | `bash scripts/run_dealix_full_verification.sh` | Yes |
| E2E dry run | `python scripts/run_dealix_e2e_dry_run.py` | Yes |
| Customer workspace | `python scripts/create_customer_workspace.py --name "<client>"` | Yes |
| Founder daily command | `python scripts/founder_daily_command.py` | Yes |
| `npm run build` | website build | **Public Launch only** |

## The rule on `npm run build`

If `npm run build` fails but the E2E, governance, and delivery gates pass, you may
begin a **Private Manual Launch** — but do **not** do a Public Launch until the
build is green.

## Current status

Run the gates above and read:

- `reports/verification/dealix_full_verification_latest.md`
- `reports/verification/e2e_dry_run_latest.md`
- `reports/founder/daily_command.md`

If the full verification and E2E dry run both PASS, the system is operable and
Private Manual Launch is unblocked.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
