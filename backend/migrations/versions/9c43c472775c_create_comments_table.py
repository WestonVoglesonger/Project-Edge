"""Create comments table

Revision ID: 9c43c472775c
Revises: 8c0417242588
Create Date: 2024-06-17 10:42:16.337985

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9c43c472775c'
down_revision = '8c0417242588'
branch_labels = None
depends_on = None


def upgrade():
    # Create comments table
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('description', sa.String(length=1000), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id'), nullable=True),
        sa.Column('discussion_id', sa.Integer, sa.ForeignKey('discussions.id'), nullable=True),
        sa.Column('parent_id', sa.Integer, sa.ForeignKey('comments.id'), nullable=True)
    )

    # Create indexes
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'])
    op.create_index(op.f('ix_comments_user_id'), 'comments', ['user_id'])
    op.create_index(op.f('ix_comments_project_id'), 'comments', ['project_id'])
    op.create_index(op.f('ix_comments_discussion_id'), 'comments', ['discussion_id'])
    op.create_index(op.f('ix_comments_parent_id'), 'comments', ['parent_id'])


def downgrade():
    # Drop indexes
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_user_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_project_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_discussion_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_parent_id'), table_name='comments')
    
    # Drop comments table
    op.drop_table('comments')