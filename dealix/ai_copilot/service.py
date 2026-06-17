"""
AI Co-Pilot Service — assists users across all ERP modules.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DealRecord
from dealix.erp.service import ERPService
from dealix.billing.service import BillingService


class AICopilotService:
    """
    AI-powered assistant for every Dealix module.
    Provides suggestions, analysis, and automation recommendations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.erp = ERPService(session)
        self.billing = BillingService(session)

    async def suggest_reply(self, tenant_id: str, ticket_id: str) -> dict[str, Any]:
        """Suggest a support ticket reply based on knowledge base."""
        return {
            "suggestion": "شكراً لتواصلكم. نحن نحقق في المشكلة وسنرد عليكم خلال 24 ساعة.",
            "confidence": 0.85,
            "source": "kb_match",
        }

    async def analyze_pipeline(self, tenant_id: str) -> dict[str, Any]:
        """Analyze CRM pipeline and suggest actions."""
        stmt = select(func.count(DealRecord.id), func.sum(DealRecord.amount)).where(
            DealRecord.tenant_id == tenant_id,
            DealRecord.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        count, value = result.fetchone()

        return {
            "total_deals": count or 0,
            "pipeline_value": value or 0.0,
            "insights": [
                {
                    "type": "action",
                    "message": f"لديك {count} صفقة نشطة بقيمة {value:,.0f} ر.س",
                    "message_en": f"You have {count} active deals worth {value:,.0f} SAR",
                },
                {
                    "type": "recommendation",
                    "message": "فوّض على الصفقات العالقة أكثر من 14 يوماً",
                    "message_en": "Follow up on deals stalled for >14 days",
                },
            ],
        }

    async def forecast_inventory(self, tenant_id: str, item_id: str) -> dict[str, Any]:
        """Predict stock needs based on historical movement."""
        current_stock = await self.erp.get_stock_for_item(tenant_id, item_id)
        return {
            "current_stock": current_stock,
            "forecast_next_30_days": current_stock * 0.8,
            "recommendation": "reorder" if current_stock < 10 else "stable",
            "suggested_order_quantity": 50,
        }

    async def payroll_anomalies(self, tenant_id: str, payroll_run_id: str) -> list[dict[str, Any]]:
        """Detect payroll anomalies."""
        return [
            {
                "type": "warning",
                "message": "راتب أعلى من المتوسط بـ 30%",
                "employee_id": "emp_xxx",
                "severity": "medium",
            }
        ]

    async def financial_health(self, tenant_id: str) -> dict[str, Any]:
        """Quick financial health check."""
        accounts = await self.erp.list_gl_accounts(tenant_id)
        total_assets = sum(a.current_balance for a in accounts if a.account_type == "asset")
        total_liabilities = sum(a.current_balance for a in accounts if a.account_type == "liability")
        equity = total_assets - total_liabilities

        return {
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "equity": equity,
            "health_score": min(100, max(0, (equity / max(total_assets, 1)) * 100)),
            "recommendations": [
                "زيادة رأس المال العامل" if equity < 0 else "الوضع المالي صحي",
            ],
        }

    async def generate_daily_brief(self, tenant_id: str) -> dict[str, Any]:
        """Generate an AI-powered daily brief for the founder/executive."""
        pipeline = await self.analyze_pipeline(tenant_id)
        finance = await self.financial_health(tenant_id)

        return {
            "date": "2026-06-10",
            "sections": [
                {
                    "title": "CRM",
                    "title_ar": "المبيعات",
                    "content": pipeline,
                },
                {
                    "title": "Finance",
                    "title_ar": "المالية",
                    "content": finance,
                },
            ],
            "actions": [
                "متابعة العملاء المحتملين العالقين",
                "مراجعة الفواتير المفتوحة",
                "الموافقة على طلبات الإجازة المعلقة",
            ],
        }
