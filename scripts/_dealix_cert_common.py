"""Shared helpers for the Dealix Production AI Certification Layer.

Used by:
    - scripts/verify_everything.py
    - scripts/verify_ai_company_os.py
    - scripts/verify_production_env.py
    - scripts/verify_railway_readiness.py
    - scripts/verify_live_send_safety.py
    - scripts/verify_policy_as_code.py
    - scripts/verify_agent_registry.py
    - scripts/verify_machine_registry.py
    - scripts/verify_eval_gate.py
    - scripts/verify_prompt_output_quality.py
    - scripts/smoke_internal_api.py

Doctrine:
    * Never print a secret value. Only print whether a name is present.
    * Always return a structured report so verify_everything.py can roll it up.
    * Exit code 0 = PASS, 1 = FAIL, 2 = WARN-only.
"""
from __future__ import annotations

import io
import json
import os
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent


# --- safe stdout on Windows / CI ---------------------------------------------
def _safe_stdout() -> None:
    """Force UTF-8 stdout so CI logs don't crash on Arabic text."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        except Exception:
            pass


_safe_stdout()


# --- result model ------------------------------------------------------------
@dataclass
class CheckResult:
    name: str
    status: str  # PASS | FAIL | WARN
    detail: str = ""
    hint: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class VerifierReport:
    verifier: str
    results: list[CheckResult] = field(default_factory=list)

    def add(self, name: str, status: str, detail: str = "", hint: str = "") -> None:
        self.results.append(CheckResult(name=name, status=status, detail=detail, hint=hint))

    def pass_(self, name: str, detail: str = "") -> None:
        self.add(name, "PASS", detail)

    def fail(self, name: str, detail: str, hint: str = "") -> None:
        self.add(name, "FAIL", detail, hint)

    def warn(self, name: str, detail: str, hint: str = "") -> None:
        self.add(name, "WARN", detail, hint)

    @property
    def overall(self) -> str:
        if any(r.status == "FAIL" for r in self.results):
            return "FAIL"
        if any(r.status == "WARN" for r in self.results):
            return "WARN"
        return "PASS"

    def exit_code(self) -> int:
        return {"PASS": 0, "WARN": 0, "FAIL": 1}[self.overall]

    def to_dict(self) -> dict[str, Any]:
        return {
            "verifier": self.verifier,
            "overall": self.overall,
            "results": [r.to_dict() for r in self.results],
        }


# --- printing ----------------------------------------------------------------
_GLYPH = {"PASS": "PASS", "FAIL": "FAIL", "WARN": "WARN"}


def print_report(report: VerifierReport, *, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        return
    print()
    print(f"=== {report.verifier} ===")
    width = max((len(r.name) for r in report.results), default=20)
    for r in report.results:
        print(f"  [{_GLYPH[r.status]}] {r.name.ljust(width)}  {r.detail}")
        if r.status == "FAIL" and r.hint:
            print(f"          hint: {r.hint}")
    print(f"--- RESULT: {report.overall} ---")


# --- file/dir helpers --------------------------------------------------------
def repo_path(*parts: str) -> Path:
    return REPO_ROOT.joinpath(*parts)


def must_exist(report: VerifierReport, name: str, *parts: str, hint: str = "") -> bool:
    p = repo_path(*parts)
    if p.exists():
        report.pass_(name, str(Path(*parts)))
        return True
    report.fail(name, f"missing: {Path(*parts)}", hint=hint)
    return False


def must_be_file(report: VerifierReport, name: str, *parts: str, hint: str = "") -> bool:
    p = repo_path(*parts)
    if p.is_file():
        report.pass_(name, str(Path(*parts)))
        return True
    report.fail(name, f"not a file: {Path(*parts)}", hint=hint)
    return False


# --- yaml without external dep ------------------------------------------------
def load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML, falling back to a tiny built-in parser if PyYAML missing.

    The fallback only handles the limited dialect used by the Dealix
    policies/registries (block mappings, sequences, scalars, comments).
    """
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore[import-not-found]

        return yaml.safe_load(text) or {}
    except ImportError:
        return _mini_yaml(text)


