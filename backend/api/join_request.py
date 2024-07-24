import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import db_session
from backend.services.join_request import JoinRequestService
from backend.models.join_request import JoinRequestCreate, JoinRequestResponse
from ..services.exceptions import UserNotFoundException, ProjectNotFoundException, JoinRequestNotFoundException

logger = logging.getLogger(__name__)

api = APIRouter(prefix="/api/join_request")
openapi_tags = {
    "name": "JoinRequests",
    "description": "Operations related to join requests.",
}

def get_join_request_service(db: Session = Depends(db_session)) -> JoinRequestService:
    return JoinRequestService(db)

@api.post("", response_model=JoinRequestResponse, tags=["JoinRequests"])
def create_join_request(join_request: JoinRequestCreate, join_request_service: JoinRequestService = Depends(get_join_request_service)):
    try:
        return join_request_service.create_join_request(join_request)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProjectNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/{join_request_id}", response_model=JoinRequestResponse, tags=["JoinRequests"])
def get_join_request(join_request_id: int, join_request_service: JoinRequestService = Depends(get_join_request_service)):
    try:
        return join_request_service.get_join_request(join_request_id)
    except JoinRequestNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("", response_model=List[JoinRequestResponse], tags=["JoinRequests"])
def list_join_requests(join_request_service: JoinRequestService = Depends(get_join_request_service)):
    try:
        return join_request_service.list_join_requests()
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing query: {str(e)}")

@api.delete("/{current_user_id}/{project_id}", response_model=JoinRequestResponse, tags=["JoinRequests"])
def delete_join_request(current_user_id: int, project_id: int, join_request_service: JoinRequestService = Depends(get_join_request_service)):
    try:
        return join_request_service.delete_join_request(current_user_id, project_id)
    except JoinRequestNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))