# Patches — README

> **Status:** Optional. Apply manually. Never auto-merge.

## Files in this directory

| File | What it does | Risk |
| --- | --- | --- |
| `MAKEFILE_OPTIONAL_LAUNCH_TARGETS.patch` | Adds 10 `make launch-*` targets to the root `Makefile` | medium |
| `WEB_OPTIONAL_LAUNCH_COMMAND_ROOM.patch` | Scaffolds `/[locale]/ops/launch` page | medium |
| `API_OPTIONAL_LAUNCH_ENDPOINTS.patch` | Adds 4 dry-run endpoints under `/api/launch/` | medium |

## How to apply

```bash
# Inspect the patch first.
cat patches/MAKEFILE_OPTIONAL_LAUNCH_TARGETS.patch

# Apply if you agree.
git apply patches/MAKEFILE_OPTIONAL_LAUNCH_TARGETS.patch

# Verify.
make help | grep launch-

# Roll back if needed.
git apply -R patches/MAKEFILE_OPTIONAL_LAUNCH_TARGETS.patch
```

## How NOT to apply

- Do not use `git apply --3way` unless the patch fails to apply cleanly.
- Do not apply the web and API patches unless you really want the launch UI / endpoints.
- Do not commit the patch as a single commit; commit each applied patch separately so it is reversible.

## What to do if a patch fails

The patches target the `feature/dealix-v6-v10-scale-enterprise-os` branch at commit `f8b4cbb`. If the repo has moved on, the patches may fail. In that case:

1. Re-read the patch.
2. Apply the change manually to the new repo state.
3. Re-test with `make help` or `pytest` or `curl`.

The patch text is the source of truth. The patch file is a convenience.
