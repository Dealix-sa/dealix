# Branch Protection — Required Checks

The `main` branch must require these GitHub Actions checks before
merge:

- `dealix-ultimate-operating-layer / verify` — runs the master verifier
  + policy + registry + eval + prompt-output + frontend build.
- (Existing) `ci` — the project's general Python CI.
- (Existing) `codeql` — static analysis.

## Recommended settings

- Require branches to be up to date before merging.
- Require linear history.
- Require signed commits for `main`.
- Restrict who can push directly to `main` to the founder.
- Disallow force pushes to `main`.

These are configured in the GitHub UI under
**Settings → Branches → Branch protection rules**; this document is the
canonical record of what should be enforced.
