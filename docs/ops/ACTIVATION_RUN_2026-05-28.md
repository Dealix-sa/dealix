# Dealix — Full Activation Run / تشغيل تفعيل شامل
**Date / التاريخ:** 2026-05-28 · **Branch:** `claude/zealous-galileo-vQVYx`

> Goal / الهدف: turn the built-but-dormant system into a **verified, running, automated** operation — and prove it runs end-to-end (not "empty files"). تحويل النظام من *مبني وخامل* إلى *محقَّق + شغّال + مؤتمت*، مع إثبات تشغيله فعليًا.

---

## TL;DR / الخلاصة

The system is **real and runs end-to-end.** API boots with **881 routes**, the doctrine gate is green, the 10-step Revenue Sprint produces a real Proof Pack (score 100), and the daily automation scripts pass. Several real onboarding/runtime gaps were closed.

النظام **حقيقي ويعمل end-to-end.** الـAPI يقلع بـ881 مسارًا، بوابة العقيدة خضراء، Sprint من 10 خطوات يُنتج Proof Pack حقيقيًا (نتيجة 100)، وسكربتات الأتمتة اليومية تنجح. وأُغلقت فجوات تشغيل/onboarding حقيقية.

---

## Workstream A — Proof it runs / إثبات التشغيل

| # | Evidence / الدليل | Result |
|---|---|---|
| 1 | Dependency install + environment repair (broken Debian `cryptography`/`cffi`, missing auth stack `jose`/`passlib`/`pyotp`/`qrcode`/`slowapi`) | ✅ fixed |
| 2 | Doctrine gate — `pytest tests/test_no_*.py tests/test_commercial_doctrine.py` | ✅ **14 passed** |
| 3 | Representative suite — sprint / proof / status-cli / client_os / sales_os | ✅ **40 passed** |
| 4 | API boot — `uvicorn api.main:app`; `GET /health` → 200; `GET /` → operational | ✅ **881 routes** |
| 5 | `GET /api/v1/sprint/sample` — 10-step orchestrator on seed CSV | ✅ Proof Pack **score 100**, tier `case_candidate`, 1 capital asset, `governance_decision=allow_with_review` |
| 6 | Founder scripts — `dealix_status.py`, `dealix_pm_daily.py`, `dealix_founder_daily_brief.py` | ✅ all rc=0 |

**Environment note:** this container's Debian `cryptography` shipped a broken Rust binding (`pyo3 PanicException`) and `pip` pointed at a different interpreter than `python`. Both were repaired by installing clean wheels with `python -m pip`. The canonical install path is `requirements.txt` (used by `Dockerfile` + `ci.yml`).

---

## Workstream B — Real gaps closed / إغلاق الفجوات

- **B1 — Repo references.** Replaced the stale `VoXc2/dealix` slug with the real remote **`Dealix-sa/dealix`** across README(s), `SECURITY.md`, `pyproject.toml`, CI/issue templates, deploy guides, and `scripts/push_via_gh_api.py` (`OWNER`). CHANGELOG history left intact.
- **B2 — `pyproject.toml [project.dependencies]` kept minimal.** `requirements.txt` is the canonical runtime install path: both the `Dockerfile` and `ci.yml` run `pip install -r requirements.txt` (CI also runs `pip install -e .`, but requirements.txt already covers the full runtime tree). Rather than duplicate the ~24-package runtime manifest into `pyproject.toml`, the `[project.dependencies]` list is left at its minimal base set so there is a single source of truth and no second manifest to keep in sync. This also keeps the dependency-review surface limited to `requirements.txt`, where transitive advisories with no patched upstream (e.g. `ecdsa` CVE-2024-23342, pulled in by `python-jose`) are already pinned to their security floors. (`ummalqura` intentionally left optional — code guards it with a Hijri fallback.)
- **B3 — Transactional email wiring.** `api/routers/auth.py` invite + password-reset now send via the already-built `EmailClient` (`integrations/email.py`) in production, bilingual AR+EN, while preserving dev/test token-return behavior. These are **pre-whitelisted transactional** emails — they do **not** route through `approval_center` (distinct from outreach). Backed by a new test.
- **B4 — Webhook signature hardening.** `api/routers/customer_webhooks.py` now verifies inbound webhooks with constant-time HMAC and rejects invalid signatures (401). Backed by a test.
- **B5 — Automation bug.** `.github/workflows/founder_commercial_daily.yml:41` used the Windows launcher `py -3` on `ubuntu-latest` (guaranteed failure) → fixed to `python3`.
- **Doctrine fix.** The repo-wide LinkedIn / no-scraping string-lock guard test was failing on `main` (a docs file that named the guard tripped its own scan); allowlisted that documentation reference without weakening the guard.

