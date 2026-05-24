"""Branded PDF/HTML proposal renderer (Track B.3).

Renders Dealix-branded, bilingual (AR/EN) commercial proposals from a Lead
and a tier name. Pricing is read from the canonical
``dealix/config/pricing.yaml`` file -- never hardcoded. PDF generation
prefers WeasyPrint and falls back to ReportLab if WeasyPrint or its
system libraries are unavailable.

Tiers
-----
- ``mini_sprint``    : Revenue Intelligence Mini Sprint (7 days)
- ``data_pack``      : Curated Data Pack (10 days)
- ``managed_ops``    : Managed Revenue Ops retainer (monthly)
- ``custom_ai``      : Custom AI Workforce build (4-8 weeks)
- ``executive_cc``   : Executive Command Center (quarterly)

Languages
---------
- ``ar``        : Arabic only (RTL)
- ``en``        : English only (LTR)
- ``bilingual`` : two-column AR (right) / EN (left)

Branding
--------
- Deep Green ``#0A4D3F``
- Gold ``#C9A961``
- Sand ``#F4F0E8``
- Footer badges: "PDPL Compliant", "ZATCA Phase 2 Ready"

No PII is logged. Pricing lives in YAML, tiers live in the
``TIER_REGISTRY`` mapping below.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Protocol

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

_LOGGER = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────
# Paths and constants
# ─────────────────────────────────────────────────────────────────────

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_TEMPLATE_DIR = Path(__file__).resolve().parent / "templates" / "proposals"
_DEFAULT_PRICING_YAML = _REPO_ROOT / "dealix" / "config" / "pricing.yaml"

# VAT rate for KSA — 15% (ZATCA standard).
VAT_RATE_KSA: float = 0.15

# Saudi local timezone — Asia/Riyadh is UTC+3, no DST.
_RIYADH_TZ = timezone(timedelta(hours=3))

SUPPORTED_TIERS: tuple[str, ...] = (
    "mini_sprint",
    "data_pack",
    "managed_ops",
    "custom_ai",
    "executive_cc",
)
SUPPORTED_LANGUAGES: tuple[str, ...] = ("ar", "en", "bilingual")

# Western to Arabic-Indic digit translation table.
_AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


# ─────────────────────────────────────────────────────────────────────
# Tier registry — references pricing.yaml keys (no numbers here).
# ─────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TierSpec:
    """Static metadata for a commercial tier."""

    tier_id: str
    pricing_yaml_path: tuple[str, ...]
    duration_days: int
    deliverable_count: int
    title_ar: str
    title_en: str
    summary_ar: str
    summary_en: str
    page_budget: int  # maximum expected PDF pages


TIER_REGISTRY: dict[str, TierSpec] = {
    "mini_sprint": TierSpec(
        tier_id="mini_sprint",
        pricing_yaml_path=("diagnostic", "standard"),
        duration_days=7,
        deliverable_count=5,
        title_ar="Sprint مصغّر — Revenue Intelligence",
        title_en="Mini Sprint — Revenue Intelligence",
        summary_ar=(
            "Sprint محكوم لمدة 7 أيام: Source Passport، Data Quality Score، "
            "نتائج Top-10، و Proof Pack مكوّن من 14 قسم."
        ),
        summary_en=(
            "Governed 7-day sprint: Source Passport, Data Quality Score, "
            "Top-10 account scoring, and a 14-section Proof Pack."
        ),
        page_budget=5,
    ),
    "data_pack": TierSpec(
        tier_id="data_pack",
        pricing_yaml_path=("diagnostic", "executive"),
        duration_days=10,
        deliverable_count=6,
        title_ar="حزمة البيانات المنظّمة — Data Pack",
        title_en="Curated Data Pack",
        summary_ar=(
            "بيانات منظّمة، مُحقّقة المصدر، جاهزة للاستخدام مع لوحة جودة "
            "وبطاقات Source Passport لكل مصدر."
        ),
        summary_en=(
            "Curated, source-validated dataset ready for use, with a data-"
            "quality dashboard and one Source Passport per feed."
        ),
        page_budget=8,
    ),
    "managed_ops": TierSpec(
        tier_id="managed_ops",
        pricing_yaml_path=("retainer", "governed_ops_monthly_min"),
        duration_days=30,
        deliverable_count=8,
        title_ar="عمليات الإيراد المُدارة — Managed Revenue Ops",
        title_en="Managed Revenue Ops",
        summary_ar=(
            "اشتراك شهري لتشغيل خط الإيراد المحكوم: Proof Pack شهري، "
            "Value Ledger، و Adoption Score."
        ),
        summary_en=(
            "Monthly retainer running the governed revenue pipeline: "
            "monthly Proof Pack, Value Ledger, and Adoption Score."
        ),
        page_budget=10,
    ),
    "custom_ai": TierSpec(
        tier_id="custom_ai",
        pricing_yaml_path=("sprint", "revenue_intelligence_from"),
        duration_days=42,
        deliverable_count=10,
        title_ar="بناء فريق ذكاء صناعي مخصّص — Custom AI Workforce",
        title_en="Custom AI Workforce Build",
        summary_ar=(
            "بناء فريق AI محكوم لعملية مختارة، مع Capital Assets قابلة "
            "لإعادة الاستخدام و Governance Runtime."
        ),
        summary_en=(
            "Build a governed AI workforce for one selected workflow, with "
            "reusable Capital Assets and Governance Runtime."
        ),
        page_budget=15,
    ),
    "executive_cc": TierSpec(
        tier_id="executive_cc",
        pricing_yaml_path=("retainer", "governed_ops_monthly_max"),
        duration_days=90,
        deliverable_count=7,
        title_ar="مركز قيادة تنفيذي — Executive Command Center",
        title_en="Executive Command Center",
        summary_ar=(
            "تقرير ربعي للقيادة التنفيذية: مؤشرات الإيراد، حالة الحوكمة، "
            "و Capital Stack."
        ),
        summary_en=(
            "Quarterly executive briefing: revenue indicators, governance "
            "posture, and Capital Stack."
        ),
        page_budget=12,
    ),
}


# ─────────────────────────────────────────────────────────────────────
# Lead protocol — accepts any object with the required shape
# ─────────────────────────────────────────────────────────────────────


class LeadLike(Protocol):
    """Minimum interface a Lead must satisfy for rendering.

    Compatible with ``auto_client_acquisition.revenue_pipeline.lead.Lead``
    and any duck-typed object exposing the same fields.
    """

    id: str
    sector: str
    region: str


@dataclass(frozen=True, slots=True)
class LeadView:
    """PII-free projection of a Lead for the template context.

    Real names / emails / phones are never placed here; only placeholders
    that the human reviewer fills in before sending the PDF.
    """

    lead_id: str
    sector: str
    region: str
    customer_label: str = "[customer_name_placeholder]"
    customer_handle: str = "[customer_handle_placeholder]"

    @classmethod
    def from_lead(
        cls,
        lead: LeadLike,
        *,
        customer_label: str | None = None,
        customer_handle: str | None = None,
    ) -> "LeadView":
        return cls(
            lead_id=lead.id,
            sector=lead.sector,
            region=lead.region,
            customer_label=customer_label or "[customer_name_placeholder]",
            customer_handle=customer_handle or "[customer_handle_placeholder]",
        )


# ─────────────────────────────────────────────────────────────────────
# Pricing helpers
# ─────────────────────────────────────────────────────────────────────


def load_pricing(yaml_path: Path | None = None) -> dict[str, Any]:
    """Load the canonical pricing YAML."""
    path = yaml_path or _DEFAULT_PRICING_YAML
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if "currency" not in data:
        data["currency"] = "SAR"
    return data


def resolve_tier_price(
    tier: str,
    pricing: Mapping[str, Any],
    *,
    custom_pricing: Mapping[str, Any] | None = None,
) -> int:
    """Return the SAR price for a tier, honouring an optional override.

    ``custom_pricing`` may supply ``{"<tier>": <int>}`` to override.
    """
    if custom_pricing and tier in custom_pricing:
        override = custom_pricing[tier]
        if not isinstance(override, int) or override <= 0:
            raise ValueError(f"custom_pricing[{tier!r}] must be a positive int")
        return override
    spec = TIER_REGISTRY[tier]
    cursor: Any = pricing
    for key in spec.pricing_yaml_path:
        if not isinstance(cursor, Mapping) or key not in cursor:
            raise KeyError(
                f"pricing.yaml is missing key path {spec.pricing_yaml_path!r} for tier {tier!r}"
            )
        cursor = cursor[key]
    if not isinstance(cursor, int) or cursor <= 0:
        raise ValueError(
            f"pricing.yaml value at {spec.pricing_yaml_path!r} is not a positive int"
        )
    return cursor


@dataclass(frozen=True, slots=True)
class PriceBreakdown:
    """Subtotal + VAT + total, all in integer SAR (rounded to nearest riyal)."""

    subtotal_sar: int
    vat_sar: int
    total_sar: int
    vat_rate: float = VAT_RATE_KSA

    def as_dict(self) -> dict[str, Any]:
        return {
            "subtotal_sar": self.subtotal_sar,
            "vat_sar": self.vat_sar,
            "total_sar": self.total_sar,
            "vat_rate": self.vat_rate,
            "vat_rate_pct": int(round(self.vat_rate * 100)),
        }


def compute_price_breakdown(subtotal_sar: int, *, vat_rate: float = VAT_RATE_KSA) -> PriceBreakdown:
    """Compute the VAT-inclusive price breakdown (KSA, 15% by default)."""
    if subtotal_sar <= 0:
        raise ValueError("subtotal_sar must be positive")
    vat = int(round(subtotal_sar * vat_rate))
    return PriceBreakdown(
        subtotal_sar=subtotal_sar,
        vat_sar=vat,
        total_sar=subtotal_sar + vat,
        vat_rate=vat_rate,
    )


# ─────────────────────────────────────────────────────────────────────
# Date / number formatting
# ─────────────────────────────────────────────────────────────────────


def format_sar(amount: int, *, language: str) -> str:
    """Format a SAR amount for display. AR uses Arabic-Indic digits."""
    formatted = f"{amount:,}"
    if language == "ar":
        formatted = formatted.translate(_AR_DIGITS)
    return f"{formatted} SAR"


def _gregorian_to_hijri(year: int, month: int, day: int) -> tuple[int, int, int]:
    """Approximate Gregorian -> Hijri conversion (tabular, no external dep).

    Uses the Umm al-Qura-aligned conversion formula (Kuwaiti algorithm).
    Accurate to within +/- 1 day, which is sufficient for proposal headers
    where the Hijri date is shown alongside the Gregorian one.
    """
    jd = (
        int((1461 * (year + 4800 + int((month - 14) / 12))) / 4)
        + int((367 * (month - 2 - 12 * int((month - 14) / 12))) / 12)
        - int((3 * int((year + 4900 + int((month - 14) / 12)) / 100)) / 4)
        + day
        - 32075
    )
    l = jd - 1948440 + 10632
    n = int((l - 1) / 10631)
    l = l - 10631 * n + 354
    j = int((10985 - l) / 5316) * int((50 * l) / 17719) + int(l / 5670) * int(
        (43 * l) / 15238
    )
    l = (
        l
        - int((30 - j) / 15) * int((17719 * j) / 50)
        - int(j / 16) * int((15238 * j) / 43)
        + 29
    )
    h_month = int((24 * l) / 709)
    h_day = l - int((709 * h_month) / 24)
    h_year = 30 * n + j - 30
    return h_year, h_month, h_day


def format_dates(now: datetime | None = None, *, language: str) -> dict[str, str]:
    """Return today's date in Gregorian + Hijri (Riyadh timezone)."""
    now = now or datetime.now(_RIYADH_TZ)
    if now.tzinfo is None:
        now = now.replace(tzinfo=_RIYADH_TZ)
    else:
        now = now.astimezone(_RIYADH_TZ)
    g_str = now.strftime("%Y-%m-%d")
    hy, hm, hd = _gregorian_to_hijri(now.year, now.month, now.day)
    h_str = f"{hy:04d}-{hm:02d}-{hd:02d}"
    if language == "ar":
        g_str = g_str.translate(_AR_DIGITS)
        h_str = h_str.translate(_AR_DIGITS)
    return {"gregorian": g_str, "hijri": h_str}


