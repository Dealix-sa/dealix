from app.commercial.sales_agent import build_sales_agent_pack
from pathlib import Path


def test_sales_agent_company_brain_assets_exist():
    required = [
        Path("docs/ops/SALES_AGENT_COMPANY_BRAIN_OS_AR.md"),
        Path("gtm/PAIN_SIGNAL_TARGETING_ENGINE_AR.md"),
        Path("sales/SALES_AGENT_NEGOTIATION_PLAYBOOK_AR.md"),
    ]
    for path in required:
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8").strip(), f"empty {path}"


def test_sales_agent_assets_keep_review_first_safety():
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            Path("docs/ops/SALES_AGENT_COMPANY_BRAIN_OS_AR.md"),
            Path("gtm/PAIN_SIGNAL_TARGETING_ENGINE_AR.md"),
            Path("sales/SALES_AGENT_NEGOTIATION_PLAYBOOK_AR.md"),
        ]
    )
    assert "EXTERNAL_SEND_ENABLED=false" in combined
    assert "OUTBOUND_MODE=draft_only" in combined
    assert "لا تعد بإيراد مضمون" in combined or "guaranteed" in combined.lower()
    assert "source_url" in combined
    assert "فرضية" in combined


def test_sales_agent_pack_builder_is_review_first():
    pack = build_sales_agent_pack(
        company_name="Sample Clinic",
        sector="clinics",
        city="Riyadh",
        source_url="https://example.com",
    )
    data = pack.to_dict()
    assert data["company_name"] == "Sample Clinic"
    assert data["recommended_offer"] == "Follow-up Recovery OS"
    assert data["communication_mode"] == "draft_only"
    assert data["owner_decision_required"] is True
    assert "https://example.com" == data["source_url"]
    assert data["discovery_questions"]
    assert data["negotiation_notes"]
