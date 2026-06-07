"""Deterministic company scoring for the Dealix Now engine.

Implements ``os/05_SCORING.yml`` exactly: 8 weighted dimensions summing to a
0-100 total, mapped to tiers (high/medium/nurture/disqualified) with colors
(green/yellow/orange/red) via ``decision_thresholds``.

The demo CSV carries no explicit per-dimension signals, so each dimension's
*level* is derived deterministically from ``sector`` (a documented
``SECTOR_DEFAULTS`` baseline) plus a keyword scan of ``notes`` and the
``relationship_status`` field. The rules were reverse-engineered from the
hand-computed golden sample (``apps/web/public/now-pack.json``) so the six
sample companies land on the same tier.

Pure and deterministic: no network, no API keys, no LLM, no clock reads.
"""

from __future__ import annotations

# ── Dimension weights / per-level score tables (mirror os/05_SCORING.yml) ──
# Each dimension maps an ordered level name to its score. The first level is
# the strongest. ``max_score`` equals the dimension weight.
DIMENSION_LEVELS: dict[str, dict[str, int]] = {
    "operations_complexity": {"high": 20, "medium": 12, "low": 5, "none": 0},
    "reporting_burden": {"high": 15, "medium": 9, "low": 4},
    "maintenance_or_field_ops": {"yes": 20, "partial": 10, "no": 0},
    "multi_branch_or_scale": {"many": 10, "some": 6, "one": 2},
    "operations_data_roles": {"strong": 10, "moderate": 6, "weak": 2},
    "growth_expansion_signals": {"strong": 10, "moderate": 6, "flat": 2},
    "reachable_decision_maker": {"clear": 10, "partial": 6, "unclear": 2},
    "founder_background_fit": {"strong": 5, "moderate": 3, "weak": 1},
}

# Stable dimension order for output (matches golden sample ordering).
DIMENSION_ORDER: tuple[str, ...] = (
    "operations_complexity",
    "reporting_burden",
    "maintenance_or_field_ops",
    "multi_branch_or_scale",
    "operations_data_roles",
    "growth_expansion_signals",
    "reachable_decision_maker",
    "founder_background_fit",
)

# Decision thresholds (os/05_SCORING.yml -> decision_thresholds).
TIER_THRESHOLDS: tuple[tuple[int, str, str, str], ...] = (
    (80, "high", "green", "أولوية عالية — جهّز brief كامل وابدأ draft"),
    (60, "medium", "yellow", "مرشحة — أرسل بعد تخصيص جيد"),
    (40, "nurture", "orange", "ضعها في nurture list — تابع بعد 60 يوم"),
    (0, "disqualified", "red", "أرشفة — لا تستحق الوقت الآن"),
)

# ── Sector baseline levels ────────────────────────────────────────────────
# Documented baseline level per dimension keyed by sector. Note-based bumps
# (below) refine these. Sectors not listed fall back to ``_DEFAULT_BASELINE``.
# Levels here are the *floor*; bumps only ever raise a level, never lower it.
_DEFAULT_BASELINE: dict[str, str] = {
    "operations_complexity": "medium",
    "reporting_burden": "medium",
    "maintenance_or_field_ops": "no",
    "multi_branch_or_scale": "one",
    "operations_data_roles": "moderate",
    "growth_expansion_signals": "moderate",
    "reachable_decision_maker": "partial",
    "founder_background_fit": "weak",
}

