"""Product Module — offer factory and lifecycle (section 117)."""

from dealix.hermes.products.experiment import Experiment, ExperimentRegistry
from dealix.hermes.products.landing_page_builder import LandingPage, LandingPageBuilder
from dealix.hermes.products.offer_builder import (
    Offer,
    OfferBuilder,
    OfferLifecycleStatus,
)
from dealix.hermes.products.offer_library import OfferLibrary
from dealix.hermes.products.packaging import OfferPackage, OfferPackager
from dealix.hermes.products.pricing_tiers import PricingTier, PricingTiers
from dealix.hermes.products.scale_kill import OfferScaleKill

__all__ = [
    "Experiment",
    "ExperimentRegistry",
    "LandingPage",
    "LandingPageBuilder",
    "Offer",
    "OfferBuilder",
    "OfferLifecycleStatus",
    "OfferLibrary",
    "OfferPackage",
    "OfferPackager",
    "PricingTier",
    "PricingTiers",
    "OfferScaleKill",
]
