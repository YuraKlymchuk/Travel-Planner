from fastapi import FastAPI
from app.routers import projects, places
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner API")

app.include_router(projects.router)
app.include_router(places.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Travel Planner API"}
