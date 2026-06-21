# Dealix Safe Execution Rules

**Applies to**: All Claude Code sessions, GitHub Actions workflows, and automated scripts.  
**Version**: 1.0  
**Last updated**: 2026-06-10

---

## The Core Rule

> AI explores, analyzes, and generates. Humans approve and send.

No exception to this rule. Ever.

---

## Forbidden Actions (Hard Stops)

These actions must NEVER happen automatically or without explicit founder confirmation:

| Action | Why |
|--------|-----|
| Send WhatsApp message to a client/lead | PDPL + relationship risk |
| Send email to a client/lead | Spam risk, relationship risk |
| Post to LinkedIn | Brand risk |
| Issue an invoice or contract | Financial commitment |
| Merge a PR to `main` | Irreversible deployment risk |
| Delete client data | PDPL, irreversible |
| Rotate production secrets | Railway/infra breakage risk |
| Charge a credit card or payment method | Financial commitment |
| Create a GitHub release | Public-facing, triggers deploy |

---

## Script Safety Rules

### Every script must:
1. Write outputs to `company/runtime/YYYY-MM-DD/` (gitignored)
2. Print a summary of what it did at the end
3. Never import or call sending functions (`send_whatsapp`, `send_email`, etc.)
4. Handle missing input files gracefully (empty fallback, not crash)
5. Be testable with `bash -n script.sh` (syntax check passes)

### Scripts must NOT:
- Start Docker containers
- Start `npm run dev` or any frontend dev server
- Call external APIs without a `--dry-run` flag
- Write to `main` branch files that are tracked in git
- Delete any existing files

---

## GitHub Actions Rules

### Allowed in workflows:
- `python script.py` (dry-run mode)
- `bash -n script.sh` (syntax check)
- `npm run typecheck` (type check only)
- `npm run build` (build only, no deploy)
- `python -m pytest tests/` (unit tests)
- Health checks against localhost

### Forbidden in workflows:
- `docker-compose up`
- `npm run dev`
- Any `curl` to external services with write operations
- `git push` from within a workflow (use GitHub Actions bot if needed)
- Railway deploy triggers (use Railway's own GitHub integration)

---

## Commit & Branch Rules

| Rule | Detail |
|------|--------|
| Branch per Wave | One feature branch per Wave, no mixing |
| Draft PRs only | Never auto-merge, always draft first |
| No generated files | `company/runtime/` is gitignored |
| No secrets | `.env*` files are gitignored |
| Commit messages | Clear, imperative, reference Wave number |

### .gitignore — Always Ignored

```
company/runtime/
*.env
.env*
company/runtime/**/*.csv
company/runtime/**/*.md
```

---

## Data Handling Rules

| Data Type | Storage | Retention |
|-----------|---------|-----------|
| Lead contact info | `company/lead_research/` (local only) | 90 days max |
| Client project files | `clients/<client-name>/` | Project lifetime |
| Daily reports | `company/runtime/YYYY-MM-DD/` | 30 days local, never committed |
| Credentials | Environment variables only | Never in files |
| WhatsApp numbers | CRM CSV local only | 90 days max |

---

## Approval Checklist Before Any External Action

Before sending, issuing, or publishing anything:

- [ ] Content reviewed by founder personally
- [ ] No false claims about AI capabilities
- [ ] No client data included without consent
- [ ] No pricing promised without contract review
- [ ] Message drafted in approval queue, not sent automatically
- [ ] PDPL classification confirmed for any personal data involved

---

## Error Recovery Rules

If a script crashes:
1. Check `company/runtime/YYYY-MM-DD/` for partial output
2. Do NOT re-run automatically
3. Report the error with the exact traceback
4. Fix the root cause before re-running

If a PR fails CI:
1. Investigate the failure
2. Fix only what caused the failure
3. Do NOT use `--no-verify` or skip hooks
4. Create a new commit — never amend a pushed commit

If main branch is broken:
1. Stop all development
2. Notify founder immediately
3. Create a hotfix branch `fix/hotfix-description`
4. Never force-push to main

---

## Wave Execution Checklist

Before starting any Wave:

- [ ] Previous Wave PR is merged to `main`
- [ ] `git checkout main && git pull origin main`
- [ ] Read `CLAUDE.md`
- [ ] Read `docs/CEO_OPERATING_CONTEXT.md`
- [ ] State which Wave and what files will be touched
- [ ] Confirm no Docker, no npm dev, no auto-send

After completing any Wave:

- [ ] Validation commands ran and passed
- [ ] Branch pushed to origin
- [ ] Draft PR created with summary
- [ ] Stopped — did not proceed to next Wave
