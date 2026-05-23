import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.founder_focus import choose_founder_focus


def test_focus_payment_after_proposal():
    metrics = {"paid": 0, "proposal_sent": 1, "contacted": 25, "sample_sent": 3}
    assert choose_founder_focus(metrics, []) == "Convert proposal to payment or PO."


def test_focus_outbound_when_contacted_low():
    metrics = {"paid": 0, "proposal_sent": 0, "contacted": 10, "sample_sent": 0}
    assert choose_founder_focus(metrics, []) == "Reach 25 founder-led DMs today."
