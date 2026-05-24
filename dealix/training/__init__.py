"""خادم التدريب — Training workspace engines."""

from __future__ import annotations

__all__: list[str] = []


def _try_export(module: str, names: tuple[str, ...]) -> None:
    try:
        mod = __import__(f"dealix.training.{module}", fromlist=list(names))
    except Exception:  # pragma: no cover — partial-build safety
        return
    for name in names:
        if hasattr(mod, name):
            globals()[name] = getattr(mod, name)
            if name not in __all__:
                __all__.append(name)


_try_export("workshop_builder", ("WorkshopBuilder", "WorkshopDraft"))
_try_export("material", ("Material", "MaterialLibrary", "MaterialType"))
_try_export("enablement_plan", ("EnablementPlan", "EnablementPlanner"))
