"""Evidence-first revenue execution planning for the canonical Company OS.

This module turns public company research into an auditable commercial plan:

    verified company -> dossier -> offer -> channel plan -> approval ->
    qualification -> proposal -> negotiation alert -> booking handoff

It deliberately has no network or provider-send function.  A plan can become
eligible for a controlled provider handoff, but the existing approval centre
and connector own the actual external action.  This keeps research, consent,
human approval, and sending as separate facts instead of treating a public
company URL as permission to contact a person.
"""

from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from autonomous_growth.product_catalog import PRODUCT_CATALOG, ProductTier

VERIFIED_STATUSES = frozenset({"verified_public", "verified_warm"})
DRAFT_ALLOWED_DECISIONS = frozenset(
    {"approved_to_draft", "approved_to_send", "founder_approved", "inbound", "warm_intro"}
)
LIVE_REVIEW_DECISIONS = frozenset(
    {"approved_to_send", "founder_approved", "inbound", "warm_intro"}
)
PROPOSAL_ALLOWED_DECISIONS = frozenset(
    {"approved_to_propose", "discovery_completed", "founder_approved"}
)
POSITIVE_REPLY_INTENTS = frozenset(
    {"interested", "send_details", "meeting_request", "qualified", "proposal_requested"}
)
RESTRICTED_COMMITMENTS = (
    "final_price",
    "discount_approval",
    "legal_terms_acceptance",
    "contract_signature",
    "payment_commitment",
    "refund_commitment",
    "guaranteed_roi",
    "guaranteed_revenue",
    "delivery_date_without_capacity_check",
)

_BOOL_TRUE = frozenset({"1", "true", "yes", "y", "approved"})
_VALID_RELATIONSHIPS = frozenset({"unknown", "cold", "warm", "inbound", "customer", "partner"})
_VALID_CONSENT = frozenset({"unknown", "opted_in", "opted_out"})
_URL_RE = re.compile(r"^https?://[^\s]+$", flags=re.IGNORECASE)


def _truthy(value: object) -> bool:
    return str(value or "").strip().lower() in _BOOL_TRUE


def _clean(value: object) -> str:
    return str(value or "").strip()


def _valid_url(value: str) -> bool:
    if not _URL_RE.match(value):
        return False
    parsed = urlparse(value)
    return bool(parsed.scheme in {"http", "https"} and parsed.netloc)


def _account_id(company_name: str, source_url: str) -> str:
    digest = hashlib.sha256(f"{company_name}|{source_url}".encode()).hexdigest()[:12]
    return f"acct-{digest}"


