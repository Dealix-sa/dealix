import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data" / "commercial" / "agentic_commercial_os_registry.json"
DOCTRINE = ROOT / "docs" / "ops" / "DEALIX_LOOP_ENGINEERING_OS.md"
RUNNER = ROOT / "scripts" / "commercial" / "run_agentic_commercial_control_plane.py"


def test_agentic_registry_exists_and_disables_live_outbound_by_default():
    assert REGISTRY.exists()
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    defaults = data["safety_defaults"]
    assert defaults["EXTERNAL_SEND_ENABLED"] is False
    assert defaults["EMAIL_SEND_ENABLED"] is False
    assert defaults["WHATSAPP_SEND_ENABLED"] is False
    assert defaults["WHATSAPP_ALLOW_LIVE_SEND"] is False
    assert defaults["SMS_SEND_ENABLED"] is False
    assert defaults["OUTBOUND_MODE"] == "draft_only"


def test_every_loop_has_stop_condition_verifier_and_human_review():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    loops = data.get("loops", [])
    assert loops
    for loop in loops:
        assert loop.get("loop_id")
        assert loop.get("goal")
        assert loop.get("outputs")
        assert loop.get("verifier")
        assert loop.get("stop_condition")
        assert loop.get("human_review_required") is True
        assert loop.get("safety_gates")


def test_commercial_products_block_fake_roi_and_uncontrolled_sends():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    products = data.get("commercial_products", [])
    assert products
    flattened = "\n".join("\n".join(p.get("forbidden_outputs", [])) for p in products).lower()
    assert "fake roi" in flattened or "guaranteed revenue" in flattened
    assert "automatic" in flattened


def test_loop_doctrine_exists_and_declares_review_first_policy():
    assert DOCTRINE.exists()
    text = DOCTRINE.read_text(encoding="utf-8")
    assert "EXTERNAL_SEND_ENABLED=false" in text
    assert "OUTBOUND_MODE=draft_only" in text
    assert "human approval" in text.lower() or "human review" in text.lower()
    assert "stop condition" in text.lower()


def test_control_plane_runner_generates_reports_with_safe_defaults(tmp_path):
    assert RUNNER.exists()
    env = os.environ.copy()
    env.update(
        {
            "EXTERNAL_SEND_ENABLED": "false",
            "EMAIL_SEND_ENABLED": "false",
            "WHATSAPP_SEND_ENABLED": "false",
            "WHATSAPP_ALLOW_LIVE_SEND": "false",
            "SMS_SEND_ENABLED": "false",
            "OUTBOUND_MODE": "draft_only",
        }
    )
    result = subprocess.run(
        [sys.executable, str(RUNNER)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "AGENTIC_COMMERCIAL_OS_CONTROL_PLANE_READY" in result.stdout
    assert "SAFETY_STATUS=safe" in result.stdout
    latest = ROOT / "reports" / "agentic_commercial_os" / "latest.json"
    assert latest.exists()
    payload = json.loads(latest.read_text(encoding="utf-8"))
    assert payload["safety"]["status"] == "safe"
    assert payload["founder_actions"]
