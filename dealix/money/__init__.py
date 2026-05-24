"""خادم المال — Money workspace engines.

Spec §41/§43: dashboards, scouts, hunters, offer match, proposal,
pricing, follow-up and invoice draft. Pure-Python, kernel-friendly.

Re-exports are defensive: modules still being scaffolded in Wave 2 are
imported under try/except so a partial package never breaks app boot
or pytest collection.
"""

from __future__ import annotations

__all__: list[str] = []


def _try_export(module: str, names: tuple[str, ...]) -> None:
    try:
        mod = __import__(f"dealix.money.{module}", fromlist=list(names))
    except Exception:  # pragma: no cover — partial-build safety
        return
    for name in names:
        if hasattr(mod, name):
            globals()[name] = getattr(mod, name)
            if name not in __all__:
                __all__.append(name)


_try_export("cash_scout", ("CashLead", "CashScout"))
_try_export("dashboard", ("MoneyDashboard", "MoneyWeeklySnapshot"))
_try_export("followup", ("FollowUpAction", "FollowUpScheduler"))
_try_export("invoice", ("InvoiceDraft", "InvoiceGenerator"))
_try_export("offer_matcher", ("Offer", "OfferMatcher"))
_try_export("pricing", ("DiscountAdvisory", "PricingEngine"))
_try_export("proposal_factory", ("ProposalDraft", "ProposalFactory"))
_try_export("revenue_hunter", ("RevenueHunter", "TargetAccount"))
