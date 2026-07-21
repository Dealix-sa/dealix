"""Negotiation & Persuasion Engine.

Bilingual objection handling, persuasion maps, and deal strategy for Saudi B2B
sales. All prices reference the canonical price book only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal

from intelligence.bilingual import BilingualBlock, BilingualRenderer, BilingualText, LanguageCode
from intelligence.ops_adapters import BattlecardsAdapter, PricingAdapter, validate_sku


class ObjectionCategory(str, Enum):
    PRICE = "price"
    TIMING = "timing"
    COMPETITION = "competition"
    TRUST = "trust"
    SCOPE = "scope"
    AUTHORITY = "authority"
    RISK = "risk"


@dataclass
class Objection:
    objection_id: str
    category: ObjectionCategory
    trigger_phrase: BilingualText
    response: BilingualBlock
    evidence_refs: list[str]
    requires_price_reference: bool = False
    price_sku: str | None = None

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "objection_id": self.objection_id,
            "category": self.category.value,
            "trigger_phrase": BilingualRenderer.filter_text(self.trigger_phrase, lang),
            "response": BilingualRenderer.filter_block(self.response, lang),
            "evidence_refs": self.evidence_refs,
            "requires_price_reference": self.requires_price_reference,
            "price_sku": self.price_sku,
        }


@dataclass
class StakeholderInfluence:
    name: str
    role: str
    influence_level: Literal["decision_maker", "influencer", "gatekeeper", "blocker"]
    key_concern: BilingualText

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "influence_level": self.influence_level,
            "key_concern": BilingualRenderer.filter_text(self.key_concern, lang),
        }


@dataclass
class PersuasionMap:
    deal_id: str
    stakeholders: list[StakeholderInfluence]
    value_props: list[BilingualText]
    risk_reversals: list[BilingualText]
    recommended_sequence: list[str]

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "stakeholders": [s.to_dict(lang) for s in self.stakeholders],
            "value_props": [BilingualRenderer.filter_text(v, lang) for v in self.value_props],
            "risk_reversals": [BilingualRenderer.filter_text(r, lang) for r in self.risk_reversals],
            "recommended_sequence": self.recommended_sequence,
        }


@dataclass
class DealStrategy:
    deal_id: str
    company_name: str
    sector: str
    strategy_type: Literal["challenger", "consultative", "relationship", "value"]
    win_themes: list[BilingualText]
    talking_points: list[BilingualBlock]
    objection_playbook: list[Objection]
    pricing_anchor: dict[str, Any]
    close_timeline_days: int
    confidence_percent: float

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "company_name": self.company_name,
            "sector": self.sector,
            "strategy_type": self.strategy_type,
            "win_themes": [BilingualRenderer.filter_text(w, lang) for w in self.win_themes],
            "talking_points": [BilingualRenderer.filter_block(t, lang) for t in self.talking_points],
            "objection_playbook": [o.to_dict(lang) for o in self.objection_playbook],
            "pricing_anchor": self.pricing_anchor,
            "close_timeline_days": self.close_timeline_days,
            "confidence_percent": self.confidence_percent,
        }


class NegotiationEngine:
    """Bilingual negotiation and persuasion engine."""

    def __init__(self) -> None:
        self.pricing = PricingAdapter()
        self.battlecards = BattlecardsAdapter()
        self._objection_library = self._build_objection_library()

    def _build_objection_library(self) -> dict[ObjectionCategory, list[Objection]]:
        return {
            ObjectionCategory.PRICE: [
                Objection(
                    objection_id="price-01",
                    category=ObjectionCategory.PRICE,
                    trigger_phrase=BilingualRenderer.bt(
                        en="Your service is expensive",
                        ar="خدمتكم غالية",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Reframe as investment", ar="إطار الاستثمار"),
                        body=BilingualRenderer.bt(
                            en="Most clients see the fee as an investment once they compare it to the cost of a missed quarter. Let's run the ROI calculation together.",
                            ar="معظم العملاء يرون الرسوم استثمارًا بمجرد مقارنتها بتكلفة ربع فائت. دعنا نحسب العائد معًا.",
                        ),
                    ),
                    evidence_refs=["roi_calculator", "case_studies"],
                    requires_price_reference=True,
                ),
            ],
            ObjectionCategory.TIMING: [
                Objection(
                    objection_id="timing-01",
                    category=ObjectionCategory.TIMING,
                    trigger_phrase=BilingualRenderer.bt(
                        en="We will look at this next quarter",
                        ar="سننظر في هذا الربع القادم",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Cost of delay", ar="تكلفة التأجيل"),
                        body=BilingualRenderer.bt(
                            en="Every month without a scored pipeline costs you leads that your competitors are already converting. A 20-minute diagnostic identifies the exact leakage this quarter.",
                            ar="كل شهر بدون خط أنابيب مُقيّد يكلفكم عملاء محتملين يحوّلها منافسوكم بالفعل. تشخيص 20 دقيقة يحدد التسرب الدقيق هذا الربع.",
                        ),
                    ),
                    evidence_refs=["leakage_diagnostic"],
                ),
            ],
            ObjectionCategory.COMPETITION: [
                Objection(
                    objection_id="competition-01",
                    category=ObjectionCategory.COMPETITION,
                    trigger_phrase=BilingualRenderer.bt(
                        en="We are already using a CRM/AI tool",
                        ar="نستخدم بالفعل أداة CRM/AI",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Layer, not replace", ar="طبقة إضافية لا بديل"),
                        body=BilingualRenderer.bt(
                            en="Dealix does not replace your CRM; it sits on top and turns Saudi market signals into qualified revenue actions with approval-first governance.",
                            ar="Dealix لا تحل محل CRM؛ بل تعمل طبقة فوقه وتحوّل إشارات السوق السعودي إلى إجراءات إيراد مؤهلة مع حوكمة الترخيص أولاً.",
                        ),
                    ),
                    evidence_refs=["integration_map", "pilot_results"],
                ),
            ],
            ObjectionCategory.TRUST: [
                Objection(
                    objection_id="trust-01",
                    category=ObjectionCategory.TRUST,
                    trigger_phrase=BilingualRenderer.bt(
                        en="How do we know this will work for us?",
                        ar="كيف نعرف أن هذا سينجح معنا؟",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Proof before commitment", ar="الإثبات قبل الالتزام"),
                        body=BilingualRenderer.bt(
                            en="We start with a 7-day pilot that documents baseline and improvement. You approve every external action; nothing ships without your sign-off.",
                            ar="نبدأ ببرنامج تجريبي 7 أيام يوثق الأساس والتحسن. توافقون على كل إجراء خارجي؛ لا شيء يُرسل بدون موافقتكم.",
                        ),
                    ),
                    evidence_refs=["pilot_framework", "proof_builder"],
                ),
            ],
            ObjectionCategory.SCOPE: [
                Objection(
                    objection_id="scope-01",
                    category=ObjectionCategory.SCOPE,
                    trigger_phrase=BilingualRenderer.bt(
                        en="This is more than we need right now",
                        ar="هذا أكثر مما نحتاجه الآن",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Modular entry", ar="دخول معياري"),
                        body=BilingualRenderer.bt(
                            en="We can start with the Revenue Diagnostic only. It gives you a full leakage map and a prioritized action plan without committing to the full program.",
                            ar="يمكننا البدء بتشخيص الإيرادات فقط. يمنحكم خريطة تسرب كاملة وخطة عمل مرتبة دون الالتزام بالبرنامج الكامل.",
                        ),
                    ),
                    evidence_refs=["service_catalog"],
                ),
            ],
            ObjectionCategory.AUTHORITY: [
                Objection(
                    objection_id="authority-01",
                    category=ObjectionCategory.AUTHORITY,
                    trigger_phrase=BilingualRenderer.bt(
                        en="I need to check with my manager/CEO",
                        ar="أحتاج للتشاور مع مديري/الرئيس",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Enable the champion", ar="تمكين الشخص المسؤول"),
                        body=BilingualRenderer.bt(
                            en="I will send you a one-page CEO brief in Arabic and English that explains the business case, investment, and pilot structure. You can forward it directly.",
                            ar="سأرسل لك ملخصًا واحدًا للرئيس التنفيذي بالعربية والإنجليزية يشرح الحالة التجارية والاستثمار وهيكل البرنامج التجريبي. يمكنك إعادة توجيهه مباشرة.",
                        ),
                    ),
                    evidence_refs=["ceo_brief_template"],
                ),
            ],
            ObjectionCategory.RISK: [
                Objection(
                    objection_id="risk-01",
                    category=ObjectionCategory.RISK,
                    trigger_phrase=BilingualRenderer.bt(
                        en="What if we do not see results?",
                        ar="ماذا لو لم نر نتائج؟",
                    ),
                    response=BilingualBlock(
                        title=BilingualRenderer.bt(en="Defined success metrics", ar="مؤشرات نجاح محددة"),
                        body=BilingualRenderer.bt(
                            en="The pilot agreement defines measurable success metrics before work starts. If we do not hit them, you only paid the pilot fee and you keep the diagnostic outputs.",
                            ar="اتفاقية البرنامج التجريبي تحدد مؤشرات النجاح القابلة للقياس قبل البدء. إذا لم نحققها، تكونون قد دفعتم رسوم البرنامج فقط وتحتفظون بمخرجات التشخيص.",
                        ),
                    ),
                    evidence_refs=["pilot_sla"],
                ),
            ],
        }

    def list_objections(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return BilingualRenderer.wrap(
            {
                "categories": [c.value for c in ObjectionCategory],
                "objections": [
                    o.to_dict(lang)
                    for category in self._objection_library.values()
                    for o in category
                ],
            },
            lang,
        )

    def handle_objection(
        self,
        category: str,
        context: dict[str, Any] | None = None,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        ctx = context or {}
        try:
            cat = ObjectionCategory(category.lower())
        except ValueError:
            cat = ObjectionCategory.TRUST
        objections = self._objection_library.get(cat, [])
        if not objections:
            objections = self._objection_library[ObjectionCategory.TRUST]
        selected = objections[0]

        # Attach price reference if needed and SKU provided
        if selected.requires_price_reference and selected.price_sku is None:
            package = ctx.get("package_sku") or ctx.get("recommended_package") or "Revenue Diagnostic"
            selected.price_sku = package if validate_sku(package) else None

        return BilingualRenderer.wrap(
            {
                "objection": selected.to_dict(lang),
                "context": ctx,
            },
            lang,
        )

    def build_persuasion_map(
        self,
        deal_id: str,
        stakeholders: list[dict[str, Any]],
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        stakeholder_objs = [
            StakeholderInfluence(
                name=s.get("name", "Unknown"),
                role=s.get("role", "Stakeholder"),
                influence_level=s.get("influence_level", "influencer"),
                key_concern=BilingualRenderer.bt(
                    en=s.get("key_concern_en", "Business outcome"),
                    ar=s.get("key_concern_ar", "النتيجة التجارية"),
                ),
            )
            for s in stakeholders
        ]

        value_props = [
            BilingualRenderer.bt(
                en="Increase qualified pipeline without adding headcount",
                ar="زيادة خط الأنابيب المؤهل دون إضافة موظفين",
            ),
            BilingualRenderer.bt(
                en="Shorten sales cycles with Saudi-specific playbooks",
                ar="تقصير دورات المبيعات بأدلة عمل سعودية محددة",
            ),
            BilingualRenderer.bt(
                en="Reduce revenue leakage through deterministic diagnostics",
                ar="تقليل تسرب الإيرادات من خلال تشخيصات حتمية",
            ),
        ]

        risk_reversals = [
            BilingualRenderer.bt(
                en="Pilot-first entry with documented success metrics",
                ar="دخول عبر برنامج تجريبي مع مؤشرات نجاح موثقة",
            ),
            BilingualRenderer.bt(
                en="Approval-first governance — no surprise commitments",
                ar="حوكمة الترخيص أولاً — لا التزامات مفاجئة",
            ),
        ]

        pmap = PersuasionMap(
            deal_id=deal_id,
            stakeholders=stakeholder_objs,
            value_props=value_props,
            risk_reversals=risk_reversals,
            recommended_sequence=[
                "Map stakeholders and their personal win",
                "Share sector-specific CEO brief",
                "Run diagnostic to create proof",
                "Present pilot proposal with clear success metrics",
                "Gain approval and schedule kickoff",
            ],
        )
        return BilingualRenderer.wrap({"persuasion_map": pmap.to_dict(lang)}, lang)

    def generate_deal_strategy(
        self,
        company_name: str,
        sector: str,
        city: str,
        package_sku: str,
        budget_hint: float | None = None,
        employees: int = 50,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        if not validate_sku(package_sku):
            raise ValueError(f"Package '{package_sku}' is not in the price catalog")

        price = self.pricing.recommend(package_sku, sector, employees, budget_hint=budget_hint)

        strategy_type: Literal["challenger", "consultative", "relationship", "value"] = "consultative"
        if sector.lower() in {"fintech", "healthcare_tech"}:
            strategy_type = "value"
        elif employees <= 50:
            strategy_type = "challenger"

        win_themes = [
            BilingualRenderer.bt(en="Prove ROI in 7 days", ar="إثبات العائد في 7 أيام"),
            BilingualRenderer.bt(en="Saudi-first compliance and language", ar="الامتثال واللغة السعودية أولاً"),
            BilingualRenderer.bt(en="No commitments without approval", ar="لا التزامات بدون موافقة"),
        ]

        talking_points = [
            BilingualBlock(
                title=BilingualRenderer.bt(en="Why now", ar="لماذا الآن"),
                body=BilingualRenderer.bt(
                    en=f"{sector} companies in {city} are moving fast on AI revenue operations. Waiting a quarter means losing scored prospects to competitors.",
                    ar=f"شركات {sector} في {city} تتسارع في عمليات إيرادات AI. انتظار ربع يعني فقدان عملاء مؤهلين للمنافسين.",
                ),
            ),
            BilingualBlock(
                title=BilingualRenderer.bt(en="Why Dealix", ar="لماذا Dealix"),
                body=BilingualRenderer.bt(
                    en="We combine Saudi market intelligence, deterministic workflows, and approval-first governance so your team closes more without adding risk.",
                    ar="نجمع بين ذكاء السوق السعودي وسير العمل الحتمي والحوكمة القائمة على الترخيص أولاً لتقفل المزيد دون إضافة مخاطر.",
                ),
            ),
            BilingualBlock(
                title=BilingualRenderer.bt(en="Investment", ar="الاستثمار"),
                body=BilingualRenderer.bt(
                    en=f"{package_sku} — {price.tier.value} tier at SAR {price.adjusted_price_sar:,.0f}. Payment terms: {price.payment_terms}.",
                    ar=f"{package_sku} — باقة {price.tier.value} بقيمة {price.adjusted_price_sar:,.0f} ريال. شروط الدفع: {price.payment_terms}.",
                ),
            ),
        ]

        playbook = [
            self._objection_library[ObjectionCategory.PRICE][0],
            self._objection_library[ObjectionCategory.TIMING][0],
            self._objection_library[ObjectionCategory.TRUST][0],
        ]

        strategy = DealStrategy(
            deal_id=f"deal-{company_name.lower().replace(' ', '-')}",
            company_name=company_name,
            sector=sector,
            strategy_type=strategy_type,
            win_themes=win_themes,
            talking_points=talking_points,
            objection_playbook=playbook,
            pricing_anchor={
                "sku": package_sku,
                "tier": price.tier.value,
                "base_price_sar": price.base_price_sar,
                "adjusted_price_sar": price.adjusted_price_sar,
                "roi_estimate_percent": price.roi_estimate_percent,
                "payment_terms": price.payment_terms,
            },
            close_timeline_days=21,
            confidence_percent=72.0,
        )
        return BilingualRenderer.wrap({"deal_strategy": strategy.to_dict(lang)}, lang)

    def get_script(
        self,
        scenario: str,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        scripts: dict[str, list[BilingualBlock]] = {
            "discovery_call": [
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Opening", ar="المقدمة"),
                    body=BilingualRenderer.bt(
                        en="Thank you for the time. Before I share anything about Dealix, I would like to understand how your team currently turns a new lead into a paid customer.",
                        ar="شكرًا لوقتكم. قبل أن أشارك أي شيء عن Dealix، أود فهم كيف يحوّل فريقكم العميل المحتمل الجديد إلى عميل مدفوع حاليًا.",
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Pain probe", ar="استكشاف الألم"),
                    body=BilingualRenderer.bt(
                        en="Where do most prospects drop out of your funnel today — and what does that cost per month?",
                        ar="أين يخرج معظم العملاء المحتملين من قمعكم اليوم — وما تكلفة ذلك شهريًا؟",
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Value bridge", ar="جسر القيمة"),
                    body=BilingualRenderer.bt(
                        en="Dealix scores your Saudi prospects, builds proof packs, and keeps every external commitment approval-gated. The goal is more qualified revenue without more risk.",
                        ar="يقوم Dealix بتقييم العملاء السعوديين المحتملين وبناء حزم الإثبات ويحافظ على كل التزام خارجي خاضع للموافقة. الهدف هو المزيد من الإيرادات المؤهلة دون مزيد من المخاطر.",
                    ),
                ),
            ],
            "objection_price": [
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Acknowledge", ar="الإقرار"),
                    body=BilingualRenderer.bt(
                        en="I understand that budget discipline matters, especially now.",
                        ar="أفهم أن انضباط الميزانية مهم، خاصة الآن.",
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Reframe", ar="إعادة الإطار"),
                    body=BilingualRenderer.bt(
                        en="Can we compare the fee to the value of one additional closed customer this quarter?",
                        ar="هل يمكننا مقارنة الرسوم بقيمة عميل إضافي واحد مُقفل هذا الربع؟",
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Offer proof", ar="عرض الإثبات"),
                    body=BilingualRenderer.bt(
                        en="Let us run a 7-day pilot with defined success metrics. You will see the numbers before any larger commitment.",
                        ar="دعنا نُجري برنامجًا تجريبيًا لمدة 7 أيام مع مؤشرات نجاح محددة. سترون الأرقام قبل أي التزام أكبر.",
                    ),
                ),
            ],
            "closing": [
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Summarize", ar="الملخص"),
                    body=BilingualRenderer.bt(
                        en="We agreed the pilot will run for 7 days, measure qualified pipeline growth, and cost SAR 499. You approve every external action.",
                        ar="اتفقنا على أن يعمل البرنامج التجريبي 7 أيام، ويقيس نمو خط الأنابيب المؤهل، ويكلف 499 ريال. توافقون على كل إجراء خارجي.",
                    ),
                ),
                BilingualBlock(
                    title=BilingualRenderer.bt(en="Next step", ar="الخطوة التالية"),
                    body=BilingualRenderer.bt(
                        en="I will send the SOW and kickoff calendar invite within the hour. Which email should I use?",
                        ar="سأرسل بيان نطاق العمل ودعوة تقويم الانطلاق خلال الساعة. ما البريد الذي يجب أن أستخدمه؟",
                    ),
                ),
            ],
        }
        blocks = scripts.get(scenario, scripts["discovery_call"])
        return BilingualRenderer.wrap(
            {
                "scenario": scenario,
                "blocks": [BilingualRenderer.filter_block(b, lang) for b in blocks],
            },
            lang,
        )
