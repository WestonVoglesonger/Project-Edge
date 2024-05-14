"""Creating tables

Revision ID: ab82a8029ff4
Revises: 
Create Date: 2024-05-14 00:40:03.167902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab82a8029ff4'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Creating the users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('accepted_community_agreement', sa.Boolean(), nullable=False, default=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('profile_picture', sa.String(length=255), nullable=True),
        sa.Column('areas_of_interest', sa.String(length=255), nullable=True),
    )

    # Creating the tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True)
    )

def downgrade() -> None:
    # Dropping the tags table
    op.drop_table('tags')

    # Dropping the users table
    op.drop_table('users')