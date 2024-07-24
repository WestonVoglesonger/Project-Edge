import logging
from sqlalchemy.orm import Session
from typing import List

from backend.entities.join_request_entity import JoinRequestEntity
from backend.entities.user_entity import UserEntity
from backend.entities.project_entity import ProjectEntity
from backend.models.join_request import JoinRequestCreate, JoinRequestResponse
from .exceptions import UserNotFoundException, ProjectNotFoundException, JoinRequestNotFoundException

logger = logging.getLogger(__name__)

class JoinRequestService:
    def __init__(self, db: Session):
        self.db = db

    def create_join_request(self, join_request_data: JoinRequestCreate) -> JoinRequestResponse:
        user_entity = self.db.query(UserEntity).filter(UserEntity.id == join_request_data.user_id).first()
        if user_entity is None:
            raise UserNotFoundException(f"User with id {join_request_data.user_id} not found")
        
        project_entity = self.db.query(ProjectEntity).filter(ProjectEntity.id == join_request_data.project_id).first()
        if project_entity is None:
            raise ProjectNotFoundException(f"Project with id {join_request_data.project_id} not found")

        join_request_entity = JoinRequestEntity.from_model(
            user_id=join_request_data.user_id,
            project_id=join_request_data.project_id
        )
        self.db.add(join_request_entity)
        self.db.commit()
        self.db.refresh(join_request_entity)
        return join_request_entity.to_join_request_response()

    def get_join_request(self, join_request_id: int) -> JoinRequestResponse:
        join_request_entity = self.db.query(JoinRequestEntity).filter(JoinRequestEntity.id == join_request_id).first()
        if join_request_entity is None:
            raise JoinRequestNotFoundException(f"JoinRequest with id {join_request_id} not found")
        return join_request_entity.to_join_request_response()

    def list_join_requests(self) -> List[JoinRequestResponse]:
        join_request_entities = self.db.query(JoinRequestEntity).all()
        return [jr.to_join_request_response() for jr in join_request_entities]

    def delete_join_request(self, join_request_id: int) -> JoinRequestResponse:
        join_request_entity = self.db.query(JoinRequestEntity).filter(JoinRequestEntity.id == join_request_id).first()
        if join_request_entity is None:
            raise JoinRequestNotFoundException(f"JoinRequest with id {join_request_id} not found")
        self.db.delete(join_request_entity)
        self.db.commit()
        return join_request_entity.to_join_request_response()
