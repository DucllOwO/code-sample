"""addairdroplist

Revision ID: 76f35b17a926
Revises: a74c0851fd8a
Create Date: 2024-07-09 21:45:29.268926

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = "76f35b17a926"
down_revision = "a74c0851fd8a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "airdrop_list",
        sa.Column('id', UUID(), primary_key=True, server_default=text('gen_random_uuid()')),
        sa.Column('airdrop_id', UUID(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('is_claimed', sa.BOOLEAN(), default=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
    )

    op.create_foreign_key(
        "fk_airdrop_list_airdrop",
        "airdrop_list", "airdrop",
        ["airdrop_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_table("airdrop_list")
