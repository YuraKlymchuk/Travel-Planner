import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas


ARTIC_API_URL = "https://api.artic.edu/api/v1/places"


async def validate_and_fetch_artic_place(external_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ARTIC_API_URL}/{external_id}", timeout=5.0)

            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Place with ID {external_id} does not exist in Art Institute of Chicago database."
                )

            response.raise_for_status()

            api_data = response.json()
            place_data = api_data.get("data", {})

            return {
                "external_id": place_data.get("id"),
                "name": place_data.get("title", "Unknown Gallery")
            }

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External API error: {e.response.status_code}"
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Art Institute of Chicago API is currently unreachable."
            )


class PlaceService:
    def __init__(self, db: Session):
        self.db = db

    async def add_place_to_project(self, project_id: int, place: schemas.PlaceImportSchema):
        db_project = crud.get_project(self.db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")

        artic_place_data = await validate_and_fetch_artic_place(place.external_id)

        return crud.add_place_to_project(
            self.db, project_id=project_id, place=place, name=artic_place_data["name"]
        )

    def update_place(self, place_id: int, place: schemas.PlaceUpdateSchema):
        db_place = crud.get_place(self.db, place_id)
        if not db_place:
            raise HTTPException(status_code=404, detail="Place not found")
        return crud.update_place(self.db, place_id=place_id, place=place)

    def get_places_for_project(self, project_id: int):
        db_project = crud.get_project(self.db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        return crud.get_places_for_project(self.db, project_id=project_id)

    def get_place(self, place_id: int):
        db_place = crud.get_place(self.db, place_id)
        if not db_place:
            raise HTTPException(status_code=404, detail="Place not found")
        return db_place


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.place_service = PlaceService(db)

    async def create_project(self, project: schemas.ProjectCreateSchema):
        db_project = crud.create_project(self.db, project)

        for place in project.places:
            await self.place_service.add_place_to_project(db_project.id, place)

        self.db.refresh(db_project)
        return db_project

    def get_project(self, project_id: int):
        db_project = crud.get_project(self.db, project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project

    def get_projects(self, skip: int = 0, limit: int = 100):
        return crud.get_projects(self.db, skip=skip, limit=limit)

    def update_project(self, project_id: int, project: schemas.ProjectUpdateSchema):
        db_project = self.get_project(project_id)
        return crud.update_project(self.db, project_id=db_project.id, project=project)

    def delete_project(self, project_id: int):
        db_project = self.get_project(project_id)
        if any(place.visited for place in db_project.places):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete project with visited places.",
            )
        return crud.delete_project(self.db, project_id=db_project.id)
