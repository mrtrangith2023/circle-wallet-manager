"""add user role

Revision ID: f14828b0d01f
Revises: e1feeb0e60c2
Create Date: 2026-07-15 17:44:55.385070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f14828b0d01f'
down_revision: Union[str, Sequence[str], None] = 'e1feeb0e60c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum(
                "ADMIN",
                "USER",
                name="userrole",
            ),
            nullable=False,
            server_default="USER",
        ),
    )


def downgrade():

    op.drop_column(
        "users",
        "role",
    )
