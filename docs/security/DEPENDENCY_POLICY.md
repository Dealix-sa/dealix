# Dependency Policy

## Purpose
Govern how Dealix adds, upgrades, and retires dependencies.

## Rules
1. **Add a dependency only when needed.** Prefer the standard library or existing dependency.
2. **Pin exact versions** in `requirements.txt`.
3. **License**: only MIT, Apache-2.0, BSD-2/3, ISC, or PSF in production.
4. **Provenance**: only PyPI for Python; only the official npm registry for JS.
5. **Security history**: skip packages with unresolved high-severity advisories in the last 90 days.
6. **Maintainer activity**: prefer packages with a release in the last 12 months.

## Workflow when adding a dependency
1. Open a draft PR with the addition.
2. Document in the PR description: purpose, alternatives considered, license.
3. Run `pip-audit` (or equivalent) and attach the result.
4. Pass the dependency-review workflow.
5. Merge only with one approval.

## Workflow when upgrading
1. Read the release notes.
2. Bump in a dedicated PR with title `chore(deps): bump <name> from X to Y`.
3. Run the full test suite locally and in CI.
4. Roll back immediately if regression detected.

## Retirement
- If a dependency is no longer used, remove it the same week.
- Document removal in the PR.

## Forbidden
- Forks or arbitrary git URLs for production code.
- `:latest` Docker tags in production.
- Pulling internal binaries from untrusted mirrors.

## Auditing
- Run `python -m pip list --outdated` weekly.
- Triage CVEs from Dependabot within 5 business days.
- Annually: full SBOM export and archive.
