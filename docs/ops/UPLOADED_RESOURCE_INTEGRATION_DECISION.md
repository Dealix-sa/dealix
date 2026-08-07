# Uploaded Resource Integration Decision

## Purpose

This document controls how uploaded Dealix OS / PR 559 / P0–P50 resource
packages are reviewed and promoted into the main repository. It exists so that
valuable uploaded work is preserved and auditable, while runtime code is never
overwritten by an unreviewed archive.

## Rule

Uploaded ZIPs are **not** merged directly into runtime code. Every archive must
pass, in order:

1. Extraction (into a temp workdir, never over the repo)
2. Diff review (against the current source tree)
3. File-by-file selection
4. Branch-based integration (single scope per branch)
5. CI verification
6. PR review
7. Founder approval

## Archive Classification

| Archive | Classification | Merge Policy |
|---|---|---|
| `dealix_resources_p0_p50.zip` | Resource vault | Add as resources only |
| `OKComputer_Dealix_OS.zip` | Source candidate | Selective merge |
| `OKComputer_تنفيذ_كامل_ومتوافق1.zip` | Source candidate | Compare against Dealix OS |
| `OKComputer_تسليم_PR_559.zip` | Historical source candidate | Selective merge only |
| `OKComputer_تسليم_PR_559_v1.zip` | Build artifact | Do **not** merge as source |

The machine-readable version of this table lives in
[`resources/company_os/UPLOADED_ARCHIVES_MANIFEST.json`](../../resources/company_os/UPLOADED_ARCHIVES_MANIFEST.json).

## Preferred Promotion Order

1. Resource vault (this branch)
2. Tests
3. Founder pages (additive route, never a replacement of the current UI)
4. Runbooks
5. Sales assets
6. UI integration
7. Build config — only after explicit review

## Hard Blocks

- No direct overwrite of production code.
- No secrets committed to the repo.
- No unchecked `package-lock.json` / lockfile replacement.
- No build artifacts committed into source paths unless explicitly intended.
- No public compliance or revenue claims without evidence or a disclaimer.

## Final Gate

Every promoted asset must pass the canonical gates before merge to `main`:

```bash
make doctor
make env-check
make security-smoke
make api-contract-check
make test
make prod-verify
```

Front-end promotions additionally run:

```bash
cd apps/web && npm ci && npm run build
```

## Tooling

- `scripts/compare_uploaded_resources.sh` — extract, checksum, summarize, and
  classify uploaded archives (read-only).
- `scripts/dealix_integration_wave.sh` — run the canonical gate bundle for an
  integration wave.
- `.github/workflows/resource-vault-check.yml` — CI guard that the vault and its
  tooling stay intact and that no archive contents leak into runtime paths.
