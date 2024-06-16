# backend/services/comment.py
import logging
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from backend.entities.comment_entity import CommentEntity
from backend.models.comment import CommentCreate, CommentResponse, CommentUpdate
from backend.services.exceptions import CommentNotFoundException, UserNotFoundException

logger = logging.getLogger(__name__)

class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(self, comment_data: CommentCreate) -> CommentResponse:
        new_comment_entity = CommentEntity.from_model(comment_data)
        self.db.add(new_comment_entity)
        self.db.commit()
        self.db.refresh(new_comment_entity)
        return new_comment_entity.to_comment_response()

    def update_comment(self, comment_id: int, comment_update: CommentUpdate) -> CommentResponse:
        try:
            comment_entity = self.db.query(CommentEntity).filter(CommentEntity.id == comment_id).one()
        except NoResultFound:
            raise CommentNotFoundException(f"Comment with id {comment_id} not found")

        update_data = comment_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(comment_entity, field, value)

        self.db.commit()
        self.db.refresh(comment_entity)
        return comment_entity.to_comment_response()

    def get_comment(self, comment_id: int) -> CommentResponse:
        comment = self.db.query(CommentEntity).filter_by(id=comment_id).first()
        if not comment:
            raise CommentNotFoundException(f"Comment with id {comment_id} not found.")
        return comment.to_comment_response()

    def get_comments_by_post(self, post_id: int) -> List[CommentResponse]:
        comments = self.db.query(CommentEntity).filter_by(post_id=post_id).all()
        return [comment.to_comment_response() for comment in comments]

    def get_comments_by_discussion(self, discussion_id: int) -> List[CommentResponse]:
        comments = self.db.query(CommentEntity).filter_by(discussion_id=discussion_id).all()
        return [comment.to_comment_response() for comment in comments]

    def delete_comment(self, comment_id: int):
        comment_entity = self.db.query(CommentEntity).filter_by(id=comment_id).first()
        if comment_entity is None:
            raise CommentNotFoundException(f"Comment with id {comment_id} not found")
        self.db.delete(comment_entity)
        self.db.commit()
        return comment_entity.to_comment_response()
