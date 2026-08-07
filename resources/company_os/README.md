# Dealix Company OS — Resource Vault

This directory is an **auditable, non-runtime vault** for uploaded Dealix OS /
PR / roadmap resource packages (Dealix OS, PR 559 deliveries, the P0–P50
roadmap, etc.).

## What this is — and what it is NOT

- ✅ A reference store for uploaded archives, their manifest, and their
  checksums, so every promotion into runtime code is traceable.
- ❌ **Not** runtime code. Nothing in this directory is imported, built, or
  deployed. Files here are reviewed and *selectively* promoted into the real
  source tree via separate, single-scope PRs.

## The hard rule

> Uploaded ZIPs are **never** copied over the repository. They are
> `Extract → Diff → Select → Branch → PR → CI → Merge`.

The full policy lives in
[`docs/ops/UPLOADED_RESOURCE_INTEGRATION_DECISION.md`](../../docs/ops/UPLOADED_RESOURCE_INTEGRATION_DECISION.md).

## Layout

```
resources/company_os/
├── README.md                          # this file
├── UPLOADED_ARCHIVES_MANIFEST.json    # declared archives + classification + checksums
└── uploaded_archives/                 # drop uploaded *.zip here (git-ignored if large)
    └── .gitkeep
```

## How to use it

1. Drop the uploaded `*.zip` archives into `uploaded_archives/`.
2. Record each archive (name, sha256, classification) in
   `UPLOADED_ARCHIVES_MANIFEST.json`.
3. Run the comparison helper:

   ```bash
   ./scripts/compare_uploaded_resources.sh
   ```

   It extracts each archive to a temp workdir, summarizes contents, and
   classifies each as a **source candidate**, **build artifact**, or
   **resource/unknown** — so you know what is safe to promote and what must
   never be merged as source.
4. Promote **selected** files in single-scope PRs, in the order defined by the
   integration decision doc (tests → founder UI → sales/delivery → ops
   runbooks → build config last).

## Archive classification (summary)

| Archive | Classification | Merge policy |
|---|---|---|
| `dealix_resources_p0_p50.zip` | Resource vault | Add as resources only |
| `OKComputer_Dealix_OS.zip` | Source candidate | Selective merge |
| `OKComputer_تنفيذ_كامل_ومتوافق1.zip` | Source candidate | Compare against Dealix OS |
| `OKComputer_تسليم_PR_559.zip` | Historical source candidate | Selective merge only |
| `OKComputer_تسليم_PR_559_v1.zip` | Build artifact | Do **not** merge as source |
