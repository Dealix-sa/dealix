#!/usr/bin/env python3
"""Commercial launch readiness verifier.

Checks that the Commercial Launch OS artifacts exist and are internally
consistent, and that the safety contract holds. Exit 0 = ready, 1 = not ready.
"""

from __future__ import annotations

import json

import commercial_launch_lib as lib

REPO_ROOT = lib.REPO_ROOT

REQUIRED_CONFIGS = [
    "commercial_launch.json",
    "commercial_verticals.json",
    "commercial_offers.json",
    "commercial_channels.json",
    "commercial_quality_gates.json",
    "commercial_compliance_gates.json",
    "commercial_draft_distribution.json",
    "commercial_risk_terms.json",
    "commercial_founder_review_rules.json",
    "commercial_metrics.json",
]

REQUIRED_DOCS = [
    "docs/commercial-launch/00_README.md",
    "docs/commercial-launch/02_OFFER_LADDER_SAR.md",
    "docs/commercial-launch/verticals/01_facilities_management.md",
    "docs/commercial-launch/verticals/05_consulting_training_b2b.md",
    "docs/media-social-os/00_MEDIA_SOCIAL_OS.md",
]


def check() -> dict:
    checks: list[dict] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    # configs present + parseable
    for cfg in REQUIRED_CONFIGS:
        p = REPO_ROOT / "config" / cfg
        ok = p.exists()
        if ok:
            try:
                json.loads(p.read_text(encoding="utf-8"))
            except Exception as exc:
                ok = False
                add(f"config:{cfg}", False, f"invalid json: {exc}")
                continue
        add(f"config:{cfg}", ok, "" if ok else "missing")

    # docs present
    for doc in REQUIRED_DOCS:
        add(f"doc:{doc}", (REPO_ROOT / doc).exists(), "")

    # verticals == 5
    verticals = lib.load_config("commercial_verticals.json")["verticals"]
    add("verticals_count==5", len(verticals) == 5, f"found {len(verticals)}")

    # distribution sums to >= 400
    dist = lib.load_config("commercial_draft_distribution.json")["distribution"]
    add("distribution>=400", sum(dist.values()) >= 400, f"sum={sum(dist.values())}")

    # safety contract in launch config
    safety = lib.load_config("commercial_launch.json")["safety"]
    add(
        "safety_contract",
        safety
        == {
            "send_allowed": False,
            "external_send_blocked": True,
            "requires_founder_approval": True,
            "no_auto_send": True,
        },
        json.dumps(safety),
    )

    # generation smoke: 400 drafts, all safe
    drafts = lib.generate_drafts(target=400)
    add("generates>=400", len(drafts) >= 400, f"{len(drafts)} drafts")
    try:
        lib.assert_safety(drafts)
        add("all_drafts_safe", True)
    except AssertionError as exc:
        add("all_drafts_safe", False, str(exc))

    passed = all(c["ok"] for c in checks)
    return {"verdict": "READY" if passed else "NOT_READY", "checks": checks}


def main(argv: list[str] | None = None) -> int:
    result = check()
    out_path = REPO_ROOT / "outputs" / "commercial_launch" / "readiness.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    for c in result["checks"]:
        mark = "✅" if c["ok"] else "❌"
        print(f"{mark} {c['check']} {('- ' + c['detail']) if c['detail'] and not c['ok'] else ''}")
    print(f"\nVerdict: {result['verdict']}")
    return 0 if result["verdict"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
