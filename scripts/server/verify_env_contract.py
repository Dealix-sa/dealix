#!/usr/bin/env python3
"""
Verify production env contract against .env.example and .env.railway.example.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    if not path.exists():
        return keys
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*[=:]", line)
        if m:
            keys.add(m.group(1))
    return keys


def main() -> int:
    example_keys = parse_keys(REPO_ROOT / ".env.example")
    railway_keys = parse_keys(REPO_ROOT / ".env.railway.example")
    required = example_keys | railway_keys

    missing: list[str] = []
    present: list[str] = []
    for key in sorted(required):
        value = __import__("os").getenv(key, "").strip()
        if value:
            present.append(key)
        else:
            missing.append(key)

    print("Dealix Env Contract Verification")
    print("=" * 60)
    for key in present:
        print(f"  ✅ {key}")
    for key in missing:
        print(f"  ❌ MISSING {key}")

    out_dir = REPO_ROOT / "reports" / "server"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "env_contract.md", "w", encoding="utf-8") as f:
        f.write("# Env Contract Verification\n\n")
        for key in present:
            f.write(f"- [x] {key}\n")
        for key in missing:
            f.write(f"- [ ] {key}\n")

    if missing:
        print(f"\nDEALIX_ENV_CONTRACT=0 ({len(missing)} missing)")
        return 1
    print("\nDEALIX_ENV_CONTRACT=1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
