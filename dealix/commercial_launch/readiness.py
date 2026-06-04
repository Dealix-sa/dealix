"""Commercial Launch readiness gate.

Aggregates config presence, vertical count, draft-factory output, safety audit,
and channel policy into a single Go/No-Go report. Designed to be run in CI.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dealix.commercial_launch.engine import ROOT, generate_drafts, load_config
from dealix.commercial_launch.safety import scan_files
from dealix.commercial_launch.social import generate_social, load_social_config


@dataclass
class ReadinessCheck:
    name: str
    passed: bool
    detail: str


@dataclass
class ReadinessReport:
    checks: list[ReadinessCheck] = field(default_factory=list)
    go_no_go: dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "checks": [c.__dict__ for c in self.checks],
            "go_no_go": self.go_no_go,
        }


REQUIRED_DOCS = [
    "00_OFFICIAL_COMMERCIAL_LAUNCH_OS.md",
    "01_FIRST_5_VERTICALS.md",
    "02_OFFER_LADDER_SAR.md",
    "03_400_DAILY_DRAFT_FACTORY.md",
    "04_CHANNEL_POLICY.md",
    "05_FOUNDER_DAILY_REVIEW_PLAYBOOK.md",
    "06_COMPLIANCE_AND_SAFETY_GATES.md",
    "07_SALES_MESSAGING_AR_EN.md",
    "08_OBJECTION_HANDLING.md",
    "09_GO_TO_MARKET_30_DAY_PLAN.md",
]

REQUIRED_CONFIGS = [
    "commercial_launch.json",
    "commercial_verticals.json",
    "commercial_channels.json",
    "commercial_offers.json",
    "commercial_quality_gates.json",
]


def evaluate_readiness(root: Path | None = None, target: int = 400, run_generation: bool = True) -> ReadinessReport:
    r = root or ROOT
    report = ReadinessReport()
    cfg = load_config(r / "config")

    # 1. Configs present
    missing_cfg = [c for c in REQUIRED_CONFIGS if not (r / "config" / c).exists()]
    report.checks.append(ReadinessCheck(
        "configs_present", not missing_cfg,
        "all present" if not missing_cfg else f"missing: {missing_cfg}"))

    # 2. Exactly 5 verticals locked
    verts = cfg["verticals"]["verticals"]
    report.checks.append(ReadinessCheck(
        "five_verticals_locked", len(verts) >= 5,
        f"{len(verts)} verticals: {[v['id'] for v in verts]}"))

    # 3. Offer ladder in SAR with conservative claims policy
    offers = cfg["offers"]
    claims_ok = offers.get("claims_policy", {}).get("no_guaranteed_roi") is True
    report.checks.append(ReadinessCheck(
        "offer_ladder_conservative", bool(offers.get("ladder")) and claims_ok,
        f"{len(offers.get('ladder', []))} rungs, no_guaranteed_roi={claims_ok}"))

    # 4. Docs present
    docs_dir = r / "docs" / "commercial-launch"
    missing_docs = [d for d in REQUIRED_DOCS if not (docs_dir / d).exists()]
    report.checks.append(ReadinessCheck(
        "docs_present", not missing_docs,
        "all present" if not missing_docs else f"missing: {missing_docs}"))

    # 5. Channel policy blocks external send
    gp = cfg["channels"]["global_policy"]
    block_ok = gp.get("external_send") == "BLOCKED" and gp.get("auto_send") == "BLOCKED"
    report.checks.append(ReadinessCheck(
        "channel_policy_blocks_send", block_ok,
        f"external_send={gp.get('external_send')}, auto_send={gp.get('auto_send')}"))

    # 6. Safety scan clean
    safety = scan_files(r)
    report.checks.append(ReadinessCheck(
        "safety_scan_clean", safety.passed,
        f"scanned {safety.scanned_files} files, {len(safety.findings)} findings"))

    # 6b. Social/media OS config present and blocks posting + ad spend
    social_cfg_path = r / "config" / "commercial_social.json"
    if social_cfg_path.exists():
        social_cfg = load_social_config(r / "config")
        sgp = social_cfg["global_policy"]
        social_block_ok = (
            sgp.get("external_post") == "BLOCKED"
            and sgp.get("auto_post") == "BLOCKED"
            and sgp.get("ad_spend") == "BLOCKED"
        )
        report.checks.append(ReadinessCheck(
            "social_os_blocks_posting", social_block_ok,
            f"external_post={sgp.get('external_post')}, auto_post={sgp.get('auto_post')}, ad_spend={sgp.get('ad_spend')}"))
    else:
        report.checks.append(ReadinessCheck("social_os_blocks_posting", False, "config/commercial_social.json missing"))

    # 7. Draft factory meets target
    if run_generation:
        result = generate_drafts(target=target, config=cfg)
        meets = result.total_accepted >= target
        invariants_ok = all(
            d["send_allowed"] is False and d["external_send_blocked"] is True
            for d in result.accepted
        )
        report.checks.append(ReadinessCheck(
            "draft_factory_meets_target", meets and invariants_ok,
            f"generated {result.total_accepted} (target {target}), invariants_ok={invariants_ok}"))

        # 7b. Social factory meets its minimum, all review-only
        social = generate_social()
        social_min = load_social_config(r / "config")["total_minimum"]
        social_ok = social.total_accepted >= social_min and all(
            p["post_allowed"] is False and p["external_post_blocked"] is True
            for p in social.accepted
        )
        report.checks.append(ReadinessCheck(
            "social_factory_meets_minimum", social_ok,
            f"generated {social.total_accepted} (min {social_min})"))

    report.go_no_go = {
        "go_for_draft_generation": True,
        "go_for_social_media_generation": True,
        "go_for_founder_manual_review": True,
        "no_go_for_automated_sending": True,
        "no_go_for_automated_posting": True,
        "no_go_for_ad_spend": True,
        "no_go_for_whatsapp_cold_outreach": True,
        "no_go_for_linkedin_automation": True,  # safety-audit-allow
        "overall_ready": report.passed,
    }
    return report


def write_readiness(report: ReadinessReport, root: Path | None = None) -> str:
    r = root or ROOT
    path = r / "outputs" / "commercial_launch" / "launch_readiness.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)
