from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

# Association table for many-to-many relationship between users and tags
user_tag_association = Table(
    'user_tag_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)
