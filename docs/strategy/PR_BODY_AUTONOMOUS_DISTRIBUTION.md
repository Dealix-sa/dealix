# PR — Autonomous Distribution Engine (Wave 16)

**Branch:** `claude/vibrant-lovelace-KwZio` → `main`
**Type:** feat (new unified engine + 4 loops + bilingual docs)
**Open at:** https://github.com/VoXc2/dealix/pull/new/claude/vibrant-lovelace-KwZio

---

## Summary (EN)

This PR adds the unified **Autonomous Distribution Engine** — a single contract that wires Dealix's 9 canonical OS modules (data_os, governance_os, sales_os, proof_os, value_os, capital_os, adoption_os, client_os, friction_log) into a governable, end-to-end customer journey. It adds the 4 cron-style loops (morning / evening / weekly / monthly), the FastAPI router, the CLI runner, and the bilingual operating docs.

**No external sends. No new doctrine bypasses. All outreach remains DRAFT-ONLY.**

## الملخص (AR)

تضيف هذه الـ PR محرّك **التصريف الذاتي** الموحد — عقد واحد يربط الموديولات الكانونية التسع في Dealix داخل رحلة عميل من البداية للنهاية، محوكَمة وقابلة للتدقيق. تضيف 4 حلقات (صباحية / مسائية / أسبوعية / شهرية)، router للـ FastAPI، CLI runner، ووثائق تشغيل ثنائية اللغة.

**لا إرسال خارجي. لا تجاوز للحوكمة. كل outreach يبقى DRAFT-ONLY بانتظار موافقة المؤسس.**

---

## What's in scope

### Engine (`auto_client_acquisition/autonomous_distribution/engine.py`)

| Function | Inputs | Output | Doctrine |
|---|---|---|---|
| `process_lead` | row + passport + ICP + answers | `LeadDecision` | DATA + GOVERNANCE + SALES; PDPL gate enforced |
| `audit_outreach_draft` | text + channel | `OutreachDraftDecision` | LinkedIn/WhatsApp always BLOCK |
| `process_payment` | invoice + status + proof_pack_score | `PaymentDecision` | Capital eligible only if paid AND score ≥ 70 |
| `assemble_proof_pack` | 14 sections | `ProofPackDecision` | publish requires score ≥ 70 + founder approval |
| `assess_retainer` | adoption + workflow gates | `RetainerDecision` | uses `wave2_retainer_eligibility` canonical check |

### Loops (`auto_client_acquisition/autonomous_distribution/loops.py`)

- `morning_loop()` — daily 6am AST — pipeline + draft queue
- `evening_loop()` — daily 8pm AST — KPIs + friction + tomorrow top-4
- `weekly_loop()` — Sunday 6pm AST — retainers + capital reconciliation
- `monthly_loop()` — Day-1 — 30/60/90 milestone audit

### FastAPI router (`api/routers/autonomous_distribution.py`)

10 endpoints under `/api/v1/autonomous-distribution/*`:
- `GET /health`
- `POST /lead/process`
- `POST /outreach/audit`
- `POST /payment/process`
- `POST /proof-pack/assemble`
- `POST /retainer/assess`
- `GET /loops/{morning,evening,weekly,monthly}`

### CLI runner (`scripts/run_autonomous_distribution_loop.py`)

```bash
python scripts/run_autonomous_distribution_loop.py morning
python scripts/run_autonomous_distribution_loop.py evening
python scripts/run_autonomous_distribution_loop.py weekly
python scripts/run_autonomous_distribution_loop.py monthly --days-since-launch 30
```

Writes bilingual markdown to `data/autonomous_loops/`.

### Docs (bilingual)

- `docs/strategy/DEALIX_AUTONOMOUS_DISTRIBUTION_MASTER_PLAN_AR.md` — full plan (9 layers, 4 loops, customer journey, integrations, KPIs, 30/60/90, decision rules, rollback)
- `docs/strategy/DEALIX_AUTONOMOUS_DISTRIBUTION_VERIFICATION_AR.md` — per-layer verdict + test summary
- `docs/sops/SOP_9_LAYERS_AR_EN.md` — one-page SOP per layer
- `docs/runbooks/FOUNDER_LOOPS_RUNBOOK_AR_EN.md` — how to invoke each loop + cron schedule
- `docs/customer/HOW_THE_ENGINE_WORKS_AR.md` — customer-facing Arabic explainer
- `docs/gtm/LINKEDIN_LAUNCH_SEQUENCE_AR_EN.md` — 5 LinkedIn drafts (MANUAL publish)

### Tests

`tests/autonomous_distribution/test_engine.py` (19 tests) + `tests/autonomous_distribution/test_loops.py` (15 tests) = **34 passing**.

7 doctrine guard tests still passing (cold whatsapp, guaranteed claims, linkedin auto, pii in logs, scraping engine, source no answer, source passport no ai).

---

## Test plan

- [x] `python -m pytest tests/autonomous_distribution/ -v --no-cov` → 34 passed
- [x] `python -m pytest tests/test_no_*.py --no-cov` → 10/10 unaffected guards pass (`test_no_linkedin_scraper_string_anywhere.py` has a pre-existing failure on `docs/enterprise_architecture/TESTS_REQUIRED.md` — NOT caused by this PR)
- [x] `python scripts/run_autonomous_distribution_loop.py all` → all four reports generated
- [x] `bash scripts/dealix_capability_verify.sh` → `DEALIX_READY=true`, 6/6 services
- [x] `bash scripts/dealix_full_ops_productization_verify.sh` → 16/17 PASS (`FORBIDDEN_CLAIMS` is a pre-existing landing-page stale allowlist, untouched by this PR)
- [x] FastAPI router routes inspected — all 10 endpoints reachable
- [x] No live sends, no live charges, no doctrine overrides
- [x] All bilingual customer-facing markdown ends with "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"

---

## Doctrine reinforcements

1. No scraping — `process_lead` BLOCKS source_type=scraping.
2. No cold WhatsApp — `audit_outreach_draft` BLOCKS channel=whatsapp.
3. No LinkedIn automation — `audit_outreach_draft` BLOCKS channel=linkedin.
4. No unsourced claims — `policy_check_draft` already catches; engine surfaces it.
5. No guaranteed sales — same gate.
6. No PII in logs — engine never logs raw lead_row.
7. No source-less answers — Source Passport gate enforced.
8. No external action without approval — every send is DRAFT-ONLY.
9. No agent without identity — `agent_transparency_card_valid` part of client_os contract.
10. No project without Proof Pack — `assemble_proof_pack` is the canonical gate.
11. No project without Capital Asset — `process_payment` mints the asset only when proof_score ≥ 70 + paid.

---

## Founder decisions pending

| Blocker | Action |
|---|---|
| Moyasar live cutover | Founder flips `MOYASAR_MODE=live` in Railway env + runs `scripts/moyasar_live_cutover.py` |
| `data/warm_list.csv` empty | Founder fills it; loop drafts outreach into approval_center |
| First 5 free diagnostics | Founder picks 5 contacts from warm list |
| `FORBIDDEN_CLAIMS` stale allowlist | Pre-existing landing-page cleanup — separate PR |

---

https://claude.ai/code/session_01GwAJCFi6UJTYaJFMdLPtXd