@dataclass(frozen=True, slots=True)
class CompanyRecord:
    """A public organisation record plus explicit, non-inferred permissions."""

    company_name: str
    sector: str
    city: str
    website: str
    source_url: str
    verification_status: str
    owner_decision: str = "research_only_no_outreach"
    contact_present: bool = False
    contact_channel: str = ""
    relationship_status: str = "unknown"
    consent_status: str = "unknown"
    consent_proof_url: str = ""
    approved_template_or_24h_window: bool = False
    human_approved: bool = False
    live_gate: bool = False
    opted_out: bool = False
    messages_sent_this_week: int = 0
    reply_intent: str = ""
    reply_text: str = ""
    qualification_status: str = "unqualified"
    decision_topic: str = ""

    @classmethod
    def from_row(cls, row: dict[str, object]) -> CompanyRecord:
        relationship = _clean(row.get("relationship_status")).lower() or "unknown"
        consent = _clean(row.get("consent_status")).lower() or "unknown"
        try:
            message_count = max(0, int(_clean(row.get("messages_sent_this_week")) or "0"))
        except ValueError:
            message_count = 0
        return cls(
            company_name=_clean(row.get("company_name") or row.get("company")),
            sector=_clean(row.get("sector")).lower(),
            city=_clean(row.get("city")),
            website=_clean(row.get("website")),
            source_url=_clean(row.get("source_url")),
            verification_status=_clean(row.get("verification_status")).lower(),
            owner_decision=_clean(row.get("owner_decision")).lower()
            or "research_only_no_outreach",
            contact_present=_truthy(row.get("contact_present"))
            or bool(_clean(row.get("contact_ref") or row.get("public_contact"))),
            contact_channel=_clean(row.get("contact_channel") or row.get("channel")).lower(),
            relationship_status=(
                relationship if relationship in _VALID_RELATIONSHIPS else "unknown"
            ),
            consent_status=consent if consent in _VALID_CONSENT else "unknown",
            consent_proof_url=_clean(row.get("consent_proof_url")),
            approved_template_or_24h_window=_truthy(
                row.get("approved_template_or_24h_window")
            ),
            human_approved=_truthy(row.get("human_approved")),
            live_gate=_truthy(row.get("live_gate")),
            opted_out=_truthy(row.get("opted_out")) or consent == "opted_out",
            messages_sent_this_week=message_count,
            reply_intent=_clean(row.get("reply_intent")).lower(),
            reply_text=_clean(row.get("reply_text")),
            qualification_status=_clean(row.get("qualification_status")).lower()
            or "unqualified",
            decision_topic=_clean(row.get("decision_topic")).lower(),
        )

    @property
    def account_id(self) -> str:
        return _account_id(self.company_name, self.source_url)

    def validation_issues(self) -> list[str]:
        issues: list[str] = []
        if not self.company_name:
            issues.append("missing_company_name")
        if not _valid_url(self.source_url):
            issues.append("missing_or_invalid_source_url")
        if self.verification_status not in VERIFIED_STATUSES:
            issues.append("unverified_company")
        if self.website and not _valid_url(self.website):
            issues.append("invalid_website")
        return issues


@dataclass(frozen=True, slots=True)
class CompanyDossier:
    account_id: str
    company_name: str
    sector: str
    city: str
    website: str
    source_url: str
    verification_status: str
    evidence_facts: tuple[str, ...]
    pain_hypotheses: tuple[str, ...]
    offer_id: str
    offer_name_ar: str
    fit_score: int
    evidence_level: str


@dataclass(frozen=True, slots=True)
class ChannelAction:
    action_id: str
    account_id: str
    channel: str
    action_type: str
    status: str
    action_mode: str
    can_provider_handoff: bool
    reason: str
    required_conditions: tuple[str, ...]
    subject: str = ""
    draft_body: str = ""


@dataclass(frozen=True, slots=True)
class DecisionAlert:
    alert_id: str
    account_id: str
    topic: str
    risk_level: str
    decision_needed: str
    recommended_safe_action: str
    restricted_commitments: tuple[str, ...] = field(default_factory=lambda: RESTRICTED_COMMITMENTS)


def load_company_records(path: Path, *, limit: int = 50) -> list[CompanyRecord]:
    """Load organisation research without accepting or emitting a contact value."""
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [CompanyRecord.from_row(row) for row in rows[: max(1, limit)]]


def _pain_hypotheses(record: CompanyRecord) -> tuple[str, ...]:
    by_sector: dict[str, tuple[str, ...]] = {
        "marketing_agency": (
            "فرضية تحتاج تحقق: قد تتوزع الفرص والمتابعات بين الإعلانات والبريد والمحادثات.",
            "فرضية تحتاج تحقق: قد يستغرق إعداد إثبات النتائج والتقارير للعملاء وقتاً يدوياً.",
        ),
        "crm_partner": (
            "فرضية تحتاج تحقق: قد تحتاج فرص الشراكات والتنفيذ المشترك إلى تأهيل ومسار متابعة موحد.",
            "فرضية تحتاج تحقق: قد تكون رؤية المبيعات والتسليم موزعة بين أكثر من نظام.",
        ),
        "training": (
            "فرضية تحتاج تحقق: قد تتسرب متابعات التسجيلات والشركات بين الحملات وفريق المبيعات.",
        ),
        "clinic": (
            "فرضية تحتاج تحقق: قد تتوزع الاستفسارات التشغيلية بين الهاتف والنماذج والمحادثات.",
        ),
    }
    return by_sector.get(
        record.sector,
        (
            "فرضية تحتاج تحقق: قد توجد فرصة لتوحيد بيانات الفرص والمتابعات والقرارات في مسار واحد.",
        ),
    )


