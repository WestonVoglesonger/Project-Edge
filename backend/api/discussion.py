import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import db_session
from backend.models.discussion import DiscussionCreate, DiscussionUpdate, DiscussionResponse
from backend.services.exceptions import DiscussionNotFoundException, UserNotFoundException
from backend.services.discussion import DiscussionService

logger = logging.getLogger(__name__)

api = APIRouter(prefix="/api/discussions")
openapi_tags = {
    "name": "Discussions",
    "description": "Discussion management operations.",
}

def get_discussion_service(db: Session = Depends(db_session)) -> DiscussionService:
    return DiscussionService(db)

@api.post("", response_model=DiscussionResponse, tags=["Discussions"])
def create_discussion(discussion: DiscussionCreate, discussion_service: DiscussionService = Depends(get_discussion_service)):
    try:
        return discussion_service.create_discussion(discussion)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/{discussion_id}", response_model=DiscussionResponse, tags=["Discussions"])
def read_discussion(discussion_id: int, discussion_service: DiscussionService = Depends(get_discussion_service)):
    try:
        return discussion_service.get_discussion(discussion_id=discussion_id)
    except DiscussionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("", response_model=List[DiscussionResponse], tags=["Discussions"])
def read_discussions(discussion_service: DiscussionService = Depends(get_discussion_service)):
    return discussion_service.get_all_discussions()

@api.get("/user/{author_id}", response_model=List[DiscussionResponse], tags=["Discussions"])
def read_discussions_by_user(author_id: int, discussion_service: DiscussionService = Depends(get_discussion_service)):
    logger.info(f"Retrieving discussions for user with ID: {author_id}")
    try:
        discussions = discussion_service.get_discussions_by_user(author_id=author_id)
        logger.info(f"Retrieved {len(discussions)} discussions for user with ID: {author_id}")
        return discussions
    except Exception as e:
        logger.error(f"Error retrieving discussions for user with ID: {author_id}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@api.put("/{discussion_id}", response_model=DiscussionResponse, tags=["Discussions"])
def update_discussion(discussion_id: int, discussion_update: DiscussionUpdate, discussion_service: DiscussionService = Depends(get_discussion_service)):
    try:
        return discussion_service.update_discussion(discussion_id=discussion_id, discussion_update=discussion_update)
    except DiscussionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{discussion_id}", response_model=DiscussionResponse, tags=["Discussions"])
def delete_discussion(discussion_id: int, discussion_service: DiscussionService = Depends(get_discussion_service)):
    try:
        return discussion_service.delete_discussion(discussion_id=discussion_id)
    except DiscussionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
