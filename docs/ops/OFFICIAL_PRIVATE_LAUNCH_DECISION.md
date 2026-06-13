# Dealix — Official Private Launch Decision / قرار الإطلاق الخاص الرسمي

- **Date / التاريخ:** 2026-06-07
- **Repository:** `Dealix-sa/dealix`
- **Base commit evaluated / الكوميت المُقيَّم:** `main` @ `7bd43c3`
- **Decision owner / صاحب القرار:** Founder (`@VoXc2`)
- **Author of this evidence pack:** automated launch review (read-only; merged/closed/charged nothing)

> **Honesty rule / قاعدة الصدق:** "Green / أخضر" = a command was actually run on
> the evaluated commit and passed. "External / خارجي" = founder-only, completable
> only in a provider dashboard. No claim here exists without evidence on this page.
>
> _Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة._

---

## 0. Verdict (TL;DR) / الخلاصة

| Decision / القرار | Verdict | One-line reason / السبب |
|---|---|---|
| **Private Launch** (warm intros · paid diagnostic · Command Sprint · manual/test payment · draft-only outreach) | **GO — conditional / مشروط** | Doctrine safety is intact and the truth-label contract already says go; conditions in §0.1. |
| **Public Launch / Paid-beta / Live charge** | **NO-GO / لا** | `REVENUE_LIVE=no`, `LIVE_CHARGE_READY=no`; needs ≥1 signed+paid+delivered customer + proof pack + Moyasar live (founder). |

### 0.1 Conditions to flip Private Launch fully green / شروط الإطلاق الخاص

1. **Merge code RC #650** — greens the doctrine-guard battery (evidence §2). _Verified required._
2. **Close the `make doctor` / `security-smoke` gap** (§2.A) — small, decision-required; **not** covered by #650.
3. **Founder-only externals** (§4) — production secrets + DNS/TLS for the public surface.
4. **Payments stay test/manual** — no live charge until §0 Public verdict flips.

This is a **private revenue launch, not a public SaaS launch.** Sell a *result*
(Command Sprint → Proof Pack), not "the whole platform."

---

## 1. Verdict ↔ codified truth labels / مطابقة القرار للعقد المُختبَر

The single source of truth is **`docs/phase-e/00_GO_NO_GO.md`**, mirrored in
**`tests/test_truth_labels_v11.py`** (this file **passed** in §2). This decision
does not contradict any label — it operationalizes them.

| Truth label | Value | Maps to this decision |
|---|---|---|
| `PHASE_E_GO` | `yes` | Founder may begin warm intros today → **Private GO** |
| `FIRST_CUSTOMER_READY` | `yes_for_warm_intro_and_diagnostic` | Diagnostic + draft message ready → **Private GO** |
| `PAID_PILOT_READY` | `yes_manual_payment_only` | Manual/test payment only → **Private GO**, no live charge |
| `PAID_BETA_READY` | `no_until_payment_or_written_commitment` | Blocks paid-beta claims → **Public NO-GO** |
| `REVENUE_LIVE` | `no` | No public revenue/ROI claims → **Public NO-GO** |
| `LIVE_SEND_READY` | `no` | Draft-only content; no live WhatsApp/email/LinkedIn send |
| `LIVE_CHARGE_READY` | `no` | Moyasar test/manual only |
| `COLD_WHATSAPP_READY` | `never` | Hard-pinned; warm-intro-only forever |

To change any label, follow the safe-flip procedure in `docs/phase-e/00_GO_NO_GO.md`
(edit label + test in the same PR, attach evidence). Never flip `LIVE_*` or
`COLD_WHATSAPP_READY` without founder + safety review.

---

## 2. Code readiness — gate evidence (run 2026-06-07) / جاهزية الكود بالأدلة

