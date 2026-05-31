"""Offer-level experiments — tied to the growth experiment store."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.growth.experiments import (
    ExperimentStatus,
    GrowthExperiment,
    GrowthExperimentStore,
)


@dataclass
class OfferExperimentLedger:
    """Thin wrapper that scopes growth experiments to a specific offer."""

    store: GrowthExperimentStore

    def propose_for_offer(
        self,
        *,
        offer_id: str,
        title: str,
        hypothesis: str,
        primary_metric: str,
        success_threshold: float,
        kill_rule: str,
    ) -> GrowthExperiment:
        exp = GrowthExperiment(
            title=f"[offer:{offer_id}] {title}",
            hypothesis=hypothesis,
            primary_metric=primary_metric,
            success_threshold=success_threshold,
            kill_rule=kill_rule,
        )
        return self.store.propose(exp)

    def kill(self, experiment_id: str) -> GrowthExperiment:
        return self.store.transition(experiment_id, ExperimentStatus.killed)
