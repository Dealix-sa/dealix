#!/usr/bin/env python3
"""Seed synthetic, PII-free sample data for the Market Production OS.

Builds the sample JSONL stores under ``data/gtm/`` from the typed models so the
samples are always schema-valid. Drafts deliberately include both clean and
violating examples so the quality gate has something to catch in CI.

    python3 scripts/gtm_seed_samples.py

No real people, emails, or phone numbers — companies are labels, recipients are
opaque refs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from auto_client_acquisition.gtm_os.outreach_draft import OutreachDraft
from auto_client_acquisition.gtm_os.records import (
    CompanySignal,
    Prospect,
    Reply,
    SuppressionEntry,
    route_reply,
    score_prospect,
)

DATA = Path(__file__).resolve().parents[1] / "data" / "gtm"


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows):>3} rows -> {path.relative_to(DATA.parents[1])}")


def seed_suppression() -> None:
    rows = [
        SuppressionEntry(recipient_ref="rcpt_supp_001", reason="unsubscribe", source="reply").model_dump(),
        SuppressionEntry(recipient_ref="rcpt_supp_002", reason="bounce", source="mailbox").model_dump(),
        SuppressionEntry(recipient_ref="rcpt_supp_003", reason="complaint", source="reply").model_dump(),
    ]
    _write_jsonl(DATA / "suppression" / "suppression.sample.jsonl", rows)


def seed_signals() -> None:
    rows = [
        CompanySignal(
            signal_id="sig_001", company_label="Riyadh marketing agency (mid)",
            sector="marketing_agencies", signal_type="hiring_sales_ops", source="public_job_board",
            evidence_note="Public job post for a Sales Ops role.", strength="high",
            suggested_offer="revenue_intelligence_sprint",
            suggested_angle_ar="نجهّز طبقة متابعة قبل توظيف Sales Ops.",
            suggested_angle_en="Set up a follow-up layer before the Sales Ops hire.",
        ).model_dump(),
        CompanySignal(
            signal_id="sig_002", company_label="Jeddah dental group (3 branches)",
            sector="clinics", signal_type="new_branch", source="founder_input",
            evidence_note="Founder saw a new-branch announcement.", strength="medium",
            suggested_offer="managed_revenue_ops",
            suggested_angle_ar="استرجاع الحجوزات وتقليل الـ no-shows مع التوسّع.",
            suggested_angle_en="Recover bookings and cut no-shows as you expand.",
        ).model_dump(),
        CompanySignal(
            signal_id="sig_003", company_label="Riyadh real-estate team",
            sector="real_estate", signal_type="new_ad_spend", source="public_post",
            evidence_note="Public campaign launch post.", strength="medium",
            suggested_offer="data_to_revenue_pack",
            suggested_angle_ar="ربط الحملات بمتابعة منظمة للـ viewings.",
            suggested_angle_en="Tie campaigns to an ordered viewings follow-up.",
        ).model_dump(),
    ]
    _write_jsonl(DATA / "signals" / "company_signals.sample.jsonl", rows)


def seed_prospects() -> None:
    s1 = score_prospect(sector_fit=1, buying_signal=1, lead_flow_likelihood=0.8,
                        decision_maker_clarity=0.8, payment_ability=0.7,
                        personalization_signal=1, risk_low=1)
    s2 = score_prospect(sector_fit=0.8, buying_signal=0.6, lead_flow_likelihood=0.6,
                        decision_maker_clarity=0.5, payment_ability=0.6,
                        personalization_signal=0.5, risk_low=1)
    rows = [
        Prospect(
            prospect_ref="acc_ma_017", company_label="Riyadh marketing agency (mid)",
            website_domain="example-agency.sa", sector="marketing_agencies", source="public_job_board",
            signal_ref="sig_001", decision_maker_role="Head of Growth",
            pain_hypothesis="Inbound leads outpace manual follow-up.",
            offer_match="revenue_intelligence_sprint",
            personalization_note="Posted a Sales Ops opening last week.",
            risk_level="low", evidence_level="L2", status="researching",
            next_action="draft_first_touch", score=float(s1["total"]), score_tier=str(s1["tier"]),
        ).model_dump(),
        Prospect(
            prospect_ref="acc_cl_004", company_label="Jeddah dental group (3 branches)",
            website_domain="example-dental.sa", sector="clinics", source="founder_input",
            signal_ref="sig_002", decision_maker_role="Operations Manager",
            pain_hypothesis="Bookings and no-shows leak revenue as branches grow.",
            offer_match="managed_revenue_ops",
            personalization_note="New-branch announcement.",
            risk_level="low", evidence_level="L1", status="new",
            next_action="research", score=float(s2["total"]), score_tier=str(s2["tier"]),
        ).model_dump(),
    ]
    _write_jsonl(DATA / "prospects" / "prospects.sample.jsonl", rows)


def seed_replies() -> None:
    def reply(rid: str, draft_ref: str, prospect_ref: str, classification: str) -> dict:
        r = route_reply(classification)
        return Reply(
            reply_id=rid, draft_ref=draft_ref, prospect_ref=prospect_ref,
            classification=classification, suggested_action=str(r["suggested_action"]),
            requires_suppression=bool(r["requires_suppression"]),
            next_step_ar=str(r["next_step_ar"]), next_step_en=str(r["next_step_en"]),
        ).model_dump()

    rows = [
        reply("rep_001", "d001", "acc_ma_017", "positive"),
        reply("rep_002", "d002", "acc_cl_004", "price_question"),
        reply("rep_003", "d003", "acc_re_009", "unsubscribe"),
    ]
    _write_jsonl(DATA / "replies" / "replies.sample.jsonl", rows)


def _draft(**kw) -> dict:
    base = {
        "region": "Saudi Arabia", "language": "ar_en", "risk_level": "low",
        "unsubscribe_included": True, "offer_matched": True, "evidence_level": "L2",
        "personalization_tier": "P2", "sequence_step": "first_touch",
        "cta": "نراجع 10 حسابات في مكالمة 20 دقيقة؟",
    }
    base.update(kw)
    return OutreachDraft(**base).model_dump()


def seed_drafts() -> None:
    rows = [
        # --- clean drafts (should PASS the gate) ---
        _draft(
            draft_id="d001", prospect_ref="acc_ma_017", company_label="Riyadh marketing agency (mid)",
            sector="marketing_agencies", recipient_role="Head of Growth", recipient_ref="rcpt_ma_017",
            signal_ref="sig_001", pain_hypothesis="Inbound leads outpace manual follow-up.",
            personalization_note="Posted a Sales Ops opening last week.",
            offer="revenue_intelligence_sprint",
            subject="ترتيب متابعة الـ leads قبل توظيف Sales Ops",
            body_ar="لاحظنا إعلانكم لوظيفة Sales Ops. عادةً نرتّب طبقة متابعة منظمة للـ leads قبل التوظيف لتقليل التسرّب، ونجهّز تشخيصًا خلال 7 أيام بأدلة.",
            body_en="Saw your Sales Ops opening. We usually set up an ordered lead follow-up layer first to cut leakage, with a 7-day evidenced diagnostic.",
        ),
        _draft(
            draft_id="d002", prospect_ref="acc_cl_004", company_label="Jeddah dental group (3 branches)",
            sector="clinics", recipient_role="Operations Manager", recipient_ref="rcpt_cl_004",
            signal_ref="sig_002", sequence_step="follow_up_1",
            pain_hypothesis="No-shows and missed bookings leak revenue.",
            personalization_note="New-branch announcement.", offer="managed_revenue_ops",
            subject="استرجاع الحجوزات وتقليل الـ no-shows مع التوسّع",
            body_ar="مع افتتاح الفرع الجديد، نساعد على ترتيب متابعة الحجوزات وتذكيرات منظمة لتقليل الـ no-shows، بقياس واضح.",
            body_en="With the new branch, we help order booking follow-up and reminders to reduce no-shows, with clear measurement.",
        ),
        _draft(
            draft_id="d003", prospect_ref="acc_re_009", company_label="Riyadh real-estate team",
            sector="real_estate", recipient_role="Sales Lead", recipient_ref="rcpt_re_009",
            signal_ref="sig_003", sequence_step="proposal_intro", offer="data_to_revenue_pack",
            pain_hypothesis="Campaign leads and viewings need ordered follow-up.",
            personalization_note="New campaign launch post.",
            subject="ربط حملاتكم بمتابعة منظمة للـ viewings",
            body_ar="نربط حملاتكم الإعلانية بمتابعة منظمة للـ leads و الـ viewings، مع حزمة بيانات أولية لقياس الأثر.",
            body_en="We connect your campaigns to an ordered leads/viewings follow-up, starting with a data pack to measure impact.",
        ),
        # --- violating drafts (should FAIL the gate, each a different reason) ---
        _draft(
            draft_id="d004_missing_unsub", recipient_ref="rcpt_x004", offer="revenue_intelligence_sprint",
            sector="marketing_agencies", subject="فكرة سريعة لمتابعة الـ leads",
            body_ar="فكرة قصيرة لترتيب متابعة الـ leads.", unsubscribe_included=False,
        ),
        _draft(
            draft_id="d005_p0_offer", recipient_ref="rcpt_x005", offer="", offer_matched=False,
            personalization_tier="P0", sector="logistics", subject="خدماتنا",
            body_ar="نقدّم خدمات لتحسين العمليات.",
        ),
        _draft(
            draft_id="d006_fake_reply", recipient_ref="rcpt_x006", offer="revenue_intelligence_sprint",
            sector="clinics", subject="Re: متابعة عرضنا السابق",
            body_ar="نتابع بخصوص ما اتفقنا عليه.",
        ),
        _draft(
            draft_id="d007_spam_subject", recipient_ref="rcpt_x007", offer="data_to_revenue_pack",
            sector="real_estate", subject="100% FREE — ACT NOW $$$",
            body_ar="عرض اليوم فقط.",
        ),
        _draft(
            draft_id="d008_guarantee", recipient_ref="rcpt_x008", offer="managed_revenue_ops",
            sector="training", subject="تحسين التسجيل في الدورات",
            body_ar="نرتّب متابعة استفسارات الدورات.",
            body_en="We guarantee ROI in 30 days for your enrollment funnel.",
        ),
        _draft(
            draft_id="d009_suppressed", recipient_ref="rcpt_supp_001", offer="revenue_intelligence_sprint",
            sector="marketing_agencies", subject="فكرة لمتابعة الـ leads",
            body_ar="فكرة قصيرة لترتيب المتابعة.",
        ),
        _draft(
            draft_id="d010_highrisk_noevidence", recipient_ref="rcpt_x010", offer="custom_ai_setup",
            sector="recruitment", subject="ترتيب متابعة المرشحين والعملاء",
            body_ar="نساعد على ترتيب متابعة المرشحين.", risk_level="high", evidence_level="",
        ),
    ]
    _write_jsonl(DATA / "outreach" / "drafts.sample.jsonl", rows)


def main() -> int:
    seed_suppression()
    seed_signals()
    seed_prospects()
    seed_replies()
    seed_drafts()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
