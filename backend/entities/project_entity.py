from typing import List
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from backend.models.project import ProjectCreate, ProjectUpdate, ProjectResponse
from backend.entities.user_entity import UserEntity

association_table_team_members = Table(
    'association_team_members', Base.metadata,
    Column('project_id', ForeignKey('projects.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True
)

association_table_project_leaders = Table(
    'association_project_leaders', Base.metadata,
    Column('project_id', ForeignKey('projects.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True
)

class ProjectEntity(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    team_members: Mapped[List[UserEntity]] = relationship('UserEntity', secondary=association_table_team_members, back_populates='projects_as_member')
    project_leaders: Mapped[List[UserEntity]] = relationship('UserEntity', secondary=association_table_project_leaders, back_populates='projects_as_leader')

    comments = relationship("CommentEntity", back_populates="project", cascade="all, delete-orphan")

    def to_project_response(self):
        return ProjectResponse(
            id=self.id,
            name=self.name,
            description=self.description,
            team_members=[member.to_user_response() for member in self.team_members],
            project_leaders=[leader.to_user_response() for leader in self.project_leaders]
        )

    @staticmethod
    def from_model(project: ProjectCreate, team_members: List[UserEntity], project_leaders: List[UserEntity]):
        return ProjectEntity(
            name=project.name,
            description=project.description,
            team_members=team_members,
            project_leaders=project_leaders
        )
