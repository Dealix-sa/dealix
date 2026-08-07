#!/usr/bin/env python3
"""
Dealix Commercial Safety Audit.

Audits the generated draft queue and asserts the non-negotiable safety
invariants before any human review happens:

  - every draft has send_allowed = False
  - every draft has external_send_blocked = True
  - every draft has no_auto_send = True
  - no draft body contains forbidden / exaggerated claims
  - draft count >= 400

Writes outputs/commercial_launch/latest/safety_audit.json with {"pass": bool, ...}.
Exit 0 if pass, 1 otherwise.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "outputs" / "commercial_launch" / "latest"
QUEUE = OUT_DIR / "draft_queue.jsonl"

FORBIDDEN_CLAIMS = [
    "guaranteed roi",
    "100%",
    "replace your team",
    "automate everything",
    "no human needed",
    "ضمان عائد",
    "بدون بشر",
]


def load_drafts() -> list[dict]:
    if not QUEUE.exists():
        return []
    drafts = []
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            drafts.append(json.loads(line))
    return drafts


def audit(drafts: list[dict]) -> dict:
    n = len(drafts)
    send_allowed_true = sum(1 for d in drafts if d.get("send_allowed") is True)
    external_blocked_false = sum(
        1 for d in drafts if d.get("external_send_blocked") is not True
    )
    no_auto_send_false = sum(1 for d in drafts if d.get("no_auto_send") is not True)

    claim_violations = []
    for d in drafts:
        text = " ".join(
            str(d.get(k, "")) for k in ("subject_en", "subject_ar", "body_en", "body_ar")
        ).lower()
        for claim in FORBIDDEN_CLAIMS:
            if claim in text:
                claim_violations.append({"id": d.get("id"), "claim": claim})

    checks = {
        "draft_count_ok": n >= 400,
        "send_allowed_true_count": send_allowed_true,
        "external_send_blocked_false_count": external_blocked_false,
        "no_auto_send_false_count": no_auto_send_false,
        "no_forbidden_claims": len(claim_violations) == 0,
    }
    passed = (
        checks["draft_count_ok"]
        and send_allowed_true == 0
        and external_blocked_false == 0
        and no_auto_send_false == 0
        and checks["no_forbidden_claims"]
    )

    return {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "draft_count": n,
        "pass": passed,
        "checks": checks,
        "claim_violations": claim_violations[:20],
    }


def main() -> int:
    drafts = load_drafts()
    result = audit(drafts)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "safety_audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    status = "PASS" if result["pass"] else "FAIL"
    print(f"[safety-audit] {status} — {result['draft_count']} drafts audited")
    for k, v in result["checks"].items():
        print(f"  - {k}: {v}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
