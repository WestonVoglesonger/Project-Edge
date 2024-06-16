"""Add discussions table

Revision ID: 8c0417242588
Revises: 7db1c6c31f73
Create Date: 2024-06-15 22:31:44.880831

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8c0417242588'
down_revision = '7db1c6c31f73'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('association_discussion_participants')
    op.drop_table('discussions')
    op.create_table(
        'discussions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    )

    op.create_table(
        'association_discussion_participants',
        sa.Column('discussion_id', sa.Integer, sa.ForeignKey('discussions.id'), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
    )

def downgrade():
    op.drop_table('association_discussion_participants')
    op.drop_table('discussions')