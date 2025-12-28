"""add metadata_json and GIN index

Revision ID: 3feecce98303
Revises: a8d5963e425b
Create Date: 2025-12-28 20:10:39.115627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3feecce98303'
down_revision: Union[str, Sequence[str], None] = 'a8d5963e425b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('publications', sa.Column('metadata_json', sa.JSON(), nullable=True))
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
    op.execute('CREATE INDEX IF NOT EXISTS idx_metadata_trgm ON publications USING gin (metadata_json::text gin_trgm_ops);')

def downgrade():
    op.drop_index('idx_metadata_trgm', table_name='publications')
    op.drop_column('publications', 'metadata_json')
