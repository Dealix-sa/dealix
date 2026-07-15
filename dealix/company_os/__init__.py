"""Canonical Company OS feature modules.

The daily runner remains the single runtime.  Modules in this package add
capabilities to that runtime without creating a second queue, approval centre,
or proof ledger.
"""

from dealix.company_os.revenue_execution import (
    CompanyRecord,
    build_revenue_execution,
    load_company_records,
)

__all__ = ["CompanyRecord", "build_revenue_execution", "load_company_records"]
from dealix.company_os.workload_router import (
    CompanyWorkloadRequest,
    WorkloadRoute,
    capability_map,
    route_company_workload,
)
from dealix.company_os.capability_evaluation import (
    benchmark_scenarios,
    evaluate_employee_output,
)
from dealix.company_os.campaign_planner import build_campaign_plan
from dealix.company_os.company_directory import analyze_company_directory
from dealix.company_os.negotiation_engine import build_negotiation_plan

__all__ = [
    "CompanyWorkloadRequest",
    "WorkloadRoute",
    "capability_map",
    "route_company_workload",
    "analyze_company_directory",
    "benchmark_scenarios",
    "build_campaign_plan",
    "build_negotiation_plan",
    "evaluate_employee_output",
]
