"""Training Engine — workshops, curricula, enablement."""

from dealix.hermes.training.curriculum import Curriculum, CurriculumModule
from dealix.hermes.training.enablement_plan import EnablementPlan, EnablementStep
from dealix.hermes.training.material import TrainingMaterial
from dealix.hermes.training.prompt_packs import PromptPack, PromptPackLibrary
from dealix.hermes.training.workshop_builder import Workshop, build_workshop

__all__ = [
    "Curriculum",
    "CurriculumModule",
    "EnablementPlan",
    "EnablementStep",
    "PromptPack",
    "PromptPackLibrary",
    "TrainingMaterial",
    "Workshop",
    "build_workshop",
]
