"""Migration for 6-implement-backend-logic-for-storing-and-retrieving-profile-data

Revision ID: 56a8ef2a2719
Revises: 
Create Date: 2024-05-14 00:28:41.232220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56a8ef2a2719'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True, autoincrement=True),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('accepted_community_agreement', sa.Boolean(), default=False, nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('profile_picture', sa.String(length=255), nullable=True),
        sa.Column('areas_of_interest', sa.String(length=255), nullable=True),
    )

def downgrade() -> None:
    op.drop_table('users')