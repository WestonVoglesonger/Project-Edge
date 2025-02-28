from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.database import db_session
from backend.services.join_request import JoinRequestService
from backend.models.join_request import JoinRequestCreate, JoinRequestResponse
from backend.services.exceptions import UserNotFoundException, ProjectNotFoundException, JoinRequestNotFoundException
from backend.services.auth import get_current_user
from backend.models.user import UserResponse

logger = logging.getLogger(__name__)

api = APIRouter(prefix="/api/join_request")
openapi_tags = {
    "name": "JoinRequests",
    "description": "Operations related to join requests.",
}

def get_join_request_service(db: Session = Depends(db_session)) -> JoinRequestService:
    return JoinRequestService(db)

@api.post("", response_model=JoinRequestResponse, tags=["JoinRequests"])
def create_join_request(join_request: JoinRequestCreate, join_request_service: JoinRequestService = Depends(get_join_request_service), current_user: UserResponse = Depends(get_current_user)):
    try:
        join_request_dict = join_request.model_dump()
        join_request_dict["user_id"] = current_user.id
        return join_request_service.create_join_request(JoinRequestCreate(**join_request_dict))
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProjectNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/{join_request_id}", response_model=JoinRequestResponse, tags=["JoinRequests"])
def get_join_request(join_request_id: int, join_request_service: JoinRequestService = Depends(get_join_request_service), current_user: UserResponse = Depends(get_current_user)):
    try:
        return join_request_service.get_join_request(join_request_id)
    except JoinRequestNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/{project_id}/all", response_model=List[JoinRequestResponse], tags=["JoinRequests"])
def get_join_request_by_project(project_id: int, join_request_service: JoinRequestService = Depends(get_join_request_service), current_user: UserResponse = Depends(get_current_user)):
    try:
        return join_request_service.get_join_request_by_project(project_id)
    except JoinRequestNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("/{project_id}/pending", response_model=List[JoinRequestResponse], tags=["JoinRequests"])
def get_pending_join_requests_by_project(project_id: int, join_request_service: JoinRequestService = Depends(get_join_request_service), current_user: UserResponse = Depends(get_current_user)):
    try:
        return join_request_service.get_pending_join_requests_by_project(project_id)
    except JoinRequestNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.get("", response_model=List[JoinRequestResponse], tags=["JoinRequests"])
def get_join_requests(join_request_service: JoinRequestService = Depends(get_join_request_service), current_user: UserResponse = Depends(get_current_user)):
    try:
        return join_request_service.get_join_requests()
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing query: {str(e)}")

@api.delete("/{current_user_id}/{project_id}", response_model=JoinRequestResponse, tags=["JoinRequests"])
def delete_join_request(current_user_id: int, project_id: int, join_request_service: JoinRequestService = Depends(get_join_request_service), current_user: UserResponse = Depends(get_current_user)):
    try:
        if current_user.id != current_user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        return join_request_service.delete_join_request(current_user_id, project_id)
    except JoinRequestNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.put("/{join_request_id}/approve", response_model=JoinRequestResponse, tags=["JoinRequests"])
def approve_join_request(join_request_id: int, join_request_service: JoinRequestService = Depends(get_join_request_service), current_user: UserResponse = Depends(get_current_user)):
    try:
        return join_request_service.approve_join_request(join_request_id)
    except JoinRequestNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.put("/{join_request_id}/reject", response_model=JoinRequestResponse, tags=["JoinRequests"])
def reject_join_request(join_request_id: int, join_request_service: JoinRequestService = Depends(get_join_request_service), current_user: UserResponse = Depends(get_current_user)):
    try:
        return join_request_service.reject_join_request(join_request_id)
    except JoinRequestNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
