#!/usr/bin/env python3
"""verify_business_os.py — every business OS doc must be useful, not a stub.

Enforced ONLY on the new English-structured docs under `docs/founder/`.
Pre-existing Arabic operating docs (under `docs/ops/`, `docs/commercial/`)
have their own structure and are size-checked by `verify_non_empty_files.py`
instead — forcing them into the English section grid would erode their
intent without improving safety.

Each `docs/founder/**.md` file named in `dealix_manifest.yaml` MUST
contain a minimum set of structural sections — owner, cadence, KPI,
source of truth, failure mode, recovery path.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML missing", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[1]

BUSINESS_LAYERS = (
    "founder_console",
    "ceo_operating_system",
    "capital_allocation",
    "revenue_factory",
    "market_attack",
    "customer_success_os",
    "launch_readiness",
)

REQUIRED_SECTIONS = (
    "owner",
    "cadence",
    "KPI",
    "source of truth",
    "failure mode",
    "recovery path",
)


def main() -> int:
    manifest = REPO / "dealix_manifest.yaml"
    if not manifest.exists():
        print("missing_manifest", file=sys.stderr)
        return 2
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    layers = data.get("layers") or {}

    failures: list[str] = []
    for layer_name in BUSINESS_LAYERS:
        layer = layers.get(layer_name)
        if not layer:
            failures.append(f"missing_layer:{layer_name}")
            continue
        for path in layer.get("required_files", []):
            # Strict section enforcement is scoped to the docs/founder/ tree:
            # those are the English-structured documents we author against
            # this verifier. Other paths are checked only for existence.
            p = REPO / path
            if not p.exists():
                failures.append(f"missing_doc:{layer_name}:{path}")
                continue
            if not path.endswith(".md"):
                continue
            if not path.startswith("docs/founder/"):
                continue
            text = p.read_text(encoding="utf-8", errors="ignore").lower()
            for section in REQUIRED_SECTIONS:
                if section.lower() not in text:
                    failures.append(
                        f"missing_section:{layer_name}:{path}:'{section}'"
                    )

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(f"BUSINESS_OS_PASS={'true' if ok else 'false'} (failures={len(failures)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
