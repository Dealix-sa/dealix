"""Doctrine guardrails for scripts/build_company_live.py (Dealix-Live snapshot).

Every assertion here is one of the 11 non-negotiables made executable:
  * drafts/calls/proposals/diagnostic are ALWAYS approval-gated (never live-send),
  * no fabricated real leads (placeholder rows never counted as real),
  * do-not-contact rows never enter drafts or calls,
  * pricing is always gated (G03),
  * scoring is transparent (breakdown sums to score).
"""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "build_company_live", REPO_ROOT / "scripts" / "build_company_live.py"
)
bcl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bcl)  # type: ignore[union-attr]


_FIELDS = [
    "company",
    "contact",
    "segment",
    "pain_hypothesis",
    "channel",
    "motion",
    "offer_id",
    "status",
    "next_action",
    "next_action_date",
    "priority",
    "notes",
]


@pytest.fixture()
def mixed_csv(tmp_path: Path) -> Path:
    rows = [
        # A real lead (no placeholder markers) — high-priority warm.
        {
            "company": "شركة الأفق للخدمات",
            "contact": "أبو محمد",
            "segment": "direct_b2b",
            "pain_hypothesis": "متابعة غير موثقة للعروض",
            "channel": "email_warm",
            "motion": "B",
            "offer_id": "ai_workflow_audit",
            "status": "not_contacted",
            "next_action": "Discovery 30 دقيقة",
            "next_action_date": "",
            "priority": "high",
            "notes": "warm من شبكة المؤسس",
        },
        # A seed placeholder — must never be counted as real.
        {
            "company": "REPLACE:وكالة من شبكتك 1",
            "contact": "REPLACE:اسم المدير",
            "segment": "agency_wedge",
            "pain_hypothesis": "لا proof أسبوعي",
            "channel": "linkedin_manual",
            "motion": "A",
            "offer_id": "revenue_ai_os",
            "status": "not_contacted",
            "next_action": "مسودة",
            "next_action_date": "",
            "priority": "high",
            "notes": "warm",
        },
        # Do-not-contact — closed_lost + "لا ترسل" — must be excluded everywhere external.
        {
            "company": "وكالة مثال — لا ترسل",
            "contact": "مدير",
            "segment": "agency_wedge",
            "pain_hypothesis": "تدريب داخلي",
            "channel": "linkedin_manual",
            "motion": "A",
            "offer_id": "revenue_ai_os",
            "status": "closed_lost",
            "next_action": "مثال",
            "next_action_date": "",
            "priority": "low",
            "notes": "مثال تدريبي — لا ترسل",
        },
    ]
    p = tmp_path / "leads.csv"
    with p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=_FIELDS)
        w.writeheader()
        w.writerows(rows)
    return p


def test_snapshot_builds_with_expected_sections(mixed_csv: Path) -> None:
    snap = bcl.build_snapshot(mixed_csv, max_drafts=10)
    for key in ("meta", "services", "pipeline", "drafts", "call_list", "proposals"):
        assert key in snap, f"missing section {key}"
    assert snap["meta"]["counts"]["services"] == 8
    assert all("pricing_note" in s for s in snap["services"])


def test_no_fabricated_real_leads(mixed_csv: Path) -> None:
    snap = bcl.build_snapshot(mixed_csv, max_drafts=10)
    # Exactly one row in the fixture is a genuine company; the rest are placeholders.
    assert snap["meta"]["counts"]["real_leads"] == 1
    real = [p for p in snap["pipeline"] if p["data_status"] == "real"]
    assert [r["company"] for r in real] == ["شركة الأفق للخدمات"]
    # The REPLACE row must be flagged placeholder, never real.
    placeholders = [p for p in snap["pipeline"] if p["data_status"] == "seed_placeholder"]
    assert any("REPLACE" in p["company"] for p in placeholders)


def test_every_draft_is_approval_required(mixed_csv: Path) -> None:
    snap = bcl.build_snapshot(mixed_csv, max_drafts=10)
    assert snap["drafts"], "expected at least one draft"
    assert all(d["approval_status"] == "approval_required" for d in snap["drafts"])


def test_calls_are_manual_and_proposals_gated(mixed_csv: Path) -> None:
    snap = bcl.build_snapshot(mixed_csv, max_drafts=10)
    assert all(c["approval_status"] == "founder_calls_manually" for c in snap["call_list"])
    assert all(p["approval_status"] == "approval_required" for p in snap["proposals"])
    assert all("G03" in p["pricing_gate"] for p in snap["proposals"])


def test_do_not_contact_excluded_from_outreach(mixed_csv: Path) -> None:
    snap = bcl.build_snapshot(mixed_csv, max_drafts=10)
    banned = "وكالة مثال — لا ترسل"
    assert all(d["company"] != banned for d in snap["drafts"])
    assert all(c["company"] != banned for c in snap["call_list"])
    assert all(p["company"] != banned for p in snap["proposals"])


def test_diagnostic_sample_is_gated(mixed_csv: Path) -> None:
    snap = bcl.build_snapshot(mixed_csv, max_drafts=10)
    diag = snap["diagnostic_sample"]
    assert diag is not None
    assert diag["approval_status"] == "approval_required"
    # The top-ranked contactable lead is the real one (highest score).
    assert diag["company"] == "شركة الأفق للخدمات"


def test_scoring_is_transparent(mixed_csv: Path) -> None:
    snap = bcl.build_snapshot(mixed_csv, max_drafts=10)
    for p in snap["pipeline"]:
        assert 0 <= p["score"] <= 100
        assert sum(p["score_breakdown"].values()) == p["score"] or p["score"] == 100


def test_doctrine_banner_present(mixed_csv: Path) -> None:
    snap = bcl.build_snapshot(mixed_csv, max_drafts=10)
    banner = " ".join(snap["meta"]["doctrine"])
    assert "موافقة" in banner
    assert "scraping" in banner
    assert "مخترعة" in banner
