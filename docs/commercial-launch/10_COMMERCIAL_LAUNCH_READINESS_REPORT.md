# Commercial Launch Readiness Report

**Date:** 2026-06-04 · **Repo:** https://github.com/Dealix-sa/dealix
**Scope:** Dealix Commercial Launch OS only. (No AI-CV. No identity change.)

---

## 1. What was implemented

A complete, review-only **Commercial Launch Operating System** for the
Saudi/GCC B2B market:

- 5 launch verticals locked, each with a full playbook.
- A SAR offer ladder (6 rungs) with a conservative, no-guarantee claims policy.
- A **400+/day draft factory** producing founder-review-only drafts across 4
  channels in Arabic + English.
- Quality, compliance, and safety gates.
- A founder daily review bundle (CSV + Markdown + JSONL).
- A daily GitHub Actions workflow (no secrets, read-only, artifacts only).
- Tests, a readiness gate, docs, README updates, and a frontend page.

**Hard guarantee:** nothing is ever sent externally. No SMTP, no API send, no
LinkedIn/WhatsApp automation, no scraping, no secrets.

## 2. Files added

**Config:** `config/commercial_launch.json`, `commercial_verticals.json`,
`commercial_offers.json`, `commercial_channels.json`, `commercial_quality_gates.json`

**Engine (`dealix/commercial_launch/`):** `__init__.py`, `engine.py`,
`safety.py`, `review.py`, `readiness.py`, `leads.py`

**Scripts:** `commercial_generate_400_drafts.py`,
`commercial_founder_review_report.py`, `commercial_safety_audit.py`,
`commercial_launch_readiness.py`, `commercial_seed_leads_validate.py`

**Tests:** `test_commercial_generate_400_drafts.py`,
`test_commercial_safety_audit.py`, `test_commercial_launch_readiness.py`,
`test_commercial_no_external_send.py`

**Docs:** `docs/commercial-launch/00…10` + a committed lightweight
`sample_output/2026-06-04/`.

**Workflow:** `.github/workflows/commercial-draft-factory.yml`

**Data:** `data/commercial_seed_leads.example.jsonl`

**Frontend:** `apps/web/app/commercial-launch/page.tsx`

**Other:** README.md + README.ar.md clone/badge URLs corrected to
`Dealix-sa/dealix`; `.gitignore` ignores generated daily runs.

## 3. First 5 verticals (and why)

| Vertical | Why |
|----------|-----|
| Facilities Management & Maintenance | High volume of recurring work orders + SLA penalties + unbilled leakage — clear, measurable pain. |
| Contracting & Project Controls | Variation/claim value lost to slow manual approvals — high deal size, governance-shaped. |
| Real Estate & Property Operations | Renewals/arrears/maintenance depend on memory — recurring, repeatable workflows. |
| Legal & Professional Services | Partner time trapped in intake/billing admin; privacy-first fit for governed AI. |
| Consulting, Training & B2B Services | Proposals/delivery/reporting cap capacity — operations-shaped, repeatable. |

All five are operations-heavy, recurring-workflow businesses where a governed
diagnostic produces fast, provable value — and where Dealix's approval-first,
evidence-first posture is a differentiator, not a blocker.

## 4. Draft target

- **Minimum:** 400/day (175 cold email + 100 follow-up + 75 LinkedIn manual + 50 website form).

## 5. Generation result

```
python scripts/commercial_generate_400_drafts.py --target 400
→ accepted=478  rejected=0  target=400  used_real_leads=True
→ safety_passed=True (findings=0, draft_violations=0)
```

478 ≥ 400. Avg quality 100/100, avg compliance 100/100, bilingual, all drafts
`send_allowed=false / external_send_blocked=true / requires_founder_approval=true`.
See `docs/commercial-launch/sample_output/2026-06-04/`.

## 6. Safety audit result

```
python scripts/commercial_safety_audit.py
→ scanned_files=15  drafts_checked=478  findings=0  draft_violations=0  → PASS
```

No active external-send code. All drafts review-only.

## 7. Tests result

```
pytest -q --noconftest -p no:cacheprovider \
  tests/test_commercial_generate_400_drafts.py \
  tests/test_commercial_safety_audit.py \
  tests/test_commercial_launch_readiness.py \
  tests/test_commercial_no_external_send.py
→ 29 passed
```

> Note: the repo's `tests/conftest.py` imports the full FastAPI app stack
> (pydantic, fastapi, httpx). The commercial tests are pure standard library and
> run with `--noconftest`, so they need no app dependencies or secrets. This is
> also how the CI workflow runs them.