def _offer(record: CompanyRecord) -> tuple[str, str]:
    # Research-stage companies always start with the lowest-commitment catalog
    # product.  Higher rungs require qualification and verified customer data.
    product = PRODUCT_CATALOG[ProductTier.FREE_DIAGNOSTIC]
    return product.id, product.name_ar


def build_dossier(record: CompanyRecord) -> CompanyDossier:
    facts = [f"اسم الشركة: {record.company_name}"]
    if record.sector:
        facts.append(f"القطاع المسجل: {record.sector}")
    if record.city:
        facts.append(f"الموقع المسجل: {record.city}")
    facts.append(f"المصدر العام: {record.source_url}")

    score = 0
    score += 40 if _valid_url(record.source_url) else 0
    score += 25 if record.verification_status in VERIFIED_STATUSES else 0
    score += 10 if record.website.startswith("https://") else 0
    score += 10 if record.sector else 0
    score += 5 if record.city else 0
    score += 5 if record.contact_present else 0
    score += 5 if record.relationship_status in {"warm", "inbound", "customer", "partner"} else 0
    offer_id, offer_name = _offer(record)
    return CompanyDossier(
        account_id=record.account_id,
        company_name=record.company_name,
        sector=record.sector or "unknown",
        city=record.city,
        website=record.website,
        source_url=record.source_url,
        verification_status=record.verification_status,
        evidence_facts=tuple(facts),
        pain_hypotheses=_pain_hypotheses(record),
        offer_id=offer_id,
        offer_name_ar=offer_name,
        fit_score=min(score, 100),
        evidence_level="L1_public_research",
    )


def _draft_preview(record: CompanyRecord, dossier: CompanyDossier, channel: str) -> tuple[str, str]:
    subject = f"{record.company_name} — فكرة تشغيلية أولية"
    body = (
        f"السلام عليكم فريق {record.company_name}،\n\n"
        f"اطلعت على المعلومات العامة المنشورة عن نشاطكم في قطاع {dossier.sector}. "
        f"لدينا فرضية أولية تحتاج تحقق: {dossier.pain_hypotheses[0]}\n\n"
        f"يمكن أن نبدأ بـ {dossier.offer_name_ar} لفهم الوضع الحالي وتحديد فرصة عملية "
        "واحدة قبل اقتراح أي نطاق أو التزام. هذه ليست نتيجة مؤكدة، بل نقطة بداية "
        "تحتاج تحققاً مع فريقكم.\n\n"
        "هل يناسبكم ملخص قصير أو جلسة تشخيص؟\n\n"
        "إذا لم ترغبوا في المتابعة، أخبرونا وسنوقف التواصل."
    )
    if channel == "linkedin":
        body = (
            f"مرحباً، اطلعت على المعلومات العامة عن {record.company_name}. لدي فرضية "
            f"تشغيلية أولية تحتاج تحقق حول {dossier.pain_hypotheses[0]} "
            f"هل يناسبكم ملخص قصير عن {dossier.offer_name_ar}؟"
        )
    return subject, body


