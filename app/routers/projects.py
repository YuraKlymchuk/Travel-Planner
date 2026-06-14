from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from app import schemas
from app.database import get_db
from app.services import ProjectService
router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProjectSchema)
async def create_project(
        payload: schemas.ProjectCreateSchema,
        db: Session = Depends(get_db)
) -> schemas.ProjectSchema:
    if not (1 <= len(payload.places) <= 10):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A project must contain between 1 and 10 places."
        )

    project_service = ProjectService(db)
    new_project = await project_service.create_project(payload)
    return new_project


@router.get("/", response_model=List[schemas.ProjectSchema])
def list_projects(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> List[schemas.ProjectSchema]:
    project_service = ProjectService(db)
    projects = project_service.get_projects(skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectSchema)
def get_project(
        project_id: int,
        db: Session = Depends(get_db)
) -> schemas.ProjectSchema:
    project_service = ProjectService(db)
    project = project_service.get_project(project_id)
    return project


@router.put("/{project_id}", response_model=schemas.ProjectSchema)
def update_project(
    project_id: int,
    payload: schemas.ProjectUpdateSchema,
    db: Session = Depends(get_db)
) -> schemas.ProjectSchema:
    project_service = ProjectService(db)
    updated_project = project_service.update_project(project_id, payload)
    return updated_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> None:
    project_service = ProjectService(db)
    project_service.delete_project(project_id)
