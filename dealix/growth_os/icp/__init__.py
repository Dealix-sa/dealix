"""ICP (Ideal Customer Profile) matrix + scoring."""

from __future__ import annotations

from dealix.growth_os.icp.matrix import ICP_MATRIX, get_icp, list_icps
from dealix.growth_os.icp.scoring import ICPFitScore, score_icp_fit

__all__ = [
    "ICP_MATRIX",
    "ICPFitScore",
    "get_icp",
    "list_icps",
    "score_icp_fit",
]
