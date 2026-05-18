"""Make payments.created_at / updated_at timezone-aware.

Revision ID: 013
Revises: 012
Create Date: 2026-05-18

The application's utcnow() helper returns a timezone-aware datetime
(datetime.now(UTC)). The payments table was created with naive
TIMESTAMP WITHOUT TIME ZONE columns, so asyncpg rejected every INSERT
from the Moyasar webhook ("can't subtract offset-naive and
offset-aware datetimes") and payment rows were silently dropped to the
DLQ. Converting the columns to TIMESTAMP WITH TIME ZONE aligns the
schema with the application default. Existing naive values are
interpreted as UTC.
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
    for column in ("created_at", "updated_at"):
        op.alter_column(
            "payments",
            column,
            type_=sa.DateTime(timezone=True),
            existing_type=sa.DateTime(),
            existing_nullable=False,
            postgresql_using=f"{column} AT TIME ZONE 'UTC'",
        )


def downgrade() -> None:
    for column in ("created_at", "updated_at"):
        op.alter_column(
            "payments",
            column,
            type_=sa.DateTime(),
            existing_type=sa.DateTime(timezone=True),
            existing_nullable=False,
            postgresql_using=f"{column} AT TIME ZONE 'UTC'",
        )
