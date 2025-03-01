import logging
from sqlalchemy.orm import Session
from typing import List

from backend.entities.join_request_entity import JoinRequestEntity
from backend.entities.user_entity import UserEntity
from backend.entities.project_entity import ProjectEntity
from backend.models.join_request import JoinRequestCreate, JoinRequestResponse
from .exceptions import (
    UserNotFoundException,
    ProjectNotFoundException,
    JoinRequestNotFoundException,
    JoinRequestAlreadyMadeException,
)

logger = logging.getLogger(__name__)


class JoinRequestService:
    def __init__(self, db: Session):
        self.db = db

    def create_join_request(
        self, join_request_data: JoinRequestCreate
    ) -> JoinRequestResponse:
        user_entity = (
            self.db.query(UserEntity)
            .filter(UserEntity.id == join_request_data.user_id)
            .first()
        )
        if user_entity is None:
            raise UserNotFoundException(join_request_data.user_id)

        project_entity = (
            self.db.query(ProjectEntity)
            .filter(ProjectEntity.id == join_request_data.project_id)
            .first()
        )
        if project_entity is None:
            raise ProjectNotFoundException(int(join_request_data.project_id))

        # Check if a join request already exists for the user and project
        existing_request = (
            self.db.query(JoinRequestEntity)
            .filter(
                JoinRequestEntity.user_id == join_request_data.user_id,
                JoinRequestEntity.project_id == join_request_data.project_id,
            )
            .first()
        )

        if existing_request:
            raise JoinRequestAlreadyMadeException(
                f"User with id {join_request_data.user_id} already made a join request for project with id {join_request_data.project_id}"
            )

        join_request_entity = JoinRequestEntity.from_model(join_request_data)
        self.db.add(join_request_entity)
        self.db.commit()
        self.db.refresh(join_request_entity)
        return join_request_entity.to_join_request_response()

    def get_join_request(self, join_request_id: int) -> JoinRequestResponse:
        join_request_entity = (
            self.db.query(JoinRequestEntity)
            .filter(JoinRequestEntity.id == join_request_id)
            .first()
        )
        if join_request_entity is None:
            raise JoinRequestNotFoundException(
                f"JoinRequest with id {join_request_id} not found"
            )
        return join_request_entity.to_join_request_response()

    def get_join_request_by_project(self, project_id: int) -> List[JoinRequestResponse]:
        project_entity = (
            self.db.query(ProjectEntity).filter(ProjectEntity.id == project_id).first()
        )
        if project_entity is None:
            raise ProjectNotFoundException(int(project_id))
        join_request_entities = (
            self.db.query(JoinRequestEntity)
            .filter(JoinRequestEntity.project_id == project_id)
            .all()
        )
        if not join_request_entities:
            return []
        return [entity.to_join_request_response() for entity in join_request_entities]

    def get_pending_join_requests_by_project(
        self, project_id: int
    ) -> List[JoinRequestResponse]:
        project_entity = (
            self.db.query(ProjectEntity).filter(ProjectEntity.id == project_id).first()
        )
        if project_entity is None:
            raise ProjectNotFoundException(int(project_id))
        join_request_entities = (
            self.db.query(JoinRequestEntity)
            .filter(
                JoinRequestEntity.project_id == project_id,
                JoinRequestEntity.status == 0,
            )
            .all()
        )
        if not join_request_entities:
            return []
        return [entity.to_join_request_response() for entity in join_request_entities]

    def get_join_requests(self) -> List[JoinRequestResponse]:
        join_request_entities = self.db.query(JoinRequestEntity).all()
        return [jr.to_join_request_response() for jr in join_request_entities]

    def delete_join_request(self, user_id: int, project_id: int) -> JoinRequestResponse:
        join_request_entity = (
            self.db.query(JoinRequestEntity)
            .filter(
                JoinRequestEntity.user_id == user_id,
                JoinRequestEntity.project_id == project_id,
            )
            .first()
        )
        if join_request_entity is None:
            raise JoinRequestNotFoundException(
                f"JoinRequest for user {user_id} and project {project_id} not found"
            )
        self.db.delete(join_request_entity)
        self.db.commit()
        return join_request_entity.to_join_request_response()

    def approve_join_request(self, join_request_id: int) -> JoinRequestResponse:
        join_request_entity = (
            self.db.query(JoinRequestEntity)
            .filter(JoinRequestEntity.id == join_request_id)
            .first()
        )
        if join_request_entity is None:
            raise JoinRequestNotFoundException(
                f"JoinRequest with id {join_request_id} not found"
            )

        # Check if the project and user exist
        project_entity = (
            self.db.query(ProjectEntity)
            .filter(ProjectEntity.id == join_request_entity.project_id)
            .first()
        )
        if project_entity is None:
            raise ProjectNotFoundException(int(join_request_entity.project_id))

        # Check if user is already a team member
        if join_request_entity.user not in project_entity.team_members:
            project_entity.team_members.append(join_request_entity.user)

        join_request_entity.status = 1

        self.db.commit()
        return join_request_entity.to_join_request_response()

    def reject_join_request(self, join_request_id: int) -> JoinRequestResponse:
        join_request_entity = (
            self.db.query(JoinRequestEntity)
            .filter(JoinRequestEntity.id == join_request_id)
            .first()
        )
        if join_request_entity is None:
            raise JoinRequestNotFoundException(
                f"JoinRequest with id {join_request_id} not found"
            )
        join_request_entity.status = 2
        self.db.commit()
        return join_request_entity.to_join_request_response()
