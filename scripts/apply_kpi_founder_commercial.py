#!/usr/bin/env python3
"""Apply founder commercial KPI entries from registry into kpi_baselines.yaml.

Merges optional dealix/transformation/kpi_founder_commercial_import.yaml (gitignored)
into the registry before apply. Rejects placeholder source_ref values.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
_REGISTRY = _REPO_ROOT / "dealix/transformation/kpi_founder_commercial_registry.yaml"
_IMPORT = _REPO_ROOT / "dealix/transformation/kpi_founder_commercial_import.yaml"
_BASELINES = _REPO_ROOT / "dealix/transformation/kpi_baselines.yaml"

_FORBIDDEN_REF = re.compile(
    r"REPLACE:|fake|invented|synthetic_default|example_only|placeholder",
    re.I,
)

# Patterns indicating the founder has not yet supplied real CRM data.
# Any of these in an import file => WAITING_ON_FOUNDER_CRM_EXPORT.
_PLACEHOLDER_TOKEN = re.compile(
    r"<fill_from_crm>|<FILL_FROM_CRM>|\bTBD\b|not_synced_yet|pending_founder_export",
    re.I,
)

_WAITING_VERDICT = "WAITING_ON_FOUNDER_CRM_EXPORT"


def _is_placeholder_value(val: object) -> bool:
    """Return True if a value is the obvious placeholder default (None or 0)."""
    if val is None:
        return True
    try:
        return float(val) == 0.0
    except (TypeError, ValueError):
        return False


def _is_placeholder_ref(ref: str) -> bool:
    """Return True if a source_ref looks like a placeholder, not a real CRM export ref."""
    if not ref or not ref.strip():
        return True
    return bool(_PLACEHOLDER_TOKEN.search(ref))


def check_import_readiness(
    import_path: Path | None = None,
) -> tuple[str, list[str]]:
    """Inspect the founder CRM import file and return (verdict, messages).

    Verdict is either 'READY' or WAITING_ON_FOUNDER_CRM_EXPORT.
    - Missing file => WAITING_ON_FOUNDER_CRM_EXPORT.
    - All entries placeholder (value=0/None or ref=<fill_from_crm>/TBD/not_synced_yet)
      => WAITING_ON_FOUNDER_CRM_EXPORT.
    """
    path = import_path or _IMPORT
    messages: list[str] = []
    if not path.exists():
        messages.append(f"missing import file: {path}")
        return _WAITING_VERDICT, messages

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    entries = data.get("entries") or {}
    if not entries:
        messages.append("import file has no entries")
        return _WAITING_VERDICT, messages

    real_count = 0
    for key, row in entries.items():
        if not isinstance(row, dict):
            continue
        val = row.get("value_numeric")
        ref = str(row.get("source_ref") or "")
        if _is_placeholder_value(val) and _is_placeholder_ref(ref):
            messages.append(f"placeholder: {key}")
        elif _is_placeholder_value(val) or _is_placeholder_ref(ref):
            messages.append(f"partial placeholder: {key}")
        else:
            real_count += 1

    if real_count == 0:
        return _WAITING_VERDICT, messages
    return "READY", messages


def _patch_snapshot_line(text: str, key: str, value: float, source_ref: str) -> str:
    lines = text.splitlines(keepends=True)
    in_key = False
    out: list[str] = []
    val_re = re.compile(r"^(\s*)value_numeric:\s*.*\n?$")
    ref_re = re.compile(r"^(\s*)source_ref:\s*.*\n?$")
    for line in lines:
        if re.match(rf"^\s*{re.escape(key)}:\s*$", line.rstrip("\n")):
            in_key = True
            out.append(line)
            continue
        if in_key:
            m_val = val_re.match(line.rstrip("\n"))
            if m_val:
                indent = m_val.group(1)
                nl = "\n" if line.endswith("\n") else ""
                out.append(f"{indent}value_numeric: {value}{nl}")
                continue
            m_ref = ref_re.match(line.rstrip("\n"))
            if m_ref:
                indent = m_ref.group(1)
                nl = "\n" if line.endswith("\n") else ""
                safe_ref = source_ref.replace('"', "'")
                out.append(f'{indent}source_ref: "{safe_ref}"{nl}')
                in_key = False
                continue
            if line.strip() and not line.startswith(" "):
                in_key = False
        out.append(line)
    return "".join(out)


def _validate_ref(key: str, source_ref: str) -> str | None:
    ref = source_ref.strip()
    if not ref:
        return f"{key}: empty source_ref"
    if _FORBIDDEN_REF.search(ref):
        return f"{key}: forbidden placeholder in source_ref"
    return None


def _merge_import_into_registry() -> int:
    if not _IMPORT.exists():
        return 0
    imp = yaml.safe_load(_IMPORT.read_text(encoding="utf-8")) or {}
    entries = imp.get("entries") or {}
    if not entries:
        return 0
    reg = yaml.safe_load(_REGISTRY.read_text(encoding="utf-8")) or {}
    commercial = reg.setdefault("commercial_entries", {})
    merged = 0
    for key, row in entries.items():
        if key not in commercial:
            continue
        val = row.get("value_numeric")
        ref = (row.get("source_ref") or "").strip()
        err = _validate_ref(key, ref) if ref else None
        if err:
            print(err, file=sys.stderr)
            return 1
        if val is not None and ref:
            commercial[key]["value_numeric"] = val
            commercial[key]["source_ref"] = ref
            merged += 1
    if imp.get("updated_period_iso"):
        reg["updated_period_iso"] = imp["updated_period_iso"]
    _REGISTRY.write_text(
        yaml.safe_dump(reg, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Merged {merged} entries from kpi_founder_commercial_import.yaml into registry")
    return 0


def _load_registry() -> dict:
    data = yaml.safe_load(_REGISTRY.read_text(encoding="utf-8"))
    return data.get("commercial_entries") or {}


def _ensure_import_file() -> None:
    if _IMPORT.exists():
        return
    bootstrap = _REPO_ROOT / "scripts" / "bootstrap_founder_kpi_import.py"
    if not bootstrap.is_file():
        return
    import subprocess

    subprocess.run([sys.executable, str(bootstrap)], check=False, cwd=_REPO_ROOT)


def _status() -> int:
    _ensure_import_file()
    entries = _load_registry()
    pending = []
    ready = []
    for key, row in entries.items():
        val = row.get("value_numeric")
        ref = (row.get("source_ref") or "").strip()
        if val is None or ref == "":
            pending.append(key)
        else:
            ready.append(key)
    print(f"commercial_registry_pending={len(pending)} ready={len(ready)}")
    if not _IMPORT.exists():
        print("hint: py -3 scripts/bootstrap_founder_kpi_import.py")
    else:
        print("kpi_import: present (fill CRM values; pending refs OK until export)")
    for key in pending:
        print(f"  pending: {key}")
    for key in ready:
        print(f"  ready: {key}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true", help="Print pending vs ready keys")
    parser.add_argument("--merge-import-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check readiness; exit non-zero with WAITING_ON_FOUNDER_CRM_EXPORT if not ready.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bypass the founder CRM readiness guard (use only when you know data is real).",
    )
    args = parser.parse_args()
    if args.status:
        return _status()

    verdict, messages = check_import_readiness()
    if args.check:
        for msg in messages:
            print(msg)
        print(f"DEALIX_KPI_IMPORT_VERDICT={verdict}")
        return 0 if verdict == "READY" else 2

    if verdict != "READY" and not args.force:
        for msg in messages:
            print(msg, file=sys.stderr)
        print(f"DEALIX_KPI_IMPORT_VERDICT={verdict}", file=sys.stderr)
        print(
            "Refusing to apply: founder has not supplied a real CRM export. "
            "Doctrine: never invent CRM numbers in automation. "
            "Re-run with --force to override after manual verification.",
            file=sys.stderr,
        )
        return 2

    if _merge_import_into_registry() != 0:
        return 1
    if args.merge_import_only:
        return 0

    entries = _load_registry()
    text = _BASELINES.read_text(encoding="utf-8")
    applied: list[str] = []
    for key, row in entries.items():
        val = row.get("value_numeric")
        ref = (row.get("source_ref") or "").strip()
        if val is None or ref == "":
            continue
        err = _validate_ref(key, ref)
        if err:
            print(err, file=sys.stderr)
            return 1
        text = _patch_snapshot_line(text, key, float(val), ref)
        applied.append(key)

    if not applied:
        print("No commercial entries to apply (fill import or registry first).")
        return 0

    if args.dry_run:
        print(f"Would apply: {', '.join(applied)}")
        return 0

    _BASELINES.write_text(text, encoding="utf-8")
    print(f"Applied commercial KPIs: {', '.join(applied)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
