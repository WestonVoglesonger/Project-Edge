from typing import List
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from backend.models.project import ProjectCreate, ProjectUpdate, ProjectResponse
from backend.entities.user_entity import UserEntity

association_table_current_users = Table(
    'association_current_users', Base.metadata,
    Column('project_id', ForeignKey('projects.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True
)

association_table_owners = Table(
    'association_owners', Base.metadata,
    Column('project_id', ForeignKey('projects.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True
)

class ProjectEntity(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    current_users: Mapped[List[UserEntity]] = relationship('UserEntity', secondary=association_table_current_users, back_populates='projects_as_user')
    owners: Mapped[List[UserEntity]] = relationship('UserEntity', secondary=association_table_owners, back_populates='projects_as_owner')

    def to_project_response(self):
        return ProjectResponse(
            id=self.id,
            name=self.name,
            description=self.description,
            current_users=[user.to_user_response() for user in self.current_users],
            owners=[owner.to_user_response() for owner in self.owners]
        )

    @staticmethod
    def from_model(project: ProjectCreate, current_users: UserEntity, owners: UserEntity):
        return ProjectEntity(
            name=project.name,
            description=project.description,
            current_users=current_users,
            owners=owners
        )
