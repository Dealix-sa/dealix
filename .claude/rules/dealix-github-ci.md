# Dealix GitHub & CI Rules

## Branch policy

- Agent/Claude branches: `claude/<slug>`
- Feature branches: `feat/<wave-name>`
- One Wave per PR — never mix unrelated systems.
- All PRs start as **draft** — never auto-merge.
- Never force-push `main`.

## Commit rules

- Commit message: imperative, English, under 72 chars.
- Never commit: `.env`, secrets, `reports/runtime/`, `node_modules`, `*.zip` archives.
- Never commit generated runtime outputs (`*_REPORT.md`, `*.csv` leads, `approval_queue*`).
- Always verify with `git diff --check` before committing.

## Required CI workflow

File: `.github/workflows/full-repo-test-matrix.yml`

Required gates (all must pass):
1. `python-version`
2. `python-compileall-core-surfaces`
3. `env-contract`
4. `security-smoke`
5. `no-auto-external-send`
6. `company-launch-ready`
7. `pytest-launch-critical-suite`
8. `apps-web-npm-ci`
9. `apps-web-verify`

Optional/non-blocking: `pytest-full-suite-diagnostic`, `launch-os-dry-runs`, `production-verify-bundle`, `testsprite-env-check`, `testsprite-mcp-smoke`

## Forbidden in CI workflows

- Do not add steps that run `docker` or `docker-compose`.
- Do not add `npm run dev` or any dev server start.
- Do not add steps that send external messages.
- Do not disable or skip safety gates to make CI green.
- Do not hide real test failures.

## PR body must include

- What changed (specific files and why)
- Verification output (`make full-repo-test` result)
- What NOT to do next (explicit)
- No secret values, no fake metrics

## Local verification before push

```bash
git status --short
git diff --check
make full-repo-test
npm --prefix apps/web run verify
python3 scripts/ops/check_railway_production_env.py || true
```