# ─────────────────────────────────────────────────────────────────────
# Renderer
# ─────────────────────────────────────────────────────────────────────


@dataclass
class RenderContext:
    """Internal context passed to Jinja2 (PII-free)."""

    tier: str
    language: str
    lead: LeadView
    spec: TierSpec
    price: PriceBreakdown
    pricing_meta: dict[str, Any]
    dates: dict[str, str]
    brand: dict[str, str]
    badges: tuple[str, ...] = field(
        default_factory=lambda: ("PDPL Compliant", "ZATCA Phase 2 Ready")
    )

    def as_jinja(self) -> dict[str, Any]:
        return {
            "tier": self.tier,
            "language": self.language,
            "lead": {
                "id": self.lead.lead_id,
                "sector": self.lead.sector,
                "region": self.lead.region,
                "customer_label": self.lead.customer_label,
                "customer_handle": self.lead.customer_handle,
            },
            "spec": {
                "title_ar": self.spec.title_ar,
                "title_en": self.spec.title_en,
                "summary_ar": self.spec.summary_ar,
                "summary_en": self.spec.summary_en,
                "duration_days": self.spec.duration_days,
                "deliverable_count": self.spec.deliverable_count,
                "page_budget": self.spec.page_budget,
            },
            "price": self.price.as_dict(),
            "price_display": {
                "subtotal": format_sar(self.price.subtotal_sar, language=self.language),
                "vat": format_sar(self.price.vat_sar, language=self.language),
                "total": format_sar(self.price.total_sar, language=self.language),
            },
            "pricing_meta": self.pricing_meta,
            "dates": self.dates,
            "brand": self.brand,
            "badges": list(self.badges),
        }


