"""
Unit tests for api/routers/meeting_agenda.py

Tests cover:
- 5 meeting types with bilingual names, agendas, avoid guidance
- Saudi meeting protocol (bilingual)
- _build_agenda: Ramadan note, client injection, governance
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.meeting_agenda import (
    _MEETING_TYPES,
    _SAUDI_MEETING_PROTOCOL,
    _build_agenda,
    MeetingAgendaRequest,
    router,
)


class TestMeetingTypes:
    def test_five_meeting_types(self):
        assert len(_MEETING_TYPES) == 5

    def test_expected_types(self):
        expected = {"discovery_call", "proposal_presentation", "executive_sponsor_brief", "qbr_quarterly_review", "renewal_close"}
        assert expected == set(_MEETING_TYPES.keys())

    def test_all_bilingual(self):
        for k, v in _MEETING_TYPES.items():
            assert v.get("name_en"), f"{k} missing name_en"
            assert v.get("name_ar"), f"{k} missing name_ar"

    def test_all_have_duration(self):
        for k, v in _MEETING_TYPES.items():
            assert v.get("duration_minutes", 0) > 0, f"{k} missing duration_minutes"

    def test_all_have_agenda_template(self):
        for k, v in _MEETING_TYPES.items():
            assert len(v.get("agenda_template_en", [])) >= 2, f"{k} needs ≥2 agenda items"

    def test_all_have_avoid(self):
        for k, v in _MEETING_TYPES.items():
            assert len(v.get("avoid_en", [])) >= 1, f"{k} needs ≥1 avoid item"

    def test_all_have_success_criteria(self):
        for k, v in _MEETING_TYPES.items():
            assert v.get("success_criteria_en"), f"{k} missing success_criteria_en"

    def test_all_have_arabic_protocol(self):
        for k, v in _MEETING_TYPES.items():
            assert v.get("arabic_protocol_en"), f"{k} missing arabic_protocol_en"

    def test_executive_brief_shorter_than_qbr(self):
        exec_dur = _MEETING_TYPES["executive_sponsor_brief"]["duration_minutes"]
        qbr_dur = _MEETING_TYPES["qbr_quarterly_review"]["duration_minutes"]
        assert exec_dur < qbr_dur

    def test_discovery_call_has_pain_discovery(self):
        agenda = " ".join(str(item) for item in _MEETING_TYPES["discovery_call"]["agenda_template_en"]).lower()
        assert "pain" in agenda or "discovery" in agenda or "context" in agenda


class TestSaudiMeetingProtocol:
    def test_protocol_is_dict(self):
        assert isinstance(_SAUDI_MEETING_PROTOCOL, dict)

    def test_has_pre_meeting(self):
        assert _SAUDI_MEETING_PROTOCOL.get("pre_meeting_en") or any("pre" in k.lower() for k in _SAUDI_MEETING_PROTOCOL.keys())

    def test_has_greeting_guidance(self):
        protocol_text = " ".join(str(v) for v in _SAUDI_MEETING_PROTOCOL.values()).lower()
        assert "greeting" in protocol_text or "handshake" in protocol_text or "coffee" in protocol_text

    def test_bilingual_protocol(self):
        # Should have both _en and _ar keys
        keys = set(_SAUDI_MEETING_PROTOCOL.keys())
        en_keys = {k for k in keys if k.endswith("_en")}
        ar_keys = {k for k in keys if k.endswith("_ar")}
        assert len(en_keys) >= 2
        assert len(ar_keys) >= 2


class TestBuildAgenda:
    def _make_request(self, **overrides) -> MeetingAgendaRequest:
        data = dict(
            meeting_type="discovery_call",
            client_name="Ahmed Al-Rashid",
            client_company="Almarai Group",
            client_title="VP Sales",
            key_topics=["ZATCA compliance", "pipeline visibility"],
            is_ramadan_period=False,
            language_preference="en",
        )
        data.update(overrides)
        return MeetingAgendaRequest(**data)

    def test_returns_dict(self):
        result = _build_agenda(self._make_request())
        assert isinstance(result, dict)

    def test_has_agenda_items(self):
        result = _build_agenda(self._make_request())
        assert len(result.get("agenda_items", [])) >= 2

    def test_has_duration(self):
        result = _build_agenda(self._make_request())
        assert result.get("duration_minutes", 0) > 0

    def test_has_protocol_notes(self):
        result = _build_agenda(self._make_request())
        assert result.get("protocol_notes") or result.get("arabic_protocol")

    def test_ramadan_note_added_when_ramadan(self):
        result = _build_agenda(self._make_request(is_ramadan_period=True))
        result_text = str(result).lower()
        assert "ramadan" in result_text

    def test_unknown_meeting_type_raises(self):
        with pytest.raises(Exception):
            _build_agenda(self._make_request(meeting_type="nonexistent_type_xyz"))

    def test_governance_allow_with_review(self):
        result = _build_agenda(self._make_request())
        assert result.get("governance_decision") == "ALLOW_WITH_REVIEW"

    def test_all_meeting_types_build_successfully(self):
        for meeting_type in _MEETING_TYPES.keys():
            result = _build_agenda(self._make_request(meeting_type=meeting_type))
            assert isinstance(result, dict)

    def test_has_success_criteria(self):
        result = _build_agenda(self._make_request())
        assert result.get("success_criteria_en") or result.get("success_criteria")


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/meeting-agenda"

    def test_router_tags(self):
        assert "Sales" in router.tags
