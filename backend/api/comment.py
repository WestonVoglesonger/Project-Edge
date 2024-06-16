import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import db_session
from backend.models.comment import CommentCreate, CommentUpdate, CommentResponse
from backend.services.comment import CommentService
from backend.services.exceptions import CommentNotFoundException, UserNotFoundException

logger = logging.getLogger(__name__)

api = APIRouter(prefix="/api/comments")
openapi_tags = {
    "name": "Comments",
    "description": "Comment management operations.",
}

def get_comment_service(db: Session = Depends(db_session)) -> CommentService:
    return CommentService(db)

@api.post("", response_model=CommentResponse, tags=["Comments"])
def create_comment(comment: CommentCreate, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.create_comment(comment)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/{comment_id}", response_model=CommentResponse, tags=["Comments"])
def read_comment(comment_id: int, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.get_comment(comment_id=comment_id)
    except CommentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("", response_model=List[CommentResponse], tags=["Comments"])
def read_comments(post_id: int = None, discussion_id: int = None, comment_service: CommentService = Depends(get_comment_service)):
    try:
        if post_id:
            return comment_service.get_comments_by_post(post_id=post_id)
        elif discussion_id:
            return comment_service.get_comments_by_discussion(discussion_id=discussion_id)
        else:
            raise HTTPException(status_code=400, detail="post_id or discussion_id must be provided")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api.put("/{comment_id}", response_model=CommentResponse, tags=["Comments"])
def update_comment(comment_id: int, comment_update: CommentUpdate, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.update_comment(comment_id=comment_id, comment_update=comment_update)
    except CommentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{comment_id}", response_model=CommentResponse, tags=["Comments"])
def delete_comment(comment_id: int, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.delete_comment(comment_id=comment_id)
    except CommentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
