"""
test_os_yaml_parse.py — Verify every os/*.yml and os/growth/*.yml is parseable
and contains the required mandatory fields.

Doctrine: os/ layer must be runtime-valid at all times.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
OS_DIR = REPO_ROOT / "os"
GROWTH_DIR = OS_DIR / "growth"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert data is not None, f"{path.name} produced null YAML"
    assert isinstance(data, dict), (
        f"{path.name} top-level must be a mapping, got {type(data).__name__}"
    )
    return data


def _yaml_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob("*.yml"))


# ---------------------------------------------------------------------------
# Parametrized: all yml files parse without error
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "yml_path",
    _yaml_files(OS_DIR) + _yaml_files(GROWTH_DIR),
    ids=lambda p: p.relative_to(REPO_ROOT).as_posix(),
)
def test_yaml_parses_cleanly(yml_path: Path) -> None:
    """Every os YAML file must parse with yaml.safe_load without raising."""
    data = _load(yml_path)
    assert data is not None


# ---------------------------------------------------------------------------
# 03_OFFERS.yml
# ---------------------------------------------------------------------------


class TestOffersYml:
    path = OS_DIR / "03_OFFERS.yml"

    def test_file_exists(self) -> None:
        assert self.path.exists(), "os/03_OFFERS.yml is missing"

    def test_has_offers_key(self) -> None:
        data = _load(self.path)
        assert "offers" in data, "03_OFFERS.yml must have top-level 'offers' key"

    def test_offers_is_dict(self) -> None:
        data = _load(self.path)
        assert isinstance(data["offers"], dict)

    def test_each_offer_has_required_fields(self) -> None:
        data = _load(self.path)
        required = {"id", "name", "category"}
        for key, val in data["offers"].items():
            missing = required - set(val.keys())
            assert not missing, f"Offer '{key}' missing fields: {missing}"

    def test_no_duplicate_offer_ids(self) -> None:
        data = _load(self.path)
        ids = [v["id"] for v in data["offers"].values() if isinstance(v, dict) and "id" in v]
        assert len(ids) == len(set(ids)), f"Duplicate offer IDs found: {ids}"


# ---------------------------------------------------------------------------
# 04_MARKETS.yml
# ---------------------------------------------------------------------------


class TestMarketsYml:
    path = OS_DIR / "04_MARKETS.yml"

    def test_file_exists(self) -> None:
        assert self.path.exists()

    def test_has_primary_markets(self) -> None:
        data = _load(self.path)
        assert "primary_markets" in data

    def test_each_market_has_id_and_priority(self) -> None:
        data = _load(self.path)
        markets = data["primary_markets"]
        for key, val in markets.items():
            if not isinstance(val, dict):
                continue
            assert "id" in val, f"Market '{key}' missing 'id'"
            assert "priority" in val, f"Market '{key}' missing 'priority'"


# ---------------------------------------------------------------------------
# 05_SCORING.yml
# ---------------------------------------------------------------------------


class TestScoringYml:
    path = OS_DIR / "05_SCORING.yml"

    def test_file_exists(self) -> None:
        assert self.path.exists()

    def test_required_top_level_keys(self) -> None:
        data = _load(self.path)
        for key in ("version", "max_score", "scoring_dimensions", "decision_thresholds"):
            assert key in data, f"05_SCORING.yml missing '{key}'"

    def test_dimension_weights_sum_to_100(self) -> None:
        data = _load(self.path)
        dims = data["scoring_dimensions"]
        total = sum(v.get("weight", 0) for v in dims.values() if isinstance(v, dict))
        assert total == 100, f"Dimension weights sum to {total}, expected 100"

    def test_decision_thresholds_coverage(self) -> None:
        data = _load(self.path)
        thresholds = data["decision_thresholds"]
        assert len(thresholds) >= 3, "Need at least 3 decision threshold tiers"


# ---------------------------------------------------------------------------
# 06_APPROVAL_GATES.yml
# ---------------------------------------------------------------------------


class TestApprovalGatesYml:
    path = OS_DIR / "06_APPROVAL_GATES.yml"

    def test_file_exists(self) -> None:
        assert self.path.exists()

    def test_required_top_level_keys(self) -> None:
        data = _load(self.path)
        for key in ("version", "enforced_by", "gates"):
            assert key in data, f"06_APPROVAL_GATES.yml missing '{key}'"

    def test_all_gates_have_id_and_approval_flag(self) -> None:
        data = _load(self.path)
        gates = data["gates"]
        for key, val in gates.items():
            if not isinstance(val, dict):
                continue
            assert "id" in val, f"Gate '{key}' missing 'id'"
            assert "requires_human_approval" in val, (
                f"Gate '{key}' missing 'requires_human_approval'"
            )

    def test_no_conflicting_gates(self) -> None:
        """Verify that gates marked allowed=false never also have requires_human_approval=true."""
        data = _load(self.path)
        gates = data["gates"]
        for key, val in gates.items():
            if not isinstance(val, dict):
                continue
            if val.get("allowed") is False:
                # Permanently forbidden gates should not require approval — they are blocked
                assert val.get("requires_human_approval") is not True, (
                    f"Gate '{key}' is permanently forbidden (allowed=false) "
                    f"but also has requires_human_approval=true — conflicting rules"
                )


# ---------------------------------------------------------------------------
# Growth OS YAML (conditional — skip if growth layer not yet present)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not (GROWTH_DIR / "CHANNEL_ROUTER.yml").exists(),
    reason="CHANNEL_ROUTER.yml not yet created",
)
class TestChannelRouterYml:
    path = GROWTH_DIR / "CHANNEL_ROUTER.yml"

    def test_has_channels_key(self) -> None:
        data = _load(self.path)
        assert "channels" in data

    def test_each_channel_has_priority_and_approval(self) -> None:
        data = _load(self.path)
        for key, val in data["channels"].items():
            if not isinstance(val, dict):
                continue
            assert "priority" in val, f"Channel '{key}' missing 'priority'"
            assert "approval_required" in val, f"Channel '{key}' missing 'approval_required'"


@pytest.mark.skipif(
    not (GROWTH_DIR / "ANTI_BAN_GUARDIAN.yml").exists(),
    reason="ANTI_BAN_GUARDIAN.yml not yet created",
)
class TestAntiBanGuardianYml:
    path = GROWTH_DIR / "ANTI_BAN_GUARDIAN.yml"

    def test_has_rules_key(self) -> None:
        data = _load(self.path)
        assert "rules" in data

    def test_each_rule_has_limits(self) -> None:
        data = _load(self.path)
        for key, val in data["rules"].items():
            if not isinstance(val, dict):
                continue
            assert "daily_limit" in val, f"Rule '{key}' missing 'daily_limit'"
            assert "hourly_limit" in val, f"Rule '{key}' missing 'hourly_limit'"
