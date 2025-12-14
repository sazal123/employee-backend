"""add resume title and type fields

Revision ID: abc123def456
Revises: 
Create Date: 2025-12-14 11:01:28

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abc123def456'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('employees', sa.Column('resume_title', sa.String(length=255), nullable=True))
    op.add_column('employees', sa.Column('resume_type', sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column('employees', 'resume_type')
    op.drop_column('employees', 'resume_title')
