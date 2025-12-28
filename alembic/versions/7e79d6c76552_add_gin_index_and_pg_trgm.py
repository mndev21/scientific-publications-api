"""add gin index and pg_trgm

Revision ID: 7e79d6c76552
Revises: fc65d2be351a
Create Date: 2025-12-28 16:19:09.303369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = 'add_gin_index_abstract'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.execute("CREATE INDEX ix_publications_abstract_gin ON publications USING gin ((abstract::text) gin_trgm_ops);")

def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_publications_abstract_gin;")
