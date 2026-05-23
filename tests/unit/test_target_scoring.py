import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.target_scoring import calculate_target_score


def test_target_score_full():
    metrics = {"lead_count": 25, "contacted": 25}
    targets = {"lead_count": 25, "contacted": 25}
    assert calculate_target_score(metrics, targets) == 100


def test_target_score_partial():
    metrics = {"lead_count": 25, "contacted": 10}
    targets = {"lead_count": 25, "contacted": 25}
    assert calculate_target_score(metrics, targets) == 50
