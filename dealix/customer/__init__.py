"""خادم العميل — Customer workspace engines."""

from __future__ import annotations

__all__: list[str] = []


def _try_export(module: str, names: tuple[str, ...]) -> None:
    try:
        mod = __import__(f"dealix.customer.{module}", fromlist=list(names))
    except Exception:  # pragma: no cover — partial-build safety
        return
    for name in names:
        if hasattr(mod, name):
            globals()[name] = getattr(mod, name)
            if name not in __all__:
                __all__.append(name)


_try_export("health_score", ("CustomerHealth", "CustomerHealthScorer"))
_try_export("value_report", ("MonthlyValueReport", "MonthlyValueReportBuilder"))
_try_export("renewal", ("RenewalAssessment", "RenewalEngine"))
_try_export("upsell", ("UpsellRecommender", "UpsellSuggestion"))
