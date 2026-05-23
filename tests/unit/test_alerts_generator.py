import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.alerts_generator import generate_alerts


def test_red_alert_when_proposal_no_payment():
    metrics = {"paid": 0, "proposal_sent": 1, "contacted": 25, "approvals_pending": 0}
    alerts = generate_alerts(metrics, [])
    assert any(a["level"] == "red" and a["area"] == "Revenue" for a in alerts)
