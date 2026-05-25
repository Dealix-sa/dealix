# Dealix Implementation Audit

> **Source of truth** for whether Dealix is *actually implemented* vs. *only documented*.
>
> Run `make audit` to recompute every level. Do not edit the **Current Result** or **Implementation Score** by hand — they are derived from `python scripts/audit_dealix_implementation.py`.

## Purpose

Verify that Dealix is **not only documented**, but **actually implemented and operational**, on four independent layers:

1. **Structure Check** — required files and directories exist.
2. **Quality Check** — files contain operating content (not just headers).
3. **Runtime Check** — public commands run end-to-end without error.
4. **Market Evidence** — private ops shows real leads, DMs, samples, proposals, payment attempts.

GitHub is the final referee: the workflow in `.github/workflows/dealix-implementation-audit.yml` runs every public check, and (once enabled in repo settings) branch protection refuses to merge to `main` unless the audit is green.

## Implementation Levels

| Level | Meaning | What proves it |
|---|---|---|
| L0 | Missing | file/dir not on disk |
| L1 | File exists | path resolves |
| L2 | File has operating content | size >= 100B and required markers present |
| L3 | Verified by script | matching `scripts/verify_*.py` exits 0 |
| L4 | Used in private ops | private audit script confirms artefacts |
| L5 | Produced market evidence | leads ≥ 25, DMs ≥ 25, samples ≥ 3, proposal ≥ 1, payment attempt ≥ 1 |

## Core Systems

| System | Public Files | Private Files | Verifier | Runtime Command | Evidence |
|---|---|---|---|---|---|
| Trust | `docs/trust/TRUST_COMMAND_CENTER.md` | `trust/` | `verify_tier0_safety.py` | `make verify` | `approval_log.csv` |
| Revenue | `docs/revenue/REVENUE_COMMAND_CENTER.md` | `pipeline/`, `revenue/`, `sales/` | `verify_tier1_revenue.py` | `make daily` | 25 leads, 25 DMs |
| Delivery | `docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md` | `delivery/`, `clients/` | `verify_tier2_delivery.py` | `make kit` | 3 samples, QA |
| Execution Engine | `execution_engine/` | `stage/` | `verify_execution_engine.py` | `make stage` / `make advance` | `evidence_report.md` |
| Revenue Sprint Kit | `docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md` | `offers/revenue_sprint/` | `verify_revenue_sprint_kit.py` | `make kit` | sample / proposal |
| CLI | `dealix_cli/` | private ops path | `verify_cli.py` | `make daily` | generated briefs |
| Dashboard | `internal_dashboard/` (optional) | local dashboard data | `verify_dashboard_v2.py` | `make dashboard` | local JSON |
| Learning | `docs/learning/` | `learning/`, `weekly_reviews/` | `verify_weekly_automation.py` | `make weekly-close` | weekly review |

## Definition of Done

Dealix is *implemented* when **all** of these are true:

- [ ] All public verification scripts in the table above exit 0.
- [ ] `python scripts/audit_dealix_implementation.py` exits 0.
- [ ] GitHub Actions workflow **Dealix Implementation Audit** is green on `main`.
- [ ] Branch protection on `main` requires that workflow as a status check.
- [ ] CLI `daily` runs and writes a brief.
- [ ] CLI `stage` runs and emits the current stage.
- [ ] CLI `advance` runs and updates the stage checklist.
- [ ] Revenue Sprint Kit files exist under `docs/offers/revenue_sprint/`.
- [ ] Private ops audit (`audit_private_ops.py`) exits 0 — i.e. **all of:**
  - [ ] 25 leads added to `pipeline/pipeline_tracker.csv`.
  - [ ] 25 DMs sent and recorded in `revenue/revenue_action_log.csv`.
  - [ ] 3 sample packs prepared.
  - [ ] 1 proposal sent.
  - [ ] 1 payment / PO / written approval being pursued.
- [ ] One weekly review file exists in `weekly_reviews/` for the current ISO week.
- [ ] At least one playbook update committed in the last 7 days.

## Current Result

<!-- audit-result:start -->
**Not yet run.** Run `make audit` to populate this block.
<!-- audit-result:end -->

## Implementation Score

| Area | Weight | Status | Points |
|---|---:|---|---:|
| Public structure | 10 | NOT_RUN | 0 |
| Private ops | 15 | NOT_RUN | 0 |
| Trust controls | 15 | NOT_RUN | 0 |
| Revenue system | 20 | NOT_RUN | 0 |
| Delivery kit | 15 | NOT_RUN | 0 |
| CLI runtime | 10 | NOT_RUN | 0 |
| GitHub protection | 10 | NOT_RUN | 0 |
| Market evidence | 5 | NOT_RUN | 0 |
| **Total** | **100** | | **0** |

### Score meaning

- **90–100** — Operating. Ship public artefacts and outreach.
- **75–89** — Ready internal. Founder runs daily but not yet selling at scale.
- **50–74** — Fix before scale. Plumbing works, content thin.
- **0–49** — Setup incomplete. Run `make audit` and walk the punch list.

> Note: **Market evidence is weighted small here on purpose** — this scorecard measures *technical readiness*. A 100/100 with zero proposals out the door still means the company has not moved commercially. The audit script will print a separate "MARKET EVIDENCE" line that reflects private-ops state.

## Next Action

- [ ] Run `make audit`.
- [ ] Fix the first failing item it reports.
- [ ] Commit and re-run until green.
- [ ] Enable required status check **Dealix Implementation Audit** on `main` in GitHub branch protection.
- [ ] Turn on **secret scanning** and **push protection** under **Code security and analysis**.

## How verification works

```
make audit
  └─ python -m dealix_cli audit --private-ops $(PRIVATE_OPS)
       ├─ python scripts/audit_dealix_implementation.py   # public
       │    ├─ existence + size checks for every PUBLIC_REQUIRED path
       │    ├─ runs every scripts/verify_*.py listed below
       │    └─ compileall on dealix*, ops_runtime, execution_engine, ...
       └─ python $(PRIVATE_OPS)/audit_private_ops.py     # private (optional)
            ├─ existence + size checks for every REQUIRED private path
            ├─ pipeline + revenue action log row counts
            └─ runs every private verify_*.py present
```

All verifier scripts live in `scripts/` and follow the same contract:

- exit code `0` → PASS
- non-zero → FAIL, with the missing items printed to stdout

See [`docs/ops/OPERATING_READINESS_LEVELS.md`](docs/ops/OPERATING_READINESS_LEVELS.md) for the meaning of each level and which artefacts unlock it.