def _email_action(record: CompanyRecord, dossier: CompanyDossier) -> ChannelAction:
    subject, body = _draft_preview(record, dossier, "email")
    issues = record.validation_issues()
    if issues:
        return ChannelAction(
            f"act-{record.account_id}-email",
            record.account_id,
            "email",
            "draft_email",
            "blocked",
            "blocked",
            False,
            "Company evidence failed validation.",
            tuple(issues),
        )
    if record.opted_out:
        return ChannelAction(
            f"act-{record.account_id}-email",
            record.account_id,
            "email",
            "draft_email",
            "blocked",
            "blocked",
            False,
            "Recipient is suppressed or opted out.",
            ("remove_from_all_outbound_queues",),
        )

    draft_authorized = record.owner_decision in DRAFT_ALLOWED_DECISIONS
    required = []
    if not draft_authorized:
        required.append("target_level_owner_decision")
    if not record.contact_present:
        required.append("approved_business_contact")
    if record.contact_channel not in {"", "email"}:
        required.append("email_contact_channel")

    handoff_missing = list(required)
    if record.owner_decision not in LIVE_REVIEW_DECISIONS:
        handoff_missing.append("approved_to_send")
    if not record.live_gate:
        handoff_missing.append("live_gate")
    if not record.human_approved:
        handoff_missing.append("human_approval")
    if record.consent_status != "opted_in" or not _valid_url(record.consent_proof_url):
        handoff_missing.append("lawful_basis_or_consent_proof")
    if record.messages_sent_this_week >= 2:
        handoff_missing.append("frequency_cap")

    can_handoff = not handoff_missing
    status = "pending_human_approval" if draft_authorized else "research_preview"
    return ChannelAction(
        f"act-{record.account_id}-email",
        record.account_id,
        "email",
        "draft_email",
        "approved_provider_handoff" if can_handoff else status,
        "controlled_handoff" if can_handoff else "draft_only",
        can_handoff,
        (
            "All target-level gates are satisfied; connector handoff is eligible and remains audited."
            if can_handoff
            else "Draft preview only; public company research is not contact permission."
        ),
        tuple(dict.fromkeys(handoff_missing)),
        subject,
        body,
    )


def _linkedin_action(record: CompanyRecord, dossier: CompanyDossier) -> ChannelAction:
    subject, body = _draft_preview(record, dossier, "linkedin")
    if record.validation_issues() or record.opted_out:
        return ChannelAction(
            f"act-{record.account_id}-linkedin",
            record.account_id,
            "linkedin",
            "draft_linkedin_manual",
            "blocked",
            "blocked",
            False,
            "Invalid evidence or suppression state.",
            tuple(record.validation_issues() or ["opted_out"]),
        )
    authorized = record.owner_decision in DRAFT_ALLOWED_DECISIONS
    missing = []
    if not authorized:
        missing.append("target_level_owner_decision")
    if not record.contact_present or record.contact_channel != "linkedin":
        missing.append("known_profile_or_business_contact")
    missing.append("human_final_send_required")
    return ChannelAction(
        f"act-{record.account_id}-linkedin",
        record.account_id,
        "linkedin",
        "draft_linkedin_manual",
        "pending_manual_review" if authorized else "research_preview",
        "approved_manual" if authorized else "draft_only",
        False,
        "LinkedIn automation and scraping are never eligible; a person performs the final send.",
        tuple(missing),
        subject,
        body,
    )


def _whatsapp_action(record: CompanyRecord) -> ChannelAction:
    missing: list[str] = []
    if record.relationship_status not in {"warm", "inbound", "customer", "partner"}:
        missing.append("existing_relationship_or_inbound")
    if record.consent_status != "opted_in" or not _valid_url(record.consent_proof_url):
        missing.append("verified_whatsapp_opt_in")
    if not record.approved_template_or_24h_window:
        missing.append("approved_template_or_24h_window")
    if not record.contact_present or record.contact_channel != "whatsapp":
        missing.append("approved_whatsapp_contact")
    if not record.live_gate:
        missing.append("live_gate")
    if not record.human_approved:
        missing.append("human_approval")
    if record.owner_decision not in LIVE_REVIEW_DECISIONS:
        missing.append("target_level_send_approval")
    if record.messages_sent_this_week >= 2:
        missing.append("frequency_cap")
    if record.opted_out:
        missing.append("opted_out")

    eligible = not missing
    return ChannelAction(
        f"act-{record.account_id}-whatsapp",
        record.account_id,
        "whatsapp",
        "approved_whatsapp_template",
        "approved_manual_handoff" if eligible else "blocked",
        "controlled_handoff" if eligible else "blocked",
        eligible,
        (
            "Opt-in, relationship, template/window, target approval, and live gates are verified."
            if eligible
            else "Cold WhatsApp, purchased lists, and broadcasts are blocked."
        ),
        tuple(dict.fromkeys(missing)),
    )


