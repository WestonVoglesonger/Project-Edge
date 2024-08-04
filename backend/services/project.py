import logging
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from backend.entities.project_entity import ProjectEntity
from backend.entities.user_entity import UserEntity
from backend.models.project import ProjectCreate, ProjectResponse, ProjectUpdate
from backend.services.exceptions import ProjectNotFoundException, UnauthorizedException
from backend.models.user import UserResponse

logger = logging.getLogger(__name__)

class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, project_data: ProjectCreate, current_user_id: int) -> ProjectResponse:
        team_members = self._get_user_entities_by_emails(project_data.team_members)
        project_leaders = self._get_user_entities_by_emails(project_data.project_leaders)

        new_project_entity = ProjectEntity.from_model(project_data, team_members, project_leaders)
        new_project_entity.owner_id = current_user_id  # Set the owner of the project
        self.db.add(new_project_entity)
        self.db.commit()
        self.db.refresh(new_project_entity)  # Refresh to get the ID

        return new_project_entity.to_project_response()

    def update_project(self, project_id: int, project_update: ProjectUpdate, current_user_id: int) -> ProjectResponse:
        logger.info(f"Starting update for project with id {project_id}")

        try:
            project_entity = self.db.query(ProjectEntity).filter(ProjectEntity.id == project_id).one()
            logger.info(f"Found project with id {project_id}")
        except NoResultFound:
            logger.error(f"Project with id {project_id} not found")
            raise ProjectNotFoundException(f"Project with id {project_id} not found")

        if project_entity.owner_id != current_user_id:
            raise UnauthorizedException("You do not have permission to update this project")

        update_data = project_update.dict(exclude_unset=True)

        all_users = {user.email: user for user in self.db.query(UserEntity).all()}

        team_members = self._get_user_entities_from_update_data(update_data, "team_members", all_users)
        self._update_user_relationships(project_entity.team_members, team_members)

        project_leaders = self._get_user_entities_from_update_data(update_data, "project_leaders", all_users)
        self._update_user_relationships(project_entity.project_leaders, project_leaders)

        for field, value in update_data.items():
            if field not in ["team_members", "project_leaders"]:
                setattr(project_entity, field, value)

        self.db.commit()
        logger.info(f"Project with id {project_id} successfully updated in the database")

        self.db.refresh(project_entity)
        logger.info(f"Project with id {project_id} refreshed from the database")

        return project_entity.to_project_response()

    def get_project(self, project_id: int) -> ProjectResponse:
        project = self.db.query(ProjectEntity).filter_by(id=project_id).first()
        if not project:
            raise ProjectNotFoundException(f"Project with id {project_id} not found.")
        return project.to_project_response()
    
    def get_all_projects(self) -> List[ProjectResponse]:
        projects = self.db.query(ProjectEntity).all()
        return [project.to_project_response() for project in projects]

    def get_projects_by_user(self, user_id: int) -> List[ProjectResponse]:
        projects = self.db.query(ProjectEntity).filter(ProjectEntity.project_leaders.any(UserEntity.id == user_id)).all()
        return [project.to_project_response() for project in projects]

    def delete_project(self, project_id: int, current_user_id: int):
        project_entity = self.db.query(ProjectEntity).filter_by(id=project_id).first()
        if project_entity is None:
            raise ProjectNotFoundException(f"Project with id {project_id} not found")

        if project_entity.owner_id != current_user_id:
            raise UnauthorizedException("You do not have permission to delete this project")

        self.db.delete(project_entity)
        self.db.commit()
        return project_entity.to_project_response()

    def _get_user_entities_by_emails(self, users: List[UserResponse]) -> List[UserEntity]:
        user_entities = []
        for user in users:
            user_entity = self.db.query(UserEntity).filter(UserEntity.email == user.email).first()
            if user_entity:
                user_entities.append(user_entity)
            else:
                logger.warning(f"User with email {user.email} not found in database")
        return user_entities

    def _get_user_entities_from_update_data(self, update_data: Dict, field: str, all_users: Dict[str, UserEntity]) -> List[UserEntity]:
        user_entities = []
        for user_data in update_data.get(field, []):
            user_email = user_data["email"]
            user_entity = all_users.get(user_email)
            if user_entity:
                user_entities.append(user_entity)
            else:
                logger.warning(f"User with email {user_email} not found in database")
        return user_entities

    def _update_user_relationships(self, current_users: List[UserEntity], new_users: List[UserEntity]):
        users_to_remove = set(current_users) - set(new_users)
        for user in users_to_remove:
            current_users.remove(user)

        users_to_add = set(new_users) - set(current_users)
        for user in users_to_add:
            current_users.append(user)
