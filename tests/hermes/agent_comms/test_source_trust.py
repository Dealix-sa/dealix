"""Trust scoring assigns higher levels to system than external/unknown sources."""

from __future__ import annotations

from dealix.hermes.agent_comms.source_trust import meets_threshold, trust_of


def test_trust_levels_ordering() -> None:
    assert trust_of("system").score > trust_of("approved_agent").score > trust_of("external").score
    assert trust_of("ghost").level == "unknown"
    assert meets_threshold("approved_agent", 50) is True
    assert meets_threshold("external", 50) is False
