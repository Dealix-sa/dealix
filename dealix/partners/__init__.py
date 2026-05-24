"""خادم الشركاء — Partner workspace engines."""

from __future__ import annotations

__all__: list[str] = []


def _try_export(module: str, names: tuple[str, ...]) -> None:
    try:
        mod = __import__(f"dealix.partners.{module}", fromlist=list(names))
    except Exception:  # pragma: no cover — partial-build safety
        return
    for name in names:
        if hasattr(mod, name):
            globals()[name] = getattr(mod, name)
            if name not in __all__:
                __all__.append(name)


_try_export("scout", ("PartnerCandidate", "PartnerScout"))
_try_export("fit_score", ("PartnerFitResult", "PartnerFitScorer"))
_try_export("pitch", ("PartnerPitchDraft", "PartnerPitchFactory"))
_try_export("onboarding", ("PartnerOnboarding", "PartnerStage", "PartnerRecord"))
_try_export("revenue_share", ("RevenueShareCalculator", "RevenueShareSplit", "PartnerTier"))
_try_export("performance", ("PartnerPerformance", "PartnerPerformanceSnapshot"))
