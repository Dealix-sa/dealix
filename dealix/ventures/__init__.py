"""خادم المغامرات — Venture workspace engines (spec §35)."""

from __future__ import annotations

__all__: list[str] = []


def _try_export(module: str, names: tuple[str, ...]) -> None:
    try:
        mod = __import__(f"dealix.ventures.{module}", fromlist=list(names))
    except Exception:  # pragma: no cover — partial-build safety
        return
    for name in names:
        if hasattr(mod, name):
            globals()[name] = getattr(mod, name)
            if name not in __all__:
                __all__.append(name)


_try_export("vertical_launcher", ("VerticalCard", "VerticalLauncher"))
_try_export("portfolio", ("VenturePortfolio",))
_try_export("kill_scale", ("VentureKillScale",))
