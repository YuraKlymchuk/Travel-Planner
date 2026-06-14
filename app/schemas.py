from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class PlaceBase(BaseModel):
    external_id: int
    notes: Optional[str] = None


class PlaceImportSchema(PlaceBase):
    pass


class PlaceSchema(PlaceBase):
    id: int
    project_id: int
    name: str
    visited: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectCreateSchema(ProjectBase):
    places: List[PlaceImportSchema]


class ProjectUpdateSchema(ProjectBase):
    pass


class ProjectSchema(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    places: List[PlaceSchema] = []

    class Config:
        from_attributes = True


class PlaceUpdateSchema(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None
