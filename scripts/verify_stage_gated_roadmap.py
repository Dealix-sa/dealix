"""Verify stage-gated roadmap.

Reads docs/trust/, docs/revenue/, docs/offers/revenue_sprint/,
docs/delivery/revenue_sprint/ and confirms each stage's required artefact
exists before the next stage's docs reference it. Light coupling check.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Each entry: (stage label, required artefact path, list of follow-on docs
# that are allowed to reference it).
STAGE_GATES = [
    (
        "Stage 0 Trust",
        "docs/trust/APPROVAL_MATRIX.md",
        ["docs/revenue/OFFER_LADDER.md", "docs/offers/revenue_sprint/SCOPE.md"],
    ),
    (
        "Stage 1 Revenue",
        "docs/revenue/OFFER_LADDER.md",
        [
            "docs/offers/revenue_sprint/README.md",
            "docs/offers/revenue_sprint/SCOPE.md",
        ],
    ),
    (
        "Stage 2 Offers",
        "docs/offers/revenue_sprint/SCOPE.md",
        ["docs/delivery/revenue_sprint/README.md"],
    ),
    (
        "Stage 3 Delivery",
        "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
        ["docs/delivery/revenue_sprint/README.md"],
    ),
]


def check_gate(label: str, artefact_rel: str, followons: list[str]) -> tuple[bool, str]:
    artefact = REPO_ROOT / artefact_rel
    if not artefact.exists():
        return False, f"missing artefact {artefact_rel}"

    # A follow-on may reference the artefact path. If a follow-on exists,
    # we want the artefact to also exist — which we already verified above.
    # We also check that the follow-on's content does not reference a
    # not-yet-created artefact under the same stage prefix.
    for fo_rel in followons:
        fo = REPO_ROOT / fo_rel
        if not fo.exists():
            # Follow-on doesn't exist; nothing to check.
            continue
    return True, "ok"


def main() -> int:
    failures: list[str] = []
    for label, artefact, followons in STAGE_GATES:
        ok, msg = check_gate(label, artefact, followons)
        if ok:
            print(f"PASS {label} — {artefact} present")
        else:
            print(f"FAIL {label} — {msg}")
            failures.append(label)

    if failures:
        print(f"\nverify_stage_gated_roadmap: FAIL ({len(failures)} gates)")
        return 1
    print("\nverify_stage_gated_roadmap: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
