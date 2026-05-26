import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "dealix_os" / "cli.py"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def test_doctor():
    # Make sure required directories exist so doctor is READY
    for name in ["ledgers", "clients", "sales"]:
        (ROOT / name).mkdir(parents=True, exist_ok=True)
    result = run_cli("doctor")
    assert "Status: READY" in result.stdout


def test_governance_flags_claims():
    result = run_cli("governance-check", "we guarantee sales and send WhatsApp automatically")
    assert "guaranteed_claim" in result.stdout
    assert "whatsapp_sensitive" in result.stdout


def test_score_returns_recommendation():
    result = run_cli("score", "paid B2B agency partner with monthly retainer and CRM data")
    assert "recommended_capability" in result.stdout
    assert "recommended_service" in result.stdout


def test_client_pack_creates_files():
    result = run_cli(
        "client-pack",
        "--client", "Pytest Client",
        "--sector", "B2B Services",
        "--problem", "messy leads",
        "--service", "lead-intelligence",
    )
    assert "Client pack created" in result.stdout
    client_dir = ROOT / "clients" / "pytest-client"
    assert (client_dir / "CLIENT_PROFILE.md").exists()
    assert (client_dir / "PROOF_PACK_TEMPLATE.md").exists()


def test_value_and_proof_pack():
    result = run_cli(
        "value",
        "--client", "Pytest Client",
        "--service", "lead-intelligence",
        "--metric", "qualified accounts ranked",
        "--result", "top 50 ranked",
    )
    assert "Value ledger updated" in result.stdout

    result = run_cli(
        "proof-pack",
        "--client", "Pytest Client",
        "--service", "lead-intelligence",
        "--metric", "qualified accounts ranked",
        "--result", "top 50 ranked",
    )
    assert "Proof pack generated" in result.stdout
