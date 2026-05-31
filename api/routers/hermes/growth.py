"""Growth router — campaigns, leads, experiments."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.routers.hermes._dependencies import get_hermes
from dealix.hermes.growth.campaigns import Campaign, CampaignStore
from dealix.hermes.growth.experiments import GrowthExperiment, GrowthExperimentStore
from dealix.hermes.growth.leads import Lead, LeadStore
from dealix.hermes.orchestrator import HermesOrchestrator


router = APIRouter(prefix="/api/v1/hermes/growth", tags=["hermes-growth"])


# Per-orchestrator stores: kept module-scoped to mirror the kernel.
_campaign_store = CampaignStore()
_lead_store = LeadStore()
_experiment_store = GrowthExperimentStore()


@router.post("/campaigns")
def create_campaign(body: Campaign, orch: HermesOrchestrator = Depends(get_hermes)):
    try:
        return _campaign_store.create(body)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.get("/campaigns")
def list_campaigns():
    return _campaign_store.list()


@router.post("/leads")
def create_lead(body: Lead):
    return _lead_store.add(body)


@router.get("/leads")
def list_leads():
    return _lead_store.list()


@router.post("/experiments")
def propose_experiment(body: GrowthExperiment):
    return _experiment_store.propose(body)


@router.get("/experiments")
def list_experiments():
    return _experiment_store.list()


@router.get("/dashboard")
def dashboard():
    return {
        "campaigns": len(_campaign_store.list()),
        "leads": len(_lead_store.list()),
        "experiments": len(_experiment_store.list()),
    }
