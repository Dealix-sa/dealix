"""proof_revenue_work_units — measurable units of revenue work
جدول وحدات العمل الإيرادي — قياس العمل القابل للإثبات

Revision ID: 013
Revises: 012
Create Date: 2026-05-18

Why
- ``PostgresProofLedger`` (``proof_ledger/postgres_backend.py``) maps a
  ``RevenueWorkUnitORM`` onto the ``proof_revenue_work_units`` table, but
  no migration created that table — the Postgres backend would fail on
  first ``record_unit`` against a real database.
- Each row is one unit of measurable revenue work (opportunity created,
  draft created, approval granted, ...), optionally linked back to a
  ``proof_events`` row via ``proof_event_id`` so the audit chain holds.

Changes
- Create proof_revenue_work_units table (append-only — no UPDATE/DELETE
  in app code).
- Indexes on (tenant_id, customer_handle, created_at) for portal queries
  and on (unit_type) for KPI rollups; index on proof_event_id for the
  proof-chain join.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "013"
down_revision: Union[str, Sequence[str], None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "proof_revenue_work_units",
        sa.Column("unit_id", sa.String(length=64), nullable=False),
        sa.Column("tenant_id", sa.String(length=64), nullable=False, server_default="default"),
        sa.Column("unit_type", sa.String(length=64), nullable=False),
        sa.Column(
            "customer_handle",
            sa.String(length=80),
            nullable=False,
            server_default="Saudi B2B customer",
        ),
        sa.Column("service_id", sa.String(length=64), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("proof_event_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.PrimaryKeyConstraint("unit_id"),
    )
    op.create_index(
        "ix_proof_revenue_work_units_tenant_customer_created",
        "proof_revenue_work_units",
        ["tenant_id", "customer_handle", "created_at"],
    )
    op.create_index(
        "ix_proof_revenue_work_units_type",
        "proof_revenue_work_units",
        ["unit_type"],
    )
    op.create_index(
        "ix_proof_revenue_work_units_proof_event",
        "proof_revenue_work_units",
        ["proof_event_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_proof_revenue_work_units_proof_event",
        table_name="proof_revenue_work_units",
    )
    op.drop_index(
        "ix_proof_revenue_work_units_type",
        table_name="proof_revenue_work_units",
    )
    op.drop_index(
        "ix_proof_revenue_work_units_tenant_customer_created",
        table_name="proof_revenue_work_units",
    )
    op.drop_table("proof_revenue_work_units")
