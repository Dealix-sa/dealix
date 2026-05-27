"""Training Module — knowledge as product (section 120)."""

from dealix.hermes.training.certification import (
    Certification,
    CertificationLedger,
)
from dealix.hermes.training.enablement_plan import EnablementPlan
from dealix.hermes.training.material import TrainingMaterial, MaterialLibrary
from dealix.hermes.training.prompt_pack import PromptPack, PromptPackLibrary
from dealix.hermes.training.workshop_builder import Workshop, WorkshopBuilder

__all__ = [
    "Certification",
    "CertificationLedger",
    "EnablementPlan",
    "MaterialLibrary",
    "TrainingMaterial",
    "PromptPack",
    "PromptPackLibrary",
    "Workshop",
    "WorkshopBuilder",
]
