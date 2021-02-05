"""Add column user_id to Scopes Table

Revision ID: dfefa2691719
Revises: 
Create Date: 2021-02-04 18:55:51.376146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfefa2691719'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("scopes", sa.Column("user_id", sa.Integer))


def downgrade():
    pass