## 8. `make` checks result

| Command | Result | Notes |
|---------|--------|-------|
| `make env-check` | ✅ PASS | Environment contract OK. |
| `make security-smoke` | ⚠️ FAIL (pre-existing) | 17 findings, **all in pre-existing files** (billing/finance tests, launch docs). **None** in any commercial-launch file. Not introduced by this work. |
| `make api-contract-check` | ⛔ BLOCKED | `ModuleNotFoundError: No module named 'fastapi'` — app deps not installed in this environment. Fix: `make install-dev` (or `pip install -r requirements.txt`). Unrelated to commercial-launch code. |
| `make prod-verify` | ⛔ BLOCKED | Depends on api-contract-check (same missing-deps cause). |
| `make test` (full) | ⛔ BLOCKED | conftest imports fastapi/pydantic; full suite needs `make install-dev`. Commercial subset passes via `--noconftest`. |

**Resolution path for blocked checks:** run `make install-dev` to install the
full backend dependency stack, then re-run `make prod-verify` and `make test`.
These blockers are environment/dependency issues, not defects in the
commercial-launch deliverables.

## 9. Frontend status

- Added `apps/web/app/commercial-launch/page.tsx` (5 verticals, SAR offer
  ladder, trust-first/approval-first, bilingual AR+EN, clear CTA, no unproven
  claims).
- `npm install` ✅ and `npm run verify` (typecheck + build) ✅ both pass.

## 10. Backend status

- **No sending endpoints were added** (by design).
- The existing API was intentionally **not modified**: the app stack is not
  installable in this environment (no fastapi/pydantic), so adding routers could
  not be verified and would risk `api-contract-check`. The commercial-launch
  config is plain JSON and can be served read-only later via a small GET router
  once deps are available, following the repo's existing read-only pattern
  (`api/routers/commercial_readiness.py`). No POST/sending behaviour will be added.

## 11. Remaining risks

- Daily outputs are generated, not committed (CI artifacts) — operators must
  download artifacts or run locally to review.
- Placeholder mode produces `research_required` drafts when no real leads exist;
  these must be enriched before any manual send.
- security-smoke has pre-existing findings in unrelated files (tracked
  separately; out of scope for this PR).

## 12. External requirements (founder-owned, before any real send)

- **Domain DNS** configured for the sending domain.
- **SPF / DKIM / DMARC** published and validated.
- **Google Postmaster** tools set up and monitored.
- **Suppression list** operational owner named.
- **CRM / manual sending process** defined (founder's inbox + logging).
- **Calendly / payment / checkout** links (if used) wired into the diagnostic CTA.

## 13. Go / No-Go

- ✅ **GO** for draft generation.
- ✅ **GO** for founder manual review.
- ⛔ **NO-GO** for automated sending.
- ⛔ **NO-GO** for automated social posting.
- ⛔ **NO-GO** for ad spend.
- ⛔ **NO-GO** for WhatsApp cold outreach.
- ⛔ **NO-GO** for LinkedIn automation.

---

## 14. Addendum — Social & Media OS (added in expansion)

A second review-only factory was added on top of the outreach factory:

- **`config/commercial_social.json`**, **`dealix/commercial_launch/social.py`**,
  **`scripts/commercial_social_factory.py`**, **`tests/test_commercial_social_factory.py`**.
- 8 platforms (LinkedIn, X, Instagram, newsletter, blog outline, Google/Meta ad
  copy with **no spend**, PR pitch), 6 content pillars, bilingual AR + EN.
- Minimum 80/day; a typical run produces **136** posts.
- Every post: `post_allowed=false`, `external_post_blocked=true`,
  `requires_founder_approval=true`, `no_ad_spend=true`, `status=founder_review`.
- The shared safety audit scans `social_queue.jsonl` and fails on any posting
  automation, scheduling API, `post_allowed=true`, or `external_post_blocked=false`.
- The launch readiness gate adds `social_os_blocks_posting` and
  `social_factory_meets_minimum` checks (both PASS).
- A best-in-class bilingual `apps/web/app/commercial-launch/page.tsx` landing page
  (hero, stats, verticals, SAR offer ladder, daily-loop steps, Social/Media OS,
  trust-first section, FAQ, CTA) — `npm run verify` ✅.

Updated results: **9/9 readiness checks PASS**, **41 commercial tests pass**,
outreach 478 drafts + social 136 posts, combined safety audit clean.
See `docs/commercial-launch/11_SOCIAL_AND_MEDIA_OS.md`.
