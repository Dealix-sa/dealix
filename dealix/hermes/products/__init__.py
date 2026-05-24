"""Product Factory — turns any pain into a sellable offer."""

from dealix.hermes.products.experiment import OfferExperiment
from dealix.hermes.products.landing_page_builder import LandingPageBuilder
from dealix.hermes.products.offer_builder import OfferBuilder, OfferCard
from dealix.hermes.products.offer_library import default_offers
from dealix.hermes.products.scale_kill import OfferScaleKill

__all__ = [
    "LandingPageBuilder",
    "OfferBuilder",
    "OfferCard",
    "OfferExperiment",
    "OfferScaleKill",
    "default_offers",
]
