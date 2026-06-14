from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    places = relationship("Place", back_populates="project", cascade="all, delete-orphan")


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    notes = Column(Text)
    visited = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    project = relationship("Project", back_populates="places")
