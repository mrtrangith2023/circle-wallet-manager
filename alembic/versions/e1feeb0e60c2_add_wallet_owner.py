"""add wallet owner"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e1feeb0e60c2"
down_revision: Union[str, Sequence[str], None] = "315b3433f5c3"
branch_labels = None
depends_on = None


def upgrade() -> None:

    with op.batch_alter_table("wallets") as batch_op:

        batch_op.add_column(
            sa.Column(
                "owner_id",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.create_foreign_key(
            "fk_wallet_owner",
            "users",
            ["owner_id"],
            ["id"],
        )


def downgrade() -> None:

    with op.batch_alter_table("wallets") as batch_op:

        batch_op.drop_constraint(
            "fk_wallet_owner",
            type_="foreignkey",
        )

        batch_op.drop_column(
            "owner_id",
        )