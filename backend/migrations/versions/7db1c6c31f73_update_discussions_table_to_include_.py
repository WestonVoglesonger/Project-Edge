"""Update discussions table to include update time and created time

Revision ID: 7db1c6c31f73
Revises: 1b1cbd10c22b
Create Date: 2024-06-14 23:18:18.461813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7db1c6c31f73'
down_revision = '1b1cbd10c22b'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('association_discussion_participants')
    op.create_table(
        'discussions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    )

    op.create_table(
        'association_discussion_participants',
        sa.Column('discussion_id', sa.Integer(), sa.ForeignKey('discussions.id'), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True)
    )

def downgrade():
    op.drop_table('association_discussion_participants')
    op.drop_table('discussions')