class ProposalRenderer:
    """Renders bilingual Dealix proposals as HTML or PDF."""

    BRAND_COLORS: dict[str, str] = {
        "deep_green": "#0A4D3F",
        "gold": "#C9A961",
        "sand": "#F4F0E8",
        "ink": "#1B2A2F",
        "muted": "#5C6B70",
    }

    def __init__(
        self,
        template_dir: Path | None = None,
        *,
        pricing_yaml: Path | None = None,
    ) -> None:
        self.template_dir = template_dir or _DEFAULT_TEMPLATE_DIR
        if not self.template_dir.exists():
            raise FileNotFoundError(
                f"Proposal template directory not found: {self.template_dir}"
            )
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html", "xml", "j2"]),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self._pricing_yaml = pricing_yaml or _DEFAULT_PRICING_YAML
        self._pricing_cache: dict[str, Any] | None = None

    # ── public API ────────────────────────────────────────────────

    def render_html(
        self,
        *,
        lead: LeadLike,
        tier: str,
        language: str = "ar",
        custom_pricing: Mapping[str, Any] | None = None,
        customer_label: str | None = None,
        customer_handle: str | None = None,
        now: datetime | None = None,
    ) -> str:
        """Render the proposal as HTML (for in-app preview)."""
        ctx = self._build_context(
            lead=lead,
            tier=tier,
            language=language,
            custom_pricing=custom_pricing,
            customer_label=customer_label,
            customer_handle=customer_handle,
            now=now,
        )
        template_name = f"{tier}_{language}.html.j2"
        try:
            template = self.env.get_template(template_name)
        except Exception as exc:
            raise FileNotFoundError(
                f"No proposal template registered for tier={tier!r} language={language!r}: {exc}"
            ) from exc
        return template.render(**ctx.as_jinja())

    def render_pdf(
        self,
        *,
        lead: LeadLike,
        tier: str,
        language: str = "ar",
        custom_pricing: Mapping[str, Any] | None = None,
        customer_label: str | None = None,
        customer_handle: str | None = None,
        now: datetime | None = None,
    ) -> bytes:
        """Render the proposal as a PDF and return its bytes.

        Prefers WeasyPrint. Falls back to a minimal ReportLab-rendered PDF
        if WeasyPrint cannot import or its system libraries are missing.
        Logs the renderer choice (PII-free).
        """
        html = self.render_html(
            lead=lead,
            tier=tier,
            language=language,
            custom_pricing=custom_pricing,
            customer_label=customer_label,
            customer_handle=customer_handle,
            now=now,
        )
        try:
            from weasyprint import HTML  # type: ignore[import-not-found]

            pdf_bytes = HTML(string=html, base_url=str(self.template_dir)).write_pdf()
            _LOGGER.info(
                "proposal_pdf_rendered",
                extra={
                    "tier": tier,
                    "language": language,
                    "engine": "weasyprint",
                    "bytes": len(pdf_bytes),
                },
            )
            return pdf_bytes
        except Exception as exc:  # noqa: BLE001
            _LOGGER.warning(
                "weasyprint_unavailable_falling_back_to_reportlab",
                extra={"tier": tier, "language": language, "error": repr(exc)},
            )

        return self._render_pdf_reportlab(
            tier=tier,
            language=language,
            html=html,
            ctx=self._build_context(
                lead=lead,
                tier=tier,
                language=language,
                custom_pricing=custom_pricing,
                customer_label=customer_label,
                customer_handle=customer_handle,
                now=now,
            ),
        )

    # ── internals ─────────────────────────────────────────────────

    def _pricing(self) -> dict[str, Any]:
        if self._pricing_cache is None:
            self._pricing_cache = load_pricing(self._pricing_yaml)
        return self._pricing_cache

    def _build_context(
        self,
        *,
        lead: LeadLike,
        tier: str,
        language: str,
        custom_pricing: Mapping[str, Any] | None,
        customer_label: str | None,
        customer_handle: str | None,
        now: datetime | None,
    ) -> RenderContext:
        if tier not in TIER_REGISTRY:
            raise ValueError(
                f"Unknown tier {tier!r}; supported: {sorted(TIER_REGISTRY)}"
            )
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unknown language {language!r}; supported: {SUPPORTED_LANGUAGES}"
            )
        spec = TIER_REGISTRY[tier]
        pricing = self._pricing()
        subtotal = resolve_tier_price(tier, pricing, custom_pricing=custom_pricing)
        price = compute_price_breakdown(subtotal)
        view = LeadView.from_lead(
            lead,
            customer_label=customer_label,
            customer_handle=customer_handle,
        )
        return RenderContext(
            tier=tier,
            language=language,
            lead=view,
            spec=spec,
            price=price,
            pricing_meta={
                "currency": pricing.get("currency", "SAR"),
                "source": "dealix/config/pricing.yaml",
            },
            dates=format_dates(now, language=language),
            brand=self.BRAND_COLORS,
        )

    def _render_pdf_reportlab(
        self,
        *,
        tier: str,
        language: str,
        html: str,  # noqa: ARG002  (kept for parity / future text extraction)
        ctx: RenderContext,
    ) -> bytes:
        """Minimal ReportLab fallback — a single-page PDF with the proposal
        title, summary, price table, and PDPL/ZATCA badges."""
        try:
            from io import BytesIO
            from reportlab.lib import colors  # type: ignore[import-not-found]
            from reportlab.lib.pagesizes import A4  # type: ignore[import-not-found]
            from reportlab.lib.styles import (  # type: ignore[import-not-found]
                ParagraphStyle,
                getSampleStyleSheet,
            )
            from reportlab.platypus import (  # type: ignore[import-not-found]
                Paragraph,
                SimpleDocTemplate,
                Spacer,
                Table,
                TableStyle,
            )
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "Neither WeasyPrint nor ReportLab is available; cannot render PDF"
            ) from exc

        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, title="Dealix Proposal")
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "title",
            parent=styles["Title"],
            textColor=colors.HexColor(self.BRAND_COLORS["deep_green"]),
        )
        body_style = styles["BodyText"]
        story: list[Any] = []
        spec = ctx.spec
        if language == "ar":
            story.append(Paragraph(spec.title_ar, title_style))
            story.append(Paragraph(spec.summary_ar, body_style))
        elif language == "en":
            story.append(Paragraph(spec.title_en, title_style))
            story.append(Paragraph(spec.summary_en, body_style))
        else:
            story.append(Paragraph(f"{spec.title_en} / {spec.title_ar}", title_style))
            story.append(Paragraph(spec.summary_en, body_style))
            story.append(Spacer(1, 8))
            story.append(Paragraph(spec.summary_ar, body_style))
        story.append(Spacer(1, 16))
        price = ctx.price
        story.append(
            Table(
                [
                    ["Subtotal (SAR)", f"{price.subtotal_sar:,}"],
                    [f"VAT {int(price.vat_rate * 100)}%", f"{price.vat_sar:,}"],
                    ["Total (SAR)", f"{price.total_sar:,}"],
                ],
                style=TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 2),
                            (-1, 2),
                            colors.HexColor(self.BRAND_COLORS["gold"]),
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor(self.BRAND_COLORS["ink"]),
                        ),
                        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ]
                ),
            )
        )
        story.append(Spacer(1, 16))
        story.append(
            Paragraph(
                " | ".join(ctx.badges)
                + f" — tier={tier} language={language}",
                body_style,
            )
        )
        doc.build(story)
        pdf_bytes = buf.getvalue()
        _LOGGER.info(
            "proposal_pdf_rendered",
            extra={
                "tier": tier,
                "language": language,
                "engine": "reportlab",
                "bytes": len(pdf_bytes),
            },
        )
        return pdf_bytes


