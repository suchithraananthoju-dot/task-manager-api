from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from auth import verify_token
from fastapi import HTTPException
from auth import get_current_user


import crud
import models
import schemas

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Database Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@app.get("/")
def home():
    return {"message": "Task Manager API is running"}


# Create Task API
@app.post("/tasks")
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return crud.create_task(db, task)


# Get All Tasks API
@app.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return crud.get_tasks(db)

# Update Task API
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return crud.update_task(db, task_id, task)


# Delete Task API
@app.delete("/tasks/{task_id}")
def delete_task(

    
    task_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return crud.delete_task(db, task_id)

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login_user(db, user)