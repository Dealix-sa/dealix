# CLAUDE.md — Dealix Repo Guide for Claude Code Sessions

This file orients Claude Code (and any contributor) inside the Dealix repository. Read this first before making changes.

## 1. What Dealix is

Saudi-native B2B revenue engine. Three engines (Lead, Service, Trust), seven revenue streams, six OS tracks, five mandatory planes. The repo combines:

- A FastAPI backend (`api/`) with 170+ routers
- A Next.js 15 frontend (`frontend/`)
- A large `auto_client_acquisition/` package containing 50+ agent / governance / OS modules
- A `dealix/` package with trust, governance, business_now, masters, registers, transformation modules
- 300+ scripts under `scripts/` for daily founder operations, verification gates, generation, and integrations
- 39 GitHub Actions workflows for CI, deploy, founder daily/weekly routines, monitoring

## 2. Repo map (existing + canonical)

The canonical Company OS layout (`policies/`, `registries/`, `evals/gates/`) is being added **alongside** the existing structure, not replacing it. Both layouts coexist:

```
/home/user/dealix/
├── CLAUDE.md                       ← this file
├── Makefile                        ← targets: lint, test, v5-*, v10-*, brand-system, ..., everything
├── policies/                       ← NEW canonical (this PR)
│   └── dealix_control_policy.yaml  ← unified A1/A2/A3 + banned claims + external send rules
├── registries/                     ← NEW canonical (this PR)
│   ├── agent_registry.yaml         ← YAML mirror of agent_governance/agent_registry.py
│   └── machine_registry.yaml       ← workers, cron jobs, GitHub workflows
├── evals/
│   ├── gates/                      ← NEW canonical (this PR)
│   │   └── dealix_agent_eval_gate.yaml
│   ├── governance_eval.yaml        ← existing
│   ├── outreach_quality_eval.yaml  ← existing
│   └── arabic_quality_eval.yaml    ← existing
├── docs/
│   ├── ops/                        ← NEW audit reports (this PR)
│   │   ├── DEALIX_IMPLEMENTATION_AUDIT.md
│   │   ├── DEALIX_MISSING_SYSTEMS.md
│   │   └── DEALIX_FINAL_READINESS_REPORT.md
│   └── ... (200+ existing docs)
├── scripts/
│   ├── verify_*.py                 ← 30 existing + 19 new (this PR)
│   ├── verify_everything.py        ← NEW master orchestrator (this PR)
│   ├── generate_*.py               ← future PRs
│   └── ... (300+ existing scripts)
├── dealix/                         ← core Python packages (trust, governance, ...)
├── auto_client_acquisition/        ← agent OS modules (governance_os, agent_registry.py, ...)
├── api/routers/                    ← 170+ FastAPI routers
├── frontend/                       ← Next.js 15 + Tailwind
└── .github/workflows/              ← 39 existing + dealix-everything.yml (this PR)
```

The `apps/web/` layout described in long-form planning docs is a **future migration target**, not the current structure. Build under `frontend/` for now.

## 3. The 5 non-negotiables (Trust + AI Safety)

Every agent, worker, button, or AI call must respect these:

1. **A3 actions are never automatic** — autonomy class A3 = founder-only execute.
2. **A2 requires approval** — any external-effect agent action must be queued, not sent.
3. **No external send without explicit approval ID** — channel gateway rejects unsigned sends.
4. **No guaranteed claims** — `guaranteed sales`, `guaranteed revenue`, `guaranteed meetings`, `guaranteed roi`, `guaranteed results`, and Arabic equivalents (`ضمان مبيعات`, `ضمان عملاء`, `ضمان اجتماعات`, `ضمان إيراد`) are blocked at draft time.
5. **Prompt + output verification** — every AI output passes through `auto_client_acquisition/governance_os/draft_gate.py` before any external surface.

These are encoded in `policies/dealix_control_policy.yaml` and enforced by:
- `scripts/verify_policy_as_code.py`
- `scripts/verify_prompt_output_quality.py`
- `scripts/verify_ai_governance_system.py`

## 4. Patterns to mirror (do NOT reinvent)

### Verifier scripts
Template: `scripts/verify_quality_score.py` (28 lines, clean):
```python
REPO = Path(__file__).resolve().parents[1]
REQUIRED = ("docs/.../FILE.md", ...)
missing = [p for p in REQUIRED if not (REPO / p).is_file()]
for m in missing:
    print(f"missing_X:{m}", file=sys.stderr)
ok = not missing
print(f"X_PASS={'true' if ok else 'false'}")
return 0 if ok else 1
```

For aggregate verifiers (runs other scripts as subprocesses), use the `_run_script` helper pattern at `scripts/verify_dealix_ready.py:135-145`.

### Makefile targets
Format: `target: ## short description` — used by the help awk filter at line 19. Two-space indent. Use `$(PYTHON)` macro.

### Generators (future PRs)
Template: `scripts/generate_client_pack.py` — argparse, `sys.stdout.reconfigure(encoding="utf-8")`, write outputs under `{PRIVATE_OPS}/<domain>/`, exit 0/1.

### Frontend pages (future PRs)
Template: `frontend/src/app/.../page.tsx` — server components, components from `frontend/src/components/`, brand from `frontend/src/styles/dealix-brand.css`.

### API routers
Template: `api/routers/auth.py` — `router = APIRouter(prefix="/...", tags=["..."])`, async with `Depends(get_db)`.

## 5. Brand palette

The repo brand is **Deep Green + Gold** (not Deep Navy + Silver). Keep this:

```
Deep Green:  #0a4d3f
Gold:        #c9a961
Sand:        #f4f0e8
Charcoal:    #1a1a1a
Success:     #2d7a4f
```

Source: `frontend/src/styles/dealix-brand.css`. Tokens file `frontend/src/lib/brand-tokens.ts` is a future PR.

## 6. How to verify the whole Company OS

```bash
make everything        # runs scripts/verify_everything.py (master gate)
make ai-governance     # trust + policy + agents + eval gate
make brand-system      # brand assets + tokens
make company-os        # layer-level existence check
```

Output format is intentional: layer-by-layer `PASS`/`FAIL`, then `Missing:` list, then `Failed:` list, then `Risk:` list, then `RESULT: PASS` or `RESULT: FAIL`.

A FAIL on first run is expected and useful — it pinpoints exactly which layer to build next.

## 7. Branches and PRs

- Default working branch: `main`
- Active epic: `claude/epic-curie-RZG1P` (this branch)
- After push, create a **draft PR** (the harness expects this).
- Do not push to `main` directly.

## 8. What this PR does NOT do

Deferred to later PRs:
- `apps/web/` migration
- 30+ `generate_*.py` report scripts
- `api/internal/` founder console internal API
- Private ops bootstrap script (`scripts/bootstrap_private_ops_runtime.py`)
- Brand token system + extended brand components
- 7 additional GitHub workflows (per-layer)

This PR scope: **verification + audit layer only.**
