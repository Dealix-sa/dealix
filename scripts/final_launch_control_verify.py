#!/usr/bin/env python3
"""
Dealix Final Launch Control — Master Verification.

Proves the commercial launch surface is real, complete, and safe. Checks files,
scripts, outputs, safety invariants, reports, workflows, README, workflow
permissions/secrets, forbidden-term hygiene, and site pages.

Writes:
  - outputs/final_launch_control/final_verification.json
  - outputs/final_launch_control/final_verification.md

Exit 0 only if every CRITICAL check passes; 1 otherwise.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "outputs" / "final_launch_control"
CL = REPO / "outputs" / "commercial_launch" / "latest"

# Files that must exist (reports + workflows).
REQUIRED_FILES = [
    "docs/commercial-launch/99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md",
    "docs/media-social-os/99_MEDIA_SOCIAL_READY_REPORT.md",
    "docs/site-launch/99_SITE_LAUNCH_REPORT.md",
    "docs/launch-control/99_FINAL_CONTROL_TOWER_REPORT.md",
    "README.md",
    ".github/workflows/commercial-draft-factory.yml",
    ".github/workflows/media-social-calendar.yml",
    ".github/workflows/site-commercial-verify.yml",
    ".github/workflows/final-launch-control.yml",
]

REQUIRED_SCRIPTS = [
    "scripts/commercial_generate_400_drafts.py",
    "scripts/commercial_safety_audit.py",
    "scripts/commercial_launch_readiness.py",
    "scripts/media_social_calendar_generate.py",
    "scripts/final_launch_control_verify.py",
]

REQUIRED_OUTPUTS = [
    CL / "draft_queue.jsonl",
    CL / "founder_review.md",
    CL / "top_50_priority.md",
    CL / "safety_audit.json",
    CL / "daily_metrics.json",
]

NEW_WORKFLOWS = [
    ".github/workflows/commercial-draft-factory.yml",
    ".github/workflows/media-social-calendar.yml",
    ".github/workflows/site-commercial-verify.yml",
    ".github/workflows/final-launch-control.yml",
]

# Content-generation scripts that must be free of external-send automation terms.
CONTENT_SCRIPTS = [
    "scripts/commercial_generate_400_drafts.py",
    "scripts/commercial_safety_audit.py",
    "scripts/commercial_launch_readiness.py",
    "scripts/media_social_calendar_generate.py",
]
FORBIDDEN_TERMS = ["smtp", "whatsapp", "linkedin"]


class Checks:
    def __init__(self) -> None:
        self.results: list[dict] = []

    def add(self, name: str, ok: bool, critical: bool, detail: str = "") -> None:
        self.results.append(
            {"name": name, "pass": bool(ok), "critical": critical, "detail": detail}
        )

    def critical_failed(self) -> list[dict]:
        return [r for r in self.results if r["critical"] and not r["pass"]]


def load_jsonl(path: Path) -> list[dict]:
    out = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def main() -> int:
    c = Checks()

    # 1) Required files
    for rel in REQUIRED_FILES:
        c.add(f"file:{rel}", (REPO / rel).exists(), critical=True)

    # 2) Required scripts
    for rel in REQUIRED_SCRIPTS:
        c.add(f"script:{rel}", (REPO / rel).exists(), critical=True)

    # 3) Required outputs
    for p in REQUIRED_OUTPUTS:
        c.add(f"output:{p.relative_to(REPO)}", p.exists(), critical=True)

    # 4) Draft safety invariants
    drafts = load_jsonl(CL / "draft_queue.jsonl")
    n = len(drafts)
    send_allowed_true = sum(1 for d in drafts if d.get("send_allowed") is True)
    ext_blocked_false = sum(1 for d in drafts if d.get("external_send_blocked") is not True)
    no_auto_false = sum(1 for d in drafts if d.get("no_auto_send") is not True)
    c.add("draft_count>=400", n >= 400, critical=True, detail=f"count={n}")
    c.add("send_allowed_true_count==0", send_allowed_true == 0, critical=True,
          detail=f"count={send_allowed_true}")
    c.add("external_send_blocked_false_count==0", ext_blocked_false == 0, critical=True,
          detail=f"count={ext_blocked_false}")
    c.add("no_auto_send_false_count==0", no_auto_false == 0, critical=True,
          detail=f"count={no_auto_false}")

    # 5) Safety audit pass
    safety = json.loads((CL / "safety_audit.json").read_text(encoding="utf-8")) \
        if (CL / "safety_audit.json").exists() else {}
    c.add("safety_audit.pass==true", safety.get("pass") is True, critical=True)

    # 6) README content + clone URL
    readme = (REPO / "README.md").read_text(encoding="utf-8") if (REPO / "README.md").exists() else ""
    c.add("README contains 'Commercial Launch OS'", "Commercial Launch OS" in readme, critical=True)
    c.add("README clone URL -> Dealix-sa/dealix.git",
          "Dealix-sa/dealix.git" in readme, critical=True)

    # 7) Workflow permissions minimal + no secrets-for-send
    for rel in NEW_WORKFLOWS:
        p = REPO / rel
        txt = p.read_text(encoding="utf-8") if p.exists() else ""
        low = txt.lower()
        no_write_all = "write-all" not in low and "permissions: write-all" not in low
        has_contents_read = "contents: read" in low
        no_secrets = "secrets." not in low
        c.add(f"workflow:{rel} no write-all", no_write_all, critical=True)
        c.add(f"workflow:{rel} contents:read", has_contents_read, critical=True)
        c.add(f"workflow:{rel} no secrets (artifact-only)", no_secrets, critical=True)

    # 8) Forbidden automation terms absent from content scripts
    for rel in CONTENT_SCRIPTS:
        p = REPO / rel
        low = p.read_text(encoding="utf-8").lower() if p.exists() else ""
        hits = [t for t in FORBIDDEN_TERMS if t in low]
        c.add(f"no forbidden terms in {rel}", not hits, critical=True, detail=str(hits))

    # 9) Site pages if apps/web present
    web = REPO / "apps" / "web" / "app"
    if web.exists():
        c.add("site:homepage page.tsx", (web / "page.tsx").exists(), critical=False)
        c.add("site:layout.tsx", (web / "layout.tsx").exists(), critical=False)
    else:
        c.add("site:apps/web present", False, critical=False, detail="apps/web absent — skipped")

    # ---- Verdict ----
    critical_fail = c.critical_failed()
    overall = len(critical_fail) == 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "overall_pass": overall,
        "draft_count": n,
        "critical_failures": [r["name"] for r in critical_fail],
        "checks": c.results,
    }
    (OUT_DIR / "final_verification.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = [
        "# Final Launch Control — Verification",
        "",
        f"_Verified: {payload['verified_at']}_",
        "",
        f"## Overall: **{'PASS ✅' if overall else 'FAIL ❌'}**",
        f"- Draft count: **{n}**",
        f"- Critical failures: **{len(critical_fail)}**",
        "",
        "| Check | Critical | Result | Detail |",
        "|-------|----------|--------|--------|",
    ]
    for r in c.results:
        md.append(
            f"| {r['name']} | {'yes' if r['critical'] else 'no'} | "
            f"{'PASS' if r['pass'] else 'FAIL'} | {r['detail']} |"
        )
    (OUT_DIR / "final_verification.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"[final-verify] OVERALL {'PASS' if overall else 'FAIL'} — drafts={n}, "
          f"critical_failures={len(critical_fail)}")
    for r in critical_fail:
        print(f"  - CRITICAL FAIL: {r['name']} {r['detail']}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