SECTOR_DEFAULTS: dict[str, dict[str, str]] = {
    # Operations-heavy logistics: dense daily ops + reporting, partial field ops.
    "logistics": {
        "operations_complexity": "high",
        "reporting_burden": "high",
        "maintenance_or_field_ops": "partial",
        "multi_branch_or_scale": "some",
        "operations_data_roles": "strong",
        "founder_background_fit": "moderate",
    },
    # Engineering / consultancy: project-heavy, partial internal maintenance.
    "engineering": {
        "operations_complexity": "high",
        "reporting_burden": "high",
        "maintenance_or_field_ops": "partial",
        "multi_branch_or_scale": "some",
        "operations_data_roles": "strong",
        "founder_background_fit": "moderate",
    },
    # Contracting / PMO: same project-controls profile as engineering.
    "contracting": {
        "operations_complexity": "high",
        "reporting_burden": "high",
        "maintenance_or_field_ops": "partial",
        "multi_branch_or_scale": "some",
        "operations_data_roles": "strong",
        "founder_background_fit": "moderate",
    },
    # Facilities management / maintenance: full field ops.
    "facilities_management": {
        "operations_complexity": "high",
        "reporting_burden": "high",
        "maintenance_or_field_ops": "yes",
        "multi_branch_or_scale": "some",
        "operations_data_roles": "strong",
        "founder_background_fit": "moderate",
    },
    "maintenance": {
        "operations_complexity": "high",
        "reporting_burden": "high",
        "maintenance_or_field_ops": "yes",
        "multi_branch_or_scale": "some",
        "operations_data_roles": "strong",
        "founder_background_fit": "moderate",
    },
    "industrial": {
        "operations_complexity": "high",
        "reporting_burden": "high",
        "maintenance_or_field_ops": "yes",
        "multi_branch_or_scale": "some",
        "operations_data_roles": "strong",
        "founder_background_fit": "moderate",
    },
    # Healthcare clinics: dense ops + reporting, no field maintenance.
    "healthcare": {
        "operations_complexity": "high",
        "reporting_burden": "high",
        "maintenance_or_field_ops": "no",
        "multi_branch_or_scale": "some",
        "operations_data_roles": "moderate",
        "founder_background_fit": "moderate",
    },
    # Multi-branch hospitality / F&B: ops-heavy, no field maintenance.
    "food_and_beverage": {
        "operations_complexity": "high",
        "reporting_burden": "medium",
        "maintenance_or_field_ops": "no",
        "multi_branch_or_scale": "some",
        "operations_data_roles": "moderate",
        "founder_background_fit": "weak",
    },
    # B2B professional services: moderate ops, strong reachability potential.
    "b2b_services": {
        "operations_complexity": "medium",
        "reporting_burden": "medium",
        "maintenance_or_field_ops": "no",
        "multi_branch_or_scale": "one",
        "operations_data_roles": "moderate",
        "founder_background_fit": "moderate",
    },
    "marketing_agency": {
        "operations_complexity": "medium",
        "reporting_burden": "medium",
        "maintenance_or_field_ops": "no",
        "multi_branch_or_scale": "one",
        "operations_data_roles": "moderate",
        "founder_background_fit": "moderate",
    },
    "training": {
        "operations_complexity": "medium",
        "reporting_burden": "medium",
        "maintenance_or_field_ops": "no",
        "multi_branch_or_scale": "one",
        "operations_data_roles": "moderate",
        "founder_background_fit": "moderate",
    },
    "real_estate": {
        "operations_complexity": "medium",
        "reporting_burden": "medium",
        "maintenance_or_field_ops": "partial",
        "multi_branch_or_scale": "some",
        "operations_data_roles": "moderate",
        "founder_background_fit": "weak",
    },
    # SaaS / technology: moderate ops, weaker founder fit (potential competitor).
    "technology": {
        "operations_complexity": "medium",
        "reporting_burden": "medium",
        "maintenance_or_field_ops": "no",
        "multi_branch_or_scale": "one",
        "operations_data_roles": "moderate",
        "founder_background_fit": "weak",
    },
    "ecommerce": {
        "operations_complexity": "medium",
        "reporting_burden": "medium",
        "maintenance_or_field_ops": "no",
        "multi_branch_or_scale": "one",
        "operations_data_roles": "moderate",
        "founder_background_fit": "weak",
    },
    # Aviation: operations-heavy but outside current ICP focus.
    "aviation": {
        "operations_complexity": "medium",
        "reporting_burden": "medium",
        "maintenance_or_field_ops": "partial",
        "multi_branch_or_scale": "one",
        "operations_data_roles": "moderate",
        "founder_background_fit": "weak",
    },
}

