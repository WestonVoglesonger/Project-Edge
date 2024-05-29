from typing import Dict, List
from pytest import Session
from sqlalchemy.exc import IntegrityError
from backend.entities.project_entity import ProjectEntity
from backend.entities.user_entity import UserEntity
from backend.models.project import Project, ProjectCreate, ProjectResponse, ProjectUpdate
from backend.models.user import User
from backend.services.exceptions import ProjectNotFoundException  # Adjust the import based on your project structure

class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, project_data: ProjectCreate) -> ProjectResponse:
        current_users: List[UserEntity] = []
        for user in project_data.current_users:
            user_entity = self.db.query(UserEntity).filter(UserEntity.email == user.email).first()
            current_users.append(user_entity)        

        owners: List[UserEntity] = []
        for owner in project_data.owners:
            owner_entity = self.db.query(UserEntity).filter(UserEntity.email == owner.email).first()
            owners.append(owner_entity)

        new_project_entity = ProjectEntity.from_model(project_data, current_users, owners)
        self.db.add(new_project_entity)
        self.db.commit()
        self.db.refresh(new_project_entity)  # Refresh to get the ID

        return new_project_entity.to_project_response()

    def update_project(self, project_id: int, project_data: ProjectUpdate) -> ProjectResponse:
        project_entity = self.db.query(ProjectEntity).filter(ProjectEntity.id == project_id).first()
        
        if not project_entity:
            raise ProjectNotFoundException(f"Project with id {project_id} not found")
        
        update_data = project_data.model_dump(exclude_unset=True)
        
        # Update `current_users` if provided
        if "current_users" in update_data:
            current_users: List[UserEntity] = []
            for user in update_data["current_users"]:
                if isinstance(user, dict):  # Ensure user is a User instance
                    user = User(**user)
                user_entity = self.db.query(UserEntity).filter(UserEntity.email == user.email).first()
                if user_entity:
                    current_users.append(user_entity)
            project_entity.current_users = current_users

        # Update `owners` if provided
        if "owners" in update_data:
            owners: List[UserEntity] = []
            for user in update_data["owners"]:
                if isinstance(user, dict):  # Ensure user is a User instance
                    user = User(**user)
                user_entity = self.db.query(UserEntity).filter(UserEntity.email == user.email).first()
                if user_entity:
                    owners.append(user_entity)
            project_entity.owners = owners

        # Update other fields
        for key, value in update_data.items():
            if key not in ["current_users", "owners"]:
                setattr(project_entity, key, value)

        self.db.commit()
        self.db.refresh(project_entity)
        return project_entity.to_project_response()

    def get_project(self, project_id: int) -> ProjectResponse:
        project = self.db.query(ProjectEntity).filter_by(id=project_id).first()
        if not project:
            raise ProjectNotFoundException(f"Project with id {project_id} not found.")
        return project.to_project_response()

    def delete_project(self, project_id: int):
        project_entity = self.db.query(ProjectEntity).filter_by(id=project_id).first()
        if project_entity is None:
            raise ProjectNotFoundException(f"Project with id {project_id} not found")
        self.db.delete(project_entity)
        self.db.commit()
        return project_entity.to_project_response()

