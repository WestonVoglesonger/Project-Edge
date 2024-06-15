"""Add discussions table

Revision ID: 1b1cbd10c22b
Revises: 660774b1923e
Create Date: 2024-06-14 23:07:10.788396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b1cbd10c22b'
down_revision = '660774b1923e'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'discussions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )

    op.create_table(
        'association_discussion_participants',
        sa.Column('discussion_id', sa.Integer, sa.ForeignKey('discussions.id'), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
    )


def downgrade():
    op.drop_table('association_discussion_participants')
    op.drop_table('discussions')