# Human-readable Arabic dimension strengths/weaknesses for top_strengths /
# top_weaknesses surfacing.
_DIMENSION_AR: dict[str, str] = {
    "operations_complexity": "عمليات يومية متكررة وكثيفة",
    "reporting_burden": "عبء تقارير يدوية مرتفع",
    "maintenance_or_field_ops": "صيانة أو عمليات ميدانية",
    "multi_branch_or_scale": "تعدد الفروع أو الحجم",
    "operations_data_roles": "وظائف operations/data واضحة",
    "growth_expansion_signals": "إشارات نمو أو توسع",
    "reachable_decision_maker": "صاحب قرار قابل للوصول",
    "founder_background_fit": "قرب القطاع من خلفية الفاوندر",
}

# Tokens that look like a strong/dense signal in either language.
_KW = {
    "maintenance_high": ("sla", "maintenance", "صيانة", "فنيين", "field", "ميدان"),
    "branches_many": ("multi-branch", "multi branch", "branches", "فروع", "فرع", " 12", "12 "),
    "branches_some": ("two", "فرعين", "مدينتين"),
    "healthcare_pii": ("pii", "pdpl", "patient", "مرضى", "صحي", "عيادات", "clinic"),
    "compliance_urgency": ("zatca", "wave 24", "compliance", "امتثال"),
    "reporting": ("report", "تقارير", "dashboard", "consolidation", "تقرير"),
    "reachable_clear": (
        "diagnostic delivered",
        "diagnostic",
        "paid diagnostic",
        "senior sponsor",
        "sponsor identified",
        "decision maker",
        "managing partner",
    ),
    "revenue_leak": (
        "revenue leak",
        "leakage",
        "losing",
        "loss",
        "follow-up",
        "follow up",
        "no-show",
        "pre-qualification",
        "lead",
        "proposals after demo",
        "تسرّب",
        "متابعة",
    ),
    "growth_strong": (
        "expansion",
        "new contract",
        "hiring",
        "growth",
        "inbound",
        "توسع",
        "نمو",
        "عقود جديدة",
    ),
    "ops_strong_roles": (
        "operations director",
        "operations manager",
        "pmo",
        "data analyst",
        "facilities manager",
        "engineers",
        "مهندس",
    ),
}


def _level_score(dimension: str, level: str) -> int:
    return DIMENSION_LEVELS[dimension].get(level, 0)


def _rank(dimension: str, level: str) -> int:
    """Index of ``level`` in its dimension's ordered level list (0 = strongest)."""
    order = list(DIMENSION_LEVELS[dimension].keys())
    try:
        return order.index(level)
    except ValueError:
        return len(order)


def _raise_to(levels: dict[str, str], dimension: str, target: str) -> None:
    """Raise a dimension level toward ``target`` (never lower it)."""
    current = levels.get(dimension)
    if current is None or _rank(dimension, target) < _rank(dimension, current):
        levels[dimension] = target


def _has(notes: str, group: str) -> bool:
    return any(token in notes for token in _KW[group])


