from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, plants, disease, reminders
from app.services.scheduler import start_scheduler
# from app.config import settings

app = FastAPI(
    title="GreenTwin API",
    description="Backend for GreenTwin: An Intelligent Plant Care Assistant",
    version="0.1.0"
)

# CORS Configuration
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(plants.router)
app.include_router(disease.router)
app.include_router(reminders.router)

from fastapi.staticfiles import StaticFiles
import os

# Create uploads directory if not exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

from app.database import engine, Base
from app.models import plant, user, plant_state, disease_record, reminder, plant_log

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    start_scheduler()

@app.get("/")
def read_root():
    return {"message": "Welcome to GreenTwin API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
