import logging
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from backend.entities.discussion_entity import DiscussionEntity
from backend.entities.user_entity import UserEntity
from backend.models.discussion import DiscussionCreate, DiscussionResponse, DiscussionUpdate
from backend.services.exceptions import DiscussionNotFoundException, UserNotFoundException

logger = logging.getLogger(__name__)

class DiscussionService:
    def __init__(self, db: Session):
        self.db = db

    def create_discussion(self, discussion_data: DiscussionCreate) -> DiscussionResponse:
        if (self.db.query(UserEntity).filter(UserEntity.id == discussion_data.author_id).count() == 0):
            raise UserNotFoundException(f"User with id {discussion_data.author_id} not found")
        
        new_discussion_entity = DiscussionEntity.from_model(discussion_data)
        self.db.add(new_discussion_entity)
        self.db.commit()
        self.db.refresh(new_discussion_entity)  # Refresh to get the ID

        return new_discussion_entity.to_discussion_response()

    def update_discussion(self, discussion_id: int, discussion_update: DiscussionUpdate) -> DiscussionResponse:
        logger.info(f"Starting update for discussion with id {discussion_id}")

        try:
            discussion_entity = self.db.query(DiscussionEntity).filter(DiscussionEntity.id == discussion_id).one()
            logger.info(f"Found discussion with id {discussion_id}")
        except NoResultFound:
            logger.error(f"Discussion with id {discussion_id} not found")
            raise DiscussionNotFoundException(f"Discussion with id {discussion_id} not found")

        update_data = discussion_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(discussion_entity, field, value)

        self.db.commit()
        logger.info(f"Discussion with id {discussion_id} successfully updated in the database")

        self.db.refresh(discussion_entity)
        logger.info(f"Discussion with id {discussion_id} refreshed from the database")

        return discussion_entity.to_discussion_response()
    
    def get_discussion(self, discussion_id: int) -> DiscussionResponse:
        discussion = self.db.query(DiscussionEntity).filter_by(id=discussion_id).first()
        if not discussion:
            raise DiscussionNotFoundException(f"Discussion with id {discussion_id} not found.")
        return discussion.to_discussion_response()
    
    def get_all_discussions(self) -> List[DiscussionResponse]:
        discussions = self.db.query(DiscussionEntity).all()
        return [discussion.to_discussion_response() for discussion in discussions]

    def delete_discussion(self, discussion_id: int):
        discussion_entity = self.db.query(DiscussionEntity).filter_by(id=discussion_id).first()
        if discussion_entity is None:
            raise DiscussionNotFoundException(f"Discussion with id {discussion_id} not found")
        self.db.delete(discussion_entity)
        self.db.commit()
        return discussion_entity.to_discussion_response()