def _derive_levels(target: dict) -> dict[str, str]:
    """Resolve every dimension to a concrete level deterministically."""
    sector = (target.get("sector") or "").strip().lower()
    notes = (target.get("notes") or "").lower()
    status = (target.get("relationship_status") or "").strip().lower()

    levels: dict[str, str] = dict(_DEFAULT_BASELINE)
    levels.update(SECTOR_DEFAULTS.get(sector, {}))

    # ── Note-based bumps (only raise levels) ──
    if _has(notes, "maintenance_high"):
        _raise_to(levels, "maintenance_or_field_ops", "yes")
    if _has(notes, "branches_many"):
        _raise_to(levels, "multi_branch_or_scale", "many")
    elif _has(notes, "branches_some"):
        _raise_to(levels, "multi_branch_or_scale", "some")
    if _has(notes, "reporting"):
        _raise_to(levels, "reporting_burden", "high")
    if _has(notes, "ops_strong_roles"):
        _raise_to(levels, "operations_data_roles", "strong")
    if _has(notes, "growth_strong"):
        _raise_to(levels, "growth_expansion_signals", "moderate")

    # Reachability. reachable=clear requires a concrete reason to believe the
    # decision maker is identified and motivated:
    #   (a) an explicit prior engagement / named sponsor / accessible DM, or
    #   (b) a warm relationship plus a compliance/deadline urgency that creates
    #       a motivated buyer, or
    #   (c) a warm relationship in an owner-led sector (small agencies and
    #       professional-services firms where the partner is the buyer).
    # Otherwise a warm relationship only confirms baseline partial reachability
    # (we have a contact, but not yet a named, qualified decision maker) and a
    # cold relationship stays at the sector baseline. This mirrors the golden
    # sample, where warm-but-cautious rows ("manual review only") stay partial.
    _owner_led = sector in {"marketing_agency", "b2b_services", "training"}
    if _has(notes, "reachable_clear") or (
        status == "warm" and (_has(notes, "compliance_urgency") or _owner_led)
    ):
        _raise_to(levels, "reachable_decision_maker", "clear")
    elif status == "warm":
        _raise_to(levels, "reachable_decision_maker", "partial")

    # A clear prior diagnostic / paid engagement firmly establishes ops roles.
    if _has(notes, "ops_strong_roles") or "diagnostic" in notes:
        _raise_to(levels, "operations_data_roles", "strong")

    return levels


def _tier_for(total: int) -> tuple[str, str, str]:
    for threshold, tier, color, action in TIER_THRESHOLDS:
        if total >= threshold:
            return tier, color, action
    last = TIER_THRESHOLDS[-1]
    return last[1], last[2], last[3]


def score_company(target: dict) -> dict:
    """Score a normalized target dict per ``os/05_SCORING.yml``.

    Returns a dict with: ``total_score`` (0-100), ``tier``, ``tier_color``,
    ``tier_action_ar``, ``dimension_scores`` (list of {id, score, level}),
    ``top_strengths`` and ``top_weaknesses`` (Arabic, derived from the
    highest/lowest scoring dimensions).
    """
    levels = _derive_levels(target)

    dimension_scores: list[dict] = []
    total = 0
    for dim in DIMENSION_ORDER:
        level = levels[dim]
        score = _level_score(dim, level)
        total += score
        dimension_scores.append({"id": dim, "score": score, "level": level})

    total = max(0, min(100, total))
    tier, color, action = _tier_for(total)

    # top_strengths: dimensions at their strongest tier, by score desc.
    strong = sorted(
        (d for d in dimension_scores if _rank(d["id"], d["level"]) == 0),
        key=lambda d: d["score"],
        reverse=True,
    )
    top_strengths = [_DIMENSION_AR[d["id"]] for d in strong[:3]]

    # top_weaknesses: lowest-scoring dimensions (score asc), at most two.
    weak = sorted(dimension_scores, key=lambda d: d["score"])
    top_weaknesses = [
        _DIMENSION_AR[d["id"]]
        for d in weak
        if _rank(d["id"], d["level"]) >= max(1, len(DIMENSION_LEVELS[d["id"]]) - 1)
    ][:2]

    return {
        "total_score": total,
        "tier": tier,
        "tier_color": color,
        "tier_action_ar": action,
        "dimension_scores": dimension_scores,
        "top_strengths": top_strengths,
        "top_weaknesses": top_weaknesses,
    }


__all__ = [
    "DIMENSION_LEVELS",
    "DIMENSION_ORDER",
    "SECTOR_DEFAULTS",
    "TIER_THRESHOLDS",
    "score_company",
]
