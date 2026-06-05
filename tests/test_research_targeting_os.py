"""Tests for the Dealix Research & Targeting OS engine (scripts/research_targeting_os.py)."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.research_targeting_os import (
    BLOCKED_SOURCES,
    Candidate,
    build_draft,
    build_drafts,
    daily_intelligence,
    dedupe_companies,
    evaluate,
    evaluate_rows,
    grade_for_score,
    load_seed,
    load_source_allowlist,
    normalize_company_name,
    normalize_domain,
    recommend_offer,
    run,
    score_candidate,
    targeting_ready,
    weakness_hypothesis,
)

# --- normalization --------------------------------------------------------


def test_normalize_company_name_drops_legal_suffix() -> None:
    assert normalize_company_name("Acme Consulting LLC") == "acme consulting"
    assert normalize_company_name("Bright Agency, Inc.") == "bright agency"


def test_normalize_company_name_strips_arabic_legal_tokens() -> None:
    assert "شركة" not in normalize_company_name("شركة برايت للدعاية")


def test_normalize_domain_strips_scheme_www_and_path() -> None:
    assert normalize_domain("https://www.example.sa/contact?x=1") == "example.sa"
    assert normalize_domain("HTTP://Example.SA/") == "example.sa"
    assert normalize_domain("ops@example.sa") == "example.sa"


# --- dedupe ---------------------------------------------------------------


def test_dedupe_merges_by_domain_and_unions_evidence() -> None:
    rows = [
        {
            "company": "Bright Agency",
            "domain": "bright.sa",
            "evidence_urls": "https://bright.sa",
            "evidence_count": "1",
        },
        {
            "company": "شركة برايت",
            "domain": "https://www.bright.sa/ar",
            "evidence_urls": "https://bright.sa/ar",
            "evidence_count": "1",
        },
    ]
    merged = dedupe_companies(rows)
    assert len(merged) == 1
    assert merged[0]["evidence_count"] == 1
    assert "https://bright.sa" in merged[0]["evidence_urls"]
    assert "https://bright.sa/ar" in merged[0]["evidence_urls"]


def test_dedupe_falls_back_to_name_when_no_domain() -> None:
    rows = [
        {"company": "Acme Consulting LLC"},
        {"company": "acme consulting"},
    ]
    assert len(dedupe_companies(rows)) == 1


# --- scoring + grading ----------------------------------------------------


def _strong_candidate(**overrides: object) -> Candidate:
    base = {
        "company": "Acme",
        "domain": "acme.sa",
        "sector": "b2b_consulting",
        "city": "Riyadh",
        "source": "founder_list",
        "services_count": 6,
        "has_contact": True,
        "has_careers": True,
        "expansion_signal": True,
        "hiring_signal": True,
        "warm_path": True,
        "relationship": "warm",
        "evidence_count": 3,
        "evidence_urls": ["https://acme.sa", "https://acme.sa/contact", "https://acme.sa/services"],
    }
    base.update(overrides)
    return Candidate(**base)  # type: ignore[arg-type]


def test_score_bounds_and_total() -> None:
    s = score_candidate(_strong_candidate())
    assert 0 <= s.total <= 100
    assert s.icp_fit <= 35
    assert s.pain_signal <= 25
    assert s.intent_timing <= 20
    assert s.access <= 10
    assert s.evidence_confidence <= 10
    assert -20 <= s.risk_penalty <= 0


def test_strong_candidate_grades_high() -> None:
    ev = evaluate(_strong_candidate())
    assert ev.grade in ("A+", "A")
    assert ev.score.total >= 70


def test_sensitive_sector_is_penalized() -> None:
    plain = score_candidate(_strong_candidate())
    sensitive = score_candidate(_strong_candidate(sensitive_sector=True, sector="defense"))
    assert sensitive.risk_penalty < 0
    assert sensitive.total < plain.total


def test_grade_thresholds() -> None:
    assert grade_for_score(90) == "A+"
    assert grade_for_score(75) == "A"
    assert grade_for_score(60) == "B"
    assert grade_for_score(45) == "C"
    assert grade_for_score(10) == "D"


# --- golden rule ----------------------------------------------------------


def test_golden_rule_caps_grade_without_evidence_or_warm() -> None:
    # No warm path, no evidence -> cannot exceed B even with strong signals.
    c = _strong_candidate(warm_path=False, relationship="cold", evidence_count=0, evidence_urls=[])
    assert targeting_ready(c) is False
    ev = evaluate(c)
    assert ev.grade not in ("A+", "A")


def test_warm_path_makes_targeting_ready() -> None:
    c = _strong_candidate(warm_path=True)
    assert targeting_ready(c) is True


# --- weakness + offer -----------------------------------------------------


def test_weakness_proof_maps_to_proof_os() -> None:
    c = Candidate(company="X", sector="agency", services_count=5, has_case_studies=False)
    code, _label, primary_os = weakness_hypothesis(c)
    assert code == "proof_weakness"
    assert primary_os == "Proof OS"


def test_weakness_data_fragmentation_maps_to_data_os() -> None:
    c = Candidate(company="X", sector="saas", data_fragmentation=True)
    _code, _label, primary_os = weakness_hypothesis(c)
    assert primary_os == "Data OS"


def test_recommend_offer_ladder() -> None:
    ready = _strong_candidate()
    assert recommend_offer(ready, "A+") == "Command Sprint"
    assert recommend_offer(ready, "B") == "Diagnostic"
    assert recommend_offer(ready, "C") == "Nurture"
    assert recommend_offer(ready, "D") == "None"
    not_ready = _strong_candidate(
        warm_path=False, relationship="cold", evidence_count=0, evidence_urls=[]
    )
    assert recommend_offer(not_ready, "A") == "Diagnostic"


# --- source policy --------------------------------------------------------


def test_blocked_sources_are_rejected() -> None:
    allowed, blocked = load_source_allowlist(None)
    rows = [
        {
            "company": "Good Co",
            "domain": "good.sa",
            "source": "founder_list",
            "evidence_count": "2",
            "evidence_urls": "a;b",
        },
        {"company": "Bad Co", "domain": "bad.sa", "source": "scraping"},
    ]
    evals, rejected = evaluate_rows(rows, allowed_sources=allowed, blocked_sources=blocked)
    assert [e.candidate.company for e in evals] == ["Good Co"]
    assert rejected and rejected[0]["reason"] == "blocked_source"


def test_non_allowlisted_source_is_rejected() -> None:
    allowed, blocked = load_source_allowlist(None)
    rows = [{"company": "Weird Co", "domain": "weird.sa", "source": "mystery_source"}]
    evals, rejected = evaluate_rows(rows, allowed_sources=allowed, blocked_sources=blocked)
    assert evals == []
    assert rejected[0]["reason"] == "source_not_allowlisted"


def test_default_allowlist_excludes_blocked() -> None:
    allowed, blocked = load_source_allowlist(None)
    for b in BLOCKED_SOURCES:
        assert b not in allowed
        assert b in blocked


# --- drafts ---------------------------------------------------------------


def test_build_draft_is_draft_only_and_carries_evidence() -> None:
    ev = evaluate(_strong_candidate())
    draft = build_draft(ev)
    assert draft["auto_send"] is False
    assert draft["status"] == "draft_for_review"
    assert draft["evidence_count"] >= 2
    assert draft["draft_en"] and draft["draft_ar"]
    # No guarantee / fake-proof language should survive the claim-safety audit.
    assert draft["claim_safety_decision"] != "BLOCK"


def test_build_drafts_only_for_ready_a_grades() -> None:
    ready = _strong_candidate()
    not_ready = _strong_candidate(
        company="Cold Co", warm_path=False, relationship="cold", evidence_count=0, evidence_urls=[]
    )
    evals = [evaluate(ready), evaluate(not_ready)]
    drafts = build_drafts(evals, limit=10)
    companies = {d["company"] for d in drafts}
    assert "Cold Co" not in companies


# --- intelligence ---------------------------------------------------------


def test_daily_intelligence_picks_best_sector() -> None:
    evals = [
        evaluate(_strong_candidate(company="A", sector="b2b_consulting")),
        evaluate(
            _strong_candidate(
                company="B",
                sector="ecommerce",
                services_count=1,
                has_case_studies=True,
                expansion_signal=False,
                hiring_signal=False,
            )
        ),
    ]
    intel = daily_intelligence(evals)
    assert intel["best_sector"] == "b2b_consulting"
    assert intel["recommendation"]


def test_daily_intelligence_handles_empty() -> None:
    intel = daily_intelligence([])
    assert intel["best_sector"] is None
    assert "No evaluable" in intel["recommendation"]


# --- seed loading + end-to-end --------------------------------------------


def test_load_seed_skips_replace_placeholders(tmp_path: Path) -> None:
    seed = tmp_path / "seed.csv"
    with seed.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["company", "domain", "source"])
        writer.writerow(["REPLACE:placeholder", "x.sa", "founder_list"])
        writer.writerow(["Real Co", "real.sa", "founder_list"])
    rows = load_seed(seed)
    assert [r["company"] for r in rows] == ["Real Co"]


def test_run_writes_all_outputs(tmp_path: Path) -> None:
    seed = tmp_path / "seed.csv"
    header = (
        "company,domain,sector,city,source,services_count,has_case_studies,has_contact,"
        "has_careers,has_customers_page,has_projects,has_support,expansion_signal,"
        "hiring_signal,launch_signal,partnership_signal,data_fragmentation,warm_path,"
        "relationship,evidence_count,evidence_urls,sensitive_sector,data_gap,notes"
    )
    rows = [
        header,
        "Acme,acme.sa,b2b_consulting,Riyadh,founder_list,6,false,true,true,false,false,false,true,true,false,false,false,true,warm,3,https://acme.sa;https://acme.sa/c;https://acme.sa/s,false,false,warm",
        "Bad,bad.sa,saas,Riyadh,scraping,1,false,false,false,false,false,false,false,false,false,false,false,false,cold,0,,false,true,blocked",
    ]
    seed.write_text("\n".join(rows) + "\n", encoding="utf-8")
    out = tmp_path / "out"
    summary = run(
        seed=seed,
        out_dir=out,
        top=50,
        discover=False,
        queries_file=None,
        allowlist_path=None,
    )
    assert summary["evaluated"] == 1
    assert summary["rejected"] == 1
    for name in (
        "ranked_targets.csv",
        "ranked_targets.jsonl",
        "daily_targeting_brief.md",
        "drafts_for_review.md",
        "weakness_map.md",
    ):
        assert (out / name).exists()
    # JSONL records carry a score breakdown.
    first = json.loads((out / "ranked_targets.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert "score_breakdown" in first
    assert first["score_breakdown"]["total"] == first["score"]


def test_run_with_template_seed_is_noop_safe() -> None:
    # The shipped template is all REPLACE: rows -> evaluates zero, never crashes.
    seed = Path("data/targeting/company_seed_template.csv")
    if not seed.exists():  # pragma: no cover - repo layout guard
        pytest.skip("template seed not present")
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        summary = run(
            seed=seed,
            out_dir=Path(td),
            top=50,
            discover=False,
            queries_file=None,
            allowlist_path=Path("data/targeting/source_allowlist.json"),
        )
    assert summary["evaluated"] == 0
