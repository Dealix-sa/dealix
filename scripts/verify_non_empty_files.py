#!/usr/bin/env python3
"""verify_non_empty_files.py — fail when manifest-listed files are empty or stub.

Reads `dealix_manifest.yaml`, then for each `required_files` entry confirms the
file's stripped content meets the appropriate minimum size. This is the single
guard against accidental commits of placeholder files like:

    # TODO: write this later

Run:
    python scripts/verify_non_empty_files.py
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML missing — run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "dealix_manifest.yaml"

STUB_MARKERS = (
    "todo: write this later",
    "todo write this later",
    "fill me in",
    "fill me later",
    "lorem ipsum",
    "xxx_replace_me",
    "اكتبه لاحقا",
    "املأه لاحقا",
    "ابنه لاحقا",
)


def size_threshold(path: str, rules: dict) -> int:
    if path.endswith(".py"):
        return int(rules.get("min_script_size_bytes", 500))
    if path.endswith((".yaml", ".yml", ".toml", ".json")):
        return int(rules.get("min_yaml_size_bytes", 200))
    if path.endswith(".sh"):
        return int(rules.get("min_script_size_bytes", 500)) // 2
    return int(rules.get("min_doc_size_bytes", 600))


def main() -> int:
    if not MANIFEST.exists():
        print("missing_manifest:dealix_manifest.yaml", file=sys.stderr)
        return 2

    try:
        data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"bad_manifest_yaml:{exc}", file=sys.stderr)
        return 2

    rules = data.get("global_rules", {})
    failures: list[str] = []

    for layer_name, layer in (data.get("layers") or {}).items():
        for path in layer.get("required_files", []):
            p = REPO / path
            if not p.exists():
                failures.append(f"missing:{layer_name}:{path}")
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            stripped = text.strip()
            min_size = size_threshold(path, rules)
            if len(stripped) < min_size:
                failures.append(
                    f"too_small:{layer_name}:{path} ({len(stripped)} < {min_size})"
                )
            low = stripped.lower()
            for marker in STUB_MARKERS:
                if marker in low:
                    failures.append(f"stub_marker:{layer_name}:{path}:'{marker}'")
                    break

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(f"NON_EMPTY_FILES_PASS={'true' if ok else 'false'} (failures={len(failures)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
