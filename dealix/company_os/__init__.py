"""Governed Company OS targeting and evaluation capabilities.

Keep package imports limited to the stable targeting surface.  Runtime and
workload-routing adapters are imported from their concrete modules so optional
commercial integrations cannot break the core package at import time.
"""

from dealix.company_os.campaign_planner import build_campaign_plan
from dealix.company_os.capability_evaluation import (
    benchmark_scenarios,
    evaluate_employee_output,
)
from dealix.company_os.company_directory import analyze_company_directory
from dealix.company_os.negotiation_engine import build_negotiation_plan

__all__ = [
    "analyze_company_directory",
    "benchmark_scenarios",
    "build_campaign_plan",
    "build_negotiation_plan",
    "evaluate_employee_output",
]
