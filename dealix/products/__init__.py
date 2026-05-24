"""خادم المنتج — Product workspace engines.

Spec §41/§43/§46: offer builder, landing-page drafter, experiment
runner, offer library, scale/kill specialisation. Defensive re-exports
keep the package importable even when an individual module is in flux.
"""

from __future__ import annotations

__all__: list[str] = []


def _try_export(module: str, names: tuple[str, ...]) -> None:
    try:
        mod = __import__(f"dealix.products.{module}", fromlist=list(names))
    except Exception:  # pragma: no cover — partial-build safety
        return
    for name in names:
        if hasattr(mod, name):
            globals()[name] = getattr(mod, name)
            if name not in __all__:
                __all__.append(name)


_try_export("offer_builder", ("OfferBuilder", "OfferBuilderError"))
_try_export("landing_page_builder", ("LandingPageBuilder", "LandingPageDraft"))
_try_export(
    "experiment",
    ("Experiment", "ExperimentRunner", "ExperimentVerdict", "ExperimentStatus"),
)
_try_export("offer_library", ("OfferLibrary",))
_try_export("scale_kill", ("ProductScaleKill",))
