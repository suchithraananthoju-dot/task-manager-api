from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate
from schemas import TaskCreate
from schemas import TaskCreate, TaskUpdate
from models import User
from auth import hash_password, verify_password, create_access_token

def create_task(db: Session, task: TaskCreate):
    new_task = Task(
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task": new_task
    }


def get_tasks(db: Session):
    return db.query(Task).all()

def update_task(db: Session, task_id: int, updated_task: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    task.title = updated_task.title
    task.description = updated_task.description
    task.status = updated_task.status

    db.commit()
    db.refresh(task)

    return {
        "message": "Task updated successfully",
        "task": task
    }



def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

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