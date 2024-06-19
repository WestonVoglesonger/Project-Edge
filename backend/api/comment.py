# backend/api/comments.py
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

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

@api.post("", response_model=CommentResponse, tags=["Comments"], status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.create_comment(comment)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating comment: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

@api.get("/{comment_id}", response_model=CommentResponse, tags=["Comments"])
def read_comment(comment_id: int, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.get_comment(comment_id=comment_id)
    except CommentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error reading comment: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

@api.get("", response_model=List[CommentResponse], tags=["Comments"])
def read_comments(
    project_id: Optional[int] = Query(None, alias="projectId"), 
    discussion_id: Optional[int] = Query(None, alias="discussionId"),
    parent_id: Optional[int] = Query(None, alias="parentId"), 
    comment_service: CommentService = Depends(get_comment_service)
):
    try:
        if project_id is not None:
            return comment_service.get_comments_by_project(project_id=project_id)
        elif discussion_id is not None:
            return comment_service.get_comments_by_discussion(discussion_id=discussion_id)
        elif project_id is None and discussion_id is None:
            return comment_service.get_comments_by_parent(parent_id=parent_id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="project_id or discussion_id or parent_id must be provided")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

@api.put("/{comment_id}", response_model=CommentResponse, tags=["Comments"])
def update_comment(comment_id: int, comment_update: CommentUpdate, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.update_comment(comment_id=comment_id, comment_update=comment_update)
    except CommentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating comment: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

@api.get("/user/{author_id}", response_model=List[CommentResponse], tags=["Comments"])
def read_comments_by_user(author_id: int, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.get_comments_by_user(author_id=author_id)
    except Exception as e:
        logger.error(f"Error reading comments by user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

@api.delete("/{comment_id}", response_model=CommentResponse, tags=["Comments"])
def delete_comment(comment_id: int, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.delete_comment(comment_id=comment_id)
    except CommentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting comment: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
