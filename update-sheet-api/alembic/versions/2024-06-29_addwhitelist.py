"""AddWhitelist

Revision ID: a74c0851fd8a
Revises: 7275def126ef
Create Date: 2024-06-29 16:04:10.854706

"""
from typing import List
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = "a74c0851fd8a"
down_revision = "7275def126ef"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("presale", sa.Column("whitelists", sa.ARRAY(sa.String()), nullable=True))

def downgrade():
    op.drop_column("presale", "whitelists")