def _call_action(record: CompanyRecord) -> ChannelAction:
    missing: list[str] = []
    if record.relationship_status not in {"warm", "inbound", "customer", "partner"}:
        missing.append("customer_permission_or_existing_relationship")
    if not record.contact_present or record.contact_channel not in {"phone", "calls"}:
        missing.append("approved_phone_contact")
    if not record.live_gate:
        missing.append("live_gate")
    if not record.human_approved:
        missing.append("human_approval")
    if record.opted_out:
        missing.append("opted_out")
    eligible = not missing
    return ChannelAction(
        f"act-{record.account_id}-call",
        record.account_id,
        "calls",
        "call_script",
        "approved_manual_handoff" if eligible else "blocked",
        "approved_manual" if eligible else "blocked",
        eligible,
        "Calls are manual and require customer permission plus target-level approval.",
        tuple(dict.fromkeys(missing)),
    )


def _decision_alerts(record: CompanyRecord) -> list[DecisionAlert]:
    text = f"{record.decision_topic} {record.reply_intent} {record.reply_text}".lower()
    rules: tuple[tuple[str, tuple[str, ...], str, str], ...] = (
        (
            "pricing_or_discount",
            ("price", "pricing", "discount", "budget", "سعر", "خصم", "ميزانية", "غالي"),
            "اعتماد نطاق/سعر أو رفض الخصم؛ النظام لا يلتزم بسعر نهائي.",
            "قدّم خيار Pilot أصغر أو نطاقاً مرحلياً دون اعتماد خصم تلقائي.",
        ),
        (
            "legal_or_contract",
            ("contract", "legal", "terms", "عقد", "قانون", "شروط"),
            "مراجعة الشروط القانونية وصلاحية التوقيع.",
            "حوّل الطلب للمسؤول القانوني/المؤسس مع ملخص غير ملزم.",
        ),
        (
            "payment_or_refund",
            ("payment", "invoice", "refund", "دفع", "فاتورة", "استرداد"),
            "اعتماد التزام الدفع أو الاسترداد أو شروط الفاتورة.",
            "جهّز handoff مالي فقط؛ لا تحصّل ولا تعد باسترداد تلقائياً.",
        ),
        (
            "guarantee_request",
            ("guarantee", "guaranteed", "ضمان", "مضمون"),
            "رفض أي ضمان إيراد/عائد وتحديد صياغة واقعية قابلة للقياس.",
            "استبدل الضمان بمؤشرات تجربة وطريقة قياس وإثبات فعلي.",
        ),
    )
    alerts: list[DecisionAlert] = []
    for topic, keywords, decision_needed, safe_action in rules:
        if any(keyword in text for keyword in keywords):
            alerts.append(
                DecisionAlert(
                    alert_id=f"alert-{record.account_id}-{topic}",
                    account_id=record.account_id,
                    topic=topic,
                    risk_level="high",
                    decision_needed=decision_needed,
                    recommended_safe_action=safe_action,
                )
            )
    return alerts


def _qualification(record: CompanyRecord) -> dict[str, Any]:
    qualified = record.qualification_status in {"qualified", "discovery_completed"}
    positive = record.reply_intent in POSITIVE_REPLY_INTENTS
    return {
        "status": "qualified" if qualified else "needs_discovery" if positive else "not_started",
        "questions": [
            {"dimension": "need", "question_ar": "ما المشكلة التشغيلية الأهم التي تريدون حلها الآن؟"},
            {"dimension": "authority", "question_ar": "من يشارك في قرار اعتماد التجربة؟"},
            {"dimension": "budget", "question_ar": "ما النطاق التقريبي المتاح للتجربة؟"},
            {"dimension": "timeline", "question_ar": "متى تريدون بدء أول تجربة قابلة للقياس؟"},
        ],
    }


