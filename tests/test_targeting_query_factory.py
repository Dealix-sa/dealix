"""Dealix Targeting OS — query factory builds deduped, phase-filtered queries."""

from __future__ import annotations

from scripts.targeting_enrichment import normalize_and_dedupe, normalize_domain
from scripts.targeting_query_factory import build_queries, load_cities, load_sectors


def test_phase1_sectors_subset_of_phase2():
    p1 = {s["id"] for s in load_sectors(phase=1)}
    p2 = {s["id"] for s in load_sectors(phase=2)}
    assert p1
    assert p1.issubset(p2)


def test_phase1_cities_include_riyadh():
    ids = {c["id"] for c in load_cities(phase=1)}
    assert "riyadh" in ids


def test_build_queries_dedupes():
    qs = build_queries(phase=1)
    assert len(qs) == len({q.lower() for q in qs})


def test_build_queries_respects_limit():
    qs = build_queries(phase=1, limit=5)
    assert len(qs) <= 5


def test_build_queries_includes_seed_first():
    seed = ['"custom seed query"']
    qs = build_queries(phase=1, seed_queries=seed, sectors=[], cities=[])
    assert qs[0] == '"custom seed query"'


def test_normalize_domain_strips_www_and_scheme():
    assert normalize_domain("https://www.Example.com/path") == "example.com"
    assert normalize_domain("example.com") == "example.com"


def test_dedupe_keeps_higher_evidence():
    rows = [
        {
            "company_name": "Dup Co",
            "website": "https://dup.example",
            "sector": "b2b_consulting",
            "source_urls": ["https://dup.example/a"],
        },
        {
            "company_name": "Dup Co",
            "website": "https://www.dup.example",
            "sector": "b2b_consulting",
            "source_urls": ["https://dup.example/a", "https://dup.example/b"],
        },
    ]
    out = normalize_and_dedupe(rows, phase=1)
    assert len(out) == 1
    assert out[0]["evidence_count"] == 2
