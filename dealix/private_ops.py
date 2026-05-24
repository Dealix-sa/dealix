"""Private Ops helper — hybrid runtime data resolution for the CEO layer.

Sensitive CEO/finance data (decisions, capital allocations, strategic
assumptions, advisor updates, leverage time audits, hire-vs-automate logs)
lives OUTSIDE the repo at the path resolved by `private_ops_root()`. Evidence
and scorecard CSVs continue to live inside `docs/ops/` and
`docs/commercial/operations/` and are reachable via `resolve_csv()` when the
relpath is not in `SENSITIVE_REGISTRY`.

Resolution order for `private_ops_root()`:
  1. `$DEALIX_OPS_PRIVATE` if set and exists.
  2. `/opt/dealix-ops-private` if it exists (Linux production default).
  3. `~/.dealix-ops-private` if it exists (macOS dev fallback).
  4. None → `is_enabled()` returns False; callers must degrade gracefully.

This module never sends external traffic, never imports network clients,
and never writes outside the resolved PRIVATE_OPS root.
"""
from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SENSITIVE_REGISTRY: frozenset[str] = frozenset({
    "ceo/decisions.jsonl",
    "ceo/strategic_assumptions.csv",
    "ceo/capital_allocations.csv",
    "ceo/advisor_updates.jsonl",
    "ceo/leverage_time_audit.csv",
    "ceo/hire_vs_automate_log.csv",
})

SKELETON_FILES: dict[str, str] = {
    "ceo/decisions.jsonl": "",
    "ceo/strategic_assumptions.csv": (
        "id,assumption,owner,kill_trigger,status,last_reviewed,notes\n"
    ),
    "ceo/capital_allocations.csv": (
        "quarter,bucket,allocated_sar,actual_sar,roi_estimate,owner,notes\n"
    ),
    "ceo/advisor_updates.jsonl": "",
    "ceo/leverage_time_audit.csv": (
        "week_end,make_hours,manage_hours,move_hours,notes\n"
    ),
    "ceo/hire_vs_automate_log.csv": (
        "date,decision,role_or_function,reasoning,outcome\n"
    ),
    "finance/.keep": "",
    "people/.keep": "",
}

_README_BODY = """# Dealix PRIVATE_OPS

This directory holds sensitive Founder/CEO operating data that MUST stay
outside the git repository. It is created and templated by
`make bootstrap-runtime` (idempotent — only writes a file if it is missing).

Contents (template only — fill with your real data):

- `ceo/decisions.jsonl` — append-only decision log
- `ceo/strategic_assumptions.csv` — assumptions register
- `ceo/capital_allocations.csv` — quarterly capital allocation
- `ceo/advisor_updates.jsonl` — advisor / board updates
- `ceo/leverage_time_audit.csv` — founder time audit
- `ceo/hire_vs_automate_log.csv` — hire vs automate vs partner decisions

NEVER commit this directory to any repository.
"""


def private_ops_root() -> Path | None:
    """Resolve the active PRIVATE_OPS directory, or None if unavailable."""
    env = os.environ.get("DEALIX_OPS_PRIVATE")
    if env:
        p = Path(env).expanduser().resolve()
        if p.exists() and p.is_dir():
            return p
        return p
    for candidate in (
        Path("/opt/dealix-ops-private"),
        Path.home() / ".dealix-ops-private",
    ):
        if candidate.exists() and candidate.is_dir():
            return candidate.resolve()
    return None


def is_enabled() -> bool:
    """True iff PRIVATE_OPS root resolves AND exists on disk."""
    root = private_ops_root()
    return root is not None and root.exists() and root.is_dir()


def _is_sensitive(relpath: str) -> bool:
    norm = relpath.replace("\\", "/").lstrip("./")
    return norm in SENSITIVE_REGISTRY


def resolve_csv(relpath: str) -> Path | None:
    """Resolve a CSV path. PRIVATE_OPS-first; falls back to repo for non-sensitive paths."""
    return _resolve(relpath, suffix=".csv")


def resolve_jsonl(relpath: str) -> Path | None:
    """Resolve a JSONL path. PRIVATE_OPS-first; falls back to repo for non-sensitive paths."""
    return _resolve(relpath, suffix=".jsonl")


def _resolve(relpath: str, suffix: str) -> Path | None:
    norm = relpath.replace("\\", "/").lstrip("./")
    root = private_ops_root()
    if root is not None:
        candidate = root / norm
        if candidate.exists():
            return candidate
    if _is_sensitive(norm):
        return None
    repo_candidate = REPO_ROOT / norm
    if repo_candidate.exists():
        return repo_candidate
    return None


def write_jsonl_append(relpath: str, record: dict) -> Path:
    """Append a record to a JSONL file inside PRIVATE_OPS. Raises if disabled.

    Writes are confined to the PRIVATE_OPS root — sensitive registry files
    cannot be written to the repo even by accident.
    """
    root = private_ops_root()
    if root is None:
        raise RuntimeError(
            "PRIVATE_OPS not configured. Set DEALIX_OPS_PRIVATE or create "
            "/opt/dealix-ops-private (or ~/.dealix-ops-private) and run "
            "`make bootstrap-runtime`."
        )
    norm = relpath.replace("\\", "/").lstrip("./")
    target = root / norm
    target.parent.mkdir(parents=True, exist_ok=True)
    record_out = dict(record)
    record_out.setdefault("recorded_at", datetime.now(UTC).isoformat())
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record_out, ensure_ascii=False) + "\n")
    return target


def missing_private_ops_note(lang: str = "en") -> str:
    """Standard bilingual graceful message when PRIVATE_OPS is unavailable."""
    if lang == "ar":
        return (
            "PRIVATE_OPS غير مهيأ. اضبط متغير البيئة DEALIX_OPS_PRIVATE أو أنشئ "
            "/opt/dealix-ops-private (أو ~/.dealix-ops-private) ثم نفّذ "
            "`make bootstrap-runtime`. هذا تحذير غير قاتل — المخرجات الحساسة لن تُولَّد."
        )
    return (
        "PRIVATE_OPS is not configured. Set DEALIX_OPS_PRIVATE or create "
        "/opt/dealix-ops-private (or ~/.dealix-ops-private), then run "
        "`make bootstrap-runtime`. This is a non-fatal warning — sensitive "
        "outputs will be skipped."
    )


def bootstrap_skeleton() -> int:
    """Create the PRIVATE_OPS skeleton. No-op if env unset; idempotent."""
    root = private_ops_root()
    if root is None:
        print("PRIVATE_OPS=disabled — set DEALIX_OPS_PRIVATE to bootstrap.")
        print(missing_private_ops_note("en"))
        return 0
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for relpath, header in SKELETON_FILES.items():
        target = root / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(header, encoding="utf-8")
            created.append(str(target))
    readme = root / "README.md"
    if not readme.exists():
        readme.write_text(_README_BODY, encoding="utf-8")
        created.append(str(readme))
    print(f"PRIVATE_OPS_ROOT={root}")
    if created:
        print("Created:")
        for path in created:
            print(f"  {path}")
    else:
        print("No new files (skeleton already in place).")
    print("BOOTSTRAP_VERDICT=OK")
    return 0


def export_status() -> dict:
    """Lightweight status payload for API consumers / verifier."""
    root = private_ops_root()
    return {
        "private_ops_enabled": is_enabled(),
        "root": str(root) if root else None,
        "sensitive_registry": sorted(SENSITIVE_REGISTRY),
    }
