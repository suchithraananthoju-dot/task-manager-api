from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging

import crud
import models
import schemas

from auth import get_current_user
from database import SessionLocal, engine


# Create Database Tables
models.Base.metadata.create_all(bind=engine)


# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# FastAPI App
app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="Task Management Backend using FastAPI"
)


# Database Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    logger.error(f"Error occurred: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error"
        }
    )


# Home API
@app.get("/")
def home():

    logger.info("Home API called")

    return {
        "message": "Task Manager API is running"
    }


# Signup API
@app.post("/signup")
def signup(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    logger.info(f"Signup attempt for user: {user.username}")

    return crud.create_user(db, user)


# Login API
@app.post("/login")
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    logger.info(f"Login attempt for user: {user.username}")

    return crud.login_user(db, user)


# Create Task API
@app.post(
    "/tasks",
    response_model=schemas.TaskResponse
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    logger.info(f"Task creation by user: {user}")

    return crud.create_task(
        db,
        task,
        user
    )


# Get Tasks API
@app.get(
    "/tasks",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    logger.info(f"Fetching tasks for user: {user}")

    return crud.get_tasks(
        db,
        user,
        skip,
        limit
    )


# Update Task API
@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    logger.info(f"Updating task {task_id}")

    return crud.update_task(
        db,
        task_id,
        task,
        current_user
    )


# Complete Task API
@app.put(
    "/tasks/{task_id}/complete",
    response_model=schemas.TaskResponse
)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    logger.info(f"Completing task {task_id}")

    return crud.update_task_status(
        db,
        task_id,
        user
    )


# Delete Task API
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    logger.info(f"Deleting task {task_id}")

    return crud.delete_task(
        db,
        task_id,
        current_user
    )


# Search Tasks API
@app.get(
    "/tasks/search",
    response_model=list[schemas.TaskResponse]
)
def search_tasks(
    keyword: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    logger.info(f"Searching tasks with keyword: {keyword}")

    return crud.search_tasks(
        db,
        keyword,
        user
    )


# Filter Tasks API
@app.get(
    "/tasks/filter",
    response_model=list[schemas.TaskResponse]
)
def filter_tasks(
    status: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    logger.info(f"Filtering tasks by status: {status}")

    return crud.filter_tasks(
        db,
        status,
        user
    )