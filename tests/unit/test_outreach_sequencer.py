"""Unit tests for outreach_sequencer."""

from auto_client_acquisition.sales_os.outreach_sequencer import (
    MotionKey,
    OutreachChannel,
    OutreachSequence,
    build_sequence,
    list_available_motions,
)


class TestBuildSequence:
    def test_returns_outreach_sequence(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        assert isinstance(seq, OutreachSequence)

    def test_motion_stored(self):
        seq = build_sequence(MotionKey.B_DIRECT)
        assert seq.motion == MotionKey.B_DIRECT

    def test_icp_tier_stored(self):
        seq = build_sequence(MotionKey.A_AGENCY, icp_tier="agency")
        assert seq.icp_tier == "agency"

    def test_pain_signal_stored(self):
        seq = build_sequence(MotionKey.A_AGENCY, pain_signal="proof_gap")
        assert seq.pain_signal == "proof_gap"

    def test_messages_nonempty(self):
        for motion in MotionKey:
            seq = build_sequence(motion)
            assert seq.total_touchpoints > 0

    def test_total_touchpoints_matches_messages(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        assert seq.total_touchpoints == len(seq.messages)

    def test_estimated_duration_is_sum_of_waits(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        expected = sum(m.wait_days_after_previous for m in seq.messages)
        assert seq.estimated_duration_days == expected

    def test_governance_note_present(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        assert len(seq.governance_note_ar) > 0
        assert len(seq.governance_note_en) > 0


class TestMessages:
    def test_all_messages_require_approval(self):
        for motion in MotionKey:
            seq = build_sequence(motion)
            for msg in seq.messages:
                assert msg.requires_approval is True

    def test_steps_numbered_from_1(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        assert seq.messages[0].step_number == 1

    def test_steps_numbered_sequentially(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        numbers = [m.step_number for m in seq.messages]
        assert numbers == list(range(1, len(numbers) + 1))

    def test_bilingual_bodies(self):
        for motion in MotionKey:
            seq = build_sequence(motion)
            for msg in seq.messages:
                assert len(msg.body_ar) > 0
                assert len(msg.body_en) > 0

    def test_bilingual_cta(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        for msg in seq.messages:
            assert len(msg.call_to_action_ar) > 0
            assert len(msg.call_to_action_en) > 0

    def test_channels_are_valid(self):
        valid_channels = set(OutreachChannel)
        seq = build_sequence(MotionKey.A_AGENCY)
        for msg in seq.messages:
            assert msg.channel in valid_channels

    def test_no_cold_whatsapp_channel(self):
        for motion in MotionKey:
            seq = build_sequence(motion)
            for msg in seq.messages:
                assert msg.channel != "cold_whatsapp"
                assert msg.channel != "whatsapp_blast"

    def test_first_message_zero_wait(self):
        for motion in MotionKey:
            seq = build_sequence(motion)
            assert seq.messages[0].wait_days_after_previous == 0


class TestMotionA:
    def test_has_4_touchpoints(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        assert seq.total_touchpoints == 4

    def test_uses_linkedin_for_first_touch(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        assert seq.messages[0].channel == OutreachChannel.LINKEDIN

    def test_uses_email_for_step_3(self):
        seq = build_sequence(MotionKey.A_AGENCY)
        assert seq.messages[2].channel == OutreachChannel.EMAIL


class TestMotionD:
    def test_executive_motion_exists(self):
        seq = build_sequence(MotionKey.D_EXECUTIVE)
        assert seq.total_touchpoints >= 2

    def test_uses_email_first(self):
        seq = build_sequence(MotionKey.D_EXECUTIVE)
        assert seq.messages[0].channel == OutreachChannel.EMAIL


class TestListAvailableMotions:
    def test_returns_all_motions(self):
        motions = list_available_motions()
        assert set(motions) == set(MotionKey)

    def test_returns_list(self):
        assert isinstance(list_available_motions(), list)
