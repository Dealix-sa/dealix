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
