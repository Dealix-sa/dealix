"""Trust contracts for public prospect previews and generated prospect output."""
from __future__ import annotations

import ast
import asyncio
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROSPECT_ROUTER = ROOT / "api" / "routers" / "prospect.py"
PROSPECTOR = ROOT / "auto_client_acquisition" / "agents" / "prospector.py"


def _load_demo() -> Any:
    source = PROSPECT_ROUTER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    demo = next(
        node
        for node in tree.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "demo"
    )
    demo.decorator_list = []
    namespace: dict[str, Any] = {"Any": Any}
    exec(
        compile(ast.Module(body=[demo], type_ignores=[]), str(PROSPECT_ROUTER), "exec"),
        namespace,
    )
    return namespace["demo"]


def test_public_demo_contains_synthetic_hypotheses_only() -> None:
    payload = asyncio.run(_load_demo()())
    assert payload["status"] == "research_hypotheses"
    assert payload["demo"] is True
    assert payload["requires_source_validation"] is True
    assert payload["external_action_allowed"] is False
    assert [lead["company_en"] for lead in payload["leads"]] == [
        "Synthetic SaaS Alpha",
        "Synthetic Services Beta",
        "Synthetic Commerce Gamma",
    ]


def test_public_demo_blocks_action_until_source_validation() -> None:
    payload = asyncio.run(_load_demo()())
    for lead in payload["leads"]:
        assert lead["website"] is None
        assert lead["linkedin"] is None
        assert lead["decision_maker_hints"] == []
        assert lead["fit_score"] == 0
        assert lead["confidence"] == 0
        assert lead["risk_level"] == "BLOCKED"
        assert lead["recommended_channel"] == "HOLD_FOR_APPROVAL"
        assert lead["next_action"] == "RESEARCH_MORE"


def test_public_demo_does_not_embed_named_real_companies() -> None:
    source = PROSPECT_ROUTER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    demo = next(
        node
        for node in tree.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "demo"
    )
    demo_source = ast.get_source_segment(source, demo) or ""
    assert not [name for name in ("Foodics", "Rekaz", '"Zid"') if name in demo_source]


def test_generated_prospect_results_declare_provenance_boundaries() -> None:
    source = PROSPECTOR.read_text(encoding="utf-8")
    required = (
        '"status": "research_hypotheses"',
        '"demo": False',
        '"requires_source_validation": True',
        '"external_action_allowed": False',
    )
    assert not [fragment for fragment in required if fragment not in source]
