# Branch Protection — Required Checks

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

Branch protection is the CI-side companion to the production
security gate. The `main` branch is protected: merges require
passing the four Dealix-specific GitHub workflows below, plus the
broader test suite. This document lists the required checks and
explains why each one is on the list.

## The four required Dealix workflows

| Workflow file                                          | Required check name                                  | Purpose                                                                 |
| ------------------------------------------------------ | ---------------------------------------------------- | ----------------------------------------------------------------------- |
| `.github/workflows/dealix-company-os.yml`               | `dealix-company-os`                                  | Top-level operating layer verifier bundle (policy, registry, eval gate, runtime contract, trust plane). |
| `.github/workflows/dealix-sovereign-operating-stack.yml`| `dealix-sovereign-operating-stack`                   | Sovereign / Saudi-ready stack verifier (security governance, internal API auth, residency posture). |
| `.github/workflows/dealix-market-entry-stack.yml`       | `dealix-market-entry-stack`                          | Market-entry stack verifier (positioning, intelligence, product ladder, revenue factory, delivery, finance, customer success). |
| `.github/workflows/dealix-brand-growth-operating-layer.yml` | `dealix-brand-growth-operating-layer`              | Brand and growth operating layer verifier (brand assets, growth segmentation, distribution). |

Each workflow runs the relevant `scripts/verify_*.py` against the
PR branch. A failure indicates a missing artifact, a drift between
the policy/registry/eval/gate files, or a drift between the
documentation and the verifier expectations.

## Why these four

The four workflows cover the four pillars of the Dealix operating
model:

| Pillar          | Workflow                                      |
| --------------- | --------------------------------------------- |
| Trust           | `dealix-company-os` (policy, eval, registry)   |
| Sovereign       | `dealix-sovereign-operating-stack` (security)  |
| Market entry    | `dealix-market-entry-stack` (positioning, delivery, finance, CS) |
| Brand and growth| `dealix-brand-growth-operating-layer`          |

A drift in any pillar is caught before the merge.

## Additional required checks

In addition to the four Dealix workflows, the following are required:

| Workflow file                            | Required check name             | Purpose                                              |
| ---------------------------------------- | ------------------------------- | ---------------------------------------------------- |
| `.github/workflows/ci.yml`                | `ci`                            | Unit and integration tests.                          |
| `.github/workflows/codeql.yml`            | `codeql`                        | Static analysis.                                     |

The full list of workflows in the repo is broader; the required
list above is what blocks a merge.

## Branch protection settings

| Setting                                              | Value                                          |
| ---------------------------------------------------- | ---------------------------------------------- |
| Required pull request reviews                        | At least 1.                                    |
| Require status checks to pass before merging         | Yes.                                           |
| Require branches to be up to date before merging     | Yes.                                           |
| Required status checks                                | The four Dealix workflows + `ci` + `codeql`.  |
| Restrict who can push to matching branches            | Founder + maintainers only.                    |
| Require signed commits                                 | Recommended (per repo policy).                 |
| Require linear history                                 | Yes; squash-merge encouraged.                  |
| Force push                                             | Disabled.                                      |
| Branch deletion                                         | Disabled.                                     |

The settings are configured in the GitHub repository settings; the
configuration is not stored in the repo itself.

## Bypass policy

| Scenario                                             | Bypass allowed?                                 |
| ---------------------------------------------------- | ----------------------------------------------- |
| Emergency hotfix                                     | No. Use an expedited PR with a single reviewer.  |
| Documentation-only change                            | No. Required checks must still pass.            |
| Trust-plane file change                              | No, and additionally requires two reviewers.    |
| Bot-driven PR                                         | No.                                             |

Branch protection is intentionally non-negotiable. Any drift in the
trust plane or operating layer must be caught before merge.

## What happens on a failing check

| Failure                                                  | Action                                                                |
| -------------------------------------------------------- | --------------------------------------------------------------------- |
| `dealix-company-os` fails                                 | A missing or invalid policy/registry/eval/gate file; fix in PR.        |
| `dealix-sovereign-operating-stack` fails                  | A missing or invalid security/trust artifact; fix in PR.               |
| `dealix-market-entry-stack` fails                         | A missing market-entry artifact; fix in PR.                            |
| `dealix-brand-growth-operating-layer` fails               | A missing brand/growth artifact; fix in PR.                            |
| `ci` fails                                                 | Test failure; fix in PR.                                                |
| `codeql` fails                                            | Security finding; triage and fix or document the exception.            |

A failed check blocks the merge. Re-runs are unlimited.

## Verifier coverage

The verifiers behind each workflow read documentation files and
configuration files and assert their presence and basic shape. They
do not lint content. Content quality is the responsibility of
reviewers and the eval gate.

## Operational discipline

1. The four workflows are not optional.
2. Bypassing branch protection is a security incident.
3. Verifier failures are diagnostic signals, not noise.
4. The required check list is reviewed quarterly.
5. New workflows added to the required list are documented here.

## Cross-references

- `PRODUCTION_SECURITY_GATE.md` for the runtime posture check.
- `DEPLOYMENT_AND_ROLLBACK_SYSTEM.md` for the deploy pipeline.
- `ULTIMATE_SECURITY_GOVERNANCE.md` for the broader model.
- The verifier scripts under `scripts/verify_*.py`.