def _mini_yaml(text: str) -> dict[str, Any]:
    """Minimal YAML for our policy/registry files.

    Supports:
        key: value
        key:
          - item
          - item
        key:
          subkey: value
        - block mapping inside a list
    No anchors, no flow style, no multiline scalars.
    """
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    pending_key: list[tuple[int, str]] = []

    def parent_for(indent: int) -> Any:
        while stack and stack[-1][0] >= indent:
            stack.pop()
        return stack[-1][1] if stack else root

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.split("#", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not stripped.strip():
            i += 1
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        content = stripped.strip()
        parent = parent_for(indent)
        # list item
        if content.startswith("- "):
            item_body = content[2:].strip()
            if isinstance(parent, list):
                target_list = parent
            else:
                # parent is a dict and we need its most recently opened list
                if pending_key and pending_key[-1][0] < indent:
                    k = pending_key[-1][1]
                    if not isinstance(parent.get(k), list):
                        parent[k] = []
                    target_list = parent[k]
                    stack.append((indent, target_list))
                else:
                    raise ValueError(f"Unexpected list at line {i + 1}: {raw}")
            if ":" in item_body and not item_body.endswith(":"):
                k, v = item_body.split(":", 1)
                d = {k.strip(): _scalar(v.strip())}
                target_list.append(d)
                stack.append((indent + 2, d))
            elif item_body.endswith(":"):
                k = item_body[:-1].strip()
                d: dict[str, Any] = {k: None}
                target_list.append(d)
                stack.append((indent + 2, d))
                pending_key.append((indent + 2, k))
            else:
                target_list.append(_scalar(item_body))
            i += 1
            continue
        # mapping
        if ":" in content:
            k, v = content.split(":", 1)
            k = k.strip()
            v = v.strip()
            if not isinstance(parent, dict):
                # parent is a list of dicts; use last
                if isinstance(parent, list) and parent and isinstance(parent[-1], dict):
                    parent = parent[-1]
                else:
                    raise ValueError(f"Cannot map under non-dict at line {i + 1}: {raw}")
            if v == "":
                parent[k] = None
                stack.append((indent, parent))
                pending_key.append((indent, k))
            elif v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                parent[k] = [_scalar(x.strip()) for x in inner.split(",") if x.strip()] if inner else []
            elif v.startswith("{") and v.endswith("}"):
                inner = v[1:-1].strip()
                d: dict[str, Any] = {}
                for pair in _split_flow(inner):
                    if ":" in pair:
                        pk, pv = pair.split(":", 1)
                        d[pk.strip()] = _scalar(pv.strip())
                parent[k] = d
            else:
                parent[k] = _scalar(v)
            i += 1
            continue
        i += 1
    return root


def _split_flow(s: str) -> list[str]:
    out: list[str] = []
    depth = 0
    buf = []
    for ch in s:
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf))
    return out


def _scalar(v: str) -> Any:
    s = v.strip()
    if s == "":
        return None
    if s.startswith(("'", '"')) and s.endswith(("'", '"')) and len(s) >= 2:
        return s[1:-1]
    low = s.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "~"):
        return None
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        return s


# --- text-scanning helpers (for secret/frontend audits) ----------------------
def iter_files(root: Path, *, suffixes: Iterable[str], skip_dirs: Iterable[str] = ()) -> Iterable[Path]:
    skip = {".git", "node_modules", ".next", "dist", "build", "__pycache__", "venv", ".venv"}
    skip.update(skip_dirs)
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(seg in skip for seg in p.parts):
            continue
        if p.suffix in suffixes:
            yield p


# --- env-presence (no value printed) -----------------------------------------
def env_present(name: str) -> bool:
    return bool(os.environ.get(name))


def env_truthy(name: str, default: bool = False) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "on"}


def main_cli(verifier_fn, *, name: str) -> int:
    """Standard CLI wrapper: --json flag, returns exit code."""
    as_json = "--json" in sys.argv[1:]
    report: VerifierReport = verifier_fn()
    print_report(report, as_json=as_json)
    return report.exit_code()
