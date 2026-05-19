from sqlalchemy.orm import Session
import models
from models import Task
from schemas import TaskCreate
from schemas import TaskCreate
from schemas import TaskCreate, TaskUpdate
from models import User
from auth import hash_password, verify_password, create_access_token

def create_task(db: Session, task, username):

    user = db.query(User).filter(
        User.username == username
    ).first()

    new_task = models.Task(
        title=task.title,
        description=task.description,
        owner_id=user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def get_tasks(db: Session, username):

    user = db.query(User).filter(
        User.username == username
    ).first()

    return db.query(Task).filter(
        Task.owner_id == user.id
    ).all()




def delete_task(db: Session, task_id: int, username: str):

    user = db.query(User).filter(
        User.username == username
    ).first()

    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user.id
    ).first()

    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

def create_user(db: Session, user):
    hashed_pwd = hash_password(user.password)

    new_user = User(
        username=user.username,
        password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }


def login_user(db: Session, user):
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not existing_user:
        return {"error": "Invalid username"}

    if not verify_password(
        user.password,
        existing_user.password
    ):
        return {"error": "Invalid password"}

    access_token = create_access_token(
        data={"sub": existing_user.username}
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }

def update_task_status(db: Session, task_id: int, username: str):

    user = db.query(User).filter(
        User.username == username
    ).first()

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user.id
    ).first()

    if not task:
        return {"error": "Task not found"}

    task.status = "completed"

    db.commit()
    db.refresh(task)

    return task

def update_task(
    db: Session,
    task_id: int,
    updated_task,
    username: str
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user.id
    ).first()

    if not task:
        return {"error": "Task not found"}

    task.title = updated_task.title
    task.description = updated_task.description

    db.commit()
    db.refresh(task)

    return task