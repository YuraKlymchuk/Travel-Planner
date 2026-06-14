from sqlalchemy.orm import Session
from . import models, schemas

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreateSchema):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        start_date=project.start_date,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: schemas.ProjectUpdateSchema):
    db_project = get_project(db, project_id)
    if db_project:
        update_data = project.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

def add_place_to_project(
    db: Session, project_id: int, place: schemas.PlaceImportSchema, name: str
):
    db_place = models.Place(**place.dict(), project_id=project_id, name=name)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


def get_place(db: Session, place_id: int):
    return db.query(models.Place).filter(models.Place.id == place_id).first()


def get_places_for_project(db: Session, project_id: int):
    return db.query(models.Place).filter(models.Place.project_id == project_id).all()


def update_place(db: Session, place_id: int, place: schemas.PlaceUpdateSchema):
    db_place = get_place(db, place_id)
    if db_place:
        update_data = place.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_place, key, value)
        db.commit()
        db.refresh(db_place)
    return db_place
