"""
Offer Registry — العروض ككائنات بيانات (ليست نصًا تسويقيًا).

كل offer يحدد: المشتري، الألم، الوعد، التسليمات، السعر، الـ CTA، مخاطر
الثقة، الـ upsell. الـ Readiness Gate يستخدم هذا الـ shape ليتحقق هل
الـ offer جاهز للإطلاق.

Section 48 list:
    revenue_hunter_pilot
    ai_trust_kit
    agency_white_label_kit
    founder_os_setup
    market_radar_report
    proposal_factory_pack
    mcp_risk_review
    evidence_pack_generator
    customer_value_report
    executive_pmo_lite
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import StrEnum


class OfferStatus(StrEnum):
    DRAFT = "draft"
    READY = "ready"
    ACTIVE = "active"
    PAUSED = "paused"
    SUNSET = "sunset"


@dataclass
class Offer:
    offer_id: str
    name: str
    buyer: str
    pain: str
    promise: str
    deliverables: list[str]
    price_min_sar: int
    price_max_sar: int
    entry_cta: str
    upsell: str | None
    trust_risks: list[str] = field(default_factory=list)
    outcome_metric: str | None = None
    delivery_checklist: list[str] = field(default_factory=list)
    proof_hypothesis: str | None = None
    case_study_url: str | None = None
    status: OfferStatus = OfferStatus.DRAFT


# ────────────────────────────────────────────────────────────────
# Default seed offers — Sections 48 + 49.
# Pricing is in SAR, aligned with the rest of the Dealix kernel.
# ────────────────────────────────────────────────────────────────


DEFAULT_OFFERS: tuple[Offer, ...] = (
    Offer(
        offer_id="revenue_hunter_pilot",
        name="Revenue Hunter Pilot",
        buyer="B2B founder / commercial lead targeting Saudi mid-market",
        pain=(
            "صعوبة توليد فرص مؤهلة من ICP محدد ومتابعتها حتى صفقة "
            "موثَّقة"
        ),
        promise=(
            "ICP مُعرَّف، 50 فرصة مؤهلة، 5 مكالمات مبنية على إشارة، "
            "وdraft عروض جاهزة خلال 14 يومًا"
        ),
        deliverables=[
            "ICP one-pager",
            "Qualified lead pack (50)",
            "Pain hypothesis matrix",
            "Outbound message variants",
            "Proposal drafts (5)",
            "Outcome ledger",
        ],
        price_min_sar=2_499,
        price_max_sar=9_999,
        entry_cta="Book Revenue Hunter Diagnostic",
        upsell="Managed Revenue Hunter monthly",
        trust_risks=[
            "overclaim about pipeline outcomes",
            "PII handling for leads",
        ],
        outcome_metric="qualified_calls_booked",
        delivery_checklist=[
            "ICP signed off",
            "Tool registry checked",
            "Pre-flight trust gate run",
            "Outcome ledger created",
        ],
        proof_hypothesis="5 calls booked from a single ICP within 14 days",
        status=OfferStatus.DRAFT,
    ),
    Offer(
        offer_id="ai_trust_kit",
        name="AI Trust Kit",
        buyer="Companies running AI agents internally without controls",
        pain="لا صلاحيات، لا موافقات، لا audit trail، لا kill switch",
        promise=(
            "حوكمة AI داخل الشركة: agent registry، tool permissions، "
            "approval workflow، وevidence pack جاهز"
        ),
        deliverables=[
            "AI use policy (AR + EN)",
            "Agent registry template",
            "Tool permission matrix",
            "Approval workflow blueprint",
            "Evidence pack template",
            "Kill switch SOP",
        ],
        price_min_sar=5_000,
        price_max_sar=25_000,
        entry_cta="Book AI Trust Diagnostic",
        upsell="AI Governance OS monthly retainer",
        trust_risks=[
            "overclaim about regulatory coverage",
            "data privacy boundaries",
            "compliance wording",
        ],
        outcome_metric="controls_in_production",
        delivery_checklist=[
            "Discovery interview",
            "Inventory of existing agents/tools",
            "Permission matrix signed off",
            "Approval workflow live",
            "Evidence pack populated",
        ],
        proof_hypothesis=(
            "Customer can answer a board question on AI usage with a "
            "single evidence pack within 60 minutes"
        ),
        status=OfferStatus.DRAFT,
    ),
    Offer(
        offer_id="agency_white_label_kit",
        name="Agency White-label Kit",
        buyer="Marketing / commercial agencies selling AI to SMBs",
        pain="عدم وجود بنية مُحوكَمة لتقديم AI للعملاء بأمان وقياس",
        promise=(
            "white-label workspace + lead packs + reports جاهزة لإعادة "
            "البيع تحت اسم الوكالة"
        ),
        deliverables=[
            "Partner workspace setup",
            "White-label report template",
            "Lead pack delivery SOP",
            "Revenue share agreement template",
        ],
        price_min_sar=7_500,
        price_max_sar=35_000,
        entry_cta="Book Agency Fit Call",
        upsell="Partner OS monthly + revenue share",
        trust_risks=["false performance claims by sub-agencies"],
        outcome_metric="partner_paid_customers",
        delivery_checklist=[
            "Partner fit score >= 70",
            "Workspace provisioned",
            "First lead pack shipped",
        ],
        proof_hypothesis=(
            "Partner ships a first paid customer within 30 days using the "
            "white-label kit"
        ),
        status=OfferStatus.DRAFT,
    ),
    Offer(
        offer_id="founder_os_setup",
        name="Founder OS Setup",
        buyer="Solo / founder-led commercial operators",
        pain="فوضى تشغيلية: لا توجد مسطرة يومية ولا تتبّع verified للنتائج",
        promise="Founder cockpit + cadence + revenue ledger خلال أسبوع",
        deliverables=[
            "Daily cadence script",
            "Weekly metrics bundle",
            "Verified revenue ledger",
            "Approval inbox",
        ],
        price_min_sar=1_999,
        price_max_sar=4_999,
        entry_cta="Book Founder OS Walkthrough",
        upsell="Founder OS monthly + accountability call",
        trust_risks=["overclaim about pipeline coverage"],
        outcome_metric="founder_daily_loop_streak",
        delivery_checklist=[
            "Cockpit deployed",
            "Daily script run twice in a row",
        ],
        proof_hypothesis="Founder runs the cockpit 5 days in a row without help",
        status=OfferStatus.DRAFT,
    ),
    Offer(
        offer_id="market_radar_report",
        name="Market Radar Report",
        buyer="Sector leaders needing Saudi-specific AI market intelligence",
        pain="غياب تقرير مكثَّف موثوق عن سوق AI في قطاع محدد",
        promise="تقرير قطاعي 20 صفحة + 3 توصيات عملية + قاعدة فرص",
        deliverables=[
            "Sector landscape map",
            "Top 20 opportunity list",
            "Pricing benchmarks",
            "Risk register",
        ],
        price_min_sar=4_999,
        price_max_sar=14_999,
        entry_cta="Request Sector Brief",
        upsell="Quarterly Market Radar subscription",
        trust_risks=["unverified claims about specific companies"],
        outcome_metric="reports_used_in_board_decision",
        delivery_checklist=[
            "Primary sources cited",
            "Trust gate pass",
            "Customer interview included",
        ],
        proof_hypothesis="Customer cites the report in a board decision within 60 days",
        status=OfferStatus.DRAFT,
    ),
    Offer(
        offer_id="proposal_factory_pack",
        name="Proposal Factory Pack",
        buyer="Sales teams losing deals on proposal speed and quality",
        pain="أسبوع لإنتاج عرض، وعروض متذبذبة الجودة",
        promise="مصنع عروض: مراحل، مكتبة، trust check، توقيع",
        deliverables=[
            "Proposal templates (3)",
            "Pricing matrix",
            "Trust check checklist",
            "Signed close-out SOP",
        ],
        price_min_sar=3_499,
        price_max_sar=12_999,
        entry_cta="Book Proposal Audit",
        upsell="Managed Proposal Factory retainer",
        trust_risks=["proposal pricing leakage"],
        outcome_metric="proposal_cycle_days",
        delivery_checklist=["3 templates signed off", "Trust check live"],
        proof_hypothesis="Proposal cycle drops by >= 40% within 30 days",
        status=OfferStatus.DRAFT,
    ),
    Offer(
        offer_id="mcp_risk_review",
        name="MCP Risk Review",
        buyer="Engineering / security leads enabling MCP servers",
        pain="MCP servers تُمكَّن بدون مراجعة سياسات أو صلاحيات",
        promise="مراجعة MCP server خلال 5 أيام: descriptor, scopes, kill switch",
        deliverables=[
            "MCP descriptor audit",
            "Scope matrix",
            "Kill switch SOP",
            "Approved/Blocked decision memo",
        ],
        price_min_sar=4_500,
        price_max_sar=18_000,
        entry_cta="Submit MCP for Review",
        upsell="Quarterly MCP audit subscription",
        trust_risks=["incorrect risk classification"],
        outcome_metric="mcp_servers_reviewed_per_quarter",
        delivery_checklist=["Decision memo signed", "Kill switch tested"],
        proof_hypothesis="Customer enables/blocks MCP within 5 working days",
        status=OfferStatus.DRAFT,
    ),
    Offer(
        offer_id="evidence_pack_generator",
        name="Evidence Pack Generator",
        buyer="Compliance / risk leaders needing board-ready AI evidence",
        pain="جمع الأدلة يستغرق أسابيع وقابل للجدال",
        promise="evidence pack مولَّد من audit log + decisions ledger خلال ساعات",
        deliverables=[
            "Evidence pack template",
            "Generator workflow",
            "Sign-off SOP",
        ],
        price_min_sar=3_500,
        price_max_sar=11_500,
        entry_cta="Run an Evidence Pack",
        upsell="Quarterly evidence cadence retainer",
        trust_risks=["claims without auditable source"],
        outcome_metric="evidence_packs_signed_off",
        delivery_checklist=[
            "Audit log access verified",
            "Sign-off owner identified",
        ],
        proof_hypothesis="First evidence pack signed off within 7 days",
        status=OfferStatus.DRAFT,
    ),
    Offer(
        offer_id="customer_value_report",
        name="Customer Value Report",
        buyer="Customer success teams proving ROI of AI services",
        pain="عميل لا يرى قيمة قابلة للقياس → churn",
        promise="تقرير قيمة شهري يربط الأفعال بالنتائج بالـ revenue",
        deliverables=[
            "Monthly value report template",
            "Outcome ledger SOP",
            "Renewal narrative",
        ],
        price_min_sar=2_999,
        price_max_sar=8_999,
        entry_cta="Request Sample Report",
        upsell="Monthly customer success retainer",
        trust_risks=["inflated outcome metrics"],
        outcome_metric="renewal_rate",
        delivery_checklist=["Outcome ledger live", "First report shipped"],
        proof_hypothesis="Renewal rate rises by >= 10 points in the segment",
        status=OfferStatus.DRAFT,
    ),
    Offer(
        offer_id="executive_pmo_lite",
        name="Executive PMO Lite",
        buyer="C-suite needing weekly disciplined cadence",
        pain="غياب إيقاع تشغيلي يربط القرارات بالنتائج",
        promise="إيقاع أسبوعي 90 دقيقة + لوحة تنفيذية + سجل قرارات",
        deliverables=[
            "Weekly cadence script",
            "Executive dashboard",
            "Decision ledger",
        ],
        price_min_sar=4_999,
        price_max_sar=16_999,
        entry_cta="Book Executive Walkthrough",
        upsell="Monthly Executive PMO retainer",
        trust_risks=["decision attribution misuse"],
        outcome_metric="executive_decisions_with_outcomes",
        delivery_checklist=["Cadence script run twice", "Dashboard live"],
        proof_hypothesis="Executive runs the cadence 3 weeks in a row",
        status=OfferStatus.DRAFT,
    ),
)


class OfferRegistry:
    def __init__(self) -> None:
        self._offers: dict[str, Offer] = {}
        self._lock = threading.Lock()

    def register(self, offer: Offer) -> None:
        with self._lock:
            if offer.offer_id in self._offers:
                raise ValueError(f"offer `{offer.offer_id}` already registered")
            self._offers[offer.offer_id] = offer

    def upsert(self, offer: Offer) -> None:
        with self._lock:
            self._offers[offer.offer_id] = offer

    def get(self, offer_id: str) -> Offer | None:
        with self._lock:
            return self._offers.get(offer_id)

    def all(self) -> list[Offer]:
        with self._lock:
            return list(self._offers.values())

    def active(self) -> list[Offer]:
        with self._lock:
            return [o for o in self._offers.values() if o.status == OfferStatus.ACTIVE]


def default_registry() -> OfferRegistry:
    reg = OfferRegistry()
    for offer in DEFAULT_OFFERS:
        reg.register(offer)
    return reg


__all__ = [
    "DEFAULT_OFFERS",
    "Offer",
    "OfferRegistry",
    "OfferStatus",
    "default_registry",
]
