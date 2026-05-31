"""
Hermes — Dealix's Sovereign Value Control Plane.

طبقات Hermes (Production Architecture v1):

    Control Plane      — السيادة، السياسات، الموافقات، الثقة، الحوكمة، الـ Audit.
    Execution Plane    — الـ Agents، الـ Tools، الـ Workflows، التحقق من المخرجات.
    Intelligence Plane — Signal/Outcome/Revenue/Attribution/Asset Graphs، Learning Engine.
    Workflows          — Revenue Hunt، Proposal، AI Trust Kit، Partner Pitch، Market Radar.
    Products           — Offer Registry، Readiness Gate.
    Growth             — Campaigns، ICP، Content، Attribution، Funnel، Revenue Verification.
    Money              — Revenue Events، Verification، Quality، Attribution، Margin.
    Security           — Prompt Injection Tests، Output Sanitizer، DLP، Sandbox، Red Team.

القواعد الذهبية (تُفرض في الكود وفي الاختبارات، ليست نصًا فقط):

    1.  لا فعل خارجي بلا موافقة (`approval_gate`).
    2.  لا أداة بلا gateway (`tool_gateway`).
    3.  لا مخرج بلا تحقق (`output_validator`).
    4.  لا دخل بلا تحقق (`money.revenue_verification`).
    5.  لا تنفيذ بلا outcome (`intelligence_plane.outcome_graph`).
    6.  لا حملة بلا attribution (`growth.attribution`).

يُستخدم كل شيء فوق Hermes (api routers, agents, workflows, frontends).
Hermes لا يعتمد على أي طبقة فوقه.
"""

from __future__ import annotations

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "contracts",
    "sovereignty",
    "control_plane",
    "execution",
    "intelligence_plane",
    "workflows",
    "products",
    "growth",
    "money",
    "trust",
    "security",
]
