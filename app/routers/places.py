from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db
from app.services import PlaceService

router = APIRouter(tags=["Places"])


@router.post(
    "/projects/{project_id}/places/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PlaceSchema,
)
async def add_place_to_project(
    project_id: int,
    payload: schemas.PlaceImportSchema,
    db: Session = Depends(get_db),
) -> schemas.PlaceSchema:
    place_service = PlaceService(db)
    new_place = await place_service.add_place_to_project(project_id, payload)
    return new_place


@router.get(
    "/projects/{project_id}/places/", response_model=List[schemas.PlaceSchema]
)
def list_places_for_project(
        project_id: int,
        db: Session = Depends(get_db)
) -> List[schemas.PlaceSchema]:
    place_service = PlaceService(db)
    places = place_service.get_places_for_project(project_id)
    return places


@router.get("/places/{place_id}", response_model=schemas.PlaceSchema)
def get_place(place_id: int, db: Session = Depends(get_db)):
    place_service = PlaceService(db)
    place = place_service.get_place(place_id)
    return place


@router.put("/places/{place_id}", response_model=schemas.PlaceSchema)
def update_place(
    place_id: int, payload: schemas.PlaceUpdateSchema, db: Session = Depends(get_db)
) -> schemas.PlaceSchema:
    place_service = PlaceService(db)
    updated_place = place_service.update_place(place_id, payload)
    return updated_place