def _proposal_and_booking(record: CompanyRecord, dossier: CompanyDossier) -> tuple[dict[str, Any], dict[str, Any]]:
    qualified = record.qualification_status in {"qualified", "discovery_completed"}
    proposal_ready = qualified and record.owner_decision in PROPOSAL_ALLOWED_DECISIONS
    booking_ready = (
        record.reply_intent in POSITIVE_REPLY_INTENTS
        and record.contact_present
        and record.human_approved
        and not record.opted_out
    )
    proposal = {
        "status": "ready_for_founder_review" if proposal_ready else "blocked_until_qualified",
        "offer_id": dossier.offer_id,
        "offer_name_ar": dossier.offer_name_ar,
        "required_conditions": []
        if proposal_ready
        else ["qualification_completed", "approved_to_propose", "scope_and_out_of_scope"],
        "final_price_commitment": False,
    }
    booking = {
        "status": "ready_for_calendar_handoff" if booking_ready else "blocked_until_positive_intent",
        "provider_write_performed": False,
        "required_conditions": []
        if booking_ready
        else ["positive_reply", "approved_contact", "human_approval"],
    }
    return proposal, booking


def build_revenue_case(record: CompanyRecord) -> dict[str, Any]:
    dossier = build_dossier(record)
    actions = [
        _email_action(record, dossier),
        _linkedin_action(record, dossier),
        _whatsapp_action(record),
        _call_action(record),
    ]
    alerts = _decision_alerts(record)
    proposal, booking = _proposal_and_booking(record, dossier)
    if record.validation_issues():
        next_action = "صحح المصدر والتحقق قبل إدخال الشركة في أي مسار تجاري."
    elif alerts:
        next_action = "قرار بشري مطلوب قبل متابعة التفاوض أو الالتزام التجاري."
    elif record.owner_decision == "research_only_no_outreach":
        next_action = "راجع الفرضيات، ثم اعتمد شركة واحدة فقط للمسودة إذا وُجد مسار دافئ أو وارد."
    elif record.reply_intent in POSITIVE_REPLY_INTENTS:
        next_action = "أكمل التأهيل ثم جهّز الحجز أو العرض حسب النتيجة."
    else:
        next_action = "راجع مسودة البريد/LinkedIn يدوياً؛ لا يوجد إرسال تلقائي."

    return {
        "account_id": record.account_id,
        "company_name": record.company_name,
        "owner_decision": record.owner_decision,
        "dossier": asdict(dossier),
        "channel_plan": [asdict(action) for action in actions],
        "qualification": _qualification(record),
        "proposal": proposal,
        "booking": booking,
        "decision_alerts": [asdict(alert) for alert in alerts],
        "next_best_action": next_action,
    }


def build_revenue_execution(records: Iterable[CompanyRecord]) -> dict[str, Any]:
    cases = [build_revenue_case(record) for record in records]
    actions = [action for case in cases for action in case["channel_plan"]]
    alerts = [alert for case in cases for alert in case["decision_alerts"]]
    return {
        "summary": {
            "companies": len(cases),
            "verified_companies": sum(
                case["dossier"]["verification_status"] in VERIFIED_STATUSES for case in cases
            ),
            "research_only": sum(
                case["owner_decision"] == "research_only_no_outreach" for case in cases
            ),
            "draft_previews": sum(
                action["status"] in {"research_preview", "pending_human_approval", "pending_manual_review"}
                for action in actions
            ),
            "provider_handoffs_eligible": sum(action["can_provider_handoff"] for action in actions),
            "proposals_ready": sum(
                case["proposal"]["status"] == "ready_for_founder_review" for case in cases
            ),
            "bookings_ready": sum(
                case["booking"]["status"] == "ready_for_calendar_handoff" for case in cases
            ),
            "decision_alerts": len(alerts),
            "external_actions_performed": 0,
        },
        "cases": cases,
        "decision_alerts": alerts,
        "policy": {
            "public_research_is_not_consent": True,
            "no_cold_whatsapp": True,
            "no_linkedin_automation_or_scraping": True,
            "target_level_approval_required": True,
            "suppression_and_frequency_cap_required": True,
            "actual_send_owned_by_existing_connector": True,
        },
    }


__all__ = [
    "ChannelAction",
    "CompanyDossier",
    "CompanyRecord",
    "DecisionAlert",
    "build_dossier",
    "build_revenue_case",
    "build_revenue_execution",
    "load_company_records",
]