All commands run on `main` @ `7bd43c3` (identical to this branch and to #650's base).

| Gate | Command | Result | Evidence |
|---|---|---|---|
| Env contract | `make env-check` | ✅ **PASS** | `Environment contract OK: backend and frontend templates checked` |
| Alembic single head | `scripts/check_alembic_single_head.py` | ✅ **PASS** | `OK: single Alembic head (013)` |
| API contract | `make api-contract-check` | ✅ **PASS** (exit 0) | schema exports cleanly; **no committed baseline** at `docs/architecture/openapi.json` to diff against (see §2.B) |
| In-process API smoke | `scripts/smoke_inprocess.py` | ✅ **PASS** | app boots; `GET /health` → **200** `{"status":"ok","service":"dealix-api","version":"3.0.0"}`; pricing/brief/launch-report → 200 |
| Truth labels | `pytest tests/test_truth_labels_v11.py` | ✅ **PASS** | GO/NO-GO contract intact |
| Doctrine-guard battery | `pytest tests/test_landing_forbidden_claims.py tests/test_no_linkedin_scraper_string_anywhere.py tests/test_v7_secret_leakage_guard.py` | ❌ **4 failed on `main`** → **fixed by #650** | exact failures match #650's allowlist scope; **no guard disabled** by the fix |
| Security smoke | `make security-smoke` | ❌ **FAIL (exit 1)** | see §2.A — **NOT fixed by #650** |
| Doctor (composite) | `make doctor` | ❌ **FAIL** | fails only because `security-smoke` fails (env + alembic pass) |

Independent of this run, **#650's own report** records the full suite at
**4628 / 4726 passing** with the residual categorized as: ~33 parallel-isolation
flakiness, ~20 env-gated (no Postgres in sandbox), 5 shell-verifier meta-tests, and
**~9 real drift needing a product decision** — notably the **billing free-tier**
money-safety question (`amount_halalas == 0` for the rung-0 Free Diagnostic vs. the
"all plans positive" invariant). That decision is **founder/PM**, not a test tweak.

### 2.A Honest finding — `make doctor`/`security-smoke` is NOT green (beyond #650)

`scripts/security_smoke.py` exits 1 on `main` for two reasons, **neither touched by
#650's 7 files**:

1. **3 git-tracked `.env.*.example` template files** at repo root —
   `.env.prod.example`, `.env.railway.example`, `.env.staging.example`. The script's
   allowlist (`security_smoke.py:89`) permits **only** `.env.example`.
2. **~16 fake-token lines** in test fixtures (`tests/test_agent_observability_integration.py`,
   `tests/test_billing_moyasar_safety.py`, `tests/test_finance_os_no_live_charge_invariant.py`, …)
   and 2 docs that don't carry an allowed placeholder marker on the same line.

> **Resolution required (small, code-side, decision-needed):** either (a) extend
> `security_smoke.py` to allow `*.example` env templates + add the fixture lines to
> its skip set, or (b) relocate/remove the extra committed `.env.*.example` files.
> Do this in the RC, not by weakening the gate. This is a **condition** for "fully
> green CI," but it is **not** a doctrine/safety violation and does **not** block the
> Private Launch business motion (warm intros, diagnostic, Sprint).

### 2.B Other honest infra notes (non-blocking)

- **pyproject ↔ requirements divergence:** `pip install -e ".[dev]"` alone does **not**
  install `python-jose` (and others), so the app won't import from the `[dev]` extra
  only. CI installs from `requirements.txt`, so CI is unaffected — but `make install-dev`
  by itself is insufficient for a local run. (PR **#636** appears to target this; see triage.)
- **No committed OpenAPI baseline** (`docs/architecture/openapi.json`): the contract
  check passes by exporting, but cannot detect breaking changes without a baseline.
  Generate one with `make openapi-export` and commit it in the RC.
- **`/health` & `/health/deep` are canonical** (real, schema-included). The legacy
  `/healthz` alias remains; #650 migrates the 3 stale landing pages to `/health`.

---

## 3. Release-candidate strategy — one RC, not a wave of merges / استراتيجية الإصدار

**The #1 project risk is PR sprawl: 50 open draft PRs, none merged, `main` still at
#559.** Do **not** merge them as a wave. Collapse to a minimal, auditable set:

| Role | PR | Action | Why |
|---|---|---|---|
| **Code RC** | **#650** | Merge after CI green | Fixes doctrine-guard battery (allowlist-only, no guard disabled) + canonical `/health`. Verified in §2. Add §2.A + §2.B fixes onto it (or a tiny follow-up) before flipping CI green. |
| **Claude wiring RC** | **#640** | Merge | Lean `CLAUDE.md` (defers to existing `AGENTS.md`) + `.github/workflows/claude-code.yml` with **minimal permissions** (`contents`/`pull-requests`/`issues: write` + `id-token: write`). |
| Duplicate | **#638** | **Close** in favor of #640 | Same two files, ~85 KB heavier; #640 is cleaner since `AGENTS.md` already exists on `main`. |
| Salvage-then-close | **#636, #630, #598** | Review for reusable CI/dep fixes, then close | #636 = pyproject divergence (relevant to §2.B); #630/#598 = Gitleaks/Trivy hardening. |
| Superseded waves | the remaining ~44 launch/Company-OS/Wave/GTM/growth/brand drafts | **Close with reason** (recommendation only) | Overlapping historical waves; their durable assets are already on `main` or in #650/#640. |

> The full per-PR triage table lives in the **pull-request description** of this
> change (recommendation only — this review closes/merges nothing).

**Rule:** ONE code RC (#650) + ONE wiring RC (#640) + this decision PR. Everything
else is closed or salvaged, never merged blindly.

---

## 4. Founder-only blockers / مهام المؤسس فقط

Cannot be done by the repo or any agent (doctrine: never charge a customer, never
send external without approval, Moyasar live is founder-flipped only). **These already
have documentation — do not duplicate it; execute it.**

| Blocker | Where it's already documented | Status |
|---|---|---|
| Production secrets (Railway/host + GitHub) | `docs/ops/PRODUCTION_SECRETS_CHECKLIST.md`, `docs/ops/PRODUCTION_ENV_TEMPLATE.md` | ☐ external |
| DNS + TLS for `api.dealix.me` | `docs/ops/GO_LIVE_INDEX.md` (workstream D) | ☐ external |
| Moyasar KYC → live cutover | `docs/ops/MOYASAR_KYC_CHECKLIST.md` → `scripts/moyasar_live_cutover.py` | ☐ external |
| Payment + webhook dashboards verified | `docs/integrations/PAYMENT_MOYASAR_LIVE.md` | ☐ external |
| Warm-list fill (no scraping, no cold) | `data/warm_list.csv` → `scripts/warm_list_outreach.py` (drafts only, approval-gated) | ☐ external |
| First real customer (signed + paid + delivered) | this doc §8 + Proof Pack | ☐ external |

> **Secret hygiene:** never store structured JSON as a single secret; one value per
> secret. Admin keys are server-side only — never in browser/`NEXT_PUBLIC_*`. Rotate
> on any suspected exposure (`docs/security/KEY_ROTATION.md`).

---

## 5. `main` branch protection (founder applies) / حماية الفرع الرئيسي

No agent tool can set branch protection here, and there is no `gh` CLI in this
environment — so the founder applies this once, with a token that has admin on the repo.

**Required ruleset:** require PR before merge · ≥1 approval · dismiss stale approvals ·
require status checks + branches up to date · require conversation resolution · require
linear history · restrict force-push · restrict deletion.

```bash
# Confirm exact check "contexts" from a recent green run first, then:
curl -X PUT \
  -H "Authorization: Bearer $GITHUB_ADMIN_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Dealix-sa/dealix/branches/main/protection \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": ["python-checks", "web-build", "frontend-build", "CodeQL", "dependency-review", "official-launch-verify"]
    },
    "enforce_admins": true,
    "required_pull_request_reviews": {
      "dismiss_stale_reviews": true,
      "required_approving_review_count": 1
    },
    "restrictions": null,
    "required_linear_history": true,
    "allow_force_pushes": false,
    "allow_deletions": false,
    "required_conversation_resolution": true
  }'
```

> Verify the exact `contexts` strings against a green CI run (job names from `ci.yml`,
> `security.yml`, `official-launch-verify.yml`) before enabling `strict`, or merges
> will block on a check name that never reports.

---

## 6. Launch scope / نطاق الإطلاق

**Allowed now / مسموح الآن** (Private Launch):
- Private demos · paid Diagnostic · Command Sprint · Proof Pack delivery
- Dry-run automation · approval-first customer workflows
- Manual / Moyasar **test-mode** payment

**Not allowed / غير مسموح** (until verdicts/labels flip with evidence):
- Cold WhatsApp (never) · scraping · LinkedIn automation
- Guaranteed-outcome claims · automated/live charging
- Public revenue/ROI claims without evidence

Enforced by the **8 hard gates** (§9) and the doctrine-guard tests.

---

## 7. Rollback / التراجع

1. **Redeploy last-green** on Railway (UI redeploy ≈ 30s) — `docs/ops/DEPLOY_RUNBOOK.md`.
2. **Disable live checkout** (revert Moyasar to test mode / pull the live key).
3. **Rotate impacted secrets** — `docs/security/KEY_ROTATION.md`.
4. **Freeze outbound workflows** (all sends are draft-only by default; keep them so).
5. **File the incident** — `docs/ops/INCIDENT_RESPONSE_QUICKCARD.md` (5-phase SOP).

---

## 8. First-revenue plan / خطة أول إيراد (founder-led, draft-only)

Offer ladder (live source: `frontend/src/components/gtm/PricingPage.tsx`):

| Rung | Offer | Price (SAR) | Note |
|---|---|---|---|
| 0 | Free Diagnostic / تشخيص مجاني | 0 | No card; entry wedge |
| 1 | Revenue Intelligence Sprint | 499 (one-time) | 48h; the **wedge to sell first** |
| 2 | Agency Proof Pack | 1,500 (one-time) | Full L0–L5 Proof Pack |
| 3 | Managed Ops Retainer | 2,999–4,999 / mo | **Only after a successful Proof Pack** (non-negotiable: no upsell before proven value) |
| 4 | Custom AI Project | 5,000–25,000 | Signed scope + final Proof Pack |

**Best first sector:** B2B services (consultancies, training firms, marketing
agencies, B2B real-estate, small tech) — they have offers, follow-ups, and decisions.
Not government/large-enterprise first.

**Founder to fill / يكملها المؤسس:**

```
Target customer:
Offer (start at the 499 Sprint):
Price:
Pipeline (warm intros only):
Target close date:
```

---

## 9. Non-negotiables honored / الثوابت غير القابلة للتفاوض

The **8 hard gates** (`scripts/wave11_hard_gate_audit.sh`, asserted by
`tests/test_constitution_closure.py`):

`NO_LIVE_SEND` · `NO_LIVE_CHARGE` · `NO_COLD_WHATSAPP` · `NO_LINKEDIN_AUTO` ·
`NO_SCRAPING` · `NO_FAKE_PROOF` · `NO_FAKE_REVENUE` · `NO_BLAST`

This decision adds **no code**, performs **no external action**, charges **no one**,
exposes **no secret**, and **disables no guard**. `/health` and `/health/deep` are
confirmed canonical and schema-included (§2).

---

## 10. Summary / الملخص

**English:** Dealix is past "build more." The bottleneck is decide + consolidate. The
doctrine safety perimeter is intact, the GO/NO-GO truth-label contract passes, and the
app boots with a healthy `/health`. The required code RC is **#650** (doctrine guards +
canonical `/health`), plus **#640** for governed Claude Code wiring; close **#638** as a
duplicate and supersede the other ~44 launch drafts. One small, honest gap remains
beyond #650 — `make doctor`/`security-smoke` (§2.A) — to fix in the RC, not by weakening
the gate. **Private Launch: GO (conditional).** **Public/Paid-beta/Live charge: NO-GO**
until a real, paid, delivered customer + Moyasar live (founder). Fastest path to money:
the **499 Command Sprint** for a B2B-services customer, then a Proof Pack, then Managed Ops.

**عربي:** Dealix تجاوز مرحلة "نبني أكثر"؛ عنق الزجاجة هو **القرار والتجميع**. محيط
الحوكمة سليم، وعقد GO/NO-GO المُختبَر ناجح، والتطبيق يعمل و`/health` يرجع 200. مرشّح
الإصدار للكود هو **#650** (حُرّاس الـ doctrine + `/health` القانوني)، و**#640** لربط
Claude Code بصلاحيات أدنى؛ أغلق **#638** كمكرر، واعتبر بقية ~44 مسودة إطلاق مُستبدَلة.
تبقّى فرق صغير صادق خارج #650 — بوابة `make doctor`/`security-smoke` (§2.A) — يُصلَح داخل
الـ RC لا بإضعاف البوابة. **الإطلاق الخاص: GO مشروط.** **الإطلاق العام/المدفوع/السحب
الحي: لا** حتى أول عميل حقيقي مدفوع ومُسلَّم + Moyasar حي (المؤسس). أسرع طريق للإيراد:
**Command Sprint بـ499** لعميل خدمات B2B، ثم Proof Pack، ثم Managed Ops.
