import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import db_session
from backend.models.project import ProjectCreate, ProjectUpdate, ProjectResponse
from backend.services.exceptions import ProjectNotFoundException
from backend.services.project import ProjectService

logger = logging.getLogger(__name__)

api = APIRouter(prefix="/api/projects")
openapi_tags = {
    "name": "Projects",
    "description": "Project management operations.",
}

def get_project_service(db: Session = Depends(db_session)) -> ProjectService:
    return ProjectService(db)

@api.post("", response_model=ProjectResponse, tags=["Projects"])
def create_project(project: ProjectCreate, project_service: ProjectService = Depends(get_project_service)):
    return project_service.create_project(project)

@api.get("/{project_id}", response_model=ProjectResponse, tags=["Projects"])
def read_project(project_id: int, project_service: ProjectService = Depends(get_project_service)):
    try:
        return project_service.get_project(project_id=project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@api.get("", response_model=List[ProjectResponse], tags=["Projects"])
def read_projects(project_service: ProjectService = Depends(get_project_service)):
    return project_service.get_all_projects()

@api.put("/{project_id}", response_model=ProjectResponse, tags=["Projects"])
def update_project(project_id: int, project_update: ProjectUpdate, project_service: ProjectService = Depends(get_project_service)):
    try:
        return project_service.update_project(project_id=project_id, project_update=project_update)
    except ProjectNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{project_id}", response_model=ProjectResponse, tags=["Projects"])
def delete_project(project_id: int, project_service: ProjectService = Depends(get_project_service)):
    try:
        return project_service.delete_project(project_id=project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
