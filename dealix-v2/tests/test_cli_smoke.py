from dealix_os.cli import services, capabilities, governance_check_text

def test_services_exist():
    data = services()
    assert "lead-intelligence" in data
    assert "company-brain" in data
    assert "ai-governance" in data

def test_capabilities_exist():
    data = capabilities()
    assert "Revenue" in data
    assert "Governance" in data

def test_governance_guarantee_flag():
    result = governance_check_text("we guarantee sales")
    assert result["decision"] == "REVIEW_REQUIRED"
    assert "guaranteed_claim" in result["flags"]