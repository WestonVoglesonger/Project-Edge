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

    def create_project(self, project_data: ProjectCreate) -> ProjectResponse:
        team_members = self._get_user_entities_by_emails(project_data.team_members)
        project_leaders = self._get_user_entities_by_emails(project_data.project_leaders)

        new_project_entity = ProjectEntity.from_model(project_data, team_members, project_leaders)
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

        # Check if the current user is a project leader
        if current_user_id not in [leader.id for leader in project_entity.project_leaders]:
            logger.error(f"User with id {current_user_id} is not authorized to update project with id {project_id}")
            raise UnauthorizedException(f"User with id {current_user_id} is not authorized to update project with id {project_id}")

        update_data = project_update.model_dump(exclude_unset=True)

        # Fetch all users from the database
        all_users = {user.email: user for user in self.db.query(UserEntity).all()}

        # Update team_members
        team_members = []
        for user_data in update_data.get("team_members", []):
            user_email = user_data["email"]
            user_entity = all_users.get(user_email)
            if user_entity:
                team_members.append(user_entity)
            else:
                logger.warning(f"User with email {user_email} not found in database")

        # Remove users that are no longer in team_members
        users_to_remove = set(project_entity.team_members) - set(team_members)
        for user in users_to_remove:
            project_entity.team_members.remove(user)

        # Add new team members
        users_to_add = set(team_members) - set(project_entity.team_members)
        for user in users_to_add:
            project_entity.team_members.append(user)

        # Update project_leaders
        project_leaders = []
        for user_data in update_data.get("project_leaders", []):
            user_email = user_data["email"]
            user_entity = all_users.get(user_email)
            if user_entity:
                project_leaders.append(user_entity)
            else:
                logger.warning(f"User with email {user_email} not found in database")

        # Remove users that are no longer in project_leaders
        users_to_remove = set(project_entity.project_leaders) - set(project_leaders)
        for user in users_to_remove:
            project_entity.project_leaders.remove(user)

        # Add new project leaders
        users_to_add = set(project_leaders) - set(project_entity.project_leaders)
        for user in users_to_add:
            project_entity.project_leaders.append(user)

        # Ensure project leaders are not empty
        if not project_entity.project_leaders:
            logger.error(f"Cannot update project with id {project_id} because it would leave the project without leaders")
            raise ValueError("Project must have at least one leader")

        # Update other fields
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

    def delete_project(self, project_id: int, current_user_id: int) -> ProjectResponse:
        project_entity = self.db.query(ProjectEntity).filter_by(id=project_id).first()
        if project_entity is None:
            raise ProjectNotFoundException(f"Project with id {project_id} not found")
        
        # Check if the current user is one of the project leaders
        if current_user_id not in [leader.id for leader in project_entity.project_leaders]:
            raise UnauthorizedException("You do not have permission to delete this project")
        
        self.db.delete(project_entity)
        self.db.commit()
        return project_entity.to_project_response()

    def leave_project(self, project_id: int, current_user_id: int) -> ProjectResponse:
        project_entity = self.db.query(ProjectEntity).filter_by(id=project_id).first()
        if project_entity is None:
            raise ProjectNotFoundException(f"Project with id {project_id} not found")
        
        # Check if the current user is one of the team members
        if current_user_id not in [member.id for member in project_entity.team_members]:
            raise UnauthorizedException("You are not a member of this project")
        
        project_entity.team_members = [member for member in project_entity.team_members if member.id != current_user_id]
        self.db.commit()
        return project_entity.to_project_response()

    def _get_user_entities_by_emails(self, users: List[UserResponse]) -> List[UserEntity]:
        return [self.db.query(UserEntity).filter(UserEntity.email == user.email).first() for user in users]
