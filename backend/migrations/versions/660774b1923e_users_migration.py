"""Users migration

Revision ID: 660774b1923e
Revises: 94e1941b80f1
Create Date: 2024-06-14 19:52:12.634186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '660774b1923e'
down_revision = '94e1941b80f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('first_name', sa.String, nullable=True),
        sa.Column('last_name', sa.String, nullable=True),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('accepted_community_agreement', sa.Boolean, default=False, nullable=False),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('profile_picture', sa.String, nullable=True),
    )

    # Create the projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
    )

    # Create association table for team members
    op.create_table(
        'association_team_members',
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id'), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
    )

    # Create association table for project leaders
    op.create_table(
        'association_project_leaders',
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id'), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
    )


def downgrade() -> None:
    # Drop association tables first
    op.drop_table('association_project_leaders')
    op.drop_table('association_team_members')

    # Drop projects table
    op.drop_table('projects')

    # Drop users table
    op.drop_table('users')