# ─────────────────────────────────────────────────────────────────────
# Convenience module-level helpers
# ─────────────────────────────────────────────────────────────────────


def render_proposal_html(
    *,
    lead: LeadLike,
    tier: str,
    language: str = "ar",
    custom_pricing: Mapping[str, Any] | None = None,
    customer_label: str | None = None,
    customer_handle: str | None = None,
) -> str:
    """One-shot HTML render (uses the default template dir)."""
    return ProposalRenderer().render_html(
        lead=lead,
        tier=tier,
        language=language,
        custom_pricing=custom_pricing,
        customer_label=customer_label,
        customer_handle=customer_handle,
    )


def render_proposal_pdf(
    *,
    lead: LeadLike,
    tier: str,
    language: str = "ar",
    custom_pricing: Mapping[str, Any] | None = None,
    customer_label: str | None = None,
    customer_handle: str | None = None,
) -> bytes:
    """One-shot PDF render (uses the default template dir)."""
    return ProposalRenderer().render_pdf(
        lead=lead,
        tier=tier,
        language=language,
        custom_pricing=custom_pricing,
        customer_label=customer_label,
        customer_handle=customer_handle,
    )


__all__ = [
    "VAT_RATE_KSA",
    "SUPPORTED_TIERS",
    "SUPPORTED_LANGUAGES",
    "TIER_REGISTRY",
    "TierSpec",
    "LeadView",
    "LeadLike",
    "PriceBreakdown",
    "ProposalRenderer",
    "compute_price_breakdown",
    "format_dates",
    "format_sar",
    "load_pricing",
    "render_proposal_html",
    "render_proposal_pdf",
    "resolve_tier_price",
]