---

## Workstream C — Automation activated / تفعيل الأتمتة

The scheduled GitHub workflows (`founder_commercial_daily.yml` @ 05:00 UTC Sun–Thu, `scheduled_healthcheck.yml`, `daily_digest`, `founder_weekly_scorecard`, …) fire automatically once merged to the default branch. Verified locally (all rc=0):

```
python scripts/run_dealix_unified_founder_day.py --quick          # → OK
python scripts/run_founder_full_autopilot.py --mode brief-only    # → VERDICT=OK
python scripts/run_full_commercial_ops_autopilot.py --execute --no-scripts  # → morning_run=PASS
```

**Single daily entrypoint (local):** `make cockpit` (→ `dealix_founder_daily_brief.py`) or `python scripts/dealix_pm_daily.py`.
**Scheduled entrypoint:** `founder_commercial_daily.yml` (now unblocked by B5).
**Founder-provided to go live on schedule:** repo secrets `DEALIX_API_BASE`, `DEALIX_ADMIN_API_KEY`, and a filled `data/warm_list.csv`.

---

## Workstream D — Launch Pack / حزمة التشغيل

Generated with **seed/demo data** (`customer_id=dealix_internal_demo`) — all customer-facing markdown ends with the required disclaimer; no real-customer outcome is implied; outreach drafts are **never sent**. Files in `data/activation_pack/` (git-ignored — they are outputs):

| Artifact | File | Regenerate |
|---|---|---|
| Proof Pack (JSON) | `sprint_sample_proofpack.json` | `GET /api/v1/sprint/sample` |
| Proof Pack (Markdown, bilingual) | `proof_pack.md` | `POST /api/v1/sprint/render/markdown` |
| Proof Pack (PDF / md-fallback) | `proof_pack.pdf` | `POST /api/v1/sprint/render/pdf` |
| PM daily brief | `pm_daily.txt` | `python scripts/dealix_pm_daily.py` |
| Founder daily brief | `founder_brief.txt` | `make cockpit` |
| Platform status | `dealix_status.txt` | `make v5-status` |
| Status snapshot (JSON) | `docs/snapshots/2026-05-28.json` | `make v5-snapshot` |
| Warm-list outreach **drafts** | `warm_list_drafts_DEMO.md` | `python scripts/warm_list_outreach.py` |
| Diagnostic proposal | `diagnostic_proposal_DEMO.md` | `python scripts/render_diagnostic_proposal.py --company …` |
| Monthly value report | `monthly_value_report_DEMO.md` | `value_os.monthly_report.generate(...)` |

---

## Founder-gated external go-live / خطوات بِيَد المؤسس (لم تُنفَّذ)

These cross the doctrine "external action requires approval" line and need **your** secrets/decision — prepared, not executed:

1. **Deploy to Railway** with real secrets (`APP_SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`, `ANTHROPIC_API_KEY`, …). `git push` to `main` triggers `railway_deploy.yml`.
2. **Moyasar live cutover** — `python scripts/moyasar_live_cutover.py` (charging is founder-flipped only).
3. **Email provider** — set `RESEND_API_KEY` (or SendGrid/SMTP) so B3 transactional emails actually send.
4. **Fill `data/warm_list.csv`** (from `data/warm_list.csv.template`) — 20 real warm contacts; then `python scripts/warm_list_outreach.py` drafts messages **for you to send manually**.
5. **Enable scheduled workflows against prod** — add the `DEALIX_API_BASE` / `DEALIX_ADMIN_API_KEY` repo secrets.
6. **Approve any real customer send** through `approval_center` (no autonomous external messages).

---

## Doctrine compliance / الالتزام بالعقيدة
- Doctrine gate green (14/14). No scraping, no cold outreach automation, no guaranteed-outcome claims.
- No invented KPIs — the value report honestly shows "none verified/observed this period."
- Every paid-flow output carries `governance_decision`; the sprint registered ≥1 capital asset.
- Transactional email (B3) kept separate from gated outreach.
- All generated artifacts labeled seed/demo.
