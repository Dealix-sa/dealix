"""
Simplify product for launch — disable non-core modules, update pricing.

Revision ID: 20260610_015_simplify_product_for_launch
Revises: 20260610_014_saas_subscription_billing
Create Date: 2026-06-10 09:45:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20260610_015_simplify_product_for_launch"
down_revision: Union[str, None] = "20260610_014_saas_subscription_billing"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update plans to simplified pricing
    op.execute("DELETE FROM plans WHERE id IN ('plan_free', 'plan_starter', 'plan_growth', 'plan_scale', 'plan_enterprise')")
    op.execute("""
        INSERT INTO plans (id, slug, name_ar, name_en, price_sar_monthly, max_users, max_leads_per_month, max_storage_gb, max_api_calls_per_month, features, sort_order)
        VALUES
        ('plan_free', 'free', 'مجاني', 'Free', 0, 1, 100, 1, 1000, '{\"crm\": true, \"projects\": false, \"support\": false, \"documents\": false, \"hr\": false, \"inventory\": false, \"finance\": false, \"api_access\": false, \"ai_copilot\": false}', 1),
        ('plan_starter', 'starter', 'بداية', 'Starter', 299, 3, 1000, 10, 10000, '{\"crm\": true, \"projects\": true, \"support\": true, \"documents\": false, \"hr\": false, \"inventory\": false, \"finance\": false, \"api_access\": false, \"ai_copilot\": false}', 2),
        ('plan_growth', 'growth', 'نمو', 'Growth', 799, 10, 10000, 50, 50000, '{\"crm\": true, \"projects\": true, \"support\": true, \"documents\": true, \"hr\": true, \"inventory\": true, \"finance\": true, \"api_access\": true, \"ai_copilot\": true}', 3),
        ('plan_enterprise', 'enterprise', 'مؤسسي', 'Enterprise', 0, 9999, 999999, 9999, 9999999, '{\"crm\": true, \"projects\": true, \"support\": true, \"documents\": true, \"hr\": true, \"inventory\": true, \"finance\": true, \"api_access\": true, \"ai_copilot\": true, \"white_label\": true, \"dedicated_support\": true}', 4)
    """)


def downgrade() -> None:
    pass
