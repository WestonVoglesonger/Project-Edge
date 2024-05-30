from typing import Dict, List
from pytest import Session
from sqlalchemy.exc import IntegrityError
from backend.entities.project_entity import ProjectEntity
from backend.entities.user_entity import UserEntity
from backend.models.project import Project, ProjectCreate, ProjectResponse, ProjectUpdate
from backend.models.user import User, UserResponse
from backend.services.exceptions import ProjectNotFoundException
from sqlalchemy.orm.exc import NoResultFound 


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, project_data: ProjectCreate) -> ProjectResponse:
        team_members: List[UserEntity] = []
        for user in project_data.team_members:
            user_entity = self.db.query(UserEntity).filter(UserEntity.email == user.email).first()
            team_members.append(user_entity)        

        project_leaders: List[UserEntity] = []
        for leader in project_data.project_leaders:
            leaders_entity = self.db.query(UserEntity).filter(UserEntity.email == leader.email).first()
            project_leaders.append(leaders_entity)

        new_project_entity = ProjectEntity.from_model(project_data, team_members, project_leaders)
        self.db.add(new_project_entity)
        self.db.commit()
        self.db.refresh(new_project_entity)  # Refresh to get the ID

        return new_project_entity.to_project_response()

    def update_project(self, project_id: int, project_update: ProjectUpdate,
) -> ProjectResponse:
        try:
            project_entity = self.db.query(ProjectEntity).filter(ProjectEntity.id == project_id).one()
        except NoResultFound:
            raise ProjectNotFoundException(f"Project with id {project_id} not found")


        update_data = project_update.model_dump(exclude_unset=True)

        # Fetch all users from the database
        all_users = {user.email: user for user in self.db.query(UserEntity).all()}

        # Update team_members
        team_members = []
        for user_data in update_data.get("team_members", []):
            user_email = user_data["email"]
            user_entity = all_users[user_email]
            team_members.append(user_entity)

        # Remove users that are no longer in team_members
        users_to_remove = set(project_entity.team_members) - set(team_members)
        for user in users_to_remove:
            project_entity.team_members.remove(user)

        # Update project_leaders
        project_leaders = []
        for user_data in update_data.get("project_leaders", []):
            user_email = user_data["email"]
            user_entity = all_users[user_email]
            project_leaders.append(user_entity)

        # Remove users that are no longer in project_leaders
        users_to_remove = set(project_entity.project_leaders) - set(project_leaders)
        for user in users_to_remove:
            project_entity.project_leaders.remove(user)

        # Update other fields
        for field, value in update_data.items():
            if field not in ["team_members", "project_leaders"]:
                setattr(project_entity, field, value)

        self.db.commit()
        self.db.refresh(project_entity)
        return project_entity.to_project_response()

    def get_project(self, project_id: int) -> ProjectResponse:
        project = self.db.query(ProjectEntity).filter_by(id=project_id).first()
        if not project:
            raise ProjectNotFoundException(f"Project with id {project_id} not found.")
        return project.to_project_response()
    
    def get_all_projects(self) -> List[ProjectResponse]:
        projects = self.db.query(ProjectEntity).all()
        return [project.to_project_response() for project in projects]

    def delete_project(self, project_id: int):
        project_entity = self.db.query(ProjectEntity).filter_by(id=project_id).first()
        if project_entity is None:
            raise ProjectNotFoundException(f"Project with id {project_id} not found")
        self.db.delete(project_entity)
        self.db.commit()
        return project_entity.to_project_response()

