from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "commercial" / "generate_growth_sales_cards.py"
spec = importlib.util.spec_from_file_location("generate_growth_sales_cards", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_growth_card_is_draft_only_and_requires_approval() -> None:
    card = module.build_card(
        1,
        {
            "company_name": "Test Company",
            "sector": "b2b",
            "city": "Riyadh",
            "source_url": "https://example.com/contact",
            "verification_status": "ready_for_review",
            "motion": "sales",
            "recommended_channel": "email",
        },
    )
    assert card.send_status == "draft_only"
    assert card.approval_required is True
    assert card.owner_decision == "review"


def test_whatsapp_growth_card_has_at_most_three_buttons() -> None:
    card = module.build_card(
        2,
        {
            "company_name": "Opt In Company",
            "sector": "clinics",
            "city": "Jeddah",
            "source_url": "https://example.com/contact",
            "verification_status": "ready_for_review",
            "motion": "sales",
            "recommended_channel": "whatsapp",
        },
    )
    assert card.recommended_channel == "whatsapp"
    assert card.risk_level == "high"
    assert len(card.buttons) <= 3
    assert [button["title"] for button in card.buttons] == ["اعتماد", "تعديل", "تخطي"]


def test_missing_source_url_is_reported() -> None:
    card = module.build_card(
        3,
        {
            "company_name": "No Source Company",
            "verification_status": "unverified",
        },
    )
    errors = module.validate_card(card)
    assert any("source_url is required" in error for error in errors)


def test_unknown_motion_falls_back_to_sales() -> None:
    assert module.normalize_motion("unknown") == "sales"
