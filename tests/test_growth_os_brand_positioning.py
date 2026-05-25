"""Brand positioning tests."""

from __future__ import annotations

from dealix.growth_os.brand.positioning import BRAND_POSITIONING


def test_hero_line_is_bilingual() -> None:
    assert BRAND_POSITIONING.hero_line.ar
    assert BRAND_POSITIONING.hero_line.en


def test_four_audience_messages_present() -> None:
    assert len(BRAND_POSITIONING.audiences) == 4
    keys = {a.audience_key for a in BRAND_POSITIONING.audiences}
    assert keys == {"founders", "enterprise", "agencies", "ai_users_governance"}


def test_each_audience_message_is_bilingual() -> None:
    for msg in BRAND_POSITIONING.audiences:
        assert msg.headline.ar and msg.headline.en
        assert msg.subhead.ar and msg.subhead.en
        assert msg.proof_anchor.ar and msg.proof_anchor.en
